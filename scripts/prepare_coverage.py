"""Pin the published definitions; map selected evidence without redefining them."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("asi", type=Path)
args = parser.parse_args()
asi = args.asi.resolve()
source = asi/"src/components/architecture-note-001.tsx"
text = source.read_text(encoding="utf-8")
def extract(name):
    content = text.split(f"const {name} = [", 1)[1].split("] as const;", 1)[0]
    return [json.loads(line.strip().rstrip(",")) for line in content.splitlines() if line.strip().startswith("[")]

invariant_cases = {
"T1": (["no-grant", "unknown-ref", "revoked", "expired", "replay", "tampered-content", "tampered-digest", "tampered-policy", "tampered-parents"], ["test_identity_positive_control_and_constant_hash_falsification", "test_expiry_boundary_and_fresh_grant"], "Trusted issuance and digest pinning assumed; guessing space, issuer compromise and cross-user identity not tested."),
"T2": (["substitute-operation", "substitute-purpose", "substitute-destination", "substitute-ref", "self-authorize"], ["test_malformed_requests_never_execute"], "Only fixed request vocabulary and trusted in-process grants; signed/distributed delegation not implemented."),
"T3": (["authorized-compute", "sandbox-isolation", "audit-channel"], ["test_os_isolation", "test_actual_worker_transport_faults_are_bounded_and_sanitized", "test_worker_failure_does_not_expose_error_text"], "Selected process/channel probes only; no residual erasure, covert-channel or compromised trusted-worker claim."),
"T4": (["authorized-compute", "lineage-confusion", "policy-laundering", "tampered-parents", "tampered-policy"], ["test_malformed_worker_output_no_registration_and_no_replay", "test_snapshot_is_identity_checked_and_used"], "One derivation level with trusted complete input mediation; semantic causation and external hidden inputs not established."),
"T5": (["compute-to-disclose", "authorized-display"], ["test_disclosure_requires_distinct_authority_not_just_unused_token", "test_deny_everything_fails_authorized_control"], "Synthetic controller display sink only; external-service release, human observation and revocation after disclosure not tested.")}
threat_cases = {
"I-1": ("tested", ["unknown-ref", "substitute-ref", "no-grant"], "Only selected unauthorized-use paths; entropy/guessing campaigns and compromised issuance are not evaluated."),
"I-2": ("tested", ["substitute-operation", "substitute-purpose", "substitute-destination", "self-authorize"], "Fixed schema and externally selected synthetic grants; not arbitrary enterprise policy."),
"I-3": ("tested", ["sandbox-isolation"], "Actual host-file/environment/FD/network/file-creation probes; no kernel or shared-kernel covert-channel claim."),
"I-4": ("tested", ["sandbox-isolation", "audit-channel"], "Real pipe faults are in the unit-test record; no arbitrary malicious trusted-code replacement or perfect erasure claim."),
"I-5": ("tested", ["authorized-compute", "lineage-confusion", "policy-laundering"], "Parent/policy enforcement for one registered transformation; complete semantic lineage remains outside scope."),
"I-6": ("untested", [], "No swap/page-cache/accelerator/residual-memory measurement. Core-dump limits are configuration, not proof of erasure."),
"I-7": ("tested", ["sandbox-isolation", "self-authorize"], "Planner cannot access mounted controller storage/environment or claim a grant; other local users/processes and persisted secret storage are outside scope."),
"I-8": ("tested", ["audit-channel"], "Decision-only synthetic audit has no tested payload leakage; timing/history inference and durable audit governance are untested."),
"I-9": ("untested", [], "Resource limits and output caps exist, but no sustained-flood or availability benchmark was performed."),
"I-10": ("untested", [], "Reference/existence/workflow metadata intentionally exposed; no timing, cardinality or structure-inference measurement.")}

record = {"schema": "asi-coverage-v1", "measurement_revision": "bb5b48bc535b23430ab439e584e2caebf1fb5115",
          "architecture_source": {"repository": "agent-security-index", "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=asi, text=True).strip(),
                                  "path": str(source.relative_to(asi)).replace("\\", "/"), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()},
          "status_meaning": "tested means selected paths were measured, not that the complete invariant/threat is proven",
          "invariants": [], "threats": [],
          "out_of_scope": ["kernel/root compromise", "malicious trusted controller/worker replacement", "multi-user identity", "external model providers", "stateful planner memory", "complete semantic causation"]}
for id, title, definition in extract("INVARIANTS"):
    cases, tests, limitation = invariant_cases[id]
    record["invariants"].append({"id": id, "title": title, "definition": definition, "status": "tested",
                                 "outcome": "selected cases passed", "cases": cases, "unit_tests": tests, "limitation": limitation})
for id, title, definition, invariants, severity in extract("THREATS"):
    status, cases, limitation = threat_cases[id]
    record["threats"].append({"id": id, "title": title, "definition": definition, "invariants": invariants,
                              "published_severity": severity, "status": status, "cases": cases,
                              "outcome": "selected paths passed" if status == "tested" else "not measured", "limitation": limitation})
(root/"results/coverage.json").write_text(json.dumps(record, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
for kind, name in (("invariants", "INVARIANT-COVERAGE.md"), ("threats", "THREAT-COVERAGE.md")):
    body = "# "+("Test-to-invariant coverage" if kind == "invariants" else "Implementation-threat coverage")+"\n\n"
    body += "Frozen definitions are copied exactly into `results/coverage.json`. Tested means selected paths only; no complete-invariant guarantee.\n\n"
    body += "| ID | Frozen topic | Outcome | Evidence | Limits |\n| --- | --- | --- | --- | --- |\n"
    for row in record[kind]:
        evidence = ", ".join(row["cases"] + row.get("unit_tests", [])) or "None"
        body += f"| {row['id']} | {row['title']} | {row['status']}: {row['outcome']} | {evidence} | {row['limitation']} |\n"
    body += "\nEvidence: `results/experiment-001.json` and `results/verification.json` at the pinned measurement revision. No selected scientific failure was observed; intentionally broken implementations are falsification controls. I-6, I-9 and I-10 remain untested. See `docs/LIMITATIONS.md`.\n"
    (root/"docs"/name).write_text(body, encoding="utf-8")
print("Pinned five invariant definitions and ten threat assessments")
