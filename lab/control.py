"""Trusted registry, issuer, Resolver and Representation Gate."""
from dataclasses import dataclass
import hmac
import secrets
import time

from .identity import commitment
from .sandbox import execute


@dataclass(frozen=True)
class Grant:
    ref: str
    digest: str
    operation: str
    purpose: str
    destination: str
    expires: float


class Control:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.registry = {}
        self.grants = {}
        self.used = set()
        self.revoked = set()
        self.audit = []
        self.worker_calls = 0
        self.display = []  # trusted synthetic destination; never returned to planner

    def register(self, text, parents=(), policy="protected"):
        ref = secrets.token_hex(24)
        record = {"text": text, "parents": list(parents), "policy": policy}
        self.registry[ref] = {**record, "digest": commitment(**record)}
        return ref

    def issue(self, ref, operation, purpose, destination, lifetime=60):
        if operation not in {"uppercase", "display"} or lifetime <= 0:
            raise ValueError("invalid grant")
        token = secrets.token_hex(32)
        self.grants[token] = Grant(ref, self.registry[ref]["digest"], operation,
                                   purpose, destination, self.clock() + lifetime)
        return token

    def handle(self, request, workflow_token=None):
        # Authenticated authority is supplied by the trusted workflow channel,
        # never by a planner field. The test runner acts as external grant issuer.
        try:
            result = self._handle(request, workflow_token)
        except (ValueError, TypeError, KeyError):
            result = {"status": "denied"}
        self.audit.append({"sequence": len(self.audit) + 1,
                           "decision": result["status"]})
        return result

    def _handle(self, request, token):
        fields = {"ref", "operation", "purpose", "destination"}
        if not isinstance(request, dict) or set(request) != fields:
            raise ValueError("invalid request schema")
        if not all(isinstance(v, str) and len(v) <= 128 for v in request.values()):
            raise ValueError("invalid request fields")
        grant = self.grants.get(token)
        ref = request["ref"]
        if (grant is None or token in self.used or ref in self.revoked or
                grant.expires <= self.clock()):
            raise ValueError("no current authority")
        if any(request[name] != getattr(grant, name) for name in fields):
            raise ValueError("grant mismatch")
        record = self.registry[ref]
        snapshot = {"text": record["text"], "parents": list(record["parents"]),
                    "policy": record["policy"]}
        actual = commitment(**snapshot)
        if not (hmac.compare_digest(actual, record["digest"]) and
                hmac.compare_digest(actual, grant.digest)):
            raise ValueError("materialized identity mismatch")
        self.used.add(token)  # consume before execution; failures cannot replay
        if grant.operation == "uppercase":
            if grant.destination != "worker":
                raise ValueError("invalid computation destination")
            self.worker_calls += 1
            candidate = execute("worker.py", {"text": snapshot["text"]})
            child = self.gate(candidate, [actual], snapshot["policy"])
            return {"status": "computed", "ref": child}
        if grant.operation == "display" and grant.destination == "display":
            self.display.append(snapshot["text"])
            return {"status": "disclosed"}
        raise ValueError("unsupported operation")

    def gate(self, candidate, manifest, policy):
        # Manifest and inherited policy originate in the trusted runtime.
        # The worker is allowed to supply only its candidate text.
        if (not isinstance(candidate, dict) or set(candidate) != {"text"} or
                not isinstance(candidate["text"], str) or
                len(candidate["text"].encode("utf-8")) > 8192):
            raise ValueError("invalid worker output")
        if policy != "protected" or len(manifest) != 1:
            raise ValueError("invalid derivation context")
        return self.register(candidate["text"], manifest, policy)
