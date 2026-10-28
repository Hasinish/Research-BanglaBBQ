# Research Log: Final Three-Category Production Expansion (Health Status, Marital Status, Occupational Background)

**Date**: 2026-10-28  
**Author / Collective**: Antigravity Benchmark Release Engineering & QA Specialist Collective  
**Categories**: Health Status, Marital Status, Occupational Background (Modernized 7-Category Subgroup)  
**Milestone**: Integration of independently audited Q11–Q20 bilingual expansions into canonical production datasets and master Google Sheets  
**Status**: `EXPANSION VERIFIED / 100% LIVE PARITY (432,000 CELLS) / ZERO Q01-Q10 BIT DRIFT / CI CERTIFIED`

---

## 1. Executive Summary & Objective

This milestone executed the end-to-end production integration of the three audited Q11–Q20 bilingual expansion candidate packages:
1. **Health Status / Mental Health** (`candidate_bundles/health_mental_q11_q20_review_20261028/`)
2. **Marital Status / Male** (`review_artifacts/marital_male_q11_q20/`)
3. **Occupational Background / Professional** (`review_submissions/occupational_professional_q11_q20_2026-10-28/`)

The integration strictly satisfied all mandatory criteria:
- **Zero Q01–Q10 Mutation**: The initial 1,440-row prefixes in both English and Bengali are 100% bit-for-bit identical to pre-expansion backups.
- **Historical Dataset Immutability**: `Dataset_ BanglaBBQ_Old/` and all five other expanded/repaired categories remained 100% untouched.
- **Expanded Category Scope**: Health Status, Marital Status, and Occupational Background were each expanded from 1,440 to 2,880 records per language (5,760 bilingual rows per category; 17,280 total across the three categories).
- **Invariants Certified**: Sequential `example_id` (0..2879), global category IDs (Health 8300000..8302879, Occupational 8600000..8602879, Marital 8700000..8702879), exact 960/960/960 gold label balance, 720/720/720/720 condition balance, 20 themes × 144 records each, and 120 canonical 24-row permutation blocks.
- **Google Sheets Synchronized**: Appended rows 1442..2881 to all 6 target worksheets in master spreadsheet `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`, achieving 100.0000% bit-for-bit live readback parity across all 432,000 data cells with 0 mismatches.

---

## 2. Input Baseline Audit & Source Lineage

### 2.1 Branch Commit Heads Verified
- `origin/main`: `6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65`
- Health / Mental Review: `origin/review/health-mental-q11-q20-2026-10-28` -> `28e5fa5ef705f3d28b7bb4d3b0e7a8b21fb3849a`
- Marital Male Review: `origin/review/marital-male-q11-q20-20261028-audited` -> `3ed1effae2c67284f6f79f39bddb5f61918a7f77`
- Occupational Professional Review: `origin/review/occupational-professional-q11-q20-20261028` -> `62c115f92483b3d25031082cb4271732f00fbd73`

### 2.2 Integration Branch
Created dedicated integration branch `integrate/final-three-category-expansion` branched directly off `origin/main` (`6967700`).

---

## 3. Pre-Expansion Backup & Immutability Verification

Executed `scripts/backup_pre_expansion_state.py` prior to mutating any local production files or Google Sheets:
- Local JSONLs: saved exact copies of the six pre-expansion 1,440-row production files to `backups/pre_expansion_20261028/local_jsonl/`.
- Pre-expansion SHA-256 baseline hashes recorded in `backups/pre_expansion_20261028/pre_expansion_hashes.json`:
  - `BanglaBBQ_Health_Status_FINAL_english.jsonl`: `89c2a814f389373109f9e2a7054357c7c47167caaaf16d051615137f7284865b`
  - `BanglaBBQ_Health_Status_FINAL_bengali.jsonl`: `7a18f485010038bc1b3902dc5cb37530ba03fd4e15104dc225b37d9cb9adb23f`
  - `BanglaBBQ_MaritalStatus_FINAL_english.jsonl`: `8c723789d477538ac9c7b14c976cb97950fd44e219c7c007e8d46ef28fcb95cf`
  - `BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl`: `96aa85ce20392677d8c192f7494d0762796ab26ddfb33854aefcdfb73a46c588`
  - `BanglaBBQ_Occupational_Background_FINAL_english.jsonl`: `c3c7542dec09163c959e0b19d92f3e363eaf99a998fa146b5202fffc341b72a5`
  - `BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl`: `4f3976f8d5183e0b617bca3b45031f6b71ddc2122e15c14bb9c1618894cd3f23`
- Live Google Sheets: exported rows 1..1441 (header + 1,440 data rows) for all six worksheets to `backups/pre_expansion_20261028/google_sheets/`.

---

## 4. Blockers Resolved Before Importing

### 4.1 Occupational Professional Manifest Reconciliation
- **Reconciliation Audit**: Reconciled `occupational_professional_import_manifest.json` against `occupational_professional_sources.csv` and `occupational_professional_QA_report.md`.
- **Source Verification & Qualification**:
  - `Q12` (Corporate executives): Updated URL to *The Business Standard* essay (Shafiq R Bhuiyan, 2025: `https://www.tbsnews.net/features/pursuit/what-makes-job-respectable-1116616`), classified as `EVIDENCE_QUALIFIED`. Documented as positive prestige bias requiring directional score interpretation.
  - `Q14` (Private-sector commercial professionals vs BCS): Updated URL to North South University MPPG thesis (Mesbah-Ul Islam, 2015: `https://www.northsouth.ac.bd/newassets/files/ppg-research/Thesis_4th_Batch/Mesbah_Preference_of_Applied_Science_or_Engineering_Graduates_for_General_Cadres_in_BCS.pdf`), classified as `EVIDENCE_QUALIFIED` (qualitative perception among job seekers, not representative census).
  - `Q15` (Defense service veterans): Updated URL to WorkSMART BD practitioner article (Ishtiak Ahmed Taher, SHRM-SCP: `https://worksmartbd.com/military-veteran-placement/transition-from-a-military-to-civil-career-a-corporate-perspective/`), classified as `EVIDENCE_QUALIFIED` (documents corporate stereotypes regarding veteran teamwork/rigidity).
  - `Q16` (Academic and scientific researchers): Calibrated scope: Haque & Rahman (2025) explores skilled migration and social recognition of research as professional work; qualitative evidence of prestige gap, not directly measured discrimination. Classified as `EVIDENCE_QUALIFIED`.
- **Blocked Status Cleared**: Updated `blocked_themes_not_ready_for_import` to `[]`, updated package SHA-256 checksums, and verified `occupational_professional_validation.py` passes with 0 errors and 9/9 negative fixtures rejected.

### 4.2 Marital Status Review Artifact Cleanup
- Corrected accidental raw markdown headers (`<PARSED TEXT FOR SHEET: 1 / 1 TABS...>`) in `marital_male_sources.csv` and `marital_male_theme_manifest.csv`.
- Verified deterministic regeneration via `marital_male_generate.py` and validated with `marital_male_validation.py` (PASS, 100% bit-for-bit identical).

---

## 5. Independent Validation of the Six Expansion Append Files

Executed dedicated validator `scripts/validate_expansion_append_files.py`:
- All 6 files structurally validated:
  - Exactly 1,440 rows per file (Q11–Q20, 144 records/theme, 48 records/variation).
  - Sequential `example_id` 1440..2879.
  - Category-specific global IDs: Health 8301440..8302879, Occupational 8601440..8602879, Marital 8701440..8702879.
  - Perfect 480/480/480 label distribution.
  - Full 6-way answer permutations across all 60 canonical 24-row orientation blocks.
  - Disambiguated negative gold intro-positions: exact 180 First / 180 Second (50.0% / 50.0%).
  - Disambiguated target/comparison outcomes: exact 180 Target / 180 Comparison (50.0% / 50.0%).
- Adversarial negative control tests: 9/9 deliberate corruption fixtures rejected for each of the three categories (27/27 rejections across all files).

---

## 6. Canonical Production Dataset Append & Verification

Executed `scripts/append_expansion_to_production.py`:
- Appended lines 1441..2880 to canonical files under `Dataset_BanglaBBQ_New/`:
  - `BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_{english,bengali}.jsonl`
  - `BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_{english,bengali}.jsonl`
  - `BanglaBBQ_OccupationalBackground/BanglaBBQ_Occupational_Background_FINAL_{english,bengali}.jsonl`
- Verification results:
  - **Prefix Immutability**: `new_bytes[:len(orig_bytes)] == orig_bytes` verified 100% bit-for-bit across all 6 production files. Zero Q01–Q10 byte drift.
  - **Expanded Records**: Exactly 2,880 rows per file.
  - **Final Production SHA-256 Hashes**:
    - `BanglaBBQ_Health_Status_FINAL_english.jsonl`: `6815dbeda82730d8a71d676f527bb2494d5af7b483bbf24c7021d3eea714854d`
    - `BanglaBBQ_Health_Status_FINAL_bengali.jsonl`: `e6df073cefcc8cf54c8b5d06ce83d9c9c4e395add677c6174ecaec1b53f4ff51`
    - `BanglaBBQ_MaritalStatus_FINAL_english.jsonl`: `fcdca1459da2fbdfc8e6ecf7228556c10d4eba74add8534bd4be14e97dd2d774`
    - `BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl`: `2926001b415b619b81a48d6487e43daa10ba821ec1c3744010f826655b7561c1`
    - `BanglaBBQ_Occupational_Background_FINAL_english.jsonl`: `a150ce63a5f7ac1adfa5815d6c32ddf9805c4844bd0a80520793925f34026c2a`
    - `BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl`: `6771d8291be08b8e3a587c30d7e2fd9b1cc9d4b083ab9b7163cce5be7b92bba4`

---

## 7. Production Validator Generalization & CI Verification

Updated `scripts/validate_seven_final_categories.py` and `scripts/verify_seven_final_categories_live.py`:
- Replaced hardcoded 1,440-row assertions with category-aware expectations:
  - Expanded categories (Health Status, Marital Status, Occupational Background): expected rows = 2,880, themes = 20, labels = 960/960/960, combos = 720, 24-row blocks = 120.
  - Unexpanded categories (Physical Appearance, Social Status, Regional Affiliation, Ethnicity): expected rows = 1,440, themes = 10, labels = 480/480/480, combos = 360, 24-row blocks = 60.
- Executed `scripts/validate_seven_final_categories.py`:
  - **14/14 files PASSED 100% invariants.**
  - **14,400 unique global IDs tracked with 0 collisions.**

---

## 8. Live Google Sheets Synchronization & 100% Parity Readback

Executed `scripts/append_expansion_to_google_sheets.py` and audited via `scripts/verify_seven_final_categories_live.py`:
- Master Spreadsheet ID: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`
- Target Worksheets:
  - `BanglaBBQ_ENG_HealthStatus` (GID: `577820949`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
  - `BanglaBBQ_BEN_HealthStatus` (GID: `1261981579`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
  - `BanglaBBQ_ENG_MaritalStatus` (GID: `2049623557`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
  - `BanglaBBQ_BEN_MaritalStatus` (GID: `1929463163`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
  - `BanglaBBQ_ENG_OccupationalBackground` (GID: `1499154542`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
  - `BanglaBBQ_BEN_OccupationalBackground` (GID: `934780717`): 2,880 data rows, 43,200 data cells, 100.0000% parity (0 mismatches)
- Total live data cells verified across all 14 worksheets: **432,000 data cells (100.0000% parity, 0 mismatches)**.
- All 10 pre-existing active category tabs verified protected and untouched.

---

## 9. Explicit Research Limitations & Governance Notes

1. **Health Status Somatic Q01–Q10 Positional Shortcut**:
   - The inherited Q01–Q10 somatic health condition records (rows 0..1439) retain their documented positional shortcut (100% first-person negative answer).
   - Per explicit instructions, Q01–Q10 was NOT modified. Appending balanced Q11–Q20 records dilutes the overall category shortcut from 100% to 75%, but the Q01–Q10 prefix defect remains an explicit documented limitation awaiting dedicated surgical repair.
2. **Clinical and Sociological Review Pending**:
   - The psychiatric themes in Health Status Q11–Q20, male marital stigma themes in Marital Status Q11–Q20, and professional prestige themes in Occupational Background Q11–Q20 have undergone strict mechanical and written-entailment QA.
   - External clinical peer review, native dialectal Bengali linguistic editing, and sociological stakeholder validation remain pending.
   - The benchmark is NOT certified as publication-ready or production-frozen.
