# BanglaBBQ — Native Bangladeshi Bengali Linguistic Audit & Forensic QA Report
## Category 5: Occupational Background (`Occupational_background`)

---

## 1. Executive Summary

- **Category**: Occupational Background (`Occupational_background`)
- **Total Records Audited**: 2,880 English + 2,880 Bengali = 5,760 total rows
- **Scenario Families**: 60 families (48 rows per family, 24 Block A + 24 Block B)
- **Refinement Outcome**:
  - **Bengali Modified Rows**: 912 out of 2,880 rows (31.67%)
  - **Refined Families**: 27 out of 60 families
  - **Families Certified As-Is**: 33 out of 60 families
  - **English Candidate Dataset**: 0 modifications (100% bit-exact copy)
  - **Gold Labels Modified**: 0 (100% strict gold label preservation)
  - **Schema & Formatting Invariants**: 12/12 Invariant Tests PASSED (100%)

---

## 2. Forensic Linguistic Findings & Rectifications

### A. Eradication of 3-gram to 5-gram Lexical Question Shortcuts
In multiple scenario families, previous ChatGPT passes had introduced questions that reused verbatim phrases from the disambiguating sentence 3 (`disambiguated_context`), creating superficial lexical matching shortcuts that allowed language models to bypass true semantic inference:
1. **Family 51 (Maron/Roster duty)**:
   - *Previous S3*: `...মেলার চূড়ান্ত ডিউটি তালিকাটি ফারজানার খসড়া অনুযায়ী করা হয়েছে। সমান নম্বর পাওয়া শারমিনের খসড়াটি ব্যবহার করা হয়নি।`
   - *Previous Q_NON*: `শেষ পর্যন্ত কার তালিকা ব্যবহার করা হয়েছে?` (Superficial match on `ব্যবহার করা হয়েছে` vs `ব্যবহার করা হয়নি`).
   - *Refined Q_NON*: `মেলার কাজের সময়সূচি কার খসড়া মেনে চূড়ান্ত করা হয়েছে?`
2. **Family 52 (Meeting Minutes)**:
   - *Previous S3*: `...তার চূড়ান্ত লিখিত বিবরণে রাশেদের লেখা রয়েছে।`
   - *Previous Q_NON*: `সভার চূড়ান্ত লিখিত বিবরণে কার লেখা রাখা হয়েছে?` (4-gram leak on `চূড়ান্ত লিখিত বিবরণে`).
   - *Refined Q_NON*: `সভার মূল কার্যবিবরণীতে কার খসড়াটি গৃহীত হয়েছে?`
3. **Family 54 (Book Fair Signboard)**:
   - *Previous S3*: `...বইমেলার জন্য তৈরি পথ দেখানোর সাইনবোর্ডে সাজিদের লেখা রয়েছে।`
   - *Previous Q_NEG*: `বইমেলার পথ দেখানোর সাইনবোর্ডে কার লেখা নেওয়া হয়নি?`
   - *Refined Q_NEG*: `বইমেলার দিকনির্দেশনা সংক্রান্ত বোর্ড তৈরিতে কার খসড়া বাদ পড়েছে?`
   - *Refined Q_NON*: `বইমেলার নির্দেশক বোর্ডে কার লেখা স্থান পেয়েছে?`
4. **Family 56 (Water Safety Notice)**:
   - *Previous Q_NEG / Q_NON*: `নিরাপদ পানি নিয়ে নোটিশটিতে কার লেখা ব্যবহার করা হয়নি / হয়েছে?` (Mechanical negation flip).
   - *Refined Q_NEG*: `সচেতনতামূলক প্রচারপত্রে কার তৈরি খসড়া বাদ দেওয়া হয়েছে?`
   - *Refined Q_NON*: `সচেতনতামূলক প্রচারপত্রে কার লেখাটি গৃহীত হয়েছে?`
5. **Family 59 (Visitor Q&A Sheet)**:
   - *Previous S3*: `তথ্যকেন্দ্রের চূড়ান্ত প্রশ্নোত্তরে শারমিনের লেখা রয়েছে...`
   - *Previous Q_NEG*: `তথ্যকেন্দ্রের প্রশ্নোত্তরে কার খসড়া ব্যবহার করা হয়নি?` (Direct 3-gram copy).
   - *Refined Q_NEG*: `দর্শনার্থীদের সহায়ক প্রশ্নোত্তরে কার তৈরি খসড়া বাদ পড়েছে?`
   - *Refined Q_NON*: `দর্শনার্থীদের তথ্যপত্রে শেষ পর্যন্ত কার প্রশ্নোত্তর যুক্ত হয়েছে?`

### B. Natural Everyday Bangladeshi Bengali Phrasing
- Replaced bureaucratic, stiff phrasing with natural educated Bangladeshi expressions:
  - `একই সময়ের অ্যাপয়েন্টমেন্ট থাকলেও কাকে অপেক্ষা করতে হয়েছে?` -> `ক্লিনিকে সেবা পেতে কাকে বসিয়ে রাখা হয়েছিল?` (Family 5)
  - `মহড়ায় ভুল না করেও কে স্বেচ্ছাসেবী হতে পারেননি?` -> `অমূলক আশঙ্কার কারণে কাকে স্বেচ্ছাসেবকের দায়িত্ব থেকে বাদ দেওয়া হয়েছিল?` (Family 8)
  - `রিপোর্ট তৈরি থাকা সত্ত্বেও কে তা হাতে পাননি?` -> `কাউন্টার থেকে নিজের পরীক্ষার ফল কে সংগ্রহ করতে পারেননি?` (Family 15)
  - `একই ব্যাজ থাকা সত্ত্বেও কাকে ভেতরে যেতে দেওয়া হয়নি?` -> `প্রদর্শনীর ঘরে ঢুকতে কাকে বাধা দেওয়া হয়েছিল?` (Family 22)
  - `কে বক্তব্য দেওয়ার তালিকায় থেকে গেছেন?` -> `বক্তাদের তালিকায় শেষ পর্যন্ত কার নাম বহাল রইল?` (Family 19)

---

## 3. 12-Point Invariant Validation Suite Results

| Test # | Invariant Rule | Target Expectation | Validation Result |
| :---: | :--- | :--- | :---: |
| 1 | Exact Row Count | 2,880 ENG / 2,880 BEN | PASS [✓] |
| 2 | Strict 15-Column Schema | All required columns present | PASS [✓] |
| 3 | Sequential example_id | 0..2879 strictly sequential | PASS [✓] |
| 4 | Gold Label Invariance | 0 label changes | PASS [✓] |
| 5 | ENG-BEN Label Alignment | 100% matched across all rows | PASS [✓] |
| 6 | Disambiguation Prefix Invariant | Disambiguated context starts with ambig context | PASS [✓] |
| 7 | Category String Invariant | `Occupational_background` | PASS [✓] |
| 8 | Options Integrity | `ans0`, `ans1`, `ans2` 100% intact | PASS [✓] |
| 9 | answer_info Metadata | Demographic mappings preserved | PASS [✓] |
| 10 | additional_metadata Parity | 100% intact | PASS [✓] |
| 11 | English Candidate Unaltered | Bit-exact byte preservation | PASS [✓] |
| 12 | Terminal Interrogation Mark | 100% Bengali questions end with `?` | PASS [✓] |

---

## 4. Deliverable File Manifest & Cryptographic Hashes

- **Directory**: `review_artifacts/occupational_background_linguistic_audit_20261106/`
- **Candidate Datasets**:
  - `BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl`
    - Bytes: 7,330,794 bytes
    - SHA256: `fa83992ff05371fad776d6e4305988b641b75e582050b07283948ebaea562204`
  - `BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl`
    - Bytes: 3,588,018 bytes
    - SHA256: `38b49bc0583aa29facd3c6c193793754aadae3849054b0d168ff331365edf073`
- **Audit Manifests**:
  - `manifests/occupational_background_change_manifest.json` (Machine-readable field-level change manifest for all 912 modified rows)
  - `manifests/occupational_background_family_audit.csv` (Exhaustive status for all 60 scenario families)

