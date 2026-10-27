# BanglaBBQ — Master QA Summary Report
**Controlled Final Quality Repair & Independent Audit**
**Date**: October 27–28, 2026  
**Auditor/Engineer**: Senior NLP Researcher + Dataset Engineer + Independent QA Auditor  
**Baseline Git Commit SHA**: `b4069d9cb9b20bf9466eb825ce7feacfb01d6fca`  
**Master Google Spreadsheet**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY` (Sync Status: Verified 100% Concordance, 0 Discrepancies)

---

## 1. Executive Summary
This QA audit and repair package addresses the remaining structural, positional, and methodological defects across the seven modernized BanglaBBQ benchmark categories. 

All repair procedures were executed under **Strict Read-Only Production Protocols**:
- No canonical production files in `Dataset_BanglaBBQ_New/` were edited.
- No live Google Sheets were modified.
- No remote Git commits or pushes were executed.
- All candidate datasets, diffs, audits, and validation logs are sequestered inside `local_candidates/final_seven_category_qa/`.

---

## 2. Phase 1 — Positional Introduction-Order Repair

### Verified Positional-Balance Statistics Across Categories
Prior to repair, Health Status, Regional Affiliation, and Ethnicity suffered from a severe structural shortcut where the correct answer in negative disambiguated scenarios was always the first-introduced entity (360 First / 0 Second), and in non-negative disambiguated scenarios was always the second-introduced entity (0 First / 360 Second). 

Applying the orthogonal 15-variation reversal pattern (5 V1, 5 V2, 5 V3 across Themes Q01–Q10) under the verified formula `start_id = (variation - 1) * 480 + (question_index - 1) * 48` achieves exact 50.0% / 50.0% balance at the category level across both polarities and both languages without altering labels, answer options, questions, or metadata.

| Category | Language | Baseline Disambig NEG (1st / 2nd) | Baseline Disambig NONNEG (1st / 2nd) | Candidate Disambig NEG (1st / 2nd) | Candidate Disambig NONNEG (1st / 2nd) | Category Level Status |
|---|---|---|---|---|---|---|
| **Health Status** | English | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Health Status** | Bengali | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Regional Affiliation** | English | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Regional Affiliation** | Bengali | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Ethnicity** | English | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Ethnicity** | Bengali | 360 / 0 (100% / 0%) | 0 / 360 (0% / 100%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | **EXACT 50/50** |
| **Physical Appearance** | EN / BN | 180 / 180 (50% / 50%) | 180 / 180 (50% / 50%) | 180 / 180 *(Untouched)* | 180 / 180 *(Untouched)* | **EXACT 50/50** |
| **Social Status** | EN / BN | 180 / 180 (50% / 50%) | 180 / 180 (50% / 50%) | 180 / 180 *(Benchmark)* | 180 / 180 *(Benchmark)* | **EXACT 50/50** |
| **Occupational Background**| EN / BN | 180 / 180 (50% / 50%) | 180 / 180 (50% / 50%) | 180 / 180 *(Benchmark)* | 180 / 180 *(Benchmark)* | **EXACT 50/50** |
| **Marital Status** | EN / BN | 180 / 180 (50% / 50%) | 180 / 180 (50% / 50%) | 180 / 180 *(Benchmark)* | 180 / 180 *(Benchmark)* | **EXACT 50/50** |

---

## 3. Phase 2 — Theme-Level Balancing & Combinatorial Constraints

### Theme-Level Indexing & Combinatorial Proof
The canonical dataset structure orders records in variation-major layout:
`start_id = (variation - 1) * 480 + (question_index - 1) * 48`

1. Each scenario variation contains 48 rows with complete 6-way answer permutations across 2 counterfactual orientations ('a' and 'b') and 2 question polarities ('neg' and 'nonneg').
2. In each variation, exactly 12 examples represent negative disambiguated contexts.
3. Therefore, reversing the introductory order of a whole variation shifts position counts in discrete blocks of **12 units**.
4. In a 3-variation theme (containing 36 negative disambiguated examples), whole-variation reversals can only yield splits of:
   - 0 reversals: 36 First / 0 Second (100% fatal shortcut)
   - 1 reversal: 24 First / 12 Second (2:1 ratio)
   - 2 reversals: 12 First / 24 Second (1:2 ratio)
   - 3 reversals: 0 First / 36 Second (100% fatal inverted shortcut)
5. Because 18 is not divisible by 12, **it is mathematically impossible to achieve an 18/18 split via whole-variation reversals**.
6. Achieving 18/18 per theme would require splitting counterfactual orientations (e.g., reversing only orientation 'b'), which rigidly binds target demographic identity to introduction position, introducing severe demographic confounding.
7. Consequently, theme-level counts are **improved from 36/0 to 24/12 or 12/24**, but remain **2:1 imbalanced**.
8. **Terminology Rule**: Reserve the label `EXACT 50/50` strictly for category-level totals (180/180). Individual themes are classified as `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW`.

### Theme-by-Theme Position Counts (Disambiguated Negative)
*(Identical across Health Status, Regional Affiliation, and Ethnicity candidates in both English and Bengali)*

| Theme ID | Focus / Domain | Baseline (1st / 2nd) | Candidate (1st / 2nd) | Reversed Variations | Theme-Level Classification |
|---|---|---|---|---|---|
| **Q01** | HIV / Noakhali / Munda | 36 / 0 | **12 / 24** | V1, V2 (2 vars) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q02** | HIV (Clinic) / Barishal / Chakma | 36 / 0 | **12 / 24** | V1, V3 (2 vars) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q03** | TB / Tangail / Chakma | 36 / 0 | **12 / 24** | V2, V3 (2 vars) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q04** | TB (Public) / Cumilla / Chakma | 36 / 0 | **12 / 24** | V1, V2 (2 vars) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q05** | COVID-19 / Rangpur / Garo | 36 / 0 | **12 / 24** | V1, V3 (2 vars) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q06** | Thalassemia / Sylhet / Santal | 36 / 0 | **24 / 12** | V1 (1 var) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q07** | Burn Scars / Sylhet / Mro | 36 / 0 | **24 / 12** | V2 (1 var) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q08** | Leprosy / Chattogram / Santal | 36 / 0 | **24 / 12** | V2 (1 var) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q09** | Hepatitis B / Chattogram / Marma | 36 / 0 | **24 / 12** | V3 (1 var) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Q10** | Hepatitis B / Dhaka / Marma | 36 / 0 | **24 / 12** | V3 (1 var) | `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW` |
| **Total** | **Category Summary** | **360 / 0** | **180 / 180** | **15 vars (5 V1, 5 V2, 5 V3)** | **EXACT 50/50** |

---

## 4. Phase 3 & 4 — Candidate Verification & Artifact Manifest

### Generated Candidate Datasets (Verified SHA-256 Hashes)
All candidate files contain exactly 1,440 records, sequential IDs 0–1439, complete 6-way permutations, and identical schemas:

- `candidates/BanglaBBQ_Health_Status_FINAL_english.jsonl`:  
  `eacb118018cebf02492955b2e0b6ada05e96fa1e72bc23291c8f55156e377f11`
- `candidates/BanglaBBQ_Health_Status_FINAL_bengali.jsonl`:  
  `16996de2013f4a45bae46b99c3b6e8b4f5e99bfd2955247c079b507871350f60`
- `candidates/BanglaBBQ_Regional_FINAL_english.jsonl`:  
  `fcf4414af7ba9c88bbdf3112302e6976b7de8ba6e1e370f52ecab312677bbb49`
- `candidates/BanglaBBQ_Regional_FINAL_bengali.jsonl`:  
  `5846999cf4b4aab40fb3b8ab45d8a83cc81a2f82bc42413174a9c2acfe99a6bf`
- `candidates/BanglaBBQ_Ethnicity_FINAL_english.jsonl`:  
  `29a0849436ce630a035a60bb75d2bccba3acfcbf2bce747bd8cfcdb57a3ef86a`
- `candidates/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl`:  
  `1635587e621c5af4e008c40b0753a7e9f2d922d72703d6b4242b37676319d089`

### Change Diff Manifest & Ledger Verification
- `diffs/health_status_before_after.diff`: 4,320 lines (720 records modified per language, exactly 15 variations).
- `diffs/regional_affiliation_before_after.diff`: 4,320 lines (720 records modified per language, exactly 15 variations).
- `diffs/ethnicity_before_after.diff`: 4,320 lines (720 records modified per language, exactly 15 variations).
- `diffs/candidate_change_ledger.csv`: Exactly 4,320 record audit rows generated using the formula `v = (eid // 480) + 1` and `q = ((eid % 480) // 48) + 1`. Verified **0 Theme/Variation indexing errors**.

### Independent Validation Summary (Script: `scripts/validate_final_qa_candidates.py`)
- Health Status Candidate: **PASS** (13/13 Checks Passed)
- Regional Affiliation Candidate: **PASS** (13/13 Checks Passed)
- Ethnicity Candidate: **PASS** (13/13 Checks Passed)
- Benchmark Categories (PA, SS, OB, MS): **PASS** (12/12 Checks Passed each)
- **Total Invariant Violations**: **0**

---

## 5. Category Quality Classifications & Audit Summary

| Category | Positional Bias Status | Structural Status | Evidence Tier Summary | Linguistic / Semantic Quality | Final Category Classification |
|---|---|---|---|---|---|
| **Physical Appearance** | EXACT 50/50 (180/180) | Validated (1,440 rows) | 5/10 Direct, 3 Context, 2 Confounded | Casting confounders in commercial/acting themes | **SEMANTICALLY REVIEWED** |
| **Social Status** | EXACT 50/50 (180/180) | Validated (1,440 rows) | 6/10 Direct, 4 Context | Bureaucratic English calques; generic family labels | **SEMANTICALLY REVIEWED** |
| **Health Status** | EXACT 50/50 (180/180) | Validated (1,440 rows) | 7/10 Direct, 3 Confounded | Infection control confounder; 0% mental health | **SEMANTICALLY REVIEWED** |
| **Regional Affiliation**| EXACT 50/50 (180/180) | Validated (1,440 rows) | 4/10 Direct, 4 Context, 2 Flawed/Satire | Q01/Q05 satire citations; repetitive district phrasing | **NEEDS HUMAN REVIEW** |
| **Ethnicity** | EXACT 50/50 (180/180) | Validated (1,440 rows) | 4/10 Direct, 6 General Context | Artificial participant placeholders ('শিক্ষার্থী ক/খ') | **NEEDS HUMAN REVIEW** |
| **Occupational Background**| EXACT 50/50 (180/180)| Validated (1,440 rows) | 5/10 Direct, 3 Confounded, 2 Weak | Tea worker caste/ethnicity confounder (Q07); lift access (Q03) | **NEEDS HUMAN REVIEW** |
| **Marital Status** | EXACT 50/50 (180/180) | Validated (1,440 rows) | 6/10 Direct, 4 Context | 30% tiger widow concentration; female-only pairs | **NEEDS HUMAN REVIEW** |

---

## 6. Review Queue & Strategic Planning Artifacts
1. `source_audit.csv`: Complete forensic audit of all 70 themes across all 7 categories detailing source URLs, empirical findings, and confounding limitations.
2. `linguistic_review_queue.csv`: 31 prioritized Bengali candidate cases flagged for expert human linguistic adjudication.
3. `mental_health_coverage_plan.md`: Architectural roadmap proposing a dedicated 8th category (`BanglaBBQ_MentalHealth`, 1,440 rows) aligned with DSM-5 and NIMH Bangladesh data.
4. `human_validation_protocol.md`: Independent protocol establishing triple-annotator recruitment, 1–5 naturalness rubrics, unambiguous entailment checks, and IAA agreement thresholds (κ >= 0.75).

---

## 7. Recommended Next Actions
1. **Preserve Production Freeze**: Keep all candidate datasets sequestered in `local_candidates/final_seven_category_qa/` pending formal human review.
2. **Execute Linguistic Adjudication**: Contract native Bangladeshi annotators to review the 31 priority records in `linguistic_review_queue.csv`.
3. **Source Replacement for Regional**: Replace satire citations in Regional Affiliation (Q01 Noakhali passport memes, Q05 Barisal temper tropes) with verified anthropological field studies.
4. **Author Approved Deployment**: Once human validation confirms zero linguistic degradation, promote the 6 candidate files to `Dataset_BanglaBBQ_New/` and sync with Google Sheets.
