# Workspace Index & Repository Map

> **VERIFIED REPOSITORY MAP**  
> Every path listed in this index has been verified to exist on disk. Active production datasets are strictly separated from legacy baseline directories.

---

## 1. Directory Structure Overview

```
Research-BanglaBBQ/
├── .github/workflows/           # Automated CI workflows (invariant validation)
├── BanglaBBQ_Politics/          # Active Politics benchmark (2,880 ENG, 2,880 BEN; base + V2/V3)
├── BanglaBBQ_Religion/          # Active Religion benchmark (2,880 ENG, 2,880 BEN; V1+V2+V3)
├── BanglaBBQ_BEN_New/           # Active verified Bengali Age benchmark (2,920 BEN)
├── BanglaBBQ_Gender/            # Active verified Gender Identity benchmark (4,696 ENG, 4,696 BEN across 34 themes)
├── Dataset_ BanglaBBQ_Old/      # Historical baseline from seniors' thesis (T2510616)
├── PakBBQ_Repo/                 # Cloned official PakBBQ benchmark repository (EMNLP 2025)
├── backups/                     # Timestamped backups of Google Sheets and datasets
├── scripts/                     # Automation, validation, migration, and audit scripts (including Politics expander)
├── research_logs/               # Permanent detailed research and audit logs
├── memory/                      # Authoritative shared project memory
├── PakBBQ_Age_English.csv       # Active English Age benchmark source pool (2,920 rows)
├── T2510616.pdf                 # Original undergraduate thesis book (84 pages)
├── T2510616_IEEE_Paper.pdf      # Original 8-page IEEE conference paper draft
├── CITATION.cff                 # Machine-readable academic citation metadata
├── README.md                    # Public repository documentation
└── requirements.txt             # Python dependencies
```

---

## 2. Active Production Datasets

These are the canonical, working datasets currently under active research and evaluation.

### A. Politics ([`BanglaBBQ_Politics/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics))
- [`banglabbq_politics_english.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics/banglabbq_politics_english.jsonl): 2,880 records across 20 source-referenced themes (Q1–Q20), 144/theme (original 48 + v2 48 + v3 48). Full 6-way permutations, four-row canonical ordering, uniform labels (960/960/960), zero exact QA duplicates, 15-column schema. Approved Q5 (historical year 2022 qualification) and Q14 (dormitory belongings negative question refinement) applied.
- [`banglabbq_politics_bengali.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics/banglabbq_politics_bengali.jsonl): 2,880 parallel Bengali records, source-aligned metadata, verified counterfactuals. Approved Q5, Q14, and Q19 (terminology aligned to 'সরকার-সমালোচক' / 'সরকার-সমালোচকের') applied.
- **Status**: `IN PROGRESS` (Expanded and synchronized with 100% bit-for-bit live Google Sheets parity; independent native Bengali linguistic review and external source-relevance reviews pending; not publication-ready).
- **Expansion materials**: [`expansion_v2v3_20261017/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics/expansion_v2v3_20261017) includes the 40 bilingual V2/V3 context templates, manifest and eight 480-row append-only shards. Canonical JSONL snapshots were materialized by GitHub Actions from SHA-verified historical backups and shards.

### B. Religion ([`BanglaBBQ_Religion/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion))
- [`Religion_eng.jsonl`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/BanglaBBQ_Religion/Religion_eng.jsonl): **2,880** production English records across V1/V2/V3, 20 × 144, six-way permutations and labels 960/960/960. **Q3/Q8/Q9/Q10/Q12/Q13 (144 records/theme) source-aligned repaired in all three waves**, preserving IDs 0–2879 and all gold label positions. Original pre-repair snapshots/shards held immutably; human semantic/source limits documented.
- [`Religion_bng.jsonl`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/BanglaBBQ_Religion/Religion_bng.jsonl): **2,880** production Bengali records, six themes × 144 rows revised in parallel, exact shared metadata with English, zero discrepancies across all 43,200 cells versus live production Bengali worksheet at verification; native linguistic review outstanding.
- [`review_v2v3_20261017.json`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/BanglaBBQ_Religion/review_v2v3_20261017.json): Original Q1–Q20 bilingual review source and 40 V2/V3 wording pairs, integrated into structurally validated production expansion on 2026-10-17; open source/translation caveats remain.
- **Religion source audit working tab**: `Review_Religion_Source_Audit_20261017` (gid `1272448316`) now documents applied Q3/Q8/Q9/Q10/Q12/Q13 evidence-aligned repairs and remaining provenance limits. `Review_Religion_20_Variations` (gid `1743426767`) contains refreshed production-aligned V1/V2/V3 bilingual exemplars for the six themes.
- [`expansion_v2v3_20261017/`](https://github.com/Hasinish/Research-BanglaBBQ/tree/main/BanglaBBQ_Religion/expansion_v2v3_20261017): SHA-pinned bilingual context templates, lineage manifest, and 16 240-record append-only shards (1,920 added records per language).
- [`evidence_revisions_20261017.json`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/BanglaBBQ_Religion/evidence_revisions_20261017.json): dated English/Bengali six-theme V1/V2/V3 context, question, option, gold-role and source revision manifest; production override without altering legacy input shards.
- [`scripts/apply_religion_evidence_revisions.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/apply_religion_evidence_revisions.py): deterministic, scope-limited correction layer applied after immutable expansion shard assembly; verifies all gold answer roles.
- **Status**: `IN PROGRESS` (Structurally validated and synchronized with live sheets; source relevance boundaries formalized; secondary native Bengali linguistic review pending; not publication-ready).

### C. Age ([`BanglaBBQ_BEN_New/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New) & `BanglaBBQ_ENG_New/`)
- **English canonical (2026-10-18):** `BanglaBBQ_ENG_New/Age.jsonl`, 2,920 records, 15 fields; 868 English context locality/grammar repairs + Q20 legal confound repair (112 records, 15/17 -> 19/20 in context, answers, answer_info). Reproduce and validate using `scripts/apply_age_english_localization_20261018.py` (tested in CI). Full pre-Q20 backup `Backup_BanglaBBQ_ENG_Age_preQ20LegalFix_20261018` (gid 1838448216; hidden); 0/43,800 live-vs-GitHub discrepancies.
- **Bengali canonical (2026-10-18):** `BanglaBBQ_BEN_New/Age.jsonl`, 2,920 parallel records; culturally localized (Shwapno, Pathao, Tasty Treat, Dhaka/Chattogram, tea stall) + Q20 legal confound repair (112 records, 15/17 -> 19/20). Pre-Q20 backup `Backup_BanglaBBQ_BEN_Age_preQ20LegalFix_20261018` (gid 1838448217; hidden); 0/43,800 live-vs-GitHub discrepancies.
- **Live worksheets:** `BanglaBBQ_ENG_Age` (`gid=0`) and `BanglaBBQ_BEN_Age` (`gid=1006819770`), 2,920 data rows each. 10/10 invariant validation passes.
- [`PakBBQ_Age_English.csv`](file:///d:/Research-BanglaBBQ/PakBBQ_Age_English.csv): 2,920 English records adapted from PakBBQ (1,872 DT + 1,048 TM).
- **Status**: `IN PROGRESS` (Structurally validated, zero underage drivers in Q20, 100% Google Sheets parity; independent colloquial Bengali linguistic review and external source-mechanism alignment remain pending; not publication-ready).

### D. Gender Identity ([`BanglaBBQ_Gender/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Gender))
- [`Gender_identity_eng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Gender/Gender_identity_eng.jsonl): **4,696** production English records across 34 themes (Q7, Q10–Q12, Q19, Q26, Q28, Q30–Q32, Q34–Q43, Q45–Q50, Q51–Q58) from PakBBQ source. Exact 15-column schema, sequential IDs 0–4695, source IDs 4388–9083, labels 1582/1552/1562.
- [`Gender_identity_bng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Gender/Gender_identity_bng.jsonl): **4,696** production parallel Bengali records. Natural Bangladeshi Bengali translations adhering to gender-sensitive guidelines (transgender vs cisgender distinguished, hijra slurs avoided, Unknown standardized as 'তথ্য অপর্যাপ্ত').
- **Live worksheets**: `BanglaBBQ_ENG_Gender` (Sheet ID: `1990010101`) and `BanglaBBQ_BEN_Gender` (Sheet ID: `1990010102`), 4,697 rows (A1:O4697) each. 100% bit-for-bit parity verified across all 140,880 data cells (0 mismatches). Production formatting replicated (navy headers #16213D, widths [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100], frozen header row 1, middle/clip alignment, 6 CF rules).
- **Validation**: `scripts/validate_gender_dataset.py` (tested in CI).
- **Status**: `IN PROGRESS` (Structurally validated and synchronized with live sheets; 10/10 offline invariants pass; secondary native colloquial Bengali review and geographical localization pending; not publication-ready).

---

## 3. Historical Baseline: Seniors' Original Dataset ([`Dataset_ BanglaBBQ_Old/`](file:///d:/Research-BanglaBBQ/Dataset_%20BanglaBBQ_Old))

> **PRESERVATION POLICY**: All files in this directory are frozen historical artifacts from thesis T2510616. They must **never** be deleted, overwritten, or silently modified.

### Root Files
- `banbbq_ben_combined.jsonl`: Partially aggregated legacy Bengali dataset (2,866 lines; contains syntax issues).

### Category Subdirectories
- **`Age/`**:
  - `Age_Bengali_800entries.jsonl`: 799 legacy Bengali records (truncated at row 798).
  - `Age_Eng.jsonl`: 2,920 legacy English records.
- **`AGE_ENG/`**:
  - `Age.jsonl`: 799 parallel English records.
- **`Banglabbq/`**:
  - `banglabbq_ben_combined.jsonl`: 850 early Bengali experimental records.
  - `banglabbq_eng_combined.jsonl`: 850 early English parallel records.
- **`BBQ/BanBBQ_BEN/`** (Consolidated legacy Bengali categories):
  - `Age.jsonl`: 799 records.
  - `Gender_identity.jsonl`: 506 records.
  - `Physical_appearance.jsonl`: 1,123 records.
  - `Regional.jsonl`: 51 records.
  - `Religion.jsonl`: 392 records.
- **`BBQ/BanBBQ_ENG/`** (Consolidated legacy English categories):
  - `Age.jsonl`: 799 records.
  - `Gender_identity.jsonl`: 506 records.
  - `Physical_appearance.jsonl`: 1,106 records.
  - `Regional.jsonl`: 51 records.
  - `Religion.jsonl`: 392 records.
- **`Educational background/`**:
  - `banglabbq_education_bengali.jsonl`: 128 records.
  - `banglabbq_education_english.jsonl`: 128 records.
- **`Gender_identity/`**:
  - `Gender_identity_bng.jsonl`: 506 records.
  - `Gender_identity_eng.jsonl`: 506 records.
- **`Marital Status/`**:
  - `Marital_status_Bengali_100entries.jsonl`: 100 records.
  - `Marital_status_Eng.jsonl`: 100 records.
- **`Mental Health/`**:
  - `Mental_health_status_Bengali_100entries.jsonl`: 100 records.
  - `Mental_health_status_Eng.jsonl`: 100 records.
- **`Physical_appearance/`**:
  - `Physical_appearance.jsonl`: 1,123 Bengali records.
- **`P_A_E/`**:
  - `Physical_appearance.jsonl`: 1,106 English records.
- **`Politics/`**:
  - `banglabbq_politics_bengali_112old.jsonl`: 112 original un-repaired legacy Bengali records.
  - `banglabbq_politics_english_112old.jsonl`: 112 original un-repaired legacy English records.
  - `banglabbq_politics_bengali.jsonl`: 960 records (mirrored from active expansion).
  - `banglabbq_politics_english.jsonl`: 960 records (mirrored from active expansion).
- **`Regional/`**:
  - `Regional_ban.jsonl`: 51 records.
  - `Regional_eng.jsonl`: 51 records.
- **`Religion/`**:
  - `Religion_bng.jsonl`: 392 records.
  - `Religion_eng.jsonl`: 392 records.

---

## 4. Versioned Backups ([`backups/`](file:///d:/Research-BanglaBBQ/backups))
- **`backups/religion_pre_wording_v2v3_20261017/`**: byte-identical 960-record original Religion English/Bengali JSONL blobs from pre-expansion main; additional hidden native Google Sheet backup tabs preserve the pre-expansion 960 records and formatting.

- **`backups/age_sheets_backup_20261017/`**:
  - `BanglaBBQ_BEN_Age.csv` & `BanglaBBQ_BEN_Age.json` (2,921 rows pre-edit backup).
  - `PakBBQ_ENG_Age.csv` & `PakBBQ_ENG_Age.json` (2,921 rows English baseline backup).
  - `Review_Age_20_Templates.csv` & `Review_Age_20_Templates.json` (21 rows review tab backup).
- **`backups/religion_sheets_backup_20261016/`**:
  - `BanglaBBQ_ENG_Religion_Phase1.jsonl` (480 records).
  - `BanglaBBQ_BEN_Religion_Phase1.jsonl` (480 records).
  - `BanglaBBQ_ENG_Religion_Phase2.jsonl` (960 records).
  - `BanglaBBQ_BEN_Religion_Phase2.jsonl` (960 records).
  - `raw_sheets_data.json` & `metadata.json`: Raw Google Sheets API dumps with SHA-256 integrity proofs.
- **`backups/politics_pre_wording_v2v3_20261017/`**: Immutable 960-record English/Bengali canonical JSONL snapshots (Git blob aliases); live workbook also contains two hidden native 960-record backup tabs.
- **`backups/politics_before_corrections/`**:
  - Pre-correction backups of Politics sheets (`BanglaBBQ_ENG_Politics_backup.csv`, `BanglaBBQ_BEN_Politics_backup.csv`, raw JSON).
- **`backups/audit_20261016/`**:
  - Live sheet dumps and local JSONL snapshots during the Politics repair phase, including `q1_q5_hashes.json` and `translation_repair_report.json`.

---

## 5. Automation, Validation, & Audit Scripts ([`scripts/`](file:///d:/Research-BanglaBBQ/scripts))

Contains specialized scripts documented in [`scripts/README.md`](file:///d:/Research-BanglaBBQ/scripts/README.md). Key active tools include:

### Benchmark Invariant Validators & CI
- [`scripts/apply_politics_q5_q14_q19_fixes.py`](file:///d:/Research-BanglaBBQ/scripts/apply_politics_q5_q14_q19_fixes.py): Idempotent content correction script applying approved Q5 historical date, Q14 entailment, and Q19 Bengali critic terminology fixes.
- [`scripts/validate_politics_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_politics_dataset.py): Expanded 960/2,880-aware validator with dual-hash verification (preserving historical baseline hashes as evidence while supporting approved post-repair hashes for active benchmark), V2/V3 lineage, permutations, bilingual alignment, and 0 duplicates.
- [`scripts/assemble_politics_expansion.py`](file:///d:/Research-BanglaBBQ/scripts/assemble_politics_expansion.py): Verifies append-only expansion from hashed pre-expansion backups and shards, with cross-platform CRLF normalization and recognized post-repair canonical records.
- [`scripts/validate_religion_dataset.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/validate_religion_dataset.py): 10-category structural invariant validator accepting both 960 historical and 2,880 expanded bilingual files, including variant-aware six-way answer permutations.
- [`scripts/assemble_religion_expansion.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/assemble_religion_expansion.py): hash-pinned append-only assembly from immutable V1 snapshots and 16 shards, validating inherited answers, metadata, source links, counterfactuals, bilingual shared fields, labels and record counts.
- [`scripts/validate_gender_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_gender_dataset.py): Automated 10-invariant offline dataset validator checking record counts (4,696 each), sequential IDs (0–4695), 15-column schema, 100% bilingual metadata parity, gold label semantic grounding (2348 ambig -> 'তথ্য অপর্যাপ্ত', 2348 disambig -> entity), answer permutations, Bengali script integrity, 34 question themes, and inherited defect audits.
- [`scripts/generate_gender_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/generate_gender_dataset.py): Deterministic generator and translation pipeline processing all 4,696 English records from PakBBQ source, translating unique context/QA entities into fluent Bangladeshi Bengali, and exporting canonical English and Bengali JSONLs with the exact 15-column schema to `BanglaBBQ_Gender/`.
- [`scripts/gender_translation/`](file:///d:/Research-BanglaBBQ/scripts/gender_translation): Modular translation engine components (`base_mappings.py`, `group1_translator.py`, `group2_translator.py`, `group3_translator.py`).
- [`.github/workflows/validate.yml`](file:///d:/Research-BanglaBBQ/.github/workflows/validate.yml): Automated GitHub Actions CI workflow executing offline validators on every push and pull request.

### Live Google Sheets Sync & Verification
- [`scripts/upload_bengali_gender_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/upload_bengali_gender_sheets.py): Chunked idempotent uploader writing all 4,697 rows (A1:O4697) of `BanglaBBQ_BEN_Gender` (Sheet ID: 1990010102) to the Master Google Spreadsheet.
- [`scripts/apply_gender_sheets_formatting.py`](file:///d:/Research-BanglaBBQ/scripts/apply_gender_sheets_formatting.py): Applies exact production formatting across both `BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender` (Sheet IDs: 1990010101, 1990010102) matching Religion/Age standards.
- [`scripts/verify_gender_live_parity.py`](file:///d:/Research-BanglaBBQ/scripts/verify_gender_live_parity.py): Exhaustive cell-by-cell live verification comparing all 140,880 data cells (70,440 cells x 2 sheets) against local canonical JSONLs, confirming 0 mismatches, exact grid dimensions, and rule parity.
- [`scripts/sync_and_validate_age.py`](file:///d:/Research-BanglaBBQ/scripts/sync_and_validate_age.py): Synchronizes live Google Sheets updates from `BanglaBBQ_BEN_Age` to `BanglaBBQ_BEN_New/Age.jsonl` and executes 10-invariant benchmark quality assurance tests across all 20 themes.
- [`scripts/push_age_repairs.py`](file:///d:/Research-BanglaBBQ/scripts/push_age_repairs.py): Pushes deterministic batch updates for repaired themes to Google Sheets and updates local canonical files.
- [`scripts/verify_politics_960_live.py`](file:///d:/Research-BanglaBBQ/scripts/verify_politics_960_live.py): Historical 960-row Politics baseline verification utility; not a full 2,880-record expanded-sheet validator. The 2026-10-17 expansion was independently verified with 15-field live chunk readbacks.
- [`scripts/verify_religion_live.py`](file:///d:/Research-BanglaBBQ/scripts/verify_religion_live.py): Fetches live Google Sheets tabs `BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion` and verifies complete parity with GitHub JSONL files.
- [`scripts/list_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/list_sheets.py): Lists all worksheets, sheet IDs, and indices in the master Google Spreadsheet.

### Forensic Audit & Diagnostic Tools
- [`scripts/audit_cultural_localization.py`](file:///d:/Research-BanglaBBQ/scripts/audit_cultural_localization.py): Scans Age TM records (Q13–Q20) for Pakistani commercial/geographic entities and compares against Bengali domestic localizations.
- [`scripts/audit_religion_sources_and_translation.py`](file:///d:/Research-BanglaBBQ/scripts/audit_religion_sources_and_translation.py): Comprehensive audit suite for Religion Q1–Q20 verifying theme-by-theme source classification, counterfactual reversibility/symmetry, ambiguous/disambiguated entailment invariants, and documentation of macro evidence boundaries.
- [`scripts/repair_politics_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/repair_politics_dataset.py): Deterministically aligned 720 Bengali `answer_info` records.
- [`scripts/apply_p1_p2_corrections.py`](file:///d:/Research-BanglaBBQ/scripts/apply_p1_p2_corrections.py): Applied Grandparent/Grandchild (56 rows) and Q7 (48 rows) fixes to Age.

---

## 6. Academic Artifacts & Methodological Reference Repositories

- [`T2510616.pdf`](file:///d:/Research-BanglaBBQ/T2510616.pdf): Complete 84-page BRAC University undergraduate thesis book (*"A Bilingual Study of Socio-Cultural Bias in Large Language Models through BanglaBBQ and a Post Processing Mitigation Pipeline"*, June 2025).
- [`T2510616_IEEE_Paper.pdf`](file:///d:/Research-BanglaBBQ/T2510616_IEEE_Paper.pdf): 8-page IEEE conference paper draft. Formulates benchmark metrics, Fleiss' Kappa formulas, paired t-tests, and SafeLLM 3-stage mitigation architecture.
- [`PakBBQ_Repo/`](file:///d:/Research-BanglaBBQ/PakBBQ_Repo): Cloned official repository of PakBBQ (*"PakBBQ: A Culturally Adapted Bias Benchmark for Question Answering in Pakistan"*, EMNLP 2025 / arXiv:2508.10186). Contains 8 benchmark categories in English and Urdu, evaluation scripts, and analysis notebooks.
- [`CITATION.cff`](file:///d:/Research-BanglaBBQ/CITATION.cff): Formal citation metadata for the BanglaBBQ project and ongoing research.

---

## 7. Authoritative Shared Memory System ([`memory/`](file:///d:/Research-BanglaBBQ/memory))

- [`memory/README.md`](file:///d:/Research-BanglaBBQ/memory/README.md): **Mandatory Entry Point**. Research mission declaration, roles of Google Sheets / GitHub / memory, synchronization protocol, and mandatory research logging rules.
- [`memory/purpose.md`](file:///d:/Research-BanglaBBQ/memory/purpose.md): **Official Research Mission**. Historical thesis context, defects of legacy baseline, BBQ & PakBBQ methodological roles, 9 bias categories, bilingual standards, and publication roadmap.
- [`memory/state.md`](file:///d:/Research-BanglaBBQ/memory/state.md): **Current Verified Progress Dashboard**. Category-by-category status table, live Google Sheet IDs, active paths, and transparent research-quality blockers.
- [`memory/history.md`](file:///d:/Research-BanglaBBQ/memory/history.md): **Historical Research Log**. Chronological append-only milestone log documenting dataset transformations and bug fixes.
- [`memory/index.md`](file:///d:/Research-BanglaBBQ/memory/index.md): **Workspace Index & Repository Map** (this document).
- [`memory/personality.md`](file:///d:/Research-BanglaBBQ/memory/personality.md): **Communication Guidelines**. Guidelines defining assistant persona and response style. *(Does not override research integrity, dataset safety, or factual verification).*

> **Notice on `personal_info.md`**:  
> Developer personal profiles (e.g. `personal_info.md`), OAuth authentication secrets (`token.json`), and private communications are **intentionally git-ignored via `.gitignore`** to safeguard personal privacy. They are not part of the tracked public GitHub memory.

---

## 8. Permanent Research Logs ([`research_logs/`](file:///d:/Research-BanglaBBQ/research_logs))

- [`research_logs/README.md`](file:///d:/Research-BanglaBBQ/research_logs/README.md): Research logging guidelines, relationship to memory, and chronological index of all milestone logs.
- [`research_logs/2026-10-18_gender_identity_expansion_and_bilingual_qa.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-18_gender_identity_expansion_and_bilingual_qa.md): Complete milestone documentation of the 4,696-record English-Bengali Gender Identity migration, translation methodology, 34-theme structure, inherited defects audit, live Google Sheets parity (140,880 cells, 0 mismatches), exact formatting replication, and CI integration.
- [`research_logs/2026-10-18_religion_final_qa_and_validation.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-18_religion_final_qa_and_validation.md): Final research-quality QA across all 20 themes (2,880 rows/lang, V1+V2+V3); source verification across Q3/Q8–Q10/Q12–Q13 and 14 themes; evaluation split grouping safeguards; live Google Sheets 43,200-cell parity.
- [`research_logs/2026-10-17_religion_six_theme_evidence_repairs.md`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/research_logs/2026-10-17_religion_six_theme_evidence_repairs.md): verified sources, exact Q3/Q8/Q9/Q10/Q12/Q13 bilingual V1/V2/V3 repairs, protected 2,880-record backups, 43,200-field live parity and limitations.
- [`research_logs/2026-10-17_religion_source_verification_q3_q8_q9_q10_q12_q13.md`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/research_logs/2026-10-17_religion_source_verification_q3_q8_q9_q10_q12_q13.md): verified citation-to-scenario findings, source URLs, contradictions, six-theme production repair gates; current canonical Religion remains 2,880/language.
- [`research_logs/2026-10-17_religion_v2v3_expansion.md`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/research_logs/2026-10-17_religion_v2v3_expansion.md): full 2,880/language expansion method, backups, SHA-pinned shards, Sheets/JSONL read-back, CI validation and unresolved source review.
- [`research_logs/2026-10-17_religion_wording_variations_review.md`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/research_logs/2026-10-17_religion_wording_variations_review.md): Documents new 20-theme Religion V2/V3 review tab, 40 distinct bilingual candidate pairs, structural read-back checks, caveats, and future 48-row expansion gates.
- [`research_logs/2026-10-17_religion_qa_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_religion_qa_repair.md): Comprehensive log for Religion QA repairs across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20, source scrutiny/classification, counterfactual symmetry, and 100% bit-for-bit live Google Sheets parity.
- [`research_logs/politics_wording_expansion_20261017.md`](file:///d:/Research-BanglaBBQ/research_logs/politics_wording_expansion_20261017.md): Methods, shard lineage, backup details, live read-back QA and outstanding human linguistic/source audits for the 2,880-row Politics expansion.
- [`research_logs/2026-10-17_politics_q5_q14_q19_fixes.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_politics_q5_q14_q19_fixes.md): Forensic audit and synchronization of approved targeted repairs across Politics Q5 (historical date 2022), Q14 (dormitory belongings negative question refinement), and Q19 (government critic Bengali terminology).
- [`research_logs/TEMPLATE.md`](file:///d:/Research-BanglaBBQ/research_logs/TEMPLATE.md): Standardized template schema for authoring research and audit logs.
- [`research_logs/2026-10-17_age_q1_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q1_context_alignment.md): Retrospective audit and context alignment of Age Q1 expanding unique contexts from 11 to 16.
- [`research_logs/2026-10-17_age_q9_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q9_context_alignment.md): Retrospective audit and alignment of Age Q9 expanding unique contexts from 60 to 144 and aligning 272 answer options.
- [`research_logs/2026-10-17_age_q19_semantic_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q19_semantic_repair.md): Semantic translation repair of neighbor mistranslation and teen/teenager lexical distinction in Age Q19 (120 -> 140 unique contexts).
- [`research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md): Lexical distinctions across Zoomer vs Gen-Z kid, teen vs teenager, high schooler vs high school student, and fights vs confrontations.
- [`research_logs/2026-10-17_age_cultural_localization_audit.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_cultural_localization_audit.md): Forensic audit of Pakistani cultural/geographic entities in TM records (Q13–Q20) and recommendations for downstream bilingual alignment.

