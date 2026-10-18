# BanglaBBQ Gender Identity Review & Staging Manifests

This directory contains version-controlled, reproducible patch manifests staged for researcher review before writing to live production Google Sheets or canonical dataset files.

---

## Manifest Disposition & Verification Status

### 1. `proposed_q54_grammar_patch.json` — **APPROVED & APPLIED (2026-10-18)**
- **Scope**: All 32 English contexts in Theme Q54 (Example IDs 4536–4567, Sheet Rows 4538–4569).
- **Target Cell Range**: `BanglaBBQ_ENG_Gender!F4538:F4569` (Column F: `context`).
- **Correction**: Removed erroneous trailing `" woman"` before `" are unmarried"` resulting from the legacy combinatorial generator template defect.
- **Before**: `A Woman and a Man woman are unmarried and focused on their careers.`
- **Applied**: `A Woman and a Man are unmarried and focused on their careers.`
- **Verification**: Safely applied to live Google Sheet (`BanglaBBQ_ENG_Gender`) and canonical `BanglaBBQ_Gender/Gender_identity_eng.jsonl`. Verified 100% bit-for-bit live parity across all 140,910 cells (0 mismatches). Bengali contexts and gold labels untouched.

### 2. `proposed_q52_q56_source_patch.json` & `rectified_source_citations.json` — **REJECTED FOR PRODUCTION / HELD IN REVIEW (`SOURCE_UNVERIFIED`)**
- **Directive**: User explicitly ordered: **DO NOT apply the 200-row citation patch or either Q56 redesign**. Some citations are demonstrably misattributed or tangential.
- **Status**: Themes Q52–Q56 are officially designated **`SOURCE_UNVERIFIED`** in project memory, research logs, and repository indexes until primary evidence review is completed.
- **Production State**: Zero source cells in Column M (`additional_metadata`) were modified. No questionable or unverified references were injected into production.
- **Held Candidates for Future Review**:
  - **Q52**: Monsoor (1999) & ALRD baseline study on *Naior* land coercion.
  - **Q53**: Sourced candidates (Amin & Huq 2008 / BANBEIS 2022) held for evidence review regarding university drop-off vs. secondary schooling.
  - **Q54**: Khatun et al. (2023) marriage penalty on career women held for evidence review.
  - **Q55**: Landmark custody ruling (*Md. Abu Baker Siddique v. S.M.A. Bakar*, 38 DLR (AD) 106) held for evidence review.
  - **Q56**: Both Option A (sentencing chivalry literature) and Option B (bail statutory redesign under CrPC Section 497(1)) are **REJECTED** and withheld from production.

---

## Safety & Invariant Guarantees
1. Production integrity: Exactly 32 English context cells updated; 0 Bengali cells modified; 0 label/ID changes; 0 source changes.
2. The patch updater (`scripts/apply_sparse_gender_patch.py`) has been hardened with bidirectional empty-value pre-checking and verified via `scripts/test_patch_updater_conflict.py` (5/5 PASS).
3. Backups preserved: `Backup_BanglaBBQ_ENG_Gender_preRepair_20261018` (362662769), `Backup_BanglaBBQ_BEN_Gender_preRepair_20261018` (1183220937), and local git backups.
