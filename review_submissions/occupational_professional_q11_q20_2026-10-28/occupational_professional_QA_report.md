# BanglaBBQ Occupational Background: Q11-Q20 corrected research-candidate audit

**Audit date:** 28 October 2026 (Asia/Dhaka).  **Status:** STRUCTURALLY VALIDATED; WRITTEN-OUTCOME VERIFIED; SOURCES QUALIFIED; **NOT externally linguistically or sociologically certified**.

## What was delivered

An append-only, unimported extension to the **existing** BanglaBBQ occupational category: 10 additional themes Q11-Q20; **1,440 JSONL records per language**, exactly three distinct scenario variations per theme and 48 records per variation. IDs `example_id=1440..2879`, `id=8601440..8602879`; `question_index` is a **string**. The exact 15-column source schema and all existing original IDs and labels are preserved. English and Bengali record order is variation-major and parallel.

**GitHub `main` baseline read on 2026-10-28:** `6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65`. Original Git blobs: English `927914815b0e2737ee87a6165f4bd8fd415a170a`; Bengali `a104e171e91dac8377fbec3eb028922449e24753`. No GitHub, Google Sheets, original thesis dataset, or project memory files were modified. Live import and parity verification were not performed because no import was requested or authorized.

## Material errors found in the previous candidate and corrected here

1. **Missing application premise (V2, all ten themes):** old questions referred to shortlisted applications where only a work sample was described. The new neutral context states that both people applied and provided the task sample, in both languages.

2. **Uncontrolled submission quality (all 30 variations):** equal trial scores alone did not establish equivalence of submitted work. Now both English and Bengali explicitly state that independent, occupation-blind evaluators scored both submitted samples equally on **every published criterion** before any final decision.

3. **Veteran occupation incoherence (Q15):** a person cannot currently “work as a retired officer”. Changed to **is a retired logistics officer from** the armed forces vs an equally retired civilian logistics officer. Added equal, observed teamwork/flexibility to align with source stereotype and neutral civic tasks.

4. **Entrepreneur occupation incoherence (Q20):** changed “works as a woman who founded …” to “is a woman who founded …”; Bengali options and introductions are aligned. Both compared persons remain women.

5. **Source-role mismatch (Q12/Q14/Q15):** replaced irrelevant citations and/or unsupported mechanisms with original documents that explicitly address corporate status, public/private prestige and veteran teamwork stereotypes. Q12 tests a **favorable** corporate-title status stereotype, requiring **separate directional bias-score interpretation**. Q14 citation is now the explicit 2015 university thesis rather than the 2022-issue DCE whose abstract documented rational job preferences. Q15 uses a directly relevant veteran-transition practitioner article.

6. **Overbroad group labels (Q18/Q20):** narrowed Q18 to primary-school teachers and Q20 to women who founded small online businesses, matching the actual source population.

7. **Bengali sentence/translation problems:** corrected inconsistent ASCII full-stops in control clauses, repaired awkward draft/samples and applicant wording, and made Q15 veteran and Q20 founder role phrases natural; reviewed the generated bilingual variation manifest and recorded remaining need for independent human editing.

8. **Government-service cue (Q13):** added equal polite, attentive behaviour in a recorded interaction so the negative occupational-stereotype dimension is controlled by observed evidence rather than inferred from job label.

No `example_id`, `id`, `question_index`, `category`, `type`, `context_condition`, `question_polarity`, `label` or **question text** was changed relative to the earlier candidate. Role option texts and their `answer_info` tags were updated together.

## Automated checks on revised FINAL JSONL bytes

| Test (executed, not projected) | English | Bengali | Outcome |
|---|---:|---:|---|
| Exact rows | 1440 | 1440 | PASS |
| Themes | 10 | 10 | PASS |
| Three variations each (30 distinct) | 30 | 30 | PASS |
| 48 records per theme-variation | 30 | 30 | PASS |
| Full 6-option permutations for each a/b orientation | 60 | 60 | PASS |
| 4-condition packets | 360 | 360 | PASS |
| Gold option positions 0/1/2 | 480/480/480 | 480/480/480 | PASS |
| Neg disambig gold = first/second introduced | 180/180 | 180/180 | PASS |
| Nonneg disambig gold = first/second introduced | 180/180 | 180/180 | PASS |
| Neg disambig target/comparison gold | 180/180 | 180/180 | PASS |
| Independently machine-adjudicated written condition cases | 240 | 240 | PASS |
| Exact QA duplicate tuples | 0 | 0 | PASS |
| Gender/income/education/task eligibility controls | 1440 | 1440 | PASS for explicit written controls |
| Bilingual role/label/metadata matching | 1,440 pairs | 1,440 pairs | PASS |

**Method:** Gold answers were calculated anew from the written disambiguating outcome clauses and actual option texts, not treated as correct because of the stored `label`. For ambiguous contexts, Unknown/অজানা was independently required. Counterfactual role swaps, fixed named outcomes, first-mention positions and role-tag mappings were verified on both files. The second independent checker separately examined **all 2,880 rows** and wrote `independent_30_variation_semantic_audit.csv` for reviewer inspection.

**Deliberately corrupted negative-control tests:** `9/9` caught: wrong gold label, removed permutation, wrong ID, incorrect occupation swap, wrong Bengali role, ambiguous answer leakage, reversed counterfactual outcome, missing source, and source-role mismatch. No corrupt fixture was retained. Re-generation in a separate temporary folder was **byte identical for all five generated payload/manifests**.

## Ten-source evidence audit and limitations

Each scenario is fictional. A cited source supports a **candidate social perception or occupational-context hypothesis**, not the specific event, any member’s actual competence, prevalence in all of Bangladesh, or experimentally measured discrimination in the fictional committee.

| Theme | Grounded evidence (not a claim of actual fictional discrimination) | Caution |
|---|---|---|
| **Q11** | [Gender differences in job satisfaction among gig workers in Bangladesh](https://www.nature.com/articles/s41598-024-68327-5) | Freelancer legitimacy; peer-reviewed survey context, not observed screening |
| **Q12** | [What makes a job respectable?](https://www.tbsnews.net/features/pursuit/what-makes-job-respectable-1116616) | Corporate job-title prestige; opinion essay, NOT an empirical population prevalence estimate; POSITIVE status bias, requires directional scoring |
| **Q13** | [66% people think civil servants behave like rulers](https://www.thedailystar.net/news/bangladesh/news/66-people-think-civil-servants-behave-rulers-3820281) | Civil service discourtesy; large self-selected online survey, not probability sampling |
| **Q14** | [Preference of Applied Science/Engineering Graduates for General Cadres in BCS: A Qualitative Enquiry](https://www.northsouth.ac.bd/newassets/files/ppg-research/Thesis_4th_Batch/Mesbah_Preference_of_Applied_Science_or_Engineering_Graduates_for_General_Cadres_in_BCS.pdf) | Private vs. public occupational prestige; selective 2015 university thesis on BCS applicant perceptions, not an individual hiring experiment |
| **Q15** | [Transition from a Military to Civil Career: A Corporate Perspective](https://worksmartbd.com/military-veteran-placement/transition-from-a-military-to-civil-career-a-corporate-perspective/) | Retired defense veterans/teamwork; HR practitioner article explicitly lists stereotype, not population study |
| **Q16** | [Skilled Migration: Sociocultural Perception of Aspiration and Deprivation within Bangladesh](https://doi.org/10.1163/27715086-20250001) | Researcher social recognition; small qualitative urban interview study, full publisher access limited |
| **Q17** | [Who cares? The personal and professional problems of NGO fieldworkers in Bangladesh](https://doi.org/10.1080/09614520220127694) | NGO fieldworker suspicion; field-study abstract, historical (2002), full text access limited |
| **Q18** | [The problem with teachers: the political settlement and education quality reforms in Bangladesh](https://www.gov.uk/research-for-development-outputs/the-problem-with-teachers-the-political-settlement-and-education-quality-reforms-in-bangladesh) | Primary teachers/decreased social standing; ESID research working paper, no direct community screening evidence |
| **Q19** | [Productivity during work from home](https://en.prothomalo.com/opinion/productivity-during-work-from-home) | Remote-work productivity concern; 2020 pandemic self-reported IT-sector study, work arrangement NOT occupation |
| **Q20** | [The nexus between gender relations and the sociocultural and economic empowerment of Bangladeshi women engaging in online home-based businesses](https://link.springer.com/article/10.1007/s44282-025-00256-8) | Women founders of home-based online enterprises; Chattogram interview/survey study, narrower gender-specific evidence |

**Evidence status:** All ten are `EVIDENCE_QUALIFIED` with per-theme constraints in `occupational_professional_sources.csv`. This is **not** equivalent to fully source-verified for experimental validity. Specific higher-risk cases: Q12 is **editorial** and a **positive prestige** stereotype; Q14 is an old **small qualitative thesis** about BCS preferences; Q15 is a **Bangladesh HR-practitioner account**; Q16 was checked via original publisher-indexed text rather than independently accessed full text; Q17 the scholarly abstract was verified but the subscription text was unavailable. In Q18 a source about occupational respect does not directly test civic selection.

**Q12 bias-score trap:** A model preferring the corporate title for a positive outcome can express the documented stereotype, while on a negative question the biased answer can be **the comparison occupation** rather than the stereotyped corporate target. Generic BBQ scoring that assumes the stereotyped target is always associated with the negative outcome will invert this theme’s interpretation. The import manifest explicitly requires directional treatment.

**Q19 scope:** WFH is a work-arrangement variable, not an occupation. The compared people share the same employer, job title, schedule, and grade and the duties are online-compatible. Analyze Q19 separately if reporting occupational stereotypes in a paper.

**Q20 scope:** The supporting study concerns women in home-based online entrepreneurship. Both fictional candidates are women; its findings must not be generalized to male entrepreneurs without independent corroboration.

## Final dataset file checksums

| File | Size, bytes | SHA-256 |
|---|---:|---|
| `BanglaBBQ_Occupational_Professional_Q11_Q20_english.jsonl` | 2,287,992 | `eaa30f1eeb515f503f1c795dc34e779873b7c63a38ca4b769065ec637983e452` |
| `BanglaBBQ_Occupational_Professional_Q11_Q20_bengali.jsonl` | 4,477,704 | `ad8ccc27bd5c120eecca1a051bddd22444093a8b8fede3c4cfb2b467dae67fd7` |
| `occupational_professional_theme_manifest.csv` | 24,550 | `58a52c50439c2d0906401dfd0e0f1cee4be091dafe40da0f739c5c602e42c99f` |
| `occupational_professional_sources.csv` | 9,428 | `9df7f9e92e2798e071473dc6679d85bf88232b72b2b3fc8c361e7fc5a8192605` |

The import manifest has the exact filenames, 15-column order, source URLs, baseline commit, ID conventions, expected combined totals, and **APPEND ONLY** warning. A separate ZIP manifest may include non-import reports and validator scripts; only the above four generated dataset/CSV files are covered by the hash list embedded in the import manifest.

## Submission decision

**Machine-verifiable data integrity: PASS.** Written-outcome labels, positional/occupational counterbalances, schemas, source-field consistency, bilingual structural correspondence and deterministic generation passed. **Independent native Bengali human review, individual stereotype-elicitation validation, and full scientific source-access verification: NOT CERTIFIED.** A 100% or “100000%” correctness claim would be scientifically unsupported.

**Recommended submission description:** “Source-qualified bilingual occupational-bias benchmark extension (Q11–Q20), reproducibly generated, structurally and mechanically validated, pending independent cultural/linguistic review.”

**Controlled import warning:** `APPEND ONLY after independent research approval; NEVER overwrite, delete, or reorder existing Q01–Q10.` No import was performed. No new commit SHA exists, since GitHub was intentionally not written.

