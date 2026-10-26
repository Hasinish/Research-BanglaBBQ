# BanglaBBQ - Ethnicity provisional local benchmark QA report

**Date:** 2026-10-26. **Scope:** Ethnicity only. **External operations:** read-only.

## 1. Provenance and live-snapshot limitations

- BanglaBBQ GitHub `main` head at audit: `98b7b85ee768ab04243fdf44d4c03bd7c0361605`; mandatory `memory/{README,purpose,state,index,history}.md` read through connected GitHub.
- Master live Google Sheet inspected read-only. No Ethnicity tab in its metadata. Sampled `BanglaBBQ_ENG_Education!A1:O9` and Bengali equivalent for 15-column fields, types, answer_info, four-condition ordering.
- Proposed **new category**, not a repair to an original Ethnicity baseline. Seniors' original nine categories retained untouched. The original thesis `T2510616.pdf`, section 4.2, omits Ethnicity and discusses minority coverage as future work.
- PakBBQ upstream latest audited `main` commit `c079dbae2d676f4e3bb82982144d6d4ac10436d4` (2025-11-05), source `PakBBQ/PakBBQ_ENG/Regional.jsonl`, blob SHA `c6d0a7a1b1ed9370eba23a2ec4c52369968fab87`. Exactly **944** JSON records, **18** distinct `question_index` values (1-18). Standalone Ethnicity category: `NO_DIRECT_EQUIVALENT`. All adjacent Regional indices audited in `banglabbq_ethnicity_pakbbq_theme_crosswalk.csv`.
- PakBBQ path `PakBBQ/PakBBQ_ENG/Ethnicity.jsonl` was checked on `main` and returned GitHub `404 NOT_FOUND`; no direct standalone counterpart. Its adjacent `PakBBQ/PakBBQ_ENG/Regional.jsonl` was fetched and fully audited.
- PakBBQ Regional entries were **not** considered evidence for Bangladesh. Index 7 provides only a methodological quota-stigma analogy, independently checked against a 2026 Bengali report containing specific Chakma testimony. No original upstream rows copied.
- No GitHub commits, PRs, edits to Google Sheets, memory changes, or connected-service writes.

## 2. Reproducible dataset construction

10 source-audited themes x 3 genuinely distinct local setting/action variations x 48 rows = **1,440 English + 1,440 Bengali** records (2,880 total).

Each 48-row variation is arranged as `a:24, b:24`, then each of six answer permutations, then four fixed conditions: `ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`. V1 occupies rows 0-479, V2 480-959, V3 960-1439. `example_id` is zero-based local; provisional `id` spans 8500000-8501439 and **is not approved for Google Sheets import** until a full-range collision scan. `question_index` is a string '1'..'10'. All scenarios are **fictional**. Sources justify themes, not events.

## 3. Executed structural QA

| Check | Result |
|---|---|
| English parsed records | 1440 |
| Bengali parsed records | 1440 |
| Exact 15-key schema and types | True |
| Sequential example_id and provisional id | True |
| Answer-position labels (EN / BN) | {0: 480, 1: 480, 2: 480} / {0: 480, 1: 480, 2: 480} |
| Four context-polarity combinations per language | {('ambig', 'neg'): 360, ('ambig', 'nonneg'): 360, ('disambig', 'neg'): 360, ('disambig', 'nonneg'): 360} |
| Every theme rows/language | 144 across 10 themes |
| 6 distinct answer permutations per (V,theme,orientation,condition,polarity) | True |
| Unknown correct in ambiguous contexts | True |
| Disambiguated context and label match explicit A/B roles | Tested in generator by source-state role entailment; no external human adjudication |
| Zero unintended complete QA tuple duplicates | EN 0 / BN 0 |
| English/Bengali metadata and option-role parity | True |
| Bengali user-facing text has zero ASCII English letters | True |
| Contiguous 60 manifest orientation blocks | True |
| Separate offline predicate and counterfactual verifier | True |
| Read-only live workbook ID collision scan | 0 collisions among 32,512 active ID cells; 10 production worksheets |
| 30 unique venue/setting strings | True |
| 30 unique negative/positive action pairs | True |
| Upstream PakBBQ crosswalk all 18 adjacent indices and 10 new themes | True |

**Structural QA verdict:** PASS. **Failures:** 0.

## 4. Theme/source audit and epistemic limits

The companion `banglabbq_ethnicity_source_audit.csv` is the required ten-theme source-to-mechanism matrix. Evidence tiers reflect the **theme's documentary support**, not confirmed individual causation and not any fictional benchmark scenario.

| Theme | Target comparison | Evidence tier | Methodological decision |
|---|---|---|---|
| Q01 Munda school-peer exclusion | Munda / ethnic Bengali | DIRECT | Accepted with community-specific/qualitative limitations |
| Q02 Chakma assessment devaluation | Chakma / ethnic Bengali | DIRECT | Accepted with community-specific/qualitative limitations |
| Q03 Chakma merit or quota stigma | Chakma / ethnic Bengali | DIRECT | Accepted with community-specific/qualitative limitations |
| Q04 Chakma rental-housing exclusion | Chakma / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |
| Q05 Garo maternal-care discrimination | Garo (Mandi) / ethnic Bengali | DIRECT | Accepted with community-specific/qualitative limitations |
| Q06 Santal social-protection access | Santal / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |
| Q07 Mro land-title credibility | Mro / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |
| Q08 Santal police-protection inequality | Santal / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |
| Q09 Marma cultural erasure | Marma / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |
| Q10 Marma consultation exclusion | Marma / ethnic Bengali | PARTIAL | Qualified; group-specific or event-level evidence incomplete |

- Sources were checked in a live web session on 2026-10-26. Source titles and URLs are recorded in the audit CSV. Exactly **four** themes have DIRECT supporting evidence for the bias mechanism; **six** have PARTIAL evidence because an Indigenous-wide claim is not a proven group-specific claim, or because the scenario is a reasoned extrapolation.
- UN-recorded Mro land allegations directly identify the affected community, but do not establish administrative title-review bias; Q07 is conservatively tiered PARTIAL. No source establishes the 30 fictional individual decisions as real.
- The Garo maternal-health study examines women and intersectional experiences; the benchmark matches pregnancy stage, health need and language to isolate ethnic labeling in the fictional text. The original research does not establish rates for all Garo women.
- Santal police-protection and application-level welfare exclusion are thematic extrapolations from institutional discrimination reports; they require additional local community review before academic publication.

## 5. Candidate screening (15 mechanisms considered)

10 included themes above. Five other candidates evaluated and rejected:

1. Ethnic criminality/smuggling suspicion: no verified Bangladesh-specific source for a group stereotype; PakBBQ Regional Q08 cannot be imported.
2. Ethnic laziness or aggression: relies on broad racial essentialism and Pakistani Reddit/lifestyle analogies without local verification.
3. Santal tea-garden work ethic: occupation and economic-class confounder; cannot isolate ethnicity.
4. Ethnic-language proficiency as a proxy for intelligence: baseline language mismatch would be a genuine performance confounder; isolate ethnicity instead.
5. Urban-rural investment inequality: region comparison, not individual ethnic identity; already belongs to Regional Affiliation.

## 6. Authorship, linguistic QA, and publication status

- **Structurally validated:** YES, conditional on the detailed automated checks above.
- **Semantic self-review of 30 bilingual base pairs:** Completed by the authoring model at template level: equal resources/eligibility and opposite explicit outcomes were constructed; deterministic role/label checks executed. This is **not** independent semantic adjudication.
- **Independent Bengali/native human language review:** PENDING. Script checks characters and role correspondence, **not** nuanced fluency or full semantic equivalence. Bengali is authored rather than bulk machine-translated; text may still contain unnatural phrasing or meaning drift.
- **Source verification:** THEME-LEVEL REVIEWED; QUALIFIED. Some evidence is testimony, commentary or broader Indigenous-policy analysis, not community-specific case-control evidence. Independent citation audit and community-informed validity study needed.
- **Read-only provisional ID collision check:** Scanned the `id` column O across 10 active production worksheets (Age, Politics, Religion, Gender and Education, ENG/BEN), 32,512 ID cells total: **0 collisions** with 8500000..8501439. Hidden backups, other external datasets, and future inserts not scanned; IDs remain **provisional**.
- **Live Ethnicity sheet reconciliation:** NOT APPLICABLE / NOT DONE; there is no Ethnicity tab and no authorized import.
- **Publication ready:** NO. Before use: independent bilingual review by speakers with Indigenous-community expertise, social-science bias construct validation, adjudication of 30 semantic pairs, source upgrades for partial themes, and final import/collision QA.
- **Legacy preservation:** Original seniors' data and all nine existing categories untouched; `Ethnicity` kept separate as a proposed addition.

## 7. SHA-256 checksums (exact files generated locally)

| File | SHA-256 |
|---|---|
| `banglabbq_ethnicity_english.jsonl` | `8c783c202fcacdcaddb841873d68e4a6bba1db72e8867ad41ccaa05ee332f81b` |
| `banglabbq_ethnicity_bengali.jsonl` | `db801f8274b804c66457f4a4818d2a7e25ae427ebafe51353aecaa3e7fc8d997` |
| `banglabbq_ethnicity_source_audit.csv` | `59ae31be909c6b9644d3f69446d7b7f98b24ff7c248c64baae9a2aec960d65fe` |
| `banglabbq_ethnicity_expansion_manifest.json` | `df63d3c868fdb8824ef1124dae49fb343a23bba50928a4d68cec44465ef7261f` |
| `banglabbq_ethnicity_pakbbq_theme_crosswalk.csv` | `3a8bc400038811510ca97b61c107d27897dc3d8a50771fc6be0af1c9821d9c90` |
| `banglabbq_ethnicity_scenario_templates.json` | `224ed557b5ef69d3db7d98c361a5ef0ff76f70b84760716b69757674854d5100` |
| `generate_ethnicity.py` | `279364b39690c0da700f48cc078dcd7bb0cc5d66fac0a4b63422367cd592dfb4` |
| `validate_ethnicity_independent.py` | `37754eb3da24ff57d003f29e5af01bfa8f9afadbdfc8dd010ab602b21d0c7214` |

The report does not hash itself to avoid a self-referential checksum cycle.

## 8. Reproduction

From the directory containing `generate_ethnicity.py`, `validate_ethnicity_independent.py`, `banglabbq_ethnicity_scenario_templates.json`, and the PakBBQ crosswalk:

```sh
python3 generate_ethnicity.py
```

The generator is offline-only, reconstructs both JSONL files, the source audit, manifest and QA report, then executes the standalone second-pass validator. It exits nonzero if checks fail. It does not modify third-party services.
