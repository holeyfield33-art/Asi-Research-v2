import copy
import unittest
from unittest.mock import patch

from lab.control import Control
from lab.identity import commitment
from lab.run import campaign, isolation
from lab.sandbox import command, execute


class Boundaries(unittest.TestCase):
    def setUp(self):
        self.now = 100
        self.c = Control(clock=lambda: self.now)
        self.ref = self.c.register("synthetic secret")
        self.token = self.c.issue(self.ref, "uppercase", "test", "worker", lifetime=5)
        self.request = {"ref": self.ref, "operation": "uppercase", "purpose": "test", "destination": "worker"}

    def test_campaign(self):
        events = campaign()
        self.assertEqual(len(events), 20)
        self.assertTrue(all(event["pass"] for event in events), events)

    def test_os_isolation(self):
        self.assertTrue(isolation()["pass"])

    def test_identity_covers_text_lineage_policy(self):
        digest = commitment("a", ["p"], "protected")
        for text, parents, policy in [("b", ["p"], "protected"), ("a", [], "protected"), ("a", ["p"], "public")]:
            self.assertNotEqual(digest, commitment(text, parents, policy))

    def test_expiry_boundary_and_fresh_grant(self):
        self.now = 105
        self.assertEqual(self.c.handle(self.request, self.token), {"status": "denied"})
        token = self.c.issue(self.ref, "uppercase", "test", "worker")
        self.assertEqual(self.c.handle(self.request, token)["status"], "computed")

    def test_malformed_requests_never_execute(self):
        requests = [None, [], {}, {**self.request, "ref": []},
                    {**self.request, "purpose": "x" * 129}, {**self.request, "authority": True}]
        for request in requests:
            self.assertEqual(self.c.handle(request, self.token), {"status": "denied"})
        self.assertEqual(self.c.worker_calls, 0)

    def test_malformed_worker_output_no_registration_and_no_replay(self):
        for candidate in ({"text": "leak", "parents": []}, {"text": "leak", "policy": "public"},
                          {"text": 42}, {"text": "x" * 8193}, "raw plaintext"):
            token = self.c.issue(self.ref, "uppercase", "test", "worker")
            with patch("lab.control.execute", return_value=candidate):
                self.assertEqual(self.c.handle(self.request, token), {"status": "denied"})
                self.assertEqual(len(self.c.registry), 1)
                self.assertEqual(self.c.handle(self.request, token), {"status": "denied"})

    def test_worker_failure_does_not_expose_error_text(self):
        with patch("lab.control.execute", side_effect=ValueError("synthetic secret")):
            self.assertEqual(self.c.handle(self.request, self.token), {"status": "denied"})
        self.assertNotIn("synthetic secret", str(self.c.audit))

    def test_snapshot_is_identity_checked_and_used(self):
        expected = copy.deepcopy(self.c.registry[self.ref])
        def worker(script, payload):
            self.c.registry[self.ref]["text"] = "concurrent substitution"
            self.assertEqual(payload, {"text": expected["text"]})
            return {"text": payload["text"].upper()}
        with patch("lab.control.execute", side_effect=worker):
            response = self.c.handle(self.request, self.token)
        child = self.c.registry[response["ref"]]
        self.assertEqual(child["text"], expected["text"].upper())
        self.assertEqual(child["parents"], [expected["digest"]])

    def test_identity_positive_control_and_constant_hash_falsification(self):
        self.c.registry[self.ref]["text"] = "substitution"
        with patch("lab.control.commitment", return_value=self.c.grants[self.token].digest):
            # Deliberately broken verification admits substitution. The campaign's
            # tampered-content case must detect this mutant as a failed check.
            response = self.c.handle(self.request, self.token)
        self.assertEqual(response["status"], "computed")
        with patch("lab.control.commitment", return_value="0" * 64):
            events = campaign()
        self.assertFalse(all(event["pass"] for event in events))

    def test_no_windows_fallback(self):
        with patch("lab.sandbox.sys.platform", "win32"):
            with self.assertRaises(RuntimeError):
                command("worker.py")

    def test_deny_everything_fails_authorized_control(self):
        with patch.object(Control, "handle", return_value={"status": "denied"}):
            events = campaign()
        self.assertFalse(events[0]["pass"])

    def test_disclosure_requires_distinct_authority_not_just_unused_token(self):
        child = self.c.handle(self.request, self.token)["ref"]
        compute = self.c.issue(child, "uppercase", "test", "worker")
        request = {"ref": child, "operation": "display", "purpose": "test", "destination": "display"}
        self.assertNotIn(compute, self.c.used)
        self.assertEqual(self.c.handle(request, compute), {"status": "denied"})
        self.assertEqual(self.c.display, [])
        display = self.c.issue(child, "display", "test", "display")
        self.assertEqual(self.c.handle(request, display), {"status": "disclosed"})

    def test_actual_worker_transport_faults_are_bounded_and_sanitized(self):
        for mode in ("stderr", "raw", "multiple", "oversized"):
            with self.assertRaises(ValueError) as context:
                execute("protocol_fault.py", {"mode": mode, "text": "synthetic secret"})
            self.assertNotIn("synthetic secret", str(context.exception))


if __name__ == "__main__":
    unittest.main()
