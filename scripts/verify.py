"""Record normal/optimized tests plus the frozen campaign; require clean source."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise SystemExit("Commit the source freeze before recording authoritative results")
    runs = []
    for optimized in (False, True):
        command = [sys.executable] + (["-O"] if optimized else [])
        command += ["-m", "unittest", "discover", "-s", "tests", "-v"]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        runs.append({"command": command, "returncode": result.returncode,
                     "stdout": result.stdout, "stderr": result.stderr})
    output = ROOT / "results/experiment-001.json"
    measured = subprocess.run([sys.executable, "-m", "lab.run", "--output", str(output)],
                              cwd=ROOT, capture_output=True, text=True, timeout=120)
    verification = {"schema": "asi-verification-v1",
                    "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                               cwd=ROOT, text=True).strip(),
                    "tests": runs, "campaign_returncode": measured.returncode,
                    "campaign_stdout": measured.stdout, "campaign_stderr": measured.stderr,
                    "campaign_report_sha256": hashlib.sha256(output.read_bytes()).hexdigest() if output.exists() else None,
                    "all_pass": all(run["returncode"] == 0 for run in runs) and measured.returncode == 0}
    (ROOT / "results/verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verification_pass": verification["all_pass"]}))
    return 0 if verification["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
