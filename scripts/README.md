# BanglaBBQ Research & Automation Scripts

This directory houses all forensic analysis, data migration, validation, and Google Sheets automation scripts for the BanglaBBQ project.

---

## 1. Age Benchmark — Corrections & Migrations

- [`apply_p1_p2_corrections.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_p1_p2_corrections.py): Corrects Grandparent / Grandchild dual terms (`দাদা-দাদি` -> `দাদু`, `নাতি-নাতনি` -> `নাতিটি`) across 56 rows and restores Q7 negative comparative question ("কে তুলনামূলকভাবে কম সৃজনশীল ছিল?") across 48 rows. Updates both live Google Sheets (`BanglaBBQ_BEN_Age`) and local mirror (`BanglaBBQ_BEN_New/Age.jsonl`).
- [`apply_family_corrections.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_family_corrections.py): Applies project-standard convention for `Grandma` -> `নানি` (24 rows) and `Grandpa` -> `নানা` (24 rows) in `BanglaBBQ_BEN_Age`.
- [`test_fixes_simulation.py`](file:///d:/Research%20BanglaBBQ/scripts/test_fixes_simulation.py): Dry-run replacement logic simulator for Problem 1 (GP/GC) and Problem 2 (Q7) before live Sheets execution.
- [`test_replacement_logic.py`](file:///d:/Research%20BanglaBBQ/scripts/test_replacement_logic.py): Simulation script validating family relationship regex replacements and checking for term leaks.

---

## 2. Age Benchmark — Live Audits & Scanners

- [`audit_live_p1_p2.py`](file:///d:/Research%20BanglaBBQ/scripts/audit_live_p1_p2.py): End-to-end live verification of Google Sheet `BanglaBBQ_BEN_Age` for the 104 modified records (56 GP/GC, 48 Q7), confirming metadata invariance, label parity, and zero unintended side-effects.
- [`audit_live_sheet_corrections.py`](file:///d:/Research%20BanglaBBQ/scripts/audit_live_sheet_corrections.py): Live audit confirming the 48 Grandma/Grandpa row replacements on Google Sheets.
- [`scan_grandparent_grandchild.py`](file:///d:/Research%20BanglaBBQ/scripts/scan_grandparent_grandchild.py): Scans English and Bengali datasets to extract all occurrences of `grandparent`, `grandchild`, `দাদা-দাদি`, and `নাতি-নাতনি`.
- [`scan_q7_problem.py`](file:///d:/Research%20BanglaBBQ/scripts/scan_q7_problem.py): Analyzes Template 7 negative and non-negative questions, verifying polarities and comparative wording.
- [`scan_family_terms_sheets.py`](file:///d:/Research%20BanglaBBQ/scripts/scan_family_terms_sheets.py): Extracts and audits all family relationship terms (`grandma`, `grandpa`, `grandmother`, `grandfather`) from the live Google Sheet.
- [`analyze_gp_gc_details.py`](file:///d:/Research%20BanglaBBQ/scripts/analyze_gp_gc_details.py): Forensic breakdown of unique contexts and answer distributions for Q16 GC, Q16 GP, and Q18 GP.
- [`analyze_terms_breakdown.py`](file:///d:/Research%20BanglaBBQ/scripts/analyze_terms_breakdown.py): Detailed frequency audit of family term representations across all 20 Age templates.
- [`inspect_gp_gc_samples.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_gp_gc_samples.py): Context and QA pair inspector for sample Grandparent and Grandchild rows.
- [`inspect_gp_gc_answers.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_gp_gc_answers.py): Compares English and Bengali answer choices for GP and GC records.
- [`inspect_q16_all.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_q16_all.py): Analyzes all 64 variations of Template 16.
- [`inspect_all_gma_gpa.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_all_gma_gpa.py): Audits all instances of Grandma and Grandpa across the full Age benchmark.
- [`inspect_grandma_grandpa_q2.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_grandma_grandpa_q2.py): Forensic examination of Template 2 family terms.
- [`inspect_family_translations.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_family_translations.py): Side-by-side English vs Bengali comparison of family terms across contexts and QA pairs.
- [`check_existing_gm_gf.py`](file:///d:/Research%20BanglaBBQ/scripts/check_existing_gm_gf.py): Verifies existing Grandmother (`দাদি`) and Grandfather (`দাদা`) entries to ensure no collisions.
- [`find_duplicates.py`](file:///d:/Research%20BanglaBBQ/scripts/find_duplicates.py): Detects duplicate contexts, questions, and answers across the Bengali dataset.
- [`find_family_terms.py`](file:///d:/Research%20BanglaBBQ/scripts/find_family_terms.py): Scans local JSONL files for mentions of family relationships.
- [`inventory_old_dataset.py`](file:///d:/Research%20BanglaBBQ/scripts/inventory_old_dataset.py): Audits legacy thesis files (`Dataset_ BanglaBBQ_Old`) for row counts, truncation, and JSON defects.
- [`list_rows_to_modify.py`](file:///d:/Research%20BanglaBBQ/scripts/list_rows_to_modify.py): Generates exact row indices and IDs requiring translation adjustments.
- [`verify_duplicates_resolved.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_duplicates_resolved.py): Verifies that Q2 duplicate pairs dropped from 8 to 0 after Grandma/Grandpa disambiguation.

- [`generate_all_politics_themes.py`](file:///d:/Research%20BanglaBBQ/scripts/generate_all_politics_themes.py): Generates all 15 new source-backed political themes (Q6–Q20) in English and Bengali, creating 48 records per theme (720 new records total) across 2 counterfactual orientations, 4 conditions, and all 6 answer permutations (3!) with 0 duplicate QA records.
- [`apply_politics_20_themes.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_politics_20_themes.py): Writes the 720 new records to rows 242–961 on `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`, replicates the 4-row styling pattern, expands conditional formatting rules across rows 1–961, and updates local production JSONL files.
- [`verify_politics_960_live.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_politics_960_live.py): Comprehensive 11-check live Google Sheets verification script auditing the full 960-record dataset: validates Q1–Q5 preservation against backup, 48 records per theme across Q1–Q20, sequential IDs 0–959, 0 duplicate QA records, 0 label errors, 100% bilingual parity, Age formatting consistency, and untouched Age sheets.
- [`apply_exact_age_style_to_politics.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_exact_age_style_to_politics.py): Applies direct `copyPaste` with `PASTE_FORMAT` from Age reference sheets (`PakBBQ_ENG_Age`, `BanglaBBQ_BEN_Age`) across header A1:O1 and all sixty 4-row blocks A2:O241 on both Politics tabs. Restores all 5 canonical conditional format rules (Col C ambig/disambig, Col D neg/nonneg, Col E NA light blue), synchronizes column widths, and sets vertical row heights (Header 28px, Ambig 42px, Disambig 88px) for complete wrapped text visibility.
- [`verify_exact_age_style.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_exact_age_style.py): Comprehensive side-by-side audit comparing Age vs Politics sheets across headers, first 4 rows, middle rows, and final rows, verifying 100% parity in column widths, frozen rows, conditional formats, row heights, and text wrapping.
- [`apply_reordering_and_formatting.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_reordering_and_formatting.py): Reorganizes all 240 records into the canonical 4-row BBQ block ordering (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`) for all 6 answer permutations and applies consistent styling across A1:O241 on both Google Sheets tabs.
- [`verify_reordering_and_formatting.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_reordering_and_formatting.py): 10-check automated live verification script auditing the 4-row block sequence, all 6 permutations, formatting consistency across rows 1-241, and untouched Age sheets.
- [`apply_240_expansion.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_240_expansion.py): Full 6-way permutation expansion (3!) expanding each of the 5 Politics templates to 48 records (240 total), syncing Google Sheets and JSONL with 100% mathematical counterfactual parity.
- [`verify_politics_240_live.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_politics_240_live.py): End-to-end live Google Sheets verification for the 240-record benchmark, auditing 48 records per template, 6 unique permutations per QA pair, 0 duplicate QA records, and 0 label errors.
- [`apply_politics_corrections.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_politics_corrections.py): Fixed 40 disambiguated gold labels, replaced probability questions with direct event-based questions, and pruned 40 duplicates.
- [`verify_politics_live.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_politics_live.py): 12-check automated audit script for the clean 120-row Politics benchmark.
- [`audit_politics_labels.py`](file:///d:/Research%20BanglaBBQ/scripts/audit_politics_labels.py): Audits disambiguated records against contextual evidence to detect counterfactual label inversion.
- [`analyze_politics_duplicates.py`](file:///d:/Research%20BanglaBBQ/scripts/analyze_politics_duplicates.py): Pinpoints exact duplicate QA pairs across English and Bengali Politics sheets.
- [`backup_politics_sheets.py`](file:///d:/Research%20BanglaBBQ/scripts/backup_politics_sheets.py): Saves raw JSON and CSV backups of Politics sheets prior to destructive updates.
- [`expand_politics_to_160.py`](file:///d:/Research%20BanglaBBQ/scripts/expand_politics_to_160.py): Expands the Politics benchmark from 112 to 160 rows, generating 32 counterbalanced variations for Q3, Q4, and Q5 with entity swaps and 3-way answer permutations.
- [`apply_160_expansion.py`](file:///d:/Research%20BanglaBBQ/scripts/apply_160_expansion.py): Pushes the fully expanded 160-row Politics datasets to Google Sheets tabs `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`.
- [`push_politics_sheets.py`](file:///d:/Research%20BanglaBBQ/scripts/push_politics_sheets.py): Initial creation and population of the Politics tabs on Google Sheets.
- [`fix_politics_color_coding.py`](file:///d:/Research%20BanglaBBQ/scripts/fix_politics_color_coding.py): Styles Google Sheets Politics tabs with executive color coding, fonts, and headers.
- [`verify_politics_sheets.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_politics_sheets.py): Audits live Politics tabs on Google Sheets for schema consistency and row counts.
- [`extract_politics_templates.py`](file:///d:/Research%20BanglaBBQ/scripts/extract_politics_templates.py): Extracts and analyzes template structures from legacy Politics JSONL files.
- [`inspect_politics.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_politics.py): Inspects English Politics dataset structure.
- [`inspect_politics_deep.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_politics_deep.py): Deep inspection of Politics questions, entities, and polarities.
- [`inspect_bengali_politics.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_bengali_politics.py): Inspects legacy Bengali Politics dataset structure.
- [`search_politics.py`](file:///d:/Research%20BanglaBBQ/scripts/search_politics.py): Entity search tool across Politics datasets.
- [`matrix_q1.py`](file:///d:/Research%20BanglaBBQ/scripts/matrix_q1.py): Validates counterbalanced permutation matrix for Politics Template 1.
- [`test_matrix_balance.py`](file:///d:/Research%20BanglaBBQ/scripts/test_matrix_balance.py): Validates balance across condition, polarity, order, and label for all templates.
- [`verify_q2_matrix.py`](file:///d:/Research%20BanglaBBQ/scripts/verify_q2_matrix.py): Audits permutation matrix for Politics Template 2.
- [`inspect_q1_pattern.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_q1_pattern.py): Analyzes variation patterns in Politics Q1.
- [`inspect_q1_q2_swaps.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_q1_q2_swaps.py): Audits entity order swapping in Politics Q1 and Q2.
- [`inspect_q3_q4_q5.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_q3_q4_q5.py): Analyzes structural deficits in legacy 16-row templates Q3, Q4, and Q5.
- [`compare_keys.py`](file:///d:/Research%20BanglaBBQ/scripts/compare_keys.py): Cross-checks JSON key schemas across English and Bengali files.

---

## 4. Google Sheets & Infrastructure Utilities

- [`refresh_google_token.py`](file:///d:/Research%20BanglaBBQ/scripts/refresh_google_token.py): Refreshes Google OAuth tokens and verifies API scope permissions.
- [`list_sheets.py`](file:///d:/Research%20BanglaBBQ/scripts/list_sheets.py): Lists all worksheet tabs and sheet IDs within the active Google Spreadsheet.
- [`inspect_age_sheet.py`](file:///d:/Research%20BanglaBBQ/scripts/inspect_age_sheet.py): Inspects metadata and grid properties of the Age sheet.
