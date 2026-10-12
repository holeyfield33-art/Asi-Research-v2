"""Record the existing four-control lab without copying or modifying its code."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("lab", type=Path)
args = parser.parse_args()
lab = args.lab.resolve()
revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=lab, text=True).strip()
status = subprocess.check_output(["git", "status", "--porcelain"], cwd=lab, text=True).strip()
files = subprocess.check_output(["git", "ls-files"], cwd=lab, text=True).splitlines()
hashes = {name: hashlib.sha256((lab/name).read_bytes()).hexdigest() for name in files}
commands = [[sys.executable, "run.py"], [sys.executable, "-O", "run.py"],
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            [sys.executable, "-O", "-m", "unittest", "discover", "-s", "tests", "-v"]]
runs = []
for command in commands:
    result = subprocess.run(command, cwd=lab, capture_output=True, text=True, timeout=30)
    runs.append({"command": command, "returncode": result.returncode,
                 "stdout": result.stdout, "stderr": result.stderr})
record = {"schema": "asi-materialized-controls-v1", "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "source_revision": revision, "worktree_status": status,
          "upstream_revision": "302cd020a3a51fd3a405e0ee8b4c8223b27c22a1",
          "source_sha256": hashes, "dependencies": "Python standard library only; no network, install or credentials",
          "environment": {"platform": platform.platform(), "python": platform.python_version()},
          "controls": ["test_baseline", "test_identical_substitution_fails", "test_changed_digest_fails", "test_constant_hash_fails"],
          "runs": runs, "all_pass": not status and all(run["returncode"] == 0 for run in runs),
          "interpretation": "Local mechanism execution, not independent reproduction or complete Experiment 001 evidence."}
(root/"provenance/materialized-controls.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"materialized_controls_pass": record["all_pass"], "revision": revision}))
raise SystemExit(0 if record["all_pass"] else 1)
