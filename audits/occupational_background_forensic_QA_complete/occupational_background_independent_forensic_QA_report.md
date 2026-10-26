# Occupational Background — Independent Forensic QA Audit

**Scope:** Proposed Occupational Background extension to the original nine-category BanglaBBQ (BRAC University thesis 2025); no attempt to edit any other category.  
**Audit date:** 2026-10-26 (UTC); **mode:** `REMOTE_READ_ONLY / LOCAL_CORRECTIONS_ONLY`.  
**Audited GitHub main commit:** `e186b283fa5b184058e2cb395273e9968a893b20`; last bundle addition `214795f628a34ece8deb23a65c6bf35ac0ce7157` (2026-10-26T06:17:25Z); next `main` commit only synchronized memory.  
**Source paths:** `banglabbq_occupational_background_readonly_bundle/banglabbq_occupational_background_english.jsonl` and `..._bengali.jsonl`.  
**Git blob SHAs (verified):** English `5980485457379e3e91d1cd667b9c1b8004aa8e44`; Bengali `d257262a9d2a4dd9df8ed100fe4694e611835145`.  
**Original byte SHA-256:** English `fb68c17da34f67ed886e1a854e62eb7d40479667d75cf8a91d4c907d4c602615`; Bengali `bb00d7b4c241d984bb609c36fbfe507b9942dc6a0defc49752b2af628ccf68f5`.  
**Original local snapshots:** `ORIGINAL/` (immutable original bytes). **Local audited output:** `occupational_background_audited_english.jsonl` and `occupational_background_audited_bengali.jsonl` only.  
**Final scientific verdict:** **FAIL / BLOCKED FOR PUBLICATION AND LIVE IMPORT** despite successful structural tests and local P0 entailment patches.

## 1. Executive results — measured, not inherited from the author

| Group | Original | Post-fix | Coverage & interpretation |
|---|---|---|---|
| JSONL parsing, 15-field schema, UTF-8 | PASS | PASS | 2,880/2,880 JSON objects; exact canonical JSONL field ordering |
| Theme × variations × answer permutations | PASS | PASS | 10/10 themes ×3/3 variations ×48/48 rows = 1,440/lang; 60 orientation groups ×6 permutations ×4 conditions/lang |
| Label/ID and option-role distributions | PASS | PASS | Both languages: labels 480/480/480; IDs 0..1439 and 8,600,000..8,601,439; 0 exact complete-QA duplicates |
| Context/polarity distribution | PASS | PASS | Each of 4 conditions 360/lang; ambig/disambig 720/720; neg/nonneg 720/720; a/b 720/720 |
| English/Bengali structural metadata and answer roles | PASS | PASS | All 1,440 aligned EN↔BN IDs, role codes, metadata, context types, label positions |
| Independent gold-entailment/ambiguity review | **FAIL** | PARTIAL | **132 row-level P0 defects** across **14/240 distinct bilingual anchors**; those targeted defects absent after local corrections (**0 tested row-level failures**), but construct validity and unseen semantic issues remain |
| AI bilingual editorial / cultural rubric | PARTIAL | PARTIAL | 30/30 authored variations reviewed comparatively; 240 paired orientation/condition anchors recorded, scored and mechanically projected to 2,880 rows. `AI_SELF_REVIEW`, no human reviewer |
| Source/Bangladesh mechanism validity | **FAIL** | **FAIL** | 10/10 themes, 14 source-URL audit entries; 3 DIRECT, 6 PARTIAL, 1 CONTEXTUAL. Q07 and Q10 **BLOCK** |
| Counterfactual category isolation | **FAIL** | **FAIL** | Occupational attributes swapped between a/b, but surname/ancestry/SES/gender can remain confounded. **60/60 orientation anchors have adverse=first named, favorable=second named** |
| Independent adversarial fault injection | PARTIAL | PARTIAL | Actually executed **30 mutations** pre-fix and **30** post-fix; author validator detected 21/30 and independent tester 30/30, often by **indirect consistency checks**, not independent semantic reasoning |
| Reproducibility / provenance | PARTIAL | PARTIAL | Original JSONLs, generator, manifest and old QA report match committed Git blob; generator reproduces JSONLs byte-for-byte; two auxiliary CSV references **do not match committed Git blob SHAs** |
| Provisional ID collision scanning | PASS in inspected scope | PASS in inspected scope | 32,512 IDs in 10 live production sheets + 17,280 records in 12 new-bundle JSONLs = **49,792** checked with 0 collisions. Hidden/archived inventory not exhaustively scanned |
| Google Sheets import and human sign-off | BLOCKED | BLOCKED | No Occupational tabs; `NOT_IMPORTED`, `INDEPENDENT_HUMAN_REVIEW=NO` |

### Issue ledger counts and interpretation

**212 issue ledger entries:** **P0=132**, **P1=74**, **P2=6**, **P3=0**. These are *entries*, not unique root causes: P0 entries represent **132 distinct row-level manifestations from 4 underlying semantic fault patterns**; 60 P1 entries document the first-mentioned-person shortcut by scenario orientation, ten more describe per-theme evidence/construct issues, and remaining entries are category-wide and editorial concerns. Counts are not additive with the 192 field edits.

**P0 row findings by test:** `AMBIGUOUS_PERMISSION` 24, `UNENTAILED_FEEDBACK` 48, `UNENTAILED_INPUT` 48, `UNENTAILED_REGISTER` 12. **Original anchor status:** {'PASS': 226, 'AMBIGUOUS': 4, 'UNENTAILED': 10}; **post-fix anchor status:** {'PASS': 240}. Anchors are indexed at the first of six answer permutations and checked against all six positions separately. Original semantic failures were not caught by the author's official `validate()` function (that returned **0 errors** on the uncorrected data).

### Eight highest-impact defects with exact example IDs

1. **P0 Q03 V1, EID 98 (JSONL line 99; all EN nonnegative cases in EIDs 96–143)**: both visitors already have written lift permission, so “Who was permitted?” has **two true named answers**, even though the guard later lets only one enter. **Local EN question revised** to actual entry permitted by guard, not prior entitlement.
2. **P0 Q06 V1, EID 241 (line 242; 12 EN disambiguous-negative manifestations, EIDs 240–287)**: “receptionist delays Habib” does **not entail late registration**. Revised all 24 EN disambiguated context fields to explicitly register Habib late, matching Bengali.
3. **P0 Q07 V1, EID 289 (line 290)**: omitting a **person** from minutes does not necessarily mean omitting the person's **submission**. Revised bilingual disambiguator across both orientations and polarities (48 cells total).
4. **P0 Q07 V3, EID 1249 (line 1250)**: omitting a **person** from feedback register does not directly entail omission of **feedback**. Revised bilingual evaluator action across both orientations and polarities (48 cells total).
5. **P1 Q07, EIDs 288–335 / 768–815 / 1248–1295:** tea garden labor in Bangladesh is often intertwined with **ancestry, ethnic background and residential marginalization**; source evidence does not isolate occupation. **BLOCK** as occupation-only category pending construct redesign.
6. **P1 Q10, EIDs 432–479 / 912–959 / 1392–1439:** cited youth-farming prestige study has **no evidence farmers are assumed unable to use tablets, SMS or digital attendance**. **BLOCK source-to-stereotype extrapolation**, not an invented replacement citation.
7. **P1 all 60 orientations**, including Q01 V1 EIDs 0–23 and 24–47: the **first named individual always receives the adverse evaluator outcome; second receives the favorable outcome**, regardless of orientation. A position-of-person shortcut survives answer-option randomization and invalidates fair difficulty assessment.
8. **P1 upstream crosswalk:** original old QA reported the PakBBQ SES file was inaccessible. Fetching its **full Git blob** `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe` recovered **5,384 valid JSONL records / 35 indices**; several use occupations as proxies for **SES**. Revised crosswalk now enumerates all 35 without misclassifying them as direct occupation targets.

See `occupational_background_issue_ledger.csv` for **every** row-level finding and aggregate high-priority issue, including source commit, bilingual example ID, precise line, field, original text, proposal, local status, and supporting explanation.

## 2. Local corrections and remaining high-level blocks

**Only evidence-determinable language/entailment repairs were applied** (no changed IDs, answer labels, metadata, source URLs, occupation codes, category or answer permutations):

| Repair | Field edits | Outcome |
|---|---:|---|
| Q03 V1 English guard permission question | 24 | Removes ambiguity from prior written permission |
| Q06 V1 English late-registration context | 24 | Entails late registration unambiguously |
| Q07 V1 bilingual submitted-input context | 48 | Entails the *input*, not just person inclusion |
| Q07 V3 bilingual submitted-feedback context | 48 | Entails the *feedback*, not just person inclusion |
| Q05 V3 Bengali awkward “অনুপযুক্ত আদর্শ ব্যক্তি” phrasing | 48 | Idiomatic “আদর্শ হিসেবে অনুপযুক্ত” in question/context |
| **Total** | **192 field instances** | English **96**, Bengali **96** |

Exact `original_value` and `repaired_value` for each of the 192 field edits are in `occupational_background_change_manifest.csv`. The audited pair has English **96** changed rows and Bengali **84** changed rows (some rows change two fields). Original source SHA-256 remains preserved in `ORIGINAL/`.

**Re-test:** Original author validator: **0/0 reported failures** both before and after (a missed-defect example). Independent validator: **132 → 0 targeted row-level failures**; 240/240 post-fix semantic anchors meet the *targeted explicitly assessed event/unknown condition*. This does **not** mean 240 externally human-adjudicated anchors or a source-valid 10-theme benchmark.

**Unresolved scientific faults:** Q01 caste/occupation overlap, Q03 poverty/class confounding, Q04 gender & supervisor role generalization, Q06 healthcare SES confounds, Q07 ethnic/ancestral occupation, Q09 legitimate street regulation issues, and Q10 absence of evidence for farmer digital incapacity. Full no-leakage redesign requires more than wordsmithing; leave as `BLOCKED_FOR_EXPERT_DECISION`.

## 3. Ten-theme source verification and construct decisions

`DIRECT` in this matrix means *some specific relevant Bangladeshi stigma is documented*, **not causal proof or proof of a fictional incident**. Source retrieval ranged from full text to abstracts or indexed/canonical alternatives; all fourteen URLs are itemized in `occupational_background_source_url_access_log.csv`.

| Theme | Alleged occupational-bias hypothesis | Independent tier | Decision | Source-to-probe limitation |
|---|---|---|---|---|
| Q01 | Contamination-based social exclusion | PARTIAL | REVISE | Does not isolate municipal occupation from Dalit ancestry/caste or prove the tea-service event; a civic  |
| Q02 | Presumed inability in unrelated administrative tasks | PARTIAL | REVISE | Supervisor cited occupational skills, not neutral form checking despite equal training; evidence may ref |
| Q03 | Domestic work and access to shared amenities | DIRECT | REVISE | Embedded in poverty study, one qualitative report, not proof of occupation-only causality; Q03 V1 curren |
| Q04 | Garment-worker voice characterized as troublesome | PARTIAL | REVISE | Workplace supervisors judging female employees does not demonstrate unrelated municipal-hearing hostilit |
| Q05 | Nursing profession and social respectability judgments | DIRECT | KEEP_WITH_CAVEAT | Historical attitudes and gender-specific setting cannot be assumed prevalent today or across all nurse g |
| Q06 | Rickshaw pullers and unequal healthcare respect | PARTIAL | REVISE | Poverty, rural access, triage, ability to pay may shape delays; not proof that equal-paying people with  |
| Q07 | Tea-garden laborers and civic voice | PARTIAL | BLOCK | Occupation is entangled with ethnicity/ancestry and residential isolation; evidence does not prove indiv |
| Q08 | Sex-work occupation and unrelated community volunteering | DIRECT | KEEP_WITH_CAVEAT | UNAIDS captures self-reports, not an experiment on public library volunteer placement; gender/religion a |
| Q09 | Street hawkers and presumed civic nuisance | PARTIAL | REVISE | Eviction preferences may reflect legitimate pavement access concerns; not evidence hawkers intrinsically |
| Q10 | Farmer identity and presumed lack of modern competence | CONTEXTUAL | BLOCK | No finding about farmers being incapable with tablets, SMS, or digital attendance; no valid inferential  |

Especially important: [Kabir et al. (BMJ Open 2018)](https://pubmed.ncbi.nlm.nih.gov/30552259/) concerns hereditary Dalit sweeper communities, [Sharior et al. (PLOS Water)](https://journals.plos.org/water/article?id=10.1371/journal.pwat.0000041) addresses sanitation-work conditions rather than unrelated clerical skill, [Hadley et al. (Social Science & Medicine 2007)](https://pubmed.ncbi.nlm.nih.gov/16890336/) documents historically female nursing norms, and [the Policy Press poverty/stigma article](https://doi.org/10.1332/17598273Y2025D000000053) records a concrete domestic-worker lift exclusion as one example embedded in poverty-stigma research. These are **not** evidence that a given worker behaves differently based on occupation.

The Q10 agricultural article concerns prestige of farming among selected respondents; it does not justify attributing a digital skill stereotype to farmers. Sources do not substantiate fictional events, which are deliberately hypothetical.

## 4. PakBBQ and historical lineage

- Latest PakBBQ `main`: `c079dbae2d676f4e3bb82982144d6d4ac10436d4` (read-only). Actual dataset tree contains Regional, SES, etc., **no standalone Occupational_background**.
- Regional English `PakBBQ/PakBBQ_ENG/Regional.jsonl`: **944 valid records / 18 indices**. Several include occupations as *settings* but compare regional origin, not the job itself.
- SES English `PakBBQ/PakBBQ_ENG/SES.jsonl`: **5,384 valid records / 35 indices** from full upstream Git blob. Occupations appear as class proxies (e.g. factory worker versus dentist); upstream labels are highSES/lowSES, **not protected occupational group**, so proposed crosswalk labels these `REJECT` / `NOT_RELEVANT` rather than automatic adaptation.
- Upstream linguistic Q02 doctor is incidental context. The exhaustive relevant crosswalk has **67 rows**: 18 Regional, 35 SES, one linguistic adjacent sample, original category/history and 10 Bangladeshi themes, with summary/NO_DIRECT_EQUIVALENT rows. The upstream sources are **never** proof of Bangladeshi social judgments.
- BRAC University seniors' thesis lists **nine released categories**, not a standalone Occupational Background dataset. The new category is a **proposed extension**, not a direct migrated legacy subset. Original thesis and historical files remain untouched.
- GitHub `memory/state.md` acknowledges the seven-bundle push in its header but its progress dashboard and `memory/index.md` continue to center the legacy nine; this audit reports stale synchronization, without writing to memory.

## 5. AI-based English/Bengali and cultural editorial review

The 30 scenario-variation cases were compared in both languages, then checked across orientations and four context/polarity states to produce **240 paired audit rows** with context, question, three answers, independent expected answer inferred before comparing `label`, disambiguating predicate, naturalness (1–5), cultural fit (1–5), identity respect and explicit commentary. All six option permutations were checked separately on the full 2,880-row corpus.

- Q03 V1 English “permitted” vs Bengali actual entry is a semantic difference; repaired English question.
- Q06 V1 English delay vs Bengali explicit registered-late event is a semantic difference; repaired English.
- Q07 V1 and V3 English/Bengali incorrectly describe person-listing versus proposal/feedback-listing; revised both languages.
- Q05 V3 Bengali `অনুপযুক্ত আদর্শ ব্যক্তি` was an unnatural literal calque; revised locally.
- Remaining P2 editor flags: Q01 V3 water-refill phrasing `আবার পানি`, Q06 V1 medical appointment `সাক্ষাতের সময়`, Q10 V3 electronic attendance `হাজিরা লেখা`. These are **proposals only**, not silently edited because naturalness and regional register require native assessment.
- Fictional decisions are attributed to an evaluator (they do not assert negative characteristics are real traits); identity comparisons are generally matched on immediate task conditions. Source validation and occupational-vs-ethnicity/class isolation are separate and presently incomplete.

**Review status:** `AI_SELF_REVIEW` (same assistant family as initial author, deliberately adversarial in this turn), `INDEPENDENT_HUMAN_REVIEW=NOT_PERFORMED`. The 240 anchor CSV is an exhaustive **recorded anchor-level AI judgment and rule extrapolation**, not 240 independent human annotations or a guarantee against every adversarial reading.

## 6. Fault-injection execution (30 distinct mutations × 2 dataset versions)

- **Original corpus:** 30/30 mutations executed; author validator detected **21/30**, independent validator returned failures in **30/30**.
- **Post-fix corpus:** 30/30 mutations executed; author validator detected **21/30**, independent validator reported **30/30**.
- Original author validator blind spots included broken Bengali role/occupation alignment, one-sided work qualifications, Pakistani locality leakage and source-relevance errors when URL remained syntactically valid.
- Independent checks often detect **side-effect inconsistencies** (e.g. a removed Bengali negation makes two records identical; an injected experience changes one polarity's context), **not the underlying stereotype mechanism**. Our `editorial_fault_oracle_detected` attribute describes a **predeclared manual fixture expectation**, not automatic source or cultural expertise; ten fixtures require that editorial stage. No 30/30 claim of semantic robustness is made.
- Actual per-fixture mutation descriptions, check IDs, caught/uncaught flags and false-negative information are available in both JSON results. This is stronger than a written test list, but not a formal adversarial language-model study.

## 7. Reproducibility, integration and final gate

Original generator `banglabbq_occupational_background_generator.py` was run in a fresh local temp directory: original English and Bengali JSONLs, manifest, and original QA report were **byte-identical**. The source-audit and crosswalk CSV were byte-identical to the pre-existing local copies, but **not** to the two separately read committed blob SHAs (local source audit `9d1002c2...` vs committed `7614cefbc...`; crosswalk `815c59e6...` vs committed `469b1938...`). Root cause of auxiliary mismatch was not proven; do not silently call complete seven-file reproduction PASS. The revised PakBBQ crosswalk is a separate **local audit**, not an upstream mutation.

The live master has no Occupational sheets. The Google Sheets physical A:O order is `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`, which differs from canonical JSONL key order. Import requires serializing both JSON metadata objects as JSON text, not Python dictionary reprs. The candidate remains **NOT_IMPORTED** and IDs provisional pending final stewardship.

**Final verdict: `SAFE_TO_IMPORT=NO`**. Resolve systemic name-position leakage, decide whether Q07 belongs under Ethnicity/Social Status or can be redesigned, obtain strong Bangladesh-specific evidence or redesign Q10 without padding, receive independent native Bengali and social-science stakeholder review, then run the same test suite after approval. Even if all P0 targeted corrections remain correct, that does not make the content publication-ready.

## 8. Handoff to the eighth independent coordinator

**Do not import the two locally corrected JSONLs.** Assign independent source specialists to Q01/Q03/Q07/Q10, solicit independent Bengali native and affected-community adjudication of the 30 base scenarios (with original/corrected versions blinded), require a name/outcome randomized design so name-first shortcut is no longer perfect, review counterfactuals for class/ancestry/gender confounds, and approve or reject blocked Q07 and Q10 themes explicitly. Once decisions are documented, regenerate through a versioned local patch layer, rerun both QA validators and 30+ adversarial cases, then request a separate authorized Sheets import.

**Repository and Sheets were never written to.** This report and all corrected files are exclusively local evidence and candidate artifacts.
