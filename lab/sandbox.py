"""Fail-closed Linux namespace launcher. Windows has no fallback launcher."""
from pathlib import Path
import os
import resource
import select
import shutil
import subprocess
import sys
import time

PUBLIC = Path(__file__).resolve().parent / "public"
SANDBOX_PYTHON = Path("/usr/bin/python3")
# The Gate accepts at most 8 KiB of UTF-8 text. JSON escaping can use six ASCII
# bytes per input byte, so a 64 KiB frame retains a bounded full-size candidate.
MAX_FRAME_BYTES = 65536


def sandbox_python_metadata():
    """Report the interpreter actually mounted and launched inside Bubblewrap."""
    if not SANDBOX_PYTHON.is_file():
        raise RuntimeError("sandbox requires /usr/bin/python3")
    version = subprocess.check_output(
        [str(SANDBOX_PYTHON), "-I", "-c",
         "import platform; print(platform.python_version())"],
        text=True, timeout=5, env={"PATH": "/usr/bin:/bin"}).strip()
    return {"executable": str(SANDBOX_PYTHON),
            "resolved_executable": str(SANDBOX_PYTHON.resolve()),
            "version": version}


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))


def command(script):
    if sys.platform != "linux" or not shutil.which("bwrap"):
        raise RuntimeError("Linux with Bubblewrap is required; no insecure fallback")
    if script not in {"planner.py", "worker.py", "probe.py", "protocol_fault.py"}:
        raise ValueError("unapproved executable")
    if not SANDBOX_PYTHON.is_file():
        raise RuntimeError("sandbox requires /usr/bin/python3")
    args = [shutil.which("bwrap"), "--unshare-all", "--die-with-parent",
            "--new-session", "--clearenv", "--cap-drop", "ALL"]
    for location in ("/usr", "/lib", "/lib64", "/bin"):
        if Path(location).exists():
            args += ["--ro-bind", location, location]
    args += ["--dir", "/dev", "--ro-bind", "/dev/null", "/dev/null",
             "--ro-bind", str(PUBLIC), "/app", "--chdir", "/app",
             "--setenv", "PYTHONDONTWRITEBYTECODE", "1", "--remount-ro", "/",
             "--", str(SANDBOX_PYTHON), "-I", "/app/" + script]
    return args


def launch(script):
    return subprocess.Popen(command(script), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", close_fds=True,
                            preexec_fn=limits, env={"PATH": "/usr/bin:/bin"})


def execute(script, payload):
    import json
    wire = json.dumps(payload, ensure_ascii=False) + "\n"
    if len(wire.encode("utf-8")) > MAX_FRAME_BYTES:
        raise ValueError("sandbox protocol failure")
    proc = launch(script)
    try:
        proc.stdin.write(wire)
        proc.stdin.close()
        buffers = {proc.stdout: bytearray(), proc.stderr: bytearray()}
        open_streams = list(buffers)
        deadline = time.monotonic() + 5
        while open_streams:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("sandbox timeout")
            ready, _, _ = select.select(open_streams, [], [], remaining)
            if not ready:
                raise ValueError("sandbox timeout")
            for stream in ready:
                chunk = os.read(stream.fileno(), 4096)
                if not chunk:
                    open_streams.remove(stream)
                else:
                    buffers[stream].extend(chunk)
                    if sum(len(buf) for buf in buffers.values()) > MAX_FRAME_BYTES:
                        raise ValueError("sandbox protocol failure")
        proc.wait(timeout=max(0.01, deadline - time.monotonic()))
        # Never reflect raw stdout/stderr into audit or planner responses.
        if proc.returncode or buffers[proc.stderr]:
            raise ValueError("sandbox protocol failure")
        try:
            return json.loads(buffers[proc.stdout])
        except (ValueError, TypeError):
            raise ValueError("sandbox protocol failure") from None
    except (BrokenPipeError, subprocess.TimeoutExpired):
        raise ValueError("sandbox protocol failure") from None
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        if not proc.stdin.closed:
            proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()
