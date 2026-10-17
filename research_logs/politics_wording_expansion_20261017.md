# Politics wording-variation expansion — 2026-10-17

## Scope and source of truth
- Dataset: existing BanglaBBQ Politics benchmark, 20 themes, original 960 records per language.
- User explicitly authorized integrating the V2/V3 proposals from the master Google Sheet tab [Review_Politics_20_Variations](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit#gid=722176577).
- Preserved all original row values and their sequential IDs 0–959, including historical Q1–Q5 hashes.
- Added 2 wording variants per theme, each containing the full 48-record counterfactual permutation block.
- New IDs: 960–2879, per language. Total: 2,880 English + 2,880 Bengali, 144/theme/language.
- Added `additional_metadata.wording_variant` (v2/v3) and `parent_example_id` for 1:1 provenance, while preserving inherited version/source/stereotyped_groups fields.

## Data generation
- The 40 original candidate V2/V3 disambiguated bilingual contexts were read from the verified live review sheet.
- For each new candidate, derived an ambiguous introductory context, with all outcome information excluded.
- Generated counterfactual direction B by controlled reversal of group assignments and outcome attribution; manually resolved irregular grammar/syntax for Q5, Q14, Q15, Q19, and Q20.
- Copied original negative/nonnegative questions, answer choices, answer_info semantic groups, gold labels, 6 answer permutations, category, and original metadata lineage.
- Original sources are used as background references from pre-existing metadata, not as claims that the invented incidents actually occurred.

## QA evidence
1. Baseline GitHub files and live English/Bengali sheets matched exactly on all 960 original rows, 15 columns each, before mutation.
2. Created two hidden backup sheets `Backup_Politics_ENG_preV2V3_20261017` and `Backup_Politics_BEN_preV2V3_20261017`.
3. All 1,920 newly appended rows in each live language tab were read back and compared across all 15 fields to versioned shards in 240-row batches (100% matched).
4. Verified the 2,880/2,880 bilingual count, 20 x 144 theme counts, 960 records in each label position per language, and zero exact QA duplicates.
5. Verified full 2-orientation, 2-condition, 2-polarity, 6-permutation coverage for every 48-row block, and both-language structural/metadata equality.
6. Verified ambiguous gold labels are Unknown and disambiguated labels are non-Unknown with theme-specific counterfactual reversal; checked disambiguated contexts begin with their ambiguous counterparts.
7. Verified Google Sheet row counts 2,881 including headers, template formatting for new rows, and original 960-row prefix retained.
8. GitHub export uses four 480-record append-only shards per language plus a manifest, immutable backups and a deterministic assembler for materializing canonical 2,880-record files; SHA-1 Git blob hashes are recorded in the manifest.

## Remaining validation
- **Human native-language review not done**: natural Bangladeshi Bengali, all 40 A/B candidate pairs, and explicit cross-language entailment auditing remain recommended.
- **Source-relevance audit not redone**: cited reports support overarching bias phenomena but not necessarily exact fictional micro-scenarios.
- **Benchmark independence**: lexical paraphrases of one theme are correlated; use grouped splits to avoid train–test contamination and do not claim 60 independent bias scenarios.
- **Status**: Structurally validated in live Google Sheets. Publication-ready status is not asserted.
