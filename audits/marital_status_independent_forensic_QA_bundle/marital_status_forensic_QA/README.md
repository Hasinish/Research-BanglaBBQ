# Marital Status — forensic QA artifact bundle (LOCAL ONLY)

Audited source: `Hasinish/Research-BanglaBBQ`, `main` commit `e186b283fa5b184058e2cb395273e9968a893b20`.
Category: `Marital_status`. Exported original JSONL blob SHA: English `5c902dd9956dc6104126a306317e98ed269d8059`; Bengali `f9f6ac2f87d3f53995e7d5db2bc4faca5df7ede0`.

**Scientific verdict: NOT SAFE TO IMPORT.** Files `banglabbq_marital_status_audited_*.jsonl` are separate, locally repaired proposals, not approved canonical GitHub or Google Sheets replacements. Q04–Q10 remain source/construct qualified. No human evaluator participated.

## Core artifacts

- `marital_status_independent_forensic_QA_report.md` — full version-pinned interpretation and test outcomes.
- `marital_status_postfix_QA_report.md` — post-fix outcome and residual blockers.
- `marital_status_issue_ledger.csv` — 5,473 per-record issue entries (not 5,473 independent defect families).
- `marital_status_semantic_anchor_review.csv` — exactly 240 EN+BN paired anchors, with original/audited text, reviewer notes, and AI scores.
- `marital_status_source_evidence_matrix.csv` — 10 themes; 3 DIRECT, 7 PARTIAL.
- `marital_status_variation_diversity_matrix.csv` — all 30 scenario contexts and repeated-predicate risks.
- `marital_status_adversarial_results.json` — 39 executed mutated fixtures, machine and AI targeted probe outcomes.
- `marital_status_independent_validator.py` — stand-alone independent structural/gold/counterfactual checks, not original generator.
- `marital_status_adversarial_suite.py` and `marital_status_adversarial_paired_suite.py` — reproducible temporary mutation runs.
- `marital_status_import_readiness.json` — precise import gates, `eligible_for_import=false`.
- `marital_status_repo_snapshot.json` — exact source paths, SHA-256, blob hashes, memory status.
- `banglabbq_marital_status_audited_english.jsonl` and `banglabbq_marital_status_audited_bengali.jsonl` — separate local candidates (1,440 records each).
- `marital_status_change_manifest.csv` — exactly 1,320 original-to-audited field edits.
- `marital_status_apply_local_repairs.py` — deterministic production of these candidates from frozen GitHub copies.
- `ORIGINAL/` — immutable copies of all seven current main Marital Status bundle source files (including original prior QA report).
- `work/` — actual script outputs, per-row fail files, generator run evidence and audit-generation scripts.
- `SHA256SUMS` — package contents except this file and ZIP.

## Run independently (from this directory)

```bash
python marital_status_independent_validator.py \
  --english ORIGINAL/banglabbq_marital_status_english.jsonl \
  --bengali ORIGINAL/banglabbq_marital_status_bengali.jsonl \
  --manifest ORIGINAL/banglabbq_marital_status_expansion_manifest.json \
  --out work/independent_initial.json \
  --row-failures work/automated_row_failures.csv
```

The original should report **96 semantic row-test failures**; machine structure passes.

```bash
python marital_status_apply_local_repairs.py \
  --english ORIGINAL/banglabbq_marital_status_english.jsonl \
  --bengali ORIGINAL/banglabbq_marital_status_bengali.jsonl \
  --outdir .
python marital_status_independent_validator.py \
  --english banglabbq_marital_status_audited_english.jsonl \
  --bengali banglabbq_marital_status_audited_bengali.jsonl \
  --manifest ORIGINAL/banglabbq_marital_status_expansion_manifest.json \
  --out work/independent_postfix.json \
  --row-failures work/automated_row_failures_postfix.csv
python marital_status_adversarial_suite.py
python marital_status_adversarial_paired_suite.py
python work/verify_reproducibility.py
```

The corrected files pass the independent machine checks with zero detected row-level failures, but no source-completeness or human review certification is implied. Do not run scripts that import into Sheets or push to GitHub; none are included.
