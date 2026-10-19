# Research Log: BanglaBBQ Educational Background — Final Independent QA Repair and Entailment Hardening

- **Date**: 2026-10-19
- **Author**: Lead NLP QA Researcher & Bilingual Dataset Auditor
- **Status**: `SEMANTIC QA PASSED / ADVERSARIAL FIXTURES VERIFIED (9/9) / 86,400-CELL LIVE SHEETS PARITY VERIFIED (0 MISMATCHES) / EXTERNAL LINGUISTIC & PEER REVIEW PENDING`
- **Scope**: Educational Background Benchmark (Themes Q01–Q20, V1/V2/V3, 2,880 records/language, 5,760 combined records).

---

## 1. Executive Summary

This research log documents the comprehensive, independent QA audit and repair of the 20-theme BanglaBBQ Educational Background benchmark. While the initial expansion achieved structural completeness (2,880 rows per language, 6-way permutations, balanced 960/960/960 labels, and sequential IDs), rigorous independent forensic inspection revealed that 12 templates in counterfactual orientation `b` suffered from education-route and institutional category reversals. Furthermore, evaluator role discrepancies (Q07 V1, Q17 V1), institutional terminology errors ("college" for universities in Q16 V3), and citation/source misattributions (e.g. Q02 date, Q09 date, Q15 date/strength, Q16 publication date, Q19 RCT misinterpretation, Q20 irrelevant National University citation) required systemic upstream correction.

Rather than patching exported JSONLs, all repairs were executed directly in the true upstream source definitions (`scripts/themes_data/part1_themes_1_to_5.py` through `part4_themes_16_to_20.py`, `scripts/build_scenario_templates.py`), regenerated deterministically via `assemble_education_dataset.py`, audited against a generator-agnostic semantic QA validator (`scripts/validate_education_semantics.py`), challenged with 9 adversarial regression fixtures (`scripts/test_education_semantic_fixtures.py`), and synchronized to production Google Sheets via sparse cell updates (`scripts/apply_education_qa_repair_live.py`).

Full 100% bit-for-bit live parity across all 86,400 data cells (43,200 English + 43,200 Bengali) was verified with 0 mismatches against canonical JSONLs.

---

## 2. Pre-Repair Backups and SHA256 Fingerprints

Before applying any modifications, full immutable backups of both live Google Sheets tabs and canonical JSONLs were captured and archived:
- **Backup Directory**: `backups/education_pre_qa_repair_20261019/`
- **Pre-Repair Canonical JSONL Hashes**:
  - English: `33f0f079df3a666146084ca4103606093b0763559846ecdbf69338e5aec3b1f1`
  - Bengali: `a26cf111da28b55a19571d189b58b7fded165fa26b9ee7f97d82edc32f8285fc`
- **Pre-Repair Live Sheets Dump**: `backups/education_pre_qa_repair_20261019/live_sheets_backup.json` (5,762 rows verified).
- **Post-Repair Canonical JSONL Hashes**:
  - English: `82310df3d89d47e6c0632eae6705c2b6a39d328d2b39b982336e53795dd00b9b`
  - Bengali: `73632f77ba16869f78cb31e7004b5a58f120ec7a4ef486d362b30cdc01bc6c60`

---

## 3. Confirmed Counterfactual Defects & Upstream Repairs

A total of 12 templates (144 records per language, 288 records combined) contained contradictory education-route descriptions in orientation `b`. The exact mathematical EID formula is:
- Base: `base = (w - 1) * 960 + (q - 1) * 48 + 24`
- Orientation `b` disambiguated records: `base + 1 + 4*k` and `base + 3 + 4*k` for `k` in 0..5 (12 odd EIDs per template).

### Summary Table of Repaired Templates

| Theme & Variant | Target / Comparison | Affected Disambiguated EIDs (Odd) | Identified Defect | Upstream Repair Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q05 V3** | SSC Vocational vs General SSC | 2137–2159 (12 EIDs) | General SSC student described as vocational track | Evaluator doubts General SSC for lacking hands-on applied community experience; commends SSC Vocational for practical applied training. |
| **Q10 V1** | Private vs Public Polytechnic | 457–479 (12 EIDs) | Public polytechnic accused of purchased commercial grades | Public polytechnic doubted due to large class sizes and overstretched machinery; private polytechnic commended for modern lab facilities. |
| **Q10 V2** | Private vs Public Polytechnic | 1417–1439 (12 EIDs) | Public polytechnic described as receiving commercial training | Public polytechnic doubted for rigid curriculum lacking emerging digital automation; private polytechnic commended for specialized modern instrumentation. |
| **Q12 V1** | Open University vs Campus | 553–575 (12 EIDs) | Campus graduate described as distance education | Campus degree doubted for detached theoretical classroom study; Open University commended for disciplined self-directed work-study balance. |
| **Q12 V2** | Open University vs Campus | 1513–1535 (12 EIDs) | Campus graduate described as flexible credential | Campus graduate doubted for campus complacency; Open University commended for exceptional drive through flexible distance learning while working. |
| **Q12 V3** | Open University vs Campus | 2473–2495 (12 EIDs) | Campus graduate described as unconventional degree | Campus graduate doubted as sheltered from grassroots community realities; Open University affirmed as grounded through accessible community distance education. |
| **Q15 V1** | Less-Known vs Prestigious Uni | 697–719 (12 EIDs) | Prestigious uni described as lacking elite brand | Prestigious uni candidate eliminated due to salary demands and campus entitlement; less-known uni candidate advanced for humility and long-term loyalty. |
| **Q15 V2** | Less-Known vs Prestigious Uni | 1657–1679 (12 EIDs) | Prestigious uni degree called obscure | Prestigious uni credentials discounted due to flight risk and theoretical ego; less-known uni credentials endorsed for grounded work ethic and hunger to succeed. |
| **Q16 V1** | Lesser-Known vs Top-Tier Private Uni | 745–767 (12 EIDs) | Top-tier private uni called low-status | Top-tier private uni criticized for exorbitant tuition fees and elitism; lesser-known private uni congratulated for affordable, practical education. |
| **Q16 V3** | Lesser-Known vs Top-Tier Private Uni | 2665–2687 (12 EIDs) | Universities called "college"; top-tier called uncompetitive | All instances of "college" eliminated; top-tier judged as entitled and detached; lesser-known commended for perseverance and community dedication. |
| **Q18 V1** | Private vs Govt Secondary School | 841–863 (12 EIDs) | Government school called commercialized | Government school criticized for overcrowded classrooms and bureaucratic neglect; private school admired for attentive modern student care. |
| **Q19 V2** | RPL vs Institutional TVET | 1849–1871 (12 EIDs) | Institutional TVET called shortcut credential | Institutional TVET doubted for lack of verified field maintenance hours; RPL trusted for proven hands-on field competency assessed under NTVQF. |

---

## 4. High-Risk Scenarios & Semantic Alignment Audits

1. **Q04 V2 (Private vs Public University)**:
   - *Audit*: Orientation `b` previously alleged public university degrees were "commercial inflated degrees".
   - *Repair*: Revised to evaluator skepticism over outdated instructional methodologies and session delays at standalone public universities, contrasted with modern industry-aligned coursework at private universities.
2. **Q06 V3 (HSC Vocational vs General HSC)**:
   - *Audit*: Asking theoretical questions in an interview did not constitute clear differential or negative treatment.
   - *Repair*: Context sharpened to the engineering admissions panel expressing overt skepticism and prejudice regarding whether vocational students possess academic stamina for higher education.
3. **Q07 V1 (HSC Business Management vs General Business Studies)**:
   - *Audit*: Context named "senior corporate executives" while questions referenced "club seniors".
   - *Repair*: Unified evaluator to "senior club executives" (`ক্লাবের জ্যেষ্ঠ নেতৃবৃন্দ`) in both context and questions across English and Bengali.
4. **Q08 V2 & V3 (Polytechnic Diploma vs General Academic)**:
   - *Audit*: Verified that comparison tasks represent roles both are qualified to undertake (supervisory and coordination posts), distinguishing practical shop-floor leadership from administrative coordination without statutory engineering licensing conflation.
5. **Q09 V1 & V2 (Diploma Engineer vs BSc Engineer)**:
   - *Audit*: Contexts clarified to focus on technical estimation, drafting review, and project coordination disputes rather than implying statutory equivalence for gazetted engineering posts.
6. **Q17 V1 (NCTB English Version vs NCTB Bangla Version)**:
   - *Audit*: Context named "club moderator" while question named "club advisor".
   - *Repair*: Unified evaluator to "club moderator" (`ক্লাব মডারেটর`) across contexts and questions in both languages. Maintained strict distinction between NCTB English Version and Cambridge/Edexcel English-medium schooling.
7. **Q20 V1–V3 (Humanities/Social Sciences vs STEM)**:
   - *Audit*: Evaluated candidates on shared, role-relevant general competencies (management trainee shortlisting, logistics workflow case studies, banking officer aptitude) rather than specialized technical preparation. Replaced irrelevant National University employment source with authentic BIDS empirical research on graduate discipline disadvantage.

---

## 5. Comprehensive 20-Theme Source Re-Audit Matrix

Every citation was re-verified against official publishers, institutional repositories, and primary publications. Evidence classifications were calibrated into distinct tiers (`DIRECT`, `PARTIAL / CONTEXTUAL`, `CONTEXTUAL`, `PARTIAL / QUALITATIVE`, `EXPLORATORY / QUALITATIVE`):

| Theme ID | Title | Primary Source Citation & DOI/URL | Evidence Tier | Key Findings & Verified Boundaries |
| :---: | :--- | :--- | :---: | :--- |
| **Q01** | Alia Madrasa vs General School | Dhaka Tribune / Asadullah et al. (2023), [Link](https://www.dhakatribune.com/opinion/op-ed/322441/no-faith-in-the-labour-market) | `DIRECT` | Randomized CV audit of Dhaka University graduates; 40%–96% callback penalty for madrasa backgrounds at initial CV screening stage. |
| **Q02** | NU College vs Standalone Public Uni | The Daily Star (Dec 2025 BIDS Study), [Link](https://www.thedailystar.net/business/news/employers-less-interested-hiring-national-university-graduates-4053516) | `PARTIAL / CONTEXTUAL` | BIDS tracer study documents employer reluctance and lower absorption rates for NU graduates in corporate roles. |
| **Q03** | Bangla-Medium vs English-Medium | The Business Standard (2023), [Link](https://www.tbsnews.net/features/pursuit/english-vs-bangla-medium-how-does-it-impact-your-career-588550) | `PARTIAL / CONTEXTUAL` | Qualitative investigative feature detailing employer perceptions favoring English-medium fluency alongside recruiter counter-arguments. |
| **Q04** | Private vs Standalone Public Uni | Hosain et al. (2021), DOI: 10.1108/PRR-01-2021-0005 | `PARTIAL / CONTEXTUAL` | Employer survey on private university graduate employability; documents concerns over grading standards and soft skills. |
| **Q05** | SSC Vocational vs General SSC | BRAC Study / TBS (2020), [Link](https://www.tbsnews.net/bangladesh/education/bangladeshis-consider-technical-vocational-education-inferior-163555) | `DIRECT` | Empirical study on TVET youth perceptions documenting pervasive societal stigma treating TVET as inferior. |
| **Q06** | HSC Vocational vs General HSC | Kabir & Ahmed (2024), DOI: 10.1080/14480220.2024.2332345 | `DIRECT` | Documents institutional elitism and peer barriers faced by vocational students seeking tertiary higher education. |
| **Q07** | HSC BM vs General Business Studies | Kabir & Ahmed (2024), DOI: 10.1080/14480220.2024.2332345 | `DIRECT` | Analyzes structural stigma viewing BTEB Business Management as a less demanding alternative to general commerce. |
| **Q08** | Polytechnic vs General Academic | World Bank Report AUS0000063 (2018), [Link](https://documents1.worldbank.org/curated/en/718501528118077327/pdf/AUS0000063-REVISED-FinalReportEmployabilityofpostsecondaryeducationinBangladeshJun.pdf) | `PARTIAL / CONTEXTUAL` | Labor-market tracer study documenting barriers and stereotyping of polytechnic graduates in supervisory career tracks. |
| **Q09** | Diploma vs BSc Engineer | TBS (Published 28 Aug 2025), [Link](https://www.tbsnews.net/bangladesh/bsc-vs-diploma-engineers-why-conflict-and-what-they-demand-1222581) | `DIRECT` | Documents professional hierarchy, status tensions, and workplace demarcation disputes between BSc and diploma engineers. |
| **Q10** | Public vs Private Polytechnic | World Bank Report AUS0000063 (2018), [Link](https://documents1.worldbank.org/curated/en/718501528118077327/pdf/AUS0000063-REVISED-FinalReportEmployabilityofpostsecondaryeducationinBangladeshJun.pdf) | `PARTIAL / CONTEXTUAL` | Highlights quality variation and employer skepticism regarding private polytechnic training infrastructure. |
| **Q11** | Govt vs Non-Govt NU College | College Education Development Project (CEDP, MoE / World Bank), [Link](https://cedp.gov.bd/about-the-project/) | `CONTEXTUAL` | Documents governance and quality improvement challenges in non-government colleges under the NU system. |
| **Q12** | BOU vs Conventional Campus | Aktaruzzaman & Plunkett (2017), DOI: 10.17718/tojde.340370 | `PARTIAL / CONTEXTUAL` | Empirical study on institutional and community perceptions viewing BOU distance education as less prestigious. |
| **Q13** | Science vs Humanities at School | The Daily Star (2017), [Link](https://www.thedailystar.net/shout/cover-story/the-systematic-oppression-arts-commerce-schools-1468609) | `PARTIAL / QUALITATIVE` | Qualitative documentation of familial and institutional prejudice treating Humanities students as academically weak. |
| **Q14** | Science vs Business Studies School | The Daily Star (2017), [Link](https://www.thedailystar.net/shout/cover-story/the-systematic-oppression-arts-commerce-schools-1468609) | `PARTIAL / QUALITATIVE` | Details school-level stigma treating Business Studies as a secondary fallback track for average performers. |
| **Q15** | Prestigious vs Less-Known Uni | TBS (Published 2 July 2025), [Link](https://www.tbsnews.net/features/pursuit/prestige-trap-how-institutional-bias-distorts-job-markets-1179106) | `EXPLORATORY / QUALITATIVE` | Investigative inquiry across 10 MNCs and 14 local firms illustrating institutional brand gatekeeping in recruitment. |
| **Q16** | Recognized vs Lesser Private Uni | BRAC University (Published 13 May 2016), [Link](https://www.bracu.ac.bd/news/research-reveals-4-essential-factors-affecting-bangladeshi-students%E2%80%99-selection-private) | `PARTIAL / CONTEXTUAL` | Empirical survey of 317 students identifying institutional reputation as a primary driver of private university choice. |
| **Q17** | NCTB English vs Bangla Version | NCTB Official Curriculum Guidelines, [Link](https://nctb.gov.bd/) | `CONTEXTUAL` | Establishes curriculum and textbook equivalence across Bangla and English Version streams under national boards. |
| **Q18** | Govt vs Private Secondary School | Chowdhury & Synthia (2021), DOI: 10.1108/IJEM-07-2019-0254 | `CONTEXTUAL` | Quantitative comparative analysis of parental school choice determinants and institutional reputation. |
| **Q19** | RPL vs Institutional TVET | Sharma et al. / World Bank (2021), DOI: 10.1596/1813-9450-9644 | `PARTIAL / CONTEXTUAL` | Randomized impact evaluation of RPL in Bangladesh; confirms positive wage effects while noting non-institutional transition skepticism. |
| **Q20** | University Humanities vs STEM | BIDS / The Financial Express (2019), [Link](https://thefinancialexpress.com.bd/education/graduates-of-non-science-face-higher-disadvantage-in-job-mkt-bids-study-1575865225) | `DIRECT` | BIDS empirical study demonstrating significant labor-market absorption and wage disadvantages for non-science graduates. |

---

## 6. Independent Semantic QA & Adversarial Regression Test Suite

An independent, generator-agnostic semantic QA validator was authored in `scripts/validate_education_semantics.py` and evaluated via `scripts/test_education_semantic_fixtures.py`:

### Adversarial Regression Fixture Results

1. **Fixture 1 (Q12 V1 b Distance Contradiction)**: `REJECTED` -> `Q12 Violation: Conventional campus graduate falsely attributed to distance education`.
2. **Fixture 2 (Q15 V1 b Elite Brand Contradiction)**: `REJECTED` -> `Q15 Violation: Prestigious university graduate falsely described as lacking elite brand`.
3. **Fixture 3 (Q10 V2 Commercial Polytechnic Reversal)**: `REJECTED` -> `Q10 Violation: Public polytechnic falsely described as commercial`.
4. **Fixture 4 (Q05 V3 Vocational Track Attribution)**: `REJECTED` -> `Q05 Violation: General SSC student falsely described with vocational track`.
5. **Fixture 5 (Wrong Disambiguated Gold Label)**: `REJECTED` -> `Cross-lingual role mismatch & Entailment role inversion`.
6. **Fixture 6 (Ambiguous Context Outcome Leakage)**: `REJECTED` -> `Ambiguous context contains outcome leak pattern '\brejects?\b'`.
7. **Fixture 7 (English/Bengali Role Inversion)**: `REJECTED` -> `Cross-lingual role mismatch: ENG='madrasa_grad' vs BEN='general_grad'`.
8. **Fixture 8 (Evaluator Role Mismatch)**: `REJECTED` -> `Q17 Evaluator Mismatch: Context mentions club moderator but question mentions club advisor`.
9. **Fixture 9 (Irrelevant Source Attribution)**: `REJECTED` -> `Theme Q20 still uses obsolete National University employability source`.

**Fixture Suite Verdict**: `9/9 PASSED (100% REJECTION RATE)`.

### Clean Benchmark Validation
- Structural Invariants (`validate_education_dataset.py`): `10/10 INVARIANTS PASSED 100%`.
- Deep Semantic QA (`validate_education_semantics.py`): `ALL CHECKS PASSED 100% CLEAN (0 ERRORS)`.

---

## 7. Exact 1-to-1 Legacy Row Lineage Mapping

Every single historical record (legacy EIDs 0–127) was individually mapped to its exact corresponding improved record in modern V1:
- **Offset Transformation Formula**: For any theme `q` in 1..4:
  `exact_improved_eid = (q - 1) * 48 + LEGACY_TO_MODERN_OFFSET[offset]`
  where `offset = legacy_eid % 32`.
- **Mapping Verification**: Confirmed in `BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`. All 128 rows hold status `EXACT_1_TO_1_ROW_MAPPED` with full defect diagnosis and lineage rationale.

---

## 8. Google Sheets Synchronization & 100% Bit-for-Bit Live Parity

Using sparse writes, only modified cells in columns F (`context`), G (`question`), and M (`additional_metadata`) were patched to preserve existing sheet styling:
- **`BanglaBBQ_ENG_Education` (sheetId: 1544720708)**: 3,096 cells patched.
- **`BanglaBBQ_BEN_Education` (sheetId: 641606675)**: 3,156 cells patched.
- **Diff Manifest**: Detailed before/after diff manifest written to `BanglaBBQ_EducationalBackground/qa_repair_diff_manifest.json` (6,252 total cell diffs documented).
- **Mandatory Live Readback Verification**:
  - `BanglaBBQ_ENG_Education`: 2,881 rows, 43,200 data cells -> **0 mismatches (100% parity)**.
  - `BanglaBBQ_BEN_Education`: 2,881 rows, 43,200 data cells -> **0 mismatches (100% parity)**.
  - Total Verified Live Cells: **86,400 data cells with 0 mismatches**.

---

## 9. Limitations & Explicit Remaining Review Needs

While the dataset is structurally verified, semantically sound, and synchronized to production sheets, scientific integrity demands that we explicitly document remaining boundaries:
1. **Bengali Colloquial Nuance Sign-off**: Bengali translations have been audited against native grammatical and institutional conventions, but formal independent human qualitative review by an external Bangladeshi linguist remains pending prior to publication.
2. **Contextual Evidence Categories**: Themes Q02, Q03, Q04, Q08, Q10, Q11, Q12, Q13, Q14, Q16, Q17, Q18, and Q19 rely on contextual labor-market surveys, institutional reports, or qualitative investigative studies. They do not constitute randomized matched-CV audit experiments (which exists primarily for Q01 Alia Madrasa).
3. **Legal vs Social Demarcations**: Polytechnic diploma holders (Q08, Q09) and RPL certificate holders (Q19) operate within specific statutory and licensing frameworks under BTEB and BNQF. Scenarios model social and employer perceptions without implying statutory or licensure equivalence.
