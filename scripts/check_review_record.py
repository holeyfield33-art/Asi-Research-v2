"""Read-only integrity check for review artifacts across Windows/Linux checkouts."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
record = json.loads((root/"results/evidence-review.json").read_text(encoding="utf-8"))
if not record.get("evidence_hash_basis", "").startswith("UTF-8 text"):
    raise SystemExit("Missing explicit text hash basis")
for path, expected in record["evidence_sha256"].items():
    normalized = (root/path).read_text(encoding="utf-8")
    actual = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    if actual != expected:
        raise SystemExit(f"review evidence digest mismatch: {path}")
if not all(record["checks"].values()) or record["publication_authorized"]:
    raise SystemExit("Review checks failed or publication gate changed")
print("PASS: four review evidence hashes match normalized UTF-8/LF text; publication gate remains closed")
