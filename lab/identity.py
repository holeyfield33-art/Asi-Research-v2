"""Versioned, experiment-specific commitment (not the inherited Helios schema)."""
import hashlib
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def commitment(text, parents, policy):
    if not isinstance(text, str) or not all(isinstance(p, str) for p in parents):
        raise ValueError("invalid representation")
    return hashlib.sha256(canonical({"schema": "asi-representation-v1",
                                    "text": text, "parents": list(parents),
                                    "policy": policy})).hexdigest()
