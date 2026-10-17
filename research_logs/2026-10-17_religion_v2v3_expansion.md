# Religion V2/V3 Expansion — Bilingual Structural QA and GitHub/Sheets Synchronization

**Date:** 2026-10-17  
**Stage:** Production dataset expansion, structurally validated; linguistic and source relevance review still outstanding  
**Status:** IN PROGRESS (not publication-ready)

## Authorization and scope

Researcher requested rechecking all 40 candidate bilingual V2/V3 wording pairs in `Review_Religion_20_Variations` (gid `1743426767`) and, if suitable, expanding the working Religion benchmark in the same 48-row combinatorial design as Politics.

Only Religion was modified. Politics, Age, other categories and `Dataset_ BanglaBBQ_Old/` were not modified. The 40 candidates are **paraphrases of existing fictional probes**, not 40 independently researched incidents.

## Baseline verification and immutable backups

- Committed baseline: `9f72d105d8dd16b6d69dd4121983ec7a90c4a745`, 960 records/language, 15 columns.
- Verified before writes: all 960 × 15 cells/language matched live Google Sheets against canonical JSONL (0 mismatches).
- Pre-expansion Git backup branch: `backup/religion-pre-v2v3-expansion-20261017`, retains the baseline commit.
- Byte-preserving GitHub blob aliases:
  - `backups/religion_pre_wording_v2v3_20261017/Religion_eng.jsonl`, blob `6aca7c1097fb673d3edac94c20dc35cb8f821b03`;
  - `backups/religion_pre_wording_v2v3_20261017/Religion_bng.jsonl`, blob `ccf33b375b995dbc269bb0abca1e58d67eb160b1`.
- Hidden native live backup tabs `Backup_Religion_ENG_preV2V3_20261017` (gid `1780480405`) and `Backup_Religion_BEN_preV2V3_20261017` (gid `713349647`). Each verified at 960 data rows with 0 cell differences from its production tab before expansion.
- The original 960 live rows were re-read after expansion: 0 cell differences against these pre-expansion backups in either language.

## Expansion implementation

**Production tabs**
- `BanglaBBQ_ENG_Religion` (gid `804112545`)
- `BanglaBBQ_BEN_Religion` (gid `860941009`)

**Canonical GitHub files**
- `BanglaBBQ_Religion/Religion_eng.jsonl`
- `BanglaBBQ_Religion/Religion_bng.jsonl`

**Version layout per language**

| Wave | IDs | Records | Description |
| --- | --- | ---: | --- |
| V1 | 0–959 | 960 | Original dataset; byte-for-byte unchanged |
| V2 | 960–1919 | 960 | 20 themes × 48 rows of wording variant 2 |
| V3 | 1920–2879 | 960 | 20 themes × 48 rows of wording variant 3 |
| **Total** | **0–2879** | **2,880** | **20 themes × 144 records** |

Per 48-record block: 2 role orientations (a/b) × 2 context conditions × 2 question polarities × 6 answer permutations. Added `additional_metadata.wording_variant` and `parent_example_id` only for appended records. Existing question wording, answer choices, `answer_info`, labels, source URLs, ID order, and 15-column top-level schema are preserved.

## Detailed generation review

The source proposal worksheet provides only one disambiguated negative-polarity, orientation-a exemplar per theme. It was **not** directly duplicated into 960 variants.

A separate `context_templates.json` defines 160 distinct bilingual contexts per language (40 theme/variant pairs × 4 contextual variants: ambig-a, disambig-a, ambig-b, disambig-b). Distinct ambiguous contexts were explicitly constructed without decision language, and counterfactual version-b narratives reverse demographic outcomes with qualifications held constant.

Special safeguards were required for Q5 nonreligious/observant Muslim grammatical inversion and Q6, Q9, Q10, Q16, where simple sentence removal would leak a disambiguated answer into the ambiguous context. All 40 English/Bengali V2/V3 pairs and derived orientations were checked for group presence, structural alignment, missing fields, answer leakage and exact duplicate contexts. No detected structural failures remained.

The **review-proposal text itself was not falsely marked as independent evidence**; inherited source citations remain unchanged and must be reviewed separately.

## Versioned reproducible artifacts

- `BanglaBBQ_Religion/review_v2v3_20261017.json` — source reviewer comparison.
- `BanglaBBQ_Religion/expansion_v2v3_20261017/context_templates.json` — explicit bilingual ambiguous/disambiguated contexts for orientations a/b.
- `BanglaBBQ_Religion/expansion_v2v3_20261017/shards/` — 16 append-only JSONL shards, 240 rows each (8 English and 8 Bengali); 1,920 additional records/language.
- `BanglaBBQ_Religion/expansion_v2v3_20261017/manifest.json` — SHA-verified shard/backup lineage and expected counts.
- `scripts/assemble_religion_expansion.py` — refuses mismatched historical blobs, changed labels/options/metadata, unrecognized canonical files, duplicate QA tuples, invalid permutations, changed gold role or out-of-order IDs.
- `scripts/validate_religion_dataset.py` — accepts 960-row historical baseline or 2,880-row active canonical; checks individual wording-variant blocks.
- `scripts/audit_religion_sources_and_translation.py` — supports variant-aware counterfactual and label checks, with explicit evidence-boundary warnings.
- `scripts/verify_religion_live.py` — reads 2,880 live records and compares full field values against canonical GitHub JSONL, when credentials are available.
- `.github/workflows/assemble_religion_expansion.yml` — SHA-validated canonical assembly and CI; bot commits materialized canonical files by fast-forward only.

## Verification conducted

1. Before expansion, ENG and BEN live/committed 960-row snapshots had **0 differences** in 14,400 field comparisons/language.
2. A staging GitHub Actions assembly/materialization run succeeded, assembling and validating all 2,880 rows in both languages with source hash verification.
3. Live production sheets were resized to 2,881 rows (header + data), preserving their 15-column schema, frozen header, column formatting, and existing first 960 records.
4. Every additional 240-row shard/language was read back immediately after write and compared across all 15 fields (2 × 1,920 × 15 = **57,600 new-field comparisons**, zero differences). One initial comparison was corrected for the native Sheet's text type in `question_index`; corrected read-back found zero actual differences and no rows were replayed.
5. Post-expansion direct comparison of original 960 production rows against the new hidden backup snapshots found **0 differences in both languages**.
6. Check target totals: 2,880 rows/language; labels 960/960/960; ambiguous/disambiguated 1,440/1,440; negative/nonnegative 1,440/1,440; 20 × 144 themes; full six-way permutations; 0 exact duplicated QA tuples; bilingual structural metadata parity.
7. GitHub Action CI executed the updated category invariant validator and counterfactual audit successfully on the staging branch.

## Evidence and human-review limitations

- **Q3**: Hindu Dalit vs Muslim Dalit differentiated water access is not specifically substantiated by its source.
- **Q8**: US Department of State report (hosted at ecoi.net) is broad country evidence, not a factory clerical-hiring case.
- **Q9–Q10**: School classroom inclusion study does not directly establish religion-based debate team or speaking-slot discrimination.
- **Q12–Q13**: MRG publication offers broad minority-exclusion background, not direct evidence for individual wedding hall/guest-list decisions.
- Independent native Bengali colloquial naturalness review, counterfactual semantic-entailment annotation, and bilingual cultural review remain outstanding.
- The 40 new variants are **correlated paraphrase families**. Use theme/family-aware evaluation splits; never count each as a new independent incident.
- These open quality questions do not invalidate the completed structural data migration but **prevent publication-ready/source-verified certification**.

## Final synchronization

The active dataset must be committed on `main` only after successful live read-back and backup preservation. Verify the final published commit SHA and GitHub Actions conclusion separately. If either is incomplete, report explicitly rather than claim synchronized status.
