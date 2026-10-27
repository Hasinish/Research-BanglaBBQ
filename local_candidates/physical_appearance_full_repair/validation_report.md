# Physical Appearance Complete Introduction-Order Repair Validation Report

## Executive Summary
- **Category**: Physical Appearance
- **Total Records Processed**: 1,440 English + 1,440 Bengali
- **Target Reversed Variations**: 15 out of 30 (5 V1, 5 V2, 5 V3)
- **Total Introduction-Order Reversals**: Exactly 720 per language (15 variations × 48 records)
- **Disambiguated Negative Gold Position Balance**: **180 First / 180 Second** in both English and Bengali (Exact 50/50 balance)
- **Demographic Counterfactual Balance**: **180 Target / 180 Comparison** in both English and Bengali (Exact 50/50 balance)
- **Permutation Closure**: All 240 condition blocks per language contain all 6 distinct permutations
- **Schema & Metadata Integrity**: 100% byte-level invariance outside the introductory name clauses

## Theme-by-Theme Reversal Table
| Theme | Name | V1 (0-479) | V2 (480-959) | V3 (960-1439) | Reversed Variations |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Q01 | Complexion/Skin Tone | Unchanged | **Reversed** | Unchanged | V2 (48 recs) |
| Q02 | Facial Attractiveness | **Reversed** | Unchanged | **Reversed** | V1, V3 (96 recs) |
| Q03 | Body Size / Weight | **Reversed** | **Reversed** | Unchanged | V1, V2 (96 recs) |
| Q04 | Thin Body Frame | Unchanged | **Reversed** | **Reversed** | V2, V3 (96 recs) |
| Q05 | Height / Stature | **Reversed** | Unchanged | **Reversed** | V1, V3 (96 recs) |
| Q06 | Hair Texture (Curly/Straight) | **Reversed** | **Reversed** | Unchanged | V1, V2 (96 recs) |
| Q07 | Hair Colour | Unchanged | Unchanged | **Reversed** | V3 (48 recs) |
| Q08 | Visible Tattoo | **Reversed** | Unchanged | Unchanged | V1 (48 recs) |
| Q09 | Facial Makeup | Unchanged | **Reversed** | Unchanged | V2 (48 recs) |
| Q10 | Facial Skin (Acne) | Unchanged | Unchanged | **Reversed** | V3 (48 recs) |
| **Total** | **All 10 Themes** | **5 Reversed** | **5 Reversed** | **5 Reversed** | **15 Variations (720 recs)** |

## Detailed Counts
- **English Modified Records**: 720 / 1,440
- **Bengali Modified Records**: 720 / 1,440
- **English Disambiguated Negative Gold Position**: 180 First / 180 Second
- **Bengali Disambiguated Negative Gold Position**: 180 First / 180 Second
- **Demographic Balance**: 180 Target / 180 Comparison (18/18 across all 10 themes)
- **Ambiguous Records Gold**: 720/720 Unknown in EN, 720/720 Unknown in BN
- **Candidate Files**:
  - `physical_appearance_english_candidate.jsonl` (1,440 records)
  - `physical_appearance_bengali_candidate.jsonl` (1,440 records)
  - `physical_appearance_before_after.diff` (4322 lines)
