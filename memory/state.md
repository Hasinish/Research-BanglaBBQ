# state.md — Current Verified Progress Dashboard

**Last Verified Date**: 2026-10-18  
**Latest Verified Production Repair Main Commit**: `8acbd8f35092e1a572d2998dd9b5227a21b402b6` (Religion Q3/Q8/Q9/Q10/Q12/Q13 source-aligned V1/V2/V3 repairs across 864 records per language; entire bilingual live production verified at 2,880 records/language, zero 43,200-cell discrepancies/language; main GitHub Actions Religion assembly `39055874833` and Dataset Invariant Validation `39055874881` both succeeded). **Preserved Pre-Repair Main Baseline**: `bba8ef471ebe0bc53fcd116ada1b16849a4a6b14` (all 2,880 original pre-repair records in Git backup branch); pre-V2/V3 snapshot `9f72d105d8dd16b6d69dd4121983ec7a90c4a745`.
**Latest Memory Synchronization**: 2026-10-17, six-theme evidence repair merged at `8acbd8f35092e1a572d2998dd9b5227a21b402b6` (this memory-header refresh is a subsequent documentation-only commit).
**Latest Worksheet Structure Update**: 2026-10-18: Live `PakBBQ_ENG_Age` (sheetId `0`) was backed up as the hidden `Backup_PakBBQ_ENG_Age_preRename_20261018` (sheetId `124282477`, 2,921 grid rows including header) and renamed in place to `BanglaBBQ_ENG_Age` (same sheetId `0`). The original 2,920 English rows and 15-column schema were not edited; header/first/last and backup-end sample readbacks passed. Bengali Age and original GitHub datasets unchanged. The new name denotes a WORKING dataset only: full Bengali-English cultural localization and independent human/source checks are pending; it must not be represented as publication-ready.
**Latest Age Content QA (2026-10-18)**: English Age localized in 868 contexts (eight themes) + Q20 underage-driver legal confound resolved (112 records/lang: 15/17 -> 19/20 in context, answers, and answer_info; 672 cells persisted in Google Sheets). Both canonical JSONL exports (`BanglaBBQ_ENG_New/Age.jsonl` and `BanglaBBQ_BEN_New/Age.jsonl`) synchronized with live sheets; 0/43,800 live-vs-GitHub cell mismatches per language; 0/43,800 pre-Q20 backup vs baseline differences. 10/10 automated invariant checks PASS; Q6 fatigue vs unwillingness nuance and Q15/Q18 source-mechanism gaps formally documented. Independent native colloquial Bengali and external source certification remain pending.
**Current Milestone**: Age benchmark fully verified, Q20 legal confound repaired, and synchronized with 100% bit-for-bit live Google Sheets parity. Religion and Politics at 2,880/language; six other categories pending.

---

## 1. Benchmark Status Dashboard across All 9 Categories

| Bias Category | English Count | Bengali Count | Status Marker | Current Working Status & Verification Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Politics** | 2,880 | 2,880 | `IN PROGRESS` | **20 themes, 144 records/theme/language** = original 48 + wording v2 (48) + wording v3 (48). Original IDs 0–959 preserved; appended IDs 960–2879. Full 6-way answer permutations, balanced labels 960/960/960, counterfactual reversals, zero exact QA duplicates and bilingual structural parity verified. Approved targeted QA content repairs applied and synchronized across live Google Sheets and canonical GitHub JSONL: Q5 (144 rows/lang qualified with year 2022), Q14 (72 neg rows/lang question text refined to remove false expulsion premise), Q19 (144 Bengali rows aligned to government critic terminology 'সরকার-সমালোচক'). Validator and assembler updated to support dual-hash verification (preserving historical baseline hashes as evidence) and 100% bit-for-bit parity confirmed (43,200 cells/lang). **Outstanding**: Independent natural Bengali translation/entailment review, source-relevance audit and correlated-paraphrase evaluation safeguards. Not publication-ready. |
| **Religion** | 2,880 | 2,880 | `IN PROGRESS` | **Evidence-aligned bilingual production repair (2026-10-17):** Q3 changed public pump to equally permitted private irrigation pond; Q8 changed final hiring to eligibility screening for legal-affairs role; Q9 changed debate leadership to school scholarship selection; Q10 changed debate slot to secular cultural performance; Q12 changed wedding-hall reservation to festival venue access with matching use/fees/security; Q13 specified both neighbors as Dalit with non-Dalit host and reception-meal invitations. All six changes applied to **V1 + V2 + V3** (144 rows/theme/language; 864 corrected rows per language); historical pre-repair V1/V2/V3 snapshots and hashed shards remain untouched. Entire live English and Bengali production sheets: 2,880 rows/language, 20×144, labels 960/960/960, 6-way permutations, gold-role semantics, IDs 0–2879, bilingual metadata equality, zero unintended QA duplicates, **0/43,200 live-versus-GitHub cell mismatches per language**; 14 unaffected themes unchanged against full hidden pre-repair backups. Backups: Git branch `backup/religion-pre-evidence-redesign-20261017`; hidden live tabs `Backup_Religion_ENG_preSixTheme_20261017` / `Backup_Religion_BEN_preSixTheme_20261017`. Versioned patch `BanglaBBQ_Religion/evidence_revisions_20261017.json` and `scripts/apply_religion_evidence_revisions.py` preserve reproducible repair, with existing immutable expansion shards protected. **Research limitations:** Q3/Q9/Q10/Q13 comparisons are caste-and-religion intersectional, not causal religious-group evidence; Q8 source documents hiring-screen allegation under investigation; Q12 source documents a venue dispute, not the exact fictional comparison. Independent native Bengali and semantic human QA and family-aware evaluation splits outstanding. **Not publication-ready.** |
| **Age** | 2,920 | 2,920 | `IN PROGRESS` | **2026-10-18 English localization & Q20 legal confound repair verified**: 868 English context-only changes across 8 themes + Q20 underage driving repair (112 records/lang: 15/17 -> 19/20 in context, answers, and answer_info; 336 cells/lang, 672 total). Canonical GitHub exports `BanglaBBQ_ENG_New/Age.jsonl` and `BanglaBBQ_BEN_New/Age.jsonl`; live sheets `BanglaBBQ_ENG_Age` (gid 0) and `BanglaBBQ_BEN_Age` (gid 1006819770). 2,920 rows per language, zero 15-field metadata mismatches and 0/43,800 live-to-canonical cell mismatches per language; 0/43,800 pre-Q20 backup vs baseline differences (hidden sheets `Backup_BanglaBBQ_ENG_Age_preQ20LegalFix_20261018`, gid 1838448216; `Backup_BanglaBBQ_BEN_Age_preQ20LegalFix_20261018`, gid 1838448217). 10/10 automated invariant checks PASS. Q6 fatigue vs unwillingness nuance and Q15/Q18 source-mechanism gaps formally documented. **Automated structurally validated and targeted bilingual cultural/legal edits confirmed; full independent native-linguistic/semantic QA and external source certification are NOT complete. Not publication-ready.** |
| **Gender Identity** | 4,696 | 4,696 | `IN PROGRESS` | **Complete 34-theme bilingual migration (2026-10-18)**: 4,696 records per language across 34 themes (Q7, Q10–Q12, Q19, Q26, Q28, Q30–Q32, Q34–Q43, Q45–Q50, Q51–Q58). Full natural Bangladeshi Bengali translation preserving gender sensitivity (trans vs cis distinguished, hijra slurs avoided, canonical 'তথ্য অপর্যাপ্ত'). Live Google Sheets `BanglaBBQ_ENG_Gender` (ID `1990010101`) and `BanglaBBQ_BEN_Gender` (ID `1990010102`) verified with 100% parity across 140,880 data cells (0 mismatches). Native production formatting replicated (Navy headers #16213D, widths [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100], frozen header row, 6 CF rules). Canonical exports `BanglaBBQ_Gender/Gender_identity_eng.jsonl` and `BanglaBBQ_Gender/Gender_identity_bng.jsonl`; 10/10 offline invariants pass in CI. Inherited defects audited. **Secondary native colloquial human linguistic review and geographic localization pending. Not publication-ready.** |
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
| `review_20_politics_templates` | `1636577158` | 1 | 21 (20 themes) | Existing Politics Q1–Q20 disambiguated context exemplars comparing current English, original thesis Bengali (Q1–Q5), and current Bengali. Review-only; production datasets untouched. |
| `Review_Politics_20_Variations` | `722176577` | 2 | 21 (20 themes) | Side-by-side original/V2/V3 bilingual contexts Q1–Q20; user authorized integration of 40 additional bilingual wording pairs into the active dataset on 2026-10-17. Independent linguistic/source review still outstanding. |
| `Review_Religion_20_Variations` | `1743426767` | 13 (verified 2026-10-17) | 21 (20 themes) | Original Religion disambiguated contexts plus proposed English/Bengali V2/V3 variants, 40 candidate pairs. **Review only**; amber source-relevance flags in Q3, Q8, Q9–Q10 and Q12–Q13. |
| `Review_Religion_Source_Audit_20261017` | `1272448316` | 22 at original creation | 7 rows (6 audited themes) | Six source-evidence verdicts now updated with applied V1/V2/V3 bilingual repairs, corrected citations and explicit limits; companion working tab `Review_Religion_20_Variations` Q3/Q8/Q9/Q10/Q12/Q13 V1–V3 exemplars read back against production. |
| `BanglaBBQ_ENG_Age` | `0` | 18 (verified 2026-10-18) | 2,921 (2,920 data) | Renamed working sheet, then 868 English context repairs + Q20 underage driver legal repair (112 records, 15/17 -> 19/20); validated 0/43,800 live-vs-GitHub cell mismatches. 10/10 invariant pass. |
| `Backup_PakBBQ_ENG_Age_preRename_20261018` | `124282477` | 20 (hidden) | 2,921 (2,920 data) | Verbatim Google Sheets backup duplicated immediately before worksheet rename; original PakBBQ source remains in GitHub. |
| `Backup_BanglaBBQ_ENG_Age_preLocalization_20261018` | `1622078680` | 24 (hidden) | 2,921 (2,920 data) | Full pre-content-edit snapshot, 0/43,800 differences against immutable PakBBQ source. |
| `Backup_BanglaBBQ_ENG_Age_preQ20LegalFix_20261018` | `1838448216` | 1 (hidden) | 2,921 (2,920 data) | Full pre-Q20-repair English snapshot; 0/43,800 differences against commit 5d67e51 baseline. |
| `Backup_BanglaBBQ_BEN_Age_preQ20LegalFix_20261018` | `1838448217` | 0 (hidden) | 2,921 (2,920 data) | Full pre-Q20-repair Bengali snapshot; 0/43,800 differences against commit 5d67e51 baseline. |
| `Review_Age_Source_Audit_20261018` | `1613882208` | 27 | 21 (20 themes) | Per-theme inherited source assessment, Bangladeshi corroboration, source-to-scenario limits and blocking Q20 issue. |
| `BanglaBBQ_BEN_Age` | `1006819770` | 4 | 2,921 (2,920 data) | Complete Bengali Age benchmark updated with Q1 context, Q9 tech, Q19 youth repairs, lexical distinctions, and Q20 legal repair (112 records, 15/17 -> 19/20). 100% unique context & cell parity with canonical exports. |
| `BanglaBBQ_ENG_Politics` | `1888499205` | 5 | 2,881 (2,880 data) | Expanded active Politics English; exact live read-back against GitHub 480-row versioned shards, 144 records/theme. |
| `BanglaBBQ_BEN_Politics` | `2128232344` | 6 | 2,881 (2,880 data) | Expanded Bengali Politics benchmark, 144 records/theme, original answers and labels preserved, 100% structural and source-shard value read-back. |
| `BanglaBBQ_ENG_Religion` | `804112545` | 7 | 2,881 (2,880 data) | Active English Religion benchmark across 20 themes (V1+V2+V3) (formerly Phase 2, promoted after backup). |
| `BanglaBBQ_BEN_Religion` | `860941009` | 8 | 2,881 (2,880 data) | Active Bengali Religion benchmark across 20 themes (V1+V2+V3) (formerly Phase 2, promoted after backup). |
| `Backup_Politics_ENG_preV2V3_20261017` | `1140714802` | 9 (hidden) | 1,000 grid (960 data) | Untouched pre-expansion English Google Sheets snapshot, 15-column records and native formatting. |
| `Backup_Politics_BEN_preV2V3_20261017` | `1323539476` | 10 (hidden) | 1,000 grid (960 data) | Untouched pre-expansion Bengali Google Sheets snapshot. |
| `BanglaBBQ_ENG_Gender` | `1990010101` | 30 | 4,697 (4,696 data) | Complete English Gender Identity benchmark across 34 themes (A1:O4697). 100% cell-by-cell verified against PakBBQ source (70,440 data cells, 0 mismatches). Production formatting replicated. |
| `BanglaBBQ_BEN_Gender` | `1990010102` | 31 | 4,697 (4,696 data) | Complete Bengali Gender Identity benchmark across 34 themes (A1:O4697). Natural Bangladeshi Bengali translation. 100% cell-by-cell verified (70,440 data cells, 0 mismatches). Production formatting replicated. |

*Note: Worksheets for the remaining 5 categories will be created systematically as each category undergoes its dedicated audit and expansion.*

---

## 3. Active GitHub Dataset Directories

| Category | Canonical Directory | Primary Files | Record Count |
| :--- | :--- | :--- | :---: |
| **Politics** | [`BanglaBBQ_Politics/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics) | `banglabbq_politics_english.jsonl`<br/>`banglabbq_politics_bengali.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Religion** | [`BanglaBBQ_Religion/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion) | `Religion_eng.jsonl`<br/>`Religion_bng.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Age** | [`BanglaBBQ_BEN_New/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New)<br/>Root | `Age.jsonl`<br/>`PakBBQ_Age_English.csv` | 2,920 BEN<br/>2,920 ENG |
| **Gender Identity** | [`BanglaBBQ_Gender/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Gender) | `Gender_identity_eng.jsonl`<br/>`Gender_identity_bng.jsonl` | 4,696 ENG<br/>4,696 BEN |

---

## 4. Completed Work

- [x] Complete 34-theme bilingual migration and natural Bangladeshi Bengali translation of Gender Identity benchmark (4,696 English & 4,696 Bengali records; Q7, Q10–Q12, Q19, Q26, Q28, Q30–Q32, Q34–Q43, Q45–Q50, Q51–Q58). Preserved 15-column schema, sequential IDs (0–4695), labels, polarities, and answer permutations. Standardized Unknown as 'তথ্য অপর্যাপ্ত'.
- [x] Replicated exact native Google Sheets production formatting on both `BanglaBBQ_ENG_Gender` (ID: `1990010101`) and `BanglaBBQ_BEN_Gender` (ID: `1990010102`): Navy headers #16213D, Arial 10pt bold, column widths `[100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]`, frozen header row 1, middle/clip alignment, and 6 conditional formatting rules (`ambig`, `disambig`, `neg`, `nonneg`, `DT`, `NA`).
- [x] Executed exhaustive cell-by-cell live readback comparison verifying 140,880 data cells (70,440/sheet) + 30 headers with ZERO mismatches.
- [x] Built standalone offline validator `scripts/validate_gender_dataset.py` verifying 10/10 invariants, and added Gender validation to GitHub Actions CI (`.github/workflows/validate.yml`).
- [x] Independently audited inherited source defects: label distribution (1,582/1,552/1,562), 200 empty source citations, 24 duplicate entity records, 8 duplicate QA tuples, 176 explicit Pakistani references, 136 missing question marks. Authored research log `research_logs/2026-10-18_gender_identity_expansion_and_bilingual_qa.md`.
- [x] Formally reviewed Age Q2 (IDs 32–127) for translation issues involving grandparent terminology, age references, and context phrasing; researcher explicitly decided to leave Q2 and the entire Age dataset unchanged for the current research phase.
- [x] Formally accepted Age benchmark for current research phase (2,920 records per language) with no further dataset modifications authorized.
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
- [x] Created `review_20_politics_templates` as a 20-theme bilingual Politics reference worksheet. Original thesis Bengali contexts are available only for Q1–Q5.
- [x] Created `Review_Politics_20_Variations` (21 rows, 4 columns) with original Q1–Q20 bilingual contexts plus 40 English–Bengali wording candidate pairs; on explicit 2026-10-17 approval, generated two full 48-record blocks/theme/language and integrated them with the active Politics datasets. Original 960 records per language were preserved exactly.
- [x] Established 20 source-referenced Politics themes (Q1–Q20) with 48 records per wording block (144 records/theme after adding v2 and v3), preserving original Q1–Q5 unchanged.
- [x] Aligned 720 Bengali `answer_info` records and corrected Bengali administrative translations in Politics.
- [x] Built comprehensive 10-invariant offline test suites: `scripts/validate_politics_dataset.py` and `scripts/validate_religion_dataset.py`.
- [x] Configured GitHub Actions CI workflow (`.github/workflows/validate.yml`) validating both benchmarks on push/PR.
- [x] Preserved legacy baseline datasets in `Dataset_ BanglaBBQ_Old/` with byte-for-byte integrity.
- [x] Backed up all 4 Religion worksheets (Phase 1 & Phase 2) to versioned GitHub backup `backups/religion_sheets_backup_20261016/`.
- [x] Promoted Phase 2 Religion (20 themes * 48 records = 960 records each) as active benchmark in `BanglaBBQ_Religion/` and live Google Sheets.
- [x] Cleaned up master Google Sheet by safely deleting archived Phase 1 Religion sheets after backup verification.
- [x] Reconciled and documented all automated research, migration, and audit scripts in `scripts/`.
- [x] Verified live Google Sheets and versioned GitHub snapshots for Politics, Religion, and Age before expansion; afterward verified all 1,920 appended Politics rows/language against the 15-column GitHub expansion shards in 240-row batches and verified CI-assembled canonical snapshots with original baselines.
- [x] Synchronized approved Religion QA repairs across live Google Sheets (`BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion`) and canonical GitHub JSONL files (528 ENG, 504 BEN rows patched across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20). Confirmed 100% bit-for-bit parity across all 960 rows x 15 columns (14,400 cells/lang) via Google Sheets API v4. Verified all 10 invariant checks and counterfactual reversibility. Authored `research_logs/2026-10-17_religion_qa_repair.md`.
- [x] Completed comprehensive research-quality final validation of the full expanded Religion benchmark (2,880 ENG, 2,880 BEN across 20 themes, V1+V2+V3). Audited Q3, Q8, Q9, Q10, Q12, Q13 and remaining 14 themes for source evidence boundaries, caste-religion intersectionality, and non-eyewitness distinctions. Verified 100% counterfactual A/B inversion, 1,440/1,440 ambiguous Unknown targets, 1,440/1,440 disambiguated grounded entities, full 6-way answer permutations across 480 sub-blocks, zero string anomalies, and 43,200 data cells per language verified with live Google Sheets. Authored `research_logs/2026-10-18_religion_final_qa_and_validation.md`.
- [x] Verified and completed Age Q20 legal confound repair (112 records/lang: 15/17 -> 19/20 in context, answers, answer_info; 672 cells in Google Sheets) eliminating underage-driver confounds under Bangladesh Road Transport Act, 2018. Synchronized canonical exports (`BanglaBBQ_ENG_New/Age.jsonl` and `BanglaBBQ_BEN_New/Age.jsonl`) with 100% bit-for-bit live Google Sheets parity (43,800 cells/lang). Updated `scripts/apply_age_english_localization_20261018.py` and `scripts/sync_and_validate_age.py`. Executed 20-theme audit documenting Q6 fatigue vs unwillingness nuance and Q15/Q18 source-mechanism gaps in `research_logs/2026-10-18_age_q20_legal_confound_repair.md`.

---

## 5. In-Progress Work & Research-Quality Blockers

### A. Age Benchmark Phase Acceptance & Outstanding Publication Considerations
- **Accepted for Current Research Phase**: The 2,920-record bilingual Age benchmark has completed English context localization (868 rows) and Q20 legal confound repair (112 rows/lang), achieving 100% parity across all 43,800 data cells per language between live Google Sheets and canonical GitHub JSONLs.
- **Q20 Underage Driver Confound Resolved**: 15/17-year-old car drivers replaced with 19/20-year-olds in both English and Bengali, aligning with Bangladesh Road Transport Act 2018 licensing age >=18. Zero underage drivers remain.
- **Age Q2 Status**: Reviewed for grandparent terminology and context phrasing; explicitly left unchanged by researcher decision.
- **Substantive Thematic Nuances Documented**: Q6 fatigue vs. unwillingness entailment friction, and Q15 / Q18 source-mechanism gaps formally documented in `research_logs/2026-10-18_age_q20_legal_confound_repair.md`.
- **Independent Bengali Linguistic Review (Outstanding)**: Review Bengali phrasing across all 20 themes for authentic colloquial naturalness with independent native Bangladeshi speakers before final publication certification.
- **Review Worksheet Exemplar Outdated**: The `Review_Age_20_Templates` sheet currently holds older exemplar rows. Retained untouched per protocol; do not modify without separate authorization.
- **Publication Status**: **NOT publication-ready** until secondary human linguistic certification and source-mechanism alignment are resolved. Ready for proceeding to Gender Identity audit.

### B. Religion Benchmark Status & Outstanding Publication Considerations
- **Comprehensive Validation Complete (2,880 records/lang)**: Full 20 themes x 144 records (V1+V2+V3) structurally verified, live Google Sheets parity confirmed (43,200 cells/lang), 10/10 invariant checks passed, zero duplicate QA tuples, zero string/whitespace anomalies.
- **Source Relevance & Evidence Boundaries Documented**: Sources for Q3, Q8–Q10, Q12–Q13 and remaining 14 themes verified. Crucial evidentiary boundary established: cited institutional reports substantiate macro-level discrimination patterns, not literal historical accounts of fictional BBQ probes; Q8 documented as an inquiry into an allegation; Q3/Q9/Q10/Q13 recognized as intersectional (caste + religion).
- **Evaluation Split Leakage Safeguards**: Records can be partitioned cleanly by `parent_example_id` (size 3) or by `question_index` (size 144) to ensure cross-validation without train/test paraphrase leakage.
- **Independent Bengali Linguistic Naturalness (Outstanding)**: Final qualitative review by native Bangladeshi speakers across all 20 themes remains an explicit requirement prior to publication.
- **Publication Status**: **NOT publication-ready** until secondary human linguistic certification is completed. Ready for proceeding to Gender Identity audit.

### C. Category-Level Audits for Remaining 6 Categories
- **Immediate Priority**: `Gender Identity`, `Physical Appearance`, `Regional Affiliation`, `Educational Background`, `Marital Status`, and `Mental Health` currently reside only in `Dataset_ BanglaBBQ_Old/`.
- Each category requires:
  1. Detailed inventory of existing legacy files and discrepancy analysis (e.g., resolving the 1,106 vs. 1,123 row count in Physical Appearance).
  2. Thematic design and source gathering for authentic Bangladeshi socio-cultural contexts.
  3. Generation of 48-record blocks across 2 orientations * 2 conditions * 2 polarities * 6 permutations.
  4. Migration to dedicated Google Sheet tabs with canonical styling.
  5. Export to versioned GitHub JSONL directories.
  6. Integration into CI test suite.

---

### D. Politics V2/V3 Wording Expansion (Structurally Validated; Human Review Outstanding)
- **Authorized**: The user explicitly requested adding both additional wording versions to all 20 Politics themes on 2026-10-17. Candidate texts came from `Review_Politics_20_Variations` (Google Sheet `gid=722176577`).
- **Counts**: 2,880 English + 2,880 Bengali active rows (20 themes x 3 wording versions x 48 answer-permutation examples). Old canonical 960-row prefix and Q1–Q5 hash invariants preserved exactly; appended IDs 960–2879.
- **QA and synchronization**: Live Google Sheets expansion compared cell-by-cell with eight GitHub shards. Balanced 960/960/960 labels, no exact duplicate QA tuples, full permutations and theme-polarity-condition balances, bilingual metadata equality verified. GitHub Actions `Materialize BanglaBBQ Politics V2/V3 Expansion` passed and committed expanded canonical JSONL at `cab9f72b6c969e19b4c97bd16b293986e4a2b771`; automated validation on staging commit `31c13939465fc146ab01a47fbb3c9043c796261d` also passed.
- **Provenance/backup**: Frozen GitHub originals at `backups/politics_pre_wording_v2v3_20261017/`; hidden Sheets backups `Backup_Politics_ENG_preV2V3_20261017`/`Backup_Politics_BEN_preV2V3_20261017`; source-review templates in `BanglaBBQ_Politics/expansion_v2v3_20261017/`, including manifest and deterministic assembler script.
- **Review cautions**: New variants are fictional paraphrases, NOT new independently evidenced incidents. Independent native Bengali linguistic review, strict EN/BN semantic entailment review, case-specific source relevance verification and grouped evaluation splits remain outstanding. **Not publication-ready**.

---

### E. Politics Q5/Q14/Q19 Approved Fixes & Live Synchronization (Verified Parity)
- **Authorized**: Researcher approved three targeted QA repairs: (1) Q5 historical qualification with year 2022 (144 records/lang), (2) Q14 negative question refinement removing unsubstantiated university expulsion premise (72 records/lang), and (3) Q19 Bengali option/context terminology alignment to government critic `সরকার-সমালোচক` (144 Bengali records).
- **Google Sheets & GitHub Parity**: Applied by ChatGPT to live sheets `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`. Local Git synchronization completed via `scripts/apply_politics_q5_q14_q19_fixes.py` (resolving remote GitHub connector timeout). 100% bit-for-bit parity confirmed across all 2,880 records (43,200 cells per language) via Google Sheets API v4.
- **Validator & Assembler Harmonization**: Updated `scripts/validate_politics_dataset.py` with dual-hash verification (preserving historical baseline hashes as evidence while supporting post-repair hashes for active benchmark). Updated `scripts/assemble_politics_expansion.py` with CRLF normalization and recognized post-repair canonical records.
- **Backups Preserved**: Historical thesis files (`Dataset_ BanglaBBQ_Old/Politics/`), pre-expansion backups (`backups/politics_pre_wording_v2v3_20261017/`), and pre-fix live sheets (`Backup_Politics_ENG_preQAfix_20261017`, `Backup_Politics_BEN_preQAfix_20261017`) preserved untouched.
- **Publication Status**: **NOT publication-ready**. Independent native-speaker Bengali linguistic review and external source-relevance verifications remain outstanding.
---

## 6. Next Recommended Actions

The primary active research priority is improving and expanding the six remaining categories:

1. **Gender Identity Audit & Thematic Design**: Conduct category-level forensic audit of legacy baseline files in `Dataset_ BanglaBBQ_Old/Gender_identity/`, audit bias dimensions, design authentic Bangladeshi thematic coverage, balance 6-way permutations, and initialize master Google Sheet integration.
2. **Physical Appearance Discrepancy Reconciliation**: Reconcile the 17-record mismatch between legacy English (1,106) and Bengali (1,123) baseline files, design balanced 20-theme architecture, and expand to canonical 48-record permutation structure.
3. **Regional Affiliation Benchmark Expansion**: Audit and expand the severely underpowered 51-sample legacy baseline into a robust multi-district benchmark covering recognized regional socio-cultural perceptions with source backing.
4. **Educational Background Modernization**: Audit legacy baseline (128 records), design expanded education/institution scenarios, balance permutations, and verify socio-cultural grounding.
5. **Marital Status Expansion**: Audit legacy baseline (100 records), develop realistic marital bias scenarios, balance 6-way permutations, and ensure cultural grounding.
6. **Mental Health Expansion**: Audit legacy baseline (100 records), expand clinical and societal bias scenarios, and balance permutations.
7. **Outstanding Publication-Readiness Audits (Religion & Age)**: Execute independent source relevance and naturalness audits for Religion (`scripts/audit_religion_sources_and_translation.py`); conduct independent native linguistic naturalness review for Age prior to publication submission.
