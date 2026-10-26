# BanglaBBQ Regional Affiliation — local candidate QA report

**Audit date:** 2026-10-26 | **Mode:** READ ONLY for all connected services; local artifacts only.
**Result:** ALL AUTOMATED STRUCTURAL CHECKS PASS (20/20).

## 1. Grounding / provenance
- BanglaBBQ live GitHub main: `98b7b85ee768ab04243fdf44d4c03bd7c0361605`; connected `memory/README.md`, `purpose.md`, `state.md`, `index.md`, recent `history.md` inspected.
- PakBBQ main: `c079dbae2d676f4e3bb82982144d6d4ac10436d4`. Actual `PakBBQ/PakBBQ_ENG/Regional.jsonl`: 944 JSONL records, 18 distinct `question_index` values; blob SHA `c6d0a7a1b1ed9370eba23a2ec4c52369968fab87`. Count by index: 1:80, 2:64, 3:64, 4:64, 5:64, 6:64, 7:16, 8:16, 9:64, 10:48, 11:64, 12:80, 13:80, 14:32, 15:32, 16:32, 17:32, 18:48.
- Legacy 51 records each EN/BN across indices 1 (21) and 2 (30). Audited historical EN: 21 empty sources, 30 generic Wikipedia sources, 29 rows missing `stereotyped_groups`, 4 duplicate complete QA tuples; at least one disambiguated gold-label reversal in news-anchor sample (EID 1). Both legacy originals untouched.
- Master spreadsheet `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`: checked metadata; no active Regional tab. Education English/Bengali validated example range A1:O3 inspected for field types and metadata. The 15 JSONL keys follow canonical historical order, not Sheet visual column order.
- Paper T2510616 and IEEE draft used as historical methodology only; source URLs opened and inspected as Bangladesh journalism/academic commentary; fictional questions are NOT reported incidents.

## 2. Local output counts and data limits
- English: **1,440**, Bengali: **1,440**, combined: **2,880**; 10 themes × 3 independent setting/action variations × 48 records/language.
- Local `example_id` 0..1439; **provisional** per-category `id` 8400000..8401439, NOT confirmed globally collision-free or committed/imported.
- 2 orientations × 4 condition-polarity pairs × 6 answer permutations; per language gold labels at 0,1,2 = **480 / 480 / 480**.
- Corpus quality status: **candidate structured dataset**, not validated by an independent regional/cultural panel, not independently human translated, not publication-ready.

## 3. Executed automated checks
- PASS: **1440 records per language** — [1440, 1440]
- PASS: **15 exact ordered top-level keys** — 15
- PASS: **field numeric/string/dict types** — int,string,dict
- PASS: **Regional category and NA type** — Regional / NA
- PASS: **sequential IDs and provisional range** — example_id 0..1439, id 8400000..8401439
- PASS: **10 themes x 3 cases x 48** — 30
- PASS: **uniform gold label positions** — {'English': {2: 480, 0: 480, 1: 480}, 'Bengali': {2: 480, 0: 480, 1: 480}}
- PASS: **balanced 4 condition/polarity pairs** — {"('ambig', 'neg')": 360, "('disambig', 'neg')": 360, "('ambig', 'nonneg')": 360, "('disambig', 'nonneg')": 360}
- PASS: **6 permutations each orientation/condition/polarity** — each of 30 cases x 2 versions x 4 conditions has all 6 exact permutations
- PASS: **gold ambiguity always Unknown** — 1440 ambiguous rows combined
- PASS: **disambiguated gold from explicit role** — gold answer roles match authors' explicitly entailed contrasting predicates
- PASS: **identical structural metadata across languages** — same IDs, labels, versions, source, category
- PASS: **aligned answer role tags and three distinct options** — same group tags at each answer index
- PASS: **answer_info text equals answer text** — all 8640 answer-info entries
- PASS: **no duplicate complete QA tuple** — 0 accidental duplicates per language
- PASS: **source URLs valid and known** — nonempty inspected URL per row
- PASS: **all wave/theme/variation canonical row ranges** — wave-major V1/V2/V3 then Q01-Q10
- PASS: **each orientation pair controls same non-origin scene** — exact scene templates reused after swapping regional slots
- PASS: **all Bengali text contains Bengali script** — all 1440 Bengali QA rows
- PASS: **zero leftover template markers** — 0 placeholders

## 4. Theme-evidence calibration and source caveats
- Source evidence tiers: 6 `DIRECT` for *documented public-discourse stereotypes/anecdotes*; 4 `PARTIAL` for weaker inference or blended generalization. **No tier claims experimental prevalence or causal discrimination.**
- Q01–Q04: The Daily Star social-identity feature is first-person/essayistic, not representative field research; reported beliefs are **false generalized allegations**.
- Q05: Rangpur slur has unusually strong historical-cultural documentation, but socioeconomic hardship must not be presented as evidence of individual intelligence.
- Q06: Evidence explicitly reports Sylhet-London association; presuming cash availability is an extrapolation. Require targeted survey before strengthening.
- Q07: Author's account directly describes Sylheti accent ridicule; one social perspective is not a prevalence estimate.
- Q08: Dhaka-related standard-media language dominance is documented; **no direct evidence** for Chattogram-origin broadcaster hiring discrimination; original legacy Q1 rejection was unverified and gold-inverted. Treat as hypothesis, strongest candidate for replacement after local broadcaster review.
- Q09: TBS and Prothom Alo document expensive Chattogram wedding practices and burdens but not blanket assumptions about every individual.
- Q10: Dhaka Tribune humor feature reports collective BNCC 'uncultured' stereotype, weakly isolates Chandpur; targeted ethnographic/survey support is needed before acceptance.
- Sources validate social discussion of bias, not fictional scenario events. All outcomes in disambiguated contexts are invented evaluator remarks with **explicitly** indicated targets, not factual allegations against real districts.
- PakBBQ crosswalk audits all 18 upstream themes (with actual counts and source availability); only its structural design leads are used. The appended local rows clearly mark each independent Bangladesh theme.

## 5. Semantic/linguistic signoff — NOT complete
- Manually authored 30 separate bilingual base variants and inspected them for intended matched credentials, no action clues in ambiguous prompts, explicit disambiguated opposite subjective assessments, and role-swappable regional identities. This is assistant-led authorship/review only, **not an independent semantic or Bengali human review**.
- Structural validators do NOT prove naturalness of each Bengali sentence, external stereotype prevalence, independent human agreement, or correctness of subjective appraisal phrasing. A Bengali regional-language panel and one independent research QA reviewer should review all 30 variants with special scrutiny on Q06/Q08/Q09/Q10.
- Counterfactuals swap region of origin **only**; all contextual behavior, education, wealth, qualifications, and decision-maker remain fixed. Evaluation is on explicitly narrated treatment, not inferred innate traits.
- Some Q01/Q02/Q04/Q10 themes draw from anecdotal feature journalism; source-independent replication is recommended. If weak `PARTIAL` themes are rejected by qualified reviewer, delete entire theme blocks in a subsequent *authorized* revision rather than silently filling quotas.

## 6. Access / synchronization
- Google Sheets, GitHub, and GitHub `memory/` were accessed strictly READ-ONLY. No commits, edits, uploads, sheet cell updates, PRs or issues were made. This local output is UNSYNCHRONIZED and must not be described as production BanglaBBQ.
- Full live workbook ID collision scan across all future categories not performed; 8400000..8401439 remain reserved provisionally pending Gemini import QA.

## 7. SHA-256 checksums (generated local files)

- `banglabbq_regional_english.jsonl` — `b6caf58f388b02c1af86e0dae139a0d116ac0ede72645e7bcff19a4491d1f677`
- `banglabbq_regional_bengali.jsonl` — `5c97a1919d3e8afaca4603edf473a4a82d1dc0eefb34fb27e011362e838b7d1b`
- `banglabbq_regional_source_audit.csv` — `14127897a86fcf9a7aa8c51d9ffb757324c922e7f7fc26e69c890bf92a589879`
- `banglabbq_regional_pakbbq_theme_crosswalk.csv` — `c74d82999e311fb61aad1ad9064a709847b9e57ed93ed8f6ec61ca7334af7864`
- `banglabbq_regional_candidate_screening.csv` — `6bd313558c162105a017c8e2cac3cab91243c5c8949a7ac8d5da721fc08a8286`
- `banglabbq_regional_scenario_templates.json` — `210159d5beed94636f462e63d001a9be0d8be9e5dd6721e567b8871da55979de`
- `banglabbq_regional_expansion_manifest.json` — `fee87582f384489138622a7083c415d8aa18ec918a94328cc5b767f14cd055c7`
- `banglabbq_regional_generator.py` — `5c29a31302d6f6fd16c889f81d43b91e4ba2f65b462fdcab61c70a552c84b89c`
- `banglabbq_regional_independent_qa.py` — `d96a13e1bac67fec5b97c27de08115e13d69c24d0084c9f7c9ce8815f4df35d0`

## 8. Reproduction
```bash
python3 banglabbq_regional_generator.py --outdir /mnt/data
```

No external requests, credentials, packages, or writes to connected services occur in this script.

## 9. Separately executed independent post-generation QA

- Executed: `python3 banglabbq_regional_independent_qa.py --outdir /mnt/data`
- Observed: **13/13 PASS**, failures: `[]`.
- Scope includes row/metadata parity, actual PakBBQ index counts, canonical quartets, all base-scenario slots, Bengali Latin-token leakage, and file checksum integrity.
