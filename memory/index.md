# Workspace Index & Repository Map

> **VERIFIED REPOSITORY MAP**
> Every path listed in this index has been verified to exist on disk. Active production datasets are strictly separated from legacy baseline directories.

---

## 1. Directory Structure Overview

```
Research-BanglaBBQ/
├── .github/workflows/           # Automated CI workflows (invariant validation)
├── Dataset_BanglaBBQ_New/       # Canonical Improved & Expanded BanglaBBQ Benchmark (ONLY JSONL, 24 files named after sheets)
│   ├── BanglaBBQ_Age/               # BanglaBBQ_ENG_Age.jsonl, BanglaBBQ_BEN_Age.jsonl (2,920 records/lang)
│   ├── BanglaBBQ_EducationalBackground/ # BanglaBBQ_ENG_Education.jsonl, BanglaBBQ_BEN_Education.jsonl (2,880 records/lang)
│   ├── BanglaBBQ_Ethnicity/         # BanglaBBQ_ENG_Ethnicity.jsonl, BanglaBBQ_BEN_Ethnicity.jsonl (1,440 records/lang)
│   ├── BanglaBBQ_Gender/            # BanglaBBQ_ENG_Gender.jsonl, BanglaBBQ_BEN_Gender.jsonl (4,696 records/lang)
│   ├── BanglaBBQ_HealthStatus/      # BanglaBBQ_ENG_HealthStatus.jsonl, BanglaBBQ_BEN_HealthStatus.jsonl (2,880 records/lang)
│   ├── BanglaBBQ_MaritalStatus/     # BanglaBBQ_ENG_MaritalStatus.jsonl, BanglaBBQ_BEN_MaritalStatus.jsonl (2,880 records/lang)
│   ├── BanglaBBQ_OccupationalBackground/ # BanglaBBQ_ENG_OccupationalBackground.jsonl, BanglaBBQ_BEN_OccupationalBackground.jsonl (2,880 records/lang)
│   ├── BanglaBBQ_PhysicalAppearance/ # BanglaBBQ_ENG_PhysicalAppearance.jsonl, BanglaBBQ_BEN_PhysicalAppearance.jsonl (1,440 records/lang)
│   ├── BanglaBBQ_Politics/          # BanglaBBQ_ENG_Politics.jsonl, BanglaBBQ_BEN_Politics.jsonl (2,880 records/lang)
│   ├── BanglaBBQ_Regional/          # BanglaBBQ_ENG_Regional.jsonl, BanglaBBQ_BEN_Regional.jsonl (1,440 records/lang)
│   ├── BanglaBBQ_Religion/          # BanglaBBQ_ENG_Religion.jsonl, BanglaBBQ_BEN_Religion.jsonl (2,880 records/lang)
│   └── BanglaBBQ_SocialStatus/      # BanglaBBQ_ENG_SocialStatus.jsonl, BanglaBBQ_BEN_SocialStatus.jsonl (1,440 records/lang)
├── metadata/                    # All non-dataset artifacts moved outside (audit matrices, templates, CSVs, reviews)
│   ├── BanglaBBQ_Age/
│   ├── BanglaBBQ_EducationalBackground/
│   ├── BanglaBBQ_Gender/
│   ├── BanglaBBQ_Politics/
│   ├── BanglaBBQ_Religion/
│   ├── eval_4000/                   # Stratified 4,000 paired sample manifest and queries
│   └── eval_results/                # Empirical JSON & CSV evaluation benchmark reports
├── audits/                      # Independent Forensic QA Complete Packages (7 categories)
│   ├── Ethnicity_forensic_QA_complete/
│   ├── health_status_complete_independent_forensic_QA/
│   ├── marital_status_independent_forensic_QA_bundle/
│   ├── occupational_background_forensic_QA_complete/
│   ├── physical_appearance_independent_forensic_QA_bundle/
│   ├── Regional_independent_forensic_QA_bundle/
│   └── banglabbq_social_status_forensic_QA_complete/
├── candidate_bundles/           # Pre-Audit Candidate Benchmark Bundles & Generators (7 categories)
│   ├── banglabbq_ethnicity_bundle/
│   ├── banglabbq_health_status_complete/
│   ├── banglabbq_marital_status_readonly_research_package/
│   ├── banglabbq_occupational_background_readonly_bundle/
│   ├── banglabbq_physical_appearance_readonly_research_bundle/
│   ├── banglabbq_regional_research_bundle/
│   └── banglabbq_social_status_complete/
├── docs/                        # Academic papers and historical audit reports
│   ├── papers/                  # Undergraduate thesis book & IEEE conference paper
│   └── reports/                 # Historical expansion and correction JSON reports
├── Dataset_ BanglaBBQ_Old/      # Historical baseline from seniors' thesis (T2510616)
├── PakBBQ_Repo/                 # Cloned official PakBBQ benchmark repository (EMNLP 2025)
├── backups/                     # Timestamped backups of Google Sheets and datasets
├── scripts/                     # Automation, validation, migration, and audit scripts
├── research_logs/               # Permanent detailed research and audit logs
├── memory/                      # Authoritative shared project memory
├── CITATION.cff                 # Machine-readable academic citation metadata
├── README.md                    # Public repository documentation
└── requirements.txt             # Python dependencies
```

---

## 2. Active Production Datasets

These are the canonical, working datasets currently under active research and evaluation.

### A. Politics ([`BanglaBBQ_Politics/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Politics))

- [`banglabbq_politics_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Politics/banglabbq_politics_english.jsonl): 2,880 records across 20 source-referenced themes (Q1–Q20), 144/theme (original 48 + v2 48 + v3 48). Full 6-way permutations, four-row canonical ordering, uniform labels (960/960/960), zero exact QA duplicates, 15-column schema. Approved Q5 (historical year 2022 qualification) and Q14 (dormitory belongings negative question refinement) applied.
- [`banglabbq_politics_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Politics/banglabbq_politics_bengali.jsonl): 2,880 parallel Bengali records, source-aligned metadata, verified counterfactuals. Approved Q5, Q14, and Q19 (terminology aligned to 'সরকার-সমালোচক' / 'সরকার-সমালোচকের') applied.
- **Status**: `IN PROGRESS` (Expanded and synchronized with 100% bit-for-bit live Google Sheets parity; independent native Bengali linguistic review and external source-relevance reviews pending; not publication-ready).
- **Expansion materials**: [`expansion_v2v3_20261017/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Politics/expansion_v2v3_20261017) includes the 40 bilingual V2/V3 context templates, manifest and eight 480-row append-only shards. Canonical JSONL snapshots were materialized by GitHub Actions from SHA-verified historical backups and shards.

### B. Religion ([`BanglaBBQ_Religion/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Religion))

- [`Religion_eng.jsonl`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/Dataset_BanglaBBQ_New/BanglaBBQ_Religion/Religion_eng.jsonl): **2,880** production English records across V1/V2/V3, 20 × 144, six-way permutations and labels 960/960/960. **Q3/Q8/Q9/Q10/Q12/Q13 (144 records/theme) source-aligned repaired in all three waves**, preserving IDs 0–2879 and all gold label positions. Original pre-repair snapshots/shards held immutably; human semantic/source limits documented.
- [`Religion_bng.jsonl`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/Dataset_BanglaBBQ_New/BanglaBBQ_Religion/Religion_bng.jsonl): **2,880** production Bengali records, six themes × 144 rows revised in parallel, exact shared metadata with English, zero discrepancies across all 43,200 cells versus live production Bengali worksheet at verification; native linguistic review outstanding.
- [`review_v2v3_20261017.json`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/Dataset_BanglaBBQ_New/BanglaBBQ_Religion/review_v2v3_20261017.json): Original Q1–Q20 bilingual review source and 40 V2/V3 wording pairs, integrated into structurally validated production expansion on 2026-10-17; open source/translation caveats remain.
- **Religion source audit working tab**: `Review_Religion_Source_Audit_20261017` (gid `1272448316`) now documents applied Q3/Q8/Q9/Q10/Q12/Q13 evidence-aligned repairs and remaining provenance limits. `Review_Religion_20_Variations` (gid `1743426767`) contains refreshed production-aligned V1/V2/V3 bilingual exemplars for the six themes.
- [`expansion_v2v3_20261017/`](https://github.com/Hasinish/Research-BanglaBBQ/tree/main/Dataset_BanglaBBQ_New/BanglaBBQ_Religion/expansion_v2v3_20261017): SHA-pinned bilingual context templates, lineage manifest, and 16 240-record append-only shards (1,920 added records per language).
- [`evidence_revisions_20261017.json`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/Dataset_BanglaBBQ_New/BanglaBBQ_Religion/evidence_revisions_20261017.json): dated English/Bengali six-theme V1/V2/V3 context, question, option, gold-role and source revision manifest; production override without altering legacy input shards.
- [`scripts/apply_religion_evidence_revisions.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/apply_religion_evidence_revisions.py): deterministic, scope-limited correction layer applied after immutable expansion shard assembly; verifies all gold answer roles.
- **Status**: `IN PROGRESS` (Structurally validated and synchronized with live sheets; source relevance boundaries formalized; secondary native Bengali linguistic review pending; not publication-ready).

### C. Age ([`BanglaBBQ_Age/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Age))

- **English canonical:** [`banglabbq_age_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Age/banglabbq_age_english.jsonl), 2,920 records, 15 fields; 868 English context locality/grammar repairs + Q20 legal confound repair (112 records, 15/17 -> 19/20 in context, answers, answer_info). Reproduce and validate using `scripts/apply_age_english_localization_20261018.py` (tested in CI). Full pre-Q20 backup `Backup_BanglaBBQ_ENG_Age_preQ20LegalFix_20261018` (gid 1838448216; hidden); 0/43,800 live-vs-GitHub discrepancies.
- **Bengali canonical:** [`banglabbq_age_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Age/banglabbq_age_bengali.jsonl), 2,920 parallel records; culturally localized (Shwapno, Pathao, Tasty Treat, Dhaka/Chattogram, tea stall) + Q20 legal confound repair (112 records, 15/17 -> 19/20). Pre-Q20 backup `Backup_BanglaBBQ_BEN_Age_preQ20LegalFix_20261018` (gid 1838448217; hidden); 0/43,800 live-vs-GitHub discrepancies.
- **Upstream source reference:** [`PakBBQ_Age_English.csv`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Age/PakBBQ_Age_English.csv): 2,920 English records adapted from PakBBQ (1,872 DT + 1,048 TM).
- **Live worksheets:** `BanglaBBQ_ENG_Age` (`gid=0`) and `BanglaBBQ_BEN_Age` (`gid=1006819770`), 2,920 data rows each. 10/10 invariant validation passes.
- **Status**: `IN PROGRESS` (Structurally validated, zero underage drivers in Q20, 100% Google Sheets parity; independent colloquial Bengali linguistic review and external source-mechanism alignment remain pending; not publication-ready).

### D. Gender Identity ([`BanglaBBQ_Gender/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender))

- [`Gender_identity_eng.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/Gender_identity_eng.jsonl): **4,696** production English records across 34 themes (Q7, Q10–Q12, Q19, Q26, Q28, Q30–Q32, Q34–Q43, Q45–Q50, Q51–Q58). 15-column schema, sequential IDs 0–4695, source IDs 4388–9083, balanced labels 1577/1553/1566. Approved 32-row Q54 English grammar fix applied (`" woman are unmarried"` -> `" are unmarried"` in EIDs 4536–4567). 24 candidate collisions in Q32/Q40/Q43 repaired with authentic female names (`Fatima`, `Maryam`), 8 repeated QA tuples resolved, 176 records localized from Pakistan to authentic Bangladeshi settings (0 Pakistani references remain).
- [`Gender_identity_bng.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/Gender_identity_bng.jsonl): **4,696** production parallel Bengali records. Natural Bangladeshi Bengali translations adhering to gender-sensitive guidelines. Completely repaired: 0 English leaks, 0 double possessives, 0 invalid hyphenated suffixes, Q11 supporter/recipient role reversal fixed, 12 answer_info tags aligned, candidate collisions repaired with Bengali transliterations (`ফাতিমা`, `মরিয়ম`), 176 records localized to Bangladeshi cultural/legal contexts (`হেফাজত ও অভিভাবকত্ব`, সালিশ, নাটক).
- **Evidence-Backed Source Rectification & Scenario Repairs (Q52–Q56)**:
  - Themes Q52, Q53, and Q54 updated in production Column M with verified primary sources (World Bank 2019 *Voices to Choices* Ch. 3 p. 71; Ashraf & Jepsen 2024, DOI `10.1177/10596011241227263`).
  - Theme Q55 updated across Columns G and M reframing child custody to societal caregiving suitability expectations (Uddin et al. 2021; Supreme Court Civil Revision 3298 of 2023).
  - Theme Q56 repaired across Columns F, G, M: preserved `version="a"`/`"b"`, eliminated Bengali hyphenated suffixes (`নারী-এর`, `পুরুষ-এর`), and cited Section 5 of the Probation of Offenders Ordinance, 1960 ([https://bdlaws.minlaw.gov.bd/act-print-302.html](https://bdlaws.minlaw.gov.bd/act-print-302.html)) as statutory framework for probation consideration.
- **Review Directory ([`BanglaBBQ_Gender/review/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review))**:
  - [`applied_q56_probation_patch.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review/applied_q56_probation_patch.json): Approved and applied sparse patch updating Columns F, G, and M across 32 records/language (192 cells total).
  - [`applied_q55_question_and_source_patch.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review/applied_q55_question_and_source_patch.json): Approved and applied sparse patch updating Columns G and M across 32 records/language (128 cells total).
  - [`applied_q52_q54_sources_patch.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review/applied_q52_q54_sources_patch.json): Approved and applied sparse patch updating Column M across 136 records/language (272 cells total).
  - [`proposed_q54_grammar_patch.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review/proposed_q54_grammar_patch.json): Standalone approved grammar patch applied on 2026-10-18 (32 cells).
  - [`README.md`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Gender/review/README.md): Detailed manifest dispositions, safety guarantees, and review instructions.
- **Live worksheets**: `BanglaBBQ_ENG_Gender` (Sheet ID: `1990010101`) and `BanglaBBQ_BEN_Gender` (Sheet ID: `1990010102`), 4,697 rows (A1:O4697) each. Exactly 592 sparse cells updated across both sheets with verified sources, caregiving questions, grammar fixes, and probation scenarios. 100% bit-for-bit parity verified across all 140,910 cells (70,455 per sheet, 70,440 data + 15 headers, 0 mismatches). Full production formatting verified (navy headers #16213D, 33px header height, 96px data row height, F–J WRAP, L–M CLIP, column widths, frozen header row 1, 6 CF rules).
- **Validation**: `scripts/validate_gender_dataset.py` (10/10 PASS) and `scripts/validate_gender_semantics.py` (100% PASS with 0 collisions, 0 empty metadata, 0 disambiguated entailment errors). Both integrated into GitHub Actions CI (`.github/workflows/validate.yml`).
- **Status**: `REPAIRED / LOCALIZED / 100% PARITY-VERIFIED / ALL 34 THEMES VERIFIED / REVIEW PENDING` (Structurally, semantically, and culturally validated, 140,910 cells live verified, 0 Pakistani references; all 34 themes verified; independent native colloquial Bengali human review pending; not publication-ready).

### E. Educational Background ([`BanglaBBQ_EducationalBackground/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground))

- [`banglabbq_education_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl): **2,880** production English records across 20 verified themes (Q01–Q20), 3 scenario variations per theme (V1/V2/V3), 144 records/theme. Complete 6-way answer permutations (3! = 6), 4-row canonical BBQ block ordering (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`), uniform labels (960/960/960), zero duplicate QA tuples, canonical 15-column schema. Repaired across all seven ChatGPT audit defects (Q16 V3 explicit commendation entailment, Q16 V1 tuition-cost confounder elimination, Q15 V3 behavioral confounder neutralization, Q20 V1/V2 competency evaluation criteria harmonization, Q16 V2 English-Bengali meaning mismatch / personality leak removal).
- [`banglabbq_education_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl): **2,880** parallel production Bengali records. Natural Bangladeshi Bengali educational terminology, complete metadata parity, symmetrical counterfactual roles, verified 1-to-1 semantic alignment with English without extraneous personality traits.
- [`expansion_manifest.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/expansion_manifest.json): Machine-readable record manifest mapping all 2,880 rows to themes, scenario variations (V1/V2/V3), conditions, and counterfactual versions ('a'/'b').
- [`scenario_templates.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/scenario_templates.json): 60 distinct bilingual scenario templates (20 themes × 3 variations) with authentic Bangladeshi contexts and questions, repaired against all route-reversal defects, confounders, and unentailed predicates.
- [`legacy_to_improved_mapping.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json): Exact 1-to-1 record mapping connecting all 128 legacy records to modern V1 counterparts with explicit defect diagnoses, scenario modifications, and lineage rationales.
- [`source_audit_matrix.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/source_audit_matrix.json) & [`source_audit_matrix.md`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/source_audit_matrix.md): Complete research and evidence audit of all 20 themes with corrected publication years, DOIs, World Bank / ILO / BIDS empirical reports, national investigative journalism, calibrated evidence tiers (DIRECT strictly restricted to randomized CV audit in Q01; Q05 and Q09 calibrated to PARTIAL / CONTEXTUAL), and explicit macro-level evidence boundaries.
- [`qa_repair_diff_manifest.json`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/qa_repair_diff_manifest.json): Machine-readable audit diff manifest documenting all 516 live Google Sheets cell modifications (240 ENG, 276 BEN) across Columns F and G.
- **Live worksheets**: `BanglaBBQ_ENG_Education` (sheetId: `1544720708`, tab index 34) and `BanglaBBQ_BEN_Education` (sheetId: `641606675`, tab index 35), 2,881 rows (A1:O2881) each. 100% bit-for-bit live parity verified across all 86,400 data cells (43,200/sheet, 0 mismatches). Full production styling verified (33px header, 96px data, column widths `[100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]`, wrap/clip, frozen row 1, alternating 4-row styling).
- **Validation**: `scripts/validate_education_dataset.py` (10/10 PASS), `scripts/validate_education_semantics.py` (deep natural-language predicate and clause entailment validator, 8/8 PASS), and `scripts/test_education_semantic_fixtures.py` (23/23 adversarial regression fixtures demonstrably rejected, 100% defect rejection rate).
- **Status**: `REPAIRED / CHATGPT AUDIT RESOLVED / ADVERSARIAL QA VERIFIED (23/23) / 100% LIVE PARITY / REVIEW PENDING` (Structurally validated [YES], Live-synchronized [YES], Independently semantically reviewed [YES], Source-verified [QUALIFIED / CALIBRATED], Linguistically reviewed [PENDING EXTERNAL HUMAN], Publication-ready [NO]).

### F. Ethnicity ([`BanglaBBQ_Ethnicity/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity))

- [`BanglaBBQ_Ethnicity_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_english.jsonl): 1,440 final production English records across documented ethnic minority scenarios in Bangladesh.
- [`BanglaBBQ_Ethnicity_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl): 1,440 final parallel production Bengali records.

### G. Health Status ([`BanglaBBQ_HealthStatus/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus))

- [`BanglaBBQ_Health_Status_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_english.jsonl): **2,880** final production English records across 20 themes (Q01–Q10 somatic/chronic conditions + Q11–Q20 psychiatric/mental health expansion). Full 6-way answer permutations, 960/960/960 balanced labels, sequential IDs 8300000..8302879.
- [`BanglaBBQ_Health_Status_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_bengali.jsonl): **2,880** final parallel production Bengali records with 100% metadata and label parity. Original 1,440 prefix preserved bit-for-bit.

### H. Marital Status ([`BanglaBBQ_MaritalStatus/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus))

- [`BanglaBBQ_MaritalStatus_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_english.jsonl): **2,880** final production English records across 20 themes (Q01–Q10 female-focused themes + Q11–Q20 male bachelor/divorce/widow themes). Full 6-way answer permutations, 960/960/960 balanced labels, sequential IDs 8700000..8702879.
- [`BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl): **2,880** final parallel production Bengali records with 100% metadata and label parity. Original 1,440 prefix preserved bit-for-bit.

### I. Occupational Background ([`BanglaBBQ_OccupationalBackground/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground))

- [`BanglaBBQ_Occupational_Background_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_Occupational_Background_FINAL_english.jsonl): **2,880** final production English records across 20 themes (Q01–Q10 blue-collar/informal laborer themes + Q11–Q20 professional/corporate prestige themes). Full 6-way answer permutations, 960/960/960 balanced labels, sequential IDs 8600000..8602879.
- [`BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl): **2,880** final parallel production Bengali records with 100% metadata and label parity. Original 1,440 prefix preserved bit-for-bit.

### J. Physical Appearance ([`BanglaBBQ_PhysicalAppearance/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance))

- [`BanglaBBQ_Physical_Appearance_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_english.jsonl): 1,440 final production English records.
- [`BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl): 1,440 final parallel production Bengali records.

### K. Regional Affiliation ([`BanglaBBQ_Regional/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Regional))

- [`BanglaBBQ_Regional_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_Regional_FINAL_english.jsonl): 1,440 final production English records covering Bangladeshi regional/district stereotypes.
- [`BanglaBBQ_Regional_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_Regional_FINAL_bengali.jsonl): 1,440 final parallel production Bengali records.

### L. Social Status ([`BanglaBBQ_SocialStatus/`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus))

- [`BanglaBBQ_SocialStatus_FINAL_english.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_SocialStatus_FINAL_english.jsonl): 1,440 final production English records.
- [`BanglaBBQ_SocialStatus_FINAL_bengali.jsonl`](file:///d:/Research-BanglaBBQ/Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_SocialStatus_FINAL_bengali.jsonl): 1,440 final parallel production Bengali records.

---

## 3. Historical Baseline: Seniors' Original Dataset ([`Dataset_ BanglaBBQ_Old/`](<file:///d:/Research-BanglaBBQ/Dataset_%20BanglaBBQ_Old>))

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

- **`backups/gender_pre_q56_final_repair_20261019/`**:

  - `live_sheets_backup.json`: Live cell contents of Columns F, G, and M (`BanglaBBQ_ENG_Gender!F4602:F4633`, `G4602:G4633`, `M4602:M4633` and Bengali equivalents) before Q56 final repair.
  - `Gender_identity_eng.jsonl` & `Gender_identity_bng.jsonl`: Complete 4,696-record canonical JSONLs pre-Q56 final repair.
- **`backups/gender_pre_q55_question_source_20261019/`**:

  - `live_sheets_backup.json`: Live cell contents of Columns G and M (`BanglaBBQ_ENG_Gender!G4570:G4601`, `M4570:M4601` and Bengali equivalents) before Q55 updates.
  - `Gender_identity_eng.jsonl` & `Gender_identity_bng.jsonl`: Complete 4,696-record canonical JSONLs pre-Q55 update.
- **`backups/gender_pre_q52_q54_sources_20261019/`**:

  - `live_sheets_backup.json`: Live cell contents of Column M (`BanglaBBQ_ENG_Gender!M4434:M4569` and `BanglaBBQ_BEN_Gender!M4434:M4569`) before source updates.
  - `Gender_identity_eng.jsonl` & `Gender_identity_bng.jsonl`: Complete 4,696-record pre-update canonical JSONLs.
- **`backups/gender_pre_followup_20261018/`**:

  - `Gender_identity_eng.jsonl` & `Gender_identity_bng.jsonl`: 4,696-record baseline before grammar and remaining issue fixes.
  - `manifest.json`: Checkpoint A verification and integrity manifest.
- **`backups/gender_pre_repair_20261018/`**:

  - `BanglaBBQ_ENG_Gender.jsonl` & `BanglaBBQ_BEN_Gender.jsonl`: Initial un-repaired 4,696-record datasets.
  - `raw_sheets_data.json` & `manifest.json`: Full pre-repair Google Sheets snapshots.
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

### Production Expansion & 7-Category Validators

- [`scripts/validate_seven_final_categories.py`](file:///d:/Research-BanglaBBQ/scripts/validate_seven_final_categories.py): Generalized invariant validator for all 7 modernized categories supporting category-aware row counts (2,880 rows for Health Status, Marital Status, and Occupational Background; 1,440 rows for Physical Appearance, Social Status, Regional Affiliation, and Ethnicity). Validates schema, 6-way permutations, balanced labels, ambiguous Unknown entailment, and 14,400 tracked unique global IDs without collisions.
- [`scripts/verify_seven_final_categories_live.py`](file:///d:/Research-BanglaBBQ/scripts/verify_seven_final_categories_live.py): Full live readback audit verifying all 14 worksheets across the master Google Spreadsheet (432,000 data cells total) against canonical exports, confirming 100.0000% parity, 0 cell mismatches, correct grid dimensions (2,881 rows for HS/MS/OB, 1,441 rows for PA/SS/RA/ETH), and 5 conditional formatting rules.
- [`scripts/validate_expansion_append_files.py`](file:///d:/Research-BanglaBBQ/scripts/validate_expansion_append_files.py): Multi-gate standalone validator for the six candidate append files (Health Status, Marital Status, Occupational Background Q11–Q20; 8,640 records total) testing schema, permutations, 180:180 positional balance, and running a 9-fixture adversarial suite with 100% rejection rate.
- [`scripts/backup_pre_expansion_state.py`](file:///d:/Research-BanglaBBQ/scripts/backup_pre_expansion_state.py): Pre-expansion snapshot utility creating bit-for-bit backups of all 6 local production files and exporting live rows 1..1441 for all 6 target worksheets into `backups/pre_expansion_20261028/`.
- [`scripts/append_expansion_to_production.py`](file:///d:/Research-BanglaBBQ/scripts/append_expansion_to_production.py): Deterministic append script integrating Q11–Q20 rows to canonical JSONLs with strict prefix verification (zero Q01–Q10 byte drift).
- [`scripts/append_expansion_to_google_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/append_expansion_to_google_sheets.py): Batch uploader appending rows 1442..2881 to Google Sheets, setting 2,881 grid row count, applying 96px row height, and verifying full readback.
- [scripts/sync_drive_dataset.py](file:///d:/Research-BanglaBBQ/scripts/sync_drive_dataset.py): Enterprise-grade Google Drive dataset synchronizer featuring 5 safety gates: (1) Pre-flight invariant validation (schema, 15 fields, sequential IDs, line counts), (2) SHA-256 and MD5 dual-hash verification against Drive native checksums and custom properties, (3) Anomaly detection for missing, outdated, and unexpected files, (4) Safe in-place remote updates via Google Drive API, and (5) Exhaustive post-sync verification gate auditing all 24 remote files.
- [	ests/test_drive_sync_safety.py](file:///d:/Research-BanglaBBQ/tests/test_drive_sync_safety.py): Unit test suite verifying that sync_drive_dataset.py rejects corrupted schemas, bad labels, and invalid line counts before contacting remote services.

- [`scripts/apply_politics_q5_q14_q19_fixes.py`](file:///d:/Research-BanglaBBQ/scripts/apply_politics_q5_q14_q19_fixes.py): Idempotent content correction script applying approved Q5 historical date, Q14 entailment, and Q19 Bengali critic terminology fixes.
- [`scripts/validate_politics_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_politics_dataset.py): Expanded 960/2,880-aware validator with dual-hash verification (preserving historical baseline hashes as evidence while supporting approved post-repair hashes for active benchmark), V2/V3 lineage, permutations, bilingual alignment, and 0 duplicates.
- [`scripts/assemble_politics_expansion.py`](file:///d:/Research-BanglaBBQ/scripts/assemble_politics_expansion.py): Verifies append-only expansion from hashed pre-expansion backups and shards, with cross-platform CRLF normalization and recognized post-repair canonical records.
- [`scripts/validate_religion_dataset.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/validate_religion_dataset.py): 10-category structural invariant validator accepting both 960 historical and 2,880 expanded bilingual files, including variant-aware six-way answer permutations.
- [`scripts/assemble_religion_expansion.py`](https://github.com/Hasinish/Research-BanglaBBQ/blob/main/scripts/assemble_religion_expansion.py): hash-pinned append-only assembly from immutable V1 snapshots and 16 shards, validating inherited answers, metadata, source links, counterfactuals, bilingual shared fields, labels and record counts.
- [`scripts/validate_gender_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_gender_dataset.py): Automated 10-invariant offline dataset validator checking record counts (4,696 each), sequential IDs (0–4695), 15-column schema, 100% bilingual metadata parity, gold label semantic grounding (2348 ambig -> 'তথ্য অপর্যাপ্ত', 2348 disambig -> entity), answer permutations, Bengali script integrity, 34 question themes, and inherited defect audits.
- [`scripts/generate_gender_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/generate_gender_dataset.py): Deterministic generator and translation pipeline processing all 4,696 English records from PakBBQ source, translating unique context/QA entities into fluent Bangladeshi Bengali, and exporting canonical English and Bengali JSONLs with the exact 15-column schema to `BanglaBBQ_Gender/`.
- [`scripts/gender_translation/`](file:///d:/Research-BanglaBBQ/scripts/gender_translation): Modular translation engine components (`base_mappings.py`, `group1_translator.py`, `group2_translator.py`, `group3_translator.py`).
- [`scripts/assemble_education_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/assemble_education_dataset.py): Assembles canonical English and Bengali JSONLs (2,880 rows each) from 60 scenario templates (20 themes × 3 variations) with 6-way permutations and balanced 4-row BBQ blocks.
- [`scripts/validate_education_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/validate_education_dataset.py): 10-invariant automated dataset validator checking record counts, schema, 144 theme balance, 4-row block sequence, 960/960/960 labels, 6-way permutations, ambiguous Unknown invariant, disambiguated named-entity grounding, bilingual metadata parity, and zero duplicate QA tuples.
- [`scripts/validate_education_semantics.py`](file:///d:/Research-BanglaBBQ/scripts/validate_education_semantics.py): Deep semantic & role-entailment validator verifying ambiguous Unknown entailment, disambiguated grounding, sub-block permutation invariance, and symmetrical counterfactual inversions.
- [`.github/workflows/validate.yml`](file:///d:/Research-BanglaBBQ/.github/workflows/validate.yml): Automated GitHub Actions CI workflow executing offline validators on every push and pull request.

### Live Google Sheets Sync & Verification

- [`scripts/apply_education_qa_repair_live.py`](file:///d:/Research-BanglaBBQ/scripts/apply_education_qa_repair_live.py): Executes sparse production patches across Columns F, G, M for `BanglaBBQ_ENG_Education` (3,096 cells) and `BanglaBBQ_BEN_Education` (3,156 cells), records diff manifest, and verifies 100% bit-for-bit parity across all 86,400 data cells.
- [`scripts/sync_education_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/sync_education_sheets.py): Chunked uploader writing all 2,881 rows (A1:O2881) of `BanglaBBQ_ENG_Education` (1544720708) and `BanglaBBQ_BEN_Education` (641606675) to the Master Google Spreadsheet and applying canonical formatting (33px header, 96px data, canonical column widths, wrap/clip, frozen row 1, alternating 4-row styling).
- [`scripts/verify_education_live_parity.py`](file:///d:/Research-BanglaBBQ/scripts/verify_education_live_parity.py): Exhaustive cell-by-cell live verification comparing all 86,400 data cells against local canonical JSONLs, confirming 0 mismatches and 100% live parity.
- [`scripts/upload_bengali_gender_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/upload_bengali_gender_sheets.py): Chunked idempotent uploader writing all 4,697 rows (A1:O4697) of `BanglaBBQ_BEN_Gender` (Sheet ID: 1990010102) to the Master Google Spreadsheet.
- [`scripts/apply_gender_sheets_formatting.py`](file:///d:/Research-BanglaBBQ/scripts/apply_gender_sheets_formatting.py): Applies exact production formatting across both `BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender` (Sheet IDs: 1990010101, 1990010102) matching Religion/Age standards.
- [`scripts/verify_gender_live_parity.py`](file:///d:/Research-BanglaBBQ/scripts/verify_gender_live_parity.py): Exhaustive cell-by-cell live verification comparing all 140,880 data cells (70,440 cells x 2 sheets) against local canonical JSONLs, confirming 0 mismatches, exact grid dimensions, and rule parity.
- [`scripts/sync_and_validate_age.py`](file:///d:/Research-BanglaBBQ/scripts/sync_and_validate_age.py): Synchronizes live Google Sheets updates from `BanglaBBQ_BEN_Age` to `BanglaBBQ_BEN_New/Age.jsonl` and executes 10-invariant benchmark quality assurance tests across all 20 themes.
- [`scripts/push_age_repairs.py`](file:///d:/Research-BanglaBBQ/scripts/push_age_repairs.py): Pushes deterministic batch updates for repaired themes to Google Sheets and updates local canonical files.
- [`scripts/verify_politics_960_live.py`](file:///d:/Research-BanglaBBQ/scripts/verify_politics_960_live.py): Historical 960-row Politics baseline verification utility; not a full 2,880-record expanded-sheet validator. The 2026-10-17 expansion was independently verified with 15-field live chunk readbacks.
- [`scripts/verify_religion_live.py`](file:///d:/Research-BanglaBBQ/scripts/verify_religion_live.py): Fetches live Google Sheets tabs `BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion` and verifies complete parity with GitHub JSONL files.
- [`scripts/list_sheets.py`](file:///d:/Research-BanglaBBQ/scripts/list_sheets.py): Lists all worksheets, sheet IDs, and indices in the master Google Spreadsheet.

### Forensic Audit & Diagnostic Tools

- [`scripts/test_education_semantic_fixtures.py`](file:///d:/Research-BanglaBBQ/scripts/test_education_semantic_fixtures.py): Adversarial regression test suite containing 9 seeded semantic errors (contradictions, role inversions, leaks, invalid sources) verifying 100% rejection rate by semantic validator.
- [`scripts/audit_cultural_localization.py`](file:///d:/Research-BanglaBBQ/scripts/audit_cultural_localization.py): Scans Age TM records (Q13–Q20) for Pakistani commercial/geographic entities and compares against Bengali domestic localizations.
- [`scripts/audit_religion_sources_and_translation.py`](file:///d:/Research-BanglaBBQ/scripts/audit_religion_sources_and_translation.py): Comprehensive audit suite for Religion Q1–Q20 verifying theme-by-theme source classification, counterfactual reversibility/symmetry, ambiguous/disambiguated entailment invariants, and documentation of macro evidence boundaries.
- [`scripts/repair_politics_dataset.py`](file:///d:/Research-BanglaBBQ/scripts/repair_politics_dataset.py): Deterministically aligned 720 Bengali `answer_info` records.
- [`scripts/apply_p1_p2_corrections.py`](file:///d:/Research-BanglaBBQ/scripts/apply_p1_p2_corrections.py): Applied Grandparent/Grandchild (56 rows) and Q7 (48 rows) fixes to Age.

---

## 6. Academic Artifacts & Methodological Reference Repositories

- [`docs/papers/T2510616.pdf`](file:///d:/Research-BanglaBBQ/docs/papers/T2510616.pdf): Complete 84-page BRAC University undergraduate thesis book (*"A Bilingual Study of Socio-Cultural Bias in Large Language Models through BanglaBBQ and a Post Processing Mitigation Pipeline"*, June 2025).
- [`docs/papers/T2510616_IEEE_Paper.pdf`](file:///d:/Research-BanglaBBQ/docs/papers/T2510616_IEEE_Paper.pdf): 8-page IEEE conference paper draft. Formulates benchmark metrics, Fleiss' Kappa formulas, paired t-tests, and SafeLLM 3-stage mitigation architecture.
- [`docs/reports/`](file:///d:/Research-BanglaBBQ/docs/reports): Historical audit and dataset expansion report JSON files (`politics_correction_report.json`, `politics_240_expansion_report.json`, `modified_records_report.json`, `p1_p2_report_data.json`).
- [`PakBBQ_Repo/`](file:///d:/Research-BanglaBBQ/PakBBQ_Repo): Cloned official repository of PakBBQ (*"PakBBQ: A Culturally Adapted Bias Benchmark for Question Answering in Pakistan"*, EMNLP 2025 / arXiv:2508.10186). Contains 8 benchmark categories in English and Urdu, evaluation scripts, and analysis notebooks.
- [`CITATION.cff`](file:///d:/Research-BanglaBBQ/CITATION.cff): Formal citation metadata for the BanglaBBQ project and ongoing research.

---

## 7. Independent Forensic QA Packages ([`audits/`](file:///d:/Research-BanglaBBQ/audits))

Contains the seven independent forensic QA audit packages (audited JSONLs, adversarial test suites, issue ledgers, change manifests, and reproducibility logs):

- [`audits/Ethnicity_forensic_QA_complete/`](file:///d:/Research-BanglaBBQ/audits/Ethnicity_forensic_QA_complete): Audited ethnicity benchmark, adversarial suites, change manifests, and source matrices.
- [`audits/health_status_complete_independent_forensic_QA/`](file:///d:/Research-BanglaBBQ/audits/health_status_complete_independent_forensic_QA): Health status independent forensic QA suite, reports, and evidence matrices.
- [`audits/marital_status_independent_forensic_QA_bundle/`](file:///d:/Research-BanglaBBQ/audits/marital_status_independent_forensic_QA_bundle): Marital status audited datasets, adversarial paired suite, and issue ledger.
- [`audits/occupational_background_forensic_QA_complete/`](file:///d:/Research-BanglaBBQ/audits/occupational_background_forensic_QA_complete): Occupational background audited datasets, fault injection logs, and reports.
- [`audits/physical_appearance_independent_forensic_QA_bundle/`](file:///d:/Research-BanglaBBQ/audits/physical_appearance_independent_forensic_QA_bundle): Physical appearance audited datasets, quantitative results, and validators.
- [`audits/Regional_independent_forensic_QA_bundle/`](file:///d:/Research-BanglaBBQ/audits/Regional_independent_forensic_QA_bundle): Regional affiliation audited datasets, candidate screening, and QA reports.
- [`audits/banglabbq_social_status_forensic_QA_complete/`](file:///d:/Research-BanglaBBQ/audits/banglabbq_social_status_forensic_QA_complete): Social status audited datasets, adversarial testing, and forensic reports.

---

## 8. Candidate Benchmark Bundles ([`candidate_bundles/`](file:///d:/Research-BanglaBBQ/candidate_bundles))

Pre-audit generation packages, raw candidate JSONLs, and generator scripts for 7 categories:

- [`candidate_bundles/banglabbq_ethnicity_bundle/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_ethnicity_bundle)
- [`candidate_bundles/banglabbq_health_status_complete/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_health_status_complete)
- [`candidate_bundles/banglabbq_marital_status_readonly_research_package/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_marital_status_readonly_research_package)
- [`candidate_bundles/banglabbq_occupational_background_readonly_bundle/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_occupational_background_readonly_bundle)
- [`candidate_bundles/banglabbq_physical_appearance_readonly_research_bundle/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_physical_appearance_readonly_research_bundle)
- [`candidate_bundles/banglabbq_regional_research_bundle/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_regional_research_bundle)
- [`candidate_bundles/banglabbq_social_status_complete/`](file:///d:/Research-BanglaBBQ/candidate_bundles/banglabbq_social_status_complete)

---

## 9. Authoritative Shared Memory System ([`memory/`](file:///d:/Research-BanglaBBQ/memory))

- [`memory/README.md`](file:///d:/Research-BanglaBBQ/memory/README.md): **Mandatory Entry Point**. Research mission declaration, roles of Google Sheets / GitHub / memory, synchronization protocol, and mandatory research logging rules.
- [`memory/purpose.md`](file:///d:/Research-BanglaBBQ/memory/purpose.md): **Official Research Mission**. Historical thesis context, defects of legacy baseline, BBQ & PakBBQ methodological roles, 9 bias categories, bilingual standards, and publication roadmap.
- [`memory/state.md`](file:///d:/Research-BanglaBBQ/memory/state.md): **Current Verified Progress Dashboard**. Category-by-category status table, live Google Sheet IDs, active paths, and transparent research-quality blockers.
- [`memory/history.md`](file:///d:/Research-BanglaBBQ/memory/history.md): **Historical Research Log**. Chronological append-only milestone log documenting dataset transformations and bug fixes.
- [`memory/index.md`](file:///d:/Research-BanglaBBQ/memory/index.md): **Workspace Index & Repository Map** (this document).
- [`memory/personality.md`](file:///d:/Research-BanglaBBQ/memory/personality.md): **Communication Guidelines**. Guidelines defining assistant persona and response style. *(Does not override research integrity, dataset safety, or factual verification).*

> **Notice on `personal_info.md`**:
> Developer personal profiles (e.g. `personal_info.md`), OAuth authentication secrets (`token.json`), and private communications are **intentionally git-ignored via `.gitignore`** to safeguard personal privacy. They are not part of the tracked public GitHub memory.

---

## 10. Permanent Research Logs ([`research_logs/`](file:///d:/Research-BanglaBBQ/research_logs))

- [`research_logs/README.md`](file:///d:/Research-BanglaBBQ/research_logs/README.md): Research logging guidelines, relationship to memory, and chronological index of all milestone logs.
- [`research_logs/2026-10-29_canonical_61312_llama31_8b_evaluation.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-29_canonical_61312_llama31_8b_evaluation.md): Complete population parameter benchmark of all 61,312 queries for meta-llama/Llama-3.1-8B-Instruct on NVIDIA L40S GPU; uncovered systemic cross-lingual safety alignment collapse across 10 of 12 categories (+0.1694 global delta, Bengali accuracy collapsing to 60.03%, ambiguous epistemic accuracy down to 22.84%).
- [`research_logs/2026-10-29_canonical_61312_gemma2_and_llama31_evaluations.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-29_canonical_61312_gemma2_and_llama31_evaluations.md): Full population parameter evaluation of 61,312 queries for google/gemma-2-9b-it on NVIDIA L40S GPU and head-to-head comparison with meta-llama/Llama-3.1-8B-Instruct; confirmed cross-lingual bias deltas in Health (+0.2722), Appearance (+0.2083), Social (+0.0652), and Politics (+0.0527), and demonstrated LLaMA's systemic cross-lingual alignment collapse (+0.1694 global bias delta).
- [`research_logs/2026-10-29_llama31_8b_4000_sample_evaluation.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-29_llama31_8b_4000_sample_evaluation.md): 4,000 paired sample evaluation of meta-llama/Llama-3.1-8B-Instruct across all 12 categories via vLLM on NVIDIA L40S; proved systemic cross-lingual safety collapse across 10 of 12 categories (Bengali ambiguous accuracy down to 26.92%, bias up to +0.7184) and decisively refuted dataset leakage hypotheses.
- [`research_logs/2026-10-29_gemma2_9b_4000_sample_evaluation.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-29_gemma2_9b_4000_sample_evaluation.md): Initial 4,000 paired sample benchmark on google/gemma-2-9b-it via vLLM on NVIDIA L40S; discovered severe cross-lingual safety alignment degradation in Health Status (+0.3167 delta), Social Status (+0.1667 delta), and Physical Appearance (+0.1666 delta).
- [`research_logs/2026-10-19_educational_background_independent_qa_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-19_educational_background_independent_qa_repair.md): Final independent QA repair across 20 themes (2,880 rows/lang); 12 confirmed orientation 'b' counterfactual defects repaired; high-risk scenarios and evaluator roles reconciled; all 20 theme sources re-audited and qualified; semantic validator upgraded with independent entailment checks; 9/9 passing adversarial regression fixtures; 6,252 sparse cells updated and 86,400 data cells verified 100% bit-for-bit live parity.
- [`research_logs/2026-10-19_educational_background_repair_and_expansion.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-19_educational_background_repair_and_expansion.md): Complete repair of 128 legacy records and expansion to 20 themes (V1/V2/V3), 2,880 records/language (5,760 total); 5 legacy defects resolved; 10/10 offline structural invariants and deep semantic entailment passed; live Google Sheets tabs `BanglaBBQ_ENG_Education` (1544720708) and `BanglaBBQ_BEN_Education` (641606675) created and verified 100% bit-for-bit across all 86,400 data cells.
- [`research_logs/2026-10-19_gender_q56_final_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-19_gender_q56_final_repair.md): Final one-pass repair of Theme Q56 (32 records/lang, 192 cells total across Col F, G, M); version="a"/"b" metadata preserved; natural Bangladeshi Bengali syntax without hyphenated suffixes restored; Probation of Offenders Ordinance 1960 Section 5 cited as statutory legal framework; 140,910-cell live parity confirmed.
- [`research_logs/2026-10-19_gender_q55_approval_and_q56_balanced_proposal.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-19_gender_q55_approval_and_q56_balanced_proposal.md): Approved Q55 question-wording & caregiving source update applied (32 records/lang, 128 cells total across Col G & M); sources accurately described as caregiving expectations (not custody outcomes); Q56 previous defect diagnosed and withheld from production; scientifically balanced Section 5 probation proposal staged in review.
- [`research_logs/2026-10-19_gender_q52_q54_sources_and_q55_q56_proposals.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-19_gender_q52_q54_sources_and_q55_q56_proposals.md): Evidence-backed source replacements for Themes Q52–Q54 (136 records/lang, 272 cells in Col M) applied and live-verified across 140,910 cells; Q55 child-custody caregiving question proposal staged; Q56 Section 5 probation-eligibility scenario proposal staged.
- [`research_logs/2026-10-18_gender_citation_grammar_semantic_refinements.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-18_gender_citation_grammar_semantic_refinements.md): Approved 32-row Q54 English grammar repair execution; role-entailment validator upgraded; patch conflict loophole closed; 140,910-cell live parity verified.
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
