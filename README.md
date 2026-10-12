# Reference ≠ Authority — Experiment 001

Small, synthetic security-boundary lab for ASI Architecture Note 001. MIT licensed.
This repository contains the implementation, reproducible evidence and a locally
reviewed article draft. Publication remains at the human review gate.

An adversarial scripted planner receives opaque references, not plaintext or
grant secrets. A trusted controller evaluates externally issued, single-use
grants; verifies the exact content snapshot; runs one uppercase operation in a
separate sandbox; and registers its output with inherited policy and the actual
parent commitment. Display requires a separate grant. A successful display is
captured in a trusted synthetic sink, never sent to the planner.

## Run

Linux, Python 3.10+, Bubblewrap and Git are required. Python uses only its standard
library. There is no network use by the lab, no model endpoint, and no credentials.
The host must permit unprivileged user namespaces. On Ubuntu, install `bubblewrap`
using your normal package-management process if it is absent.

```sh
python3 -m unittest discover -s tests -v
python3 -O -m unittest discover -s tests -v
python3 -m lab.run --output results/local-run.json
```

For an authoritative record, start from a clean committed checkout and run
`python3 scripts/verify.py`. It captures both test modes and the campaign, then
`python3 scripts/check_record.py` checks source hashes against Git objects and
the measured report against the verification record.

On Windows, run these commands inside Ubuntu WSL from the repository directory.
There is deliberately no unsandboxed Windows execution fallback. The measured
configuration is Linux inside WSL, not native Windows isolation.

Read [the frozen protocol](docs/PROTOCOL.md), [provenance](PROVENANCE.md), and
[results](results/README.md). A bounded pass applies only to recorded tests under
the stated trusted computing base. It does not validate a production system,
establish truth of content, or demonstrate end-to-end protection against a model.

Start with the [beginner runbook](docs/BEGINNER-RUNBOOK.md), which uses a separate
checkout of the measured revision and preserves historical reports. The
[invariant matrix](docs/INVARIANT-COVERAGE.md), [threat matrix](docs/THREAT-COVERAGE.md),
[limits and negative results](docs/LIMITATIONS.md) and
[publication readiness](docs/PUBLICATION-READINESS.md) distinguish measured paths
from untested conditions. Machine-readable coverage and evidence review are in
`results/coverage.json` and `results/evidence-review.json`.

## Layout

- `lab/control.py`: trusted issuer, registry, Resolver and Representation Gate.
- `lab/identity.py`: commitment to text, parent digests and inherited policy.
- `lab/sandbox.py`: fail-closed process and namespace launcher.
- `lab/public/`: only code made visible inside planner and worker sandboxes.
- `tests/`: boundary, OS probe and deliberately broken verification controls.
- `provenance/`: source revisions and file hashes; no imported Git histories.
- `results/`: versioned observations and explicit untested boundaries.

The controller's authority-selection logic in `lab/run.py` is a **test driver**.
Case labels select predetermined synthetic grants to exercise each boundary.
It is not a production workflow interface, identity system or authorization API.
