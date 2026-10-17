# Research Log: Politics Q5, Q14, and Q19 Approved Content Fixes & Bilingual Synchronization

**Date**: 2026-10-17  
**Category**: Politics (Q5, Q14, Q19)  
**Status**: `VERIFIED COMPLETE` (Structurally validated, synchronized across Google Sheets and GitHub; linguistic and source audits remain outstanding)  
**Authors/Collaborators**: Hasin Ishrak (Researcher), ChatGPT (Live Sheets Editor), Antigravity (Local Synchronization & Verification Agent)  

---

## 1. Executive Summary & Scope

Following the 2,880-record bilingual expansion of the BanglaBBQ Politics benchmark (20 themes x 3 wording versions x 48 answer-permutation examples), a preliminary quality review identified three localized content issues across themes Q5, Q14, and Q19.

The researcher explicitly authorized three targeted corrections:
1. **Q5 Historical Year 2022 Qualification**: Adding temporal qualification (year 2022) to avoid presenting historical legal/political micro-scenarios as ungrounded timeless assertions.
2. **Q14 Entailment & Premise Refinement**: Amending the negative question text to ask whose belongings were forcibly thrown out of the dormitory, eliminating an unsubstantiated premise of formal university expulsion.
3. **Q19 Bengali Option & Context Terminology Alignment**: Standardizing Bengali context and answer-choice options from "সরকারবিরোধী" ("anti-government") to "সরকার-সমালোচক" ("government critic") to ensure precise semantic correspondence with English and contemporary journalistic usage.

ChatGPT applied and verified these repairs directly in the active production tabs of the master Google Spreadsheet (`BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`). The remote Git repair branch (`fix/politics-q5-q14-q19-20261017`) successfully synchronized English canonical JSONL but stalled on Bengali JSONL due to connector timeouts. This operation completed the local synchronization, reconciled the Politics validator and expansion assembler assumptions, preserved historical baselines and backups, verified 100% bit-for-bit parity against live Google Sheets, and merged the validated changes into `main`.

---

## 2. Preservation & Audit Lineage

To ensure scientific reproducibility and audit preservation:
- **Pre-Fix Git Branch**: `backup/politics-pre-q5-q14-q19-fixes-20261017` at commit `6a1462f306ecad7198f8c795df73761e16e9c583`.
- **Pre-Fix Google Sheets Snapshots**: Hidden backup worksheets `Backup_Politics_ENG_preQAfix_20261017` (gid `1744544726`) and `Backup_Politics_BEN_preQAfix_20261017` (gid `1886409399`).
- **Pre-Expansion 960-Record Snapshots**: `backups/politics_pre_wording_v2v3_20261017/banglabbq_politics_english_960.jsonl` and `banglabbq_politics_bengali_960.jsonl` preserved byte-for-byte without modification.
- **Original Seniors' Thesis Baseline**: `Dataset_ BanglaBBQ_Old/Politics/` preserved byte-for-byte without modification.
- **Unrelated Records**: Zero modifications to categories outside of Politics (Age, Religion, and all legacy baseline files remain untouched).

---

## 3. Detailed Description of Changes

### A. Politics Q5 (Historical Year 2022 Qualification)
- **Affected Rows**: 144 records per language.
  - V1 (Original): Rows 192–239 (48 records)
  - V2: Rows 1344–1391 (48 records)
  - V3: Rows 1392–1439 (48 records)
- **English Context Phrasing**:
  - Prefixed with `"In Bangladesh in 2022, "` (or `"In 2022, "` depending on clause syntax).
- **Bengali Context Phrasing**:
  - Prefixed with `"২০২২ সালে "`.
- **Unchanged Fields**: All IDs, labels, polarities, conditions, questions, answer options, and metadata remain untouched.

### B. Politics Q14 (Negative Question Entailment Refinement)
- **Affected Rows**: 72 records per language (negative polarity only across all 3 wording versions).
  - V1: Rows 624–647, 672–695 (negative polarity rows)
  - V2/V3: Corresponding negative polarity rows in theme 14 (Rows 2208–2231, 2256–2279, etc.).
- **English Question Change**:
  - Old: *"Whose belonging were forcibly thrown out of the dormitory after university expulsion?"* (or similar premise-laden phrasing)
  - New: `"Whose belongings were forcibly thrown out of the dormitory?"`
- **Bengali Question Change**:
  - New: `"কার জিনিসপত্র জোর করে আবাসিক হলের বাইরে ফেলে দেওয়া হয়েছিল?"` / `"কার জিনিসপত্র জোর করে আবাসিক হলের বাইরে ফেলে দেওয়া হয়েছিল?"`
- **Rationale**: Removes the unsubstantiated premise of formal expulsion, aligning question directly with factual scenario evidence.

### C. Politics Q19 (Bengali Terminology Alignment)
- **Affected Rows**: 144 records total in Bengali.
  - Context: 48 V1 rows (Rows 864–911) updated from `"সরকারবিরোধীর"` -> `"সরকার-সমালোচকের"` and `"সরকারবিরোধী"` -> `"সরকার-সমালোচক"` (V2/V3 contexts already used critic terminology).
  - Answer Options: All 144 Bengali records (Rows 864–911, 2688–2783) had their answer option containing the target phrase updated across `ans0`, `ans1`, and `ans2`:
    - Old: `"বিদেশে থাকা সরকারবিরোধীর পরিবার"`
    - New: `"বিদেশে থাকা সরকার-সমালোচকের পরিবার"`
- **Rationale**: Aligns Bengali phrasing with English ("government critic") and eliminates conflation between legitimate political criticism and militant/anti-state opposition.

---

## 4. Validator & Expansion Assembler Harmonization

### A. Dual Hash Preservation in `scripts/validate_politics_dataset.py`
Because Check 10 evaluates `recs[:240]`, the modification of Q5 (Rows 192–239) altered the SHA-256 hash of the initial 240 records:
- **Historical Baseline Pre-Repair Hashes** (preserved as evidence for legacy datasets and historical audits):
  - English: `2ab59aec0cb6f6ce42f60e8912c861373b96008db8dec2af281046def64595b3`
  - Bengali: `eb6ae51a7b0d4d739243c995e23e5e7a6a55dc895c4a791975dbb18c50d4fc23`
- **Approved Post-Repair Hashes** (for active canonical dataset reflecting Q5 historical qualification):
  - English: `7390c9ed9d008dc2c0e937ecab545e9d2521fbdb8b44b0adab2b9d218180c51a`
  - Bengali: `e30d2b1d8085f6f01ed95e12548ea466aac8cef6317b8c0a678fe4c10c32eda6`
- **Implementation**: The validator now supports both valid sets of hashes, distinguishing `Historical Baseline` from `Approved Post-Q5 Repair`.

### B. Assembler Harmonization in `scripts/assemble_politics_expansion.py`
- Added cross-platform CRLF normalization (`replace(b'\r\n', b'\n')`) when calculating Git blob hashes on Windows environments.
- Recognized the verified post-repair canonical records as an authorized state, avoiding destructive overwrites or assertion crashes when running expansion verification.

---

## 5. Verification Results

All 11 automated invariant checks were executed and confirmed:

```
====================================================================
COMPREHENSIVE OFFLINE VALIDATION: BANGLABBQ POLITICS BENCHMARK
====================================================================
--- Check 1: Record Counts ---
  ENG count: 2880 (PASS)
  BEN count: 2880 (PASS)

--- Check 2: Sequential IDs & Schema ---
  Sequential IDs (0-2879): PASS
  15-Column Schema Integrity: PASS

--- Check 3: Theme Counts & Condition Balances (144 per theme) ---
  All 20 Themes 144 records with 72/72 condition & polarity balances: PASS

--- Check 4: Canonical 4-row Block Ordering ---
  Canonical 4-row BBQ Block Sequence throughout all expected rows: PASS

--- Check 5: Label Distribution & Permutations ---
  Uniform Label Distribution (960 each): PASS

--- Check 6: Ambiguous Context Invariant (Must be Unknown) ---
  All expected Ambiguous QA pairs correctly target Unknown/অজানা: PASS

--- Check 7: Disambiguated Semantic Ground Truth & Counterfactual Inversion ---
  All expected Disambiguated QA pairs logically proven by contextual ground truth: PASS

--- Check 8: Bilingual Structural Equality & Metadata Parity ---
  100% Bilingual Equality across all 10 structural/metadata fields: PASS

--- Check 9: Duplicate QA Records Check ---
  Zero Duplicate QA Records (2880/2880 completely unique tuples): PASS

--- Check 10: Q1-Q5 Hash Preservation ---
  Q1-Q5 ENG SHA-256: 7390c9ed9d008dc2c0e937ecab545e9d2521fbdb8b44b0adab2b9d218180c51a (PASS - Approved Post-Q5 Repair)
  Q1-Q5 BEN SHA-256: e30d2b1d8085f6f01ed95e12548ea466aac8cef6317b8c0a678fe4c10c32eda6 (PASS - Approved Post-Q5 Repair)

--- Check 11: V2/V3 Wording Expansion Audit ---
  40 x 48-row bilingual variants, metadata lineage, and 6-way permutations: PASS

====================================================================
ALL COMPREHENSIVE BENCHMARK INVARIANT CHECKS PASSED!
====================================================================
```

### Live Google Sheets Bit-for-Bit Parity:
A complete live read-back via Google Sheets API v4 comparing local canonical JSONL with sheets `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics` confirmed:
- **English discrepancies across 2,880 rows x 15 columns (43,200 cells)**: `0`
- **Bengali discrepancies across 2,880 rows x 15 columns (43,200 cells)**: `0`
- **Result**: `100% BIT-FOR-BIT PARITY CONFIRMED`.

---

## 6. Open Limitations & Publication Readiness

> [!WARNING]
> **NOT PUBLICATION-READY**: The benchmark has achieved automated structural integrity, schema conformity, and live-to-repository synchronization. However, independent native Bengali linguistic reviews, whole-benchmark translation naturalness audits, external source-relevance verifications, and evaluation leakage safeguards (grouping correlated paraphrases across train/eval splits) remain outstanding.

---
