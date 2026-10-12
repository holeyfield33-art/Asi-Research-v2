# Test-to-invariant coverage

Frozen definitions are copied exactly into `results/coverage.json`. Tested means selected paths only; no complete-invariant guarantee.

| ID | Frozen topic | Outcome | Evidence | Limits |
| --- | --- | --- | --- | --- |
| T1 | Reference is not authority | tested: selected cases passed | no-grant, unknown-ref, revoked, expired, replay, tampered-content, tampered-digest, tampered-policy, tampered-parents, test_identity_positive_control_and_constant_hash_falsification, test_expiry_boundary_and_fresh_grant | Trusted issuance and digest pinning assumed; guessing space, issuer compromise and cross-user identity not tested. |
| T2 | No self-authorization | tested: selected cases passed | substitute-operation, substitute-purpose, substitute-destination, substitute-ref, self-authorize, test_malformed_requests_never_execute | Only fixed request vocabulary and trusted in-process grants; signed/distributed delegation not implemented. |
| T3 | Controlled plaintext | tested: selected cases passed | authorized-compute, sandbox-isolation, audit-channel, test_os_isolation, test_actual_worker_transport_faults_are_bounded_and_sanitized, test_worker_failure_does_not_expose_error_text | Selected process/channel probes only; no residual erasure, covert-channel or compromised trusted-worker claim. |
| T4 | No derived-data laundering | tested: selected cases passed | authorized-compute, lineage-confusion, policy-laundering, tampered-parents, tampered-policy, test_malformed_worker_output_no_registration_and_no_replay, test_snapshot_is_identity_checked_and_used | One derivation level with trusted complete input mediation; semantic causation and external hidden inputs not established. |
| T5 | Compute does not imply disclose | tested: selected cases passed | compute-to-disclose, authorized-display, test_disclosure_requires_distinct_authority_not_just_unused_token, test_deny_everything_fails_authorized_control | Synthetic controller display sink only; external-service release, human observation and revocation after disclosure not tested. |

Evidence: `results/experiment-001.json` and `results/verification.json` at the pinned measurement revision. No selected scientific failure was observed; intentionally broken implementations are falsification controls. I-6, I-9 and I-10 remain untested. See `docs/LIMITATIONS.md`.
