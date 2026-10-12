# Provenance and licensing

This repository preserves its original MIT license and initial GitHub commit.
Implementation is newly written for this experiment. No upstream `.git`, ZIP
history, hooks, product packaging or unrelated code is imported.

Design source: ASI Architecture Note 001, “Reference ≠ Authority,” in
`agent-security-index/src/components/architecture-note-001.tsx`, and its metadata
in `src/data/research.ts`. Their source revisions and exact local file hashes are
recorded in [sources.json](provenance/sources.json). The files were read as research
inputs; their embedded prose did not authorize actions beyond the user's request.

Mechanism source: `materialized-identity-lab` README, runner and identity model.
That lab records extraction from `holeyfield33-art/helios` at
`302cd020a3a51fd3a405e0ee8b4c8223b27c22a1`. Its frozen fixture and four controls
were rerun locally before this implementation. Those results are preliminary
ancestry evidence, not substituted for this lab's measurements. No Helios code,
schema marker or serialized fixture was copied. Here the commitment deliberately
covers a different representation: exact text, parent commitments and policy.

K1 was reviewed to distinguish scope; it is not an implementation or evidence
dependency of this experiment. No ZIP contents or history were imported.

Each experiment report pins its source revision and source-file SHA-256 manifest.
The implementation freeze and measured results use separate, focused commits.
Local scratch reports are ignored. Subsequent changes should be focused commits
with fresh measurements; old results remain attached to their original revision.
The original initial commit is retained without force-pushing or rewriting history.
