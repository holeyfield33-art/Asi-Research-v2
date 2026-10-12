# Implementation-threat coverage

Frozen definitions are copied exactly into `results/coverage.json`. Tested means selected paths only; no complete-invariant guarantee.

| ID | Frozen topic | Outcome | Evidence | Limits |
| --- | --- | --- | --- | --- |
| I-1 | Reference issuance & registry | tested: selected paths passed | unknown-ref, substitute-ref, no-grant | Only selected unauthorized-use paths; entropy/guessing campaigns and compromised issuance are not evaluated. |
| I-2 | Resolver request interface | tested: selected paths passed | substitute-operation, substitute-purpose, substitute-destination, self-authorize | Fixed schema and externally selected synthetic grants; not arbitrary enterprise policy. |
| I-3 | Process isolation | tested: selected paths passed | sandbox-isolation | Actual host-file/environment/FD/network/file-creation probes; no kernel or shared-kernel covert-channel claim. |
| I-4 | Worker output channels | tested: selected paths passed | sandbox-isolation, audit-channel | Real pipe faults are in the unit-test record; no arbitrary malicious trusted-code replacement or perfect erasure claim. |
| I-5 | Representation Gate | tested: selected paths passed | authorized-compute, lineage-confusion, policy-laundering | Parent/policy enforcement for one registered transformation; complete semantic lineage remains outside scope. |
| I-6 | Residual plaintext | untested: not measured | None | No swap/page-cache/accelerator/residual-memory measurement. Core-dump limits are configuration, not proof of erasure. |
| I-7 | Grant storage | tested: selected paths passed | sandbox-isolation, self-authorize | Planner cannot access mounted controller storage/environment or claim a grant; other local users/processes and persisted secret storage are outside scope. |
| I-8 | Audit history | tested: selected paths passed | audit-channel | Decision-only synthetic audit has no tested payload leakage; timing/history inference and durable audit governance are untested. |
| I-9 | Resolver availability | untested: not measured | None | Resource limits and output caps exist, but no sustained-flood or availability benchmark was performed. |
| I-10 | Planner-visible metadata | untested: not measured | None | Reference/existence/workflow metadata intentionally exposed; no timing, cardinality or structure-inference measurement. |

Evidence: `results/experiment-001.json` and `results/verification.json` at the pinned measurement revision. No selected scientific failure was observed; intentionally broken implementations are falsification controls. I-6, I-9 and I-10 remain untested. See `docs/LIMITATIONS.md`.
