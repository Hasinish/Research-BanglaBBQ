# state.md — Current Workspace State

## Active Goals & Todo
- [x] Cloned official PakBBQ repository into `PakBBQ_Repo`
- [x] Converted `PakBBQ_ENG/Age.jsonl` to clean Excel-ready CSV: `PakBBQ_Age_English.csv` (2,920 rows)
- [x] Successfully refreshed Google OAuth token and authenticated with Google Sheets API
- [x] Created executive color-coded 3-column review tab `Review_Age_20_Templates` (Tab Index 0) in Google Sheet for Provat Saha (Indigo for PakBBQ ENG, Amber/Rose for Legacy Thesis, Emerald for Hasin's New Translations).
- [x] Translated and verified all 2,920 rows of Templates 1 through 20 (Rows 0 to 2,919) into conversational Bengali in Tab 2 (`BanglaBBQ_BEN_Age`), with 100% mathematical invariant parity (zero leakage).
- [x] Exported production-ready, verified JSONL dataset to `BanglaBBQ_BEN/Age.jsonl` (2,920 entries).
- [x] Fully expanded Politics benchmark from 112 to 160 rows: expanded Q3, Q4, and Q5 to 32 rows each with complete entity order counterbalancing and answer rotations. Updated `Dataset_ BanglaBBQ_Old/Politics/` (English and Bengali JSONL) and synced live Google Sheet tabs `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics` (161 rows each).
- [x] Completed forensic audit and correction of family relationship terms in `BanglaBBQ_BEN_Age`: mapped Grandma -> নানি (24 rows) and Grandpa -> নানা (24 rows), eliminating all duplicate records in Q2 (from 8 to 0). Verified 100% parity across all 2,920 rows and synced to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Corrected Grandparent / Grandchild singular translations (56 rows) and Q7 comparative question mismatch (48 rows) in `BanglaBBQ_BEN_Age`. Live Google Sheets updated and synced to `BanglaBBQ_BEN_New/Age.jsonl` with 100% mathematical invariant parity.
- [x] Cleaned and organized all 43 research, migration, and audit scripts into a dedicated `scripts/` folder with a detailed index `scripts/README.md`.
- [x] Corrected and validated Politics benchmark: fixed 40 disambiguated gold labels strictly grounded in contextual evidence, eliminated probability wording across Q1-Q5, removed 40 exact duplicates, re-indexed 120 unique records sequentially (0-119), updated Google Sheets tabs (`BanglaBBQ_ENG_Politics`, `BanglaBBQ_BEN_Politics`), and synced local JSONL files with 100% mathematical counterfactual parity.
- [x] Fully expanded, reorganized, and formatted Politics benchmark to 240 records: canonical 4-row BBQ block ordering throughout (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`) across all 6 answer permutations (3!) for both orientations in all 5 themes. Applied consistent styling (headers, alignments, text wrap, row heights, column widths, conditional formatting) across the entire A1:O241 range in Google Sheets and local JSONL.
- [x] Restored exact visual replication of Age formatting on both Politics sheets (`BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`): applied direct `copyPaste` with `PASTE_FORMAT` from Age sheets across header A1:O1 and all sixty 4-row blocks A2:O241. Replicated column widths, restored all 5 canonical conditional format rules (Col C ambig/disambig, Col D neg/nonneg, Col E NA light blue), and set row heights (Header 28px, Ambig 42px, Disambig 88px) so multi-line wrapped text displays with complete vertical clarity and zero truncation.
- [x] Successfully expanded Politics benchmark from 5 to 20 source-backed themes (Q1–Q20): preserved Q1–Q5 100% unchanged, added 15 new themes (Q6–Q20) with 48 records each across 2 counterfactual orientations, 4 conditions, and all 6 answer permutations (3!). Total 960 records per language (IDs 0–959) written to live Google Sheets and local JSONL with 0 duplicates, 0 label errors, 100% bilingual parity, and full Age styling replication across rows 1–961.
- [x] Initialized Git repository and pushed initial commit (878c75b) containing Age (2,920 rows) and Politics 20 themes (960 rows) to https://github.com/Hasinish/Research-BanglaBBQ.git
- [x] Un-ignored and pushed full `PakBBQ_Repo` baseline (150+ files, 133MB, evaluation pipelines, analysis results, and datasets) in commit `bd18ed4` while keeping Google credentials (`token.json`) protected.
- [x] Completed end-to-end audit, repair, validation, and live synchronization of Politics benchmark: aligned 720 Bengali `answer_info` records to English canonical identities, corrected Bengali administrative translations (Q6, Q10, Q16, Q18), updated source URLs (Q6 HRW, Q13 CPJ), built comprehensive 10-invariant offline test suite (`scripts/validate_politics_dataset.py`), added GitHub Actions CI (`.github/workflows/validate.yml`), authored `CITATION.cff`, updated `README.md` and relative links in `scripts/README.md`, synchronized Google Sheets tabs, and verified 100% parity with untouched Q1-Q5 and Age tabs.
- [ ] Receive evaluation / SafeLLM pipeline code link promised tomorrow by team member

## Last Session (Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd)
- Created full workspace memory infrastructure (`personality.md`, `personal_info.md`, `purpose.md`, `state.md`, `history.md`, `index.md`).
- Senior brother identified as Provat Saha (BRACU CSE, author on T2510616).
- Task specified: Provat requested direct translation of `PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl` into Bengali.
- Cloned `Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA` to [`PakBBQ_Repo`](file:///d:/Research%20BanglaBBQ/PakBBQ_Repo).
- Deep analysis completed on `PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl`:
  - Exactly 2,920 rows: 1,872 DT (Directly Translated BBQ) and 1,048 TM (Target Modified).
  - Perfectly balanced: 1,460 ambig / 1,460 disambig, 1,460 neg / 1,460 nonneg, 1,460 unique contexts (2 QA pairs per context), and only 37 unique questions (22 in DT, 16 in TM).
  - Legacy thesis translation in `Dataset_ BanglaBBQ_Old/BBQ/BanBBQ_BEN/Age.jsonl` only contains rows 0-798 (799 samples). Rows 799-2919 (2,121 samples) remain untranslated.
  - Critical discovery: TM samples contain Pakistani cultural entities (Imtiaz supermarket, Indrive, Jalal Sons, Karachi, Lahore). Direct translation without Bangladeshi localization (Swapno, Pathao, Dhaka) will undermine the paper's claim of Bangladeshi socio-cultural grounding.
- Full forensic audit on `Dataset_ BanglaBBQ_Old` for Age completed:
  - All 5 Age files in the repo are duplicates of just 3 base files: full 2,920 PakBBQ English, 799 truncated English slice, and 799 Bengali translated slice.
  - File named `Age_Bengali_800entries.jsonl` contains only 799 entries (identical SHA to `BBQ/BanBBQ_BEN/Age.jsonl`).
  - Bengali translation method evaluated: literal Google Translate style with English digits ("58 বছর বয়সী-এর") and transliterations ("জুমারটি", "জেন-এক্সারটি").
  - Discovered syntax errors in legacy combined files: `banbbq_ben_combined.jsonl` has 101 broken JSON lines, and `Banglabbq/banglabbq_ben_combined.jsonl` has 29 broken JSON lines.

## Current Blockers & Notes
- Translation execution on hold per Hasin's instruction ("dont do it now").
- Need to flag to Provat that 799 samples are ALREADY translated in their legacy folder, and whether to localize Pakistani entities in TM samples (1,872-2,919) to Bangladeshi equivalents.
- Team member promised existing pipeline codebase tomorrow.
