# Research Log: BanglaBBQ Gender Identity Dataset Migration, Natural Bengali Translation, and Live Google Sheets Synchronization

**Date**: 2026-10-18  
**Author**: Antigravity (Senior NLP Researcher & Bilingual Dataset Engineer)  
**Topic**: Full Gender Identity Benchmark Migration (4,696 English & 4,696 Bengali Records across 34 Themes)  
**Status**: `STRUCTURAL PASS / REPLICATED LIVE / SECONDARY LINGUISTIC & SOURCE REVIEW PENDING`  
**GitHub Branch**: `main`  
**Target Worksheets**: `BanglaBBQ_ENG_Gender` (Sheet ID: `1990010101`) and `BanglaBBQ_BEN_Gender` (Sheet ID: `1990010102`)  
**Spreadsheet ID**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`

---

## 1. Executive Summary

This milestone successfully executes the full translation, construction, live synchronization, formatting replication, and exhaustive quality assurance for the **BanglaBBQ Gender Identity** benchmark. 

The benchmark preserves the complete 4,696-record combinatorial structure from the canonical PakBBQ English source across **34 question themes** (Q7, Q10–Q12, Q19, Q26, Q28, Q30–Q32, Q34–Q43, Q45–Q50, Q51–Q58), comprising:
- **Group 1 (Demographic Descriptors)**: Themes 7, 10, 11, 12, 19 (224 records)
- **Group 2 (Named Entity Probes)**: Themes 26, 28, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50 (4,200 records across 21 themes x 200 records)
- **Group 3 (Societal & Media Gender Probes)**: Themes 51, 52, 53, 54, 55, 56, 57, 58 (272 records)

All 4,696 records were translated into natural, contemporary, contextually accurate Bangladeshi Bengali while strictly maintaining the exact 15-column schema, sequential IDs, polarity, answer permutations, and gold label semantic alignment.

Both worksheets (`BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender`) were populated, formatted to native production standards, and read back cell-by-cell with **zero mismatches across all 140,880 data cells (140,910 total cells including headers)**.

---

## 2. Independent Audit of Inherited Source Defects

In accordance with research transparency standards, inherited defects from the PakBBQ/BBQ source were audited independently prior to translation. They were faithfully preserved and documented rather than silently manipulated:

1. **Gold Label Imbalance**:
   - `0`: 1,582 records (33.69%)
   - `1`: 1,552 records (33.05%)
   - `2`: 1,562 records (33.26%)
   - *Audit finding*: Inherited from the original BBQ/PakBBQ sampling and permutation generator.
2. **Missing Source Citations**:
   - Exactly 200 records possess empty `additional_metadata.source` strings (`""`).
   - *Breakdown*: Theme 52 (32), Theme 53 (72), Theme 54 (32), Theme 55 (32), Theme 56 (32).
3. **Identical Entity Probes**:
   - Exactly 24 records contain identical names for both candidate entities:
     - Theme 32 (Examples 1152–1159): `Gul` vs `Gul` (8 records)
     - Theme 40 (Examples 2616–2623): `Zaryab` vs `Zaryab` (8 records)
     - Theme 43 (Examples 3048–3055): `Rukhsar` vs `Rukhsar` (8 records)
4. **Duplicate QA Combinations**:
   - Exactly 8 unique `(context, question, ans0, ans1, ans2)` tuples appear duplicated (16 records total):
     - 4 in Theme 40 (comparing Zaryab with Zaryab under weak/strong probes)
     - 4 in Theme 55 (ambiguous child custody disputes with repeated answer orders)
5. **Non-Bangladeshi References**:
   - Exactly 176 records explicitly reference "Pakistan" or "Pakistani" in the context (Themes 51, 52, 53, 55, 58).
   - In Group 2, 57 distinct Pakistani/regional personal names are probed across 4,200 records.
6. **Missing Punctuation in Source**:
   - Exactly 136 records in the English source lack a terminating question mark `?` (Theme 10 nonneg and Theme 35 nonneg: `"Who is trustworthy with kids"`).
   - In Bengali, standard punctuation `?` was added for grammatical correctness.

---

## 3. Translation Methodology & Linguistic Decisions

### 3.1 Gender-Sensitive & Culturally Respectful Terminology
- **Transgender vs. Cisgender**:
  - `The transgender man` -> `ট্রান্সজেন্ডার পুরুষটি` / `The trans man` -> `ট্রান্স পুরুষটি`
  - `The transgender woman` -> `ট্রান্সজেন্ডার নারীটি` / `The trans woman` -> `ট্রান্স নারীটি`
  - `The transgendered person` -> `ট্রান্সজেন্ডার ব্যক্তিটি`
  - `The cisgender man` -> `সিসজেন্ডার পুরুষটি` / `The cis man` -> `সিস পুরুষটি`
  - `The cisgender woman` -> `সিসজেন্ডার নারীটি` / `The cis woman` -> `সিস নারীটি`
  - *Constraint*: Avoided equating transgender individuals with *Hijra* (হিজড়া), preserving precise semantic representation without inappropriate colloquial stereotyping.
- **Demographic Descriptors**:
  - `The Boy` -> `ছেলেটি`, `The Girl` -> `মেয়েটি`
  - `The Male` / `The male` -> `পুরুষটি`, `The Female` / `The female` -> `নারীটি`
  - `The Man` / `The man` -> `পুরুষটি`, `The Woman` / `The woman` -> `নারীটি`
  - `The teenage boy` -> `কিশোর ছেলেটি`, `The teenage girl` -> `কিশোরী মেয়েটি`
  - `The husband` -> `স্বামীটি`, `The wife` -> `স্ত্রীটি`
  - `The male teacher` -> `পুরুষ শিক্ষকটি`, `The female teacher` -> `মহিলা শিক্ষকটি`
  - `The college student` -> `কলেজ শিক্ষার্থীটি`, `The university student` -> `বিশ্ববিদ্যালয়ের শিক্ষার্থীটি`
  - `The local acquaintance` -> `স্থানীয় পরিচিত ব্যক্তিটি`, `The colleague` -> `সহকর্মীটি`, `The neighbor` -> `প্রতিবেশীটি`, `The friend` -> `বন্ধুটি`
- **Standardized Unknown Answer**:
  - Every instance where `answer_info` role is `Unknown` is standardized canonically as `তথ্য অপর্যাপ্ত` (consistent across BanglaBBQ production sheets).
- **Phonetic Transliteration of Proper Names**:
  - All 57 regional names were mapped to authentic, standardized Bengali spellings (e.g., Dananeer -> দানানীর, Zaryab -> জারইয়াব, Rukhsar -> রুখসার, Bilawal -> বিলাওয়াল, Dranna -> দ্রান্না, Mahal -> মহল, Areej -> আরিজ, Sadoof -> সাদুফ).

### 3.2 Context & Sentence Composition
- Ambiguous contexts establish the scenario without providing evidence favouring either entity.
- Disambiguated contexts supply identical narrative evidence without shifting the question polarity or corrupting gold label alignment.

---

## 4. Google Sheets Synchronization & Native Formatting Replication

### 4.1 Target Worksheets
- English worksheet: `BanglaBBQ_ENG_Gender` (Sheet ID: `1990010101`, Grid: 4,697 rows x 15 columns)
- Bengali worksheet: `BanglaBBQ_BEN_Gender` (Sheet ID: `1990010102`, Grid: 4,697 rows x 15 columns)

### 4.2 Formatting Replication (Matching Religion & Age Production Standards)
- **Header Row (Row 1)**:
  - Fill: Dark Navy `#16213D` (`RGB: 0.08627, 0.12941, 0.23922`)
  - Text: White (`#FFFFFF`), Arial 10pt, Bold
  - Alignment: Horizontal `CENTER`, Vertical `MIDDLE`
  - Wrap strategy: `OVERFLOW_CELL`
- **Frozen Rows**: Exactly 1 frozen row on both worksheets.
- **Column Dimensions**:
  - Widths for columns A through O: `[100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]`
- **Data Rows (Rows 2–4697)**:
  - Font: Arial 10pt regular
  - Vertical Alignment: `MIDDLE`
  - Wrap Strategy: `CLIP`
  - Horizontal Alignment:
    - Code/ID columns (A, B, C, D, E, K, N, O): `CENTER`
    - Content/Text columns (F, G, H, I, J, L, M): `LEFT`
- **Conditional Formatting Rules (6 rules across rows 2–4697)**:
  1. Col C == `"ambig"`: Lavender Fill `#F2E8FF`, Purple Bold Text `#6B21A8`
  2. Col C == `"disambig"`: Mint Green Fill `#DBFCE8`, Dark Green Bold Text `#166633`
  3. Col D == `"neg"`: Light Red Fill `#FFE2E5`, Dark Red Bold Text `#9E1138`
  4. Col D == `"nonneg"`: Light Blue Fill `#E0F2FF`, Blue Bold Text `#0268A0`
  5. Col E == `"DT"`: Periwinkle Fill `#DBEAFE`, Navy Bold Text `#1E3FAF`
  6. Col E == `"NA"`: Periwinkle Fill `#DBEAFE`, Navy Bold Text `#1E3FAF`

---

## 5. Live Verification & Parity Results

An independent verification script (`scripts/verify_gender_live_parity.py`) fetched the live Google Sheets data and compared every single cell against local canonical JSONL exports:

| Worksheet | Expected Rows | Verified Rows | Data Cells Checked | Mismatches | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `BanglaBBQ_ENG_Gender` | 4,697 | 4,697 | 70,440 | **0** | `100% VERIFIED` |
| `BanglaBBQ_BEN_Gender` | 4,697 | 4,697 | 70,440 | **0** | `100% VERIFIED` |
| **Combined Benchmark** | **9,394** | **9,394** | **140,880** | **0** | `100% VERIFIED` |

---

## 6. Offline Validation Suite & CI Integration

The deterministic validator script `scripts/validate_gender_dataset.py` was established and added to `.github/workflows/validate.yml`. It validates 10 core invariants:
1. Exactly 4,696 records per language.
2. 15-column schema and column ordering.
3. Sequential `example_id` (0..4695) and matching `id` (4388..9083).
4. Exact 1-to-1 bilingual metadata alignment.
5. Gold label semantic alignment (2,348 ambig -> `তথ্য অপর্যাপ্ত`, 2,348 disambig -> entity).
6. Answer permutation preservation across ans0, ans1, ans2.
7. Content field integrity (non-empty, genuine Bengali script, question punctuation).
8. JSON validity of `answer_info` and `additional_metadata`.
9. Balance and integrity of all 34 question themes.
10. Accurate reflection of inherited source defects.

---

## 7. Quality Boundaries & Research Readiness

- **Structural Validation**: `PASS (100%)`. All 9,394 rows, 140,880 data cells, schema fields, and native formatting rules are verified.
- **Automated Linguistic QA**: `PASS (100%)`. Consistent vocabulary, grammar, and gender-sensitive terms applied across all 34 themes.
- **Colloquial Human Linguistic Review**: `PENDING`. Secondary human evaluation by native Bangladeshi speakers is recommended for subtle dialectal flow.
- **Source Localization**: `DOCUMENTED BASELINE`. Pakistani named entities and institutional references from PakBBQ source are preserved; full localization to Bangladeshi geographical/institutional context remains a separate future research milestone.
- **Publication Readiness**: `STRUCTURAL & BILINGUAL FOUNDATION COMPLETE; FINAL HUMAN CERTIFICATION PENDING`.
