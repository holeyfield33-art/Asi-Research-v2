"""Trusted single-operation worker. No imports from the trusted controller."""
import json
import sys

request = json.loads(sys.stdin.readline(65536))
if set(request) != {"text"} or not isinstance(request["text"], str):
    sys.exit(2)
print(json.dumps({"text": request["text"].upper()}, ensure_ascii=False))
