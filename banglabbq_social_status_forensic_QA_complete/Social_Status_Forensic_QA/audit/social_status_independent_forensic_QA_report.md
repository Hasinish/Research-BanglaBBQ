# BanglaBBQ Social Status — Independent Forensic QA (AI SELF REVIEW, NOT HUMAN)
**Audited at 2026-10-26; latest `main` commit:** `e186b283fa5b184058e2cb395273e9968a893b20`. **Original seven-bundle introduction:** `214795f628a34ece8deb23a65c6bf35ac0ce7157`.

## Executive verdict
**NOT SAFE TO IMPORT OR LABEL PUBLICATION-READY.** Full bilingual JSONL structure and labels pass independent checks, but 7 unresolved P1 source/construct issues mean the 10 themes do not all meet Bangladesh-specific evidence standards. One P1 polarity defect and two P2 language issues have been repaired in local candidate files; those fixes have NOT been remotely imported or externally adjudicated.
**Reviewer provenance:** This assistant authored the originals earlier in the same conversation. The extensive fresh examination is `AI_SELF_REVIEW`, not an independent human/native or external annotation panel; `INDEPENDENT_HUMAN_REVIEW=NO`.

## 1. Immutable source and Git verification
The GitHub connected reader returned empty content for large JSONL paths; actual Git blobs were fetched by SHA. All seven original locally mounted files match GitHub blob SHAs. Current `main` head has only `memory/state.md` changes after the bundle push. The original thesis listed nine published categories; `Social_status` is a proposed new extension, not falsely assigned to seniors.
- `banglabbq_social_status_english.jsonl`: Git blob `64d2c01a06d0e216666abb7f3ee6757bd2f2e4c1`; bytes `1302258`; SHA-256 `40d7a9aae0a51285ceaa6cad83a317fdd70e0fcb4b8c47cbdadf3e3432ed3705`; match `True`
- `banglabbq_social_status_bengali.jsonl`: Git blob `af0bc36a35eb8b7244d9d62124f1700e894e1f4b`; bytes `2087178`; SHA-256 `ebbf776c88d35593610241eda7913d0ec7fe8522d68c5eec236f080a8a783589`; match `True`
- `banglabbq_social_status_expansion_manifest.json`: Git blob `b53f33a9c76668ec91f854ce7f30f716b511bc84`; bytes `91933`; SHA-256 `791be0f90ee30db25fc7421db10b2792c4884041348c9fe2f2fb8d926f74cb12`; match `True`
- `banglabbq_social_status_generate.py`: Git blob `118b6c679607bab7f68623d7f4480bb42f3f3bf6`; bytes `81885`; SHA-256 `ca9b13a742b6e421dda8ca8e72c3d0ad290f374a8a2e0173db90f88e6d5c30d2`; match `True`
- `banglabbq_social_status_pakbbq_theme_crosswalk.csv`: Git blob `92729f2261871034a8549652a49cdb8ec512fe09`; bytes `6883`; SHA-256 `009e72bc2d44cf8e00f9897c0b339d28df65ce837c877b86af7e25a0d4df39f3`; match `True`
- `banglabbq_social_status_qa_report.md`: Git blob `817484ba02b4bb6b5f5362ecbbf793e0dd210c86`; bytes `9288`; SHA-256 `f0fdaf3e40077c142c668e82c4cc4d1819ec17fa4aa94c5124d77ae28bb2682d`; match `True`
- `banglabbq_social_status_source_audit.csv`: Git blob `ee2a28ad51ce0781d0a27e710b9ae44743d07076`; bytes `10130`; SHA-256 `f8af8b4da5d3656c13e9e2391afc38f04c1689492843f79c159cda5487ef885f`; match `True`

## 2. Executed tests and actual denominators
| Test group | Status | Actual test scope / result |
|---|---|---|
| JSON parsing, exact key order, types, nested metadata | PASS | All 2,880 original + 2,880 local candidate JSONL rows; 0 independent programmatic failures |
| Counts and six-way answer permutations | PASS | 10 themes × 3 waves × 2 orientations × 4 conditions × 6 permutations, per language |
| Identifiers, labels, answer role tags | PASS | 2,880 rows each version, 480/480/480 gold positions per language, exact role mapping |
| English/Bengali structural and named-entity parity | PASS | 1,440 aligned row pairs pre/post; same IDs, roles, gold, source and subject names |
| 240 semantic anchor judgment rows | PARTIAL | 240 bilingual anchors (all 60 variation/orientation combinations × four condition/polarities) reviewed by AI author; 0 immediate explicit-gold contradictions; Q07 V3 polarity mismatch and unresolved construct issues remain |
| 30 distinct variation and cultural assessments | PARTIAL | 30/30 base variants read and scored; Q05 and Q08 show near-duplicate outcomes; only two male-coded names used |
| 9 source URLs across 10 themes | FAIL | 9 distinct original citation URLs attempted and logged; only 3 themes have directly relevant evidence and 7 remain partial/contextual |
| PakBBQ SES crosswalk | PASS | Actual 5,384 JSONL rows, 35 distinct question indices read from upstream Git blob and all 35 crosswalked; no unsupported direct-copy claims |
| Generator reproducibility | PASS | Ran original local generator; all six outputs from run reproduced byte-for-byte; 19/19 original checks passed |
| Independent validator original and candidate | PASS | 0 structural/role failures on original and local corrected 2,880-row pairs; exact reports attached |
| 29+ adversarial fault injections | PARTIAL | See executed mutation result JSON; automated detection cannot guarantee expert semantic/source verification |
| Local fixes and full retest | PARTIAL | 240 field-level edits, 2,880 candidate rows; 0 structural issues and original generator 19/19 checks on candidate; unresolved evidence blocks publication |
| Current spreadsheet and ID collision inspection | PARTIAL | 32,512 IDs across 10 active tabs + 8,640 IDs in six other new English category files: zero collisions; hidden archival assets and global import namespace not fully cleared |
| Independent human Bengali review | BLOCKED | No human reviewer or documented adjudication |

## 3. Statistical structure and derivation
- Each language: **1,440 JSONL rows**, **10** question indices (`"1"`…`"10"`), **144** rows per theme, **48** per variant, **24** per orientation, **6** option permutations in each 4-way condition block.
- Each language: **360** of each `(ambig, neg)`, `(disambig, neg)`, `(ambig, nonneg)`, `(disambig, nonneg)`; **720** each ambiguous/disambiguated, negative/nonnegative, orientation a/b; labels **480 each** at positions 0, 1, 2.
- **No true identical QA tuples** across full dataset; intended six-way option-order permutations not misclassified as duplicate scenarios. Exact row sequence is V1 Q01–Q10, V2 Q01–Q10, V3 Q01–Q10.
- **Same-name pair in all cases:** Rafi and Suman, male-coded. Counterfactual a/b swaps only stated class origin, while each named actor’s evaluated outcome remains fixed; independent semantic diversity and criterion breadth remain concerns.

## 4. Root issue counts and transparent counts
**15 root issues: P0=0; P1=8; P2=6; P3=1.** This is root-cause counting. The machine-readable ledger expands root issues to **317 precisely localized entries**, including **240 distinct local field modifications**. No structural label corruption was established. Do not treat issue ledger entries as distinct scientific root failures.
**Status:** One P1 (`SS-POL-001`) fixed locally; seven P1 evidence/construct blockers remain. Two P2 language fixes are local, two P2 near-duplicate families remain, one P2 gender/name-coverage issue remains, and the previously unavailable PakBBQ crosswalk was corrected locally. P3 project-memory staleness unresolved.

### High-impact findings, example IDs are zero-based (JSONL line = EID+1)
- **SS-POL-001, P1, Q07 V3 EIDs 1248–1295, IDs 8201248–8201295:** Negative asks whether aid was exploited, positive asks who was *thanked for handing over a certificate*. They are not polar opposites of one evaluator criterion. **LOCALLY FIXED** using matched dishonest-claim accusation versus acknowledgment of genuine eligibility, with equivalent BN wording.
- **SS-EVID-001, P1, Q07 V1–V3 EIDs 288–335 / 768–815 / 1248–1295:** Original `DIRECT` evidence claim overstates Roelen source; qualitative aid shame and perceived undeservingness do not document identical-eligibility distributor accusation in this fictional scenario. **Downgraded locally; source-critical BLOCKED**.
- **SS-EVID-002, P1, Q02 V1 EIDs 48–95 (also V2/V3):** NGO clinic access barriers do not directly substantiate skipped equal queue tokens or same-booking service delays. **BLOCKED**.
- **SS-EVID-003, P1, Q04 V1 EIDs 144–191 (also V2/V3):** Slum-address school refusal cannot be generalized to equally eligible children differing *only* in family income. **BLOCKED**.
- **SS-EVID-004, P1, Q05 V1 EIDs 192–239 (also V2/V3):** Study reports hidden slum addresses/fear of work exclusion rather than blind matched-CV family-wealth discrimination. **BLOCKED**.
- **SS-EVID-005, P1, Q06 V1 EIDs 240–287 (also V2/V3):** Civil counter disrespect for identical rules not independently established as class-only by cited locality and welfare research. **BLOCKED**.
- **SS-EVID-006, P1, Q08 V1 EIDs 336–383 (also V2/V3):** Elite-skewed meeting *participation* does not prove chair silencing a fully matched poor speaker. **BLOCKED**.
- **SS-EVID-007, P1, Q09 V3 EIDs 1344–1391:** Evidence shows poverty stigma and spatial self-exclusion, not specific host denying an equally registered neighbour a seat. **BLOCKED**.
- **SS-LING-001, P2, Q04 V1 EIDs 144–191:** Two children cannot submit literally "identical documents"; English locally changed to "the same types of required documents", preserving Bengali meaning.
- **SS-LING-002, P2, Q10 V1 EIDs 432–479:** Bengali mechanical phrase `সমানসংখ্যক যাচাই করা স্বেচ্ছাসেবী কাজের ঘণ্টা` revised to idiomatic equal volunteer-work time and equal books catalogued.

## 5. Bangladesh-specific source evidence and limitations
**Original cited URLs actually checked: 9; audited theme tiers:** **DIRECT 3**, **CONTEXTUAL 1**, **PARTIAL/CONTEXTUAL 6**, no unconditional across-theme source sign-off. All fictional incidents are constructed probes, not real reported cases.
- Q01 direct: [Hamid et al. (2021) doctor–patient study](https://onlinelibrary.wiley.com/doi/full/10.1002/hsr2.394) identifies social-status discrimination and failure to explain prescriptions among perceived relationship deficits; not a matched-patient causal trial.
- Q03 and Q10 direct mechanisms: [Roelen et al. (2025 online / vol 34 2026), poverty and stigma in urban Bangladesh](https://doi.org/10.1332/17598273Y2025D000000053) uses fieldwork from low-income Dhaka/Chattogram and records market-class dismissal, stigmatizing narratives of laziness. It cannot by itself prove equally qualified family-wealth-only comparisons.
- Q02 contextual: [Ahmed et al. NGO health access study](https://pubmed.ncbi.nlm.nih.gov/17591342/) concerns barriers in accessing care, not controlled priority tokens.
- Q04–Q06: [Rashid (2009) on urban slum exclusion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2928105/) and Roelen address territorial stigma, insufficient for a purely income-origin class causal interpretation.
- Q07: Roelen and BIGD protection publications document aid shame/stigma; prior Q07 `DIRECT` overclaims the specific interpersonal accusation. Q08: [J-PAL Bangladesh inclusive-decision study](https://www.povertyactionlab.org/evaluation/examining-preferences-inclusive-decision-making-bangladesh) evaluates elite participation in 171 villages, not controlled interpersonal moderator silencing.
- Several citations are multiple presentations of the **same** Roelen paper (journal DOI and BIGD research summary); do not count them as independent replications.
- Source retrieval includes publisher full text, PubMed abstracts, and search-indexed snippets; BIGD Ward Shabha page full access failed, and source PDF screenshot request returned a cache error (HTML/PDF text inspected instead). These access limitations are preserved in the URL log.

## 6. Counterfactual, construct validity and cultural QA
- All 30 base scenarios were reviewed as aligned fictional cases; the two-person disambiguating contrast contains an explicit adverse action for one named actor and an opposing favorable action for the other. The automated independent inference from clause ordering was checked after manual review of source sentences and is **not a general natural-language theorem prover**.
- Baseline 240 anchor rows use only original text. The new postfix 240 rows show corrected text and record the retained source limitations; independent role and gold checks cover all 1,440 permutations in each language.
- Counterfactual class swaps pass formal text reversibility: no extra occupation, school, regional, religion or gender features are changed between a/b. However, all cases pair Rafi/Suman and simply swap `low-income family` ↔ `affluent family`; this restricts gender, wealth-continuum, and real-world perceived-class signals.
- Theme Q05 is employment-screening/class concern with overlap against Educational Background and Occupational Background. Q08 community participation overlaps Politics and regional power; sources need isolation from political influence and participation barriers. Q04 may conflate location stigma with school admissions. Q02 and Q07 risk ability-to-pay/eligibility conflation, which fictional contexts partly control but primary sources do not.
- Strong dependence persists for the three V variants of Q05 (similar recruitment credibility decisions) and Q08 (similar proposal dismissal decisions); prevent V1/V2/V3 from being split across evaluation train/test folds.
- `AI_LINGUISTIC_REVIEW_COMPLETED` here means same-author AI review of paired 240 anchors, not an independent human. Bengali cultural regional representativeness and independent native-language sign-off remain **NOT_PERFORMED**.

## 7. PakBBQ SES baseline: corrected verification
- Upstream `Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA` commit `c079dbae2d676f4e3bb82982144d6d4ac10436d4`, `PakBBQ/PakBBQ_ENG/SES.jsonl`, blob `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe`.
- **5,384 parseable records and 35 distinct question indices**. Crosswalk file now enumerates all 35 with observed counts, groups, scenario summary, cited-source availability qualifiers and adaptation verdict.
- Upstream mixes rich/poor scenarios with highly confounded profession/school/regional proxy cases, includes US citations, Pakistani references and some missing sources. None is imported verbatim into Bangladesh cases; a related stereotype concept is not evidence of direct adaptation or local prevalence.

## 8. Source and generator reproducibility + validation limitations
- All seven source files are immutable in `original/`; all six original generator outputs reproduced byte-for-byte in `regenerated/`. Original validator: **19/19 PASS**. New independent validator: **0 findings out of all 2,880 rows** on committed originals and **0** on corrected candidates.
- Local candidate edits changed **120 English + 120 Bengali individual fields = 240 total**; example IDs, integer provisional IDs `8200000..8201439`, label/answer order/role/group metadata remain unchanged. Original local text replacements and the granular change manifest justify every edit.
- Scientific and source constraints remain despite zero structural findings. The candidate manifest is tagged as `LOCAL_FORENSIC_QA_CANDIDATE`, not publication-ready. The original generator still produces the immutable originals, while the separate `social_status_apply_local_fixes.py` applies the 240 authorized field changes against SHA-256-checked originals. The local candidate JSONLs have been independently reproduced byte-for-byte by the patcher; the candidate manifest is a separate audited metadata document.
- The checked full Social Status pair currently occupies **2,880** data rows total, 1,440 each language; master spreadsheet has no Social Status tab, so **live parity is NOT_APPLICABLE / NOT_IMPORTED**, not verified.

## 9. Adversarial fault-injection verdict
See `social_status_adversarial_results.json` for one result per actually injected local mutant. Detection by a general-purpose validator may be incidental (e.g. it catches an orientation or question mismatch rather than the substantive wrong meaning). The executed benchmark includes source-valid-but-irrelevant citations and cleanly propagated semantic/bilingual confounds; expert/source checking is required.

## 10. Final integration gates and coordinator recommendation
**Import: NO.** Ask the independent eighth QA coordinator to adjudicate seven P1 theme/evidence conflicts (Q02, Q04, Q05, Q06, Q07, Q08, Q09), commission actual native Bengali and domain-expert review, decide whether weak themes must be replaced rather than padded, ensure family-wise evaluation splits, verify hidden historical/global IDs and approve the `Social_status` taxonomy token. Only after these approvals should a separate agent consider spreadsheet import. No external writes occurred in this audit.

**Executed adversarial mutation suite:** 33/33 injected; original validation flagged 23; independent validation flagged 28; neither flagged 5; original/independent exceptions in 2 fixtures. See per-fixture notes and root causes in JSON; “flagged” can mean a correlated structural side-effect rather than detection of semantic fault.

## File inventory
`social_status_semantic_anchor_review.csv`, `social_status_postfix_semantic_anchor_review.csv`, `social_status_issue_ledger.csv`, `social_status_root_issue_summary.json`, `social_status_source_evidence_matrix.csv`, `social_status_source_url_access_log.csv`, `social_status_pakbbq_35_theme_crosswalk.csv`, `social_status_change_manifest.csv`, `social_status_adversarial_results.json`, `social_status_snapshot_integrity.json`, `social_status_import_readiness.json`, both validators, generator run/recheck logs, original and corrected bilingual JSONL snapshots.

## 11. Additional forensic checks completed after initial report

- **Upstream source presence:** The 35-theme PakBBQ crosswalk now includes actual per-index citation status from the full Git blob. Exactly **864/5,384** upstream records in indices **26–32** have no source URL; 4,520 rows contain URLs, not necessarily reliable or Bangladesh-specific sources. Indices 20–21 contain a suspicious `.com` suffix after an article identifier; citation validity is not assumed.
- **Specific scenario editorial work:** `social_status_30_scenario_editorial_reviews.csv` lists 30 distinct real BN/EN cases with source/construct caveats, Bengali+English disambiguating predicates, explicit questions and venue-specific review notes; all **240** original and postfix anchor rows inherit their corresponding case-specific notes. These are **AI_SELF_REVIEW** findings and automated role/gold checks, not an independent 240-case human panel.
- **Formula-injection scan executed:** 2,880 original and 2,880 candidate rows, checking context, question, and all three options for spreadsheet formula-leading `=`, `+`, `-`, `@`: **zero hits**; actual Google Sheets import not performed.
- **Corrected candidate *independently reproducible*:** `social_status_apply_local_fixes.py` reads SHA-256-pinned immutable originals, applies precisely **120 EN and 120 BN field edits** from the granular manifest, and reproduces the local corrected JSONLs **byte-for-byte** (SHA-256 verified), without GitHub or Sheets writes. This supersedes an earlier statement that a candidate patcher did not yet exist.
- **Adversarial suite exact result:** **33** injections attempted/executed. Original validator gave controlled detection for **23**, independent implementation detected **28**; **five** cleanly propagated semantic/source defects escaped *both* automated validators (FX26, FX30, FX31, FX32, FX33). Two structurally malformed cases caused the original validator to throw exceptions rather than provide controlled failure statuses. See JSON for exact mutation, modified rows, failure tests, and exceptions. These are no human annotations.
- **Reviewer caveat:** The author AI manually examined all **30 distinct authored scenario variations**, while **240 anchors** were systematically instantiated, compared and assessed using case-specific notes and a constrained name/predicate inference heuristic. This is **not equivalent to 240 independently adjudicated human judgments** or full population linguistic certification.

## 12. Cross-category boundary inspection (read-only)

The connected GitHub reader was used to inspect the committed manifests of **all six other 2026-10-26 bundles**, without altering their datasets: `Ethnicity`, `Health_status`, `Marital_status`, `Occupational_background`, `Physical_appearance`, and `Regional` (the last manifest records regional-origin themes). Combined with the original thesis category descriptions and the live Educational Background pair, this supports a provisional taxonomy-boundary audit:

- **Social_status vs Occupational_background:** Q05 hiring credibility must turn on family class signal, *not* someone’s actual occupational prestige or professional credentials. The Social Status fictional qualifications are controlled, but the class-only employer mechanism is insufficiently sourced.
- **Social_status vs Educational Background:** Q04 parent income is distinct from academic attainment and school-stream prestige; the cited school exclusions are intertwined with slum address and location, so a pure wealth mechanism remains evidence-qualified.
- **Social_status vs Regional/Ethnicity:** Q08 civic hierarchy and Q03 market treatment are class-coded in the authored hypothetical, but sources include place, migration and community-power moderators. They cannot be generalized as district/ethnic traits.
- **Social_status vs Health_status/Mental Health:** Q01–Q02 address perceived class treatment *in healthcare*, not health diagnosis or infectious risk; task-specific medical eligibility was deliberately held constant, and no clinical inference is drawn.
- **Social_status vs Marital_status/Physical_appearance:** There is no explicit marital or appearance contrast in the controlled actor pair; omission of gender/name diversity remains a cross-cultural generalizability risk.

All six new bundle manifests were **read only** for taxonomy-boundary checks. Their themes and translation quality were **not independently audited** in this Social Status assignment. Sources that support regional, occupational or location stigma do not automatically prove a clean causal family-class stereotype.
