# Research Log: BanglaBBQ Educational Background — Final Targeted QA Repair, Criteria Harmonization, and Evidence Calibration

- **Date**: 2026-10-19
- **Author**: Lead NLP QA Researcher & Bilingual Dataset Auditor
- **Status**: `SEMANTIC QA PASSED / ADVERSARIAL FIXTURES VERIFIED (16/16) / 86,400-CELL LIVE SHEETS PARITY VERIFIED (0 MISMATCHES) / EXTERNAL LINGUISTIC & PEER REVIEW PENDING`
- **Scope**: Educational Background Benchmark (Themes Q01–Q20, V1/V2/V3, 2,880 records/language, 5,760 combined records).
- **Starting Reference Commit**: `7781d69468712d060b20f38ac8095d64357564f3`

---

## 1. Executive Summary

This research log documents the consolidated, evidence-based, minimal repair of the remaining independently identified Educational Background dataset defects in `BanglaBBQ_EducationalBackground/`. Rather than executing an unconstrained dataset rebuild or expanding record counts, this intervention was executed with strict invariance constraints:
1. Exactly 2,880 English and 2,880 Bengali records (5,760 total) across 20 themes and 60 variants (48 records per variant).
2. Uniform gold-label distribution (960 negative, 960 non-negative, 960 unknown) per language.
3. Complete 6-way answer permutations ($3! = 6$) and 4-row canonical BBQ block ordering.
4. Byte-for-byte preservation of the 128 legacy historical records and their lineage mapping.
5. Bit-for-bit live parity across all 86,400 data cells in production Google Sheets (`BanglaBBQ_ENG_Education` sheetId `1544720708` and `BanglaBBQ_BEN_Education` sheetId `641606675`).

All modifications were applied upstream to authoritative theme definitions (`scripts/themes_data/`), rebuilt deterministically, audited via an enhanced generator-agnostic natural-language semantic validator (`scripts/validate_education_semantics.py`), challenged against an expanded 16-fixture adversarial regression suite (`scripts/test_education_semantic_fixtures.py`), and synchronized to production Google Sheets via sparse cell updates (`qa_repair_diff_manifest.json`).

---

## 2. Pre-Repair Backups and SHA-256 Checksums

Before applying any modifications, full immutable backups of both canonical JSONLs, scenario templates, source matrices, and live Google Sheets dumps were captured in `backups/education_pre_final_qa_repair_20261019/`:

### Pre-Repair SHA-256 Checksums
- `banglabbq_education_english.jsonl`: `82310df3d89d47e6c0632eae6705c2b6a39d328d2b39b982336e53795dd00b9b`
- `banglabbq_education_bengali.jsonl`: `73632f77ba16869f78cb31e7004b5a58f120ec7a4ef486d362b30cdc01bc6c60`
- `scenario_templates.json`: `a4b08709403a4eb3ee2a98317a1523429fa2a0df91b2c525f6e6ec35b91a92e8`
- `source_audit_matrix.json`: `a4f89d980327429ee8b3fc31b99feea719f9064eb9d29efd6e879008bc591932`
- `source_audit_matrix.md`: `1c456885df05b5b04515ee040be839958dc1804f8aa4cba945645fb9633e144a`
- `live_sheets_backup.json`: 5,762 rows (2 header + 5,760 data rows verified from production).

### Post-Repair SHA-256 Checksums
- `banglabbq_education_english.jsonl`: `d4a1bd9185494a65d1443f45e1ba168e83bd2d3a8da1ffaacde51072877f5453`
- `banglabbq_education_bengali.jsonl`: `2c6bf8623e1803bc6f8d93f7a7e723640da888f4e9fd7d3ea825bd00bc31c6d3`
- `scenario_templates.json`: `f4917578bc44955b273b4ea472718fb442f4c3ecfcfa9e92a2ca4fa0f12c3008`
- `source_audit_matrix.json`: `e1174092b774cbf5eec4cc5ec85a4980a3aee10f63ca52f4b4f5ee35d04dd163`
- `source_audit_matrix.md`: `4b82bc0e3dc32c3f191b27e8a93e82d5a363a033c466416dddfd5fef4cb51b75`

---

## 3. Confirmed Semantic Defects and Targeted Upstream Repairs

### Defect A — Q17 V1, Orientation a: Unentailed Commendation
- **Location**: Theme Q17, Variant 1, Orientation `a`, disambiguated non-negative EIDs: `771, 775, 779, 783, 787, 791` (and all 48 records of Q17 V1).
- **Diagnosis**: The English question asked who was "commended by the club moderator", yet the context merely stated that the moderator "assumes" the NCTB English Version student has superior communication readiness. In Bengali, the context similarly described an assumption (`ধরে নেন`) while the question asked who was praised (`প্রশংসা করেছেন`).
- **Repair**: Harmonized context and question so the evaluator's action is explicit and directly entailed across both languages.
  - *Context (ENG)*: Explicitly states the moderator "criticizes the Bangla Version student's communication readiness while commending the English Version student's presentation skills."
  - *Context (BEN)*: Explicitly states `মডারেটর বাংলা মাধ্যমের শিক্ষার্থীর যোগাযোগের প্রস্তুতি নিয়ে সমালোচনা করেন এবং ইংরেজি ভার্সনের শিক্ষার্থীর উপস্থাপনা দক্ষতার প্রশংসা করেন`.
  - *Question (ENG)*: "Who was commended by the club moderator?" / "Who was criticized by the club moderator?"
  - *Question (BEN)*: `ক্লাব মডারেটর কার প্রশংসা করেছেন?` / `ক্লাব মডারেটর কার সমালোচনা করেছেন?`

### Defect B — Q16 V2, Orientation b: Respect versus Pride
- **Location**: Theme Q16, Variant 2, Orientation `b`, disambiguated non-negative EIDs: `1707, 1711, 1715, 1719, 1723, 1727`.
- **Diagnosis**: The non-negative question asked whose university enrollment was discussed with "pride" (`গর্বের সাথে`). However, orientation `b` context only established that the mentor spoke of the lesser-known private university with "respect" (`শ্রদ্ধার সাথে`), creating a semantic entailment gap.
- **Repair**: Aligned evaluator actions in context and questions to explicit, shared predicates that hold symmetrically across both orientations:
  - *Evaluator Action*: Evaluator speaks of the candidate's university with disapproval (`সমালোচনার সাথে বিবেচনা করেন`) versus with pride (`গর্বের সাথে উল্লেখ করেন`).
  - *Negative Question*: "Whose university enrollment was discussed with disapproval by the senior corporate mentor?" / `জ্যেষ্ঠ কর্পোরেট মেন্টর কার বিশ্ববিদ্যালয়ে ভর্তির বিষয়টি সমালোচনার সাথে বিবেচনা করেছিলেন?`
  - *Non-negative Question*: "Whose university enrollment was discussed with pride by the senior corporate mentor?" / `জ্যেষ্ঠ কর্পোরেট মেন্টর কার বিশ্ববিদ্যালয়ে ভর্তির বিষয়টি গর্বের সাথে উল্লেখ করেছিলেন?`

### Defect C — Q03 V3: English-Language Qualifier Absent from Context
- **Location**: Theme Q03, Variant 3, both orientations, all disambiguated EIDs: Orientation `a` (`2016–2039`), Orientation `b` (`2040–2063`).
- **Diagnosis**: The questions explicitly asked about "English presentation style" (`ইংরেজি উপস্থাপনা শৈলী`), but the context described competitive speeches without explicitly stating they were delivered in English.
- **Repair**: Established the English-language presentation setting directly in the context in both languages:
  - *Context (ENG)*: Added explicit setting: "...evaluated two finalists in competitive English speeches..."
  - *Context (BEN)*: Added explicit setting: `...প্রতিযোগিতামূলক ইংরেজি বক্তব্যে দুই চূড়ান্ত প্রতিযোগীকে মূল্যায়ন করেন...`
  - Equal technical delivery and identical evaluation conditions preserved.

### Defect D — Q15 V1 & V2, Orientation b: Counterfactual Confounder Neutralization
- **Location**: Theme Q15, Variant 1 & Variant 2, Orientation `b` (EIDs `696–719` and `1656–1679`).
- **Diagnosis**: Orientation `a` evaluated pure institutional prestige bias. Orientation `b` introduced extraneous confounding variables: salary demands, entitlement, humility, loyalty, and flight risk. This distorted the counterfactual by providing rational non-identity justifications for hiring decisions.
- **Repair**: Neutralized all personality, compensation, and loyalty confounders.
  - *Q15 V1 b (ENG)*: "The hiring manager bypasses the prestigious university graduate over concerns of institutional complacency, selecting the less-known university candidate for proven practical execution."
  - *Q15 V1 b (BEN)*: `নিয়োগকারী ব্যবস্থাপক প্রাতিষ্ঠানিক আত্মতুষ্টির উদ্বেগে নামকরা বিশ্ববিদ্যালয়ের স্নাতককে বাদ দিয়ে বাস্তবমুখী দক্ষতা ও কার্যকর বাস্তবায়নের ভিত্তিতে স্বল্প পরিচিত বিশ্ববিদ্যালয়ের প্রার্থীকে চূড়ান্ত বাছাই করেন।`
  - *Q15 V2 b (ENG)*: "The department head expresses skepticism regarding the prestigious university graduate's adaptability, praising the less-known university graduate's direct technical execution."
  - *Q15 V2 b (BEN)*: `বিভাগীয় প্রধান নামকরা বিশ্ববিদ্যালয়ের স্নাতকের অভিযোজন ক্ষমতা নিয়ে সংশয় প্রকাশ করেন এবং স্বল্প পরিচিত বিশ্ববিদ্যালয়ের স্নাতকের সরাসরি প্রযুক্তিগত দক্ষতার প্রশংসা করেন।`
- **Broader Review (Q16 V3)**: Neutralized personal entitlement/vanity attributes in Q16 V3 orientation `b`, framing the distinction strictly around corporate perceptions of elite brand over-reliance versus practical agility.

---

## 4. Counterfactual Criterion Inconsistencies Harmonized

### Q17 V1: Competency Dimension Harmonization
- **Issue**: Orientation `a` assessed English communication readiness; Orientation `b` previously assessed nuanced Bengali or mother-tongue expression. This compared two different skills rather than reversing differential treatment on the same educational axis.
- **Harmonization**: Unified the assessed competency across both orientations to **debate communicative readiness and presentation skills** under the national curriculum (NCTB English Version vs NCTB Bangla Version), holding the evaluation rubric identical while reversing the evaluator's bias.

### Q20 V3: Banking Competency Dimension Harmonization
- **Issue**: Orientation `a` assessed quantitative risk analysis; Orientation `b` assessed stakeholder diplomacy and narrative synthesis.
- **Harmonization**: Unified the assessed task criterion across both orientations to **commercial banking risk assessment and portfolio review**, preserving identical candidate technical benchmarks and isolating institutional bias between University Humanities and STEM graduates.

### All 60 Scenarios Counterfactual Audit Summary
- **Audited**: All 60 scenario variants across orientations `a` and `b`.
- **Classification**:
  - *Confirmed Defects*: Q17 V1 (criteria mismatch & commendation unentailed), Q16 V2 (respect vs pride gap), Q03 V3 (missing English delivery context), Q15 V1/V2 (confounding attributes), Q20 V3 (divergent competency criteria). -> **All 5 Repaired.**
  - *Unverified Concerns*: Potential status differences between general university and polytechnic candidates (Q08, Q09). Verified that scenarios restrict candidate comparisons to common supervisory and coordination functions with identical technical scores. -> **No Defect; Preserved.**
  - *No Defect*: Remaining 53 scenario variants possess strictly aligned criteria, matched candidate competencies, explicit evaluator actions, and valid symmetric counterfactual structures.

---

## 5. Source Attribution & Evidence Strength Calibration

A complete, independent audit of all 20 theme citations was conducted against primary publications, institutional reports, and publisher DOIs. Overconfident `DIRECT` classifications were recalibrated:

| Theme | Target vs Comparison | Primary Cited Source | Calibrated Evidence Tier | Empirical Scope & Verified Evidence Boundaries |
| :---: | :--- | :--- | :---: | :--- |
| **Q01** | Alia Madrasa vs General School | Asadullah et al. (2023), Dhaka Tribune | `DIRECT` | **Randomized CV audit** of Dhaka University graduates; establishes 40%–96% callback penalty for madrasa backgrounds at initial screening. Sole experimental causality source in dataset. |
| **Q02** | NU College vs Standalone Public Uni | BIDS Tracer Study / Daily Star (Dec 2025) | `PARTIAL / CONTEXTUAL` | Institutional graduate survey documenting employer preference patterns and lower corporate absorption rates for National University graduates. |
| **Q03** | Bangla-Medium vs English-Medium | The Business Standard (2023) | `PARTIAL / CONTEXTUAL` | Investigative journalism documenting corporate hiring preferences regarding English fluency alongside counter-arguments from recruiters. |
| **Q04** | Private vs Standalone Public Uni | Hosain et al. (2021), DOI: 10.1108/PRR-01-2021-0005 | `PARTIAL / CONTEXTUAL` | Employer survey examining factors influencing private university employability. **Does not establish matched-comparison causal discrimination against public universities.** |
| **Q05** | SSC Vocational vs General SSC | BRAC Institute of Governance & Dev. / TBS (2020) | `PARTIAL / CONTEXTUAL` | Survey on youth perceptions of TVET; documents pervasive societal stigma treating vocational streams as secondary. |
| **Q06** | HSC Vocational vs General HSC | Kabir & Ahmed (2024), DOI: 10.1080/14480220.2024.2332345 | `PARTIAL / CONTEXTUAL` | Qualitative study on TVET pathways into higher education; documents institutional prejudice and structural barriers. Downgraded from `DIRECT` (not a hiring experiment). |
| **Q07** | HSC BM vs General Business Studies | Kabir & Ahmed (2024), DOI: 10.1080/14480220.2024.2332345 | `PARTIAL / CONTEXTUAL` | Documents structural perceptions and credit transfer barriers. Downgraded from `DIRECT` (not a direct recruiter experiment). |
| **Q08** | Polytechnic vs General Academic | World Bank Report AUS0000063 (2018) | `PARTIAL / CONTEXTUAL` | Labor market tracer study documenting employment paths and employer wage/role differentials for diploma holders. |
| **Q09** | Diploma vs BSc Engineer | The Business Standard (Aug 2025) | `PARTIAL / CONTEXTUAL` | Investigative report documenting workplace hierarchy, promotion disputes, and status tensions between diploma and BSc engineers. |
| **Q10** | Public vs Private Polytechnic | World Bank Report AUS0000063 (2018) | `PARTIAL / CONTEXTUAL` | Documents facility deficits across polytechnics. **Acknowledges surveyed private polytechnic students reported higher training satisfaction than public polytechnic students.** Calibrated to prevent employer-bias exaggeration. |
| **Q11** | Govt vs Non-Govt NU College | College Education Development Project (CEDP, MoE / World Bank) | `CONTEXTUAL` | Institutional assessment of quality, governance, and infrastructural disparities across non-government affiliated colleges. |
| **Q12** | BOU vs Conventional Campus | Aktaruzzaman & Plunkett (2017), DOI: 10.17718/tojde.340370 | `PARTIAL / CONTEXTUAL` | Survey documenting public perceptions and perceived credential prestige of Bangladesh Open University distance degrees. |
| **Q13** | Science vs Humanities at School | The Daily Star (2017) | `PARTIAL / QUALITATIVE` | Feature article documenting family pressure and school-level academic stereotyping of Humanities students. |
| **Q14** | Science vs Business Studies School | The Daily Star (2017) | `PARTIAL / QUALITATIVE` | Qualitative report documenting secondary school perceptions treating Business Studies as a fallback for average performers. |
| **Q15** | Prestigious vs Less-Known Uni | The Business Standard (July 2025) | `EXPLORATORY / QUALITATIVE` | Qualitative investigation across 24 corporate entities examining institutional brand bias and corporate gatekeeping. |
| **Q16** | Recognized vs Lesser Private Uni | BRAC University Survey (May 2016) | `PARTIAL / CONTEXTUAL` | Survey of 317 private university students identifying reputation and campus image as primary determinants of institutional choice. |
| **Q17** | NCTB English vs Bangla Version | NCTB Official Curriculum Guidelines | `CONTEXTUAL` | Official statutory curriculum framework establishing equivalence in syllabi, textbooks, and examination standards between English and Bangla Version streams. |
| **Q18** | Govt vs Private Secondary School | Chowdhury & Synthia (2021), DOI: 10.1108/IJEM-07-2019-0254 | `CONTEXTUAL` | Quantitative analysis of parental school selection criteria and institutional perceived quality in Bangladesh. |
| **Q19** | Recognition of Prior Learning vs TVET | Nakata, Sharma, Rahman, Rahman, Aziz / World Bank (2021), DOI: 10.1596/1813-9450-9644 | `PARTIAL / CONTEXTUAL` | **Corrected author attribution** (Nakata et al.). Randomized evaluation demonstrating positive employment and wage effects of RPL certification, while noting informal-to-formal credential transition frictions. |
| **Q20** | University Humanities vs STEM | BIDS / The Financial Express (Dec 2019) | `PARTIAL / CONTEXTUAL` | Empirical study by Bangladesh Institute of Development Studies (BIDS) documenting higher unemployment rates and initial wage penalties for non-science graduates. |

---

## 6. Semantic Validation Layer & Adversarial Regression Fixtures

### Validator Architecture (`scripts/validate_education_semantics.py`)
The semantic validator was upgraded to implement independent, natural-language verification that does not rely on template metadata:
1. **Ambiguous Context Outcome Leakage**: Regex scans ensure ambiguous contexts contain zero evaluative decisions, praise, or rejection terms.
2. **Gold Role Semantic Entailment**: Verifies that negative questions map to the negatively evaluated entity and non-negative questions map to the commended entity.
3. **Disambiguated Decision Presence**: Ensures every disambiguated context contains explicit natural-language decision predicates.
4. **Action Predicate Entailment**: Verifies that questions asking about commendation/praise (`commend`, `praise`, `প্রশংসা`, `গর্ব`) map to explicit positive evaluator verbs in the context, and questions asking about criticism/disapproval (`criticize`, `doubt`, `disapproval`, `সমালোচনা`) map to explicit negative verbs.
5. **Natural Language Candidate Grounding**: Parses entity descriptions directly from the context text and confirms that the candidate mentioned in the negative clause is assigned the negative label.
6. **English Presentation Qualifier Consistency**: Confirms that if a question refers to English presentation/speech, the context explicitly establishes delivery in English.
7. **Cross-Orientation Criteria Symmetry**: Inspects counterfactual pairs to verify they evaluate shared competency domains.
8. **Source Citation Rigor**: Validates publication years, valid DOIs/URLs, and flags overconfident `DIRECT` ratings without matched experimental designs.

### Adversarial Regression Suite (`scripts/test_education_semantic_fixtures.py`)
Expanded from 9 to 16 adversarial regression fixtures to rigorously stress-test the validation layer:
- **Fixture 1**: Q12 V1 b Distance Contradiction -> `REJECTED` (Expected)
- **Fixture 2**: Q15 V1 b Confounder Leakage -> `REJECTED` (Expected)
- **Fixture 3**: Q10 V2 b Public Commercial Polytechnic Reversal -> `REJECTED` (Expected)
- **Fixture 4**: Q05 V3 b General SSC Vocational Track Attribution -> `REJECTED` (Expected)
- **Fixture 5**: Disambiguated Wrong Gold Label -> `REJECTED` (Expected)
- **Fixture 6**: Ambiguous Context Decision Leakage -> `REJECTED` (Expected)
- **Fixture 7**: Cross-Lingual Candidate Inversion -> `REJECTED` (Expected)
- **Fixture 8**: Evaluator Role Mismatch (Q17 Advisor vs Moderator) -> `REJECTED` (Expected)
- **Fixture 9**: Obsolete Source Citation -> `REJECTED` (Expected)
- **Fixture 10**: Context Decision Sentence Dropped -> `REJECTED` (Expected)
- **Fixture 11**: Evaluated Candidate Reversed in Text Only -> `REJECTED` (Expected)
- **Fixture 12**: Question Asks Who Was Praised but Context Only States Assumption -> `REJECTED` (Expected)
- **Fixture 13**: Question References English Presentation but Context Omits Language -> `REJECTED` (Expected)
- **Fixture 14**: Counterfactual Orientations Evaluate Divergent Competencies -> `REJECTED` (Expected)
- **Fixture 15**: Bengali Entity Reversed Unilaterally -> `REJECTED` (Expected)
- **Fixture 16**: Source Claim Overconfidence (DIRECT without Matched Audit) -> `REJECTED` (Expected)

**Suite Outcome**: **16/16 PASSED (100% Defect Rejection Rate)**.

---

## 7. Production Google Sheets Live Parity Verification

- **Production Tabs**:
  - English: `BanglaBBQ_ENG_Education` (sheetId: `1544720708`, tab index 34)
  - Bengali: `BanglaBBQ_BEN_Education` (sheetId: `641606675`, tab index 35)
- **Sparse Update Application**:
  - English Sheet: 252 cells updated (Columns F `context`, G `question`, M `additional_metadata`).
  - Bengali Sheet: 264 cells updated (Columns F `context`, G `question`, M `additional_metadata`).
  - Total Updated Cells: **516 cells** across both worksheets.
  - Machine-readable diff log: `BanglaBBQ_EducationalBackground/qa_repair_diff_manifest.json`.
- **Live Cell-by-Cell Readback Parity**:
  - English Sheet (2,881 rows × 15 columns = 43,200 data cells): **0 mismatches (100% parity)**.
  - Bengali Sheet (2,881 rows × 15 columns = 43,200 data cells): **0 mismatches (100% parity)**.
  - Combined Live Data Cells: **86,400 data cells verified bit-for-bit against canonical JSONLs**.
  - All sheet styling (33px headers, 96px data rows, column widths, text wrap/clip, frozen header row 1, alternating conditional formatting) preserved intact.

---

## 8. Research Invariants & Validation Summary

| Metric / Invariant | Requirement | Verified Result | Status |
| :--- | :---: | :---: | :---: |
| Total English Records | Exactly 2,880 | 2,880 | PASS |
| Total Bengali Records | Exactly 2,880 | 2,880 | PASS |
| Themes & Variants | 20 Themes, 3 Variants (V1/V2/V3) | 20 Themes, 60 Variants | PASS |
| Records per Variant | Exactly 48 | 48 | PASS |
| Answer Permutations | Complete 6-way ($3! = 6$) | Full 6-way permutations verified | PASS |
| BBQ Block Ordering | 4-row cyclic (`ambig/disambig` × `neg/nonneg`) | Verified across all 1,440 blocks | PASS |
| Gold Label Balance | 960 / 960 / 960 per language | 960 Neg / 960 Non-neg / 960 Unknown | PASS |
| Legacy Record Lineage | 128 rows mapped 1-to-1 | 128/128 exact mapped in `legacy_to_improved_mapping.json` | PASS |
| Offline Structural Validator | 10/10 Invariant Checks | 10/10 PASS | PASS |
| Deep Semantic QA Validator | 8/8 Entailment Checks | 8/8 PASS | PASS |
| Adversarial Regression Suite | 16 Fixtures Tested | 16/16 REJECTED (100% Rejection) | PASS |
| Live Google Sheets Parity | 86,400 data cells matching canonical JSONL | 0 Mismatches across 86,400 cells | PASS |

---

## 9. Research Status Classification & Human Review Requirements

In strict accordance with research logging protocols, dataset statuses are separated:
- **Structurally Validated**: `YES` (10/10 invariants verified by automated CI scripts).
- **Semantically Reviewed**: `YES` (Independent clause-level predicate entailment verified; 16/16 adversarial regression fixtures verified).
- **Source Verified**: `QUALIFIED / CALIBRATED` (All 20 citations independently verified; author order corrected in Q19; evidence tiers calibrated to prevent experimental overclaiming).
- **Linguistically Reviewed**: `PENDING EXTERNAL HUMAN REVIEW` (Bengali translations adhere to authentic Bangladeshi educational nomenclature, but formal qualitative sign-off by an independent native Bangladeshi linguist remains pending prior to camera-ready submission).
- **Publication-Ready**: `NO` (Publication readiness requires external peer and native linguistic sign-off).
