# BanglaBBQ Social Status (Socioeconomic Status) — local read-only QA report

**Audit date:** 2026-10-26
**Category token:** `Social_status` (proposed new taxonomy extension; not yet approved).
**Status:** STRUCTURAL AUTOMATED VALIDATION PASS; assistant scenario logic draft reviewed; independent Bengali linguistic and expert source sign-off PENDING; publication-ready: NO.

## 1. Baseline grounding and no-write guarantee

- Connected GitHub `main`: read `memory/README.md`, `memory/purpose.md`, `memory/state.md`, `memory/index.md`, and opening recent entries of `memory/history.md`. The memory state was last verified 2026-10-20; it lists the seniors' nine categories without Social Status.
- Master workbook `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`: read tab metadata and actual `BanglaBBQ_ENG_Education!A1:O4` and `BanglaBBQ_BEN_Education!A1:O3` examples. No Social Status worksheet was present. JSONL order follows the canonical key order, rather than the Google Sheets column order.
- Original BRAC thesis T2510616.pdf (Chapter 4, Data Construction Methodology, pp. 23–32), supplied by user, specifies ambiguous Unknown and disambiguated named person and 9 categories. Its generic narrative references SES/occupation templates elsewhere without demonstrating a released Social Status category: an internally inconsistent historical description, not proof of legacy rows.
- No remotely stored files, sheets, Git history, memory, issues or pull requests were modified. All output files are local.

## 2. Upstream PakBBQ SES audit — MATERIAL UNRESOLVED BLOCKER

- Repository `Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA`, upstream commit SHA `c079dbae2d676f4e3bb82982144d6d4ac10436d4` confirmed by connected GitHub commit metadata.
- SES path `PakBBQ/PakBBQ_ENG/SES.jsonl` exists on `main`; Git blob SHA `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe` confirmed by GitHub file read. The connector returned an empty content string in both UTF-8 and base64 modes while the blob itself is not the empty-blob hash. Thus **file is not verified empty**.
- Upstream SES **record count: UNVERIFIED; distinct `question_index` count and every theme index: UNVERIFIED; scenario narratives, group mappings, citation support: UNVERIFIED**. The Urdu SES file also appears in the same upstream commit but could not be read. An adjacent Religion sample was inspected through GitHub code search to confirm it is not interchangeable with SES.
- Crosswalk CSV `banglabbq_social_status_pakbbq_theme_crosswalk.csv` explicitly logs this restriction and all ten Bangladesh themes as `NEW_INDEPENDENT_NOT_CLAIMED_ADAPTATION`. **This is not an exhaustive source-to-theme crosswalk**; it must be completed after verified access to SES rows. No fabricated Pakistan stereotypes or upstream indices were inserted.

## 3. Research and candidate selection

- Considered 13 candidate mechanisms; retained **10 distinct** class-linked interpersonal mechanisms for draft QA probes. Source-evidence tiers: {'DIRECT': 4, 'PARTIAL': 6}. `DIRECT` means Bangladesh source actually documents mechanism, often via interviews/perceptions; it **does not imply causal identification** under controlled group swaps. `PARTIAL` means direct identity-only causal mechanism not established; material location, occupation or power confounders are documented.
- Q01 clinical communication respect (DIRECT), Q02 clinic service priority (PARTIAL), Q03 market purchase credibility (DIRECT), Q04 school application dignity (PARTIAL), Q05 hiring credibility (PARTIAL), Q06 administrative-counter respect (PARTIAL), Q07 social assistance humiliation (DIRECT), Q08 civic meeting voice (PARTIAL), Q09 social mixing (PARTIAL), Q10 laziness attribution (DIRECT).
- Rejected candidates: class-based criminal suspicion (confounds social class with slum geography / ethnicity), rental lease approval (structural rent/payment-security confound, no controlled interpersonal evidence), credit default presumption (collateral and prior credit-risk confounds without clean social stereotype source).
- Evidence examples: Hamid et al. (2021) `https://pubmed.ncbi.nlm.nih.gov/34622027/` explicitly reports social-status discrimination in patient communication; Ahmed et al. (2006) `https://pubmed.ncbi.nlm.nih.gov/17591342/` reports perceptions NGO clinics primarily serve the rich (not same-appointment priority); Roelen et al. (online 2025) `https://doi.org/10.1332/17598273Y2025D000000053` directly describes market, school, employment, office and welfare-related stigma; J-PAL `https://www.povertyactionlab.org/evaluation/examining-preferences-inclusive-decision-making-bangladesh` reports elite-skewed village-meeting participation (not causal exclusion by a moderator).
- Research sources and actual claims (not fictional events) are individually enumerated in `banglabbq_social_status_source_audit.csv`. Several sources were accessible as abstract/official institutional summary or indexed full text rather than as unrestricted PDF; those constitute qualified source review, not independent publication certification.

## 4. Structural build and actual validation

- Production pattern: **10 themes × 3 different contexts × 2 orientations × 4 condition-polarity blocks × 6 option permutations = 1,440 rows per language**. All context events are invented for methodological testing, not factual reports.
- Waves: V1 0–479, V2 480–959, V3 960–1439. Every 48-row scenario contains orientation `a` rows 0–23 and `b` rows 24–47 relative to its start. Each orientation contains six permutations, with ordered four-condition blocks. Per-category numerical ID range 8,200,000–8,201,439 is **provisional**. Read-only ID column scan of 10 active production tabs checked 32,512 nonempty IDs with zero collisions on 2026-10-26; hidden backups and future imports are not certified.
- Measured answer-position frequencies by language: `{"en": {"0": 480, "1": 480, "2": 480}, "bn": {"0": 480, "1": 480, "2": 480}}`.

| Automated check | Result |
|---|---|
| `each_language_1440_rows` | **PASS** |
| `exact_field_sequence` | **PASS** |
| `field_types` | **PASS** |
| `sequential_ids` | **PASS** |
| `category_and_type` | **PASS** |
| `theme_wave_counts` | **PASS** |
| `four_condition_cycle` | **PASS** |
| `position_balance` | **PASS** |
| `zero_accidental_duplicate_QA_tuples` | **PASS** |
| `valid_answer_info` | **PASS** |
| `source_and_metadata` | **PASS** |
| `condition_correct_gold` | **PASS** |
| `complete_6way_blocks` | **PASS** |
| `orientation_balance` | **PASS** |
| `bilingual_nontext_metadata_parity` | **PASS** |
| `bengali_script_present` | **PASS** |
| `class_switch_only` | **PASS** |
| `disambiguated_answer_entailment_by_named_action` | **PASS** |
| `deterministic_semantic_template_sanity` | **PASS** |

**Automated failures:** None observed.

## 5. Review matrix and unresolved limitations

| Status dimension | Assessment |
|---|---|
| JSON parse and structural invariants | PASS; real local script execution |
| Bilingual ID, role, gold-label and metadata alignment | AUTOMATED PASS; not independent semantic verification |
| Assistant-authored scenario logic sanity | 30/30 bilingual bases inspected at authoring; 60/60 language templates tested mechanically; author review is NOT blinded independent review |
| Socioeconomic-only counterfactual reversibility | AUTOMATED checked; family background strings swap, other scenario facts unchanged |
| Bangladeshi sociocultural grounding | Evidence-linked, but Q02/Q04/Q05/Q06/Q08/Q09 are PARTIAL; evidence does not causally prove identical-circumstance discrimination |
| Independent native Bengali linguistic review | NOT DONE (PENDING) |
| Independent social-science / expert source sign-off | NOT DONE (PENDING) |
| PakBBQ source-to-theme exhaustive index audit | BLOCKED (upstream SES content inaccessible) |
| Live master cell/ID collision check | 10 active production tabs, 32,512 IDs inspected in column O, 0 provisional range collisions; hidden/archive full scan NOT DONE |
| Publication-ready | NO |

## 6. File SHA-256 checksums (byte-exact)

| Local file | SHA-256 |
|---|---|
| `banglabbq_social_status_english.jsonl` | `40d7a9aae0a51285ceaa6cad83a317fdd70e0fcb4b8c47cbdadf3e3432ed3705` |
| `banglabbq_social_status_bengali.jsonl` | `ebbf776c88d35593610241eda7913d0ec7fe8522d68c5eec236f080a8a783589` |
| `banglabbq_social_status_source_audit.csv` | `f8af8b4da5d3656c13e9e2391afc38f04c1689492843f79c159cda5487ef885f` |
| `banglabbq_social_status_pakbbq_theme_crosswalk.csv` | `009e72bc2d44cf8e00f9897c0b339d28df65ce837c877b86af7e25a0d4df39f3` |
| `banglabbq_social_status_expansion_manifest.json` | `791be0f90ee30db25fc7421db10b2792c4884041348c9fe2f2fb8d926f74cb12` |
| `banglabbq_social_status_generate.py` | `ca9b13a742b6e421dda8ca8e72c3d0ad290f374a8a2e0173db90f88e6d5c30d2` |

## 7. Regeneration

Run `python banglabbq_social_status_generate.py --out /your/directory` with Python 3 standard library only. Script creates all six data/audit outputs plus QA report; deterministic JSONL, metadata and answer orders. No network calls.

**Do not import to production** until upstream PakBBQ SES enumeration, final category taxonomy approval, crosswalk completion, independent Bengali QA, source sign-off and ID collisions have been resolved.
