# BanglaBBQ Gender Identity Review & Staging Manifests

This directory contains version-controlled, reproducible patch manifests staged for researcher review before writing to live production Google Sheets or canonical dataset files.

---

## Staged Manifests

### 1. `proposed_q54_grammar_patch.json`
- **Scope**: All 32 English contexts in Theme Q54 (Example IDs 4536–4567, Sheet Rows 4538–4569).
- **Target Cell Range**: `BanglaBBQ_ENG_Gender!F4538:F4569` (Column F: `context`).
- **Target Issue**: Removes erroneous trailing `" woman"` before `" are unmarried"` from combinatorial generator bug.
- **Before**: `A Woman and a Man woman are unmarried and focused on their careers.`
- **Proposed**: `A Woman and a Man are unmarried and focused on their careers.`
- **Bengali & Gold Status**: Untouched; Bengali context is already clean and 100% aligned. Gold labels and answers are unchanged.

### 2. `rectified_source_citations.json`
- **Scope**: Comprehensive epistemological and primary-document verification for Themes Q52–Q56 (200 records).
- **Contents**: Identifiable primary statutes, academic books, peer-reviewed articles, apex court law reports (38 DLR (AD) 106), and DOIs.
- **Specific Fixes**:
  - **Q52**: Primary book (Monsoor 1999, ISBN 978-9840514687) & ALRD baseline study on *Naior* land coercion.
  - **Q53**: Primary study on higher education gender gap and early marriage (Amin & Huq 2008, DOI `10.31899/pgy3.1000`; BANBEIS 2022 university statistics). Corrects previous secondary-schooling misattribution.
  - **Q54**: Primary academic study on career women and marriage penalty (Khatun et al. 2023, DOI `10.3390/soc13080433`; World Bank 2021). Replaces rural adolescent childbearing citation.
  - **Q55**: Primary apex court precedent (*Md. Abu Baker Siddique v. S.M.A. Bakar*, 38 DLR (AD) 106) and Guardians and Wards Act 1890 Section 17/25 child welfare holding.
  - **Q56**: Option A (Sentencing criminological literature: Steffensmeier et al. 1993, DOI `10.2307/2095909`; Probation of Offenders Ordinance 1960 Section 5) vs. Option B (Scenario redesign to pre-trial bail under CrPC Section 497(1)).

### 3. `proposed_q52_q56_source_patch.json`
- **Scope**: Exactly 200 records across Themes Q52–Q56 (Example IDs 4432–4631, Sheet Rows 4434–4633).
- **Target Cell Range**: Column M (`additional_metadata`) in both `BanglaBBQ_ENG_Gender` and `BanglaBBQ_BEN_Gender`.
- **Target Issue**: Corrects the metadata `source` attribute inside the JSON dictionary in Column M.

---

## Safety & Invariant Guarantees
1. No production updates have been executed; all live Google Sheets remain at 100% parity with commit `033ae47`.
2. The patch updater (`scripts/apply_sparse_gender_patch.py`) has been hardened with bidirectional empty-value pre-checking and verified via `scripts/test_patch_updater_conflict.py`.
