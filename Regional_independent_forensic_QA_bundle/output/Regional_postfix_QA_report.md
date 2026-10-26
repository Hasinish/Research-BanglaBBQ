# Regional — Locally audited candidate post-fix QA results

**Status: NOT SAFE TO IMPORT.** Structural and 240-anchor role/label checks pass after local-only editorial repairs, but four theme-level evidence blockers and absence of independent Bengali human review remain.

| Test | Committed originals | Locally audited candidates | Meaning |
|---|---:|---:|---|
| Record counts | 1,440 EN + 1,440 BN | 1,440 EN + 1,440 BN | PASS |
| Schema/keys/types/category | 2,880/2,880 | 2,880/2,880 | PASS automated |
| Question_index 10 themes × 3 variations | 30/30 | 30/30 | PASS structural |
| 48 rows per variation | 30/30 per language | 30/30 per language | PASS |
| Four conditions and 6 answer permutations | 360 permutation quartets per language | Same | PASS |
| Labels 0/1/2 and 2 counterfactual versions | 480/480/480 and 720/720 per language | Same | PASS |
| Blind explicit-predicate gold inference | 240/240 paired anchors matched in both languages | 240/240 | PASS for covered predicate templates |
| Independent validator issue count | 0 | 0 | PASS automated (not human judgment) |
| Complete QA duplicates | 0 | 0 | PASS |
| Bilingual metadata and roles | 1,440/1,440 | 1,440/1,440 | PASS structural |
| Modified natural-language cells | 0 | 480 | 348 language-specific records affected |
| Source support critical | 4 provisional themes | Same 4 provisional themes | **BLOCKED** |
| Native speaker/editor independent certification | Not performed | Not performed | **BLOCKED** |
| Active Google Sheets ID scan | 32,512, no collisions | Same | PASS within actively scanned 10 tabs |
| Global/hidden historical ID scan | Not exhaustive | Not exhaustive | PARTIAL |
| Local replay | Original generator 20/20, original files byte-identical | Patch reproduced 5 files byte-identically | PASS determinism |
| Deliberate fault injection | 28/28 after checker improvement | 28/28 checked on patched candidate | PASS on known faults, not general semantic guarantee |

## Before/after change scope

Exactly **19 template-field edits** expanded deterministically into **480 context/question cell revisions** across **348 distinct language-specific records**. 120 changed English field values, 360 changed Bengali field values, no changed key/ID/answer-role/gold/source/metadata field. Full 480-cell before/after table: `Regional_change_manifest.csv`. The fixes cover seven template variation families (Q03 V2, Q04 V2, Q05 V1/V2, Q06 V3, Q07 V2, Q10 V2). The 30 revised bilingual templates are preserved alongside the reproducible local patch script.

**Original SHA-256 English:** `b6caf58f388b02c1af86e0dae139a0d116ac0ede72645e7bcff19a4491d1f677`.
**Original SHA-256 Bengali:** `5c97a1919d3e8afaca4603edf473a4a82d1dc0eefb34fb27e011362e838b7d1b`.
**Audited SHA-256 English:** `a526b1c1014a03333cbdcb9c86d48f94ebdf9723d2d92d95492fb72efc2b0bb9`.
**Audited SHA-256 Bengali:** `c15f1ca46f63e7541c761b68ecdc96ec3388607c427caa18879985c128218608`.

## Adversarial suites executed, not inferred

- Initial version of new independent validator: **26/28 specifically detected**; F24 subtle bilingual factual mismatch and F25 unequal education confound were missed as such.
- Improved independent validator: **28/28 specifically detected** in second executed run on the original dataset with temporary injected faults; **0 baseline false positives** on both original and audited datasets.
- Existing creator-side validator: **21/28 specific**, **6/28 generic hash-only**, **1/28 unstructured error (F06 missing-row case)**. A hash-only mismatch is insufficient to claim specific semantic detection.
- Improved standalone validator on **audited candidate** with 28 newly executed temporary mutations: **28/28 specifically detected**. Its original-file SHA comparison was intentionally skipped because revised files necessarily differ from the committed originals.

The test fixtures are now known to the improved checker; result demonstrates the executable regression harness, not out-of-distribution semantic correctness. See `Regional_adversarial_results*.json` for exact fixture claims and failure IDs.

## Post-fix acceptance gates

- **PASS**: structure, roles, IDs within category, cross-language metadata, inferred label positions, source URL presence, no accidental duplicate, no formula-leading natural-language fields, all 240 explicit-predicate anchor checks, deterministic regeneration.
- **PARTIAL**: AI self-reviewed Bengali cultural/translation nuance, other six category text-level overlap check, globally complete ID collision scan, variation independence.
- **BLOCKED**: Q06 Sylhet London financial access extrapolation, Q08 Chattogram broadcast-selection extrapolation, Q09 individual wedding spending assumption, Q10 isolated Chandpur uncultured claim; real independent native Bengali review; absent live import.

The local candidate deliberately retains the four evidence-critical themes **with unresolved status**, not as approved data. The user authorized read-only research and local files only; all connected services remain untouched.
