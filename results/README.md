# Results

Measured configuration: Ubuntu 26.04 under WSL2, Python 3.14.4, Bubblewrap 0.11.1.
Measurement: 2026-10-12T08:25:55Z (October 12, 2026, 1:25 a.m. PDT).
Source freeze: `bb5b48bc535b23430ab439e584e2caebf1fb5115`; clean worktree at measurement.

- [Campaign observations](experiment-001.json): 19 request/decision scenarios,
  one audit/coverage check, and one grouped sandbox probe; all 21 passed.
- [Verification record](verification.json): 13 tests passed in ordinary mode and
  the same 13 passed under optimization. These are repeated runs of one suite,
  not independent reproduction or 26 distinct tests.
- `python3 scripts/check_record.py`: verified all 20 source-file hashes against
  the frozen Git objects and matched the campaign report's SHA-256.

Verdict: **BOUNDED_PASS** for this selected suite on this configuration.
`local-*.json` reports are exploratory and ignored by Git.

Interpretation is bounded by [PROTOCOL.md](../docs/PROTOCOL.md). A test pass does
not establish production security or a validated catalog mitigation. The research
article is deferred until results are reviewed.

The results were reviewed for coverage, successful authorized controls, denial
side effects, inherited policy/actual parents, and a fresh compute-only grant in
the disclosure test. The [article draft](../docs/ARTICLE.md) was written afterward.
Hosted CI status is separate from these local measurements.
