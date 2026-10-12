# Run Experiment 001 without changing historical evidence

Use synthetic data only. This is a research lab, not a tool to protect real secrets.
You do not need an AI subscription, API key, model endpoint or Python package install.
On Windows, open your Ubuntu WSL terminal. The measured boundary is Linux.

## Check your tools

```sh
python3 --version
git --version
bwrap --version
```

Python must be 3.10 or newer. If Bubblewrap is absent on Ubuntu, install it using
your usual package-management process (`sudo apt-get install bubblewrap`). The
host must allow unprivileged user namespaces. If that is blocked, the experiment
must fail; do not remove isolation flags or substitute an unsandboxed run.

## Use the measured source in a new folder

```sh
git clone https://github.com/holeyfield33-art/Asi-Research-v2.git asi-experiment-001-reproduce
cd asi-experiment-001-reproduce
git switch --detach bb5b48bc535b23430ab439e584e2caebf1fb5115
git status --short
```

The last command should show nothing. The detached checkout preserves the
recorded source definition in a separate reproduction folder.

## Run and record

```sh
python3 scripts/verify.py
python3 scripts/check_record.py
```

The first command runs 13 tests normally and under optimization, then the
21-check campaign. It creates `results/experiment-001.json` and `verification.json`
in this new checkout. The second verifies source/report hashes. Inspect any
failure; do not change expectations to make it pass.

Success means selected paths passed on your configuration. Timestamps,
references and environments vary. Compare meaningful decisions and limits,
not random identifiers. Another local run is not external independent reproduction.

In the reviewed package, read the invariant/threat matrices, limitations and
publication-readiness report. I-6, I-9 and I-10 are untested. No pass proves
production security, truth, perfect erasure or a real-model defense.
