# Reference ≠ Authority: Measuring an AI Agent Data Boundary

**ASI Research v2 — article draft, based on Experiment 001.**

An agent can name protected information and request a transformation without
receiving that information. Experiment 001 implements this separation in a small
synthetic lab and measures selected ways it could fail. The result is a bounded
pass on the recorded Linux configuration: authorized computation succeeds,
unauthorized requests fail, and a separate permission is required for disclosure.
The experiment does not establish production security or protection against a
real language model.

Implementation and evidence: [Asi-Research-v2](https://github.com/holeyfield33-art/Asi-Research-v2),
[frozen implementation](https://github.com/holeyfield33-art/Asi-Research-v2/tree/bb5b48bc535b23430ab439e584e2caebf1fb5115),
[protocol](PROTOCOL.md), [campaign record](../results/experiment-001.json), and
[test record](../results/verification.json).

## The question

AI agent workflows often pass data to the planner as soon as an operation involves
that data. This couples coordination with possession. It can also blur the
distinction between permission to compute and permission to send the result to a
human or external service.

The original ASI Architecture Note 001 proposed a different arrangement: opaque
references for planning, authorization outside the planner, controlled
materialization for execution, and a Representation Gate for derived outputs.
Experiment 001 asks whether these boundaries can be implemented and exercised in
a deliberately narrow process model.

The planner in this experiment is scripted. It actively submits invalid requests,
but it is not a language model and does not search adaptively for new attacks.
This makes the first measurement about the control boundary rather than model
behavior. Future model-driven testing would be a distinct experiment.

## What was built

The lab uses a trusted controller, a separate planner process, and a separate
worker process. The controller registers two synthetic strings. The planner
receives their random references and a minimal workflow view. It receives no
protected plaintext or grant secrets.

A trusted test driver issues narrow grants outside the planner. Each grant pins
the reference and content digest, operation, purpose, destination and expiry.
Grants are single-use and are stored inside the controller. This is an in-process
authority model; the experiment does not implement signed delegations,
distributed issuers or enterprise identity.

The only transformation is uppercase conversion. Before running it, the Resolver
checks the request against the grant and computes a SHA-256 commitment over the
exact copied representation, including its text, parent digests and policy.
Computation uses that same checked snapshot. It does not resolve the reference
again after verification.

The worker returns a candidate through a controlled pipe. The Gate accepts only
the expected output schema, reconstructs the parent from the actual execution
input, preserves the protected policy, and issues a new opaque reference. The
planner learns that a result exists, without receiving its text.

Display is a separate operation requiring a separate grant. The test's display
destination is a synthetic sink inside the trusted controller. It models an
independently authorized release; it is not a test of an external provider or
human-facing application.

## Why materialized identity matters

A correct-looking locator does not establish that the object returned under it
is the intended object. The earlier Materialized Identity Lab demonstrated this
narrow substitution mechanism. Experiment 001 incorporates a new commitment
format into the trusted execution path rather than importing that lab's product
ancestry or Git history.

The campaign changes content, lineage, policy, and the registry digest in separate
cases. In the strongest selected substitution case, both content and the registry
digest change while the original grant remains pinned. The request is denied
before worker execution. This result depends on the issuer's pinned digest being
trusted. It does not survive compromise of both the issuer and the registry.

A separate test mutates the registry after the worker receives its input. The
output still uses the checked snapshot and its original parent commitment. This
tests the implementation's snapshot discipline, not arbitrary concurrent storage
or distributed time-of-check-to-time-of-use behavior.

Content identity does not authenticate a publisher, establish truth, or prove
semantic causation. Here lineage means the dependency recorded by the trusted
runtime for one execution.

## What the tests found

The frozen implementation was measured on October 12, 2026, using Ubuntu 26.04
under WSL2, Python 3.14.4 and Bubblewrap 0.11.1. The campaign recorded 19
request/decision scenarios, an audit/coverage check, and a grouped isolation probe.
All 21 selected checks passed. Thirteen tests passed in ordinary Python, and the
same suite passed under optimization.

| Boundary | Observation in this configuration |
| --- | --- |
| Reference without authority | No-grant and unknown-reference requests were denied without worker execution. |
| Planner-controlled request fields | Changed reference, operation, purpose or destination did not widen authority; extra grant, lineage and policy fields were rejected. |
| Grant lifecycle | Revoked, expired and replayed grants were denied. |
| Materialized identity | Changed content, policy, parents, and content plus registry digest were denied against the pinned grant. |
| Governed derivation | Authorized computation produced the expected uppercase text, actual parent commitment and protected policy. |
| Separate disclosure | A fresh compute-only grant for the child did not authorize display. A separately issued display grant succeeded. |
| Planner and audit channels | Selected planner responses and audit records contained no synthetic protected text. |
| Process isolation | Host-file, controller-code, process-memory-path, inherited-descriptor, network and file-creation probes were blocked by the selected launch policy. |

The isolation probe used the same Bubblewrap arguments as planner and worker.
It included a host-readable synthetic file, an explicitly inheritable open file
descriptor, and a reachable host listener as positive setup controls. The
sandbox received read-only code and system mounts, a filtered environment and
separate namespaces. It had no host data mount, `/proc`, shared-memory directory
or arbitrary writable filesystem path.

Bubblewrap is a mechanism for constructing a sandbox; its protection depends on
the launch policy. This lab records and tests its own policy rather than treating
the presence of Bubblewrap as evidence of isolation. See the
[upstream security model](https://github.com/containers/bubblewrap#sandbox-security).

The tests also checked ways a misleading pass could arise. A deny-everything
controller fails the authorized control. A deliberately constant hash breaks
the campaign's expected identity denials. Real transport fault tests exercised
stderr, raw text, multiple JSON values and oversized output. Those outputs were
rejected without reflecting protected error text. The controller bounds pipe
collection and applies a timeout before accepting an output candidate.

## What remains untested

These observations do not exclude every way to violate the architecture's five
invariants. The trusted controller, worker implementation, operating system and
launch configuration are part of the trusted computing base. Root or kernel
compromise, arbitrary replacement of trusted code, covert channels, residual
memory and perfect erasure were not demonstrated or solved.

The experiment also excludes durable planner memory, real-model end-to-end
attacks, multi-user identity, external-service disclosure and unrestricted
request flooding. The read-only system runtime is not a minimal hardened image.
The reported runs share one host configuration and one scripted suite; they are
not independent reproduction.

## Evidence and next steps

The measured revision is `bb5b48bc535b23430ab439e584e2caebf1fb5115`.
The record includes a clean worktree state, host versions, a manifest of 20 source
file hashes, grant constraints, requests, decisions and individual observations.
A separate checker matched those source hashes to Git objects and matched the
campaign report to its recorded SHA-256. These checks establish record
consistency; they do not turn observations into a universal guarantee.

The repository retains its MIT license and records design and mechanism sources
in [the provenance manifest](../provenance/sources.json). Its original initial
commit is preserved, followed by a focused implementation freeze and a results
and article-draft commit. No upstream histories or K1 experiment artifacts were
imported.

The next useful research steps are independent reproduction, adversarial model
integration under the same frozen boundaries, and targeted expansion into
stateful memory and richer policy. Experiment 001 supplies a reproducible first
measurement: coordination without automatic plaintext possession worked for the
selected workflow, and computation did not automatically grant disclosure.
