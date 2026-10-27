# Research Log: Non-Mental-Health Comprehensive Dataset Repair, Semantic Validation, Source Verification & Bilingual QA

**Date**: 2026-10-28  
**Researcher / Collective**: Antigravity Autonomous Research Specialist Collective (Senior NLP Benchmark Specialist, Bangladeshi Sociocultural Specialist, English-Bengali Linguistic QA Engineer, Scientific Citation Auditor, Adversarial QA Reviewer)  
**Category**: Seven Modernized Categories (Physical Appearance, Social Status, Health Status Q01-Q10, Regional Affiliation, Ethnicity, Occupational Background Q01-Q10, Marital Status Q01-Q10)  
**Git Branch**: `review/non-mental-health-repair-20261028` (based on verified `origin/main` commit `6967700`)  
**Status**: `CANDIDATE REPAIRS GENERATED / INVARIANTS 100% PASS / ADVERSARIAL TESTS 13/13 REJECTED / ZERO PRODUCTION MUTATIONS`  

---

## 1. Executive Summary & Research Scope
In response to the Master Research Execution Prompt, this milestone executed a comprehensive, non-destructive repair and validation package for the non-Mental-Health portions of the **BanglaBBQ Benchmark**.

### Strict Scope & Protected Boundaries
- **Included Categories**: The seven modernized categories (Physical Appearance, Social Status, Health Status Q01–Q10, Regional Affiliation, Ethnicity, Occupational Background Q01–Q10, Marital Status Q01–Q10).
- **Strict Exclusions (Protected Parallel Agent Work)**:
  - **Mental Health Expansion**: Health Status Q11–Q20 (IDs 1440–2879) remained completely untouched.
  - **Marital Status Male Expansion**: Male-focused Q11–Q20 handled in parallel chat; existing Q01–Q10 audited without ID collisions.
  - **Occupational Background Expansion**: Professional Q11–Q20 handled in parallel chat; existing Q01–Q10 audited without ID collisions.
  - **Five Working Categories**: Age, Gender Identity, Educational Background, Religion, Politics evaluated under read-only regression checks only.
- **Non-Destructive Enforcement**: Zero writes to `Dataset_BanglaBBQ_New/`, zero mutations to historical thesis dataset `Dataset_ BanglaBBQ_Old/`, zero edits to the live master Google Spreadsheet (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`).

---

## 2. Baseline Manifest & Cryptographic Hashes
A complete cryptographic inventory of the 14 production files (10,080 rows per language = 20,160 total records) was generated and locked at `local_candidates/non_mental_health_repair_20261028/baseline_manifest.json`:
- All 14 files conform to the exact 15-key schema: `example_id`, `question_index`, `context_condition`, `question_polarity`, `type`, `context`, `question`, `ans0`, `ans1`, `ans2`, `label`, `answer_info`, `additional_metadata`, `category`, `id`.
- Pre-repair SHA-256 hashes verified bit-for-bit against commit `6967700`.

---

## 3. Priority P0: Positional Shortcut Elimination
Prior audits revealed that **100.0% of negative disambiguated gold answers were the first-mentioned entity (360/0)** in Health Status, Regional Affiliation, and Ethnicity. Models selecting the first-mentioned entity achieved 100% accuracy on negative questions without reasoning about context.

### Repaired Positional Performance
- **Repaired Candidate Datasets**:
  - `BanglaBBQ_Ethnicity_repaired_english.jsonl` & `_bengali.jsonl`
  - `BanglaBBQ_Health_Status_repaired_english.jsonl` & `_bengali.jsonl`
  - `BanglaBBQ_Regional_repaired_english.jsonl` & `_bengali.jsonl`
  - `BanglaBBQ_SocialStatus_repaired_english.jsonl` & `_bengali.jsonl`
- **Result**: Achieved **exact 180 First / 180 Second (50.0% / 50.0%)** across all repaired categories in both English and Bengali.
- **Shortcut Reduction**: "Always Select First Mentioned" heuristic dropped from **100.0% to 50.0% (random baseline)** on negative disambiguated conditions.

### Combinatorial Proof of Theme-Level Residual Skew
- Full 6-way answer permutation closure ($3! = 6$) requires that all 6 records of a scenario orientation share identical context and introduction order.
- To balance [Target/Non-Target] x [First/Second], 4 cells x 6 records = 24 records minimum are required.
- Because a 48-record variation has only 12 disambiguated rows, within-variation orthogonal balancing is mathematically impossible without breaking permutation closure.
- Variations partition into a 24/12 or 12/24 ratio (2:1). Aggregated across 10 themes, these cancel out to achieve exact 180:180 balance.

---

## 4. Priority P0: Ethnicity Placeholder Eradication
- **Defect**: Baseline Ethnicity contained artificial tokens (`Munda student A`, `Chakma candidate A`, `ethnic Bengali student B`, `শিক্ষার্থী ক`, `শিক্ষার্থী খ`).
- **Correction**: Replaced placeholders across all 10 themes with authentic, culturally vetted Bangladeshi Indigenous and Bengali names (e.g., Bikash Munda, Tanvir Ahmed, Ripon Chakma, Nafis Iqbal).
- **Verification**: Evaluated with strict boundary regex. Both English and Bengali candidate files contain **0 bad rows (100% natural names)**.
- **Bilingual Role Sync**: Synchronized `answer_info` dictionaries so both English and Bengali records carry matching role tags (`munda`, `ethnic_bengali`, etc.).

---

## 5. Priority P1: Confounder Isolation & Prototypes
- **Health Status (Q02, Q04, Q05, Q07)**: Integrated 576 rows of audited prototypes removing medical contagion confounders (TB, COVID-19, Hepatitis B) and focusing purely on non-transmissible desk work stigma.
- **Social Status (Q07 V3)**: Integrated 48 rows of procedural compliance prototypes ensuring identical paperwork/documentation standards across socioeconomic backgrounds.
- **Physical Appearance (Q02 Special Case)**: Production records were reinspected and found to *already* use non-visual roles ("behind-the-camera script-editing", "voice-only recordings", "subtitle-editing"). The proposed bank-auditing prototype was **rejected** to prevent degrading culturally authentic media-production scenarios.

---

## 6. Priority P0/P1: Source Evidence Verification
All 70 themes across the seven categories were audited and categorized into strict, mutually exclusive tiers in `source_evidence_matrix.csv`:
- **32 DIRECTLY_SUPPORTED**: Empirical studies demonstrating bias mechanism.
- **31 CONTEXTUALLY_SUPPORTED**: Valid contextual documentation of cultural stereotypes.
- **2 HISTORICAL_ONLY**: Pre-independence era studies (e.g., Schuman 1966).
- **5 UNSUPPORTED / BLOCKED**:
  - Regional Q03 (Tangail satire column)
  - Regional Q10 (Old Dhaka culinary/heritage article)
  - Physical Appearance Q05 (Humorous height column)
  - Physical Appearance Q06 (Curly hair styling guide)
  - Occupational Background Q10 (Livelihood paper for meeting competence)
- All 5 unsupported themes are marked `BLOCKED_SOURCE` and prohibited from production release.

---

## 7. Priority P1: Independent Semantic Validation & Adversarial Suite
- **Engine Design**: Built non-circular, gold-blind predicate entailment and clause-matching validator (`independent_semantic_validator.py`). Labels and answer options are hidden during semantic evaluation.
- **Adversarial Test Suite**: Evaluated against 13 deliberate failure fixtures (`test_adversarial_validator.py`):
  - Result: **13/13 (100.0%) adversarial fixtures successfully caught and rejected**.
- **Candidate Evaluation**:
  - Evaluated 960 distinct semantic cases across repaired candidates:
  - **822/960 (85.6%) INDEPENDENTLY_VALIDATED**.
  - Remaining 138 cases flagged for human adjudication (`AWAITING_HUMAN_ADJUDICATION`) in `semantic_validation_report.csv`.
  - Ethnicity achieved **240/240 (100.0%) independent validation**.

---

## 8. Priority P1: Complete Bilingual Review Queue
- Generated `bilingual_review_queue.csv` containing 53 detailed items with full English context, Bengali context, questions, options, stored label, expected semantic answer, defect descriptions, and native-speaker review statuses.
- Zero placeholder strings (`See parallel candidate record`) and zero ambiguous variation markers (`V`).

---

## 9. Methodological Comparison with ArXiv:2610.24764
An independent comparative review against the original-team preprint (arXiv:2610.24764) confirmed:
1. The preprint retains severe positional skew (100% first-mentioned in negative disambiguated conditions for 3 categories). Our candidate repair eliminates this artifact (180:180).
2. The preprint employs artificial alphanumeric labels (`student A`). Our candidate introduces culturally authentic names.
3. The preprint relies on satirical and informal columns. Our audit enforces strict 5-tier evidence classification and blocks unverified sources.
4. Confounders (medical contagion, procedural asymmetry) present in earlier versions are systematically isolated in candidate prototypes.

---

## 10. Deliverables Manifest
All artifacts generated under `local_candidates/non_mental_health_repair_20261028/`:
1. `baseline_manifest.json`: Baseline inventory with cryptographic SHA-256 hashes.
2. `reports/issue_register.csv`: 15 prioritized defect entries.
3. `candidates/`: 8 repaired JSONLs (Ethnicity, Health Status, Regional, Social Status).
4. `reports/change_ledger.csv`: 16,200 field-level modifications documented.
5. `reports/source_evidence_matrix.csv`: 70-theme source audit.
6. `reports/semantic_validation_report.csv`: 960-case gold-blind evaluation report.
7. `reports/position_and_counterfactual_audit.csv`: Balance and baseline statistics.
8. `reports/bilingual_review_queue.csv`: 53 full-text bilingual review items.
9. `scripts/`: Automated invariant and adversarial test scripts.
10. `reports/qa_dashboard.md`: Multi-dimensional status dashboard.
11. `reports/unresolved_blockers.md`: Blocked sources and scientific limitations.
12. `reports/integration_plan.md`: Step-by-step production promotion procedure.
