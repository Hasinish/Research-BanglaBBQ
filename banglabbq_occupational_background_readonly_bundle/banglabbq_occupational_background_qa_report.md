# Occupational Background — local BanglaBBQ draft QA and provenance

**Date:** 2026-10-26  
**Mode:** STRICTLY READ ONLY for GitHub and Google Sheets; all files local.  
**Overall status:** **RESEARCH DRAFT / NOT PUBLICATION-READY**.  
**Structural QA:** **PASS** (0 failures; see below).  
**Semantic QA:** author-template and deterministic-role audit performed; independent expert/adversarial review **PENDING**.  
**Source verification:** 10 Bangladesh-grounded themes selected provisionally (evidence tier distribution: {'PARTIAL': 7, 'DIRECT': 3}); sources substantiate bias contexts, **not** fictional events; evidence/confound boundaries in source audit CSV.  
**Independent native Bengali review:** **PENDING**.  
**Live sheet synchronization:** NOT ATTEMPTED (READ-ONLY); **no sheet was changed**.  

## Grounding and limitations

- GitHub project `main` SHA: `98b7b85ee768ab04243fdf44d4c03bd7c0361605`; current memory/README.md, purpose.md, state.md, index.md, and relevant history entries were read via connected GitHub on 2026-10-26.
- Master workbook: `https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit`; checked metadata for 37 tabs and visible Education/Politics EN+BN exemplar cells. There is **no Occupational Background working tab**. Canonical *JSONL* key order differs from *physical spreadsheet* column order; JSONL follows the requested 15-key source order.
- Original thesis `T2510616.pdf` (BRAC University 2025) defines the nine released categories and the ambiguous/disambiguated bilingual BBQ method; it mentions Occupational Class in a proposed-template discussion, without a released standalone occupational category. GitHub `Dataset_ BanglaBBQ_Old/` has no standalone occupational folder.
- PakBBQ `main` SHA: `c079dbae2d676f4e3bb82982144d6d4ac10436d4`. Upstream `PakBBQ/PakBBQ_ENG/` has no occupational category. `Regional.jsonl`: **944/944 parsed**, **18 `question_index`** values with counts documented per index in crosswalk CSV; job contexts compare *regional origins*, not occupations. `ENG-linguistic(language_formality_biases).jsonl`: **88/88 parsed**, **11 indices**; Q02 has a doctor as setting, not comparison. `SES.jsonl`: **4,423,468 bytes in directory listing, content inaccessible** through connected file read, including bounded reads; **SES record and theme counts NOT VERIFIED**. Thus `NO_DIRECT_EQUIVALENT` is a directory-supported classification **with an SES audit caveat**. Never claim a completed full SES content audit.
- All 30 settings and events are **invented**, not historical incidents or actual research cases. No personal identities or evidence-of-event claims are made.
- Ten selected themes cover sanitation-contact, waste-worker unrelated competence, domestic-worker shared access, garment-worker voice, nursing social respectability, rickshaw-puller healthcare treatment, tea-garden-worker civic inclusion, sex-worker neutral volunteering, street-hawker nuisance stereotyping, and farmer presumed digital incompetence. The separate source audit CSV gives specific supported claims and contrasts each with a **fictional** prompt. Sources **do not** justify asserting stereotype prevalence, individual traits or causal occupational effects.
- Considered 14 candidates, with 4 omitted because of job-relevant confounding or mechanism duplication. See below.

## Generated counts and checks

| Test | English | Bengali |
|---|---:|---:|
| Valid JSONL rows | 1440 | 1440 |
| Themes | 10 | 10 |
| Distinct authored variations | 30 | 30 |
| Orientation blocks (24 records) | 60 | 60 |
| Complete 4-condition permutation blocks | 360 | 360 |
| Ambig / disambig | 720 / 720 | 720 / 720 |
| Negative / non-negative | 720 / 720 | 720 / 720 |
| Counterfactual a / b | 720 / 720 | 720 / 720 |
| Gold labels 0 / 1 / 2 | 480 / 480 / 480 | 480 / 480 / 480 |
| Accidental duplicate complete QA tuples | 0 | 0 |

Checks executed for **every row**: JSON parsing; exact ordered 15-key schema; key/value types; category/type; sequential and non-colliding within-draft `example_id` and provisional `id`; group-index totals; six distinct role permutations for each orientation/variation/condition; canonical four-condition ordering; one-to-one English/Bengali metadata and option-role identity; ambiguous Unknown gold; disambiguated selected-person gold; local source URL presence; duplicate *complete* (context, question, three options) records. No permutation variants were misclassified as duplicates. **Collisions with future or other concurrent drafts cannot be fully excluded without final import-time coordination**.

### Row mapping

- **V1:** Q01 rows 0–47, Q02 48–95, …, Q10 432–479.
- **V2:** Q01 rows 480–527, …, Q10 912–959.
- **V3:** Q01 rows 960–1007, …, Q10 1392–1439.
- In each 48-row theme variation: **orientation a** occupies 24 records, then **b** 24. In each orientation, six option-role permutations appear in Python `itertools.permutations((0,1,2))` order, each with four rows: `(ambig,neg)`, `(disambig,neg)`, `(ambig,nonneg)`, `(disambig,nonneg)`.
- `example_id` is row 0–1439, and `id` is **provisional** 8600000–8601439. Live `id` column O was read from all five extant EN active category tabs (Age 2920, Gender 4696, Education 2880, Religion 2880, Politics 2880, totaling 16,256 values); zero collisions observed in this reserved range. Future concurrent imports remain subject to collision review. Spreadsheet future row number = example_id + 2 (header assumed); no sheet/tab was created.
- Target/comparison jobs are reversed between a/b, while names, neutral qualifications and explicit negative-A / positive-B outcomes remain fixed; thus negative and positive factual answers reverse *occupation group* across orientations while remaining logically identifiable from context. Ambiguous versions never state a result.
- **WARNING:** `answer_info` in Bengali uses Bengali option text (aligned stable role codes), matching the verified live Education example; no invented top-level columns.

### Semantic, cultural and evidence caveats

The 30 authored bilingual base variants were inspected at authoring for: occupation-irrelevant evaluators, matched task credentials where relevant, logically opposed negative/positive questions, explicit disambiguator identifying one person for each question, no disambiguation predicate in ambiguous text, reversed occupation labels and non-identical settings/actions across the 3 variations. This is **author self-review**, not independent human certification or a claim of zero latent semantic defects. Natural Bengali was drafted manually; **native-speaker independent editing, cultural fairness/adversarial evaluation and source-mechanism peer review remain pending**.

Verification access varied; the source audit explicitly distinguishes opened pages from indexed full-text/abstract content when publisher access was blocked. Source tier semantics: `DIRECT` = primary study or authoritative report directly documents a relevant reported judgment/exclusion, but **not** the fictional specific event; `PARTIAL` = occupation-related exclusion/attitude is documented but occupational causality is confounded or transfer to the selected neutral task is inferential. `CONTEXTUAL`/`UNSUPPORTED` themes are not selected. Q01 ancestry/caste, Q07 tea-garden ethnicity, Q08 gender/religion, Q09 street-trading laws, Q10 low-income contexts are **especially important reviewer caveats**. The test is *whether a model infers the fictional outcome solely from the occupation*, not a claim that members of any occupation behave in a characteristic manner.

### Candidate triage (not selected)
- **Community health worker COVID-19 home-visit refusal** — `REJECT`: Risk-aversion during contagious outbreaks may be medically relevant; not an occupation-only fair comparison. Source considered: https://journals.plos.org/globalpublichealth/article?id=10.1371/journal.pgph.0000595
- **Police officer mistrust** — `REJECT`: Service-specific authority and conduct can create legitimate differences; evidence does not isolate irrelevant occupation-based judgments. Source considered: https://journal.mbstu.ac.bd/index.php/jst/article/view/91
- **Bus-driver reputation** — `REJECT`: Road safety/traffic-related competence and behavior can differ by driving history; topic risks real job-relevant differences. Source considered: https://www.ti-bangladesh.org/en/articles/research/6926
- **Informal waste picker contamination** — `REJECT_AS_DUPLICATE`: Overlaps Q01 sanitation stigma and Q02 waste-collector ability; thematic distinctness too weak. Source considered: https://mro.massey.ac.nz/items/e08856ef-acc2-4adf-8692-3f0104a2a5dc

### Structural failures

None in executed automated structural validation.

## SHA-256 for local deliverables

- `banglabbq_occupational_background_english.jsonl`: `fb68c17da34f67ed886e1a854e62eb7d40479667d75cf8a91d4c907d4c602615`
- `banglabbq_occupational_background_bengali.jsonl`: `bb00d7b4c241d984bb609c36fbfe507b9942dc6a0defc49752b2af628ccf68f5`
- `banglabbq_occupational_background_source_audit.csv`: `37f301092c66eff025b406d5320a209bcf69be4afc4a7265f282b148675c7bc8`
- `banglabbq_occupational_background_expansion_manifest.json`: `e0ae832137539dbfeff4fc3e6bf02335bd7338e039e1c83b5041b0449e5cd298`
- `banglabbq_occupational_background_pakbbq_theme_crosswalk.csv`: `6f0fe0783ddadb24d7d0e90401ae283a3725640d953695ec3ca09f2870373625`
- `banglabbq_occupational_background_generator.py`: `3ef60a69aa32e6c6018c1149559b2896e4ebde13ea13b216320b62eda9a4f93f`

Report checksum omitted to avoid self-reference. Generator script is self-contained and recreates all named data/audit outputs; it does not touch GitHub or Sheets.
