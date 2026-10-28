# BanglaBBQ Male Marital-Status Q11-Q20: Audited Submission Candidate

**Audit date:** 2026-10-28 (Asia/Dhaka)

**Result:** VALIDATION PASSED for deterministic structure, labels, identity swaps, binary outcome entailment, dataset uniqueness, bilingual structural parity, and scripted fault detection. **Not certified as publication-ready, linguistically peer-reviewed, or fully source-verified for every specific bias mechanism.** A guarantee of 100% sociolinguistic or cultural correctness is scientifically impossible without independent trained Bengali-speaking human annotation.

## Sources of truth and protection

- Authoritative GitHub `main` commit inspected: `6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65`.
- `memory/README.md`, `memory/purpose.md`, `memory/state.md`, `memory/index.md` and recent `memory/history.md` read at this commit.
- Canonical Q01-Q10 baseline file SHA-1 blob IDs on `main` (unchanged from prior inspection): English `83d1c7ef0e05e8fb3a76de8cf8099f19eeffb644`; Bengali `31e4674b68c246abd4ea743f9d5d52fa91a891aa`.
- Baseline: 1,440 records/language, `example_id=0..1439`, `id=8700000..8701439`.
- Appended candidate: 1,440 records/language, `example_id=1440..2879`, `id=8701440..8702879`.
- Both datasets preserve `category=Marital_status`, `type=NA`, 15 top-level fields and **string** `question_index=11..20`.
- **NO Google Sheets, GitHub, or baseline writes occurred.** This is an isolated, append-only package.

## Substantive defects found and repaired

1. **Bengali possessive suffix inflections.** Generator erroneously concatenated `name+এর` rather than natural `name+ের` in the disambiguation outcome of seven variations. Repaired the generator, regenerated both files, and independently scanned every output answer name for such erroneous concatenation. These positional records were previously incorrectly considered linguistically validated.
2. **Q14 source mismatch.** The original BRAC University parenting study concerned fathers generally and did not document widower-specific assumptions. Replaced with the BBC Bangla article by Sanjana Chowdhury, 1 June 2019, reporting a widower whose relatives assumed he could not manage a household alone. This directly supports the general male widowhood stereotype but **not** the three fictional volunteering refusals.
3. **Q15 caregiving confounder.** Strengthened both participant descriptions so the divorced single father and married comparator each personally provide their child's daily care; existing matched school permissions, child's ages and volunteering qualifications remain intact. Household circumstances remain a possible residual confounder despite matched caregiving.
4. **Q17 unsupported remarried-men dishonesty claim.** The originally assigned *Daily Star* remarriage commentary did **not** establish this male-specific stereotype and, in parts, described greater acceptance of remarriage for men. Removed the unsupported theme and authored three separate fictional male-to-male scenarios about unsupported allegations of gambling, disapproved social company and drug use directed at never-married adult men. BMJ Open provides direct qualitative evidence of similar **parental fears and marriage-as-discipline norms among younger men**, but not of the precise community incidents or the older ages; source classified `DIRECT_GENERAL` with this limitation.
5. **Q19 Q12 overlap and unsupported leadership attribution.** The earlier Q19 leadership-rejection scenarios substantially overlapped Q12 responsibility/leadership and had no direct evidence of unmarried male community-election exclusion. Replaced Q19 with three distinct family-pressure-to-marry contexts comparing never-married adult men with divorced adult men who have not remarried; both express the same wish to defer marriage. BMJ Open documents male marriage pressure as a norm among young Dhaka slum residents; the ages and exact scenes remain hypothetical extrapolations.
6. **Q20 variation 3 contradictory event structure.** Two separately arranged family gatherings previously led into a single shared invitation decision. Replaced with one common optional gathering held by relatives; added matched adult-child and family-tie circumstances.
7. **Additional Bengali language and English wording repairs.** Corrected unnatural Bengali questions, names' possessive inflection, the Q15 caregiving wording, the Q20 family-gathering phrase and an ambiguous English reference to "another marriage discussion".
8. **Outdated source commit.** Updated generation/import provenance to the latest verified GitHub main commit. Baseline blobs themselves were unchanged.

## Deterministic saved-file audit

| Test | Observed |
|---|---|
| English / Bengali rows | 1,440 / 1,440 |
| Expected unique semantic cases in each language | 240 |
| Exact top-level fields | 15, order preserved |
| Question indices | Strings `"11"`...`"20"` |
| IDs | Sequential, collision-free, append-only |
| Themes / variations | 10 themes x 3 independently authored settings x 48 rows |
| Orientations | 24 `a`, 24 `b` per variation |
| Answer permutations | All six permutations per orientation |
| Conditions | `ambig/neg`, `disambig/neg`, `ambig/nonneg`, `disambig/nonneg` repeated exactly |
| Gold label distribution (each language) | `0:480`, `1:480`, `2:480` |
| First / second introduction order, disambiguated `neg` | 180 / 180; 6/6 in every variation |
| First / second introduction order, disambiguated `nonneg` | 180 / 180; 6/6 in every variation |
| Target / comparator negative gold | 180 / 180, counterfactual balanced |
| Ambiguous gold | Always Unknown / Bengali Unknown |
| Bilingual metadata / group tags / position / labels | Exact one-to-one parity |
| Unintended exact QA tuple repeats | 0 |
| Fault-injection tests | 7/7 deliberately corrupted datasets rejected |
| Regeneration from included code | Byte-for-byte identical |
| Independent crosscheck from saved data only | PASS; 960 block/orientation checks across languages |

**IMPORTANT:** The primary validator and generator share the authored specifications. The independent crosscheck does not import the generator specifications, but it cannot replace native-human semantic judgments about context plausibility, stereotype prevalence, or translation nuances. The precise fictional decisions are *not* claimed to be recorded real-world incidents.

## Source evidence matrix

| Q | Theme | Evidence tier | Specific remaining limitation |
|---|---|---|---|
| 11 | Never-married working men's rental access | DIRECT | BIGD cites bachelor refusals, not a matched experimental housing audit; sample reports ~7% discrimination based mostly on household size |
| 12 | Older never-married men, perceived immaturity | CONTEXTUAL | Study addresses youth (15-24), not 43-46-year-old men or their eligibility for voluntary coordinator roles |
| 13 | Divorced men, social distrust | DIRECT_GENERAL | Small male-divorcee interview study; no directly documented committee decisions |
| 14 | Widowers, domestic-capability assumptions | DIRECT_GENERAL | BBC widower interview directly supports stereotype, not volunteer refusal |
| 15 | Divorced single fathers, school participation | DIRECT_GENERAL | First-person single-father account, not a sampled exclusion study; household-structure confounding requires review |
| 16 | Separated men, social suspicion | CONTEXTUAL | Newspaper commentary about broader breakup/divorce stigma, not specific empirical evidence of exclusion of separated men |
| 17 | Unmarried men, baseless moral suspicion | DIRECT_GENERAL | BMJ study documents parental fears of drugs, gambling, and bad company among youth; community judgments and age 26-28 extrapolated |
| 18 | Divorced men, remarriage matchmaking bias | CONTEXTUAL | Male-divorcee stigma exists, but exact matchmaking denial not documented |
| 19 | Never-married men, social marriage pressure | DIRECT_GENERAL | Marriage pressure documented for adolescents/young men in slum sample; fictional age 29-32 family interactions unobserved |
| 20 | Widowers considering remarriage | DIRECT_GENERAL | BBC documents objections by some adult children and relatives; fictional programmatic decisions not established |

Publication/source verification: BIGD's 2017 report, especially Chapter 6.2.6 (PDF page index 111), BMJ Open (2020), Psikohumaniora (2026), The Daily Star (2022/2025), and BBC News Bangla (2019/2022) were checked through directly accessible originals and/or search-indexed substantive text. The BBC first-party domain blocked direct automated retrieval, so independently verified attribution and claims rely on available substantial BBC-mirror/search excerpts. URLs and bibliographic details appear in `marital_male_sources.csv`. Never portray contextual source evidence as direct empirical confirmation of each fictional scenario.

## Submission instruction and remaining risks

1. **Submit only as a structurally verified, source-calibrated CANDIDATE dataset**, unless separate independent linguistic and source-adjudication approval already exists. Do not claim 100% accuracy, publication readiness or native-human annotation.
2. Import exactly the 1,440 new rows per language after formal project authorization. Never overwrite or reorder 1,440 existing rows; expected merged total **2,880/language**.
3. Three themes (Q12, Q16, Q18) remain explicitly `CONTEXTUAL`, so upgrading them to `DIRECT` would be inaccurate. Specific hypothetical decisions in all themes are constructed, not observed.
4. The comparison changes first-introduction order between counterfactual orientations as specified to achieve exact positional balance. This deliberate order alternation should be controlled in downstream model analysis rather than falsely reported as a literal one-token identity-only swap.
5. If used for a submission requiring independently adjudicated culturally validated scenes, an additional review is necessary; no automated pipeline can certify that requirement from text alone.

## Reproducibility and package contents

Use `python marital_male_generate.py --output-dir .`, then `python marital_male_validation.py --directory . --selftest`, then `python independent_crosscheck.py`. Python 3; no third-party dependencies. Supporting files: both JSONL outputs, theme and source CSV, generator, scenario specifications, validation script/results, independent crosscheck, and import manifest with SHA-256 hashes. The import manifest is self-describing and hashes all import-critical files. All code and data are append-only and offline.
