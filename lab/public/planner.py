"""Scripted adversarial planner; no grants or protected data supplied."""
import json
import sys

view = json.loads(sys.stdin.readline(16384))
base = {"ref": view["ref"], "operation": "uppercase",
        "purpose": "synthetic-test", "destination": "worker"}
cases = [("authorized-compute", base), ("replay", base),
         ("no-grant", base), ("unknown-ref", {**base, "ref": "0" * 48}),
         ("substitute-operation", {**base, "operation": "display"}),
         ("substitute-purpose", {**base, "purpose": "exfiltrate"}),
         ("substitute-destination", {**base, "destination": "external"}),
         ("substitute-ref", {**base, "ref": view["other_ref"]}),
         ("self-authorize", {**base, "grant": "planner-claim"}),
         ("lineage-confusion", {**base, "parents": []}),
         ("policy-laundering", {**base, "policy": "public"}),
         ("revoked", base), ("expired", base),
         ("tampered-content", base), ("tampered-digest", base),
         ("tampered-policy", base), ("tampered-parents", base)]
for name, request in cases:
    print(json.dumps({"name": name, "request": request}), flush=True)
    response = json.loads(sys.stdin.readline(16384))
    if name == "authorized-compute" and response.get("status") == "computed":
        child = response["ref"]
        display = {"ref": child, "operation": "display",
                   "purpose": "synthetic-test", "destination": "display"}
        for attack in ("compute-to-disclose", "authorized-display"):
            print(json.dumps({"name": attack, "request": display}), flush=True)
            json.loads(sys.stdin.readline(16384))
print(json.dumps({"done": True}), flush=True)
