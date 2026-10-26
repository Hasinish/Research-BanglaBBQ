# Occupational Background — post-local-fix QA report

- Audited source GitHub main: `e186b283fa5b184058e2cb395273e9968a893b20`. Original immutable blob SHAs: EN `5980485457379e3e91d1cd667b9c1b8004aa8e44`, BN `d257262a9d2a4dd9df8ed100fe4694e611835145`.
- Mode: **local-only edits**, remote READ ONLY. The output is a candidate correction, **not a replacement committed baseline**.
- 1440 English / 1440 Bengali records, ten themes × three variations ×48, 60 orientation blocks/lang, 6 permutations each, exact 4 context-polarity combinations, labels 480/480/480, unique sequential IDs.
- Repaired **192 field instances** (EN 96 / BN 96) across English 96 and Bengali 84 distinct row IDs; all before/after values in change manifest.
- Original 132 independent targeted row-level P0 findings reduced to **0**. Post-fix independent script `report()` ran across 2,880 rows, with source URL map, bilingual metadata, gold-position role checks, six-way permutations, date, Unicode and other structural invariants. Author generator's structural validator also returned zero failures.
- Postfix bilingual AI rubric: **240/240** anchor records classified PASS for the **targeted scenario predicate/unknown tests only**. No independent human review or evidence-based theme approval.
- Full 30 executed fault injections repeated after correction: author validator 21/30, independent validator 30/30, many indirect consistency detections; no categorical guarantee of detecting arbitrary coordinated semantic mutations.
- Systemic P1 remains: **first-mentioned person negative in all 60/60 orientations**, outcomes and entity names confounded. Q07 ancestry/ethnicity overlap and Q10 unverified farmer-digital-competence stereotype remain BLOCKED. 3 DIRECT limited-mechanism, 6 PARTIAL, 1 CONTEXTUAL source tiers remain. Human Bengali reviewer absent.
- **Import readiness:** NO; project approval and independent cultural review needed. No change to original GitHub or Google Sheets.

### Post-fix candidate checksums

| File | SHA-256 |
|---|---|
| `occupational_background_audited_english.jsonl` | `577f693d051d4e4cd9cc4e39f80cea8c6d423867c8fce46914ddc82d0e83fe32` |
| `occupational_background_audited_bengali.jsonl` | `7e595d4d059b70c8f2032c8ceacf74e2496fc68f0dcb9ec9ab6006e7e3a166a1` |

For detailed original defect/root-problem breakdown see `occupational_background_independent_forensic_QA_report.md`; for exact changes see `occupational_background_change_manifest.csv`.
