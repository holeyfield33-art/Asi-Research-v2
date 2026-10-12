# Experiment 001 publication readiness

Decision: **CONDITIONAL GO for the bounded-results draft; publication is not authorized.**

## Evidence review

The measured implementation remains `bb5b48bc535b23430ab439e584e2caebf1fb5115`.
Its 20 source hashes and report hash verify against immutable Git objects. The
21 selected campaign checks and 13 ordinary/optimized tests are preserved;
their records are not overwritten by documentation changes. A distinct local
review passed 14 evidence-consistency/coverage checks, recorded in
`results/evidence-review.json`. This is not independent external reproduction.

The existing materialized identity lab remains intact at
`2dbcbc3081fa1fdfe52dbbf645910cda68db1f1c`, with recorded upstream extraction
revision `302cd020a3a51fd3a405e0ee8b4c8223b27c22a1`. Its four controls passed in
both modes; exact outputs, dependencies, environment and file hashes are in
`provenance/materialized-controls.json`. Experiment 001 reuses its integrity
principle with an explicit new commitment for text, parents and inherited policy;
the old memory-object schema would not commit this experiment's policy envelope.
No existing code or history was discarded, and the initial MIT commit is preserved.

## Coverage and limits

All five frozen definitions are copied exactly in `results/coverage.json`.
Selected paths for T1–T5 passed; this is not proof of complete invariant enforcement.
Seven of ten implementation threats have selected-path evidence. I-6 residual
plaintext, I-9 sustained availability attacks and I-10 metadata inference remain
untested. Excluded trust compromises and model/stateful/provider boundaries are
explicitly listed. Negative/falsification and pre-freeze development failures are
documented in `docs/LIMITATIONS.md`. K1 contributes no findings to this experiment.

## Publication preparation

The ten-section draft uses the directive's title and required structure. It cites
the original architecture, pinned implementation, campaign and test records,
includes both coverage matrices and explains failures and limits. Beginner
instructions reproduce the measured revision in a separate clean checkout.

The ASI integration is prepared on local branch `research/experiment-001-results`:
distinct ASI-EXPERIMENT-001 route, independent article synchronization, pinned
research links, preserved original architecture text/status, and publication
regressions. The catalog, AAC definitions, incidents, mitigations, sources and
product claims are not changed. ASI-RESEARCH-001's source and synchronization logic
are preserved.

Local ASI type checking, 20 regression tests, strict catalog validation and build
passed. Twenty-four focused desktop/mobile browser checks passed, including
new-article navigation/refresh, coverage rendering, original-note rendering,
existing article navigation and catalog integrity. Opening/threat screenshots
were visually reviewed; mobile tables scroll inside bounded containers without
horizontal page overflow. UI screenshots are publication previews, not experimental
security evidence. The production build retains a non-blocking bundle-size warning.

## Remaining conditions

1. Human review and approval of the actual results, bounds and article.
2. Hosted GitHub CI could not start because of an account billing lock. This
   external blocker remains visible; local tests are not misrepresented as hosted CI.
3. The publisher must retain the bounded/local evidence labels and untested threat
   disclosures. Independent reproduction and real-model testing remain future work.

The directive says: “Stop at the publication review gate.” ASI publication
standards also reserve merge/deploy approval to the human operator. The ASI branch
is held locally; no follow-up conclusion is deployed to the live site.
