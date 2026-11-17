# BanglaBBQ V2.1 Targeted Repair & Full Revalidation Report

**Date**: 2026-11-17  
**Candidate Input (`untouched`)**: `fixed jsonL v2/` (SHA-256 verified 100% immutable)  
**Repaired Output**: `fixed JsonL v2.1/` (20 JSONL files: 10 categories × 2 languages = 46,080 records)  
**Audit Package**: `audits/fixed_jsonl_v21_repair_20261117/`  

---

## 1. Executive Summary & Three-Outcome Classification

| Verification Dimension | Outcome | Exact Empirical Evidence |
| :--- | :---: | :--- |
| **1. V2 Bit-for-Bit Preservation** | **PASS** | `SHA256_MANIFEST.json` proves 20/20 files in `fixed jsonL v2/` match pre-repair SHA-256 hashes identically (`v2_untouched_all: true`). Production `Dataset_BanglaBBQ_New/`, `fixed JsonL/`, Google Drive, and Google Sheets remain untouched. |
| **2. Schema, IDs, Permutations & Counterfactuals** | **PASS** | `final_structural_validation.json`: 20/20 files PASS (46,080 records, 15-field schema, sequential IDs `0..N-1`, exact `1/3` labels, exact `50/50` condition/polarity splits, 6-way permutations, 0 duplicates, 0 counterfactual gold-role flip failures, 0 protected-field mutations). |
| **3. Scoring-Engine Compatibility** | **PASS** | `scripts/bbq_scoring_engine.py` + `metadata/sidecar_stereotype_target_map.json` processed **46,080 / 46,080** V2.1 records with **0 errors**. |
| **4. Question-Family Rewrites & Consistency** | **PASS** | `question_family_validation.csv`: **480 / 480** scenario families PASS. Both missed V1 incident-lookup variations (`Ethnicity Q3 EIDs 576..623` & `HealthStatus Q15 EIDs 2592..2639`) were upgraded to PakBBQ-style questions. **0 / 23,040** `ambig == disambig` mismatches. |
| **5. Corrupted Ambiguous Prefix Repair** | **PASS** | Discovered and repaired 2 corrupted Bengali `ambig` prefixes (inherited from V1) where wrong-theme prefixes were stitched onto `disambig` S3 cues (`Ethnicity BEN Q3 EIDs 576..623` & `HealthStatus BEN Q15 EIDs 2592..2639`). **0 / 960** orientation blocks now have missing answer entities in `ambig`. |
| **6. Sentence 3 Indirectness & Zero Shortcut Check** | **PASS** | `semantic_entailment_audit.csv`: **960 / 960** blocks PASS automated checks (`0` 3-gram S3/Q overlaps across ENG/BEN, `0` remaining administrative-rejection markers after rewriting **208 orientation blocks** covering 63 ENG / 63 BEN unique S3 strings). *(Note: False-positive behavioral cues like `Education Q11` teaching skip, `PhysicalAppearance Q4`, `Politics Q10`, and `SocialStatus Q2/Q3/Q4/Q7/Q9` were deliberately preserved).* |
| **7. Targeted Bengali Suffix & Vocabulary Repairs** | **PASS** | `healthstatus_bengali_suffix_fixes.csv` & `bengali_linguistic_repair_audit.csv`: Confirmed `নাবিল-র` was a regex boundary hit inside `নাবিল-রিফাতের` (EIDs `960..1007`, 48 rows) and replaced it with `নাবিল ও রিফাতের` (`0` broken hyphen suffixes dataset-wide). Fixed stiff terms (`সাক্ষাৎকারগ্রহণকারী`, `ব্যবস্থাপক`, non-journalistic `সাক্ষাৎকার`, training `সনদ`, school `কর্মশালা`) across 116 disambig blocks while keeping genuinely natural uses (`জন্মনিবন্ধনের সনদ`, journalistic `সাক্ষাৎকার`, community `কর্মশালা`, `Education` unnamed `প্রথমজন`/`দ্বিতীয়জন`). |
| **8. Exhaustive Manual Semantic Entailment (960 Blocks)** | **INCONCLUSIVE** | While all 208 repaired blocks and sampled blocks across all 10 categories were manually inspected and passed automated agent-role/consistency checks, exhaustive line-by-line human verification of every single untouched S3 block was not performed independently in full. |
| **9. Native Human Linguistic & External Source Verification** | **INCONCLUSIVE** | Human native Bangladeshi Bengali sign-off across all 23,040 Bengali records and live URL verification of external `additional_metadata` sources have not been executed externally. |

---

## 2. Major Forensic Discoveries Fixed in V2.1 (`5,208` Field Repairs Total)

1. **`নাবিল-র` Was a Boundary Artifact Inside `নাবিল-রিফাতের` (`HealthStatus Q1`, EIDs `960..1007`)**:
   - Inspection revealed `"নাবিল-রিফাতের নম্বর সমান"` (`Nabil-Rifat's scores are equal`), NOT a broken `-র` possessive! Blind global replacement would have corrupted it into `"নাবিলেরিফাতের"`. Replaced surgically with `"নাবিল ও রিফাতের"` across all 48 rows (`healthstatus_bengali_suffix_fixes.csv`).
   - Full-dataset token scan confirmed **0** true broken hyphenated inflection suffixes anywhere across all 23,040 Bengali records (`৫-এর` in `Education Q13` is standard numeric hyphenation).
2. **Two Corrupted Ambiguous Prefixes + Missed V1 Incident Questions Repaired**:
   - `Ethnicity Q3 (EIDs 576..623)`: Bengali `ambig` prefix described a Bandarban photo exhibition (`মারমা শিক্ষার্থী`) stitched onto a Chattogram internship S3 (`চাকমা প্রার্থী`), and ENG/BEN questions stayed in old V1 incident-lookup phrasing. Rewritten cleanly in both ENG and BEN (`bilingual_alignment_report.csv`: **960 / 960 PASS**).
   - `HealthStatus Q15 (EIDs 2592..2639)`: Bengali `ambig` prefix described a Dhaka volunteer role (`তানভীর ও নাবিল`, bipolar disorder) stitched onto a Gazipur proofreading S3 (`নাবিল ও ফাহিম`, OCD), and ENG/BEN questions stayed in old V1 incident-lookup phrasing. Rewritten cleanly while preserving `Gold_neg = Fahim`, `Gold_nonneg = Nabil`, and counterfactual OCD swaps.
3. **208 Orientation Blocks Rewritten from Direct Roster/List-Crossing to Behavioral Evidence**:
   - Replaced all `crossed out`, `struck out`, `struck through`, `crossed off`, `removed`, `deleted`, `erased`, `rejected column`, and `passed over` administrative list-cutting clichés (`Ethnicity Q7/Q10`, `HealthStatus Q1..Q20`, `MaritalStatus Q12`, `Regional Q8/Q10`, `Religion Q8/Q9/Q10/Q11/Q14/Q16/Q18`, `SocialStatus Q8`) with natural situational/behavioral cues in both English and Bengali.
4. **Post-Repair Bengali Residual Counts (`0` Across All Categories)**:
   - `নাবিল-র` / broken hyphen suffixes: **0**
   - `সাক্ষাৎকারগ্রহণকারী`: **0**
   - Non-journalistic `সাক্ষাৎকার`: **0** (journalistic interviews preserved in `HealthStatus Q16` & `Politics Q12`)
   - `ব্যবস্থাপক`: **0**
   - Bureaucratic terms (`উক্ত`, `অবহিত`, `দাখিল`, `প্রদান করেন`, `ব্যর্থ হন`): **0**
   - English token leaks in Bengali: **0**

---

## 3. Deliverables Under `audits/fixed_jsonl_v21_repair_20261117/`

- `REPAIR_REPORT.md`
- `repair_change_manifest.csv` (5,208 exact `(file, eid, field, old_value, new_value, reason)` entries)
- `healthstatus_bengali_suffix_fixes.csv`
- `bengali_linguistic_repair_audit.csv`
- `sentence3_indirectness_repair_audit.csv`
- `question_family_validation.csv`
- `semantic_entailment_audit.csv`
- `bilingual_alignment_report.csv`
- `final_structural_validation.json`
- `SHA256_MANIFEST.json`
- Reproducible scripts under `scripts/` (`apply_v21_repairs.py`, `validate_v21_full.py`)
