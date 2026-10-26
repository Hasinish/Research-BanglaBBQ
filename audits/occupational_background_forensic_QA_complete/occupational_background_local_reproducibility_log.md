# Occupational Background local forensic QA run log

- Audit date: 2026-10-26 UTC; GitHub `main`: `e186b283fa5b184058e2cb395273e9968a893b20`; original English/Bengali blobs exact to committed raw files.
- Connected GitHub READ operations: current branch SHA; five memory files; contents directory + exact blob SHAs; PakBBQ full SES blob (5384 parsed/35 themes) and Regional (944/18); six other bundles x2 JSONL files (12 x1440 parsed).
- Connected Google Sheets READ operations: metadata, canonical Education EN/BN A1:O3, active Age/Politics/Religion/Gender/Education EN/BN ID column O2:Oend. Scanned **32,512** active ID cells; **0** occupational ID collisions. Cross-bundle GitHub **17,280** records, **0** occupational collision. Hidden sheets not enumerated by content.
- Original generator invoked in separate directory:
  `python /mnt/data/banglabbq_occupational_background_generator.py --out /mnt/data/occupational_forensic_audit/WORK/regenerated_original`
  Execution: **PASS**, source English/Bengali JSONLs byte-identical; manifest and old QA report byte-identical; source and crosswalk CSV byte-identical to *locally supplied generator reference* but not to corresponding live committed Git blob SHA (see below).
- Author validator directly called via Python on original records and 60 manifest orientations: **0 failures**. Repeated on local repaired pair: **0 failures**. This validator **MISSED** 132 original sentence-level P0 row defects.
- Independent validator invoked:
  `python occupational_background_independent_validator.py --english ORIGINAL/banglabbq_occupational_background_english.jsonl --bengali ORIGINAL/banglabbq_occupational_background_bengali.jsonl --manifest /mnt/data/banglabbq_occupational_background_expansion_manifest.json --source-map /mnt/data/banglabbq_occupational_background_source_audit.csv --json-out WORK/original_independent_validation_sources.json`
  Result: **132 issues** (original) out of **2,880 total rows**.
- Local repairs through `WORK/patch_semantics_and_fix.py` (fixed literal-scoped text only): **192 field edits** (English 96; Bengali 96), 2 audited JSONL files, diff CSV. The patch script is local and does not contact any remote service.
- Independent validator on revised pair, same source-map and manifest: **0 automated row-level failures**, all 2,880 rows; all 240 post-fix paired semantic anchors regenerated with original judge notes adjusted only where repairs actually changed text.
- Adversarial mutation fixture runner actually executed **30** distinct mutations on original and **30** on audited pair; existing original validator detected 21/30, independent validator detected 30/30. IMPORTANT: many detections were *indirect consistency failures*, not true understanding of the injected cultural/semantic defect. `editorial_fault_oracle_detected` is specified by human-written fixture expectation, not automatic human adjudication or generic semantic correctness.
- Source verification: **14 URL audit entries** across 10 themes, independently scoped and tier-calibrated in source matrix. All URLs were attempted as original or indexed/canonical alternatives; publisher direct access can be 403 or abstract-only; no claim all full texts opened.
- Semantic/editorial: 30 pairwise variations × 2 orientations × 4 context/polarity states = **240 paired EN/BN anchor entries**, with textual reasoning and editorial/cultural scores; six permutations then mechanically validated across **1,440 records per language**. Language assessment is **AI_SELF_REVIEW**, not independently human certified.
- No git write/push/issue/PR, Google Sheets write/update or remote mutation. Local immutable ORIGINAL snapshots retained unchanged.

## Reference-vs-commit divergence discovered

Two pre-existing local auxiliary files (not JSONLs) have Git blob SHA mismatches with committed `main`:

| Artifact | Local Git blob SHA | Committed SHA | Consequence |
|---|---|---|---|
| source_audit.csv | `9d1002c2db205253ed9531f551be74275b371762` | `7614cefbc78a299e73284606f56730e83ac61278` | Original auxiliary not byte-identical; use independent evidence matrix, committed source names read via connector |
| pakbbq_theme_crosswalk.csv | `815c59e68d64cc8acacdd439d08fba6b65a5906c` | `469b19383171987d065790f7baaf93b04940f00b` | Old local crosswalk needed SES correction and not a verified committed byte snapshot |

The generator/manifest/English/Bengali/old QA report DID match their committed Git blobs. Local auxiliary mismatches may be serialization differences and were not silently normalized.

## Checksums

| Artifact | SHA-256 |
|---|---|
| immutable source English | `fb68c17da34f67ed886e1a854e62eb7d40479667d75cf8a91d4c907d4c602615` |
| immutable source Bengali | `bb00d7b4c241d984bb609c36fbfe507b9942dc6a0defc49752b2af628ccf68f5` |
| local audited English | `577f693d051d4e4cd9cc4e39f80cea8c6d423867c8fce46914ddc82d0e83fe32` |
| local audited Bengali | `7e595d4d059b70c8f2032c8ceacf74e2496fc68f0dcb9ec9ab6006e7e3a166a1` |
