"""Verify report-to-Git provenance independently of the current worktree."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
report_path = ROOT / "results/experiment-001.json"
report = json.loads(report_path.read_text())
verification = json.loads((ROOT / "results/verification.json").read_text())
revision = report["source_revision"]
if report["worktree_status"]:
    raise SystemExit("measurement had a dirty worktree")
if revision != verification["source_revision"]:
    raise SystemExit("test and campaign revisions differ")
for path, expected in report["source_sha256"].items():
    content = subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)
    if hashlib.sha256(content).hexdigest() != expected:
        raise SystemExit(f"source digest mismatch: {path}")
if hashlib.sha256(report_path.read_bytes()).hexdigest() != verification["campaign_report_sha256"]:
    raise SystemExit("report digest mismatch")
if not verification["all_pass"] or not report["tested_cases_pass"]:
    raise SystemExit("record contains failures")
print(f"PASS: {len(report['source_sha256'])} source files match Git revision {revision}; report digest matches")
