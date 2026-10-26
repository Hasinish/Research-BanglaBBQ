# BanglaBBQ Physical Appearance — local read-only QA report

**Date:** 2026-10-26. **Status:** Research draft, NOT publication-ready. **Remote writes:** ZERO.

## 1. Verified live baselines
- Project `main` commit `98b7b85ee768ab04243fdf44d4c03bd7c0361605` and PakBBQ `main` commit `c079dbae2d676f4e3bb82982144d6d4ac10436d4` read via connected GitHub.
- Mandatory `memory/README.md`, `purpose.md`, `state.md`, `index.md`, relevant `history.md` read from live main.
- Current master sheet metadata: 37 tabs, no dedicated Physical Appearance tab. Active English/Bengali Education sheets supplied canonical 15-column live examples (native sheet column order differs from JSONL serialization order).
- PakBBQ `PakBBQ/PakBBQ_ENG/Physical_appearance.jsonl`: 1,368 English records, 23 distinct `question_index` theme indices, all included in `banglabbq_physical_appearance_pakbbq_theme_crosswalk.csv`. Verified Git blob SHA `6cc24e37cf04bd2d6d561d8eeb0b89a2bddb8096`.
- Old EN `Dataset_ BanglaBBQ_Old/P_A_E/Physical_appearance.jsonl`: 1,106 nonblank valid JSON objects, Git blob `43f040b4c9de392f08dd0d7cc78cd24160df123b`. Old Bengali `Dataset_ BanglaBBQ_Old/Physical_appearance/Physical_appearance.jsonl`: 1,123 nonblank valid objects, Git blob `0e13825f97f3a64c4581bb8060d682971c4f29fa`.
- Exact historical net discrepancy: Bengali repeats EIDs 842–861 (20 records, index 16), but omits EIDs 557–559 (3 records, index 6): +20 −3 = +17. Two Bengali blank lines are NOT malformed JSON. There are 59 same-EID gold-label differences requiring row-level translation/permutation adjudication. Originals never changed.
- Provisional range 8100000–8101439: live master search returned no `8100` prefix in column O across ten active EN/BN category tabs. Hidden backups were not all searched. IDs remain provisional until import QA.

## 2. Scope, format and actual computed results
- Actual checks: `{"English_JSON_records": 1440, "Bengali_JSON_records": 1440, "bilingual_total": 2880, "theme_count": 10, "variant_count": 30, "upstream_pakbbq_question_indices": 23, "upstream_pakbbq_record_total": 1368, "upstream_crosswalk_rows": 33, "source_audit_rows": 10, "English_gold_positions": {"0": 480, "1": 480, "2": 480}, "Bengali_gold_positions": {"0": 480, "1": 480, "2": 480}, "unique_English_QA_tuples": 1440, "unique_Bengali_QA_tuples": 1440, "issue_count": 0}`.
- Deterministic generator expands 10 local theme bases × 3 distinct fictional scenarios × two appearance-swapped orientations × four canonical contexts/polarities × all six exact 3! option permutations.
- Each block has 48 records: orientation a, permutations ABC/ACB/BAC/BCA/CAB/CBA each with ambig-neg, disambig-neg, ambig-nonneg, disambig-nonneg; then orientation b identical permutation logic.
- Across files: ambiguous questions always have the Unknown answer; disambiguated settings explicitly question the first named person’s relevant ability and praise the second named person’s relevant ability, independent of appearance assignment.
- Bilingual parity tests match IDs, question indices, context conditions, polarities, option group-role order, group metadata, sources, labels and version across every paired row. Translation is not independently human-reviewed.
- Answer permutation is intentional: repeated context+question with a DIFFERENT option ordering is not an accidental duplicate. The duplicate QA test includes all 3 ordered answer strings.

## 3. Evidence-to-theme matrix and caveats
- `banglabbq_physical_appearance_source_audit.csv` has all 10 theme-level source decisions. Evidence tiers: {'DIRECT': 6, 'PARTIAL': 4}.
- `DIRECT` means an opened Bangladesh-specific source describes the stigma/appearance mechanism, NOT that an experimental hiring or judgment effect was causally demonstrated.
- `PARTIAL` Q03 (larger-build reliability), Q04 (thin-build spokesperson authority), Q05 (height and public speaking) and Q10 (facial acne and perceived confidence) rely on documented shaming/appearance anxiety rather than direct evaluator-outcome measurements. The benchmark tests hypothetical stereotypes; these are lower-confidence candidates even though included as a qualified research draft.
- Q02 peer-reviewed media article (Heliyon 2024) indexed full abstract checked via PubMed/PMC web search; direct publisher/PMC openings encountered 403 or CAPTCHA at inspection. This limits full-text source verification status. No unseen paper passages are claimed verified.
- Candidate screening exceeded 12 options. Four additional proposals rejected:
  - Q-C11: Baldness vs full hair — REJECT: no opened Bangladesh source showing targeted competence stereotype, just hair-loss anxiety
  - Q-C12: Visible facial scars vs clear skin acting selection — REJECT: upstream Pakistani evidence and possible injury/health confound
  - Q-C13: Beard and soup kitchen receipt — REJECT: religious/poverty confounds and no local equivalence
  - Q-C14: Designer expensive clothing and leadership — REJECT: class/wealth and clothing care confounds

## 4. PakBBQ upstream audit and traceability
- `banglabbq_physical_appearance_pakbbq_theme_crosswalk.csv` includes each of 23 upstream distinct indices and their source, exact record count, scenario, group comparison, legacy counts and `ADAPT`/`REPLACE`/`REJECT`/`NOT_RELEVANT` decision, plus 10 explicit `NEW_LOCAL` rows.
- Imported Pakistani cases (Lahore salon, TV auditions, pregnancy, mayor elections, soup kitchens) were NOT copied as local facts. Chosen local scenes are independently fictional and unrelated to asserted real incidents.
- Legacy original and consolidated Git blob hashes are unchanged. This output is a separate, provisional new series, NOT a claim that every original sample was repaired in place or mapped one-to-one.

## 5. Separate QA statuses
- Structural validation: **PASS**; actual failures: 0. Bengali phrase and punctuation fixes applied after local spot review, then entire dataset regenerated and rechecked.
- Author semantic/template review: **AUTHORING_RULES_CHECKED_HUMAN_ADVERSARIAL_REVIEW_PENDING**. 30 authored bilingual base scenes reviewed for obvious confounders in construction but not blinded, independently validated, or crowd-annotated.
- Source verification: **QUALIFIED** (6 DIRECT mechanism sources; 4 PARTIAL mechanisms; limited causal inference; Q02 publisher direct access blocked).
- Native independent Bengali linguistic review: **PENDING**. Translation fluency and semantic entailment require independent Bangladeshi annotators before import.
- Publication ready: **NO**. Literature refresh, Bengali review, bias-mechanism validation, human annotations, adversarial challenge testing and downstream experiment review remain.
- Remote synchronization: **NOT PERFORMED BY DESIGN**. No GitHub commit, spreadsheet write, memory update, or external resource mutation.

## 6. Observed automated failures
- None from the implemented structural tests. This is NOT evidence of complete semantic correctness.

## 7. Local SHA-256 file integrity
- `banglabbq_physical_appearance_english.jsonl` — `851719a3d90c678f1cee6f61d3b23550c32d38bf202f8eeafcbc98e0d8e72e7c`
- `banglabbq_physical_appearance_bengali.jsonl` — `48aa63d1eae530ab246ab0ddef5488230d8032e7524643bd533ab1f3db482a0d`
- `banglabbq_physical_appearance_source_audit.csv` — `0d219ee37147ee4e7eebe77ec6bac72aa41ec28582ad4bd09ba713421c6ea7ce`
- `banglabbq_physical_appearance_pakbbq_theme_crosswalk.csv` — `27a6122cc00b0b382d218e3ddea52371b644f4fa526e20c5d402e9028a88604e`
- `banglabbq_physical_appearance_expansion_manifest.json` — `8f866420f669cfb7c13e6a0a7a053b685349655825862efd541d091a36817780`
- `banglabbq_physical_appearance_generator.py` — `3da90784391aa4035800ad2c3ee7bfd21f0497de5ede184ebba856212d47dcc4`

The QA report itself is excluded from its own checksum list to avoid a circular hash.
