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

| Date | Log File | Category | Focus / Scope | Status |
| :--- | :--- | :---: | :--- | :---: |
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

