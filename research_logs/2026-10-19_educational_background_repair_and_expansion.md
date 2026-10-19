# Research Log: BanglaBBQ Educational Background Complete Repair and 2,880-Record Expansion

**Date**: 2026-10-19  
**Researcher / Agent**: Antigravity (Lead NLP Researcher, Bilingual Dataset Engineer & QA Auditor)  
**Category**: Educational Background  
**Milestone Scope**: Complete repair of 128 legacy records and expansion to exactly 20 themes, 3 distinct scenario variations (V1, V2, V3), and 2,880 records per language (5,760 total records); full 6-way answer permutation balancing (3!); canonical 15-column schema; and 100% bit-for-bit live Google Sheets production replication across 86,400 data cells.  
**Status**: `STRUCTURAL PASS / LIVE REPLICATED / ALL 20 THEMES AUDITED / REVIEW PENDING`

---

## 1. Research Objective & Context

The original undergraduate thesis dataset (T2510616, BRAC University, June 2025) for Educational Background contained 128 English and 128 Bengali records structured across 4 rudimentary themes. While pioneering, forensic auditing revealed critical structural, logical, and semantic defects that compromised benchmark validity:
1. Disambiguated contexts frequently entailed the opposite answer from the recorded gold label.
2. Incomplete permutation layouts produced repeated identical QA tuples across counterfactual orientations.
3. Scenario evidence relied on unsupported stereotypes or flawed equivalences.

This research milestone executes a complete, scientifically rigorous repair and expansion adhering to the validated methodological framework established in the BanglaBBQ Politics and Religion expansions:
- **Exact Target Scale**: Exactly 20 distinct themes, 3 scenario variations per theme (V1, V2, V3), 48 records per variation, yielding 144 records per theme and exactly 2,880 records per language (5,760 records combined).
- **Preservation of Seniors' Legacy Work**: The original 128-record files in `Dataset_ BanglaBBQ_Old/Educational background/` remain strictly immutable, preserved byte-for-byte with SHA-256 integrity verification. All modern repaired and expanded data resides in `BanglaBBQ_EducationalBackground/`.
- **Live Production Parity**: Direct synchronization to the master Google Spreadsheet (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`) into dedicated production tabs `BanglaBBQ_ENG_Education` (sheetId: `1544720708`) and `BanglaBBQ_BEN_Education` (sheetId: `641606675`), matching native formatting (33px header, 96px data, canonical column widths, wrap/clip, frozen row 1, alternating 4-row styling) with 100% cell-by-cell parity.

---

## 2. Source Files & Live Google Sheet References

- **Master Google Sheet**: [BanglaBBQ Master Spreadsheet](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)
- **Worksheet Titles & IDs**:
  - `BanglaBBQ_ENG_Education` (ID: `1544720708`, Tab Index: 34)
  - `BanglaBBQ_BEN_Education` (ID: `641606675`, Tab Index: 35)
- **Sheet Grid Dimensions**: 2,881 rows (1 header + 2,880 data rows) x 15 columns (`A1:O2881`) per worksheet.
- **Data Cell Count**: 43,200 data cells per language; 86,400 data cells total (excluding headers).
- **Example ID Range**: Contiguous 0-indexed integers `0` to `2879`.
- **Canonical GitHub Datasets**:
  - English: [`BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl) (SHA256: `33f0f079df3a666146084ca4103606093b0763559846ecdbf69338e5aec3b1f1`)
  - Bengali: [`BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl) (SHA256: `a26cf111da28b55a19571d189b58b7fded165fa26b9ee7f97d82edc32f8285fc`)
- **Metadata & Manifests**:
  - Expansion Manifest: [`BanglaBBQ_EducationalBackground/expansion_manifest.json`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/expansion_manifest.json)
  - Scenario Templates: [`BanglaBBQ_EducationalBackground/scenario_templates.json`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/scenario_templates.json)
  - Legacy Mapping: [`BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json)
  - Source Audit Matrix: [`BanglaBBQ_EducationalBackground/source_audit_matrix.json`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/source_audit_matrix.json) & [`source_audit_matrix.md`](file:///d:/Research-BanglaBBQ/BanglaBBQ_EducationalBackground/source_audit_matrix.md)

---

## 3. Original Defect Diagnosis & Forensic Rectification

Forensic auditing of the seniors' legacy files (`Dataset_ BanglaBBQ_Old/Educational background/`) identified five severe systemic defects, completely mapped and repaired in `BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`:

### Defect A: 32 Inverted Disambiguated Gold Labels (25.0% of legacy data)
- **Forensic Diagnosis**: In counterfactual orientation "b" (version = "b"), the legacy authors reversed which demographic candidate suffered negative outcomes or demonstrated positive competence in the context. However, the legacy pipeline hardcoded the stereotyped group candidate index into the gold `label` without evaluating the factual entailment of the disambiguated context.
- **Affected Legacy EIDs**:
  - Q1: 5, 7, 9, 11, 17, 19, 29, 31 (8 records)
  - Q2: 37, 39, 41, 43, 49, 51, 61, 63 (8 records)
  - Q3: 69, 71, 73, 75, 81, 83, 93, 95 (8 records)
  - Q4: 101, 103, 105, 107, 113, 115, 125, 127 (8 records)
- **Repair**: Reconstructed context entailment from first principles. When the non-stereotyped candidate is explicitly evidenced as receiving negative treatment, the gold label dynamically points to that candidate, ensuring 100% factual accuracy.

### Defect B: 32 Exact Duplicate QA Tuples per Language
- **Forensic Diagnosis**: In orientation "b", the legacy dataset repeated the exact context, question, and ordered answer choices from orientation "a", creating duplicate QA inputs:
  - Q1: Pairs `(8, 28)`, `(9, 29)`, `(10, 30)`, `(11, 31)`, `(12, 24)`, `(13, 25)`, `(14, 26)`, `(15, 27)`
  - Q2, Q3, Q4: Identical duplication pattern offset by +32, +64, and +96.
- **Repair**: Full six-way permutation engineering ($3! = 6$) ensures every QA tuple has distinct answer option orderings while maintaining rigorous counterfactual balance.

### Defect C: Incomplete Answer Permutations
- **Forensic Diagnosis**: The legacy dataset implemented only partial answer rotation (often only 2 or 4 permutations), skewing candidate position frequencies.
- **Repair**: Every condition-polarity-counterfactual block is engineered across all 6 possible permutations of `[target_group, comp_group, unknown]`, guaranteeing exact label uniformity (960 labels for position 0, 960 for 1, and 960 for 2 per language).

### Defect D: Asymmetrical Counterfactual Alignment
- **Forensic Diagnosis**: Contexts reversed demographic assignments without adjusting qualification levels or contextual facts, producing semantic asymmetries.
- **Repair**: All 60 scenario templates (20 themes x 3 variations) were written with strict counterfactual parity, ensuring both demographic orientations ('a' and 'b') hold qualifications, job levels, and evaluation settings identical.

### Defect E: Weak or Flawed Scenario Premises
- **Legacy Q1**: Fictional context claimed madrasa background guaranteed non-interview, whereas empirical audit literature documents resume-stage callback differences. Grounded in Asadullah et al. (2021) resume audit study.
- **Legacy Q2**: Confused National University (which is a public affiliating university) with private colleges. Reframed to compare NU-affiliated regional colleges with autonomous standalone public universities (DU, RU, CU), holding academic grades constant.
- **Legacy Q3**: Recruiter conversation continuing was conflated with an assured job offer. Matched demonstrated English oral fluency to isolate schooling-track prejudice from actual language ability.
- **Legacy Q4**: Asserted discriminatory government hiring against private universities, which is legally barred under PSC merit examinations. Reframed to corporate/banking private-sector recruitment bias (Hosain et al., 2021).

---

## 4. Methodology & Mathematical Design

The benchmark expansion adheres strictly to the canonical BBQ mathematical architecture:

```
20 Themes × 3 Variations (V1, V2, V3) = 60 Scenario Units
Each Scenario Unit = 48 Records:
  - 2 Counterfactual Orientations ('a', 'b') × 24 records
  - 2 Context Conditions ('ambig', 'disambig') × 12 records
  - 2 Question Polarities ('neg', 'nonneg') × 6 records
  - 6 Answer Permutations (3!) = 6 records per condition-polarity block
Total = 60 × 48 = 2,880 records per language (5,760 total)
```

### Canonical 4-Row Block Sequence
Throughout the entire dataset, records follow the strict 4-row cyclical pattern:
1. `ambig` + `neg` (Gold: Unknown)
2. `disambig` + `neg` (Gold: Entailed candidate)
3. `ambig` + `nonneg` (Gold: Unknown)
4. `disambig` + `nonneg` (Gold: Entailed candidate)

### Invariants Maintained
- **Ambiguous Invariant**: Exactly 1,440 ambiguous records per language, 100% entailing `Unknown` (ENG) / `অজানা` (BEN).
- **Disambiguated Invariant**: Exactly 1,440 disambiguated records per language, 100% entailing explicitly grounded named entities.
- **Label Uniformity**: Exactly 960 labels at index `0`, 960 at index `1`, and 960 at index `2`.
- **Condition Balance**: 1,440 ambiguous / 1,440 disambiguated; 1,440 negative / 1,440 nonnegative.
- **Theme Balance**: Exactly 144 records per theme across all 20 themes.
- **Metadata Conventions**: Preserved all 15 canonical schema fields (`example_id`, `question_index`, `context_condition`, `question_polarity`, `type`, `context`, `question`, `ans0`, `ans1`, `ans2`, `label`, `answer_info`, `additional_metadata`, `category`, `id`). Counterfactual orientation tracked in `additional_metadata.version = "a"|"b"`; scenario variations tracked via `variation = "v1"|"v2"|"v3"` in the expansion manifest.

---

## 5. Source Audit & Evidence Grounding Matrix

All 20 themes were audited against primary peer-reviewed literature, statutory frameworks, World Bank / ILO research, and Bangladesh investigative journalism:

| Theme ID | Title | Target vs Comparison | Primary Source Citation | Source Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Q01** | Alia Madrasa vs General School Background | Alia Madrasa vs General School | Asadullah et al. (2021), *No Faith in the Labour Market*, Dhaka Tribune | `DIRECT` |
| **Q02** | NU-Affiliated College vs Standalone Public University | NU-Affiliated College vs Standalone Public | The Daily Star (2019/2024), *NU Graduates Lagging Behind Job Market* | `DIRECT` |
| **Q03** | Bangla-Medium vs English-Medium Schooling | Bangla-Medium vs English-Medium | The Business Standard (2023), *English vs Bangla Medium Career Impact* | `DIRECT` |
| **Q04** | Private vs Standalone Public University | Private vs Standalone Public | Hosain et al. (2021), *PRR*, DOI: 10.1108/PRR-01-2021-0005 | `DIRECT` |
| **Q05** | SSC Vocational vs General SSC | SSC Vocational vs General Academic SSC | The Business Standard (2020), *Technical Education Inferiority Stigma* | `DIRECT` |
| **Q06** | HSC Vocational vs General HSC | HSC Vocational vs General HSC | Rahman et al. (2024), *IJTR*, DOI: 10.1080/14480220.2024.2332345 | `DIRECT` |
| **Q07** | HSC Business Management vs General Business Studies | HSC BM vs General HSC Business Studies | Rahman et al. (2024), *IJTR*, DOI: 10.1080/14480220.2024.2332345 | `DIRECT` |
| **Q08** | Polytechnic Diploma vs General Academic Pathway | Polytechnic Diploma vs Higher Secondary General | World Bank (2019), *Employability of Post-Secondary Education in BD* | `DIRECT` |
| **Q09** | Diploma Engineer vs BSc Engineer | Diploma Engineer vs BSc Graduate Engineer | The Business Standard (2025), *BSc vs Diploma Engineers Social Friction* | `DIRECT` |
| **Q10** | Public vs Private Polytechnic Institute | Private Polytechnic vs Public Polytechnic | World Bank (2019), *Tertiary Technical Employability Report* | `PARTIAL` |
| **Q11** | Government vs Nongovernment NU-Affiliated College | Non-Govt NU College vs Govt NU College | CEDP / World Bank (2021), *College Education Development Project* | `PARTIAL` |
| **Q12** | Bangladesh Open University vs Conventional Campus | BOU Distance Degree vs Conventional University | Islam et al. (2017), *TOJDE*, DOI: 10.17718/tojde.340370 | `DIRECT` |
| **Q13** | Science vs Humanities at School | Humanities Stream vs Science Stream | The Daily Star Shout (2017), *Systematic Oppression of Arts/Commerce* | `DIRECT` |
| **Q14** | Science vs Business Studies at School | Business Studies vs Science Stream | The Daily Star Shout (2017), *Arts/Commerce Marginalization* | `DIRECT` |
| **Q15** | Prestigious vs Less-Known University in Recruitment | Less-Known University vs Prestigious University | The Business Standard (2024), *Prestige Trap in Job Markets* | `DIRECT` |
| **Q16** | Highly Recognized vs Lesser-Known Private University | Top-Tier Private vs Low-Tier Private University | BRAC University (2022), *University Selection Drivers in BD* | `PARTIAL` |
| **Q17** | NCTB English Version vs NCTB Bangla Version | NCTB Bangla Version vs NCTB English Version | National Curriculum and Textbook Board (NCTB) / TBS (2023) | `PARTIAL` |
| **Q18** | Government vs Private Secondary School Background | Private Non-Govt School vs Govt High School | Alam & Parvin (2020), *IJEM*, DOI: 10.1108/IJEM-07-2019-0254 | `DIRECT` |
| **Q19** | Recognition of Prior Learning vs Conventional Training | RPL Certified vs Formal TVET Graduate | World Bank (2021), Policy Research Working Paper 9644 / ILO BNQF | `DIRECT` |
| **Q20** | University Humanities vs University STEM Background | Humanities Graduate vs STEM Graduate | World Bank (2019), *Post-Secondary Employability* / JMBE (2022) | `DIRECT` |

---

## 6. Pre-Edit and Post-Edit Backups

- **Legacy Historical Baseline Files**:
  - `Dataset_ BanglaBBQ_Old/Educational background/banglabbq_education_english.jsonl`  
    SHA256: `d66b34ee1ef147ceec25a51f9e5cedd8569fd0eac6bfa48a4095125a4bc49ebd`
  - `Dataset_ BanglaBBQ_Old/Educational background/banglabbq_education_bengali.jsonl`  
    SHA256: `ba308416a74e0dc070fb58f98d495fac7f4ef34a137680ec6a590eea94e319ee`
  - *Verification*: Both baseline files verified untouched byte-for-byte with zero modifications.
- **Modern Canonical Expansion Datasets**:
  - `BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl`  
    SHA256: `33f0f079df3a666146084ca4103606093b0763559846ecdbf69338e5aec3b1f1`
  - `BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl`  
    SHA256: `a26cf111da28b55a19571d189b58b7fded165fa26b9ee7f97d82edc32f8285fc`

---

## 7. Quality Assurance & Validation Results

### Automated Offline Test Suite Execution
Two purpose-built test suites were executed on the assembled datasets:

1. **Structural Invariants** (`scripts/validate_education_dataset.py`):
   - Check 1 (Record Counts): 2,880 ENG / 2,880 BEN (PASS)
   - Check 2 (Sequential IDs & 15-Column Schema): IDs 0–2879, valid schema (PASS)
   - Check 3 (Theme Counts & Balance): Exactly 144 records per theme across all 20 themes, 72 ambig / 72 disambig (PASS)
   - Check 4 (Canonical 4-row Block Ordering): Canonical BBQ block sequence maintained throughout all 2,880 rows (PASS)
   - Check 5 (Label Distribution): Exactly 960 labels at index 0, 960 at index 1, 960 at index 2 (PASS)
   - Check 6 (Six-Way Permutations): All 480 condition-polarity sub-blocks contain full 6 answer rotations (PASS)
   - Check 7 (Ambiguous Invariant): All 1,440 ambiguous records strictly entail Unknown (PASS)
   - Check 8 (Disambiguated Invariant): All 1,440 disambiguated records strictly entail named entities (PASS)
   - Check 9 (Bilingual Parity): 100% field, label, and role parity between ENG and BEN (PASS)
   - Check 10 (Zero Duplicate QA Records): 2,880/2,880 unique QA tuples (PASS)
   - **Result**: `ALL 10 STRUCTURAL INVARIANTS PASSED 100%`

2. **Semantic & Role-Entailment Invariants** (`scripts/validate_education_semantics.py`):
   - Semantic Check 1 (Ambiguous Unknown Entailment): 1,440/1,440 ambiguous records map strictly to Unknown / অজানা (PASS)
   - Semantic Check 2 (Disambiguated Grounding): 1,440/1,440 disambiguated records grounded in named entities with 100% role parity (PASS)
   - Semantic Check 3 (Permutation Invariance): All 480 condition-polarity sub-blocks exhibit strict permutation role invariance (PASS)
   - Semantic Check 4 (Counterfactual Inversion): All 60 scenarios demonstrate 100% symmetrical counterfactual inversion (PASS)
   - **Result**: `ALL SEMANTIC & ROLE-ENTAILMENT INVARIANTS PASSED 100%`

3. **Live Production Parity Verification** (`scripts/verify_education_live_parity.py`):
   - English: 43,200/43,200 live data cells verified bit-for-bit against canonical JSONL (0 mismatches, 100% parity).
   - Bengali: 43,200/43,200 live data cells verified bit-for-bit against canonical JSONL (0 mismatches, 100% parity).
   - Total Verified Cells: 86,400 live data cells (100% parity).
   - Formatting Verified: 33px header height, 96px data row height, frozen row 1, canonical column widths `[100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]`, alternating 4-row styling.

---

## 8. Remaining Limitations & Open Issues

1. **Human Colloquial Bengali Linguistic Review**:
   - While all Bengali translations were engineered using natural Bangladeshi educational vocabulary (e.g., `মাদ্রাসা ব্যাকগ্রাউন্ড`, `জাতীয় বিশ্ববিদ্যালয় অধিভুক্ত কলেজ`, `পলিটেকনিক ডিপ্লোমা`, `বিএসসি ইঞ্জিনিয়ারিং`, `কারিগরি শিক্ষা`), full independent review by a native Bangladeshi linguist is recommended prior to formal academic publication.
2. **Themes Designated `PARTIAL`**:
   - Themes Q10 (Public vs Private Polytechnic), Q11 (Govt vs Non-Govt NU College), Q16 (Reputable vs Lesser-Known Private University), and Q17 (English Version vs Bangla Version) are supported by institutional context and educational choice reports rather than direct randomized resume audits. While scientifically grounded in real educational disparities, their experimental interpretation must be noted in the final benchmark paper.
3. **Publication Status**:
   - Not marked publication-ready until external peer validation and independent native Bengali certification are finalized.

---

## 9. Git & Commit Tracking

- **Committed Files**:
  - `BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl`
  - `BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl`
  - `BanglaBBQ_EducationalBackground/expansion_manifest.json`
  - `BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json`
  - `BanglaBBQ_EducationalBackground/scenario_templates.json`
  - `BanglaBBQ_EducationalBackground/source_audit_matrix.json`
  - `BanglaBBQ_EducationalBackground/source_audit_matrix.md`
  - `scripts/assemble_education_dataset.py`
  - `scripts/build_all_themes_def.py`
  - `scripts/build_scenario_templates.py`
  - `scripts/education_themes_def.py`
  - `scripts/sync_education_sheets.py`
  - `scripts/themes_data/`
  - `scripts/validate_education_dataset.py`
  - `scripts/validate_education_semantics.py`
  - `scripts/verify_education_live_parity.py`
  - `.github/workflows/validate.yml`
  - `research_logs/2026-10-19_educational_background_repair_and_expansion.md`
  - `research_logs/README.md`
  - `memory/state.md`
  - `memory/history.md`
  - `memory/index.md`
- **Remote Synchronization**: Pushed to `origin/main` without force-pushing.
