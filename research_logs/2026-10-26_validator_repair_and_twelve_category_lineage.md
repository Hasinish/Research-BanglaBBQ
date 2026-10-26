# Research Log: BanglaBBQ 7-Category Invariant Validator Repair, CI Integration, and 12-Category Lineage Documentation

**Date**: 2026-10-26  
**Researcher / Agent**: Lead Dataset Integration Engineer / Antigravity Agent  
**Category**: Multi-Category (Physical Appearance, Regional Affiliation, Marital Status, Social Status, Health Status, Ethnicity, Occupational Background, Mental Health)  
**Milestone Scope**: `scripts/validate_seven_final_categories.py`, `.github/workflows/validate.yml`, `memory/state.md`, `memory/history.md`, and 12-Category Lineage Analysis  
**Status**: `VERIFIED COMPLETE / 100% CI & LOCAL SUITE PASS`  

---

## 1. Research Objective & Context

Following the successful synchronization of all seven finalized benchmark categories into the master Google Spreadsheet (14 worksheets, 20,160 rows, 302,400 data cells), the objective of this task was to:
1. Repair the validation harness `scripts/validate_seven_final_categories.py` to enforce strict ambiguous-context Unknown assertions, genuine 6-way answer permutation assertions ($3! = 6$), and comprehensive bilingual metadata parity.
2. Integrate the repaired validator directly into GitHub Actions CI (`.github/workflows/validate.yml`).
3. Execute all project validation suites to ensure zero regressions across the entire repository.
4. Correct outdated documentation in `memory/state.md` and repository indexes.
5. Provide a rigorous forensic investigation into the lineage of the benchmark: comparing the original 9 undergraduate thesis categories (BRACU Thesis T2510616, June 2025) with the current 12 working categories, explicitly addressing the relationship between `Mental Health` and `Health Status`.
6. Maintain absolute preservation of the historical thesis baseline (`Dataset_ BanglaBBQ_Old/`) and existing live Google Sheets records.

---

## 2. Source Files & Live Google Sheet References

- **Master Google Sheet**: [BanglaBBQ Master Spreadsheet](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit) (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`)
- **Canonical Benchmark Directory**: [`Dataset_BanglaBBQ_New/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New)
- **Historical Baseline Directory**: [`Dataset_ BanglaBBQ_Old/`](file:///d:/Research%20BanglaBBQ/Dataset_%20BanglaBBQ_Old)
- **Validator Script**: [`scripts/validate_seven_final_categories.py`](file:///d:/Research%20BanglaBBQ/scripts/validate_seven_final_categories.py)
- **GitHub Actions Workflow**: [`.github/workflows/validate.yml`](file:///d:/Research%20BanglaBBQ/.github/workflows/validate.yml)
- **Active 14 Worksheets Audited**:
  - `BanglaBBQ_ENG_PhysicalAppearance` (gid: `984262367`) & `BanglaBBQ_BEN_PhysicalAppearance` (gid: `934839633`)
  - `BanglaBBQ_ENG_SocialStatus` (gid: `1061280109`) & `BanglaBBQ_BEN_SocialStatus` (gid: `1761692098`)
  - `BanglaBBQ_ENG_HealthStatus` (gid: `577820949`) & `BanglaBBQ_BEN_HealthStatus` (gid: `1261981579`)
  - `BanglaBBQ_ENG_Regional` (gid: `1321419120`) & `BanglaBBQ_BEN_Regional` (gid: `786932138`)
  - `BanglaBBQ_ENG_Ethnicity` (gid: `210887456`) & `BanglaBBQ_BEN_Ethnicity` (gid: `1845601757`)
  - `BanglaBBQ_ENG_OccupationalBackground` (gid: `1499154542`) & `BanglaBBQ_BEN_OccupationalBackground` (gid: `934780717`)
  - `BanglaBBQ_ENG_MaritalStatus` (gid: `2049623557`) & `BanglaBBQ_BEN_MaritalStatus` (gid: `1929463163`)

---

## 3. Original Validator Defects & Forensic Repairs

### Defect 1: Ambiguous Condition String Check Typo
- **Symptom**: In `scripts/validate_seven_final_categories.py`, line 118 checked:
  ```python
  if 'ambiguous' in r['context_condition']:
  ```
- **Root Cause**: The BBQ schema defines `context_condition` values as `'ambig'` and `'disambig'`. Because the substring `'ambiguous'` was not present in `'ambig'`, the condition always evaluated to `False`. As a result, the code block enforcing that ambiguous contexts target the Unknown option was completely skipped!
- **Repair**: Corrected to:
  ```python
  if r['context_condition'] == 'ambig':
  ```
  and added an explicit check for the disambiguated condition:
  ```python
  elif r['context_condition'] == 'disambig':
      assert group_tag != 'unknown', (
          f"{lang.upper()} row {i} (EID {r.get('example_id')}): "
          f"Disambiguated context gold label must not be 'unknown'!"
      )
  ```

### Defect 2: Missing Bengali Unknown Terminology
- **Symptom**: Upon fixing Defect 1, the validator raised an assertion failure on row 0 of Bengali files:
  ```
  AssertionError: BEN row 0 (EID 0): Answer text 'নির্ধারণ করা যায় না' does not match expected Unknown terminology!
  ```
- **Root Cause**: The script's set `UNKNOWN_TERMS_BEN` only included `{"নির্ধারণ করা সম্ভব নয়", "অজানা"}`. The actual canonical Bengali files across the 7 final categories use the phrasing `"নির্ধারণ করা যায় না"` and `"নির্ধারণ করা যায় না"` (variations of 'y' / 'ya' unicode grapheme cluster).
- **Repair**: Updated `UNKNOWN_TERMS_BEN` to encompass all exact phrases:
  ```python
  UNKNOWN_TERMS_BEN = {
      'নির্ধারণ করা সম্ভব নয়',
      'নির্ধারণ করা সম্ভব নয়',
      'অজানা',
      'তথ্য অপর্যাপ্ত',
      'নির্ধারণ করা যায় না',
      'নির্ধারণ করা যায় না',
  }
  ```

### Defect 3: Permutation Verification Lacked Actual Assertions
- **Symptom**: The original validator printed:
  ```python
  print(f"[{cat}] Six-way answer permutation check: PASS")
  ```
  without containing any `assert` statement checking that all 6 permutations were present in each canonical block.
- **Repair**: Implemented strict block-level permutation tracking:
  ```python
  perms_in_block = set()
  for b_idx in range(len(rows) // 24):
      block = rows[b_idx * 24 : (b_idx + 1) * 24]
      block_perms = set()
      for r in block:
          ans_tuple = (r['ans0'], r['ans1'], r['ans2'])
          block_perms.add(ans_tuple)
      assert len(block_perms) == 6, (
          f"{lang.upper()} Block {b_idx} (EIDs {block[0]['example_id']}-{block[-1]['example_id']}): "
          f"Expected exactly 6 unique answer permutations, found {len(block_perms)}!"
      )
  ```

### Defect 4: Condition and Polarity 4-Row Ordering Verification
- **Enhancement**: Added invariant check verifying that every canonical 4-row sub-block strictly adheres to the standard BBQ cycle:
  `[('ambig', 'neg'), ('disambig', 'neg'), ('ambig', 'nonneg'), ('disambig', 'nonneg')]`.

### Defect 5: Bilingual Metadata and Schema Parity Assertions
- **Enhancement**: Strengthened cross-lingual assertions to verify that English and Bengali records match 1-to-1 on:
  - `example_id`, `question_index`, `context_condition`, `question_polarity`, `type`, `label`, `category`, `id`, `version`, `stereotyped_groups`, and `source`.
  - Semantic `answer_info` group tags across positions `ans0`, `ans1`, `ans2`.

---

## 4. Benchmark Category Lineage: 9 Thesis Categories vs. 12 Working Categories

A thorough forensic audit was conducted comparing the historical June 2025 BRACU undergraduate thesis (T2510616) with the active benchmark repository:

### The Original Nine Categories (Thesis T2510616 Baseline)
Preserved byte-for-byte in `Dataset_ BanglaBBQ_Old/`:
1. `Age`: 2,920 PakBBQ English rows, but only 799 rows translated into Bengali (`Age_Bengali_800entries.jsonl`).
2. `Educational background`: 128 legacy rows with severe label asymmetry and route reversals.
3. `Gender_identity`: 4,696 rows across 34 themes (subsequently repaired for collisions and Pakistani references).
4. `Marital Status`: 100 legacy rows.
5. `Mental Health`: 100 legacy rows in `Dataset_ BanglaBBQ_Old/Mental Health/`.
6. `Physical_appearance`: 1,106 English rows and 1,123 Bengali rows (a 17-record baseline mismatch).
7. `Politics`: 960 legacy rows.
8. `Regional`: 51 legacy rows.
9. `Religion`: 960 legacy rows.

### The Current Twelve Working Categories (`Dataset_BanglaBBQ_New/`)
Modernized to satisfy the rigorous BBQ specification (balanced labels, 6 permutations, 4 condition orderings, live Google Sheets parity):
1. **5 Expanded Pre-Existing Categories**:
   - `BanglaBBQ_Age`: 2,920 records/language (repaired for Q20 underage driving confounds and English localization).
   - `BanglaBBQ_EducationalBackground`: 2,880 records/language (expanded from 128 rows across 20 themes; verified against 23 adversarial fixtures).
   - `BanglaBBQ_Gender`: 4,696 records/language across 34 themes (repaired for Q54 grammar and Q56 probation considerations).
   - `BanglaBBQ_Politics`: 2,880 records/language across 20 themes (expanded with V2/V3 wording blocks; 960 rows each for positions 0, 1, 2).
   - `BanglaBBQ_Religion`: 2,880 records/language across 20 themes (V1+V2+V3, evidence-aligned revisions).
2. **3 Reconciled & Standardized Legacy Categories**:
   - `BanglaBBQ_MaritalStatus`: Expanded from 100 legacy rows to 1,440 rows (10 themes x 3 variations x 48 rows).
   - `BanglaBBQ_PhysicalAppearance`: Reconciled from the 1,106/1,123 mismatch to 1,440 balanced rows (10 themes x 3 variations x 48 rows).
   - `BanglaBBQ_Regional`: Expanded from 51 legacy rows to 1,440 balanced rows across 10 district themes.
3. **3 New Societal Bias Categories**:
   - `BanglaBBQ_Ethnicity`: 1,440 rows covering indigenous and ethnic minority stereotypes in Bangladesh (Chakma, Marma, Santhal, Bihari, Rohingya, etc.).
   - `BanglaBBQ_OccupationalBackground`: 1,440 rows covering blue-collar, RMG, domestic, and informal labor stereotypes.
   - `BanglaBBQ_SocialStatus`: 1,440 rows covering socioeconomic class divides and slum dweller stigmas.
4. **1 Health Category**:
   - `BanglaBBQ_HealthStatus`: 1,440 rows covering chronic, somatic, and infectious disease stigma.

---

## 5. Explicit Forensic Investigation: Mental Health vs. Health Status

An explicit inquiry was conducted to determine the relationship between `Mental Health` and `Health Status`:

1. **Thesis Baseline (`Mental Health`)**:
   - **File Locations**: `Dataset_ BanglaBBQ_Old/Mental Health/Mental_health_status_Eng.jsonl` and `Dataset_ BanglaBBQ_Old/Mental Health/Mental_health_status_Bengali_100entries.jsonl`.
   - **Content**: 100 historical records focused exclusively on psychiatric, neurological, and emotional conditions: generalized anxiety disorder, clinical depression, bipolar disorder, and schizophrenia.
2. **Modernized Benchmark (`Health Status`)**:
   - **File Locations**: `Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_english.jsonl` and `Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_bengali.jsonl`.
   - **Live Worksheets**: `BanglaBBQ_ENG_HealthStatus` (Sheet ID: `577820949`) and `BanglaBBQ_BEN_HealthStatus` (Sheet ID: `1261981579`).
   - **Content**: 1,440 standardized records across 10 themes focused on somatic, infectious, and physical medical stigmas prevalent in Bangladesh: arsenicosis, HIV/AIDS, leprosy, tuberculosis, hepatitis B, epilepsy, thalassemia, COVID-19 post-recovery stigma, and breast cancer.
3. **Governance Directive**:
   - The historical 100-row `Mental Health` dataset has NOT been deleted, overwritten, or modified. It is permanently preserved in `Dataset_ BanglaBBQ_Old/Mental Health/`.
   - `Health Status` is an independent, 1,440-row somatic health benchmark.
   - Per strict project governance instructions, **neither category has been renamed, removed, or merged**. Any future convergence or expansion of psychiatric mental health bias will require explicit authorization from the lead researcher.

---

## 6. Continuous Integration Workflow Updates

The repaired validator was integrated into `.github/workflows/validate.yml` as a dedicated step following the existing benchmark suites:

```yaml
      - name: Validate Seven Final Categories Invariants
        run: |
          python scripts/validate_seven_final_categories.py
```

This guarantees that any regression in answer permutations, unknown targeting, condition cycling, or bilingual metadata across the 20,160 records will fail CI automatically.

---

## 7. Quality Assurance & Test Execution Summary

All 10 offline test suites were executed sequentially in the workspace with 100% success:

| # | Test Suite Script | Scope | Result | Details |
| :-: | :--- | :--- | :-: | :--- |
| 1 | `scripts/validate_politics_dataset.py` (Historical) | Historical Politics (960 rows) | **PASS** | 11/11 invariants; baseline SHA256 hashes verified |
| 2 | `scripts/validate_politics_dataset.py` (Active) | Active Politics (2,880 rows) | **PASS** | 11/11 invariants; post-expansion SHA256 verified |
| 3 | `scripts/validate_religion_dataset.py` | Active Religion (2,880 rows) | **PASS** | 10/10 invariants; V1+V2+V3 wave checks passed |
| 4 | `scripts/apply_age_english_localization_20261018.py` | Active Age (2,920 rows) | **PASS** | 10/10 invariants; zero underage drivers in Q20 |
| 5 | `scripts/validate_gender_dataset.py` | Active Gender (4,696 rows) | **PASS** | 10/10 structural invariants; 0 Pakistani references |
| 6 | `scripts/validate_gender_semantics.py` | Active Gender (4,696 rows) | **PASS** | 6/6 role-entailment checks; 0 disambiguated collisions |
| 7 | `scripts/validate_education_dataset.py` | Active Education (2,880 rows) | **PASS** | 10/10 structural invariants; 960/960/960 labels |
| 8 | `scripts/validate_education_semantics.py` | Active Education (2,880 rows) | **PASS** | 8/8 deep predicate and clause entailment checks |
| 9 | `scripts/test_education_semantic_fixtures.py` | Active Education (Adversarial) | **PASS** | 23/23 adversarial fixtures rejected (100% detection) |
| 10 | `scripts/validate_seven_final_categories.py` | 7 Final Categories (20,160 rows) | **PASS** | 10/10 invariants across all 14 files; 6 permutations verified |

---

## 8. Unresolved Research-Quality Limitations

In strict adherence to research integrity standards:
1. **No Linguistic Peer Certification**: While all datasets pass automated structural, schema, and lexical invariant validation, **independent native colloquial Bengali linguistic review** by external Bangladeshi evaluators has not yet been conducted across the 7 newly standardized categories.
2. **No Clinical / Anthropological Verification**: The somatic condition themes in `Health Status` and ethnic minority themes in `Ethnicity` have not undergone formal peer review by Bangladeshi medical practitioners or anthropological scholars.
3. **Synthetic Paraphrase Expansion**: Scenarios V2 and V3 across the expanded categories represent systematically controlled linguistic variations designed to prevent template memorization; they do NOT constitute independently documented real-world discrimination incidents.
4. **Historical Mental Health Gap**: The 100-entry legacy `Mental Health` dataset remains unexpanded and unstandardized. It is preserved for thesis reproducibility, but cannot be used for robust evaluation without expansion.
