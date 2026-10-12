# Experiment 001 — frozen scope and interpretation

Protocol version: 1. Freeze at the implementation commit named in each report.
Changes to code, fixtures or expectations require a new source manifest and run.

## Question and scope

Can an untrusted scripted planner coordinate a protected transformation without
receiving plaintext or selecting its own authority, in a single-machine,
multi-process, one-hop-grant, one-derivation-level model?

Input: the string `synthetic protected canary 7d42`; positive control: uppercase it
inside a designated worker and independently authorize display in the trusted
sink. A second synthetic object supports reference-substitution tests. Random
references and grant tokens are generated per run. Tokens stay in the controller;
reports record grant constraints, not token secrets. Expiry uses monotonic time.

Authority is stored in the trusted controller rather than serialized signed
delegations. A token is a high-entropy internal identifier supplied through a
trusted workflow channel. This tests separation of planner requests and trusted
authority; it does not test cryptographic signatures or distributed issuers.

The content commitment is SHA-256 of compact UTF-8 JSON, sorted object keys, with
fields `schema=asi-representation-v1`, `text`, ordered `parents`, and `policy`.
Text is committed exactly, without Unicode normalization. This is a new local
format, not compatibility with Helios or a general cross-language standard.
Trusted grant issuance pins the digest; a changed object plus changed registry
digest is still denied against that pin. Compromising both issuer and registry
is outside this threat model. Verification and computation use one copied
snapshot; no second resolution takes place after verification.

## Invariants and cases

| Invariant | Selected tests |
| --- | --- |
| T1: reference is not authority | no grant, unknown ref, revoked/expired grant, replay, materialized text/digest/parent/policy substitution |
| T2: planner cannot authorize itself | operation/purpose/destination/reference substitution; extra authority field; malformed requests |
| T3: controlled plaintext | filtered environment, inherited FD canary, host-file and controller-code probes, process-memory and shared-memory paths, host and external networking, file-creation attempts |
| T4: no derived-data laundering | actual parent and protected child after authorized execution; rejected planner/worker lineage and policy fields; malformed worker output |
| T5: compute does not imply disclose | compute grant denied for child display; separate display grant succeeds; denied cases execute no worker and disclose no data |

Audit records contain only sequence and decision. Planner responses contain only
status and an opaque child reference where appropriate. Exceptions and worker
stderr are not echoed to the planner or audit. Worker stdout is intercepted by
the controller, checked for a single exact-schema JSON candidate, then registered.
Worker-output rejection and errors are fault-injection tests, not claims that a
malicious replacement of a trusted worker has been contained.
The test-only `protocol_fault.py` also exercises real pipes with stderr, raw text,
multiple JSON values and oversized output. The controller drains with a timeout
and a combined 16 KiB cap before parsing, rather than buffering unlimited output.
The Resolver never chooses that test-only script.

## OS boundary

Three roles run as distinct processes. Planner and worker use separate Bubblewrap
user/PID/network/IPC/UTS/cgroup namespaces, no capabilities, no host home/data or
controller mounts, no `/proc` or `/dev/shm`, a filtered environment, closed inherited
descriptors, a read-only root and code/system mounts, and only stdin/stdout/stderr
protocol channels. CPU, address-space, file-size, FD and core-dump limits are set.
System binaries/libraries are exposed read-only; this is not a minimal runtime.

The probe is executed with the exact same launch policy as planner and worker.
A live host listener and an inheritable open synthetic file are positive setup
controls for network/FD tests. File creation (not only writing bytes) must fail.
The one output pipe is controlled transport, not a human/external destination.
Planner computation is short-lived and has no durable memory.
Bubblewrap supplies mechanisms; the launch arguments define this lab's policy.
See the [upstream security model](https://github.com/containers/bubblewrap#sandbox-security).

## Result rules

Every selected check must pass. Authorized controls must succeed, preventing a
deny-everything implementation from passing. A constant-hash mutant must break
the campaign's expected denials; this checks that identity tests are falsifiable.
Ordinary tests and optimized-mode tests must both pass. Failed assertions are
reported as failures, never replaced by skips or an unsupported host fallback.

A `BOUNDED_PASS` means the selected cases passed on the recorded configuration.
It is not proof that all possible attacks against T1–T5 are excluded. Untested
boundaries are kept separate: root/kernel compromise, residual memory/swap/page
cache and perfect erasure, side/covert channels, arbitrary malicious replacement
of trusted code, real-model attacks, long-term memory, multi-user identity,
external providers, unrestricted flooding, and semantic truth/provenance.

Record host/Python/Bubblewrap versions, source revision and worktree state, source
file hashes, grant constraints, requests, decisions, and individual observations.
Result reports themselves contain synthetic data only. Review reports and tests
before the article is drafted. No catalog mitigation validation is claimed.
