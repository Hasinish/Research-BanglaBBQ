# BanglaBBQ Research Logs

Welcome to the **BanglaBBQ Research Logs** directory (`research_logs/`). This directory houses detailed, evidence-backed, reproducible records of every substantial milestone, audit, dataset repair, benchmark expansion, linguistic review, and experimental validation in the BanglaBBQ project.

---

## 1. Role & Relationship to `memory/`

To maintain clarity and separation of concerns across human researchers, AI coding agents (Antigravity, Cursor, Claude Code), and conversational assistants (ChatGPT):

- **`memory/` (High-Level State & Dashboard)**:
  - Houses the authoritative, concise project dashboard (`state.md`), chronological overview (`history.md`), official mission (`purpose.md`), directory map (`index.md`), and synchronization protocol (`README.md`).
  - Intended to be read at the start of every session for immediate orientation.
- **`research_logs/` (Detailed Technical Evidence & Audit Reports)**:
  - Houses deep-dive investigative logs, before/after diffs, exact row ranges, backup links, statistical distributions, linguistic rationales, and test suite execution logs.
  - Every major dataset change or architectural decision must produce a dedicated research log.

---

## 2. Mandatory Research Logging Rules

1. **Standardized Naming Convention**:
   - Every research log file must follow the pattern:  
     `research_logs/YYYY-MM-DD_<topic_in_snake_case>.md`  
     *(Example: `research_logs/2026-10-17_age_q1_context_alignment.md`)*
2. **Template Adherence**:
   - All logs must follow the standard structure defined in [`research_logs/TEMPLATE.md`](TEMPLATE.md).
3. **Empirical Evidence & Zero Fabrication**:
   - Never invent statistics, test results, citations, or commit SHAs.
   - Record exact pre-edit backup URLs or paths, sheet row ranges, and record ID ranges.
4. **Index Maintenance**:
   - Whenever a new research log is created, add an entry to the index table below.
5. **Quality over Quantity**:
   - Clearly document remaining limitations, linguistic nuances, and pending reviews. Never claim a dataset is publication-ready based purely on automated structural validation.

---

## 3. Chronological Index of Research Logs

| **2026-10-19** | [`2026-10-19_educational_background_final_targeted_qa_repair.md`](2026-10-19_educational_background_final_targeted_qa_repair.md) | Educational Background (Themes Q01–Q20) | Final targeted QA repair; resolved confirmed semantic defects: Q17 V1 unentailed commendation, Q16 V2 respect vs pride, Q03 V3 English delivery qualifier, Q15 V1/V2 counterfactual confounders; harmonized competency criteria across Q17 V1 and Q20 V3; calibrated all 20 source evidence tiers (downgraded non-experimental DIRECT claims in Q06, Q07, Q10, Q20; corrected Q19 author attribution to Nakata et al.); upgraded generator-agnostic semantic validator with natural-language predicate entailment; verified 16/16 adversarial regression fixtures (100% rejection rate); synchronized 516 live cells via sparse updates; verified 100% bit-for-bit live parity across all 86,400 data cells (0 mismatches) | `SEMANTIC QA PASSED / ADVERSARIAL FIXTURES VERIFIED (16/16) / 86,400-CELL LIVE PARITY 100% PASS / REVIEW PENDING` |
| **2026-10-19** | [`2026-10-19_educational_background_independent_qa_repair.md`](2026-10-19_educational_background_independent_qa_repair.md) | Educational Background (Themes Q01–Q20) | Final independent QA audit & repair; 12 counterfactual orientation 'b' defects resolved; evaluator mismatches fixed (Q07, Q17); institutional terminology aligned (college -> university in Q16); source citations & dates verified (Q02, Q09, Q15, Q16, Q19, Q20); generator-agnostic semantic QA validator built; 9/9 adversarial regression fixtures verified (100% rejection rate); 6,252 sparse live cell patches applied; 100% bit-for-bit live parity verified across all 86,400 data cells (0 mismatches) | `SEMANTIC QA PASSED / ADVERSARIAL FIXTURES VERIFIED (9/9) / 86,400-CELL LIVE PARITY 100% PASS / REVIEW PENDING` |
| **2026-10-19** | [`2026-10-19_educational_background_repair_and_expansion.md`](2026-10-19_educational_background_repair_and_expansion.md) | Educational Background (Themes Q01–Q20) | Complete repair of 128 legacy records and expansion to 20 themes (V1/V2/V3), 2,880 records/language (5,760 total); 5 legacy defects resolved (32 label reversals, 32 duplicate QA tuples, incomplete permutations, counterfactual inversions, weak evidence); 10/10 offline structural invariants and deep semantic entailment passed; live Google Sheets tabs `BanglaBBQ_ENG_Education` (1544720708) and `BanglaBBQ_BEN_Education` (641606675) created and verified 100% bit-for-bit across all 86,400 data cells | `STRUCTURAL PASS / LIVE REPLICATED / ALL 20 THEMES AUDITED / REVIEW PENDING` |
| **2026-10-19** | [`2026-10-19_gender_q56_final_repair.md`](2026-10-19_gender_q56_final_repair.md) | Gender Identity (Theme Q56) | Final one-pass repair of Theme Q56 (32 records/lang, 192 cells total across Col F, G, M); version="a"/"b" metadata preserved; natural Bangladeshi Bengali syntax without hyphenated suffixes restored; Probation of Offenders Ordinance 1960 Section 5 cited as legal framework; 140,910-cell live parity confirmed | `Q56 APPLIED & VERIFIED / 140,910-CELL LIVE PARITY 100% PASS / ALL 34 THEMES VERIFIED / REVIEW PENDING` |
| **2026-10-19** | [`2026-10-19_gender_q55_approval_and_q56_balanced_proposal.md`](2026-10-19_gender_q55_approval_and_q56_balanced_proposal.md) | Gender Identity (Q55, Q56) | Approved Q55 question-wording & caregiving source update applied (32 records/lang, 128 cells total across Col G & M); sources accurately described as caregiving expectations (not custody outcomes); Q56 previous defect diagnosed and withheld from production; scientifically balanced Section 5 probation proposal staged in review; 140,910-cell live parity confirmed | `Q55 APPLIED & VERIFIED / Q56 BALANCED PROPOSAL STAGED / 140,910-CELL LIVE PARITY PASS` |
| **2026-10-19** | [`2026-10-19_gender_q52_q54_sources_and_q55_q56_proposals.md`](2026-10-19_gender_q52_q54_sources_and_q55_q56_proposals.md) | Gender Identity (Q52–Q56) | Evidence-backed source replacement for Themes Q52–Q54 (136 records/lang, 272 cells in Col M) applied and live-verified; Q55 child-custody caregiving question proposal staged; Q56 Section 5 probation-eligibility scenario proposal staged; 140,910-cell live parity confirmed | `Q52–Q54 SOURCES VERIFIED / Q55–Q56 PROPOSALS STAGED / 140,910-CELL LIVE PARITY PASS` |
| **2026-10-18** | [`2026-10-18_gender_citation_grammar_semantic_refinements.md`](2026-10-18_gender_citation_grammar_semantic_refinements.md) | Gender Identity (Q11, Q52–Q56) | Q54 English grammar applied & verified (32 records); Themes Q52–Q56 designated SOURCE_UNVERIFIED; 200-row citation patch & Q56 redesigns withheld from production; role-entailment validator upgraded; patch conflict loophole closed; 140,910-cell live parity confirmed | `Q54 GRAMMAR APPLIED / Q52-Q56 SOURCE_UNVERIFIED / CITATION PATCH WITHHELD / LIVE PARITY PASS` |
| **2026-10-18** | [`2026-10-18_gender_remaining_issues_audit.md`](2026-10-18_gender_remaining_issues_audit.md) | Gender Identity (Q7–Q58) | Forensic audit of 24 candidate collisions (Q32/Q40/Q43); 8 repeated QA tuples resolved; 34-theme source audit (26 general, 3 partial, 5 Bangladesh citations sourced); 176 Pakistani localization proposals staged; semantic validator & sparse production tooling built | `AUDITED / PROPOSALS STAGED / VALIDATOR ENHANCED / APPROVAL REQUIRED` |
| **2026-10-18** | [`2026-10-18_gender_full_repair.md`](2026-10-18_gender_full_repair.md) | Gender Identity (Q7–Q58) | Complete benchmark repair; 0 English leaks, 0 double possessives, 0 hyphen defects; Q11 role reversal fixed; 12 metadata errors fixed; 33px/96px WRAP/CLIP formatting restored; 140,910 cells live verified; 34-theme source audit | `REPAIRED / FORMATTED / LIVE-PARITY-VERIFIED / LOCALIZATION-PROPOSED` |
| **2026-10-18** | [`2026-10-18_gender_identity_expansion_and_bilingual_qa.md`](2026-10-18_gender_identity_expansion_and_bilingual_qa.md) | Gender Identity (Q7..Q58) | Full 4,696-record bilingual migration; natural Bangladeshi Bengali translation; 140,880 data cells live verified; 100% native production formatting replication; 10/10 offline invariants | `STRUCTURAL PASS / LIVE REPLICATED / REVIEW PENDING` |
| **2026-10-18** | [`2026-10-18_religion_final_qa_and_validation.md`](2026-10-18_religion_final_qa_and_validation.md) | Religion (Q1–Q20) | Comprehensive QA of all 2,880 records across V1/V2/V3; source verification (Q3/Q8–Q10/Q12–Q13 & 14 themes); split safeguards | `VERIFIED COMPLETE (QA)` |
| **2026-10-17** | [`2026-10-17_religion_six_theme_evidence_repairs.md`](2026-10-17_religion_six_theme_evidence_repairs.md) | Religion (Q3, Q8–Q10, Q12–Q13) | Source-aligned bilingual revisions across V1/V2/V3; 864 corrected records/language, 100% production parity; human/source caveats remain | `STRUCTURAL PASS / REVIEW PENDING` |
| **2026-10-17** | [`2026-10-17_religion_source_verification_q3_q8_q9_q10_q12_q13.md`](2026-10-17_religion_source_verification_q3_q8_q9_q10_q12_q13.md) | Religion (Q3, Q8–Q10, Q12–Q13) | Six-theme citation verification; credible alternatives, contradicted/mismatched mechanisms, and source-backed redesign gates, without production data changes | `SOURCE AUDIT COMPLETE / REPAIRS PENDING` |
| **2026-10-17** | [`2026-10-17_religion_v2v3_expansion.md`](2026-10-17_religion_v2v3_expansion.md) | Religion (Q1–Q20) | Bilingual V2/V3 expansion 960 → 2880 records/language; immutable baselines, SHA-pinned shards, Sheets write/read-back and source caveats | `STRUCTURAL PASS / SOURCE REVIEW PENDING` |
| **2026-10-17** | [`2026-10-17_religion_wording_variations_review.md`](2026-10-17_religion_wording_variations_review.md) | Religion (Q1–Q20) | 40 bilingual V2/V3 review candidates in separate Google Sheet; source-sensitive caveats and no production expansion | `REVIEW PROPOSAL` |
| **2026-10-17** | [`2026-10-17_religion_qa_repair.md`](2026-10-17_religion_qa_repair.md) | Religion (Q1–Q20) | QA repairs across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20; source scrutiny; live sheets parity | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_politics_q5_q14_q19_fixes.md`](2026-10-17_politics_q5_q14_q19_fixes.md) | Politics (Q5, Q14, Q19) | Content repairs: Q5 year 2022 qualification, Q14 negative question refinement, Q19 Bengali terminology alignment | `VERIFIED COMPLETE` |
| **2026-10-17** | [`politics_wording_expansion_20261017.md`](politics_wording_expansion_20261017.md) | Politics | Politics expansion from 960 to 2,880 records per language with 40 audited wording variants | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_q1_context_alignment.md`](2026-10-17_age_q1_context_alignment.md) | Age (Q1) | Retrospective audit and context alignment expanding unique contexts from 11 to 16 | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_q9_context_alignment.md`](2026-10-17_age_q9_context_alignment.md) | Age (Q9) | Retrospective audit and alignment of technology stereotypes expanding unique contexts from 60 to 144 | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_q19_semantic_repair.md`](2026-10-17_age_q19_semantic_repair.md) | Age (Q19) | Semantic repair of neighbor substitution for friend/someone else and teen/teenager distinction (120 -> 140 unique contexts) | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md`](2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md) | Age (Q3, Q8, Q10–Q12) | Lexical distinctions (Zoomer vs Gen-Z kid, teen vs teenager, high schooler vs high school student, fights vs confrontations) | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_cultural_localization_audit.md`](2026-10-17_age_cultural_localization_audit.md) | Age (Q13–Q20) | Comprehensive audit of Pakistani cultural/geographic entities in TM records and recommendations for English alignment | `VERIFIED COMPLETE` |

| **2026-10-18** | [`2026-10-18_age_english_localization_semantic_source_audit.md`](2026-10-18_age_english_localization_semantic_source_audit.md) | Age (Q1–Q20) | 868 English context corrections in 8 themes, full 2,920-row bilingual metadata parity, 43,800-cell live checks, 20-theme source audit; Q20 legal confound and Q15/Q18 source mismatches explicitly open | `STRUCTURALLY VALIDATED / SEMANTIC & SOURCE REVIEW PENDING` |
| **2026-10-18** | [`2026-10-18_age_q20_legal_confound_repair.md`](2026-10-18_age_q20_legal_confound_repair.md) | Age (Q20 & Q1–Q20) | Q20 underage-driver legal confound repair (112 records/lang, 15/17 -> 19/20); 100% 43,800-cell Google Sheets live parity; 10/10 invariant pass; Q6 fatigue vs unwillingness nuance and Q15/Q18 source gaps audited | `STRUCTURAL PASS / SOURCE & LINGUISTIC REVIEW PENDING` |


- [2026-10-18 — Gender translation QA checkpoint](2026-10-18_gender_translation_qa_checkpoint.md): Live bilingual screening, confirmed errors, translator-code-only patches, backup, limitations, and outstanding production synchronization.
