#!/usr/bin/env python3
import csv,json,collections,hashlib,subprocess,sys
from pathlib import Path
P=Path('/mnt/data/marital_forensic_qa');O=P/'ORIGINAL'
orig=json.loads((P/'work/independent_initial.json').read_text());fin=json.loads((P/'work/independent_postfix.json').read_text());adv=json.loads((P/'marital_status_adversarial_results.json').read_text());repr=json.loads((P/'work/reproducibility_summary.json').read_text());repo=json.loads((P/'marital_status_repo_snapshot.json').read_text());read=json.loads((P/'marital_status_import_readiness.json').read_text());m=json.loads((O/'banglabbq_marital_status_expansion_manifest.json').read_text())
with (P/'marital_status_issue_ledger.csv').open(encoding='utf8',newline='') as f:issues=list(csv.DictReader(f))
with (P/'marital_status_source_evidence_matrix.csv').open(encoding='utf8',newline='') as f:sources=list(csv.DictReader(f))
with (P/'marital_status_change_manifest.csv').open(encoding='utf8',newline='') as f:changes=list(csv.DictReader(f))
with (P/'marital_status_semantic_anchor_review.csv').open(encoding='utf8',newline='') as f:anchors=list(csv.DictReader(f))
assert len(anchors)==240;assert len(sources)==10;assert len(changes)==1320;assert len(adv['fixtures'])==39
severity=collections.Counter(x['severity'] for x in issues)
clusters={s:sorted(set(x['issue_id'] for x in issues if x['severity']==s)) for s in ('P0','P1','P2','P3')}
status=collections.Counter(x['status'] for x in issues)
source_count=collections.Counter(s['evidence_tier_independent'] for s in sources)
failed_orig=collections.Counter(x['test_id'] for x in orig['row_failures'])
assert len(orig['row_failures'])==96 and len(fin['row_failures'])==0
from itertools import chain
# Exact full 15 key schema in original JSONL vs A:O sheet
headers=m['spreadsheet_headers']
source_rows='\n'.join(f"| {s['question_index']} | {s['theme']} | {s['evidence_tier_independent']} | {s['decision']} |" for s in sources)
issue_rows='\n'.join(f"| **{severity_id}** | {len(clusters[severity_id])} | {severity[severity_id]:,} | {', '.join(clusters[severity_id])} |" for severity_id in ('P0','P1','P2','P3'))
report=f'''# BanglaBBQ Marital Status — Independent Forensic QA Report

**Audit date:** 26 October 2026 (Asia/Dhaka). **External access: READ-ONLY.** No GitHub/Google Sheets edits, commits, issues, PRs, uploads, memory updates, or other remote writes occurred.

## Executive verdict

- **IMPORT SAFE: NO. PUBLICATION READY: NO.** Corrected local JSONLs are **structurally valid but SOURCE/CONSTRUCT REVIEW BLOCKED**. The current category remains a *research candidate*, not a scientifically certified import.
- The **unchanged committed original** has exactly **1,440 English and 1,440 Bengali records**, 10 themes, 3 variations/theme, 48 rows/variation. All 2,880 JSONL records are structurally valid under the independent validator. **But the original fails 96 row-level semantic-entailment tests in three issue families** that the generator's own validator missed.
- **240 unique bilingual semantic anchors** (30 scenarios × 2 demographic orientations × 4 condition/polarity states) were independently AI-self-reviewed; the other 2,640 positional permutations were mechanically validated. **No external human reviewer was involved.** Thirty variations and all sixty orientation-specific base situations were checked by reading EN/BN contexts and event clauses; the 240 paired anchor files preserve each full context and question for scrutiny.
- **Local candidate repairs:** {len(changes):,} changed fields across both languages, of which 144 semantic P0 text edits, 24 Bengali P2 clarity edits, and 1,152 P1 citation-provenance edits. The 2,880 corrected rows subsequently return **zero failures** under the independent machine assertions. **The scientific source caveats still remain.**
- Theme evidence classification: **{source_count['DIRECT']} DIRECT (Q01–Q03), {source_count['PARTIAL/CONTEXTUAL']} PARTIAL/CONTEXTUAL (Q04–Q10), 0 unsupported beyond-the-source theme candidates accepted as verified.** Seven require adjudication. 

## 1. Actual version, repository synchronization and byte identity

| Fact | Verified value |
|---|---|
| Repository branch | `Hasinish/Research-BanglaBBQ` → `main` |
| **Audited commit** | `{repo['main_sha']}` (2026-10-26 06:18 UTC) |
| Seven-bundle predecessor commit | `{repo['seven_bundle_commit_sha']}` |
| Committed package | `banglabbq_marital_status_readonly_research_package/` |
| Original English JSONL Git blob | `{repo['git_blob_sha']['english']}` |
| Original Bengali JSONL Git blob | `{repo['git_blob_sha']['bengali']}` |
| Original English SHA-256 | `{repr['local_original_sha256']['english']}` |
| Original Bengali SHA-256 | `{repr['local_original_sha256']['bengali']}` |
| Audited English SHA-256 | `{repr['candidate_sha256']['english']}` |
| Audited Bengali SHA-256 | `{repr['candidate_sha256']['bengali']}` |

The six key original local files were checked with actual `git hash-object`; blob identities exactly match the **committed main tree**, not merely a previous chat attachment or an unverified label. The project-memory README/purpose/state/index/history were freshly read. `memory/state.md` reflects the bundle push but retains an older (20 Oct) Last Verified Date and still shows the historic Marital Status task as pending; `memory/index.md` does not list the newly committed seven bundles. **Those memory files were not edited.**

The current live workbook does **not** have a Marital Status working worksheet; comparing the candidate to a nonexistent live tab would be false parity. Read-only headers/examples from `BanglaBBQ_ENG_Education` and `BanglaBBQ_ENG_Politics` confirm 15 Google Sheets A:O columns in order:

`{', '.join(headers)}`.

These **differ** from JSONL key order:

`{', '.join(m['schema_keys'])}`.

Import must serialize `answer_info` and `additional_metadata` objects as JSON cell strings and map A:O deliberately; blind JSONL-key-order paste is wrong.

## 2. Executed test matrix

| Test group | Actual denominator and method | Original | Locally audited | Limit |
|---|---|---|---|---|
| UTF-8/JSONL schema/types/order | 2,880 JSON objects × all 15 keys and nested checks | PASS | PASS | No malformed/blank/zero-width/CSV-injection characters found |
| 10×3×48 factorial structure | 60 language-specific 48-row blocks; 120 orientation subblocks; 720 four-condition permutation blocks | PASS | PASS | Exactly two orientations per block |
| Option permutation balance | Each (wave,theme,orientation,language) all six permutations; 720 positional condition blocks | PASS | PASS | Intended permutations not counted as duplicates |
| IDs and labels | All 2,880 rows, range `8700000–8701439` each language; labels 480/480/480 | PASS | PASS | IDs remain provisional |
| Source URL syntax and metadata | 2,880 records; URLs parsed and matched to manifest source catalog | PASS | PASS | Syntax/manifest matching is **not** source relevance proof |
| Unknown/label roles and evidence-position | 720 ambiguous and 720 disambig per language; blind event-clause actor-position checks | PASS | PASS | Event-order heuristic not a substitute for predicate adjudication |
| **Independent semantic entailment** | **240 bilingual EN/BN anchors** reviewed; all 2,880 permutations rechecked | **FAIL: 96 row-level failures** | PASS for repaired predicates | AI self-review, not human-certified; some source/construct risks remain |
| Bilingual identity/structural parity | 1,440 aligned pairs; metadata, entity/answer mapping, locations, status terms | PASS | PASS | AI semantics can miss pragmatic nuances |
| Exact QA tuples / counterfactuals | 2,880 complete tuples and **1,440** paired a↔b counterfactual surface comparisons | PASS | PASS | Causal selection effects cannot be inferred from fictional balanced pairs |
| Variant diversity / family leakage | 30 variation contexts + same-theme action/setting/question comparisons | PARTIAL | PARTIAL | V1/V2/V3 repeat many outcome predicates, though settings/actions differ |
| Bangladesh-specific source audit | **5 unique original audit URLs**, 10 themes, full available web text/sections checked | PARTIAL | PARTIAL | Q04–Q10 weak comparator/population matching |
| Upstream PakBBQ baseline | Current main tree and 3 smaller adjacent datasets fully read; 5 larger paths inaccessible at audit | PARTIAL | PARTIAL | `NO_DIRECT_EQUIVALENT` established at category-path level, not all adjacent content |
| Adversarial validators | **39 actually executed isolated fault injections**, 31 normal + 8 paired/balanced | PARTIAL | PARTIAL | 8 independent automated false negatives; AI probes are targeted, not general |
| Generator and local repair reproducibility | Original generation + repair in fresh temp directory; two language byte comparisons + diff manifest; 60 row-map entries | PASS | PASS | Must apply **separate patch script** to original seed generator |
| Live IDs / global collisions | 10 active language tabs, **32,512** ID cells read; six additional provisional ranges inspected as manifests | PARTIAL | PARTIAL | 0 active-tab collisions; full across-all-bundles data scan not executed |
| Independent human bilingual / cultural review | 0 real human reviewers | BLOCKED | BLOCKED | `INDEPENDENT_HUMAN_REVIEW=NO` |

### Numeric invariants re-computed

Per language: 10 distinct `question_index` values × 144 rows; 3 variations × 48 rows; 720 each ambiguous/disambiguated, 720 each neg/nonneg; 4 combined conditions × 360; answer labels `{{0:480,1:480,2:480}}`; 720 records each version `a` and `b`; 1,440 unique complete QA tuples. Exactly 60 orientation-and-variation groups per language with six complete permutations each. Bilingual `example_id`, `id`, group tags, sources and metadata all agree one-to-one.

Across **360 disambiguated negative rows per language**, each theme places its stereotyped group in the adverse-answer role in **18 out of 36** examples (and the comparison group in 18/36); there is no systematic association of adverse *facts* with only the target status. Ambiguous answers are Unknown in all 720/language. The disambiguation evidence tells us who was acted upon; it **does not establish the social cause** of the fictional decision.

## 3. Discoveries: actual defects, severity, exact examples

Counts below are **issue clusters** and **ledger rows**, not independent scientific findings. A source-scope defect that affects 288 EN/BN records is intentionally entered on those precise lines. Many rows carry multiple separate issues.

| Severity | Unique issue clusters | Issue-ledger rows | IDs |
|---|---:|---:|---|
{issue_rows}

**P0 local semantic repairs** (all recorded per affected field in `marital_status_change_manifest.csv`):

1. **Q01 V3 — EID 963 / ID 8700963 and all corresponding orientations and permutations.** Original positive question asked who was *offered* a rental, but disambiguation said the room was merely *reserved*. Reserving a room does not entail a rental offer. Locally corrected EN + BN to explicitly state rental refusal and actual offer; 48 context fields changed.
2. **Q03 V3 — EID 1059 / ID 8701059.** Question attributed the description to building *staff* but the narrator identifies a building *committee member*. A member need not be staff. Locally corrected both questions to the committee member; 48 question fields changed.
3. **Q06 V3 — EID 1201 / ID 8701201 and negative contexts.** Both language questions originally asked who received a proposition *at work*, whereas the base premise described trainees in a retail-training center; their employment/workplace was not established. Locally asked who received the proposition **while requesting the evaluation appointment**; 48 question fields changed. The original question risks an unsupported presupposition and wrong disambiguated gold interpretation.

**P2 locally repaired:** Q02 V3 — EID 1009 / ID 8701009. The Bengali narrative merely instructed a person to obey ordinary rules; English explicitly exempted her from extra restrictions. Fixed Bengali to explicitly **permit standard-policy treatment without extra restrictions** (24 disambiguated Bengali context fields).

**P1 provenance remediation:** Q04–Q07, all waves and orientations, **1,152 `additional_metadata.source` values** (576 per language) changed locally from `10.1186/s12905-022-02088-z` to `10.1163/27715086-20250002`. The former is a nationwide child-marriage/disruption/remarriage analysis and does **not** measure these four exact social outcomes; the latter reports firsthand qualitative accounts of blame, isolation, remarriage pressure and unwelcome propositions in Khulna. This is a better **relevance match**, **not** proof of all the benchmark's fictional cases, matched comparison groups or other city settings.

**High-priority unresolved blockers** (retain the correct group IDs and avoid silent unsupported invention):

- **Q04** — EID 144 / 8700144: Studies of post-divorce blame do not directly support labeling someone irresponsible in a recycling/volunteer evaluation. General character stigma versus task-specific competence is a construct leap.
- **Q05** — EID 192 / 8700192: General social exclusion does not document an otherwise eligible individual's omission from an event invitation list as a marital-status decision.
- **Q06 V2/V3** — EIDs 720–767 and 1200–1247: A documented garment worker's unwelcome proposals do not establish the same mechanism in Dhaka office payroll or Chattogram trainee evaluations, nor a controlled comparison with married peers. V3 wording has been repaired but evidence scope has not.
- **Q07** — EID 288 / 8700288: Family/community pressure to remarry divorced women is documented, but the study does not compare an equally situated widowed woman refusing remarriage.
- **Q08** — EID 336 / 8700336: Wedding exclusion in a **tiger-widow** sample should not be applied uncritically to all widowed women; the candidate has only generic widowhood in its scenario.
- **Q09** — EID 384 / 8700384: The same population mismatch applies to local decision-making exclusion; simulated elected committee rights are new controls, not observed survey facts.
- **Q10** — EID 432 / 8700432: In addition to the tiger-widow generalization, the category title says employment denial was justified by a **superstition**, but no fictional employer actually states that motive. Rejection does not entail superstition-based causation.
- **Q01/Q03/Q04/Q07/Q10 family**: V1/V2/V3 change venue and evaluator but largely reuse the same question and outcome predicate, creating related-case leakage if randomly split by rows. Use family/group-wise train–test split and cluster-robust reporting. An apparent 144-row/theme sample is not 144 independently sourced stereotypes.
- **Coverage limitation:** All 10 themes concern pairs of women. Findings cannot generalize to divorced/widowed/unmarried men or separated/remarried adults. That sampling choice also limits general construct coverage.

## 4. Ten-theme independent source evidence matrix

| Q | Mechanism / theme | Evidence tier | Independent decision |
|---|---|---|---|
{source_rows}

**Five independently opened source URLs and actual support:**

1. **UK Home Office Bangladesh country note** (updated 28 Apr 2026), [official source](https://www.gov.uk/government/publications/bangladesh-country-policy-and-information-notes/country-policy-and-information-note-women-fearing-gender-based-violence-bangladesh-january-2024-accessible). Cites Bangladesh reporting on single women's difficulty obtaining housing and social restriction; it is a secondary source with **no randomized married-vs-unmarried rental experiment**.
2. **Aynun Nahar Esha, The Business Standard, 15 Jan 2026**, [housing feature](https://www.tbsnews.net/features/panorama/hurdles-living-alone-single-young-woman-dhaka-1334591). Reports cases of refusals to rent to unmarried women, restrictions on visitors/rooftop access and gossip by housing personnel; also describes a supportive landlord. Supports Q01–Q03 as **documented allegations/experiences, not universal facts**.
3. **M. Mofizul Islam, 2022, BMC Women's Health**, [national survey analysis](https://link.springer.com/article/10.1186/s12905-022-02088-z). Analyzes first marriage timing, marital disruption and remarriage in Bangladesh MICS data (n=57,476). The dataset's particular labels about social exclusion, harassment and invitations are **not estimated outcomes** of the survey. Supplemental discussion about stigma cannot substitute for direct comparison evidence.
4. **Ety Rani and Sumya Sultana, 2025, Journal of Bangladesh Studies**, [DOI/full article](https://doi.org/10.1163/27715086-20250002). Primary interviews with **13 women** of modest socioeconomic background from four wards in Khulna, August 2022. §3.2 directly describes family/neighborhood blame, pressure to remarry and one garment worker's unsolicited proposals. §5 explicitly cautions that the findings **cannot be nationally generalized**. It does not show paired married comparators.
5. **Md. Al-Mamun et al., 2025, Humanities and Social Sciences Communications**, [Nature study](https://www.nature.com/articles/s41599-025-05988-1). Qualitative interviews with **27 tiger widows** in particular Sundarbans communities; discusses weddings, employment and social decision-making exclusion related to stigma. **Tiger widowhood is a narrower causal population than generic widowhood** in Q08–Q10. Even a nationally representative ordinary widow sample would not make the fictional incident factual.

`DIRECT` denotes a study/report documenting a relevant prejudice mechanism in Bangladesh **within its studied population**. It does not imply causal controlled evaluation or validated frequency. `PARTIAL/CONTEXTUAL` means there are real related phenomena, but the exact group, population, comparison, decision or mechanism is unproven. No inaccessible publication was quoted as directly inspected.

**PakBBQ crosswalk:** Upstream main tree SHA `c079dbae2d676f4e3bb82982144d6d4ac10436d4` has **no standalone Marital Status dataset**, hence `NO_DIRECT_EQUIVALENT`. Adjacent files actually parsed: Regional 944 records/18 indices, Religion 400/25, English formality 88/11; none contained explicit marital-status terms. Other large upstream files, particularly **Gender Identity** and **SES**, were not exhaustively retrieved. Their themes remain `UPSTREAM_CONTENT_UNVERIFIED`; absence is **not** asserted. PakBBQ is a design baseline, not evidence of Bangladesh-specific prevalence. The main committed source-audit and crosswalk artifacts are preserved unchanged in `ORIGINAL/`.

## 5. Bilingual linguistic, construct, and cultural assessment

**Review provenance:** `AI_LINGUISTIC_REVIEW_COMPLETED=YES (AI_SELF_REVIEW)`. `INDEPENDENT_HUMAN_REVIEW=NO`. Naturalness/cultural-fit scores appear **per anchor** in the companion CSV and are not external-native certifications.

We read all 30 EN+BN base variants, both a/b demographic orientations and both outcome event clauses, and recorded 240 bilingual anchor contexts/questions and paired choices. Full positional permutations were mechanically replayed for all 2,880 rows. The two languages consistently use **unmarried/অবিবাহিত, married/বিবাহিত, divorced/বিবাহবিচ্ছিন্ন, widowed/বিধবা** while preserving person transliterations and question polarity. Both sexes were not varied: every named candidate is a woman, so the held-constant gender is intentional but limits construct breadth.

- **Observed material BN disparity:** Q02-V3 Bengali had the agent *tell someone to obey the ordinary rules*, not explicitly *permit/allow* normal-policy treatment as the English had; corrected locally in context, maintaining the same answer-role ordering.
- **Observed question-agent disparity in both languages:** Q03-V3 used “building staff/ভবনের কর্মী” when the evaluating person was “committee member/কমিটির সদস্য”; fixed as an entailment defect, not just a style preference.
- **Observed locative/presuppositional disparity:** Q06-V3 trainees at a retail-training center were said to receive harassment *at work*; removed the unsupported workplace premise in both versions.
- **Naturalness considerations:** The Bengali phrasing is generally intelligible and formal-neutral. Q02's “only standard residence rules” abstraction is stilted across three different visitor/roof/curfew situations; exact action-specific paraphrases are preferable after approval. Some V1–V3 variations share identical English/Bengali question stems, which is a methodological correlation as well as a style issue.
- **Context specificity:** Q08–Q10 cultural-fit ratings of 3/5 (not 4+) for V3 mark broader Satkhira/Shyamnagar descriptions against study communities; these cases remain **blocked** rather than made publication-ready by polishing language.

**Counterfactual and taxonomy verdict:** English/Bengali surface comparisons swap only the marital-status attribute, retain female gender, identical age/skill/financial constraints per scenario, and preserve the same named actors and decisions across a/b. All 1,440 within-language comparisons passed mechanical surface checking. However, the referenced studies generally do not include those matched married/comparator groups. Q06 also probes gendered sexual harassment (related to Gender Identity but paired gender is controlled), Q04 competence labels overlap occupational stereotypes, and Q08–Q10 integrate coastal tiger-bereavement with widowhood. Verdicts: Q01–Q03 **IN_SCOPE** with urban gender-population scope; Q04–Q07 **INTERSECTIONAL_BUT_CONTROLLED** in prompt text but **SOURCE_PARTIAL**; Q08–Q10 **CONFOUNDED_BY_SOURCE_POPULATION**, especially if interpreted as generalized widowhood. No extrapolated causal population claims are approved.

## 6. Adversarial fault-injection results — executed, not hypothetical

`marital_status_adversarial_suite.py` ran 31 mutations; `marital_status_adversarial_paired_suite.py` then ran eight stronger paired/balance-preserving mutations. Mutation files existed **only in disposable local directories**, which were removed. Each was evaluated by the original generator's `check()`, our independent `run()`, and a targeted AI semantic/source probe where applicable. Complete actual results and per-fixture failure codes are in `marital_status_adversarial_results.json`.

- Executed fixtures: **{adv['executed_fixture_count']}**.
- Detected by previous generator: **{adv['aggregate_detection']['legacy_generator_detected']}/39**; **{adv['legacy_false_negatives']} original-check false negatives**.
- Detected by independent automated validation: **{adv['aggregate_detection']['independent_validator_detected']}/39**; **{adv['independent_automated_false_negatives']} independent machine false negatives**.
- Detected by targeted AI expert probes: **{adv['aggregate_detection']['AI_expert_probe_detected']}/39**; several overlap with machine findings.
- Combined **{adv['aggregate_detection']['combined_detected']}/39 identified**; baseline original and repaired datasets had **zero automated false positives on the unmutated pass**. **This is not proof that all possible semantic errors can be detected**. Some fixtures were constructed to expose a specific known unsupported predicate or source-population issue.

**Notable detector blind spots:** Balanced paired wrong gold labels can escape the old check; both validators failed some *unentailed praise*, *different-gender comparison*, *3 p.m. vs 8 p.m. BN/EN mismatch*, and *irrelevant criminality mechanism* attacks until targeted AI reasoning checked those claims. These adversarial tests demonstrate why a PASS from structural tooling cannot be interpreted as human/semantic certification.

## 7. Historical lineage, reproducibility and import readiness

**Legacy:** The frozen BRAC thesis Marital Status category has **100 valid English + 100 Bengali rows**, all under one `question_index`, with restricted answer-option order and 25/50/25 labels. Every row references [PMID 29307947](https://pubmed.ncbi.nlm.nih.gov/29307947/), a U.S. substance-use-treatment stigma study that does **not** support the Dhaka married/unmarried work-event flexibility claims. Historical rows remain unmodified, and **none of the 100 were copied verbatim**; the current benchmark is an explicitly traced *repair/replacement expansion*, not a continuation of 100 already-validated records. The original scope primarily over-inferred family caregiving from marriage.

**Reproducibility actually executed:**

- Frozen unedited seed files have the exact current Git blob identities and SHA-256s listed above.
- The original generator, run in an empty local directory with committed manifest/crosswalk, returned **code 0** and produced **byte-identical original EN/BN JSONL files**.
- `marital_status_apply_local_repairs.py`, run in a separate temporary directory on those regenerated originals, returned **code 0** and produced **byte-identical corrected EN/BN JSONL files** plus an **identical 1,320-row change manifest**.
- **60 manifest `row_map` entries** (30 variants × a/b) checked against revised EIDs, ranges, category tokens and group-version metadata; **0 mapping failures**.
- Running the original generator's own `check()` on both original and audited records returns 0 failures, despite that validator missing the three original semantic flaws. Running the **separate** independent validator reports **96 original row-level semantic failures** before repair and **0 after repair**.
- **No new seed manifests were silently presented as current canonical GitHub truth.** The committed generator alone would regenerate the old defects; the additional local patch step is mandatory to reproduce the candidates. Merge/replace original manifest templates **only after authorization and review**.

**Import-readiness gate:** `NOT_IMPORTED / NOT_SAFE_FOR_IMPORT`. Verified no Marital tabs in the live workbook. Current active production sheets (Age, Politics, Religion, Education, Gender; two languages each) were checked via read-only Col O for **32,512** populated IDs, with **0 collisions** in reserved `8700000–8701439`. The six other proposed category ranges were observed in committed metadata/manifests but the entire combined 7-category JSONL population was **not** exhaustively scanned in this session. Thus “globally collision-free and approved” would overstate the verification. The corrected data use proper 15-key JSONL schema and all 15 spreadsheet columns can be serialized but the 10 themes still lack human linguistic certification and seven have source/construct qualification blockers.

## 8. Prioritized instructions for the eighth QA coordinator

1. **Reject live import for now.** Review 7 source-partial themes, especially Q08–Q10's tiger-widow-to-all-widows extrapolation and Q10's unobserved superstition motivation. Do not presume the seven approved local source citations establish differential causal social treatment.
2. **Adjudicate Q04, Q05, Q06 V2/V3 and Q07 independently** against Bangladesh-specific reporting. Supply directly relevant comparator evidence or *revise/reduce/remove* affected theme families; **do not preserve 1,440 rows by weak padding**. Human reviewers must review actual EN+BN text, not assert certification from AI-generated scores.
3. **Use the corrected local candidates only for the next review stage** and do not overwrite committed originals. Verify the 1,320-row patch manifest, decide whether the Q04–Q07 DOI metadata improvement is authorized, then revise canonical generator seed and provenance once accepted.
4. **Fix evaluation design** by splitting entire scenario/theme families across train/test folds, not individual 6-way option permutations or superficial V1/V2/V3 variants. Add reviewer-approved group-balanced coverage beyond women if primary evidence is available.
5. Run a **global across-seven-bundles ID collision scan** and obtain explicit Google Sheets import authorization, then import into dedicated English and Bengali Marital Status sheets with precise A:O mapping, backup, sparse readback and versioned GitHub synchronization. None of these remote actions occurred in this audit.

## Evidence and deliverables

Attached per-row issue ledger (5,473 entries), 240 paired EN/BN anchor reviews with raw/corrected contexts, ten-theme source matrix, 30 variation-diversity matrix, 39-mutation adversarial output, independent validator, local repair script, reproducibility run summary and precise change manifest are part of the ZIP. This report is an **AI self-review** supported by real executed scripts and opened web documents, **not** an independent human editorial or social-science validation.
'''
(P/'marital_status_independent_forensic_QA_report.md').write_text(report,encoding='utf8')
post=f'''# Marital Status — Post-fix QA (LOCAL-ONLY, NOT PUBLICATION READY)

**GitHub source commit:** `{repo['main_sha']}`. No remote writes. Original committed files unchanged.

- English audited rows: {fin['checks']['en_count']}; Bengali audited rows: {fin['checks']['bn_count']}.
- Full 15-field schema, 10×3×48, a/b, 4 conditions, all 6 permutations, label counts 480/480/480 per language: **PASS**.
- Independent machine row-level failures: **{len(fin['row_failures'])}** (down from {len(orig['row_failures'])} original failures in three semantic defect test IDs). This count does **not** include source-evidence/construct residuals.
- Complete QA tuple duplicates: **0** per language; 1,440 unique per language.
- Original local audited-patch changes: **{len(changes)}** fields; category and IDs untouched; separate exact change manifest exists.
- Source evidence: {source_count['DIRECT']} DIRECT-within-population and {source_count['PARTIAL/CONTEXTUAL']} PARTIAL/CONTEXTUAL; Q04–Q10 require independent expert support or narrowing.
- 240 AI-reviewed bilingual anchors (30 thematic variants × 2 orientations × 4 cases), 39 executed mutation fixtures. `INDEPENDENT_HUMAN_REVIEW=NO`.
- Audited SHA256 English `{repr['candidate_sha256']['english']}`; Bengali `{repr['candidate_sha256']['bengali']}`.
- Original generator in a fresh directory produced identical originals; fresh patch step produced identical audited candidates and diff manifest. Source seeds are unchanged, so generator **without** patch regenerates the original semantic defects.
- **Import verdict: NO**. No Marital Status spreadsheet tabs currently exist; full cross-bundle global collisions and independent human linguistic review are pending. Source population mismatch (27 tiger widows, not generic widows) unresolved.
'''
(P/'marital_status_postfix_QA_report.md').write_text(post,encoding='utf8')
runlog=f'''# Actual local reproducibility and execution log (2026-10-26)

Scope: 2,880 committed Marital Status JSONL objects; GitHub and Sheets strictly read-only. Python standard library, no live writes.

1. Current `main` SHA `{repo['main_sha']}` and seven dataset Git blob/object IDs obtained with read-only connected GitHub and `git hash-object` over local immutable files. Each hash agreed.
2. `python marital_status_independent_validator.py --english ORIGINAL/banglabbq_marital_status_english.jsonl --bengali ORIGINAL/banglabbq_marital_status_bengali.jsonl --manifest ORIGINAL/banglabbq_marital_status_expansion_manifest.json --out work/independent_initial.json --row-failures work/automated_row_failures.csv` → **96** row failure checks, **3** semantic detector IDs, 0 structural-only defects.
3. `python marital_status_apply_local_repairs.py --english ORIGINAL/banglabbq_marital_status_english.jsonl --bengali ORIGINAL/banglabbq_marital_status_bengali.jsonl --outdir .` → **{len(changes)}** local field updates; source ID/category/gold labels unchanged.
4. `python marital_status_independent_validator.py --english banglabbq_marital_status_audited_english.jsonl --bengali banglabbq_marital_status_audited_bengali.jsonl --manifest ORIGINAL/banglabbq_marital_status_expansion_manifest.json --out work/independent_postfix.json --row-failures work/automated_row_failures_postfix.csv` → **0** row failures.
5. `python marital_status_adversarial_suite.py` → 31 actual baseline isolated mutations. `python marital_status_adversarial_paired_suite.py` → 8 further paired/balanced mutations; **39/39** identified by machine and/or specific AI expert probes, **{adv['independent_automated_false_negatives']}** independent machine false negatives; `marital_status_adversarial_results.json` records all per-fixture evidence.
6. `python work/verify_reproducibility.py` → original generator return code 0, original EN/BN byte identity TRUE, patch script return code 0, corrected EN/BN byte identity TRUE, change manifest byte identity TRUE, 60/60 manifest row maps correct.
7. `python work/build_forensic_artifacts.py`, `python work/augment_issue_ledger.py`, `python work/finalize_auxiliary.py`, `python work/write_final_report.py` → 10-theme evidence matrix; 240-paired-anchor review; 5,473 exact issue-ledger entries; import readiness; repo SHA snapshots; reports. No claimed external human review.

Script-generated low-level outputs are also included under `work/` in the bundle. Original mutable-seed files are kept under `ORIGINAL/`; no independent human reviewer participated. The original generator check passes original and patched files even though the independent semantic audit found the three original semantic defect families.
'''
(P/'marital_status_reproducibility_run_log.md').write_text(runlog,encoding='utf8')
print(json.dumps({'report_length':len(report),'source_tiers':dict(source_count),'severity_ledger_rows':dict(severity),'issue_clusters':{k:len(v) for k,v in clusters.items()},'adversarial':adv['executed_fixture_count'],'anchor_reviews':len(anchors),'change_fields':len(changes)},indent=2))
