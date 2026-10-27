# Research Log: Physical Appearance Introduction-Order Repair & Production Deployment

- **Date**: 2026-10-27
- **Author**: Antigravity AI Assistant & Hasin Ishrak
- **Scope**: Canonical Benchmark Category `BanglaBBQ_PhysicalAppearance` (`Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/`)
- **Action**: Full Introduction-Order Repair (15 Variations Reversed Across 10 Themes) & Production Deployment

---

## 1. Executive Summary & Problem Context

Prior forensic audits revealed a fatal 100% position shortcut in the Physical Appearance category: the first-introduced person was condemned to receive the adverse/negative outcome across all 360 disambiguated negative questions (360 First / 0 Second).

To eliminate this shortcut without altering benchmark size, IDs, schema, demographic counterfactual balance, or answer options, an introduction-order balancing strategy was designed and deployed:
- Exact 48-row per variation structure preserved.
- Exactly 15 of the 30 variations across themes Q01–Q10 had their Sentence 1 coordinate introduction order reversed ("X and Y" -> "Y and X" in English; "X ও Y" -> "Y ও X" in Bengali).
- Exactly 5 variations each were reversed across V1, V2, and V3.
- Demographic assignments, verdicts, gold labels, 6-way answer permutations, and bilingual meanings were preserved 100% byte-for-byte.

---

## 2. Reversal Schedule & Mathematical Feasibility

Across the 30 variations (10 themes × 3 variations), exactly 15 were reversed:

| Theme | Name | V1 (0–479) | V2 (480–959) | V3 (960–1439) | Reversed Variations | Reversed Records |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Q01 | Complexion / Skin Tone | Unchanged | **Reversed** | Unchanged | V2 | 48 |
| Q02 | Facial Attractiveness | **Reversed** | Unchanged | **Reversed** | V1, V3 | 96 |
| Q03 | Body Size / Weight | **Reversed** | **Reversed** | Unchanged | V1, V2 | 96 |
| Q04 | Thin Body Frame | Unchanged | **Reversed** | **Reversed** | V2, V3 | 96 |
| Q05 | Height / Stature | **Reversed** | Unchanged | **Reversed** | V1, V3 | 96 |
| Q06 | Hair Texture (Curly/Straight) | **Reversed** | **Reversed** | Unchanged | V1, V2 | 96 |
| Q07 | Hair Colour | Unchanged | Unchanged | **Reversed** | V3 | 48 |
| Q08 | Visible Tattoo | **Reversed** | Unchanged | Unchanged | V1 | 48 |
| Q09 | Facial Makeup | Unchanged | **Reversed** | Unchanged | V2 | 48 |
| Q10 | Facial Skin (Acne) | Unchanged | Unchanged | **Reversed** | V3 | 48 |
| **Total** | **All 10 Themes** | **5 Reversed** | **5 Reversed** | **5 Reversed** | **15 Variations** | **720 Records** |

---

## 3. Pre vs. Post Deployment Verification Metrics

| Metric | Pre-Repair Production | Post-Repair Production | Status |
| :--- | :--- | :--- | :--- |
| **Total Records per File** | 1,440 EN / 1,440 BN | 1,440 EN / 1,440 BN | **Verified** |
| **Modified Records** | 0 | 720 EN / 720 BN | **Verified** |
| **Modified Fields** | 0 | Strictly `context` Sentence 1 | **Verified** |
| **Disambig Neg Gold Position** | 360 First / 0 Second (100% Bias) | **180 First / 180 Second (50.0% / 50.0%)** | **PERFECT PARITY** |
| **Demographic Balance** | 180 Target / 180 Comparison | **180 Target / 180 Comparison** | **PERFECT SYMMETRY** |
| **Ambiguous Gold** | 720 Unknown | 720 Unknown | **Verified** |
| **6-Way Permutations** | 240/240 condition blocks complete | 240/240 condition blocks complete | **Verified** |
| **Bilingual Parity** | 100% aligned | 100% aligned | **Verified** |
| **Official CI Validator** | PASSED | PASSED (`scripts/validate_seven_final_categories.py`) | **100% PASS** |

---

## 4. Deployed Production Files

- `Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_english.jsonl`
- `Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl`
- Full repair generator script: `scripts/repair_physical_appearance_full.py`
- Q01 prototype script: `scripts/repair_pa_q01_intro_order.py`
- Verification script: `scratch/verify_prod_pa_balance.py`
