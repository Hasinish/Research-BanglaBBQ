# Marital Status — Post-fix QA (LOCAL-ONLY, NOT PUBLICATION READY)

**GitHub source commit:** `e186b283fa5b184058e2cb395273e9968a893b20`. No remote writes. Original committed files unchanged.

- English audited rows: 1440; Bengali audited rows: 1440.
- Full 15-field schema, 10×3×48, a/b, 4 conditions, all 6 permutations, label counts 480/480/480 per language: **PASS**.
- Independent machine row-level failures: **0** (down from 96 original failures in three semantic defect test IDs). This count does **not** include source-evidence/construct residuals.
- Complete QA tuple duplicates: **0** per language; 1,440 unique per language.
- Original local audited-patch changes: **1320** fields; category and IDs untouched; separate exact change manifest exists.
- Source evidence: 3 DIRECT-within-population and 7 PARTIAL/CONTEXTUAL; Q04–Q10 require independent expert support or narrowing.
- 240 AI-reviewed bilingual anchors (30 thematic variants × 2 orientations × 4 cases), 39 executed mutation fixtures. `INDEPENDENT_HUMAN_REVIEW=NO`.
- Audited SHA256 English `52e99118b2bc35a4ffbdcd561d5a24ec08dbf9e21b2a582dfa9586532256d356`; Bengali `708154702b7b88269fa86726185997a4d66982fd9cf12b3fdd69e76396339c21`.
- Original generator in a fresh directory produced identical originals; fresh patch step produced identical audited candidates and diff manifest. Source seeds are unchanged, so generator **without** patch regenerates the original semantic defects.
- **Import verdict: NO**. No Marital Status spreadsheet tabs currently exist; full cross-bundle global collisions and independent human linguistic review are pending. Source population mismatch (27 tiger widows, not generic widows) unresolved.
