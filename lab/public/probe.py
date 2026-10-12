"""Adversarial sandbox probe. It receives only synthetic test paths."""
import json
import os
import socket
import sys

request = json.loads(sys.stdin.readline(16384))
observations = {"environment_secret": "ASI_CANARY" in os.environ,
                "pid": os.getpid(), "fds": [], "stdout_open": True}
for fd in range(3, 32):
    try:
        os.fstat(fd)
        observations["fds"].append(fd)
    except OSError:
        pass
for name, path in request["paths"].items():
    try:
        with open(path, "rb") as stream:
            stream.read(1)
        observations[name] = "readable"
    except OSError:
        observations[name] = "blocked"
for path in ("/app/escape.txt", "/tmp/escape.txt", "/escape.txt", "/dev/escape.txt"):
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        observations["write:" + path] = "allowed"
    except OSError:
        observations["write:" + path] = "blocked"
try:
    with socket.socket() as sock:
        sock.settimeout(0.2)
        sock.connect(("127.0.0.1", request["port"]))
    observations["host_network"] = "connected"
except OSError:
    observations["host_network"] = "blocked"
try:
    with socket.socket() as sock:
        sock.settimeout(0.2)
        sock.connect(("1.1.1.1", 443))
    observations["external_network"] = "connected"
except OSError:
    observations["external_network"] = "blocked"
print(json.dumps(observations))
