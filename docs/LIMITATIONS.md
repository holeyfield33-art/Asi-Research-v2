# Limits, negative controls and development failures

No selected scientific failure was observed in the frozen 21-check campaign.
Seventeen denied requests are expected negative cases, not proof of complete
invariant enforcement. The authorized compute and display controls prevent an
implementation that denies everything from being interpreted as secure.

The constant-hash mutant intentionally accepts a substituted object. The campaign
then fails its expected-denial checks. This is a falsification control, not a pass
for broken verification. Malformed worker schema, stderr, raw/multiple JSON output
and oversized transport are rejected in the recorded test suite. Tests do not
claim arbitrary replacement of the trusted worker is secure.

Before the implementation freeze, a snapshot test failed with `KeyError: 'ref'`:
its mock callback accepted one argument while the worker API passed script and
payload. The callback was corrected before freezing. This development failure is
recorded separately from experimental findings; the old failure did not establish
a broken security invariant. Native Windows Python aliases initially failed to
launch; a real installation was located. The measured boundary runs use Linux
inside WSL, not a native Windows isolation claim.

The host, trusted worker, issuer, controller and launch configuration are trusted.
Grant authentication is an in-process trusted channel, not signatures or enterprise
identity. The Gate's manifest is supplied by trusted mediation. Its lineage is a
runtime dependency record, not semantic proof or truth authentication. One type,
uppercase operation, derivation level and synthetic display sink are measured.

The grouped sandbox probe uses the same launcher as planner and worker. Blocking
the host-process memory pathname without `/proc` is evidence for that selected
access path; it is not an exhaustive shared-kernel attack test. External-network
connection failure is supplemented by denial of a positively reachable live host
listener, not treated as proof from a possibly unreachable internet endpoint alone.

I-6 residual data, I-9 sustained availability attacks and I-10 metadata inference
remain untested. CPU/core/file limits and bounded transport exist but do not prove
erasure, flood resilience or metadata privacy. Root/kernel compromise, malicious
trusted code, external model providers, stateful memory, multi-user identity,
covert/timing channels and revocation of already disclosed information are not
solved. No language model was run, and no mitigation is validated end-to-end.

All executions and this separate evidence-review pass are local. No independent
external reproduction is claimed. GitHub run 38223711858 did not start because the
account was locked due to billing; its infrastructure failure is preserved at
https://github.com/holeyfield33-art/Asi-Research-v2/actions/runs/38223711858.
K1 is a separate investigation and supplies no evidence for Experiment 001.

## Post-freeze implementation corrections

PR review found two portability/capacity issues outside the frozen ASCII campaign.
The sandbox always launched `/usr/bin/python3`, while the campaign originally
recorded only the invoking Python version. The current launcher records the exact
sandbox interpreter path, resolved path and version separately in future reports.
The frozen launcher selected Ubuntu's `/usr/bin/python3`; its saved report records
the invoking Python as 3.14.4 but not the worker version. In the reviewed Ubuntu
environment, both paths currently report 3.14.4. The existing report is not
retroactively rewritten.

The original worker protocol escaped non-ASCII JSON and could deny a valid
Unicode result before the 8 KiB Gate text limit. The current code serializes
Unicode directly and uses a 64 KiB bounded frame, large enough for the worst
JSON escaping of an 8 KiB candidate. Focused tests cover non-ASCII text and
control characters at the Gate limit. These are later implementation fixes,
not new evidence for the frozen 21-check campaign or an expansion of its scope.
