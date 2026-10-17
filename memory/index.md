# Workspace Index & Repository Map

> **VERIFIED REPOSITORY MAP**  
> Every path listed in this index has been verified to exist on disk. Active production datasets are strictly separated from legacy baseline directories.

---

## 1. Directory Structure Overview

```
Research-BanglaBBQ/
├── .github/workflows/           # Automated CI workflows (invariant validation)
├── BanglaBBQ_Politics/          # Active Politics benchmark (2,880 ENG, 2,880 BEN; base + V2/V3)
├── BanglaBBQ_Religion/          # Active verified Religion benchmark (960 ENG, 960 BEN)
├── BanglaBBQ_BEN_New/           # Active verified Bengali Age benchmark (2,920 BEN)
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
- [`Religion_eng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion/Religion_eng.jsonl): 960 records across 20 source-grounded themes (Q1–Q20), 48 records per theme. Full 6-way answer permutations ($3!$), canonical 4-row block sequence, uniform label balance (320/320/320), 0 duplicates, 15-column schema. Approved QA repairs applied across Q2–Q20 (Q3 equal water access premise, Q5 nonreligious/observant Muslim distinction, Q7 civic health project reframing, Q8 clerical job denial, Q9/Q10 academic classroom study citations, Q12/Q13 MRG public exclusion citations, Q18 Feni flood relief grounding, Q20 Chittagong government high school quota grounding).
- [`Religion_bng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion/Religion_bng.jsonl): 960 parallel Bengali records with 100% structural parity and 100% bit-for-bit agreement with live Google Sheet `BanglaBBQ_BEN_Religion`.
- **Status**: `IN PROGRESS` (Structurally validated and synchronized with live sheets; source relevance boundaries formalized; secondary native Bengali linguistic review pending; not publication-ready).

### C. Age ([`BanglaBBQ_BEN_New/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New) & Root)
- [`PakBBQ_Age_English.csv`](file:///d:/Research-BanglaBBQ/PakBBQ_Age_English.csv): 2,920 English records adapted from PakBBQ (1,872 DT + 1,048 TM).
- [`BanglaBBQ_BEN_New/Age.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New/Age.jsonl): 2,920 parallel Bengali records translated and audited for family relationship terms (নানা/নানি, দাদু/নাতিটি) and Q7 comparative formulation.
- **Status**: `IN PROGRESS` (Translation complete; pending cultural localization of Pakistani entities in TM records 1,872–2,919).

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
- [`scripts/validate_religion_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_religion_dataset.py): 10-invariant offline validator for Religion (counts, 15-column schema, 48 rows/theme, 6-way permutations, ambig/disambig grounding, bilingual parity, 0 duplicates).
- [`.github/workflows/validate.yml`](file:///d:/Research-BanglaBBQ/.github/workflows/validate.yml): Automated GitHub Actions CI workflow executing offline validators on every push and pull request.

### Live Google Sheets Sync & Verification
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
- [`research_logs/2026-10-17_religion_qa_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_religion_qa_repair.md): Comprehensive log for Religion QA repairs across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20, source scrutiny/classification, counterfactual symmetry, and 100% bit-for-bit live Google Sheets parity.
- [`research_logs/politics_wording_expansion_20261017.md`](file:///d:/Research-BanglaBBQ/research_logs/politics_wording_expansion_20261017.md): Methods, shard lineage, backup details, live read-back QA and outstanding human linguistic/source audits for the 2,880-row Politics expansion.
- [`research_logs/2026-10-17_politics_q5_q14_q19_fixes.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_politics_q5_q14_q19_fixes.md): Forensic audit and synchronization of approved targeted repairs across Politics Q5 (historical date 2022), Q14 (dormitory belongings negative question refinement), and Q19 (government critic Bengali terminology).
- [`research_logs/TEMPLATE.md`](file:///d:/Research-BanglaBBQ/research_logs/TEMPLATE.md): Standardized template schema for authoring research and audit logs.
- [`research_logs/2026-10-17_age_q1_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q1_context_alignment.md): Retrospective audit and context alignment of Age Q1 expanding unique contexts from 11 to 16.
- [`research_logs/2026-10-17_age_q9_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q9_context_alignment.md): Retrospective audit and alignment of Age Q9 expanding unique contexts from 60 to 144 and aligning 272 answer options.
- [`research_logs/2026-10-17_age_q19_semantic_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q19_semantic_repair.md): Semantic translation repair of neighbor mistranslation and teen/teenager lexical distinction in Age Q19 (120 -> 140 unique contexts).
- [`research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md): Lexical distinctions across Zoomer vs Gen-Z kid, teen vs teenager, high schooler vs high school student, and fights vs confrontations.
- [`research_logs/2026-10-17_age_cultural_localization_audit.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_cultural_localization_audit.md): Forensic audit of Pakistani cultural/geographic entities in TM records (Q13–Q20) and recommendations for downstream bilingual alignment.

