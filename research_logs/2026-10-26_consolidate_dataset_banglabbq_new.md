# Research Log: Consolidating All 12 Benchmark Categories into `Dataset_BanglaBBQ_New`

- **Date**: 2026-10-26
- **Topic**: Modernized Benchmark Consolidation into `Dataset_BanglaBBQ_New/`
- **Status**: `VERIFIED COMPLETE / 100% CI PASS`
- **Related Commits**: `3b7000c`, `dc1bc0a`, `214795f`

---

## 1. Context & Motivation

Following the successful migration, semantic QA verification, and formatting of all active benchmark categories, the project contained 12 individual top-level category directories matching `BanglaBBQ_<category>` sitting in the workspace root:
- `BanglaBBQ_Age` (2,920 records/lang)
- `BanglaBBQ_EducationalBackground` (2,880 records/lang)
- `BanglaBBQ_Ethnicity` (1,440 records/lang)
- `BanglaBBQ_Gender` (4,696 records/lang)
- `BanglaBBQ_HealthStatus` (1,440 records/lang)
- `BanglaBBQ_MaritalStatus` (1,440 records/lang)
- `BanglaBBQ_OccupationalBackground` (1,440 records/lang)
- `BanglaBBQ_PhysicalAppearance` (1,440 records/lang)
- `BanglaBBQ_Politics` (2,880 records/lang)
- `BanglaBBQ_Regional` (1,440 records/lang)
- `BanglaBBQ_Religion` (2,880 records/lang)
- `BanglaBBQ_SocialStatus` (1,440 records/lang)

Sitting alongside the historical seniors' thesis baseline (`Dataset_ BanglaBBQ_Old/`), this caused visual disorganization and lacked an intuitive mirror structure.

To establish structural parity and architectural clarity, all 12 categories were consolidated into a unified master directory: `Dataset_BanglaBBQ_New/`.

---

## 2. Structural Schema

```
Research-BanglaBBQ/
├── Dataset_BanglaBBQ_New/            # Canonical Modernized Benchmark (12 Categories)
│   ├── BanglaBBQ_Age/                # 2,920 rows/lang (English & Bengali canonical JSONLs)
│   ├── BanglaBBQ_EducationalBackground/ # 2,880 rows/lang (20 themes, V1/V2/V3)
│   ├── BanglaBBQ_Ethnicity/          # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_Gender/             # 4,696 rows/lang (34 themes, 100% live parity)
│   ├── BanglaBBQ_HealthStatus/       # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_MaritalStatus/      # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_OccupationalBackground/ # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_PhysicalAppearance/ # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_Politics/           # 2,880 rows/lang (20 themes, V1/V2/V3)
│   ├── BanglaBBQ_Regional/           # 1,440 rows/lang (FINAL canonical JSONLs)
│   ├── BanglaBBQ_Religion/           # 2,880 rows/lang (20 themes, V1/V2/V3)
│   └── BanglaBBQ_SocialStatus/       # 1,440 rows/lang (FINAL canonical JSONLs)
├── Dataset_ BanglaBBQ_Old/           # Historical thesis working tree (preserved byte-for-byte)
├── audits/                           # Independent Forensic QA Complete Packages (7 categories)
├── candidate_bundles/                # Pre-Audit Candidate Benchmark Bundles & Generators
├── docs/                             # Academic papers & historical audit reports
├── scripts/                          # Invariant validation, assembly & synchronization tooling
├── backups/                          # Versioned immutable pre-repair backups
└── memory/                           # Agent state dashboard, index, and audit trail
```

---

## 3. Workflow & Tooling Updates

1. **GitHub Actions Workflows**:
   - `.github/workflows/validate.yml`: Updated all test paths for Politics, Religion, Age, Gender, and Educational Background to point to `Dataset_BanglaBBQ_New/...`.
   - `.github/workflows/assemble_politics_expansion.yml`: Updated push path trigger and file validation paths to `Dataset_BanglaBBQ_New/BanglaBBQ_Politics/...`.
   - `.github/workflows/assemble_religion_expansion.yml`: Updated push path triggers, patch manifests, and validation paths to `Dataset_BanglaBBQ_New/BanglaBBQ_Religion/...`.

2. **Validation & Assembly Scripts**:
   - Updated default path resolution and fallback mechanisms across 24 scripts in `scripts/`:
     - `apply_age_english_localization_20261018.py`
     - `sync_and_validate_age.py`
     - `audit_cultural_localization.py`
     - `assemble_politics_expansion.py`
     - `assemble_religion_expansion.py`
     - `apply_religion_evidence_revisions.py`
     - `audit_religion_sources_and_translation.py`
     - `validate_religion_dataset.py`
     - `validate_gender_dataset.py`
     - `validate_gender_semantics.py`
     - `validate_education_dataset.py`
     - `validate_education_semantics.py`
     - `test_education_semantic_fixtures.py`
     - `verify_religion_live.py`
     - `verify_gender_live_parity.py`
     - `verify_education_live_parity.py`
     - `sync_education_sheets.py`
     - `upload_sparse_gender_updates.py`
     - `upload_bengali_gender_sheets.py`
     - `generate_gender_dataset.py`
     - `build_scenario_templates.py`
     - `backup_pre_repair.py`
     - `backup_and_export_religion.py`
     - `repair_politics_dataset.py`

---

## 4. Empirical Verification & Invariant Pass Rates

All local test suites were executed against the new paths and passed 100%:
- **Politics Invariant Validator**: 11/11 Checks PASS (2,880 rows/lang).
- **Religion Invariant Validator**: 10/10 Checks PASS (2,880 rows/lang).
- **Age Reproduction & Localization**: 10/10 Invariant Checks PASS (2,920 rows/lang).
- **Gender Identity Invariants & Semantics**: 10/10 Structural PASS, 6/6 Role Entailment PASS (4,696 rows/lang, 0 collisions, 0 Pakistani references).
- **Educational Background Invariants & Semantics**: 10/10 Structural PASS, 8/8 Deep Semantic Checks PASS (2,880 rows/lang).
- **Adversarial Regression Test Suite**: 23/23 Fixtures Rejected (100% defect rejection rate).
- **Assembly Engines**: Both `assemble_politics_expansion.py` and `assemble_religion_expansion.py` verified and synchronized without regressions.
