"""Distinct local evidence-review pass. Not independent external reproduction."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root/"scripts/check_record.py")], cwd=root, check=True)
read = lambda path: json.loads((root/path).read_text(encoding="utf-8"))
campaign, verification, coverage = read("results/experiment-001.json"), read("results/verification.json"), read("results/coverage.json")
baseline = read("provenance/materialized-controls.json")
events = {row["case"]: row for row in campaign["events"]}
tests = {node.name for node in ast.walk(ast.parse((root/"tests/test_boundaries.py").read_text())) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")}
checks = {"measured_worktree_clean": not campaign["worktree_status"],
          "all_21_selected_cases_pass": len(events) == 21 and all(e["pass"] for e in events.values()),
          "ordinary_and_optimized_tests_recorded": len(verification["tests"]) == 2 and all(r["returncode"] == 0 and "Ran 13 tests" in r["stderr"] for r in verification["tests"]),
          "materialized_controls_recorded": baseline["all_pass"] and len(baseline["controls"]) == 4,
          "five_invariants": [r["id"] for r in coverage["invariants"]] == [f"T{i}" for i in range(1, 6)],
          "ten_threats": [r["id"] for r in coverage["threats"]] == [f"I-{i}" for i in range(1, 11)],
          "matrix_case_and_test_ids_resolve": all(all(c in events for c in r["cases"]) and all(t in tests for t in r.get("unit_tests", [])) for r in coverage["invariants"]+coverage["threats"]),
          "authorized_compute_and_display": events["authorized-compute"]["decision"]["status"] == "computed" and events["authorized-display"]["decision"]["status"] == "disclosed",
          "fresh_child_compute_grant_does_not_disclose": events["compute-to-disclose"]["grant"]["operation"] == "uppercase" and events["compute-to-disclose"]["grant"]["ref"] == events["compute-to-disclose"]["request"]["ref"] and events["compute-to-disclose"]["decision"]["status"] == "denied",
          "denial_side_effect_checks": all(e["checks"].get("no_worker_execution") and e["checks"].get("no_disclosure") for e in events.values() if e.get("decision", {}).get("status") == "denied"),
          "actual_parent_and_protected_child": events["authorized-compute"]["checks"]["actual_parent"] and events["authorized-compute"]["checks"]["protected_child"],
          "isolation_positive_controls_and_observations": all(events["sandbox-isolation"]["checks"].values()),
          "untested_threats_explicit": {r["id"] for r in coverage["threats"] if r["status"] == "untested"} == {"I-6", "I-9", "I-10"},
          "initial_MIT_commit_preserved": subprocess.run(["git", "merge-base", "--is-ancestor", "50e17f7c0a039e383744d1f1dfc3af50688f3b3c", "HEAD"], cwd=root).returncode == 0}
record = {"schema": "asi-evidence-review-v1", "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "review_kind": "distinct local verification pass by the coding agent; not independent reproduction",
          "measurement_revision": campaign["source_revision"], "checks": checks,
          "evidence_hash_basis": "UTF-8 text with CRLF normalized to LF; frozen campaign raw hash remains independently checked",
          "evidence_sha256": {path: hashlib.sha256((root/path).read_text(encoding="utf-8").encode("utf-8")).hexdigest() for path in ("results/experiment-001.json", "results/verification.json", "results/coverage.json", "provenance/materialized-controls.json")},
          "bounded_evidence_review_pass": all(checks.values()),
          "readiness": "CONDITIONAL GO" if all(checks.values()) else "NO-GO",
          "conditions": ["human publication review and approval", "state all measured/untested limits in article", "hosted CI could not start due to account billing lock; local results do not replace independent reproduction"],
          "publication_authorized": False}
(root/"results/evidence-review.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"readiness": record["readiness"], "review_checks": len(checks), "all_pass": all(checks.values())}))
raise SystemExit(0 if all(checks.values()) else 1)
