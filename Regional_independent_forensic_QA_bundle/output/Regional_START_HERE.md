# Regional Affiliation — Independent Forensic QA bundle

Audit of GitHub `main` HEAD `e186b283fa5b184058e2cb395273e9968a893b20` on 2026-10-26.

## START HERE

1. `output/Regional_independent_forensic_QA_report.md` — complete forensic report and precise limitations.
2. `output/Regional_postfix_QA_report.md` — post-fix test results.
3. `output/Regional_issue_ledger.csv` — 1,637 row-addressable flagged entries (16 distinct issue families; repeated flags are NOT independent defects).
4. `output/Regional_semantic_anchor_review.csv` — 240 EN+BN paired anchor cases; mixed AI self-review and explicit-predicate automated checks, NOT independent human judgment.
5. `output/Regional_source_evidence_matrix.csv` — 10 themes, 6 DIRECT/4 PARTIAL, four unresolved source blockers.
6. `output/Regional_adversarial_results.json` and `output/Regional_adversarial_results_on_corrected.json` — 28 executed mutations against original and corrected datasets.
7. `output/banglabbq_regional_audited_english.jsonl`, `output/banglabbq_regional_audited_bengali.jsonl` — LOCAL amended candidates; NEVER remotely imported.
8. `output/Regional_change_manifest.csv` — all 480 individual field changes, and `output/Regional_reproducibility_runlog.md` with executed commands.
9. `original/` — immutable byte-for-byte committed GitHub snapshots; preserve them.
10. `output/Regional_import_readiness.json` — import SAFE=NO.

## Critical caveat

Source-support critical themes Q06/Q08/Q09/Q10 remain BLOCKED FOR EXPERT DECISION. Neither the original nor the audited JSONLs are publication-ready or safe for production import. No real independent native Bengali human review was performed.

Remotely read-only: no GitHub, Google Sheets, or any other external writes.
