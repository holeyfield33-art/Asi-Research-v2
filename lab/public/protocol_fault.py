"""Test-only transport fault generator, never selected by the Resolver."""
import json
import sys

request = json.loads(sys.stdin.readline(16384))
mode = request["mode"]
if mode == "stderr":
    print(request["text"], file=sys.stderr)
    print(json.dumps({"text": "candidate"}))
elif mode == "raw":
    print(request["text"])
elif mode == "multiple":
    print('{}\n{}')
elif mode == "oversized":
    print("x" * 100000)
else:
    sys.exit(2)
