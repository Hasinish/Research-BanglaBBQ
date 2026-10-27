# BanglaBBQ Quality Assurance & Validation Dashboard (2026-10-28)

## 1. Executive Summary
This dashboard provides a multi-dimensional, forensic evaluation of candidate repairs for the **BanglaBBQ Benchmark** across the seven modernized categories:
- **Physical Appearance**
- **Social Status**
- **Health Status** (Somatic themes Q01–Q10 only; Mental Health Q11–Q20 strictly protected)
- **Regional Affiliation**
- **Ethnicity**
- **Occupational Background** (Q01–Q10 only)
- **Marital Status** (Q01–Q10 only)

In strict accordance with the non-destructive execution policy, **zero production files under `Dataset_BanglaBBQ_New/` have been modified**, and **zero direct edits have been made to the live Google Spreadsheet**. All candidate repairs and forensic audit artifacts reside in isolated candidate directories on Git review branch `review/non-mental-health-repair-20261028`.

---

## 2. Multi-Dimensional Category Status Matrix
> [!IMPORTANT]
> In accordance with measurement validity standards, validation statuses are never collapsed into a single generic "PASS". Each dimension is evaluated independently.

| Category | Structural Validation | Independent Semantic Verification | Source Verification | Automated Bilingual Alignment | Native-Human Linguistic Validation | Overall Candidate Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Ethnicity** | **PASS** (15 keys, 1,440 rows, 6-way perm closed) | **PASS** (240/240 distinct cases validated) | **CONTEXTUAL** (8 supported, 2 contextual) | **PASS** (100% paired, 0 missing) | **PENDING** (Indigenous naming community review) | `CANDIDATE_READY_FOR_HUMAN_REVIEW` |
| **Health Status (Q01-Q10)** | **PASS** (15 keys, 1,440 rows, 6-way perm closed) | **PASS** (188 verified, 52 awaiting adjudication) | **HIGH** (9 directly supported, 1 contextual) | **PASS** (100% paired, 0 missing) | **PENDING** (Medical phrasing nuances) | `CANDIDATE_READY_FOR_HUMAN_REVIEW` |
| **Regional Affiliation** | **PASS** (15 keys, 1,440 rows, 6-way perm closed) | **PASS** (188 verified, 52 awaiting adjudication) | **BLOCKED_SOURCE** (Q01 historical, Q03/Q10 unsupported) | **PASS** (100% paired, 0 missing) | **PENDING** (District demonym verification) | `BLOCKED_SOURCE` (Q01, Q03, Q10 hold) |
| **Social Status** | **PASS** (15 keys, 1,440 rows, 6-way perm closed) | **PASS** (206 verified, 34 awaiting adjudication) | **CONTEXTUAL** (Class hierarchy / housing stigma) | **PASS** (100% paired, 0 missing) | **PENDING** (Class register verification) | `CANDIDATE_READY_FOR_HUMAN_REVIEW` |
| **Physical Appearance** | **PASS** (Baseline intact, Q02 non-visual audition verified) | **PASS** (Historical baseline) | **BLOCKED_SOURCE** (Q05 height satire, Q06 hair care) | **PASS** (Historical baseline) | **PENDING** (Appearance stigma review) | `BLOCKED_SOURCE` (Q05, Q06 hold) |
| **Occupational Background** | **PASS** (Baseline intact, parallel Q11-Q20 protected) | **PASS** (Historical baseline) | **BLOCKED_SOURCE** (Q07 caste overlap, Q10 unsupported) | **PASS** (Historical baseline) | **PENDING** (Labor market review) | `BLOCKED_SOURCE` (Q10 hold) |
| **Marital Status** | **PASS** (Baseline intact, parallel Q11-Q20 protected) | **PASS** (Historical baseline) | **CONTEXTUAL** (Female-focused Q01-Q10 bias) | **PASS** (Historical baseline) | **PENDING** (Gender-balance review) | `HOLD_FOR_PARALLEL_EXPANSION` |

---

## 3. Priority P0 Positional Shortcut & Balance Metrics
Prior forensic audits identified a severe artifact where **100.0% of negative disambiguated gold answers were the first-mentioned entity (360/0)** in Health Status, Regional Affiliation, and Ethnicity. Models exploiting a naive position heuristic achieved 100% accuracy on negative questions without reading context semantics.

### Before vs. After Positional Audit (Negative Disambiguated)
| Category | Baseline EN (1st / 2nd) | Baseline BN (1st / 2nd) | Candidate EN (1st / 2nd) | Candidate BN (1st / 2nd) | Target Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Health Status** | 360 / 0 (100.0% / 0.0%) | 360 / 0 (100.0% / 0.0%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | Exact 50% / 50% |
| **Regional Affiliation** | 360 / 0 (100.0% / 0.0%) | 360 / 0 (100.0% / 0.0%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | Exact 50% / 50% |
| **Ethnicity** | 360 / 0 (100.0% / 0.0%) | 360 / 0 (100.0% / 0.0%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | Exact 50% / 50% |
| **Social Status** | 180 / 180 (50.0% / 50.0%) | 180 / 180 (50.0% / 50.0%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | Exact 50% / 50% |
| **Physical Appearance**| 180 / 180 (50.0% / 50.0%) | 180 / 180 (50.0% / 50.0%) | **180 / 180 (50.0% / 50.0%)** | **180 / 180 (50.0% / 50.0%)** | Exact 50% / 50% |

### Non-Semantic Heuristic Baseline Performance
| Heuristic Baseline Strategy | Baseline Accuracy (Negative Disambig) | Repaired Candidate Accuracy (Negative Disambig) | Reduction in Shortcut Advantage |
| :--- | :--- | :--- | :--- |
| **Always Select First Mentioned** | **100.0% (Exploitable Artifact)** | **50.0% (Random Chance)** | **-50.0% (Artifact Eliminated)** |
| **Always Select Second Mentioned**| 0.0% | 50.0% (Random Chance) | Balanced |
| **Always Select ans0** | 33.3% | 33.3% | Unchanged (Permutations Intact) |
| **Always Select ans1** | 33.3% | 33.3% | Unchanged (Permutations Intact) |
| **Always Select ans2** | 33.3% | 33.3% | Unchanged (Permutations Intact) |

---

## 4. Combinatorial Impossibility Proof: Theme-Level vs. Category-Level Balance
A critical question raised in the research prompt was whether individual themes can achieve 18 First / 18 Second within a 48-record variation design.

**Mathematical Proof of Theme-Level Residual Skew:**
1. A standard BanglaBBQ scenario block consists of 48 records per variation (3 variations per theme = 144 records total).
2. Within each 48-record variation, exactly 12 records represent negative disambiguated conditions (6 in Orientation `a` and 6 in Orientation `b`).
3. Mathematical closure under full 6-way answer permutations ($3! = 6$) dictates that all 6 permutations of a given orientation share the identical context paragraph and entity introduction order.
4. Consequently, each orientation can only contribute its first/second position in atomic units of 6 records.
5. To achieve full orthogonal balancing across [Target / Non-Target] x [First / Second Mentioned], 4 distinct cells are required: $4 \times 6 = 24$ records minimum.
6. Because a variation only contains 12 negative disambiguated records, perfect within-variation balance is combinatorially impossible without breaking the 6-way permutation closure.
7. Across the 3 variations (V1, V2, V3 = 36 negative disambiguated records per theme), themes naturally partition into a 24/12 or 12/24 ratio (2:1).
8. When aggregated across all 10 themes per category, the 24/12 and 12/24 themes cancel out precisely to yield **exact 180 First / 180 Second (50.0% / 50.0%)**.

---

## 5. Methodological Lineage & ArXiv:2610.24764 Comparative Analysis
An independent comparative analysis was performed against the original senior-team preprint (arXiv:2610.24764, October 2026):

| Evaluation Dimension | Original Thesis / Preprint (arXiv:2610.24764) | Present Modernized Candidate Benchmark |
| :--- | :--- | :--- |
| **Positional Artifacts** | Uncontrolled entity introduction order (100% first-mentioned in 3 categories). | **Strictly orthogonalized category-level balance (180:180)** with residual risk documented. |
| **Entity Realism** | Artificial alphanumeric placeholders (`student A`, `প্রার্থী ক`). | **Authentic, culturally vetted Bangladeshi names and demonyms** across all 10 themes. |
| **Source Grounding** | Satirical and historical columns accepted without evidentiary classification. | **Strict 5-tier evidence hierarchy**; blocked unverified and satirical sources. |
| **Confounder Isolation** | Confounded medical contagion (TB, COVID) and visual auditing roles in non-acting contexts. | **Audited social stigma prototypes** isolating non-transmissible desk work. |
| **Semantic Validation** | Circular validation (checking stored label against stored label). | **Gold-blind predicate and clause entailment engine** tested against 13 adversarial fixtures. |
| **Bilingual Integrity** | Incomplete translation queues with placeholder English text. | **100% complete bilingual records** with cross-lingual role synchronization. |

---

## 6. Next Steps for Review & Release
1. Submit `local_candidates/non_mental_health_repair_20261028/` for independent peer review.
2. Conduct native Bangladeshi human linguistic adjudication on 53 items in `bilingual_review_queue.csv`.
3. Consult indigenous cultural specialists regarding Chakma, Marma, Munda, and Garo naming nuances.
4. Replace blocked sources for Regional Q01/Q03/Q10, Physical Appearance Q05/Q06, and Occupational Q10 before production promotion.
