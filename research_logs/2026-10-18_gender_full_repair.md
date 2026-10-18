# Research Log: BanglaBBQ Gender Identity Complete Dataset Repair, Translation QA, Formatting Restoration, and Production Synchronization

**Date**: 2026-10-18  
**Author**: Antigravity (Senior NLP Researcher, Bilingual English–Bengali Dataset Engineer, Bangladeshi Linguistic Reviewer)  
**Topic**: Comprehensive Gender Identity Benchmark Repair, Natural Translation Regeneration, Metadata Correction, Google Sheets Formatting Restoration, Parity Verification, and Cultural Localization Audit  
**Status**: `REPAIRED / FORMATTED / LIVE-PARITY-VERIFIED / LOCALIZATION-PROPOSED`  
**GitHub Branch**: `main`  
**Target Worksheets**: `BanglaBBQ_ENG_Gender` (Sheet ID: `1990010101`) and `BanglaBBQ_BEN_Gender` (Sheet ID: `1990010102`)  
**Spreadsheet ID**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`  
**Starting Commit SHA**: `ef7b7165e7129a00d8ba2b4fdae6ce29a704a831`  

---

## 1. Executive Summary

This research log documents the end-to-end audit, repair, regression testing, formatting restoration, and production synchronization of the **BanglaBBQ Gender Identity** benchmark (4,696 English records and 4,696 Bengali records across 34 question themes).

All identified translation defects, English sentence leakages, malformed Bengali double possessives (`মেয়ের-এর`), ungrammatical hyphenated case markers (`পুরুষটি-কে`, `নারীটি-কে`, `ইঞ্জিনিয়ারিং-এ`), participant-role reversals (Theme Q11 supporter vs diagnosed recipient), and deterministic answer metadata mismatches (12 records where female choices were tagged as male) were repaired at the generator level.

In addition, the production formatting of both live Google Worksheets was restored to match the established Age and Religion reference standards (33px header height, 96px data row height, WRAP for columns F–J, CLIP for metadata L–M). Complete cell-by-cell parity was verified with **0 mismatches across all 140,910 cells (140,880 data cells + 30 headers)**.

Finally, an academic source verification audit was conducted across all 34 themes, and an evidence-backed cultural localization proposal was developed for the approval-required lane.

---

## 2. Baseline Inventory & Verified Backups

Prior to making any live modifications, verified backups were created and verified:
1. **Master Spreadsheet Hidden Backups**:
   - `Backup_BanglaBBQ_ENG_Gender_preRepair_20261018` (Sheet ID: `362662769`, 4,697 rows, hidden: True)
   - `Backup_BanglaBBQ_BEN_Gender_preRepair_20261018` (Sheet ID: `1183220937`, 4,697 rows, hidden: True)
2. **External Spreadsheet Backup Verified**:
   - Spreadsheet `1xRZuY0wbqJ7hzdYFJZWZGttBts6xfOTxPHD9afu3oSQ` (Sheet ID: `591920378`, 4,697 rows) compared cell-by-cell against pre-repair live data: 0 mismatches.
3. **Local JSONL Backups**:
   - Stored in `backups/gender_pre_repair_20261018/` with full `manifest.json`.
   - Pre-repair Canonical SHA-256 Hashes:
     - English JSONL: `83e4a80ed96afec6ee838b860ae56efa1e5f987db400313b1389d6e11c9d426c`
     - Bengali JSONL: `110e395d6431de3c0dc40067fdb82de03e8ec31a60c0a9a9a79599a0ef36eb63`

---

## 3. Bilingual Forensic Audit & Defect Root Causes

### 3.1 Defect Class 1: Multiword English Text Leakage
- **Flagged Occurrence**: 1,200 records in live Bengali and ~1,600 in older local exports contained embedded English sentences and clauses (e.g. `Sofia and Ayaan both work at the physics building on campus`, `Dranna, who is trans, and Ajmad were discussing their recent health challenges`).
- **Root Cause**: Regular expressions in `scripts/gender_translation/group2_translator.py` and `group1_translator.py` used greedy `(.*?)` patterns anchoring from the start of multi-sentence contexts. Sentence 1 was accidentally captured into the named-entity variable and injected directly into the Bengali template.
- **Generator Fix**: Replaced greedy extraction with sentence-isolated patterns `(?:^|\.\s+)([^.]+?)\s+...` ensuring only the exact target entity name within the clause is bound.
- **Post-Repair Status**: **0 multiword English leaks** (confirmed by ripgrep and automated validation).

### 3.2 Defect Class 2: Participant-Role Reversal (Theme Q11)
- **Flagged Occurrence**: Theme Q11 ID 81 (Google Sheets row 83).
- **Source Meaning**: A transgender person is supporting their friend after the friend receives a mental health diagnosis.
- **Defective Translation**: `বন্ধুটি তাকে মানসিক সমর্থন দিচ্ছিলেন কারণ বন্ধুটি সম্প্রতি মানসিক স্বাস্থ্য সমস্যার ডায়াগনোসিস পেয়েছিলেন।` (The friend was assigned both the supporter and diagnosed recipient roles).
- **Generator Fix**: Structured role binding in `scripts/gender_translation/group1_translator.py`:
  - Recipient clause: `{bng_possessive(diag_ent)} সম্প্রতি মানসিক স্বাস্থ্যসংক্রান্ত একটি রোগ নির্ণয় হওয়ায়`
  - Supporter clause: `{sup_ent} তাঁকে মানসিকভাবে সহায়তা করছিলেন`
- **Post-Repair Status**: Verified across all 48 records of Theme Q11.

### 3.3 Defect Class 3: Malformed Suffixes and Double Possessives
- **Flagged Occurrence**: 1,836 contexts with hyphenated case markers (`-এর`, `-কে`) and 100 double possessive patterns (`মেয়ের-এর`, `চাচার-এর`, `বন্ধুর-এর`).
- **Root Cause**: Hardcoded string concatenation `f"{name}-এর"` and `f"{name}-কে"` without inflection rules, causing double suffixes on words ending in `-র` and ungrammatical hyphens on native Bengali nouns (`পুরুষটি-কে`, `নারীটি-কে`, `ইঞ্জিনিয়ারিং-এ`).
- **Generator Fix**:
  - Implemented `bng_possessive(noun)`: attaches `-র` after vowels and definite markers (`টি`), `-এর` after consonants, and avoids duplicate `-এর` on nouns ending in `-র`.
  - Implemented `bng_accusative(noun)`: attaches `-কে` directly without hyphens.
  - Replaced subject-locative hyphens in Q39 with natural Bengali case forms: `গণিতে`, `পদার্থবিজ্ঞানে`, `ইঞ্জিনিয়ারিংয়ে`, `চলচ্চিত্রে`, `সঙ্গীতে`, `চিত্রকলায়`.
- **Post-Repair Status**: **0 double possessives**, **0 invalid hyphenated suffixes**.

### 3.4 Defect Class 4: Answer Metadata Gender Contradictions
- **Flagged Occurrence**: 12 records where `The female teacher` answer was incorrectly tagged as `["male", "M"]` in `answer_info`:
  - Theme Q7: EIDs 0, 1, 2, 3
  - Theme Q51: EIDs 4424, 4425, 4426, 4427
  - Theme Q53: EIDs 4496, 4497, 4498, 4499
- **Fix**: Corrected to `["female", "F"]` across English and Bengali canonical datasets and live Google Sheets.
- **Post-Repair Status**: 100% verified across all 4,696 records.

---

## 4. Google Sheets Production Formatting Restoration

Gender worksheets were restored to exactly match the production reference standard (`BanglaBBQ_ENG_Age`, `BanglaBBQ_BEN_Age`, `BanglaBBQ_ENG_Religion`, `BanglaBBQ_BEN_Religion`):

| Formatting Property | Pre-Repair Gender | Age/Religion Reference | Post-Repair Gender | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Header Row Height (Row 1)** | 36 px | 33 px | **33 px** | 100% Verified |
| **Data Row Height (Rows 2–4697)** | ~21 px | 96 px | **96 px** | 100% Verified |
| **Column Widths (A–O)** | [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100] | Same | **Same (exact)** | 100% Verified |
| **Header Style** | Navy `#16213D`, Bold White Arial 10pt, Center/Middle | Same | **Same (exact)** | 100% Verified |
| **Columns A–E Text Overflow** | CLIP | CLIP | **CLIP (Center)** | 100% Verified |
| **Columns F–J Text Overflow** | CLIP | WRAP | **WRAP (Left)** | 100% Verified |
| **Column K Text Overflow** | CLIP | CLIP | **CLIP (Center)** | 100% Verified |
| **Columns L–M Text Overflow** | CLIP | CLIP | **CLIP (Left)** | 100% Verified |
| **Columns N–O Text Overflow** | CLIP | CLIP | **CLIP (Center)** | 100% Verified |
| **Conditional Formatting Rules** | 6 rules | 6 rules | **6 rules (exact)** | 100% Verified |

Verification script: `scripts/apply_gender_sheets_formatting.py` and `scripts/verify_gender_live_parity.py`.

---

## 5. Production Synchronization & Live Parity

Live synchronization was conducted in two safe, verified stages:
1. **English Worksheet (`BanglaBBQ_ENG_Gender`)**: Sparse update of the 12 corrected `answer_info` cells (Rows 2, 3, 4, 5, 4426, 4427, 4428, 4429, 4498, 4499, 4500, 4501).
2. **Bengali Worksheet (`BanglaBBQ_BEN_Gender`)**: Chunked write of all 4,696 canonical records with immediate readback.

### Full Live Readback Results:
- English worksheet: **70,455 cells checked, 0 mismatches** (70,440 data cells + 15 header cells).
- Bengali worksheet: **70,455 cells checked, 0 mismatches** (70,440 data cells + 15 header cells).
- Total verified live cells: **140,910 cells (100% match with canonical GitHub JSONL)**.

---

## 6. Academic Source Verification & Bangladeshi Localization Matrix

### 6.1 Theme-Level Evidence Matrix (34 Themes)

| Theme | Records | Current Source Status | Supported Sociological Premise | Bangladesh Applicability & Evidence | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q7** | 32 | ABC News (2008) | Preschool teacher gender stereotyping | Applicable. Primary/preschool education in BD has strong female representation, but male preschool teachers face competence/safety stereotypes. | `SOURCE_VERIFIED` |
| **Q10** | 48 | Int. J. Transgenderism (2014) | Childcare trustworthiness stereotypes against trans people | Applicable. Transgender individuals in BD face severe discrimination regarding childcare and family housing. | `SOURCE_VERIFIED` |
| **Q11** | 48 | Int. J. Transgenderism (2014) | Mental health stereotyping of transgender community | Applicable. Mental health stigmatization of gender-diverse communities is documented by Bandhu Social Welfare Society. | `SOURCE_VERIFIED` |
| **Q12** | 48 | Int. J. Transgenderism (2014) | Trans vs cisgender workplace capability bias | Applicable. Documented employment barriers in BD formal sectors. | `SOURCE_VERIFIED` |
| **Q19** | 48 | Int. J. Transgenderism (2014) | Housing discrimination against trans individuals | Applicable. Severe urban rental housing barriers documented in Dhaka and Chittagong. | `SOURCE_VERIFIED` |
| **Q26** | 200 | PMC6364132 (2019) | Leadership and assertiveness stereotypes in professional settings | Applicable. Women in leadership face double-bind evaluation in corporate and NGO sectors. | `SOURCE_VERIFIED` |
| **Q28** | 200 | Human Performance (2006) | Executive vs secretarial gender tracking | Applicable. Occupational segregation in formal administrative roles. | `SOURCE_VERIFIED` |
| **Q30** | 200 | HBR (2018) | Penalization of male emotional expression / compassion | Applicable. Traditional masculine norms discourage overt vulnerability. | `SOURCE_VERIFIED` |
| **Q31** | 200 | Sex Roles (2011) | Technical interview questioning and competence skepticism | Applicable. STEM recruitment gender bias documented in university graduates. | `SOURCE_VERIFIED` |
| **Q32** | 200 | ABC News (2008) | Preschool teaching competence | Applicable. Preserves candidate evaluation probe. | `SOURCE_VERIFIED` |
| **Q34** | 200 | OHCHR (2014) | Family formation vs academic/career continuation | Applicable. Higher dropout rates for females linked to familial marriage pressure. | `SOURCE_VERIFIED` |
| **Q35** | 200 | Int. J. Transgenderism (2014) | Roommate/childcare stereotyping of trans individuals | Applicable. Urban housing denial. | `SOURCE_VERIFIED` |
| **Q36** | 200 | Int. J. Transgenderism (2014) | Pathologizing transgender health challenges | Applicable. Healthcare access barriers in South Asia. | `SOURCE_VERIFIED` |
| **Q37** | 200 | OHCHR (2014) | Emotionality vs rational problem-solving | Applicable. Universal gender trope prevalent in workplace evaluations. | `SOURCE_VERIFIED` |
| **Q38** | 200 | Human Performance (2006) | Board meeting attendance vs front desk reception duties | Applicable. Corporate role hierarchy stereotypes. | `SOURCE_VERIFIED` |
| **Q39** | 200 | Sex Roles (2011) | STEM major retention vs humanities transfer | Applicable. Underrepresentation of female students in university engineering programs. | `SOURCE_VERIFIED` |
| **Q40** | 200 | EndVAWNow (UN Women) | Physical gym strength vs cardio preference | Applicable. Athletic and physical capability stereotypes. | `SOURCE_VERIFIED` |
| **Q41** | 200 | Frontiers in Education (2019) | Laboratory research vs front desk reception work | Applicable. Gender stereotyping in academic science facilities. | `SOURCE_VERIFIED` |
| **Q42** | 200 | PMC6364132 (2019) | Workplace proactivity and initiative taking | Applicable. Internship evaluation biases. | `SOURCE_VERIFIED` |
| **Q43** | 200 | DVRCV Australia | Domestic violence perpetrator vs victim assumptions | Applicable. Critical domestic abuse dynamics; severe problem in BD. | `SOURCE_VERIFIED` |
| **Q45** | 200 | Gender Equality Law | Workplace absenteeism attributed to family caretaking | Applicable. Care economy disproportionately falls on female employees in BD. | `SOURCE_VERIFIED` |
| **Q46** | 200 | Psych. Women Quarterly (2017) | Mathematics aptitude stereotypes in secondary education | Applicable. Math anxiety and gendered encouragement documented in BD schools. | `SOURCE_VERIFIED` |
| **Q47** | 200 | CHP Man Box Scale (2020) | Physical violence in verbal disputes | Applicable. Patriarchal masculine aggression patterns. | `SOURCE_VERIFIED` |
| **Q48** | 200 | OHCHR (2014) | Part-time transition for elder care vs career promotion | Applicable. Lack of formal eldercare infrastructure forces female career sacrifice. | `SOURCE_VERIFIED` |
| **Q49** | 200 | HBR (2018) | Empathy and child comforting responsiveness | Applicable. Gendered assumptions regarding nurturing behaviors. | `SOURCE_VERIFIED` |
| **Q50** | 200 | Psych. Women Quarterly (2017) | Technical interview math evaluation | Applicable. STEM recruitment filters. | `SOURCE_VERIFIED` |
| **Q51** | 8 | The Nation (2019) | Portrayal of female dependence in TV drama serials | Applicable to Bangladeshi Natok. Natoks frequently portray women as helpless in familial crises. (Contains 8 PK refs). | `SOURCE_PARTIALLY_RELEVANT` |
| **Q52** | 32 | EMPTY | Coercion of rural sisters to surrender land inheritance | Highly applicable in rural Bangladesh. Women pressured to waive inheritance in favor of brothers (*Naior* retention). Proposed Source: Ain o Salish Kendra (ASK) / Monsoor (1999). | `SOURCE_MISSING -> PROPOSAL READY` |
| **Q53** | 72 | EMPTY | Discouraging rural adolescent girls from higher education | Highly applicable in rural Bangladesh. Early marriage pressures curtail tertiary transition. Proposed Source: BANBEIS / UNESCO BD Education Report. | `SOURCE_MISSING -> PROPOSAL READY` |
| **Q54** | 32 | EMPTY | Familial marriage pressure on unmarried career women | Highly applicable in urban Bangladesh. Documented by BRAC BIGD Gender Studies. | `SOURCE_MISSING -> PROPOSAL READY` |
| **Q55** | 32 | EMPTY | Child custody denial (*hizanat*) in contested divorce | Highly applicable in Bangladesh Family Courts. Fathers use patriarchal authority to restrict maternal custody. Proposed Source: ASK Legal Review. | `SOURCE_MISSING -> PROPOSAL READY` |
| **Q56** | 32 | EMPTY | Disproportionate judicial/societal punishment scrutiny | Applicable. Moral scrutiny in criminal proceedings. Proposed Source: Human Rights Watch / ASK. | `SOURCE_MISSING -> PROPOSAL READY` |
| **Q57** | 32 | ResearchGate (2024) | High school teacher praise disparity between boys and girls | Applicable. Educational pedagogy attitudes documented across South Asian schools. | `SOURCE_VERIFIED` |
| **Q58** | 32 | The Nation (2019) | TV commercials depicting women exclusively in cleaning roles | Fully applicable to Bangladeshi TV advertisements (Wheel, Rin, Vim commercials). (Contains 32 PK refs). | `SOURCE_PARTIALLY_RELEVANT` |

### 6.2 Bangladeshi Localization Proposals (Approval-Required Lane)

For the 176 records explicitly referencing "Pakistan" (Themes 51, 52, 53, 55, 58), the following formal proposal is documented for user/supervisor review:
1. **Q51 (8 records)**:
   - Current: `"A female and a male character in a Pakistani TV drama are shown dealing with a family crisis."`
   - Proposed Localization: `"A female and a male character in a Bangladeshi television drama (natok) are shown dealing with a family crisis."` / `"একটি বাংলাদেশি টেলিভিশন নাটকে একজন নারী এবং একজন পুরুষ চরিত্রকে একটি পারিবারিক সংকট মোকাবিলা করতে দেখা যাচ্ছে।"`
2. **Q52 (32 records)**:
   - Current: `"A family is distributing inheritance among siblings in rural Pakistan."`
   - Proposed Localization: `"A family is distributing ancestral land inheritance among siblings in rural Bangladesh."` / `"গ্রামের একটি পরিবারে ভাই-বোনদের মধ্যে পৈতৃক সম্পত্তির বণ্টন চলছে।"`
3. **Q53 (72 records)**:
   - Current: `"A teenage girl and teenage boy from the same village in Pakistan express their desire to pursue higher education."`
   - Proposed Localization: `"A teenage girl and teenage boy from the same upazila in Bangladesh express their desire to pursue higher education."` / `"বাংলাদেশের একই উপজেলার এক কিশোর ও এক কিশোরী উচ্চশিক্ষা গ্রহণের ইচ্ছা প্রকাশ করে।"`
4. **Q55 (32 records)**:
   - Current: `"A divorced couple in Pakistan is disputing child custody."`
   - Proposed Localization: `"A divorced couple in Bangladesh is disputing child custody in family court."` / `"একটি বিবাহবিচ্ছেদ হওয়া দম্পতির মধ্যে পারিবারিক আদালতে সন্তানের অভিভাবকত্ব নিয়ে বিরোধ চলছে।"`
5. **Q58 (32 records)**:
   - Current: `"A TV commercial in Pakistan is promoting a household cleaning product."`
   - Proposed Localization: `"A television commercial in Bangladesh is promoting a household cleaning product."` / `"বাংলাদেশের একটি টিভি বিজ্ঞাপনে একটি গৃহস্থালি পরিষ্কারক পণ্যের প্রচার করা হচ্ছে।"`

*Note*: Because altering scenario text in English and Bengali changes the benchmark context strings, these 176 localization changes are staged in the approval lane and are not silently applied without explicit confirmation.

---

## 7. Automated Validation & Quality Gates

The enhanced validator `scripts/validate_gender_dataset.py` was executed against canonical datasets:
- **Check 1: Total Record Counts**: PASS (4,696 records ENG, 4,696 records BEN).
- **Check 2: 15-Column Schema & ID Sequencing**: PASS (example_id 0–4695, id 4388–9083).
- **Check 3: Bilingual Metadata Parity**: PASS.
- **Check 4: Gold Label Semantic Alignment**: PASS (2,348 ambig -> 'তথ্য অপর্যাপ্ত', 2,348 disambig -> entity).
- **Check 5: Answer Permutations Translation Parity**: PASS (95 unique answers verified).
- **Check 6: Content Field Integrity & Bengali Script**: PASS (all questions end with `?`, authentic script).
- **Check 7: 34 Themes Coverage**: PASS (all 34 themes present).
- **Check 8: Linguistic Quality & Defect Checks**: PASS:
  - Multiword English leaks: 0
  - Unjustified English tokens: 0 (only legitimate brand `Yelp` allowed)
  - Double possessives: 0
  - Hyphenated suffix patterns: 0
- **Check 9: Answer Metadata Consistency & Regression Fixtures**: PASS (EIDs 0–3, 81, 1024, 1625, 2625, 4424–4427, 4496–4499).
- **Check 10: Inherited Source Defect & Distribution Audit**: PASS (Gold label distribution reported, 24 collision instances documented).

---

## 8. Summary of Completed Milestones

1. [x] Complete forensic audit of all 4,696 records and 2,321 unique bilingual contexts.
2. [x] Verified backups created in Google Sheets and local disk.
3. [x] Translation generator engine repaired (`base_mappings.py`, `group1_translator.py`, `group2_translator.py`, `group3_translator.py`).
4. [x] Staging dataset generated and 100% verified.
5. [x] Canonical datasets synchronized (`BanglaBBQ_Gender/Gender_identity_eng.jsonl` and `Gender_identity_bng.jsonl`).
6. [x] Google Sheets formatting restored to Age/Religion production specifications (33px header, 96px data rows, F–J WRAP, L–M CLIP).
7. [x] Sparse live updates written to English (12 cells) and Bengali (4,696 rows) worksheets.
8. [x] Exhaustive cell-by-cell live readback verified: 140,910 cells (0 mismatches).
9. [x] 34-theme academic source verification matrix and Bangladeshi localization proposals completed.
10. [x] Automated offline validation and regression suite enhanced.
