# BanglaBBQ Regional — Independent Forensic QA (actual executed audit)

**Audit date:** 26 October 2026 (Asia/Dhaka). **Category:** `Regional` only. **Remote mode:** read-only throughout. **Reviewer status:** AI SELF-REVIEW (the model assisted earlier with dataset authoring); **independent human/native Bengali verification: NOT PERFORMED**. All fictional cases remain hypotheses, not real documented incidents.

## 1. Exact committed inputs and provenance

- GitHub `main` HEAD inspected: `e186b283fa5b184058e2cb395273e9968a893b20` (memory-only update). The Regional bundle was introduced at `214795f628a34ece8deb23a65c6bf35ac0ce7157`; no subsequent Regional data commit observed.
- Original committed paths:
  - `banglabbq_regional_research_bundle/banglabbq_regional_english.jsonl`: Git blob `081ad561c9671e7eb3b68bdf706bc95e1aef1a5e`, **1,330,338 bytes**, SHA256 `b6caf58f388b02c1af86e0dae139a0d116ac0ede72645e7bcff19a4491d1f677`.
  - `banglabbq_regional_research_bundle/banglabbq_regional_bengali.jsonl`: Git blob `6c8ca8a8e4a511fb1315e96dc3e5395825cf6035`, **2,290,938 bytes**, SHA256 `5c97a1919d3e8afaca4603edf473a4a82d1dc0eefb34fb27e011362e838b7d1b`.
- Git blob IDs were confirmed using `git hash-object` on immutable local snapshots, not inferred from filenames. Original snapshots are preserved under `original/` in the audit ZIP.
- Live GitHub `memory/README.md`, `purpose.md`, `state.md`, `index.md`, and recent `history.md` read and checked. `state.md` and `index.md` still describe the legacy 51-row Regional category and omit the newly committed bundle; `history.md` documents the October 26 push. Remote memory was not edited.
- Master Google Sheet verified read-only: no Regional production tabs. A:O columns are **not** in the same order as JSONL keys. Education exemplar confirms `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`.

## 2. Actual quantitative baseline (both full languages)

| Group | Original committed result | Local audited candidate result | Verdict |
|---|---:|---:|---|
| UTF-8 JSONL / 15 canonical keys / required nested metadata | 2,880/2,880 | 2,880/2,880 | PASS (syntax/schema) |
| Theme IDs | 10/theme × 144 per language | Same | PASS |
| Meaningfully different settings per theme | 3/3 each (30 authored variants) | Same | PARTIAL (correlated mechanisms in Q08/Q09) |
| 48-row variation × 30 per language | 30/30 | 30/30 | PASS |
| Counterfactual orientations a/b | 720/720 each language | Same | PASS |
| Ambig-neg, disambig-neg, ambig-nonneg, disambig-nonneg | 360 each × language | Same | PASS |
| Labels 0/1/2 | 480/480/480 each language | Same | PASS |
| All 6 permutations per orientation/condition | 360 permutation quartets per language | Same | PASS |
| `example_id` 0–1439 and `id` 8400000–8401439 | Complete, sequential | Unchanged | PASS for own category |
| Exact duplicate complete QA tuples | 0/2,880 | 0/2,880 | PASS |
| Identical answer options / leaked template markers / formula-leading fields / zero-width markers | 0 cases | 0 cases | PASS in tested fields |
| Cross-language structural identity, metadata, IDs, labels, roles | 1,440/1,440 pairs | Same | PASS structurally, not linguistically |
| Independent blind role/label heuristic, 240 distinct bilingual anchors | 240/240 inferred gold aligned each language | 240/240 | PASS for *tested explicit predicate template patterns* |
| Existing generator’s 20 checks | 20/20 observed | Not used on corrected candidate | PASS on originals, not sufficient scientific QA |
| Existing independent script’s 13 checks | 13/13 observed | Expected to fail original SHA on modified files | PASS on originals only |
| Separate new independent structural/anchor validator | 0 detected structural/gold errors | 0 detected structural/gold errors | PASS in automated scope |
| Theme-to-source claim support | 6 DIRECT, 4 PARTIAL | unchanged | **FAIL import gate** for Q06/Q08/Q09/Q10 |
| Independent native Bengali human editorial assessment | 0/240 | 0/240 | NOT PERFORMED |
| Live Regional spreadsheet sync | No worksheet | No worksheet | NOT IMPORTED |

**Important distinction:** a `PASS` here means a stated deterministic test passed, not proof of socioeconomic prevalence, perfect translation, or a human-validated gold label. The independent gold heuristic reads the context and question first and extracts explicit negative/positive evaluator attribution; it cannot reason about arbitrary synonyms or pragmatic implications. The 30 authored bilingual templates were AI self-reviewed; all 240 derived anchor rows were independently checked mechanically, with 240 per-anchor entries in the review CSV. Independent human judgments of all 240 anchors are not available.

## 3. Actual issue inventory and severity

The row-addressable ledger contains **1,637 entries**, including **480 corrected field changes** and **1,152 source-dependent record flags** (four provisional themes × 144 records per language × two languages). These are **not 1,637 independent conceptual defects**. There are **16 distinct issue families**:

| Severity | Families | Ledger entries | Interpretation |
|---|---:|---:|---|
| P0 | 0 | 0 | No demonstrated committed wrong gold label, malformed JSONL or irreversible semantic corruption |
| P1 | 10 | 1,608 | Six material wording/meaning correction families plus four open evidence-critical theme families |
| P2 | 4 | 27 | One Bengali grammar family, two correlated-variation/split-leakage findings, one stale shared-memory index |
| P3 | 2 | 2 representative entries | Minor Bengali style issues; each entry points to a representative, not exhaustive permutation expansion |

Examples with **exact 0-based `example_id` (JSONL line is EID + 1)**:

| Family | Example ID / provisional `id` | Diagnosis | Status |
|---|---|---|---|
| `R-SRC-Q08` | EID **336** / `8400336` | Media prestige article does not demonstrate Chattogram-origin broadcaster selection discrimination | **BLOCKED** |
| `R-SRC-Q06` | EID **240** / `8400240` | London association does not show that a Sylheti individual can supply funds or sponsorship; source leap | **BLOCKED** |
| `R-SRC-Q09` | EID **384** / `8400384` | Chattogram ceremonial spending does not imply an individual’s demands despite fixed budget | **BLOCKED** |
| `R-SRC-Q10` | EID **432** / `8400432` | BNCC joking label is a four-district aggregation, not convincing Chandpur-specific social treatment evidence | **BLOCKED** |
| `R-ED-Q03-V2` | EID **577** / `8400577` | Prior wording commended expense sharing before payment; corrected to proposed/willing participation in both languages | APPLIED LOCALLY |
| `R-ED-Q05-V1` | EID **193** / `8400193` | Bengali described *inexperience with modern work* while English described an *unsophisticated* social judgment | APPLIED LOCALLY |
| `R-ED-Q05-V2` | EID **673** / `8400673` | “knows city rules” was not equivalent to “street-smart”; corrected Bengali social judgment | APPLIED LOCALLY |
| `R-ED-Q06-V3` | EID **1201** / `8401201` | Ambiguous earlier donation versus proposed donation; corrected temporal entailment EN/BN | APPLIED LOCALLY, Q06 source still BLOCKED |
| `R-ED-Q07-V2` | EID **768** / `8400768` | Bengali “similar kind of project” vs English “identical project”; corrected to identical | APPLIED LOCALLY |
| `R-ED-Q10-V2` | EID **913** / `8400913` | Bengali “exhibitor” incorrectly represented museum tour guide; rewritten scene/evaluator/questions | APPLIED LOCALLY, Q10 source still BLOCKED |

Other corrected family: `R-ED-Q04-V2` Bengali unnatural `কাকে বিবেচনার বিরোধিতা` → `কাকে বিবেচনায় নেওয়ার বিরোধিতা` (representative EID 624, P2). Remaining minor style issues: Q07 V1 (EID 289, Bengali speech-style adjective) and Q04 V3 (EID 1105, redundant family wording). Q08 and Q09 V1/V2/V3 are functionally close enough that train/test splits must be grouped by theme/variant, not randomly by individual rows.

## 4. Scientific evidence and source verification

**All nine distinct URLs actually cited in the 10-theme source CSV were opened and inspected as readable article text on October 26, 2026.** Their publication dates, publisher/author when visible, source-level passage summaries, and accessible URLs are in `Regional_source_access_log.csv`. No unsupported quotation from an inaccessible page was used. Reopening a URL is necessary if its content changes.

| Theme | Mechanism tested (as an allegation) | Source assessment | Verdict |
|---|---|---|---|
| Q01 | Noakhali-origin person treated as dishonest | DIRECT: Daily Star explicitly mentions trope; second source is satire | KEEP, with limited-prevalence caveat |
| Q02 | Barishal-origin person labelled hot-headed | DIRECT: explicitly named in the same Daily Star feature | KEEP, with limited-prevalence caveat |
| Q03 | Tangail-origin person labelled miserly | DIRECT: explicitly named in Daily Star; time predicate fixed | LOCAL REVISED |
| Q04 | Cumilla-origin partner rejected in family discussion | DIRECT: first-person report of family disapproval | KEEP, anecdotal rather than population-level |
| Q05 | Rangpur-origin person assigned “Mofiz”/naivete label | DIRECT: Daily Star investigative/reflective feature documents degrading label | LOCAL REVISED |
| Q06 | Sylheti people presumed to raise money from British contacts | PARTIAL: documented London-association trope, not individualized funding demands | **BLOCK** pending evidence/decision |
| Q07 | Sylheti speech mocked in otherwise equally clear conversation | DIRECT: first-person testimony of ridicule | LOCAL REVISED |
| Q08 | Chattogram-origin speaker disfavored in broadcaster evaluations | PARTIAL: dominance of Dhaka standard in media, not demonstrated Chattogram hiring bias | **BLOCK** pending evidence |
| Q09 | Chattogram-origin event planner presumed to demand lavish spending | PARTIAL: actual local wedding costs and individual anecdotal stereotype, not proven group-wide preference | **BLOCK** pending evidence/design decision |
| Q10 | Chandpur-origin person judged uncultured | PARTIAL: light-hearted four-district BNCC stereotype; little Chandpur-specific evidence | **BLOCK** pending evidence/design decision |

**Source independence is limited:** Q01–Q04 rely heavily on one July 2022 Daily Star feature, while Q06–Q07 share a first-person Sylheti essay. `DIRECT` means the text genuinely documents the alleged stereotype; it does **not** mean a statistical estimate, demographic fact, or actual occurrence of any fictional QA scene.

Specific checked evidence links:

- [Nahian Nawar, The Daily Star, July 7, 2022](https://online.thedailystar.net/shout/news/what-your-ancestral-home-really-says-about-you-3065576): describes the Noakhali, Barishal, Tangail labels and Cumilla-origin relationship objection; author rejects factual generalization.
- [Saad Quasem, The Daily Star, June 13, 2025](https://www.thedailystar.net/slow-reads/big-picture/news/stereotypes-struggle-and-survival-reclaiming-the-story-behind-mofiz-3916331): Rangpur “Mofiz” origin/poverty/class stigma, not competence truth.
- [Farhat Afzal, The Daily Star, February 24, 2021](https://www.thedailystar.net/shout/news/lost-sylheti-translation-2050557): ridicule of Sylheti speech and indiscriminate London connection assumption.
- [Subah Jahwa Purba, The Financial Express, September 24, 2025](https://today.thefinancialexpress.com.bd/print/why-are-dialects-vanishing-among-the-bangladeshi-youth-1758638911): standard-Dhaka speech in media, not broadcaster hiring study.
- [Asma Sultana Prova, TBS, October 4, 2024](https://www.tbsnews.net/features/panorama/rishta-meeting-walk-park-literally-958301) and [NH Sajjad, Prothom Alo](https://en.prothomalo.com/bangladesh/fx154tmywr): local wedding expense pressure, not personal stereotypes reliably generalized.
- [Dhaka Tribune, BNCC: Hometown stereotypes, May 29, 2014](https://www.dhakatribune.com/magazine-archive/weekend-tribune/376375/bncc-hometown-stereotypes): explicitly light-hearted district jokes, including Chandpur, and one anecdote about Chattogram weddings.
- [The Daily Star, explicitly labelled satire, 2017](https://www.thedailystar.net/shout/humour/the-truth-about-noakhaillas-1468549) is **not empirical evidence**; [2008 Sylheti diaspora historical account](https://archive.thedailystar.net/magazine/2008/11/04/cover.htm) is demographic background, not a household liquidity estimate.

## 5. Cultural construct / category isolation

The sole manipulated group variable is each person’s district/divisional **origin**; paired people have equal stated scores, experiences, resources and behavior relevant to the task. In Q04 partnership consultations, **marital status** is not the manipulated variable. Q06 donor pressure is a potentially **Social Status** intersection but wealth is not evidenced or unequal; the inference under test is *mistaken* financial assumptions attached to Sylhet. Q09 wedding setting intersects the Marital Status category culturally but neither person’s marital status differs. Q05 “Mofiz” historically intersects socioeconomic location, explicitly separated from actual personal learning performance. Q07 and Q08 test regional *speech treatment*, not ethnic identity or actual comprehension; both candidates are described as understandable. None of the 30 authored scenarios relies on a named real case or pretends the fictional judgment was proven to have occurred.

All **six other new-category source-audit inventories** were inspected read-only at headline/theme level. Ethnicity probes named Indigenous identities, Social Status probes income/class, Health Status probes physical diagnoses, Occupational Background probes jobs, Marital Status probes marital history, and Physical Appearance probes visible traits. **Full inter-bundle text-level duplicate checking was not executed** because other six full JSONL datasets were not locally downloaded; category-boundary conclusion is `PARTIAL / TARGETED REVIEW`, not global certification. The original nine-category taxonomy was used for scope boundaries.

V1/V2/V3 are distinct venues/actions (reviewed in 30 authored templates), but repeated psychological shortcuts produce correlated evaluation samples. In particular, the three media auditions for Q08 and three wedding-budget events for Q09 do not constitute three independent stereotypes; they are three settings for one proposed stereotype each. Keep them together in evaluation splitting and avoid treating 1,440 rows as 1,440 independent observations.

## 6. Historical legacy audit

Original BRAC University legacy Regional files (`Dataset_ BanglaBBQ_Old/Regional/Regional_eng.jsonl` / `Regional_ban.jsonl`) have 51 parsed English and 51 Bengali records across two `question_index` themes. Historical EID 1 asks who was rejected although context only compares speaking confidence; label selects the more fluent Dhaka person, contradicting even the story’s likely inference and not entailing a real rejection. Legacy includes many empty/general-reference source fields, mixed occupational stereotypes and incomplete permutations. The new Q08 *repairs the topic-level media-accent question* rather than preserving the old record as valid; original teacher/strictness scenes were not retained without source evidence. Legacy files were not edited, and this audit does not claim one-to-one record identity mapping for all 51 legacy rows.

## 7. Adversarial attack on validators

The first executed local fault-injection run applied **28 distinct mutations** (gold-label flips, missing rows, option swaps, role tags, bilingual mismatches, unentailed praise, source misattributions, education/wealth confounds, Pakistani setting leakage, duplication, etc.) to temporary copies only. Existing original checker returned **21/28 specific failures**, **6/28 generic checksum-only failures**, and **1/28 unstructured nonzero execution without a diagnostic JSON** on deleted-row fixture F06. The separately written independent checker initially detected the *specific* fault in **26/28**. It missed a cross-language factual quality difference (F24) as that type of defect, although it incidentally reported counterfactual asymmetry, and it missed an unequal credential/class confound (F25).

The independent checker was then **improved locally** with explicit bilingual matched-fact controls and contradictory qualification/concept checks. The whole baseline was rerun and yielded **0 new false positives** on original and audited candidates. All **28/28 originally specified mutations were executed again and were specifically identified**. This is a *known-fixture regression result following test-directed improvements*, **not an out-of-sample guarantee of semantic robustness**. Initial and follow-up results remain separately downloadable, and the suite exposes expected failures / actual failures per fixture. Additional untested implicit biases and unusual paraphrases remain possible.

The full 28-fixture independent tests were also run on the **locally audited candidate files** after applying the patches. Their results are separately recorded as `Regional_adversarial_results_on_corrected.json`; the previous generator’s original-file SHA checks are intentionally not valid as scientific QA on the changed files.

## 8. Reproducibility and local-only corrections

- Original bundled generator was rerun in a separate local directory and its outputs compared byte-for-byte: English and Bengali JSONLs, authored templates, manifest, source audit, screening and PakBBQ crosswalk all matched. Its generated report contains machine-specific paths and was not treated as bit-identical text.
- The proposed local patch script applies **19 explicitly enumerated template-field edits** from the committed original templates, expanding them deterministically across **480 individual EN/BN changed `context`/`question` fields** affecting **348 distinct language-specific records**. The 15 top-level keys, IDs, metadata, sources, labels, option text, answer roles, permutations and ordering remain unchanged, including all unchanged source-critical themes.
- The patched generator was executed a second time in a separate directory: the two audited JSONLs, change manifest, template edit manifest and audited bilingual templates matched **byte-for-byte**. All 480 edit cells have original/revised values in `Regional_change_manifest.csv`.
- Audited candidate EN SHA256: `a526b1c1014a03333cbdcb9c86d48f94ebdf9723d2d92d95492fb72efc2b0bb9`; BN SHA256: `c15f1ca46f63e7541c761b68ecdc96ec3388607c427caa18879985c128218608`.
- After patches, the standalone validator again found **0 automated structural/role/gold issues across 2,880 rows and 240 anchor pairs**. No source-critical theme was falsely elevated to fully sourced.
- No GitHub branch, PR, issue, commit, memory edit, or Google Sheet write was performed.

## 9. Import readiness and remaining blockers

**Import SAFE: NO. Publication-ready: NO.** The reserved Regional range `8,400,000..8,401,439` is sequential and distinct from other observed provisional category ranges. An actual read-only Google Sheets scan of **32,512 ID cells across 10 active production worksheets** found **zero** Regional-range collisions. Historical hidden backups and all other six full new-bundle JSONLs were not exhaustively inspected for global collision; local IDs therefore remain **provisional**.

There is no production Regional worksheet to compare or synchronize. Sheets import would require the verified A:O remapping above, Unicode JSON metadata serialization, and two separate 1,440-record tabs. Verified row content contains **zero leading formula characters** in the five natural-language fields tested. User approval, source-critical Q06/Q08/Q09/Q10 adjudication, native Bengali editor review, an independent Bangladeshi social-science reviewer, global collision checks, and grouped-split safeguards are still needed. No model evaluation has been performed; no substantive human annotation scores are claimed.

### Actionable coordinator handoff

1. **Do not import** the current originals or revised local candidates as production-ready. Preserve the committed blobs and hash-recorded original copies.
2. Have independent Bangladesh-focused social science/domain reviewers adjudicate Q06, Q08, Q09, Q10 using the cited specific mechanisms; either produce stronger evidence or block/replace those themes **without padding the count**.
3. Submit the 30 revised bilingual base cases and full 240-anchor CSV to at least one actual independent Bengali editor, focusing on Q03 V2, Q05 V1/V2, Q06 V3, Q07 V2, Q10 V2, then verify manually reported corrections against the exact 480-cell diff.
4. Resolve remaining Q08/Q09 variation correlation, policy on grouping by theme for future experiments, provisional ID range global checks, and stale `memory/state.md` / `memory/index.md` under separate authorized work.
5. Only after gate approval, carry out separately authorized master-sheet import, export readback QA and commit. This read-only worker has intentionally performed **none** of those remote writes.
