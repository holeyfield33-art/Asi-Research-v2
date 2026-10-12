# Reference ≠ Authority: Experimental Results from a Controlled Materialization Boundary

## Experiment 001 — Selected deterministic control paths, measured locally

## 1. Research question and prior architecture

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

The published architecture note remains the intellectual starting point, with its historical experiment-pending status preserved. This follow-up is a distinct experimental artifact. K1 is separate and contributes no evidence here.

## 2. Implementation and trust assumptions

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

## 3. Experimental setup and reproducibility

The measured source revision is bb5b48bc535b23430ab439e584e2caebf1fb5115. The frozen run occurred on October 12, 2026, at 08:25:55 UTC on Ubuntu 26.04 under WSL2, Python 3.14.4 and Bubblewrap 0.11.1. Its worktree was clean. This is Linux process isolation on a Windows host, not native Windows isolation.

The protected input is the synthetic string “synthetic protected canary 7d42”; uppercase conversion is the positive control. Random references and tokens vary per run. Tokens remain in the controller, while grant constraints, requests, decisions, observations, host versions and a 20-file source manifest are recorded.

The original materialized identity lab's four controls were rerun in ordinary and optimized mode. Their source/upstream revisions, tracked-file hashes, environment, exact commands and outputs are recorded separately. The dependency is Python's standard library only. That local mechanism evidence is ancestry, not a replacement for Experiment 001 or independent reproduction.

## 4. Five invariants and test methodology

The original T1–T5 definitions are copied exactly into the machine-readable coverage record; this summary does not redefine them. Tested means selected control paths were measured, not that a complete invariant was proven.

| Invariant | Selected tests | Interpretation limit |
| --- | --- | --- |
| T1 — Reference is not authority | no-grant, unknown-ref, revoked, expired, replay, tampered-content, tampered-digest, tampered-policy, tampered-parents | Trusted issuance and digest pinning assumed; guessing space, issuer compromise and cross-user identity not tested. |
| T2 — No self-authorization | substitute-operation, substitute-purpose, substitute-destination, substitute-ref, self-authorize | Only fixed request vocabulary and trusted in-process grants; signed/distributed delegation not implemented. |
| T3 — Controlled plaintext | authorized-compute, sandbox-isolation, audit-channel | Selected process/channel probes only; no residual erasure, covert-channel or compromised trusted-worker claim. |
| T4 — No derived-data laundering | authorized-compute, lineage-confusion, policy-laundering, tampered-parents, tampered-policy | One derivation level with trusted complete input mediation; semantic causation and external hidden inputs not established. |
| T5 — Compute does not imply disclose | compute-to-disclose, authorized-display | Synthetic controller display sink only; external-service release, human observation and revocation after disclosure not tested. |

Authorized compute and display controls reject a deny-everything interpretation. Denied requests must execute no worker and release no display. The disclosure case uses a fresh, unused compute-only grant for the exact child, so it measures authority constraints rather than replay alone.

The grouped sandbox probe uses the identical launcher as planner and worker. Actual host-file, controller-code, process-memory-path, environment, inheritable-FD, live host-listener and file-creation attempts supplement source inspection. Blocking selected paths is not an exhaustive process-isolation proof.

## 5. Actual results and failures

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

Of the 19 request/decision scenarios, two are authorized controls and 17 are expected denials. No selected scientific invariant failure was observed. The constant-hash mutant and deny-everything controller deliberately fail the relevant controls; these negative results are preserved, not relabeled as secure operation.

Before freezing, a snapshot test failed with a missing child reference because its mock callback did not match the two-argument worker API. The callback was corrected before the measured revision. This is a development failure, not a scientific invariant result. Hosted GitHub CI did not start because of an account billing lock; that infrastructure result remains documented separately from local execution.

## 6. Ten implementation-threat assessments

Every published implementation threat is assessed below. Tested means the selected paths passed, with the stated limitations. I-6, I-9 and I-10 remain untested. No selected threat path failed; intentionally broken implementations are falsification controls.

| Threat | Assessment | Remaining boundary |
| --- | --- | --- |
| I-1 — Reference issuance & registry | tested: selected paths passed | Only selected unauthorized-use paths; entropy/guessing campaigns and compromised issuance are not evaluated. |
| I-2 — Resolver request interface | tested: selected paths passed | Fixed schema and externally selected synthetic grants; not arbitrary enterprise policy. |
| I-3 — Process isolation | tested: selected paths passed | Actual host-file/environment/FD/network/file-creation probes; no kernel or shared-kernel covert-channel claim. |
| I-4 — Worker output channels | tested: selected paths passed | Real pipe faults are in the unit-test record; no arbitrary malicious trusted-code replacement or perfect erasure claim. |
| I-5 — Representation Gate | tested: selected paths passed | Parent/policy enforcement for one registered transformation; complete semantic lineage remains outside scope. |
| I-6 — Residual plaintext | untested: not measured | No swap/page-cache/accelerator/residual-memory measurement. Core-dump limits are configuration, not proof of erasure. |
| I-7 — Grant storage | tested: selected paths passed | Planner cannot access mounted controller storage/environment or claim a grant; other local users/processes and persisted secret storage are outside scope. |
| I-8 — Audit history | tested: selected paths passed | Decision-only synthetic audit has no tested payload leakage; timing/history inference and durable audit governance are untested. |
| I-9 — Resolver availability | untested: not measured | Resource limits and output caps exist, but no sustained-flood or availability benchmark was performed. |
| I-10 — Planner-visible metadata | untested: not measured | Reference/existence/workflow metadata intentionally exposed; no timing, cardinality or structure-inference measurement. |

Published severity labels remain provisional priorities, not evidence maturity. Out-of-scope conditions include kernel/root compromise, malicious trusted components, multi-user identity, external providers, durable planner memory and complete semantic causation.

## 7. Observed limitations and unresolved questions

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

The core-dump limit does not prove erasure. Output caps and CPU limits do not measure sustained flood resilience. Visible references and workflow existence are not evidence of metadata privacy. A blocked host-process memory pathname without /proc does not exhaust shared-kernel attacks. External connection denial is supplemented by a positively reachable live host-listener control.

## 8. Interpretation and implications for agent security

The result is narrower than “the architecture is secure.” In this measured workflow, the planner coordinates a protected transformation without receiving plaintext, and compute authority does not automatically authorize disclosure. A checked snapshot and grant-pinned commitment address selected substitution paths; neither content identity nor authorization alone supplies all the required controls.

A distinct local evidence-review pass verified source/report consistency, positive controls, denial side effects, real sandbox observations and coverage. It is not external independent reproduction. The review gives CONDITIONAL GO for a bounded experimental article, subject to human publication review and explicit limits. No incident, AAC mapping, validated mitigation, product claim, novelty proof or production security guarantee follows from these results.

## 9. Reproduction instructions and evidence links

Use a separate checkout of the exact measured revision, preserving historical reports. Linux, Python 3.10+, Git and Bubblewrap are required; Windows users run inside Ubuntu WSL. No AI subscription, API key or model endpoint is needed.

- Clone Asi-Research-v2 and check out bb5b48bc535b23430ab439e584e2caebf1fb5115.
- Run python3 scripts/verify.py to capture ordinary tests, optimized tests and the campaign.
- Run python3 scripts/check_record.py to match report and source hashes.
- Read the beginner runbook, coverage matrices, limitations and evidence review before interpreting a pass.

The [frozen implementation](https://github.com/holeyfield33-art/Asi-Research-v2/tree/bb5b48bc535b23430ab439e584e2caebf1fb5115), [campaign record](https://github.com/holeyfield33-art/Asi-Research-v2/blob/f5e603ee8f10953c8ca38601f7467eb77bf4cb06/results/experiment-001.json), [test record](https://github.com/holeyfield33-art/Asi-Research-v2/blob/f5e603ee8f10953c8ca38601f7467eb77bf4cb06/results/verification.json), and [frozen protocol](https://github.com/holeyfield33-art/Asi-Research-v2/blob/bb5b48bc535b23430ab439e584e2caebf1fb5115/docs/PROTOCOL.md) are immutable evidence links. The [original architecture note](https://index.aletheia-core.com/#/research/reference-not-authority) remains separate.

## 10. Conclusion and future research

Experiment 001 supplies reproducible evidence for selected controlled-materialization paths under explicit trust assumptions. All selected checks passed and authorized controls worked. Untested threats remain visible, and local execution is distinguished from independent reproduction.

Next steps are independent reproduction, adversarial model integration under the same frozen boundaries, and targeted residual, availability and metadata measurements. Stateful or richer-policy extensions require new scope and measured revisions. The results article stays at the human publication review gate; the original architecture note retains its historical status.
