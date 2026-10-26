# Research Log: Workspace Directory Reorganization & Clutter Cleanup

- **Date**: 2026-10-26
- **Topic**: Workspace Directory Reorganization & Clutter Reduction
- **Status**: `VERIFIED COMPLETE / 100% CI PASS`
- **Related Commits**: `214795f` (7 category bundles), `dc1bc0a` (7 forensic QA bundles)

---

## 1. Context & Motivation

Following the push of 7 new candidate benchmark bundles and 7 independent forensic QA complete packages in recent commits, 14 directories and multiple loose legacy files were located directly in the workspace root. This caused severe cognitive clutter and hindered developer navigation across the 40+ top-level root items.

The objective of this task was to safely reorganize the workspace into logical, clean directories without altering internal bundle logic or breaking active CI workflows.

---

## 2. Reorganization Schema

### A. Independent Forensic QA Packages (`audits/`)
The seven forensic QA complete packages (containing audited JSONLs, adversarial test suites, issue ledgers, change manifests, and reproducibility logs) were moved under `audits/`:
- `audits/Ethnicity_forensic_QA_complete/`
- `audits/health_status_complete_independent_forensic_QA/`
- `audits/marital_status_independent_forensic_QA_bundle/`
- `audits/occupational_background_forensic_QA_complete/`
- `audits/physical_appearance_independent_forensic_QA_bundle/`
- `audits/Regional_independent_forensic_QA_bundle/`
- `audits/banglabbq_social_status_forensic_QA_complete/`

### B. Candidate Generation Bundles (`candidate_bundles/`)
The seven pre-audit candidate benchmark bundles and their generator scripts were moved under `candidate_bundles/`:
- `candidate_bundles/banglabbq_ethnicity_bundle/`
- `candidate_bundles/banglabbq_health_status_complete/`
- `candidate_bundles/banglabbq_marital_status_readonly_research_package/`
- `candidate_bundles/banglabbq_occupational_background_readonly_bundle/`
- `candidate_bundles/banglabbq_physical_appearance_readonly_research_bundle/`
- `candidate_bundles/banglabbq_regional_research_bundle/`
- `candidate_bundles/banglabbq_social_status_complete/`

### C. Academic Papers & Reports (`docs/`)
- Academic papers moved to `docs/papers/`:
  - `docs/papers/T2510616.pdf`
  - `docs/papers/T2510616_IEEE_Paper.pdf`
- Historical expansion and correction JSON reports moved to `docs/reports/`:
  - `docs/reports/modified_records_report.json`
  - `docs/reports/p1_p2_report_data.json`
  - `docs/reports/politics_240_expansion_report.json`
  - `docs/reports/politics_correction_report.json`

### D. Production Benchmark Categories (Preserved in Root for Zero CI Breakage)
The following active benchmarks remain at their canonical root paths to guarantee backward compatibility with GitHub Actions CI workflows (`validate.yml`, `assemble_politics_expansion.yml`, `assemble_religion_expansion.yml`) and existing evaluation scripts:
- `BanglaBBQ_Politics/`
- `BanglaBBQ_Religion/`
- `BanglaBBQ_Gender/`
- `BanglaBBQ_EducationalBackground/`
- `BanglaBBQ_BEN_New/` & `BanglaBBQ_ENG_New/` (Age Benchmark)
- `Dataset_ BanglaBBQ_Old/` (Senior Thesis Baseline)
- `PakBBQ_Repo/` & `PakBBQ_Age_English.csv` (PakBBQ reference baselines)

---

## 3. Verification & Validation Evidence

All existing invariant test suites and semantic regression suites were executed locally against the reorganized tree:

1. **Politics**:
   - `python scripts/validate_politics_dataset.py "Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl" "Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl"` -> **PASS**
   - `python scripts/validate_politics_dataset.py BanglaBBQ_Politics/banglabbq_politics_english.jsonl BanglaBBQ_Politics/banglabbq_politics_bengali.jsonl` -> **PASS**
2. **Religion**:
   - `python scripts/validate_religion_dataset.py BanglaBBQ_Religion/Religion_eng.jsonl BanglaBBQ_Religion/Religion_bng.jsonl` -> **PASS**
3. **Age**:
   - `python scripts/apply_age_english_localization_20261018.py` -> **PASS**
4. **Gender Identity**:
   - `python scripts/validate_gender_dataset.py BanglaBBQ_Gender/Gender_identity_eng.jsonl BanglaBBQ_Gender/Gender_identity_bng.jsonl` -> **PASS**
   - `python scripts/validate_gender_semantics.py BanglaBBQ_Gender/Gender_identity_eng.jsonl BanglaBBQ_Gender/Gender_identity_bng.jsonl` -> **PASS**
5. **Educational Background**:
   - `python scripts/validate_education_dataset.py BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl` -> **PASS**
   - `python scripts/validate_education_semantics.py BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl` -> **PASS**
   - `python scripts/test_education_semantic_fixtures.py` -> **23/23 PASSED (100% REJECTION RATE)**
