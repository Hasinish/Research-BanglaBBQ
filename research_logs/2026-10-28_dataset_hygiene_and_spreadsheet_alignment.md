# Research Log: Dataset Hygiene and Spreadsheet Naming Alignment

**Date**: 2026-10-28  
**Author**: Antigravity (AI Research & Release Engineer)  
**Topic**: Canonical Dataset Hygiene, Non-Dataset Artifact Migration, and Google Spreadsheet Tab Naming Alignment

---

## 1. Objective

Standardize the canonical production benchmark directory `Dataset_BanglaBBQ_New/` so that:
1. `Dataset_BanglaBBQ_New/` and all its category subdirectories strictly contain ONLY English and Bengali JSONL files (`*.jsonl`).
2. All non-dataset files (manifests, audit matrices, scenario templates, review folders, shards, and CSVs) are moved completely outside of `Dataset_BanglaBBQ_New/` into dedicated `metadata/<CategoryName>/` directories.
3. Every single JSONL file in `Dataset_BanglaBBQ_New/` is renamed to mirror the exact corresponding worksheet tab name from the master Google Spreadsheet (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`).

---

## 2. Directory Transformation Summary

### Before
`Dataset_BanglaBBQ_New/` contained inconsistent JSONL filenames (e.g., `Religion_bng.jsonl`, `Gender_identity_eng.jsonl`, `banglabbq_education_english.jsonl`, `BanglaBBQ_Health_Status_FINAL_english.jsonl`) alongside stray CSVs, JSON manifests, and nested review/expansion shard subdirectories.

### After
`Dataset_BanglaBBQ_New/` contains exactly 24 files across 12 category subdirectories (exactly 1 English and 1 Bengali JSONL per category). Zero non-JSONL files exist in `Dataset_BanglaBBQ_New/`.

| Category Directory | English JSONL File | Bengali JSONL File | Corresponding Google Sheets Tab |
| :--- | :--- | :--- | :--- |
| `BanglaBBQ_Age/` | `BanglaBBQ_ENG_Age.jsonl` | `BanglaBBQ_BEN_Age.jsonl` | `BanglaBBQ_ENG_Age` / `BanglaBBQ_BEN_Age` |
| `BanglaBBQ_EducationalBackground/` | `BanglaBBQ_ENG_Education.jsonl` | `BanglaBBQ_BEN_Education.jsonl` | `BanglaBBQ_ENG_Education` / `BanglaBBQ_BEN_Education` |
| `BanglaBBQ_Ethnicity/` | `BanglaBBQ_ENG_Ethnicity.jsonl` | `BanglaBBQ_BEN_Ethnicity.jsonl` | `BanglaBBQ_ENG_Ethnicity` / `BanglaBBQ_BEN_Ethnicity` |
| `BanglaBBQ_Gender/` | `BanglaBBQ_ENG_Gender.jsonl` | `BanglaBBQ_BEN_Gender.jsonl` | `BanglaBBQ_ENG_Gender` / `BanglaBBQ_BEN_Gender` |
| `BanglaBBQ_HealthStatus/` | `BanglaBBQ_ENG_HealthStatus.jsonl` | `BanglaBBQ_BEN_HealthStatus.jsonl` | `BanglaBBQ_ENG_HealthStatus` / `BanglaBBQ_BEN_HealthStatus` |
| `BanglaBBQ_MaritalStatus/` | `BanglaBBQ_ENG_MaritalStatus.jsonl` | `BanglaBBQ_BEN_MaritalStatus.jsonl` | `BanglaBBQ_ENG_MaritalStatus` / `BanglaBBQ_BEN_MaritalStatus` |
| `BanglaBBQ_OccupationalBackground/` | `BanglaBBQ_ENG_OccupationalBackground.jsonl` | `BanglaBBQ_BEN_OccupationalBackground.jsonl` | `BanglaBBQ_ENG_OccupationalBackground` / `BanglaBBQ_BEN_OccupationalBackground` |
| `BanglaBBQ_PhysicalAppearance/` | `BanglaBBQ_ENG_PhysicalAppearance.jsonl` | `BanglaBBQ_BEN_PhysicalAppearance.jsonl` | `BanglaBBQ_ENG_PhysicalAppearance` / `BanglaBBQ_BEN_PhysicalAppearance` |
| `BanglaBBQ_Politics/` | `BanglaBBQ_ENG_Politics.jsonl` | `BanglaBBQ_BEN_Politics.jsonl` | `BanglaBBQ_ENG_Politics` / `BanglaBBQ_BEN_Politics` |
| `BanglaBBQ_Regional/` | `BanglaBBQ_ENG_Regional.jsonl` | `BanglaBBQ_BEN_Regional.jsonl` | `BanglaBBQ_ENG_Regional` / `BanglaBBQ_BEN_Regional` |
| `BanglaBBQ_Religion/` | `BanglaBBQ_ENG_Religion.jsonl` | `BanglaBBQ_BEN_Religion.jsonl` | `BanglaBBQ_ENG_Religion` / `BanglaBBQ_BEN_Religion` |
| `BanglaBBQ_SocialStatus/` | `BanglaBBQ_ENG_SocialStatus.jsonl` | `BanglaBBQ_BEN_SocialStatus.jsonl` | `BanglaBBQ_ENG_SocialStatus` / `BanglaBBQ_BEN_SocialStatus` |

---

## 3. Non-Dataset Artifact Migration to `metadata/`

The following files and folders were migrated from `Dataset_BanglaBBQ_New/` into dedicated `metadata/` subdirectories:

1. `BanglaBBQ_Age`:
   - `PakBBQ_Age_English.csv` -> `metadata/BanglaBBQ_Age/PakBBQ_Age_English.csv`
2. `BanglaBBQ_EducationalBackground`:
   - `expansion_manifest.json` -> `metadata/BanglaBBQ_EducationalBackground/expansion_manifest.json`
   - `legacy_to_improved_mapping.json` -> `metadata/BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`
   - `qa_repair_diff_manifest.json` -> `metadata/BanglaBBQ_EducationalBackground/qa_repair_diff_manifest.json`
   - `scenario_templates.json` -> `metadata/BanglaBBQ_EducationalBackground/scenario_templates.json`
   - `source_audit_matrix.json` -> `metadata/BanglaBBQ_EducationalBackground/source_audit_matrix.json`
   - `source_audit_matrix.md` -> `metadata/BanglaBBQ_EducationalBackground/source_audit_matrix.md`
3. `BanglaBBQ_Gender`:
   - `review/` -> `metadata/BanglaBBQ_Gender/review/` (10 patch/review JSON files)
4. `BanglaBBQ_Politics`:
   - `expansion_v2v3_20261017/` -> `metadata/BanglaBBQ_Politics/expansion_v2v3_20261017/` (10 shard/template files)
5. `BanglaBBQ_Religion`:
   - `evidence_revisions_20261017.json` -> `metadata/BanglaBBQ_Religion/evidence_revisions_20261017.json`
   - `review_v2v3_20261017.json` -> `metadata/BanglaBBQ_Religion/review_v2v3_20261017.json`
   - `expansion_v2v3_20261017/` -> `metadata/BanglaBBQ_Religion/expansion_v2v3_20261017/` (18 context templates and shard files)

---

## 4. Cryptographic & Invariant Verification

1. **Bit-for-Bit Hash Preservation**:
   - SHA-256 hashes of all 24 JSONL files were computed prior to renaming and verified after renaming.
   - Exact 100.0% match on all 24 hashes (0 byte difference, zero content drift).
2. **Automated Validation Suite Pass**:
   - Updated `.github/workflows/validate.yml` to reflect new canonical paths.
   - Updated path defaults in validation scripts (`scripts/validate_seven_final_categories.py`, `scripts/verify_seven_final_categories_live.py`, `scripts/apply_age_english_localization_20261018.py`, `scripts/validate_education_semantics.py`, `scripts/test_education_semantic_fixtures.py`, `scripts/validate_politics_dataset.py`, `scripts/validate_religion_dataset.py`, `scripts/validate_gender_dataset.py`).
   - Ran all offline test suites locally:
     - `validate_politics_dataset.py` (Old & New): PASS
     - `validate_religion_dataset.py`: PASS (10/10 checks)
     - `apply_age_english_localization_20261018.py`: PASS (2,920 records/lang)
     - `validate_gender_dataset.py`: PASS (10/10 checks)
     - `validate_gender_semantics.py`: PASS (100% clean)
     - `validate_education_dataset.py`: PASS (10/10 checks)
     - `validate_education_semantics.py`: PASS (100% clean)
     - `test_education_semantic_fixtures.py`: PASS (23/23 adversarial fixtures rejected)
     - `validate_seven_final_categories.py`: PASS (14/14 files, 14,400 tracked IDs)
