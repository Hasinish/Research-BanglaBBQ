# state.md — Current Verified Progress Dashboard

**Last Verified Date**: 2026-10-17  
**Last Verified Git Commit**: `2ed23ad` (`docs(memory): establish official research mission and shared GitHub memory system`)  
**Current Milestone**: Synchronizing Age Q1 & Q9 Context Alignments and Establishing Research Logs  

---

## 1. Benchmark Status Dashboard across All 9 Categories

| Bias Category | English Count | Bengali Count | Status Marker | Current Working Status & Verification Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Politics** | 960 | 960 | `VERIFIED COMPLETE` | **20 themes (Q1–Q20)**, 48 rows/theme, full 6-way answer permutations ($3!$). 10/10 offline invariants passed. Live Google Sheets synced with 100% bit-for-bit parity. Untouched baseline Q1–Q5 verified. CI workflow active. |
| **Religion** | 960 | 960 | `IN PROGRESS` | **20 themes (Q1–Q20)**, 48 rows/theme, 1,920 total records. Phase 2 promoted to active dataset (`BanglaBBQ_Religion/`) and live sheets. Phase 1 safely archived to `backups/religion_sheets_backup_20261016/`. 10/10 offline checks passed. **Outstanding**: Independent source relevance check, Bengali translation naturalness review, and realistic counterfactual audit. |
| **Age** | 2,920 | 2,920 | `IN PROGRESS` | English source adapted from PakBBQ (`PakBBQ_Age_English.csv`). Bengali working dataset fully translated (2,920 rows) in Google Sheet `BanglaBBQ_BEN_Age` and synchronized to `BanglaBBQ_BEN_New/Age.jsonl`. Q1 (IDs 0–31) context diversity aligned (11 -> 16 unique contexts). Q9 (IDs 912–1199) context & answer options aligned (60 -> 144 unique contexts, 272 answer choices aligned). **Outstanding**: Cultural localization audit (reviewing Pakistani entities in TM records 1,872–2,919 for Bangladeshi equivalents) and independent native Bengali linguistic naturalness review. Exemplar rows in `Review_Age_20_Templates` flagged for future update. |
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
| `Review_Age_20_Templates` | `99887766` | 0 | Header + Samples | Executive 3-column review tab comparing PakBBQ English vs Legacy Thesis vs Hasin's Bengali translations. *(Contains older Q1 and Q9 exemplar rows; do NOT modify without approval).* |
| `PakBBQ_ENG_Age` | `0` | 1 | 2,921 (2,920 data) | Complete English Age benchmark source pool imported from PakBBQ. |
| `BanglaBBQ_BEN_Age` | `1006819770` | 2 | 2,921 (2,920 data) | Complete Bengali Age benchmark updated with Q1 context alignment (F2:F33) and Q9 context/answer alignment (F914:F1201, H914:J1201). |
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
- [x] Developed and executed 10-invariant QA verification script `scripts/sync_and_validate_age.py` confirming 100% compliance across all 2,920 records.
- [x] Established permanent `research_logs/` infrastructure with `README.md`, `TEMPLATE.md`, and retrospective logs `2026-10-17_age_q1_context_alignment.md` and `2026-10-17_age_q9_context_alignment.md`.
- [x] Audited, corrected, and expanded Politics benchmark through multiple phases (112 -> 160 -> 120 -> 240 -> 960 records).
- [x] Established 20 source-backed Politics themes (Q1–Q20) with 48 records each, preserving original Q1–Q5 untouched.
- [x] Aligned 720 Bengali `answer_info` records and corrected Bengali administrative translations in Politics.
- [x] Built comprehensive 10-invariant offline test suites: `scripts/validate_politics_dataset.py` and `scripts/validate_religion_dataset.py`.
- [x] Configured GitHub Actions CI workflow (`.github/workflows/validate.yml`) validating both benchmarks on push/PR.
- [x] Preserved legacy baseline datasets in `Dataset_ BanglaBBQ_Old/` with byte-for-byte integrity.
- [x] Backed up all 4 Religion worksheets (Phase 1 & Phase 2) to versioned GitHub backup `backups/religion_sheets_backup_20261016/`.
- [x] Promoted Phase 2 Religion (20 themes $\times$ 48 records = 960 records each) as active benchmark in `BanglaBBQ_Religion/` and live Google Sheets.
- [x] Cleaned up master Google Sheet by safely deleting archived Phase 1 Religion sheets after backup verification.
- [x] Reconciled and documented all automated research, migration, and audit scripts in `scripts/`.
- [x] Verified 100% bit-for-bit parity between live Google Sheets and GitHub JSONL for Politics and Religion.

---

## 5. In-Progress Work & Research-Quality Blockers

### A. Age Cultural Localization & Linguistic Review (Outstanding)
- **Pakistani Entity Audit in TM Records**: The 1,048 Target-Modified (TM) records (rows 1,872–2,919) adapted from PakBBQ contain Pakistani commercial and geographic entities (e.g., Imtiaz supermarket, InDrive, Jalal Sons, Karachi, Lahore). While translation is 100% complete and Q1/Q9 context alignments are synchronized, authentic Bangladeshi publication requires replacing these with local equivalents (Swapno, Pathao, Shwapno, Dhaka, Chittagong).
- **Independent Bengali Linguistic Review**: Review Bengali phrasing across all 20 themes for authentic colloquial naturalness.
- **Review Worksheet Exemplar Outdated**: The `Review_Age_20_Templates` sheet currently holds older exemplar rows for Q1 (Row 2) and Q9 (Row 10). Do not modify this worksheet without separate authorization.
- **Publication Readiness**: Cultural localization and linguistic review must be completed before Age can be certified `VERIFIED COMPLETE`.

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
