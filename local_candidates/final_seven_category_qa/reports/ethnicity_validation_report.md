# Category Validation Report — Ethnicity

**Validation Status**: `STRUCTURALLY VALIDATED`

- **Total Invariants Tested**: 13
- **Pass Count**: 13
- **Fail Count**: 0

## Test Results by Invariant Gate

| Gate # | Invariant Description | Status | Details |
| :---: | :--- | :---: | :--- |
| 1 | Total record count (1,440 per lang) | `PASS` | EN: 1440, BN: 1440 |
| 2 | 15-column schema preservation | `PASS` | All 15 keys present: True |
| 3 | Contiguous sequential example_id (0..1439) | `PASS` | EN IDs ok: True, BN IDs ok: True |
| 4 | 10 themes with 144 records each | `PASS` | Themes: EN 10, BN 10 |
| 5 | Bilingual 1-to-1 metadata alignment | `PASS` | Mismatches: 0 |
| 6 | Uniform label distribution (480 / 480 / 480) | `PASS` | EN: {2: 480, 0: 480, 1: 480}, BN: {2: 480, 0: 480, 1: 480} |
| 7 | Condition & polarity balance (360 each) | `PASS` | Counts: {('ambig', 'neg'): 360, ('disambig', 'neg'): 360, ('ambig', 'nonneg'): 360, ('disambig', 'nonneg'): 360} |
| 8 | Canonical 4-row block ordering | `PASS` | All 360 blocks match: True |
| 9 | Ambiguous context Unknown grounding | `PASS` | EN ok: True, BN ok: True |
| 10 | Disambiguated context non-Unknown grounding | `PASS` | EN ok: True, BN ok: True |
| 11 | Complete 6-way answer permutations closure | `PASS` | Permutations valid across all 60 blocks: True |
| 12 | Position balance (180 First / 180 Second in Neg and NonNeg) | `PASS` | EN Neg: 180/180, NonNeg: 180/180 | BN Neg: 180/180, NonNeg: 180/180 |
| 13 | Surgical minimal modification (exactly 720 context edits, 0 other diffs) | `PASS` | EN modified: 720, BN modified: 720, Non-context diffs: 0 |

## Candidate Artifact Hashes (SHA-256)

- **English Candidate**: `BanglaBBQ_Ethnicity_FINAL_english.jsonl` -> `29a0849436ce630a035a60bb75d2bccba3acfcbf2bce747bd8cfcdb57a3ef86a`
- **Bengali Candidate**: `BanglaBBQ_Ethnicity_FINAL_bengali.jsonl` -> `1635587e621c5af4e008c40b0753a7e9f2d922d72703d6b4242b37676319d089`
