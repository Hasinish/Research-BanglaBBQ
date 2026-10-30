# state.md — Current Verified Progress Dashboard

**Last Verified Date**: 2026-10-29  
**Latest Engineering Milestone (All 8 Full Evaluation Scripts Upgraded & Offline Certified)**: 2026-10-30: Upgraded all eight 61,312-query benchmark evaluator scripts (scripts/modal_eval_*_full_60k_l40s.py) to use scripts/modal_eval_core.py and scripts/bbq_scoring_engine.py. Eliminated flawed compute_metrics() fallthrough role bug and added correct Parrish et al. (2022) BBQ metrics (s_amb, s_dis). Integrated native instruction/chat formatting across all eight model architectures (Gemma 2, LLaMA 3.1, Ministral 8B, Mistral-Nemo, Qwen 2.5 3B/7B, BanglaLLM, Titulm Alpaca). Implemented durable incremental checkpointing on anglabbq-eval-volume (24 chunk files/model with automatic resume) and independent raw response re-parsing verification. Hardened checkpoint commit fail-hard (RuntimeError on volume commit failure) and strict pre-resume verification of model identity, example_id sequences, and counts. All 4 offline test suites (38 tests total) certified PASS with zero defects. Ready for manual execution.

**Latest Verification Milestone (Certified 200-Query Modal Pilot Completed on Qwen 2.5 7B)**: 2026-10-30: Successfully executed certified 200-query pilot benchmark on Qwen/Qwen2.5-7B-Instruct on NVIDIA L40S GPU via Modal (scripts/modal_eval_pilot_qwen_7b.py). Saved all 200 raw outputs and parsed predictions to metadata/eval_predictions/pilot_qwen2_5_7b_predictions.jsonl with 0 historical report overwrites. Verified 100% bit-for-bit offline rescoring invariants using scripts/bbq_scoring_engine.py (s_amb, s_dis, acc bit-for-bit identical). Empirical findings: ENG Acc 98.0% (Ambig Acc 96.0%, s_amb +0.0400, s_dis +0.0400, unparseable 0.0%); BEN Acc 52.0% (Disambig Acc 98.0%, Ambig Acc 6.0%, s_amb +0.1000, s_dis 0.0000, unparseable 0.0%). Demonstrated severe Bengali ambiguous collapse (-90.0% acc drop) with zero parsing failures. Total wall time: 99.83s (inference 3.67s, 54.5 q/s), GPU cost: USD 0.0499 (~USD 0.05).

**Latest Forensic Milestone (Evaluation Scoring Audit & Certified BBQ Engine Built)**: 2026-10-30: Completed critical forensic audit of 61,312-query evaluation pipeline across all eight models. Proved that previous evaluators suffered from a fallthrough role bug in compute_metrics() (classifying almost all negative non-Unknown picks as biased because ans_role != 'non_target' was unconditionally true) and omitted s_dis. Confirmed zero sample-level predictions were saved to persistent storage, making offline rescoring physically impossible. Solved root cause by: (1) authoring metadata/sidecar_stereotype_target_map.json across all 214 themes (61,232/61,312 records cleanly mapped, 80 legacy Gender entries flagged non-directional); (2) engineering scripts/bbq_scoring_engine.py strictly implementing Parrish et al. (2022) BBQ formulas (s_amb, s_dis, acc_ambig, acc_disambig, unparseable_rate); (3) authoring tests/test_bbq_scoring_engine.py (14/14 unit tests PASS) and tests/test_target_mapping_invariants.py (61,312/61,312 records PASS). Workload to rerun certified suite on NVIDIA L40S estimated at USD 0.0499 (~USD 0.05) for pilot, ~USD 0.84 to ~USD 1.02 for top 4 publication models, or ~USD 1.68 to ~USD 2.04 for all 8 models.

**Latest Grand Empirical Milestone (Eight-Model Canonical 61,312-Query Benchmark Suite Certified)**: 2026-10-29: Fully completed and certified full-population 61,312-query benchmark evaluations across all 12 categories for EIGHT major models on NVIDIA L40S GPU:
1. google/gemma-2-9b-it: 90.03% ENG / 86.92% BEN | Delta +0.0569 (Benchmark Champion 👑)
2. mistralai/Mistral-Nemo-Instruct-2407: 87.56% ENG / 82.44% BEN | Delta -0.0222 (Perfect Cross-Lingual Alignment 🛡️)
3. Qwen/Qwen2.5-7B-Instruct: 92.05% ENG / 72.30% BEN | Delta +0.3174 (SOTA English, but high Bengali bias delta)
4. mistralai/Ministral-8B-Instruct-2410: 83.18% ENG / 65.55% BEN | Delta +0.2397 (Catastrophic Appearance/Health collapse)
5. meta-llama/Llama-3.1-8B-Instruct: 71.68% ENG / 60.03% BEN | Delta +0.1694 (Systemic cross-lingual safety collapse)
6. Qwen/Qwen2.5-3B-Instruct: 83.25% ENG / 57.89% BEN | Delta +0.3414 (Severe 3B capacity breakdown)
7. BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct 🥇: 80.79% ENG / 59.15% BEN | Delta +0.2196 (Bengali fine-tune improves base 3B by +1.26% acc and dampens delta from +0.3414 to +0.2196, but still collapses in Politics/Religion)
8. hishab/titulm-llama-3.2-3b-v2.0-Instruct-v1.0 🥈: 33.03% ENG / 26.29% BEN | Delta +0.2775 (Complete sub-random degeneration, +0.9367 Bengali ambiguous bias saturation)

**Prior Empirical Benchmark Milestone (Ministral 8B Population Benchmark Completed)**: 2026-10-29: Executed complete 61,312-query canonical population benchmark on mistralai/Ministral-8B-Instruct-2410 via vLLM on NVIDIA L40S in 439.54s (139.5 q/s). Uncovered the most severe cross-lingual safety alignment collapse observed across all models (+0.2397 global bias delta, eclipsing LLaMA's +0.1694 and Gemma's +0.0569). While disambiguated accuracy remained high (86-98%), ambiguous Bengali accuracy collapsed to near zero in Physical Appearance (8.61% acc, +0.9139 bias) and Health Status (12.99% acc, +0.8701 bias), proving catastrophic dissolution of RLHF humility guardrails under Latin-centric tokenization. Documented in research_logs/2026-10-29_canonical_61312_ministral_8b_evaluation.md and generated metadata/eval_results/full_benchmark_report_ministral_8b.json.
**Prior Architecture & Evaluation Milestone (Ministral 3B vs 8B Parameter Scaling Setup)**: 2026-10-29: Verified persistent Modal volumes (ministral-3b-volume and ministral-8b-volume) containing full safetensors for mistralai/Ministral-3-3B-Instruct-2512 and mistralai/Ministral-8B-Instruct-2410. Authored and compiled dedicated L40S bilingual smoke test suites (scripts/modal_test_ministral_3b_l40s.py, scripts/modal_test_ministral_8b_l40s.py) and full-scale 61,312-query population benchmark runners (scripts/modal_eval_ministral_3b_full_60k_l40s.py, scripts/modal_eval_ministral_8b_full_60k_l40s.py) computing Parrish et al. (2022) BBQ bias metrics, accuracy, and cross-lingual deltas across all 12 categories.
**Prior Empirical Evaluation Milestone (Dual 61,312-Query Population Parameter Evaluation)**: 2026-10-29: Completed canonical 61,312-query evaluations across all 12 categories for BOTH google/gemma-2-9b-it (10.3 mins, 99.2 q/s) and meta-llama/Llama-3.1-8B-Instruct (13.0 mins, 78.7 q/s) on NVIDIA L40S GPU. Certified empirical population parameters: Google maintains high bilingual robustness (90.03% ENG / 86.92% BEN) with localized bias surges in Health (+0.2722 delta), Appearance (+0.2083 delta), Social (+0.0652 delta), and Politics (+0.0527 delta). Meta suffers systemic cross-lingual safety alignment collapse across 10 of 12 categories (71.68% ENG / 60.03% BEN, global bias delta +0.1694), with ambiguous accuracy collapsing to 22.84% in Bengali (vs 80.45% in Gemma), conclusively proving RLHF humility guardrail breakdown in low-resource settings. Regional Affiliation leakage hypothesis decisively refuted. Documented in research_logs/2026-10-29_canonical_61312_gemma2_and_llama31_evaluations.md and research_logs/2026-10-29_canonical_61312_llama31_8b_evaluation.md.
**Latest Milestone (Final Three-Category Production Expansion)**: 2026-10-28: Integrated independently audited Q11–Q20 bilingual expansions into canonical production datasets and master Google Sheets for Health Status, Marital Status, and Occupational Background. Expanded each category from 1,440 to 2,880 records per language (17,280 new bilingual records; 5,760 records/category). Verified 100% bit-for-bit immutability of original 1,440-row prefixes (0 byte drift). Resolved Occupational manifest blockers (Q12/Q14/Q15 qualified, Q16 calibrated). Certified 100% invariants across all 14 canonical benchmark files (14,400 tracked global IDs). Expanded live Google Sheets to 2,881 rows, formatted row height to 96px, and verified 100.0000% bit-for-bit live cell readback parity across all 432,000 data cells with 0 mismatches. Preserved all 10 pre-existing active category tabs and historical baseline byte-for-byte.
**Previous Milestone (Zero-Assumption Audit)**: 2026-10-28: Completed exhaustive independent source & semantic forensic audit across all 7 modernized categories. Verified bit-for-bit SHA-256 integrity (19/19 files identical), verified 180:180 negative/non-negative disambiguated gold position parity across Health Status, Regional Affiliation, and Ethnicity candidates (with explicit `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW (2:1)` labeling), verified 12/12 candidate and prototype JSONLs on all structural invariants, verified Regional Q05 direct source text (*Daily Star* Saad Quasem, June 14, 2025), qualified Regional Q01 Schuman (1966) as historical-only context, and validated 128 prototype semantic cases with 0 positional regressions. All candidate and prototype datasets remain safely isolated in `local_candidates/final_seven_category_qa/` awaiting final human sign-off; canonical production datasets remain 100% untouched.
**Latest Production Repair Deployed (Physical Appearance Introduction-Order)**: 2026-10-27: Fully repaired and deployed `BanglaBBQ_PhysicalAppearance` (both English and Bengali; 1,440 rows each) under `Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/`. Reversed initial character introduction order across 15 of 30 variations (5 in V1, 5 in V2, 5 in V3), eliminating the 100% first-person negative answer shortcut and establishing exact **180 First / 180 Second (50.0% / 50.0%)** parity in negative disambiguated gold positions. Preserved 100% byte-level invariance for IDs, labels, schema, answer permutations, and 18/18 demographic counterfactual balance across all 10 themes. 100% PASS on official CI validator (`scripts/validate_seven_final_categories.py`).
**Latest Google Spreadsheet Import (7 Final Categories)**: 2026-10-26: Successfully imported all 14 bilingual worksheets (7 English, 7 Bengali; 20,160 rows; 302,400 data cells) into the master Google Spreadsheet (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`) using canonical `Education` formatting templates via `duplicateSheet`. Verified 100.0000% bit-for-bit live parity across all 302,400 data cells with 0 mismatches. Preserved all 10 pre-existing active category sheets and 27 backup/review sheets with identical Sheet IDs.
**Latest Dataset Consolidation**: 2026-10-26: Consolidated all 12 canonical category directories into a unified master benchmark directory [`Dataset_BanglaBBQ_New/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New). Preserved seniors' historical baseline `Dataset_ BanglaBBQ_Old/` byte-for-byte. Updated GitHub Actions workflows, validation scripts, and test suites with 100% invariant pass rate and 23/23 adversarial fixtures rejected.
**Latest Workspace Reorganization**: 2026-10-26: Cleared root directory clutter by moving 14 candidate and forensic QA bundles into dedicated [`audits/`](file:///d:/Research-BanglaBBQ/audits) and [`candidate_bundles/`](file:///d:/Research-BanglaBBQ/candidate_bundles) directories, and moving loose thesis papers and legacy reports into [`docs/papers/`](file:///d:/Research-BanglaBBQ/docs/papers) and [`docs/reports/`](file:///d:/Research-BanglaBBQ/docs/reports). Verified 100% invariant tests and 23/23 adversarial fixtures pass locally without regression.
**Latest Verified Production Main Commit**: c0e5582 (Merge pull request #1 from Hasinish/integrate/final-three-category-expansion); PR #1 merged, CI green (run 40697842949), local and remote main synchronized, working tree clean.
**Current Milestone**: Zero-Assumption Independent Source & Semantic Forensic Audit completed and cryptographically locked across all 7 categories; Master Google Spreadsheet 100% synchronized across all 12 categories (24 active worksheets); 100% bit-for-bit live parity verified across all 302,400 newly imported data cells and all pre-existing datasets; CI validation passing for canonical benchmarks; Physical Appearance introduction-order shortcut repaired in canonical production with 180:180 balance.

---

## 1. Benchmark Status Dashboard across All 12 Canonical Working Categories

| Bias Category | English Count | Bengali Count | Status Marker | Current Working Status & Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Politics** | 2,880 | 2,880 | `IN PROGRESS / LIVE-SYNCHRONIZED` | **20 themes, 144 records/theme/language** = original 48 + wording v2 (48) + wording v3 (48). Full 6-way answer permutations, balanced labels 960/960/960, counterfactual reversals. Approved targeted QA content repairs applied: Q5, Q14, Q19. Verified 100% bit-for-bit parity confirmed (43,200 cells/lang) in `BanglaBBQ_ENG_Politics` (1888499205) and `BanglaBBQ_BEN_Politics` (2128232344). Outstanding: Independent native Bengali translation/entailment review. Not publication-ready. |
| **Religion** | 2,880 | 2,880 | `IN PROGRESS / LIVE-SYNCHRONIZED` | **Evidence-aligned bilingual production repair (2026-10-17):** Six theme repairs (Q3, Q8, Q9, Q10, Q12, Q13) across V1+V2+V3. 2,880 rows/language, 20×144, labels 960/960/960, 6-way permutations, gold-role semantics, IDs 0–2879, 100% live parity confirmed (43,200 cells/lang) in `BanglaBBQ_ENG_Religion` (804112545) and `BanglaBBQ_BEN_Religion` (860941009). Outstanding: Independent native Bengali semantic review. Not publication-ready. |
| **Age** | 2,920 | 2,920 | `IN PROGRESS / LIVE-SYNCHRONIZED` | **2026-10-18 English localization & Q20 legal confound repair verified**: 868 English context repairs + Q20 underage driving repair (112 records/lang: 15/17 -> 19/20). Verified 0/43,800 live cell mismatches in `BanglaBBQ_ENG_Age` (0) and `BanglaBBQ_BEN_Age` (1006819770). 10/10 automated invariant checks PASS. Outstanding: Full independent native-linguistic/semantic QA. Not publication-ready. |
| **Gender Identity** | 4,696 | 4,696 | `REPAIRED / LOCALIZED / 100% PARITY-VERIFIED` | **Final Q56 Probation Repair & 100% Live Parity (2026-10-19)**: Q54 grammar and Q56 probation ordinance repair. All 34 themes verified and live-synchronized in `BanglaBBQ_ENG_Gender` (1990010101) and `BanglaBBQ_BEN_Gender` (1990010102). 100% live parity verified across all 140,910 cells (0 mismatches). Outstanding: Independent colloquial Bengali linguistic review. Not publication-ready. |
| **Educational Background** | 2,880 | 2,880 | `REPAIRED / CHATGPT AUDIT RESOLVED / 100% LIVE PARITY` | **Final Semantic QA Repair & Evidence Rigor Calibration (2026-10-20)**: Resolved all 7 defects from ChatGPT independent audit: Q16 V3 explicit commendation, Q16 V1 tuition-cost confounder, Q15 V3 behavioral confounder, Q20 V1/V2 criteria harmonization, Q16 V2 meaning mismatch, Q05/Q09 evidence calibration. Verified 23/23 adversarial regression fixtures (100% rejection rate). 100% bit-for-bit live parity across all 86,400 data cells in `BanglaBBQ_ENG_Education` (1544720708) and `BanglaBBQ_BEN_Education` (641606675). Outstanding: Independent external human evaluation. Not publication-ready. |
| **Physical Appearance** | 1,440 | 1,440 | `POSITION-REPAIRED / 100% BALANCED / CI VERIFIED` | **Production Introduction-Order Repair (2026-10-27)**: Reversed initial name introduction order across 15 of 30 variations (5 V1, 5 V2, 5 V3). Disambiguated negative gold positions balanced from 360/0 to exact 180 First / 180 Second (50.0% / 50.0%). 18/18 demographic counterfactual balance preserved across all 10 themes. Full 6-way answer permutations and schema intact. 100% bit-for-bit CI invariant pass. Next step: Sync Google Sheets `BanglaBBQ_ENG_PhysicalAppearance` (984262367) and `BanglaBBQ_BEN_PhysicalAppearance` (934839633). |
| **Social Status** | 1,440 | 1,440 | `STANDARDIZED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark (2026-10-26)**: 1,440 rows across 10 socioeconomic class themes (slum dwellers / informal settlements, urban affluent elites, rural-urban economic divides, generational wealth). Full 6-way answer permutations and 4-condition ordering verified. 100% bit-for-bit live parity verified across all 21,600 cells/lang in `BanglaBBQ_ENG_SocialStatus` (1061280109) and `BanglaBBQ_BEN_SocialStatus` (1761692098). Outstanding: Independent colloquial linguistic review. Not publication-ready. |
| **Health Status** | 2,880 | 2,880 | `EXPANDED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark Q01–Q20 (2026-10-28)**: 2,880 rows across 20 themes (10 somatic/chronic Q01–Q10 + 10 psychiatric/mental health Q11–Q20). Full 6-way answer permutations, balanced labels 960/960/960, and 4-condition ordering verified in CI. 100% bit-for-bit live parity verified across all 43,200 cells/lang in `BanglaBBQ_ENG_HealthStatus` (577820949) and `BanglaBBQ_BEN_HealthStatus` (1261981579). Original 1,440 prefix preserved bit-for-bit. Note: Inherited somatic Q01–Q10 positional-bias defect explicitly preserved and documented; psychiatric Q11–Q20 balanced at 180:180. Clinical and linguistic peer review pending. Not publication-ready. |
| **Regional Affiliation** | 1,440 | 1,440 | `STANDARDIZED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark (2026-10-26)**: Overcame legacy 51-row defect, expanded to 1,440 rows across 10 district themes (Noakhali, Barisal, Sylhet, Chittagong, Rangpur/Monga, Old Dhaka, etc.). Full 6-way answer permutations and 4-condition ordering verified. 100% bit-for-bit live parity verified across all 21,600 cells/lang in `BanglaBBQ_ENG_Regional` (1321419120) and `BanglaBBQ_BEN_Regional` (786932138). Outstanding: Native dialectal linguistic review. Not publication-ready. |
| **Ethnicity** | 1,440 | 1,440 | `STANDARDIZED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark (2026-10-26)**: 1,440 rows across 10 indigenous and ethnic minority themes (Chakma, Marma, Tripura, Garo, Santhal, Bihari/Stranded Pakistanis, Rohingya). Full 6-way answer permutations and 4-condition ordering verified. 100% bit-for-bit live parity verified across all 21,600 cells/lang in `BanglaBBQ_ENG_Ethnicity` (210887456) and `BanglaBBQ_BEN_Ethnicity` (1845601757). Outstanding: Community and linguistic peer review. Not publication-ready. |
| **Occupational Background** | 2,880 | 2,880 | `EXPANDED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark Q01–Q20 (2026-10-28)**: 2,880 rows across 20 occupational themes (10 blue-collar/informal Q01–Q10 + 10 professional/corporate Q11–Q20). Full 6-way answer permutations, balanced labels 960/960/960, and 4-condition ordering verified in CI. 100% bit-for-bit live parity verified across all 43,200 cells/lang in `BanglaBBQ_ENG_OccupationalBackground` (1499154542) and `BanglaBBQ_BEN_OccupationalBackground` (934780717). Original 1,440 prefix preserved bit-for-bit. Sources qualified (Q12 corporate prestige, Q14 BCS vs private, Q15 defense veterans, Q16 research prestige). Labor-advocate/linguistic review pending. Not publication-ready. |
| **Marital Status** | 2,880 | 2,880 | `EXPANDED / 100% LIVE PARITY / CI VERIFIED` | **Canonical Modernized Benchmark Q01–Q20 (2026-10-28)**: 2,880 rows across 20 marital themes (10 female-focused Q01–Q10 + 10 male-focused bachelor/divorce/widow Q11–Q20). Full 6-way answer permutations, balanced labels 960/960/960, and 4-condition ordering verified in CI. 100% bit-for-bit live parity verified across all 43,200 cells/lang in `BanglaBBQ_ENG_MaritalStatus` (2049623557) and `BanglaBBQ_BEN_MaritalStatus` (1929463163). Original 1,440 prefix preserved bit-for-bit. Gender/sociological review pending. Not publication-ready. |

### Category Lineage & Distinction: Original 9 Thesis Categories vs. Current 12 Working Categories

1. **Original Nine Categories (BRACU Thesis T2510616, June 2025)**:
   The seniors pioneered the conceptual framework across 9 categories preserved in `Dataset_ BanglaBBQ_Old/`:
   - `Age` (2,920 PakBBQ English rows, but only 799 rows translated into Bengali)
   - `Educational background` (128 legacy rows)
   - `Gender_identity` (4,696 rows)
   - `Marital Status` (100 legacy rows)
   - `Mental Health` (100 legacy rows in `Dataset_ BanglaBBQ_Old/Mental Health/`)
   - `Physical_appearance` (1,106 ENG / 1,123 BEN rows with 17-row mismatch)
   - `Politics` (960 legacy rows)
   - `Regional` (51 legacy rows)
   - `Religion` (960 legacy rows)

2. **Current Twelve Working Categories (`Dataset_BanglaBBQ_New/`)**:
   During the modernization and expansion phase to establish a publication-grade benchmark conforming to BBQ and PakBBQ standards, the project expanded to 12 canonical working categories (all 12 now live in Google Sheets at 100% verified cell parity):
   - **Expanded Categories (5)**: `BanglaBBQ_Age` (2,920/lang), `BanglaBBQ_EducationalBackground` (2,880/lang), `BanglaBBQ_Gender` (4,696/lang), `BanglaBBQ_Politics` (2,880/lang), `BanglaBBQ_Religion` (2,880/lang).
   - **Modernized & Reconciled Categories (3)**: `BanglaBBQ_MaritalStatus` (expanded from 100 to 1,440 rows), `BanglaBBQ_PhysicalAppearance` (reconciled from 1,106/1,123 to 1,440 rows), `BanglaBBQ_Regional` (expanded from 51 to 1,440 rows).
   - **New Societal Bias Categories (3)**: `BanglaBBQ_Ethnicity` (1,440 rows, indigenous/minority bias), `BanglaBBQ_OccupationalBackground` (1,440 rows, blue-collar/informal labor bias), `BanglaBBQ_SocialStatus` (1,440 rows, socioeconomic class/slum dweller bias).
   - **Health Condition Benchmark (1)**: `BanglaBBQ_HealthStatus` (1,440 rows).

3. **Explicit Investigation: Mental Health vs. Health Status**:
   - **Historical Baseline (`Mental Health`)**: The seniors' thesis created a 100-row dataset located in `Dataset_ BanglaBBQ_Old/Mental Health/` (`Mental_health_status_Eng.jsonl` and `Mental_health_status_Bengali_100entries.jsonl`). It was exclusively focused on psychiatric, neurological, and emotional conditions: generalized anxiety, clinical depression, bipolar disorder, and schizophrenia.
   - **Modernized Working Benchmark (`Health Status`)**: The active category located in `Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/` and live in Google Sheets as `BanglaBBQ_ENG_HealthStatus` / `BanglaBBQ_BEN_HealthStatus` contains 1,440 rows across 10 themes. It evaluates social stigma around physical, chronic, and infectious health conditions: arsenicosis, HIV, leprosy, tuberculosis, hepatitis B, epilepsy, thalassemia, COVID-19 recovery, and breast cancer.
   - **Status & Policy**: The historical 100-row `Mental Health` dataset is preserved byte-for-byte in `Dataset_ BanglaBBQ_Old/Mental Health/` and has NOT been overwritten, deleted, or merged. The modernized 1,440-row `Health Status` benchmark is actively tracked and tested in CI. Per strict governance instructions, **no category renaming, deletion, or merging between Mental Health and Health Status will be performed without explicit human researcher authorization**.

> **Status Marker Definitions**:
> - `VERIFIED COMPLETE`: Structurally and semantically validated, verified against pre-expansion baselines, synchronized between Google Sheets and GitHub, passing automated CI.
> - `IN PROGRESS / LIVE-SYNCHRONIZED`: Dataset expanded, structurally validated, and live-synchronized at 100% cell parity in Google Sheets; pending secondary native linguistic or external peer certification.
> - `STANDARDIZED / 100% LIVE PARITY / CI VERIFIED`: 1,440-row balanced benchmark with 6-way answer permutations and 4-condition ordering verified in CI and verified at 100% live readback parity in Google Sheets.
> - `PENDING`: Baseline files cataloged; awaiting dedicated category audit and modernization.
> - `UNVERIFIED`: Claim or dataset not yet verified against primary evidence.
> - `BLOCKED`: Work halted due to dependencies or missing external artifacts.

---

## 2. Google Drive Benchmark Directory & Continuous Synchronization Policy

**Master Google Drive Folder ID**: 1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe  
**Master Google Drive Link**: [https://drive.google.com/drive/folders/1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe](https://drive.google.com/drive/folders/1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe)  
**Synchronization Script**: scripts/sync_drive_dataset.py

> **Continuous Synchronization Rule & Safety Architecture**:
> Dataset_BanglaBBQ_New on Google Drive must ALWAYS mirror GitHub main bit-for-bit.
> 1. **Dual-Hash Auditing**: SHA-256 (custom properties.sha256) and MD5 (native md5Checksum) compared against local files.
> 2. **Pre-Flight Invariant Validation**: Before remote transmission, local files must pass 15-field schema, sequential ID, valid label (0/1/2), and exact row count checks (2,880 for expanded, 2,920 for Age, 4,696 for Gender, 1,440 for unexpanded). Never overwrites approved remote data with unvalidated files.
> 3. **Anomaly Detection**: Flags missing, outdated, and unexpected files across all 12 category folders.
> 4. **Automated Lifecycle Sync**: Triggered automatically via local git hooks (.githooks/post-merge, .githooks/post-commit) and CI (.github/workflows/sync_drive_on_main.yml) whenever changes reach main.
> 5. **Exhaustive Post-Sync Gate**: All 24 canonical files are read back and audited against expected hashes and line counts, requiring 100% PASS.

---

## 3. Google Spreadsheet Working Tabs

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
| `BanglaBBQ_ENG_Gender` | `1990010101` | 30 | 4,697 (4,696 data) | Complete English Gender Identity benchmark across 34 themes (A1:O4697). Approved Q54 grammar patch applied to F4538:F4569 (32 cells). 100% live parity verified (70,455 cells, 0 mismatches). |
| `BanglaBBQ_BEN_Gender` | `1990010102` | 31 | 4,697 (4,696 data) | Complete Bengali Gender Identity benchmark across 34 themes (A1:O4697). Natural Bangladeshi Bengali translation. 100% cell-by-cell verified (70,455 cells, 0 mismatches). |
| `BanglaBBQ_ENG_Education` | `1544720708` | 34 | 2,881 (2,880 data) | Complete English Educational Background benchmark across 20 themes (V1, V2, V3; 48 rows/variation, 144/theme). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_Education` | `641606675` | 35 | 2,881 (2,880 data) | Complete Bengali Educational Background benchmark across 20 themes (V1, V2, V3; 48 rows/variation, 144/theme). Natural Bangladeshi Bengali syntax. 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_PhysicalAppearance` | `984262367` | 37 | 1,441 (1,440 data) | Complete English Physical Appearance benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_PhysicalAppearance` | `934839633` | 38 | 1,441 (1,440 data) | Complete Bengali Physical Appearance benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_SocialStatus` | `1061280109` | 39 | 1,441 (1,440 data) | Complete English Social Status benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_SocialStatus` | `1761692098` | 40 | 1,441 (1,440 data) | Complete Bengali Social Status benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_HealthStatus` | `577820949` | 41 | 2,881 (2,880 data) | Expanded English Health Status benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_HealthStatus` | `1261981579` | 42 | 2,881 (2,880 data) | Expanded Bengali Health Status benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_Regional` | `1321419120` | 43 | 1,441 (1,440 data) | Complete English Regional Affiliation benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_Regional` | `786932138` | 44 | 1,441 (1,440 data) | Complete Bengali Regional Affiliation benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_Ethnicity` | `210887456` | 45 | 1,441 (1,440 data) | Complete English Ethnicity benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_Ethnicity` | `1845601757` | 46 | 1,441 (1,440 data) | Complete Bengali Ethnicity benchmark. 100% live parity verified (21,600 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_OccupationalBackground` | `1499154542` | 47 | 2,881 (2,880 data) | Expanded English Occupational Background benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_OccupationalBackground` | `934780717` | 48 | 2,881 (2,880 data) | Expanded Bengali Occupational Background benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_ENG_MaritalStatus` | `2049623557` | 49 | 2,881 (2,880 data) | Expanded English Marital Status benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |
| `BanglaBBQ_BEN_MaritalStatus` | `1929463163` | 50 | 2,881 (2,880 data) | Expanded Bengali Marital Status benchmark (Q01–Q20). 100% live parity verified (43,200 data cells, 0 mismatches). |

*All 12 active benchmark categories (24 bilingual worksheets) are now 100% live in the Master Google Spreadsheet.*

---

## 3. Active GitHub Dataset Directories

| Category | Canonical Directory | Primary Files | Record Count |
| :--- | :--- | :--- | :---: |
| **Politics** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Politics/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Politics) | `banglabbq_politics_english.jsonl`<br/>`banglabbq_politics_bengali.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Religion** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Religion/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Religion) | `Religion_eng.jsonl`<br/>`Religion_bng.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Age** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Age/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Age) | `banglabbq_age_english.jsonl`<br/>`banglabbq_age_bengali.jsonl`<br/>`PakBBQ_Age_English.csv` | 2,920 BEN<br/>2,920 ENG |
| **Gender Identity** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Gender/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender) | `Gender_identity_eng.jsonl`<br/>`Gender_identity_bng.jsonl` | 4,696 ENG<br/>4,696 BEN |
| **Educational Background** | [`Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground) | `banglabbq_education_english.jsonl`<br/>`banglabbq_education_bengali.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Ethnicity** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity) | `BanglaBBQ_Ethnicity_FINAL_english.jsonl`<br/>`BanglaBBQ_Ethnicity_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Health Status** | [`Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus) | `BanglaBBQ_Health_Status_FINAL_english.jsonl`<br/>`BanglaBBQ_Health_Status_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Marital Status** | [`Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus) | `BanglaBBQ_MaritalStatus_FINAL_english.jsonl`<br/>`BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Occupational Background** | [`Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground) | `BanglaBBQ_Occupational_Background_FINAL_english.jsonl`<br/>`BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Physical Appearance** | [`Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance) | `BanglaBBQ_Physical_Appearance_FINAL_english.jsonl`<br/>`BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Regional Affiliation** | [`Dataset_BanglaBBQ_New/BanglaBBQ_Regional/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Regional) | `BanglaBBQ_Regional_FINAL_english.jsonl`<br/>`BanglaBBQ_Regional_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |
| **Social Status** | [`Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/`](file:///d:/Research%20BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus) | `BanglaBBQ_SocialStatus_FINAL_english.jsonl`<br/>`BanglaBBQ_SocialStatus_FINAL_bengali.jsonl` | 1,440 ENG<br/>1,440 BEN |

- [x] Unified Age Benchmark into BanglaBBQ_Age (2026-10-26):
  - Eradicated legacy fragmented directories `BanglaBBQ_ENG_New` and `BanglaBBQ_BEN_New`.
  - Consolidated canonical English (`banglabbq_age_english.jsonl`), Bengali (`banglabbq_age_bengali.jsonl`), and upstream PakBBQ reference CSV into [`BanglaBBQ_Age/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Age).
  - Updated validation tooling and verified 100% test pass rate in CI.
- [x] Canonical Final Category Organization (2026-10-26):
  - Created dedicated top-level canonical directories for all 7 newly exported final benchmarks: `BanglaBBQ_Ethnicity`, `BanglaBBQ_HealthStatus`, `BanglaBBQ_MaritalStatus`, `BanglaBBQ_OccupationalBackground`, `BanglaBBQ_PhysicalAppearance`, `BanglaBBQ_Regional`, `BanglaBBQ_SocialStatus`.
  - Moved all 14 `_FINAL_` JSONL exports into their corresponding canonical directories, establishing full category-level parity with Politics, Religion, Gender, and Education.
- [x] Workspace Root Organization & Clutter Reduction (2026-10-26):
  - Moved 14 candidate and forensic QA bundles out of root into dedicated directories: [`audits/`](file:///d:/Research-BanglaBBQ/audits) (7 forensic QA complete packages) and [`candidate_bundles/`](file:///d:/Research-BanglaBBQ/candidate_bundles) (7 raw generation bundles).
  - Moved loose thesis academic papers into [`docs/papers/`](file:///d:/Research-BanglaBBQ/docs/papers) and legacy JSON execution reports into [`docs/reports/`](file:///d:/Research-BanglaBBQ/docs/reports).
  - Maintained 100% CI compatibility: offline benchmark validators for Politics, Religion, Age, Gender, and Educational Background all PASS 100% with zero regressions.


- [x] BanglaBBQ Educational Background Complete Repair and 2,880-Record Expansion Applied, 5 Defects Resolved, and 86,400-Cell Live Parity Verified (2026-10-19):
  - Completely repaired and expanded category from 128 legacy rows to exactly 20 distinct themes, 3 scenario variations (V1/V2/V3), and 2,880 records per language (5,760 total), strictly following Politics and Religion methodology.
  - Byte-for-byte preservation of seniors' historical files in `Dataset_ BanglaBBQ_Old/Educational background/` verified via SHA256 hashes (`d66b34ee1ef147ce...` ENG, `ba308416a74e0dc0...` BEN). Repaired and expanded dataset placed in dedicated directory `BanglaBBQ_EducationalBackground/`.
  - Resolved 5 legacy defects: Defect A (32 disambiguated gold label reversals corrected based on context entailment), Defect B (32 duplicate QA tuples eliminated via full 6-way answer permutations $3! = 6$), Defect C (label uniformity 960/960/960 across positions 0, 1, 2), Defect D (counterfactual symmetry in orientation 'b'), and Defect E (grounded in Asadullah 2021, Hosain 2021, World Bank 2019/2021, ILO BNQF, and national journalism).
  - Production worksheets `BanglaBBQ_ENG_Education` (sheetId: `1544720708`, index 34) and `BanglaBBQ_BEN_Education` (sheetId: `641606675`, index 35) created, formatted (33px header, 96px data, canonical column widths, wrap/clip, frozen row 1, alternating 4-row styling), and populated with 2,881 rows (1 header + 2,880 data).
  - Standalone verifier `scripts/verify_education_live_parity.py` confirmed 100% bit-for-bit live parity across all 86,400 data cells (43,200 per language, 0 mismatches).
  - 10/10 offline structural invariant tests (`scripts/validate_education_dataset.py`) and deep semantic entailment checks (`scripts/validate_education_semantics.py`) passed 100% with 0 errors. Integrated into CI workflow.
- [x] Final BanglaBBQ Gender Identity Q56 Repair Applied, 3 Defects Resolved, and 140,910-Cell Live Parity Verified (2026-10-19):
  - Completed final controlled one-pass repair of Theme Q56 (Sentencing / Probation Consideration, 32 records, Example IDs 4600–4631, Google Sheets Rows 4602–4633) across Columns F (`context`), G (`question`), and M (`additional_metadata`) in both `BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender` worksheets (192 cells total).
  - Preserved metadata: original `subcategory` (`"None"`), `stereotyped_groups` (`["M"]`), and `version` (specifically preserved `version="b"` for EIDs 4616–4631; `version="a"` for EIDs 4600–4615). Only the `source` field in `additional_metadata` was modified.
  - Corrected unnatural Bengali phrasing: eradicated hyphenated suffixes (`নারী-এর`, `পুরুষ-এর`), establishing natural Bangladeshi Bengali (`একজন পুরুষ এবং একজন নারীকে`, `পুরুষটির`, `নারীটির`, `প্রকৃত অনুশোচনা`) with exact English semantic alignment.
  - Rectified citation: removed incorrect Steffensmeier DOI `10.2307/2095909`; cited official Bangladesh Probation of Offenders Ordinance, 1960, Section 5 ([https://bdlaws.minlaw.gov.bd/act-print-302.html](https://bdlaws.minlaw.gov.bd/act-print-302.html)), accurately described as the statutory procedural framework for pre-sentence probation consideration, NOT empirical proof of gender-biased sentencing.
  - Verified 100% label entailment and counterfactual symmetry across all 32 records (zero label collisions).
  - Pre-check 0 conflicts; readback 192/192 cells verified; `scripts/verify_gender_live_parity.py` confirmed 100% bit-for-bit live parity across all 140,910 cells (0 mismatches).
  - Preserved pre-patch live cells and canonical JSONL backup in `backups/gender_pre_q56_final_repair_20261019/`.
- [x] Approved Q55 Question-Wording & Evidence-Backed Caregiving Sources Applied, Q56 Balanced Redesign Staged, and 140,910-Cell Live Parity Verified (2026-10-19):
  - Safely applied approved 32-record Q55 question-wording correction reframing child custody to societal caregiving suitability across Columns G and M in both English and Bengali production datasets (128 cells total) in `BanglaBBQ_ENG_Gender!G4570:G4601`, `BanglaBBQ_ENG_Gender!M4570:M4601`, `BanglaBBQ_BEN_Gender!G4570:G4601`, `BanglaBBQ_BEN_Gender!M4570:M4601`, and canonical JSONLs.
  - Sourced citations accurately described: Uddin et al. (2021, DOI: 10.1186/s12939-021-01404-7) for societal caregiving expectations, and Supreme Court Civil Revision No. 3298 of 2023 for child welfare principle, NOT guaranteed judicial custody outcomes.
  - Verified 100% label alignment and counterfactual symmetry across all 32 records (zero label collisions).
  - Explicitly withheld Q56 from production: forensically diagnosed previous defect where hardcoded statutory clauses broke counterfactual reversibility and contradicted gold labels in Orientation 1 (EIDs 4617, 4619, 4621, 4623, 4625, 4627, 4629, 4631).
  - Engineered and staged scientifically balanced alternative `proposed_q56_probation_scenario_redesign.json` (32 records) varying individualized probation officer findings symmetrically under Section 5(1) of the Probation of Offenders Ordinance, 1960. 100% label alignment verified. Zero production writes.
  - Pre-check 0 conflicts; readback 128/128 cells verified; 140,910-cell live parity confirmed across both sheets.
  - Preserved pre-patch backup in `backups/gender_pre_q55_question_source_20261019/`.
- [x] Evidence-Backed Source Replacements for Themes Q52–Q54 Applied, Q55–Q56 Proposals Staged, and 140,910-Cell Live Parity Verified (2026-10-19):
  - Independently confirmed genuine Bangladesh-specific sources: Q52 (World Bank 2019 Voices to Choices Ch. 3 p. 71 on sister inheritance surrender, 32 records), Q53 (Ashraf & Jepsen 2024 on female higher education marriage barriers / Amin & Huq 2008, 72 records), and Q54 (Ashraf & Jepsen 2024 on career women marriage pressure, 32 records).
  - Executed sparse patch `BanglaBBQ_Gender/review/applied_q52_q54_sources_patch.json` updating ONLY Column M (`additional_metadata`) across 136 records per language (272 cells total) in `BanglaBBQ_ENG_Gender!M4434:M4569`, `BanglaBBQ_BEN_Gender!M4434:M4569`, and canonical JSONLs.
  - Zero conflicts on pre-check; 272/272 cells verified via readback; full live parity verified across all 140,910 cells (0 mismatches).
  - Staged minimal question-wording proposal for Q55 (`proposed_q55_question_correction.json`, 32 records) and probation-eligibility scenario redesign for Q56 (`proposed_q56_probation_scenario_redesign.json`, 32 records). Zero production edits to Q55/Q56.
  - Preserved live cells backup in `backups/gender_pre_q52_q54_sources_20261019/live_sheets_backup.json` and canonical JSONLs in `backups/gender_pre_q52_q54_sources_20261019/`.
- [x] Approved Q54 English Grammar Patch Applied, Q52–Q56 Designated SOURCE_UNVERIFIED, and 140,910-Cell Live Parity Verified (2026-10-18):
  - Safely applied approved 32-row Q54 English grammar correction removing `" woman"` before `" are unmarried"` across `BanglaBBQ_ENG_Gender!F4538:F4569` and `BanglaBBQ_Gender/Gender_identity_eng.jsonl` (EIDs 4536–4567).
  - Executed `scripts/verify_gender_live_parity.py` confirming 100% bit-for-bit live parity across all 140,910 cells (70,455 per sheet, 0 mismatches).
  - Explicitly withheld 200-row citation patch and both Q56 redesigns from production per researcher directive. Themes Q52–Q56 officially designated `SOURCE_UNVERIFIED` in benchmark documentation pending primary evidence review.
  - Closed empty-value conflict loophole in `scripts/apply_sparse_gender_patch.py` and validated with 5/5 passing unit tests in `scripts/test_patch_updater_conflict.py`.
  - Moved review manifests to version-controlled `BanglaBBQ_Gender/review/`.
  - Verified preservation of Google Sheets backups (`Backup_BanglaBBQ_ENG_Gender_preRepair_20261018`, `Backup_BanglaBBQ_BEN_Gender_preRepair_20261018`) and local git backups.
- [x] Completed Checkpoints A–I remaining issues forensic audit, citation grounding, and semantic repair staging for Gender Identity (2026-10-18):
  - Checkpoint A: Re-verified baseline commit SHA `a4602f64f93531edd24521cad735b42f8f910dc8`, confirmed SHA256 integrity of canonical JSONLs, verified live Google Sheets backups (`362662769`, `1183220937`), created local snapshot in `backups/gender_pre_followup_20261018/`, and generated machine-readable audit manifest `scratch/checkpoint_a_manifest.json`.
  - Checkpoint B: Diagnosed 24 candidate collisions in Q32 (Gul vs Gul), Q40 (Zaryab vs Zaryab), Q43 (Rukhsar vs Rukhsar) as PakBBQ empty candidate slot artifacts; built verified patch proposal `scratch/checkpoint_b_proposal_manifest.json` restoring authentic female candidates (`Fatima`, `Maryam`) and balanced gold labels.
  - Checkpoint C: Formally classified 8 repeated QA tuples: Q40 duplicates confirmed as candidate collision artifacts that resolve naturally with `Maryam`; Q55 pairs confirmed as necessary ambiguous control partners across counterfactual orientations.
  - Checkpoint D: Completed 34-theme source audit (26 general academic verified, 3 partially relevant, 5 Bangladesh citations sourced); built `scratch/checkpoint_d_source_matrix.json` and rectified historical 29-theme overclaims.
  - Checkpoint E: Prepared authentic Bangladeshi cultural localization proposals for all 176 records referencing Pakistan in `scratch/checkpoint_e_proposal_manifest.json` (approval lane).
  - Checkpoint F: Enhanced semantic validation suite `scripts/validate_gender_semantics.py` with unique-answer gates, non-empty metadata checks, and role-sensitive entailment tests.
  - Checkpoint G: Built bilingual linguistic review framework `scratch/checkpoint_g_linguistic_review.json` covering all 34 themes.
  - Checkpoint H: Developed genuinely sparse, idempotent production updater `scripts/apply_sparse_gender_patch.py` and validated via dry run (156 targeted cells, 0 bulk rewrites).
  - Checkpoint I: Authored comprehensive research log `research_logs/2026-10-18_gender_remaining_issues_audit.md` and updated project memory.
- [x] Complete Gender Identity dataset repair, QA, and synchronization (2026-10-18): 0 multiword English leaks, 0 double possessives, 0 invalid hyphenated suffixes, Q11 supporter/recipient reversal fixed, 12 answer_info gender tag contradictions fixed.
- [x] Restored complete native production formatting on `BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender` (33px header height, 96px data row height, F–J WRAP, L–M CLIP, exact column widths, 6 conditional formatting rules).
- [x] Verified full live Google Sheets parity: 140,910 cells (70,440 data cells + 15 headers per sheet) with ZERO mismatches.
- [x] Completed 34-theme academic source verification matrix and proposed Bangladeshi cultural localizations for 176 Pakistani reference records in approval lane.
- [x] Enhanced automated validator `scripts/validate_gender_dataset.py` with linguistic quality checks, answer metadata consistency, regression fixtures (EIDs 0-3, 81, 1024, 1625, 2625), and flexible baseline reporting.
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

### C. Modernization and Standardization of the 7 Final Categories (Completed 2026-10-26)
- **Standardization & Live Sheets Synchronization**: Successfully standardized 7 benchmark categories (`Physical Appearance`, `Regional Affiliation`, `Marital Status`, `Social Status`, `Health Status`, `Ethnicity`, `Occupational Background`) to exactly 1,440 records per language (10 themes x 3 scenario variations x 48 rows; 10,080 records per language; 20,160 rows total).
- **Invariants Enforced**: Enforced full 6-way answer permutations ($3! = 6$), 4-row canonical condition/polarity ordering (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`), perfectly balanced labels (480 each across positions 0, 1, 2), and bilingual 1-to-1 metadata alignment.
- **Master Google Spreadsheet Import**: Created 14 new worksheets via `duplicateSheet` replicating canonical `Education` formatting (33px navy header, 96px data rows, 15 column widths, wrap/clip, frozen row 1, 5 CF rules). Uploaded all 20,160 rows and verified 100.0000% bit-for-bit live parity across all 302,400 data cells with 0 mismatches.
- **Historical Baseline Preservation**: Preserved seniors' original thesis files in `Dataset_ BanglaBBQ_Old/` byte-for-byte, including the historical 100-entry `Mental Health` dataset.
- **CI Validation Integration**: Enforced strict CI validation via `scripts/validate_seven_final_categories.py` in `.github/workflows/validate.yml`.
- **Publication Status**: **NOT publication-ready** until independent native colloquial Bengali linguistic review and external sociological source audits are completed.

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

### F. Gender Identity Benchmark Status & Outstanding Publication Considerations
- **Complete Migration, Localization & Parity**: 4,696 records per language across all 34 themes. 100% bit-for-bit live parity confirmed across all 140,910 cells (70,455 per sheet, 0 mismatches) between Google Sheets (`BanglaBBQ_ENG_Gender`, `BanglaBBQ_BEN_Gender`) and canonical local JSONLs.
- **Approved Q54 Grammar Correction Applied**: Exactly 32 English contexts (EIDs 4536–4567) updated to remove `" woman"` before `" are unmarried"`. Parallel Bengali contexts and all gold labels/IDs untouched.
- **Evidence-Backed Source Rectification (Q52–Q55)**:
  - Q52 (Inheritance, 32 records): World Bank (2019) *Voices to Choices*, Chapter 3, p. 71 (pressure on sisters to surrender land shares to brothers).
  - Q53 (Higher Education, 72 records): Ashraf & Jepsen (2024), *Group & Organization Management*, DOI: `10.1177/10596011241227263` (marriage mandated before overseas study vs brothers supported); supplementary: Amin & Huq (2008), DOI: `10.31899/pgy3.1000`.
  - Q54 (Marriage vs Career, 32 records): Ashraf & Jepsen (2024), DOI: `10.1177/10596011241227263` (private patriarchal pressure to marry vs career encouragement for men).
  - Q55 (Custody Caregiving Suitability, 32 records): Uddin et al. (2021, DOI: `10.1186/s12939-021-01404-7`) documenting societal caregiving expectations, and Supreme Court Civil Revision No. 3298 of 2023 establishing the child welfare principle. Question wording reframed to caregiving suitability expectations. 128 cells updated across Columns G and M.
- **Final Q56 Repair Applied & Verified**:
  - Q56 (Sentencing / Probation Consideration, 32 records, EIDs 4600–4631): Controlled one-pass repair across Columns F, G, M (192 cells total). Original metadata `version="a"`/`"b"`, `subcategory="None"`, and `stereotyped_groups=["M"]` preserved. Natural Bangladeshi Bengali grammar restored (`নারী-এর` / `পুরুষ-এর` eliminated). Sourced Section 5 of the Probation of Offenders Ordinance, 1960 ([https://bdlaws.minlaw.gov.bd/act-print-302.html](https://bdlaws.minlaw.gov.bd/act-print-302.html)) as the statutory framework for probation consideration.
- **Structural and Role-Entailment Validation**: Both `scripts/validate_gender_dataset.py` (10/10 PASS) and `scripts/validate_gender_semantics.py` (deep role-entailment, 100% PASS) run in CI.
- **Outstanding Requirements**: Independent native colloquial Bengali linguistic review across all 34 themes.
- **Publication Status**: **NOT publication-ready** until secondary human linguistic review across all 34 themes is conducted.
- **Status of Other Categories**: All 12 canonical working categories are now live in Google Sheets and tracked in GitHub; historical thesis baseline preserved in `Dataset_ BanglaBBQ_Old/`.

---

### G. Educational Background Benchmark Final Targeted QA Repair & Parity Verification
- **Complete Expansion & Targeted Repair**: Exactly 2,880 records per language across 20 themes (144 records/theme; V1, V2, V3 waves; 5,760 total) preserving seniors' legacy baseline files in `Dataset_ BanglaBBQ_Old/Educational background/` byte-for-byte.
- **Confirmed Semantic Defects Repaired**:
  - *Defect A (Q17 V1, EIDs 771, 775, 779, 783, 787, 791)*: Context stated "assumed" while questions asked who was "commended/praised". Repaired context to explicitly describe the club moderator criticizing the Bangla Version candidate while commending the English Version candidate for debate communicative readiness.
  - *Defect B (Q16 V2, EIDs 1707, 1711, 1715, 1719, 1723, 1727)*: Non-negative question asked about "pride" while context only stated "respect". Aligned evaluator action across both orientations to explicit disapproval (`সমালোচনার সাথে বিবেচনা করেন`) and pride (`গর্বের সাথে উল্লেখ করেন`).
  - *Defect C (Q03 V3, EIDs 2016–2063)*: Question specified "English presentation style" but context lacked English delivery. Context explicitly establishes "competitive English speeches" (`প্রতিযোগিতামূলক ইংরেজি বক্তব্য`).
  - *Defect D (Q15 V1 & V2 orientation b)*: Confounder neutralization across EIDs 696–719 and 1656–1679. Removed extraneous personal attributes (salary demands, entitlement, humility, loyalty, flight risk) to preserve pure institutional bias. Also neutralized personal entitlement in Q16 V3.
- **Criteria Harmonization Across Orientations**:
  - *Q17 V1*: Unified assessed competency across both orientations to debate communicative readiness under the national curriculum.
  - *Q20 V3*: Unified assessed competency across both orientations to commercial banking risk assessment.
  - *All 60 Scenarios Audited*: 5 confirmed defects repaired; remaining 55 scenario variants confirmed clean with matched competencies and symmetrical counterfactuals.
- **Source Attribution & Evidence Strength Calibration**:
  - Audited all 20 theme citations against primary literature.
  - Only Q01 Asadullah et al. (2023) designated `DIRECT` (randomized CV audit).
  - Downgraded Q06, Q07, Q10, Q20 from overconfident `DIRECT` to `PARTIAL / CONTEXTUAL`.
  - Q10 (World Bank Report AUS0000063) calibrated to document that surveyed private polytechnic students reported higher training satisfaction than public polytechnic students, preventing employer-bias exaggeration.
  - Q19 author citation corrected to Shiro Nakata, Uttam Sharma, Tashmina Rahman, Mokhlesur Rahman, Mustahsin-Ul Aziz (World Bank 2021, DOI 10.1596/1813-9450-9644).
- **Independent Semantic QA Engine & 16 Adversarial Fixtures**:
  - Upgraded `scripts/validate_education_semantics.py` with natural-language context extraction, evaluator predicate matching, and cross-orientation criterion symmetry.
  - Expanded `scripts/test_education_semantic_fixtures.py` from 9 to 16 comprehensive adversarial regression fixtures (16/16 rejected, 100% failure detection).
- **1-to-1 Legacy Row Lineage**: All 128 legacy rows preserved and mapped in `BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`.
- **Production Google Sheets Sparse Update & Live Parity**:
  - Sparse update executed via `scripts/apply_education_qa_repair_live.py`: 252 ENG cells, 264 BEN cells (516 total diffs documented in `qa_repair_diff_manifest.json`).
  - Bit-for-bit live parity confirmed: 0 mismatches across all 86,400 data cells in `BanglaBBQ_ENG_Education` (1544720708) and `BanglaBBQ_BEN_Education` (641606675).
- **Formal Status Separation**:
  - **Structurally Validated: YES** (10/10 invariant checks passing in `scripts/validate_education_dataset.py`, 960/960/960 labels, full 6-way permutations).
  - **Live-Synchronized: YES** (0 mismatches across all 86,400 data cells between live Google Sheets and canonical GitHub JSONLs).
  - **Independently Semantically Reviewed: YES** (Clause-level predicate entailment checks passing 100% clean, 16/16 adversarial fixtures rejected).
  - **Source-Verified: QUALIFIED / CALIBRATED** (All 20 sources re-audited, author order corrected in Q19, non-experimental DIRECT claims appropriately qualified).
  - **Linguistically Reviewed: PENDING EXTERNAL INDEPENDENT HUMAN REVIEW** (Syntactically verified; external colloquial review by native Bangladeshi speakers pending).
  - **Publication-Ready: NO** (Not until external human linguistic sign-off and formal peer review).

---

## 6. Next Recommended Actions

The primary active research priorities are:

1. **Independent Native Colloquial Bengali Linguistic Review**: Conduct formal native Bangladeshi speaker qualitative reviews across all 12 expanded/standardized categories to certify linguistic naturalness and dialectal nuance prior to publication submission.
2. **Automated Semantic Entailment & Adversarial QA Engines**: Build deep natural-language semantic entailment checkers and adversarial regression suites for the 7 newly standardized categories (analogous to `validate_education_semantics.py` and `validate_gender_semantics.py`).
3. **External Source & Sociological Evidence Audit**: Verify external institutional literature citations for all 7 new categories, ensuring transparent demarcation between macro-level sociological evidence and fictional evaluation scenarios.
4. **Historical Mental Health Baseline Policy Decision**: Formally decide with lead researcher whether to preserve the 100-record legacy `Mental Health` dataset purely as an archived thesis artifact or to engineer a separate, dedicated psychiatric bias benchmark distinct from `Health Status`.
5. **Evaluation Split Construction & De-Leakage Partitioning**: Generate deterministic, leak-free train/eval/test cross-validation splits partitioned by parent example ID and theme to enable reproducible LLM benchmarking without prompt leakage.


