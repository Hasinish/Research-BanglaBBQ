# BanglaBBQ Health Status (Physical Health) — Local Read-only QA Report

**Prepared:** 2026-10-26 (Asia/Dhaka).  
**Category:** `Health_status` (**PROPOSED NEW** category, outside original nine).  
**Status:** **AUTOMATED STRUCTURAL QA PASSED; NOT publication-ready.**  
**Total records generated:** English 1440; Bengali 1440; combined 2880.  
**Fictionality:** All 30 scenario variations are **invented for a benchmark**, not reports of real cases. Literature supports potential bias mechanisms, not fictional outcomes.

## 1. Read-only grounding and category boundary

- Connected GitHub `main` was fetched for `memory/README.md`, `memory/purpose.md`, `memory/state.md`, `memory/index.md` and recent `memory/history.md` (latest memory verified through 2026-10-20). Original thesis `T2510616.pdf` and IEEE draft were reviewed. Original BanglaBBQ has **nine categories including Mental Health and Physical Appearance** but does **not** contain `Health_status`.
- Live Google Sheets workbook: <https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit>. The 37 tabs include no Health Status sheet. Existing Education / Politics ENG/BEN records established 15-field schema, `NA`, `version` a/b, `subcategory` `None`, answer-info conventions and row ordering. Live sheet order is A:O `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`; JSONL uses the same **15 fields** in the explicitly required JSONL order listed in the manifest. No worksheet was created or changed.
- Physical health includes diagnosis, treatment and recovery history. **Excluded:** psychiatric conditions, autism/ADHD as neurodevelopmental traits, disability status as an independent target, skin/appearance ratings, clinically valid safety restrictions, and hypothetical contagion when none is supported. Epilepsy included as **neurological physical-health diagnosis**, only for non-hazardous writing/reading tasks.
- HIV, hepatitis B and current TB can require clinically appropriate precautions in certain activities. The scenarios do **not** give medical advice or claim these diseases are never transmissible; tasks are nonclinical, non-exposure, or administrative, with all relevant eligibility equal. Post-treatment TB and recovered COVID-19 scenarios explicitly establish no current infection risk.

## 2. PakBBQ baseline audit — NO_DIRECT_EQUIVALENT

- Repository: <https://github.com/Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA>.
- **Verified `main` commit:** `c079dbae2d676f4e3bb82982144d6d4ac10436d4` (published upstream commit dated 2025-11-05).
- **Exact checked file:** `PakBBQ/PakBBQ_ENG/Disability_status.jsonl` (blob SHA `1a4b58cb5e56a7a9d52130e9f0103b2262e60b0b`). GitHub `fetch_blob` returned and JSON-parsed all **1,380 rows**, spanning **33 distinct `question_index` values**: 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 15, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38.
- Its themes concern impairments/disability, deafness/blindness, neurodevelopmental and psychiatric status. These are **not equivalent** to physical illness/treatment/recovery stigma. No direct analogous source category or records were used. Upstream sources (including Pakistani examples) are not treated as evidence about Bangladesh.
- Crosswalk **`banglabbq_health_status_pakbbq_theme_crosswalk.csv`** has 33 enumerated upstream indices marked `NOT_RELEVANT` plus 10 independent Bangladesh proposals marked `REPLACE` / `NO_DIRECT_EQUIVALENT`. Row-wise source URLs reflect upstream citations only; they are not independently validated as Bangladeshi evidence. Missing original disability category indices were not invented.
- Neither the original thesis's Mental Health category nor the legacy Physical Appearance category was repurposed. `legacy_rows_reused=0`, `legacy_records_altered=0`.

## 3. Source audit and candidate selection

**Candidates screened: 12 distinct health-stigma mechanisms/conditions.** Ten were retained; two were rejected as insufficiently isolated from disability/appearance or unsupported for the intended stigma mechanism.

- **Rejected: lymphatic filariasis/lymphoedema**. Bangladesh research describes social exclusion but often inseparable from visible limb changes/disability. Relevant study: <https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0013384>. Excluded to prevent measuring physical appearance/ability rather than health status.
- **Rejected: chronic kidney disease disclosure**. Relevant Bangladesh clinical/social studies were identified, but a credible direct source for unjustified peer/hiring selection by kidney-disease status was not established. No candidate rows generated. Example screened study: <https://pubmed.ncbi.nlm.nih.gov/42005050/>.

Selected themes, evidence tier, and caveat:

- **Q01 HIV disclosure and non-clinical employment** — DIRECT; Source documents actual workplace stigma, not any fictional firm's particular decision.
- **Q02 HIV disclosure and appointment-access prejudice** — DIRECT; Provider-level clinical denial reported; fictional receptionist decisions are an administrative analogue, not documented incidents.
- **Q03 Completed tuberculosis treatment and coworker acceptance** — DIRECT; Clearly completed treatment and medical clearance; no current contagion or task restrictions; online convenience sample not nationally representative.
- **Q04 Leprosy treatment history and community inclusion** — PARTIAL; This theme needs disease-vs-disability construct validation. The 2026-10-16 published correction changes study-site/method wording, not the reported discrimination proportions.
- **Q05 Recovered COVID-19 survivors and community acceptance** — DIRECT; Interview research illustrates lived experiences; fictional events are not actual cases and are confined to past pandemic-era settings.
- **Q06 Thalassemia disclosure and peer-group acceptance** — DIRECT; Direct Bangladesh peer-friendship attitude evidence exists, but exact debate/film/history club selection has not been observed by the source.
- **Q07 Arsenicosis-related community participation stigma** — DIRECT; Arsenicosis can produce visible symptoms; manuscript must independently review the proposed non-appearance construct.
- **Q08 Epilepsy status and academic-group belonging** — DIRECT; Clinic-based adolescent self-report does not directly establish actual editors' choices.
- **Q09 Breast cancer treatment history and women's community inclusion** — PARTIAL; Evidence is for patients' community neglect and judgmental attitudes; survivor-specific committee selection is an extrapolation requiring external validation.
- **Q10 Chronic hepatitis B disclosure and non-exposure social inclusion** — DIRECT; Hepatitis B is transmissible by specific routes; no claim that it is universally noninfectious. Fictional activities require no medically relevant exposure.

Evidence tier **DIRECT** means Bangladesh-specific study documented the **stigma mechanism or respondent perception**; **PARTIAL** means a plausible bias mechanism is documented but the narrow target population, survival stage, or fictional institution/action is not directly measured. Direct evidence does **not** mean the precise fictional event took place or the study is representative. Source record detail and links: `banglabbq_health_status_source_audit.csv`. Evidence-tier distribution: {'DIRECT': 8, 'PARTIAL': 2}. Source URLs were researched using external source pages and abstracts; no independent expert has certified all medical/social interpretations.

## 4. Exact expansion design and lineage

- Ten independent themes Q01–Q10, three explicitly different settings/tasks/evaluators per theme, three waves V1 Q01..Q10 (example_ids 0–479), V2 Q01..Q10 (480–959), and V3 Q01..Q10 (960–1439).
- Each 48-record variation consists of **a** (first 24) and **b** (next 24). For each orientation, all six permutations of the first named person / second named person / Unknown are generated; each permutation has ordered four conditions: `ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`.
- **Counterfactual method:** the **same two named fictional individuals, same accomplishments, same evaluators, same explicit outcomes**. Version **a** assigns the physical-health condition to the first named person, while version **b** assigns it to the second named person. Thus a negative outcome switches from the condition-bearing to the unaffected person **without changing qualifications or event facts**. English names correspond to their Bengali transcriptions (for example, Rifat/রিফাত); names remain unchanged across a/b. In disambiguated prompts, the first named person explicitly receives a negative outcome and the second explicitly receives the corresponding positive outcome; negative vs nonnegative questions ask these exact outcomes. In ambiguous prompts, neither outcome is stated.
- Manifest: `banglabbq_health_status_expansion_manifest.json` includes 30 complete bilingual base variants, source link, 60 orientation-block row and hypothetical spreadsheet ranges, orientation and gold role, provenance, no legacy linkage, and IDs.
- Every English/Bengali row has same `example_id` (0..1439) and **provisional** category `id` (8300000..8301439), `question_index` integer, `label` integer, role-coded answer-info, 15 top-level keys; Bengali answer text and context naturally differ as expected. `type='NA'`.
- **Live collision sentinel:** The `id` column O of all **ten active production ENG/BEN tabs** was searched for string `8300`: there was one unrelated legacy `8300` in each Gender sheet and zero such hits in the eight others; **no** value in 8,300,000..8,301,439 was returned. A complete recheck at future import remains necessary because no write/import occurred.

## 5. Executed automated QA

| Test | Actual result | Detail |
|---|---|---|
| jsonl_record_counts | PASS | English=1440, Bengali=1440; expected 1440 per language |
| jsonl_schema_and_types | PASS | all rows exactly 15 named keys with expected primitives, category and NA type |
| en_seq_example_ids | PASS | 0..1439 unique and strictly sequential |
| en_seq_provisional_ids | PASS | 8300000..8301439, strictly sequential |
| en_balanced_label_positions | PASS | positions={2: 480, 0: 480, 1: 480} |
| en_balanced_conditions | PASS | condition counts={('ambig', 'neg'): 360, ('disambig', 'neg'): 360, ('ambig', 'nonneg'): 360, ('disambig', 'nonneg'): 360} |
| en_no_duplicate_complete_qa | PASS | 0 accidentally duplicate complete QA tuples; permuted answer positions counted as distinct |
| en_theme_counts | PASS | themes={1: 144, 2: 144, 3: 144, 4: 144, 5: 144, 6: 144, 7: 144, 8: 144, 9: 144, 10: 144} |
| en_answer_info_positions | PASS | all answer_info roles map to matching option text and target/control/unknown exactly once |
| en_unknown_ambiguous | PASS | every ambiguous gold label points to explicit unknown option |
| en_disambig_entailment_by_design | PASS | explicit resolving sentence always describes A negative and B positive; no ambiguous role assigned |
| en_all_6_permutations_per_orientation_condition | PASS | for every 24-row oriented variation and all 4 conditions, 6 role permutations exactly once |
| en_canonical_four_order | PASS | exact 4-condition order repeated within 6 permutations in both orientations |
| en_metadata_conventions | PASS | subcategory None, version a/b, verified-source URL, exactly one target group |
| en_counterfactual_A_B_health_only | PASS | a has first named person as target, b has first as matched comparison; labels and factual outcomes remain name-based |
| bn_seq_example_ids | PASS | 0..1439 unique and strictly sequential |
| bn_seq_provisional_ids | PASS | 8300000..8301439, strictly sequential |
| bn_balanced_label_positions | PASS | positions={2: 480, 0: 480, 1: 480} |
| bn_balanced_conditions | PASS | condition counts={('ambig', 'neg'): 360, ('disambig', 'neg'): 360, ('ambig', 'nonneg'): 360, ('disambig', 'nonneg'): 360} |
| bn_no_duplicate_complete_qa | PASS | 0 accidentally duplicate complete QA tuples; permuted answer positions counted as distinct |
| bn_theme_counts | PASS | themes={1: 144, 2: 144, 3: 144, 4: 144, 5: 144, 6: 144, 7: 144, 8: 144, 9: 144, 10: 144} |
| bn_answer_info_positions | PASS | all answer_info roles map to matching option text and target/control/unknown exactly once |
| bn_unknown_ambiguous | PASS | every ambiguous gold label points to explicit unknown option |
| bn_disambig_entailment_by_design | PASS | explicit resolving sentence always describes A negative and B positive; no ambiguous role assigned |
| bn_all_6_permutations_per_orientation_condition | PASS | for every 24-row oriented variation and all 4 conditions, 6 role permutations exactly once |
| bn_canonical_four_order | PASS | exact 4-condition order repeated within 6 permutations in both orientations |
| bn_metadata_conventions | PASS | subcategory None, version a/b, verified-source URL, exactly one target group |
| bn_counterfactual_A_B_health_only | PASS | a has first named person as target, b has first as matched comparison; labels and factual outcomes remain name-based |
| en_bn_ids_and_qa_metadata_parity | PASS | all 1440 row pairs match on IDs, conditions, question indices, gold positions, target codes and identical metadata |
| different_variations_and_30_base_scenarios | PASS | 10 themes x 3 authored scenario variations x 48 rows = 1440; 60 orientation 24-row blocks |
| pakbbq_adjacent_audit_coverage | PASS | 33 distinct adjacent disability indices and 1380 upstream records; no direct physical-health counterpart |
| source_link_and_tier_coverage | PASS | 10 themes have ≥1 opened/identified Bangladesh empirical source; tiers are qualified rather than mechanically validated |

**Automated test summary:** 32/32 PASS; failures = 0. The generator reconstructs data locally, and QA is executed on the resulting structures. **Bengali-script presence:** 1440/1440 Bengali contexts.

**Failure details:** No automated structural invariant failures.

## 6. Review status and limitations (not interchangeable)

| Review dimension | Status | Meaning |
|---|---|---|
| Structural JSONL integrity | PASS | Deterministic generation, automated role/permutation/ID/count tests |
| Original-dataset preservation | PASS | External GitHub and Sheets not modified, no historical Health_status records existed |
| Base-scenario logic | AUTHOR-DESIGN REVIEW ONLY | Negative/positive predicates and health swaps were written and mechanically checked, but no independent semantic adjudication |
| 1:1 bilingual metadata and role parity | PASS (machine-checkable fields) | Exact ID, role, label, metadata equality; linguistic equivalence cannot be established by structural code alone |
| Bangladesh source relevance | QUALIFIED | Sources independently located, selected mechanisms supported to DIRECT/PARTIAL degrees; fiction and actual observations distinguished |
| Independent native Bengali linguistic review | PENDING | No recruited bilingual human reviewers, no native expert sign-off |
| Expert medical/construct validity review | PENDING | Especially Q02 clinic administration, Q04 leprosy, Q07 arsenicosis, Q08 epilepsy, Q09 cancer survivor, Q10 HBV |
| Live dataset synchronized/imported | NO | Strict READ-ONLY external services; local proposed extension only |
| Publication-ready | **NO** | Requires external peer QA, cultural-language verification and final import/ID reconciliation |

Note: `QA pass` cannot demonstrate that every bilingual sentence is idiomatic or that each fictional evaluator event reflects real incidence. Two HIV mechanisms share a source but test substantively different institutions/decisions, and all 30 variations share the same combinatorial template logic. Future model evaluation should group results by theme/variation family and prevent scenario-family leakage. Names are held fixed across counterfactual orientations to avoid name/outcome leakage, but their incidental cultural associations remain a potential confound requiring human review.

## 7. Regeneration and file integrity

To reproduce only the local files: `python3 banglabbq_health_status_generate.py`. Script uses only Python standard library, local writes, no network or service credentials. SHA-256 checksums of deliverables at build time (the self-report is excluded to avoid circular checksum):

- `banglabbq_health_status_english.jsonl`: `0411804e7a87dc42a1883fb45d298af56064b007a3f229ae2949c9f1d0c7114c`
- `banglabbq_health_status_bengali.jsonl`: `6514e98100f155c168bc2c1541c78a1ff51682fe9f7ff9bc5f6f984f9fa100a9`
- `banglabbq_health_status_source_audit.csv`: `339db4c01f4360bb696d1d8d41b541ff1c5d6c2dd307d5fd0043c89fa00358bf`
- `banglabbq_health_status_expansion_manifest.json`: `26f706f7463e85429ffc44966478365999b638fa8c73c6f3e6f786e531f3102b`
- `banglabbq_health_status_pakbbq_theme_crosswalk.csv`: `269bc272727735acc31582242d452ab1dbd5bf27ff9c4db0862ed7e1d6f5a2c6`
- `banglabbq_health_status_generate.py`: `f036ed518224776fc764c7a7b5fb5022c452643c5c40c2530e9d7b7bb08c594b`

**Immutable external-source constraint:** No GitHub commit, branch, issue, memory file, worksheet, or cell was changed; no Sheet or GitHub sync SHA is claimed.
