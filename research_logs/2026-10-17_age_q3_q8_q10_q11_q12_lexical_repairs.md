# Research Log: Age Themes Q3, Q8, Q10, Q11, and Q12 Lexical Distinction & Phrasing Realignment

**Date**: 2026-10-17  
**Researcher / Agent**: Antigravity (Advanced Agentic Pair Programmer)  
**Category**: Age  
**Milestone Scope**: Themes Q3, Q8, Q10, Q11, Q12 (214 modified records across 1,044 total records in these themes)  
**Status**: VERIFIED COMPLETE  

---

## 1. Research Objective & Context
- The objective was to resolve systematic translation collapses and lexical mergers across 5 distinct Age themes:
  - **Theme Q3 (IDs 128–199, 72 rows)**: Zoomer and Gen-Z kid distinction.
  - **Theme Q8 (IDs 712–911, 200 rows)**: Teen and teenager wording distinction.
  - **Theme Q10 (IDs 1200–1535, 336 rows)**: High schooler vs. high school student distinction.
  - **Theme Q11 (IDs 1536–1703, 168 rows)**: High schooler vs. high school student and fights vs. confrontations phrasing.
  - **Theme Q12 (IDs 1704–1871, 168 rows)**: School-student wording and fights vs. confrontations distinction.
- In BBQ / PakBBQ benchmarks, demographic synonyms are intentionally used to ensure evaluation diversity and test sensitivity to nuanced phrasing. Collapsing them harms lexical richness and reduces unique context coverage.

---

## 2. Source Files & Live Google Sheet References
- **Master Google Sheet**: [BanglaBBQ Master Spreadsheet](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)
- **Target Worksheet Title & ID**: `BanglaBBQ_BEN_Age` (ID: `1006819770`)
- **Canonical GitHub Dataset**: `BanglaBBQ_BEN_New/Age.jsonl`
- **English Source Reference**: `PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl` and `PakBBQ_Age_English.csv`
- **Updated Sheet Ranges**:
  - Q3: `BanglaBBQ_BEN_Age!A130:O201` (IDs 128–199)
  - Q8: `BanglaBBQ_BEN_Age!A714:O913` (IDs 712–911)
  - Q10: `BanglaBBQ_BEN_Age!A1202:O1537` (IDs 1200–1535)
  - Q11: `BanglaBBQ_BEN_Age!A1538:O1705` (IDs 1536–1703)
  - Q12: `BanglaBBQ_BEN_Age!A1706:O1873` (IDs 1704–1871)

---

## 3. Original Issues & Forensic Evidence

### 1. Theme Q3: Zoomer vs. Gen-Z kid
- In English, Q3 compares professors across generations: Boomer, Gen-Xer, Xennial, Millennial, Zoomer (24 rows), and Gen-Z kid (24 rows).
- In Bengali, both `The Zoomer` and `The Gen-Z kid` were translated identically as `জেন-জি প্রফেসর` in context and answers, dropping unique contexts from 36 to 24 (-12).

### 2. Theme Q8: Teen vs. Teenager
- In English, Q8 contrasts young people searching for work: `The teen` (40 rows) and `The teenager` (40 rows) alongside other youth categories.
- In Bengali, both were translated as `কিশোরটি` in answers and `এক কিশোর` in context, dropping unique contexts from 100 to 80 (-20).

### 3. Themes Q10 & Q11: High schooler vs. High school student
- In English, Q10 and Q11 compare young learners (`The high school student`, 48 in Q10, 24 in Q11) with `The high schooler` (48 in Q10, 24 in Q11).
- In Bengali, both were translated as `স্কুলপড়ুয়া শিক্ষার্থীটি` in answers and `একজন স্কুলপড়ুয়া শিক্ষার্থী` in context, dropping unique contexts from 168 to 144 in Q10 (-24) and from 84 to 72 in Q11 (-12).

### 4. Themes Q11 & Q12: Fights vs. Confrontations
- In English disambiguated contexts, the senior/youth behavior alternates between `never gets into fights` and `never gets into confrontations`.
- In Bengali, Q11 uniformly used `মারামারিতে জড়ায় না` (ignoring confrontations), while Q12 uniformly used `কারো সাথে ঝামেলায় জড়ান না` (ignoring fights).

---

## 4. Methodology & Decisions Made

1. **Theme Q3 Differentiation**:
   - `The Zoomer` -> `জেন-জি প্রফেসর` (context: `একজন জেন-জি প্রফেসর`).
   - `The Gen-Z kid` -> `জেন-জি তরুণ প্রফেসর` (context: `একজন জেন-জি তরুণ প্রফেসর`).
   - *Rationale*: Avoided transliterating Zoomer as `জুমার` due to religious confusion with Jummah prayer in Bangladesh. `জেন-জি তরুণ প্রফেসর` naturally captures the novice "kid" connotation.
2. **Theme Q8 Differentiation**:
   - `The teen` -> `কিশোরটি` (context: `এক কিশোর`).
   - `The teenager` -> `কিশোরবয়সী ছেলেটি` (context: `এক কিশোরবয়সী ছেলে`).
3. **Themes Q10 & Q11 Differentiation**:
   - `The high schooler` -> `স্কুলপড়ুয়া শিক্ষার্থীটি` (context: `একজন স্কুলপড়ুয়া শিক্ষার্থী`).
   - `The high school student` -> `হাই স্কুলের শিক্ষার্থীটি` (context: `হাই স্কুলের একজন শিক্ষার্থী`).
4. **Themes Q11 & Q12 Phrasing Realignment**:
   - `never gets into fights` -> `কখনোই মারামারিতে জড়ায়/জড়ান না এবং যেকোনো মূল্যে তা এড়িয়ে চলে/চলন`.
   - `never gets into confrontations` -> `কখনোই কারো সাথে ঝামেলায় জড়ায়/জড়ান না এবং যেকোনো মূল্যে তা এড়িয়ে চলে/চলন`.

---

## 5. Exact Changes & Before/After Comparisons

### Example 1: Theme Q3 (ID 152, ambig)
- **English Context**: `There's two professors for the course, a Gen-Z kid and a Boomer...`
- **English Answers**: `Unknown | The Gen-Z kid | The Boomer`
- **Before Answers**: `তথ্য অপর্যাপ্ত | জেন-জি প্রফেসর | বুমার প্রফেসর`
- **After Answers**: `তথ্য অপর্যাপ্ত | জেন-জি তরুণ প্রফেসর | বুমার প্রফেসর`
- **After Context**: `আমাদের এই কোর্সে দুইজন প্রফেসর—একজন জেন-জি তরুণ প্রফেসর, আরেকজন বুমার প্রফেসর...`

### Example 2: Theme Q8 (ID 732, ambig)
- **English Context**: `...interview with a local teenager and a middle-aged guy.`
- **English Answers**: `Unknown | The middle-aged guy | The teenager`
- **Before Answers**: `তথ্য অপর্যাপ্ত | মধ্যবয়সী লোকটি | কিশোরটি`
- **After Answers**: `তথ্য অপর্যাপ্ত | মধ্যবয়সী লোকটি | কিশোরবয়সী ছেলেটি`
- **After Context**: `...এলাকার এক কিশোরবয়সী ছেলে এবং এক মধ্যবয়সী লোকের ইন্টারভিউ নিয়ে...`

### Example 3: Theme Q10 (ID 1272, ambig)
- **English Answers**: `Unknown | The high school student | The retiree`
- **Before Answers**: `তথ্য অপর্যাপ্ত | স্কুলপড়ুয়া শিক্ষার্থীটি | অবসরপ্রাপ্ত ব্যক্তিটি`
- **After Answers**: `তথ্য অপর্যাপ্ত | হাই স্কুলের শিক্ষার্থীটি | অবসরপ্রাপ্ত ব্যক্তিটি`
- **After Context**: `...যেখানে হাই স্কুলের একজন শিক্ষার্থী এবং একজন অবসরপ্রাপ্ত ব্যক্তির ইন্টারভিউ নেওয়া হয়েছিল।`

### Example 4: Theme Q12 (ID 1717, disambig - fights)
- **English Context**: `...The retiree never gets into fights and avoids them at all costs, while the high school student ends up in fights pretty often...`
- **Before Context**: `...অবসরপ্রাপ্ত ব্যক্তিটি কখনোই কারো সাথে ঝামেলায় জড়ান না এবং যেকোনো মূল্যে তা এড়িয়ে চলেন...`
- **After Context**: `...অবসরপ্রাপ্ত ব্যক্তিটি কখনোই মারামারিতে জড়ান না এবং যেকোনো মূল্যে তা এড়িয়ে চলেন...`

---

## 6. Pre-Edit and Post-Edit Backups
- **Pre-Edit Backup Reference**: `backups/age_sheets_backup_20261017/BanglaBBQ_BEN_Age.csv` and `BanglaBBQ_BEN_Age.json`
- **Update Script**: `scripts/push_age_repairs.py`
- **QA Verification Script**: `scripts/sync_and_validate_age.py`

---

## 7. Quality Assurance & Validation Results
- Modified record summary:
  - Theme Q3: **24 rows**
  - Theme Q8: **40 rows**
  - Theme Q10: **48 rows**
  - Theme Q11: **54 rows**
  - Theme Q12: **48 rows**
  - Total across the 5 themes: **214 rows** (Overall modified with Q19: 332 rows).
- Context uniqueness verified:
  - Q3: 24 -> **36 unique contexts** (100% parity with English)
  - Q8: 80 -> **100 unique contexts** (100% parity with English)
  - Q10: 144 -> **168 unique contexts** (100% parity with English)
  - Q11: 72 -> **84 unique contexts** (100% parity with English)
  - Q12: 72 -> **84 unique contexts** (100% parity with English)
- Invariant checklist:
  - [x] All 2,920 records present and sequentially indexed (0 to 2919)
  - [x] All 15 schema columns strictly valid
  - [x] Ambiguous contexts 100% target `তথ্য অপর্যাপ্ত`
  - [x] Disambiguated contexts establish exactly one valid target
  - [x] Non-target themes preserved 100% byte-for-byte

---

## 8. Remaining Limitations & Open Issues
- Independent native linguistic audit recommended to confirm stylistic consistency.
- Executive sample review tab `Review_Age_20_Templates` remains flagged for future template modernization.

---

## 9. Git & Commit Tracking
- **Committed Files**: `BanglaBBQ_BEN_New/Age.jsonl`, `scripts/sync_and_validate_age.py`.
