# state.md — Current Verified Progress Dashboard

**Last Verified Date**: 2026-10-17  
**Last Verified Git Commit**: `a25b61e` (`docs(memory): sync state and history with research logs infrastructure`)  
**Current Milestone**: Age Dataset Translation Repairs (Q19, Q3, Q8, Q10, Q11, Q12) and Cultural Localization Audit  

---

## 1. Benchmark Status Dashboard across All 9 Categories

| Bias Category | English Count | Bengali Count | Status Marker | Current Working Status & Verification Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Politics** | 960 | 960 | `VERIFIED COMPLETE` | **20 themes (Q1–Q20)**, 48 rows/theme, full 6-way answer permutations (3!). 10/10 offline invariants passed. Live Google Sheets synced with 100% bit-for-bit parity. Untouched baseline Q1–Q5 verified. CI workflow active. |
| **Religion** | 960 | 960 | `IN PROGRESS` | **20 themes (Q1–Q20)**, 48 rows/theme, 1,920 total records. Phase 2 promoted to active dataset (`BanglaBBQ_Religion/`) and live sheets. Phase 1 safely archived to `backups/religion_sheets_backup_20261016/`. 10/10 offline checks passed. **Outstanding**: Independent source relevance check, Bengali translation naturalness review, and realistic counterfactual audit. |
| **Age** | 2,920 | 2,920 | `IN PROGRESS` | English source adapted from PakBBQ (`PakBBQ_Age_English.csv`). Bengali working dataset fully translated (2,920 rows) in Google Sheet `BanglaBBQ_BEN_Age` and synchronized to `BanglaBBQ_BEN_New/Age.jsonl`. **100% Unique Context Parity across all 20 themes (Q1–Q20)** achieved: Q1 (16/16), Q3 (36/36), Q8 (100/100), Q9 (144/144), Q10 (168/168), Q11 (84/84), Q12 (84/84), Q19 (140/140). Q19 semantic neighbor mistranslation repaired across 88 rows. 332 total rows repaired across 6 target themes with synchronized answer choices and preserved gold labels. Cultural localization audit completed for TM records Q13–Q20. **Outstanding**: Independent native Bengali linguistic naturalness review. Exemplar rows in `Review_Age_20_Templates` flagged for future update. |
| **Gender Identity** | 506 *(legacy)* | 506 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Gender_identity/` and `BBQ/BanBBQ_.../Gender_identity.jsonl`. Requires category-level forensic audit, permutation expansion, and Google Sheet integration. |
| **Physical Appearance** | 1,106 *(legacy)* | 1,123 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Physical_appearance/` and `P_A_E/`. **Known Defect**: 17-record mismatch between English and Bengali legacy sets. Requires category-level audit, reconciliation, and permutation balancing. |
| **Regional Affiliation** | 51 *(legacy)* | 51 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Regional/`. **Known Defect**: Severely underpowered sample size (only 51 entries). Requires comprehensive expansion across Bangladeshi district stereotypes with source backing. |
| **Educational Background** | 128 *(legacy)* | 128 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Educational background/`. Requires category-level audit, scenario expansion, 6-way answer permutation balancing, and source grounding. |
| **Marital Status** | 100 *(legacy)* | 100 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Marital Status/`. Requires category-level audit, expansion beyond 100 rows, permutation balancing, and cultural grounding. |
| **Mental Health** | 100 *(legacy)* | 100 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Mental Health/`. Requires category-level audit, clinical/social scenario expansion, and permutation balancing. |

> **Status Marker Definitions**:
> - `VERIFIED COMPLETE`: Structurally and semantically validated, verified against pre-expansion baselines, synchronized between Google Sheets and GitHub, passing automated CI.
> - `IN PROGRESS`: Dataset expanded and structurally validated; pending secondary linguistic, cultural, or source verification.
> - `PENDING`: Baseline files cataloged; awaiting dedicated category audit and modernization.
> - `UNVERIFIED`: Claim or dataset not yet verified against primary evidence.
> - `BLOCKED`: Work halted due to dependencies or missing external artifacts.

---

## 2. Google Spreadsheet Working Tabs

**Master Spreadsheet ID**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`  
**Master Spreadsheet Link**: [https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)

| Sheet Title | Sheet ID | Tab Index | Active Rows | Description |
| :--- | :---: | :---: | :---: | :--- |
| `Review_Age_20_Templates` | `99887766` | 0 | Header + Samples | Executive 3-column review tab comparing PakBBQ English vs Legacy Thesis vs Hasin's Bengali translations. *(Contains older exemplar rows; do NOT modify without approval).* |
| `PakBBQ_ENG_Age` | `0` | 1 | 2,921 (2,920 data) | Complete English Age benchmark source pool imported from PakBBQ. |
| `BanglaBBQ_BEN_Age` | `1006819770` | 2 | 2,921 (2,920 data) | Complete Bengali Age benchmark updated with Q1 context alignment, Q9 technology alignment, Q19 semantic signer/youth repairs, and Q3, Q8, Q10, Q11, Q12 lexical distinctions. 100% unique context parity with English. |
| `BanglaBBQ_ENG_Politics` | `1888499205` | 3 | 961 (960 data) | Active English Politics benchmark across 20 source-backed themes (Q1–Q20). |
| `BanglaBBQ_BEN_Politics` | `2128232344` | 4 | 961 (960 data) | Active Bengali Politics benchmark with aligned `answer_info` and repaired administrative terms. |
| `BanglaBBQ_ENG_Religion` | `804112545` | 5 | 961 (960 data) | Active English Religion benchmark across 20 themes (formerly Phase 2, promoted after backup). |
| `BanglaBBQ_BEN_Religion` | `860941009` | 6 | 961 (960 data) | Active Bengali Religion benchmark across 20 themes (formerly Phase 2, promoted after backup). |

*Note: Worksheets for the remaining 6 categories will be created systematically as each category undergoes its dedicated audit and expansion.*

---

## 3. Active GitHub Dataset Directories

| Category | Canonical Directory | Primary Files | Record Count |
| :--- | :--- | :--- | :---: |
| **Politics** | [`BanglaBBQ_Politics/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics) | `banglabbq_politics_english.jsonl`<br/>`banglabbq_politics_bengali.jsonl` | 960 ENG<br/>960 BEN |
| **Religion** | [`BanglaBBQ_Religion/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion) | `Religion_eng.jsonl`<br/>`Religion_bng.jsonl` | 960 ENG<br/>960 BEN |
| **Age** | [`BanglaBBQ_BEN_New/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New)<br/>Root | `Age.jsonl`<br/>`PakBBQ_Age_English.csv` | 2,920 BEN<br/>2,920 ENG |

---

## 4. Completed Work

- [x] Cloned and integrated official PakBBQ repository baseline (`PakBBQ_Repo`).
- [x] Generated Excel-ready CSV for Age (`PakBBQ_Age_English.csv`, 2,920 rows).
- [x] Created 3-column comparative review tab `Review_Age_20_Templates` in master Google Sheet.
- [x] Translated all 2,920 Age rows to conversational Bengali in Google Sheet `BanglaBBQ_BEN_Age` and exported to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Corrected Bengali family terms (Grandma/Grandpa -> নানা/নানি, Grandparent/Grandchild -> দাদু/নাতিটি) and Q7 comparative formulation.
- [x] Synchronized live Google Sheets updates for Age Q1 (IDs 0–31) context diversity (expanded from 11 to 16 unique contexts) to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Synchronized live Google Sheets updates for Age Q9 (IDs 912–1199) context diversity (expanded from 60 to 144 unique contexts) and aligned 272 answer choices in columns H–J to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Repaired semantic mistranslation in Age Q19 (IDs 2360–2639) correcting 88 disambiguated rows where neighbor was incorrectly substituted for friend (48 rows) and someone else (40 rows).
- [x] Resolved lexical youth collapses in Age Q19 and Q8 distinguishing "The teen" (`কিশোরটি`) and "The teenager" (`কিশোরবয়সী ছেলেটি`).
- [x] Resolved lexical collapses in Age Q3 distinguishing "The Zoomer" (`জেন-জি প্রফেসর`) and "The Gen-Z kid" (`জেন-জি তরুণ প্রফেসর`).
- [x] Resolved lexical collapses in Age Q10, Q11, and Q12 distinguishing "The high schooler" (`স্কুলপড়ুয়া শিক্ষার্থীটি`) and "The high school student" (`হাই স্কুলের শিক্ষার্থীটি`).
- [x] Realigned "fights" (`মারামারিতে জড়ান/জড়ায় না`) vs. "confrontations" (`কারো সাথে ঝামেলায় জড়ান/জড়ায় না`) in Age Q11 and Q12 disambiguated contexts.
- [x] Achieved 100% unique context parity between English and Bengali across ALL 20 Age themes (Q1–Q20) with 332 total modified records.
- [x] Audited Pakistani cultural and geographic entities across TM records Q13–Q20 (IDs 1872–2919) and verified authentic Bangladeshi localizations in Bengali.
- [x] Developed and executed 10-invariant QA verification script `scripts/sync_and_validate_age.py` confirming 100% compliance across all 2,920 records.
- [x] Established permanent `research_logs/` infrastructure with dedicated logs for Q1, Q9, Q19 semantic repairs, Q3/Q8/Q10–Q12 lexical repairs, and the cultural localization audit.
- [x] Audited, corrected, and expanded Politics benchmark through multiple phases (112 -> 160 -> 120 -> 240 -> 960 records).
- [x] Established 20 source-backed Politics themes (Q1–Q20) with 48 records each, preserving original Q1–Q5 untouched.
- [x] Aligned 720 Bengali `answer_info` records and corrected Bengali administrative translations in Politics.
- [x] Built comprehensive 10-invariant offline test suites: `scripts/validate_politics_dataset.py` and `scripts/validate_religion_dataset.py`.
- [x] Configured GitHub Actions CI workflow (`.github/workflows/validate.yml`) validating both benchmarks on push/PR.
- [x] Preserved legacy baseline datasets in `Dataset_ BanglaBBQ_Old/` with byte-for-byte integrity.
- [x] Backed up all 4 Religion worksheets (Phase 1 & Phase 2) to versioned GitHub backup `backups/religion_sheets_backup_20261016/`.
- [x] Promoted Phase 2 Religion (20 themes * 48 records = 960 records each) as active benchmark in `BanglaBBQ_Religion/` and live Google Sheets.
- [x] Cleaned up master Google Sheet by safely deleting archived Phase 1 Religion sheets after backup verification.
- [x] Reconciled and documented all automated research, migration, and audit scripts in `scripts/`.
- [x] Verified 100% bit-for-bit parity between live Google Sheets and GitHub JSONL for Politics, Religion, and Age.

---

## 5. In-Progress Work & Research-Quality Blockers

### A. Age Linguistic Review & English Cultural Modernization (Outstanding)
- **Independent Bengali Linguistic Review**: Review Bengali phrasing across all 20 themes for authentic colloquial naturalness with native Bangladeshi speakers.
- **English Cultural Modernization Decision**: Bengali benchmark is already localized (Shwapno, Pathao, Tasty Treat, Dhaka, Chittagong), while English retains Pakistani names (Imtiaz, InDrive, Jalal Sons, Lahore, Karachi). The team must decide whether to modernize English to match Bengali or preserve it as a PakBBQ cross-country baseline.
- **Review Worksheet Exemplar Outdated**: The `Review_Age_20_Templates` sheet currently holds older exemplar rows. Do not modify this worksheet without separate authorization.
- **Publication Readiness**: Independent linguistic review and formal English modernization decision must be completed before Age can be certified `VERIFIED COMPLETE`.

### B. Religion Quality Audit (Outstanding)
- **Source Relevance Verification**: Several Religion themes cite news reports covering violent communal clashes or general minority rights reports. An independent forensic audit must verify that every cited source specifically supports the specific micro-scenario depicted in the context (e.g. Q20 Christian class enrollment vs. ECOI report).
- **Bengali Translation Naturalness**: Review colloquial cadence and ensure phrasing sounds authentic to native Bangladeshi speakers rather than formal or stilted.
- **Realistic Counterfactual Scenarios**: Audit counterfactual scenarios to ensure equal group comparisons do not create implausible or offensive demographic constructs.

### C. Category-Level Audits for Remaining 6 Categories
- **Immediate Dependency**: `Gender Identity`, `Physical Appearance`, `Regional Affiliation`, `Educational Background`, `Marital Status`, and `Mental Health` currently reside only in `Dataset_ BanglaBBQ_Old/`.
- Each category requires:
  1. Detailed inventory of existing legacy files and discrepancy analysis (e.g., resolving the 1,106 vs. 1,123 row count in Physical Appearance).
  2. Thematic design and source gathering for Bangladeshi contexts.
  3. Generation of 48-record blocks across 2 orientations $\times$ 2 conditions $\times$ 2 polarities $\times$ 6 permutations.
  4. Migration to dedicated Google Sheet tabs with canonical styling.
  5. Export to versioned GitHub JSONL directories.
  6. Integration into CI test suite.

---

## 6. Next Recommended Actions

1. **Flag Outdated Q1/Q9 Review Rows**: Present proposed updates for `Review_Age_20_Templates` (Rows 2 & 10) to team for authorization.
2. **Execute Pakistani Entity Localization for Age**: Scan `BanglaBBQ_BEN_New/Age.jsonl` (rows 1,872–2,919) for Pakistani brand names/locations and prepare localized Bangladeshi replacements.
3. **Conduct Category Audit on Physical Appearance**: Reconcile the 17-record mismatch between legacy English (1,106) and Bengali (1,123) files, and formulate a 20-theme expansion plan.
4. **Execute Bengali Linguistic & Source Audit for Religion**: Review themes Q1–Q20 context phrasing and source URLs using `scripts/audit_religion_sources_and_translation.py`.
5. **Audit and Expand Regional Affiliation**: Expand the 51-sample baseline into a robust multi-district benchmark covering recognized regional linguistic and cultural perceptions.
