#!/usr/bin/env python3
from pathlib import Path
import csv,json,hashlib,collections,datetime,subprocess
R=Path(__file__).resolve().parent
O=R/'ORIGINAL'
HEAD='e186b283fa5b184058e2cb395273e9968a893b20'
PUSH='214795f628a34ece8deb23a65c6bf35ac0ce7157'
ST=json.load(open(R/'Ethnicity_forensic_statistics.json',encoding='utf-8'))
ADV=json.load(open(R/'Ethnicity_adversarial_results.json',encoding='utf-8'))
IR=json.load(open(R/'Ethnicity_import_readiness.json',encoding='utf-8'))
EV=list(csv.DictReader(open(R/'Ethnicity_source_evidence_matrix.csv',encoding='utf-8')))
AL=list(csv.DictReader(open(R/'Ethnicity_semantic_anchor_review.csv',encoding='utf-8')))
LE=list(csv.DictReader(open(R/'Ethnicity_issue_ledger.csv',encoding='utf-8')))

def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def write_csv(path,rows):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

# Verify all PakBBQ adjacent Regional questions against actual GitHub connector counts (944/18).
up_counts=[80,64,64,64,64,64,16,16,64,48,64,80,80,32,32,32,32,48]
with open(O/'banglabbq_ethnicity_pakbbq_theme_crosswalk.csv',encoding='utf-8',newline='') as f:rr=list(csv.DictReader(f))
up=[x for x in rr if x['record_type']=='upstream_theme']
assert len(up)==18 and sum(up_counts)==944
cw=[]
for x in up:
 i=int(x['upstream_question_index'])
 n=int(x['upstream_record_count'])
 assert n==up_counts[i-1]
 cw.append({'upstream_source':'PakBBQ/PakBBQ_ENG/Regional.jsonl','upstream_main_commit':'c079dbae2d676f4e3bb82982144d6d4ac10436d4','upstream_blob_sha':'c6d0a7a1b1ed9370eba23a2ec4c52369968fab87',
 'direct_standalone_ethnicity_category':'NO_DIRECT_EQUIVALENT; checked Ethnicity.jsonl -> 404',
 'upstream_question_index':i,'actual_upstream_rows':up_counts[i-1],
 'crosswalk_row_count':n,'count_matches_current_upstream':True,
 'actual_scenario_summary_checked':x['upstream_scenario_summary'],
 'upstream_groups_target':x['group_comparison_and_target_variable'],
 'upstream_citation_present_reported':x['upstream_citation_available'],'original_crosswalk_decision':x['decision'],
 'BanglaBBQ_theme_mapping':x['proposed_BanglaBBQ_mapping'],
 'independent_decision':'ADAPT_QUALIFIED_Q03' if i==7 else x['decision'],
 'independent_analogy_assessment':'Q03 quota merit/stigma plausible after independent Bangladeshi Chakma source check, not proof of any fictional event' if i==7 else 'Rejected/limited as noted; no source supports generic transposition of Pakistani stereotypes to Bangladesh.',
 'upstream_access':'FULL_944_JSONL_CONNECTED_GITHUB_2026-10-26',
 'crosswalk_snapshot_warning':'Crosswalk mounted blob differs from committed GitHub CSV; connector preview checked; actual 18 upstream counts independently verified.'})
write_csv(R/'Ethnicity_pakbbq_independent_crosswalk_audit.csv',cw)

# Taxonomy boundary over 30 variants, independent of gold labels. Distinguishes identity from context.
boundary={
 1:('IN_SCOPE','Education/Regional','Peer ostracism triggered by ethnicity; grades and Bengali skills matched. Source community locality differs; do not use school location as group attribute.'),
 2:('INTERSECTIONAL_BUT_CONTROLLED','Educational Background','Academic assessment decisions are also education outcomes; all candidates have same university, previous marks, fluency. Need direct source on V2/V3 specific evaluator.'),
 3:('IN_SCOPE','Educational Background','Stigma about Indigenous quota merit is a claim about ethnic identity, even where selection is open and identical, not objective ability.'),
 4:('IN_SCOPE','Social Status/Regional','Income, employment, identification, budget and residence controlled; ethnic renter identity foregrounded. No causal trial data.'),
 5:('INTERSECTIONAL_BUT_CONTROLLED','Health Status/Gender','Pregnancy and clinical conditions are matched; test is ethnic care, not pregnancy risk or healthcare treatment recommendations.'),
 6:('CONFOUNDED','Social Status/Regional','Welfare eligibility and identity legal status may matter; equal need-based eligibility asserted fictionally but underlying source broad Indigenous, not Santal.'),
 7:('CONFOUNDED','Regional/Property legal rights','Mro ancestral customary tenure can differ legally from registered title regimes; avoid falsely interchangeable land paperwork and inferring discrimination.'),
 8:('CONFOUNDED','Politics/Regional/Institutional','Police violence source does not entail complaint-desk service bias; threats and evidentiary procedure appear matched only fictionally.'),
 9:('CONFOUNDED','Religion/Regional/Education','Heritage exhibits differ intrinsically by subject; source discusses Indigenous textbook identity, not Marma museum/radio and equal content selection.'),
 10:('CONFOUNDED','Politics/Social Status/Regional','General policy representation is not Marma-specific consultation hearing; academic/public authority venues differ, speaking time originally contradictory.')}
tax=[]
for q in range(1,11):
 for v in range(1,4):
  verdict,overlap,note=boundary[q]
  start=(v-1)*480+(q-1)*48
  tax.append({'theme':f'Q{q:02d}','variation':f'V{v}','example_ids':f'{start}..{start+47}','id_range':f'{8500000+start}..{8500000+start+47}',
  'ethnicity_isolation_verdict':verdict,'overlapping_existing_or_proposed_categories':overlap,'group_comparison':EV[q-1]['groups'],
  'specific_confounder_or_guardrail':note,'balanced_counterfactual_orientations':'YES_24_A_24_B_PER_VARIATION',
  'adverse_assignment_held_to_A_not_group':'YES_IN_ROLE_ASSIGNMENT',
  'intervention_recommendation':'RESEARCH_SOURCE_AND_CONTEXT_REDESIGN' if verdict=='CONFOUNDED' else 'KEEP_WITH_LOCALIZED_AND_INDEPENDENT_REVIEW',
  'independent_human_reviewer':'NO'})
write_csv(R/'Ethnicity_taxonomy_boundary_review.csv',tax)

# Transparent reproduction and execution log; commands have been run previously, now rerun safe checks.
cmds=[
 ['python','-m','py_compile',str(R/'Ethnicity_independent_validator.py'),str(R/'apply_justified_local_repairs.py'),str(R/'build_qa_artifacts.py'),str(R/'run_adversarial_ethnicity.py')],
 ['python',str(R/'Ethnicity_independent_validator.py'),'--en',str(R/'banglabbq_ethnicity_audited_english.jsonl'),'--bn',str(R/'banglabbq_ethnicity_audited_bengali.jsonl'),'--manifest',str(R/'Ethnicity_audited_expansion_manifest.json'),'--source-audit',str(O/'banglabbq_ethnicity_source_audit.csv'),'--templates',str(R/'Ethnicity_audited_scenario_templates.json'),'--quiet','--output',str(R/'postfix_final_rerun_validator_results.json')],
]
runs=[]
for cmd in cmds:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=str(R),timeout=45)
 runs.append({'argv':cmd,'returncode':p.returncode,'stdout':p.stdout[-600:],'stderr':p.stderr[-600:]})
 assert p.returncode==0,repr(p.stderr[-300:])
for a,b in [('banglabbq_ethnicity_english.jsonl','banglabbq_ethnicity_audited_english.jsonl'),('banglabbq_ethnicity_bengali.jsonl','banglabbq_ethnicity_audited_bengali.jsonl')]:
 aa=R/'audited_generation'/a;bb=R/b
 runs.append({'argv':['cmp','-s',str(aa),str(bb)],'returncode':0 if aa.read_bytes()==bb.read_bytes() else 1,'stdout':'local candidate vs re-generated from audited templates byte-identical' if aa.read_bytes()==bb.read_bytes() else 'DIFF','stderr':''})
 assert aa.read_bytes()==bb.read_bytes()
(R/'Ethnicity_local_repro_execution.json').write_text(json.dumps({'executed_utc_date':'2026-10-26','runs':runs,'prior_original_regeneration_byte_checks':json.load(open(R/'repro_compare.json')),'validator_fixture_batches_executed':[str(R/'adv_batch0.txt'),str(R/'adv_batch1.txt'),str(R/'adv_batch2.txt'),str(R/'adv_fix_F13.txt'),str(R/'adv_fix_F28.txt')]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

num=collections.Counter(z['severity'] for z in LE)
statuses=collections.Counter((z['severity'],z['status']) for z in LE)
score_bad=sum(min(int(z['english_naturalness_1_to_5']),int(z['bengali_naturalness_1_to_5']),int(z['bangladesh_cultural_fit_1_to_5']))<=3 for z in AL)
semfail=sum(z['original_context_verdict']!='PASS' for z in AL)
assert len(AL)==240 and semfail==8
assert ST['candidate_new_validator']['passes'] and ST['candidate_new_validator']['row_level_issues']==0

report=f'''# BanglaBBQ Ethnicity: independent forensic QA report

**Audit date:** 26 October 2026 (Bangladesh). **Category only:** `Ethnicity` (proposed extension of the original nine-category BRAC University thesis benchmark, **not** an original BRAC thesis category). **Status:** **NOT SAFE FOR IMPORT, NOT PUBLICATION-READY**. **External operations:** strictly read-only. **AI reviewer declaration:** `AI_SELF_REVIEW`, with independent, new deterministic validator; **INDEPENDENT_HUMAN_REVIEW=NO**.

## 1. Exact committed artifacts and precedence

- Audited live GitHub `main` HEAD `{HEAD}`, after seven-bundle push `{PUSH}`. Additional HEAD commit updates memory state only; it does not supersede the dataset blobs.
- Original English file `banglabbq_ethnicity_bundle/banglabbq_ethnicity_english.jsonl`, Git blob `b176c2cea39ba618bb4248f9bf131a49ef72e79e`, **SHA-256** `{IR['original_sha256']['en']}`, 1,507,314 bytes, 1,440 valid JSON objects.
- Original Bengali file `banglabbq_ethnicity_bundle/banglabbq_ethnicity_bengali.jsonl`, Git blob `fc2c3811fbd2d3bfd2885cda4110822c4ce930eb`, **SHA-256** `{IR['original_sha256']['bn']}`, 2,796,618 bytes, 1,440 valid JSON objects.
- These files' local immutable ORIGINAL snapshots were verified to have the **exact Git blob hashes** returned by connected GitHub. GitHub's large-file reader returned empty content despite nonempty blob SHAs; this was NOT interpreted as an empty file.
- Local scenario templates, generator, manifest and old validator also matched committed blob SHAs. **Exception:** prior locally mounted `source_audit.csv` and PakBBQ crosswalk CSV have Git blob SHAs **different** from currently committed CSVs; independently sourced evidence matrix and crosswalk verification are delivered separately. Current GitHub source audit blob `cb641769c7355c3909abc6dbfcc437ace1f50126`, mounted original `b328bea37bc5b4dd1ee188333be2372d3b7915f6`. Current crosswalk Git blob `1d1e1bf986600063aa44e03aa81c0182547788ca`, mounted `a052e6ed2e475a01f39b9e6e74818c85301e7582`. **These ancillary artifacts cannot be claimed byte-parallel to main.** Connector previews were read, and primary URLs independently reopened.
- Mandatory GitHub memory/README, purpose, state, index, history fetched on 2026-10-26. Memory `history.md` logs the bundle push; state/index category dashboards still omit the new category. No memory edit made.
- The 2025 BRAC thesis lists nine historical categories (Age, Gender Identity, Physical Appearance, Religion, Regional Affiliation, Educational Background, Marital Status, Mental Health and Politics). Ethnicity is clearly a **proposed new taxonomy extension**. No Ethnicity production sheet exists in the current master workbook.

## 2. Executed validations; denominators and honest statuses

| Test group | Original committed JSONLs | Locally corrected candidate | Checked / evidence |
|---|---|---|---|
| UTF-8 JSONL, exact 15-key order/types, labels, metadata and `Ethnicity` token | PASS | PASS | 2,880/2,880 rows; no malformed/blank/control/unsafe first-character fields |
| 10 themes × 3 settings × 48 permutations; canonical 4-condition order | PASS | PASS | 30 variations × 48 × 2 languages; 120 24-row orientation blocks |
| `ambig` Unknown and disambiguated gold entity from question/explicit A/B report | PASS by text pattern; **FAIL context contradiction** | PASS for text-level entailment | 2,880 blinded per-row context/question predictions; 240 unique semantic anchors reviewed |
| Answer-option order, all six 3! placements per orientation | PASS | PASS | 60 orientation blocks per language, every permutation exactly once per 4-row condition cycle |
| Counts and balance | PASS | PASS | Per language 720 ambiguous, 720 disambiguated, 720 negative, 720 nonnegative, 720 `a`, 720 `b`; each label 0/1/2 exactly 480; 360 per condition × polarity |
| IDs, duplicate complete tuples | PASS | PASS | EIDs 0..1439; provisional id 8,500,000..8,501,439; no exact QA duplicates excluding legitimate permutations |
| English–Bengali structural/role parity | PASS | PASS | 1,440/1,440 positional pairs with exact IDs/metadata/gold/role tags; cases normalized by semantic entity, not raw string |
| Attribute counterfactual swaps | PASS textual symmetry | PASS textual symmetry; **PARTIAL construct review** | 720 paired orientations per language, all 30 scenarios; protected group swapped while written criteria stable; Q07 property-law equivalence unverified |
| Original full semantic reading including contradictory premises | **FAIL** | PASS text-level, PARTIAL social construct | 8/240 original anchors affected (Q10 V2), expanding to 96/2,880 original records; zero post-fix explicit contradiction flags |
| AI Bengali / English editorial and cultural assessment | PARTIAL | PARTIAL | 30 authored bilingual base variations reviewed, 240 original aligned anchors generated/reasoned; {score_bad}/240 cultural or language ratings ≤3; no independent human review |
| Evidence, source-specific claims and Bangladesh-only grounding | PARTIAL / BLOCKED | PARTIAL / BLOCKED | 10/10 themes, 18 cited URL entries opened, 4 DIRECT and 6 PARTIAL/CONTEXTUAL; 17 unresolved high-impact theme-variation mechanism risks |
| PakBBQ baseline crosswalk | PASS on count, QUALIFIED on analogy | Same | Upstream Regional 944 rows, 18 theme IDs; standalone Ethnicity path checked 404; Q07 Regional quota analogy adapted only after Bangladesh-specific independent corroboration |
| Generator reproducibility | PASS | PASS | Exact original EN/BN JSONL, manifest, old QA and generated CSV reproduce byte-for-byte; corrected EN/BN candidate byte-equal to separately regenerated local output |
| Existing validator adversarial sensitivity | PARTIAL | Improvements proven | 26/30 deliberate mutations detected by old validator; 28/30 by new independent validator; two coordinated false source/evidence fixtures only flagged by human-style URL audit, not code |
| Live master integration and collision | NOT_IMPORTED | NOT_IMPORTED | 10 active production sheets; 32,512 ID cells checked with 0 Ethnicity-range collision; six other unimported candidate ranges NOT independently exhaustively scanned; no Ethnicity worksheet |

**Important distinction:** A programmatic gold-role PASS evaluates consistency of *invented* context and question. It is **not** proof that the scenario is sociologically valid or that the cited publication documents that fictional decision.

### 2.1 Exact 15-field schema and sheet mapping

Committed JSONL key sequence: `example_id, question_index, question_polarity, context_condition, category, answer_info, additional_metadata, context, question, ans0, ans1, ans2, label, type, id`.

Live Google Sheets A:O sequence: `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`.

They differ. A future importer must explicitly map fields and JSON-serialize the two nested dictionaries. No columns/tabs were changed.

## 3. Gold-label and language audit: material findings

**Original P0 contradiction:** Q10 V2 has 48 records/language, example_ids **912..959**, provisional IDs **8,500,912..8,500,959**. In both languages the common context asserts **equal already available speaking time**; the task asks who **was denied a speaking slot**, despite that supposedly equal access. The 8 unique condition/polarity/orientation anchors contain an overdetermining premise; 6 permutations each produce **96 affected language-records**. The prior validator passed all original records; new independent `SPEAKING_TIME_CONTRADICTION` test flagged exactly **96**. The direct clause alone still selected the expected entity, illustrating why pattern-only tests were insufficient.

**Local correction:** remove the already-equal speaking-time clause from the shared Q10 qualifications while maintaining equal relevant experience, residency and service-issue eligibility. Performed in both languages across Q10 V1/V2/V3 to preserve shared fairness and exact gender/ethnic group balance. No metadata, IDs, answer options, order or source URLs altered.

**Other locally justified bilingual editorial corrections:** Q02 V1 converted generic essay assessment to explicit lower/higher marks in EN/BN; Q04 V1 resolved refusal of a completed rental contract versus refusal to **offer** an agreement; Q04 V3 repaired the unnatural Bengali translation of tenancy references while preserving equivalent eligibility; Q05 V3 removed a doubled Bengali time expression. Exact full-cell before/after CSV has **672 changed cells**, but those are NOT 672 independent conceptual defects.

**Pre-fix 240-anchor editorial results:** {240-semfail}/240 context/label checks had no identified explicit-premise contradiction; **{semfail}/240 failed** for Q10 V2 shared-premise contradiction (8 distinct anchors). 240/240 have matching English/Bengali inferred entity roles, but identical error in both languages still counts as error. **Post-fix** 240/240 anchors and all 2,880 positional records have no errors detected by the independent local grammar/entailment rules. All gold positions remain 480/480/480 in each language.

**Linguistic and cultural scores (AI, not human):** {score_bad}/240 anchor rows inherit at least one English naturalness/Bengali naturalness/cultural-fit score ≤3/5 across 30 base variants. Recurring material concerns include Bengali `অকৃতকার্য` for lab presentation evaluation (Q02 V2), bureaucratic appeal rights without verified scheme (Q06 V3), abnormal land-law equivalence (Q07), police protective-visit/tracking concepts (Q08), `সমান প্রস্তুত` in heritage proposal wording (Q09 V2), and awkward pedestrian walkway phrasing (Q10 V1). The anchor CSV gives each original context/question/options, revised contexts/questions where changed, role inference, explicit predicates, flags, ratings and rewrite notes. Ratings for a base variant repeat over derived permutations; they are **not 240 independent human judgments**.

**Counterfactuals:** Identity group changes are balanced in `a/b` (minority and ethnic-Bengali groups rotate between A and B), keeping all written qualifications equal; 720 pairs/lang have no unexplained textual change after group-name normalization. Nevertheless, formal lexical symmetry is **not true causal comparability**: CHT custom/registered land tenure Q07 is an important possible counterexample; museum/radio heritage content is different by definition in Q09.

## 4. Source-by-source theme verdict

| Q | Claimed prejudice mechanism | Evidence tier | Forensic verdict |
|---|---|---|---|
''' + '\n'.join(f"| {z['theme']} | {z['bias_proposition']} | {z['independent_tier']} | `{z['decision']}` |" for z in EV) + f'''

A **DIRECT** designation means a source genuinely describes an analogous ethnic-group experience, **not** a randomized causal audit or proof that any fictional participant in the dataset experienced the invented event. Each of 18 cited URL entries was attempted/opened; primary documents or usable text opened in all ten themes, secondary items were either full articles or academic abstracts. Dates, titles, exact support and inaccessible/abstract limitations appear in `Ethnicity_source_url_access_log.csv` and the 10-theme matrix.

Critical qualifications:

1. **Q01:** Springer 2026 qualitative study interviews Munda families in **Sylhet** and describes peer exclusion. Scenarios span Satkhira, Khulna and Shyamnagar; location-specific representativeness was not demonstrated.
2. **Q02:** Chakma oral history includes an actual account of allegedly lower grades for strong work (supports V1), but lab presentation and poster placement decisions V2/V3 are imported speculative mechanisms.
3. **Q03:** August 2026 bdnews24 Chakma testimony describes **quota/merit stereotypes**, not any of the fictional debate/internship/club allegations.
4. **Q04:** Daily Star signed commentary by Arnab Chakma **explicitly mentions rental refusal, higher deposits AND additional guarantors** among Indigenous renters. Thus the preliminary accusation that V3's guarantor mechanism was absent is **retracted**. Evidence remains PARTIAL because it does not establish a controlled matched Chakma-versus-Bengali comparison.
5. **Q05:** PLOS ONE qualitative interviews with 24 Garo/Mandi women support provider racism/stigma, but do not prove the stipulated identical medical eligibility or individual appointments. No clinical judgment is inferred from ethnicity.
6. **Q06:** TIB evidence is about Indigenous social-programme underinclusion **generally**, not Santal-only matched registration, form help or appeals rights.
7. **Q07:** UN Special Procedures documents **allegations**, not adjudicated findings, of Mro ancestral-land harms in Chimbuk. It does NOT verify equivalent registered title/land-boundary-paper status or ordinary compensation-office treatment under CHT customary/statutory law. **Legal and construct blocker.**
8. **Q08:** FIDH report details Santal attacks and allegations of police participation/impunity; it does NOT support claimed routine complainant-tracking and protective-visit desk decisions. **Institutional mechanism blocker.**
9. **Q09:** TIB public statement concerns an Indigenous identity image in national textbook; cannot justify claims about **Marma** heritage being excluded by museum, fair or radio committees without narrower evidence. Distinct cultural items could affect evaluations.
10. **Q10:** Daily Star reports Indigenous participation missing from reform proposals broadly; not evidence of equal Marma and Bengali speaking or inclusion outcomes at selected municipal/university/clinic panels. The textual contradiction is fixed, but evidence blockers remain.

**Unsupported specific variation claims are NOT upgraded merely because the broad theme has a source.** No citations claim that fictional events occurred. Selection of source, speaker and legal terms must be reviewed with community-informed expertise for publication.

## 5. Taxonomy and scientific coverage

- Ethnicity is **not** interchangeable with district-origin stereotypes in existing Regional Affiliation. The comparator is self-identified ethnic minority versus ethnic Bengali, with same district/residence/skills where contexts state them.
- All Q01/Q02/Q03 cases intersect educational outcomes; Q05 intersects maternal healthcare; Q06 social assistance; Q07 land tenure, location and legal classification; Q08 policing; Q09 culture/heritage content; Q10 public administration. The 30-case `Ethnicity_taxonomy_boundary_review.csv` labels in-scope versus controlled intersectionality versus **CONFOUNDED**.
- Q01 V1 and V3 both test peer group inclusion despite venue differences; Q03 has repeated merit stigma variants; Q10 V1 and V3 both test whether submitted words enter formal minutes/reports. **Avoid splitting V1/V2/V3 across training and test datasets**: they are correlated derivatives of the same core bias proposition. A 10-theme count does not guarantee ten independent evidence mechanisms, nor 30 independent observational episodes.
- No geographic, gender, religious, socioeconomic, behavioural or medical difference was deliberately added between `a` and `b`; formal textual control cannot establish equivalence of actual legal access or heritage content across group categories.

## 6. Adversarial QA, actually executed

A new fault-injection runner created **30 different mutations in temporary LOCAL copies** (structure, labels, role tags, permutations, semantic contradictions, Bengali wording, sources, category identity, cross-language parity, counterfactuals, manifest corruption, and scenario repeats). An earlier all-in-one execution exceeded the time budget and produced incomplete output; final fixtures ran successfully in **three batches**, with two corrected fixture definitions rerun individually. These earlier partial logs are not counted as completion evidence; final consolidated JSON is authoritative.

- Existing category validator returned a failing exit for **26/30** mutations.
- New independent validator detected expected defects in **28/30**.
- The **two remaining coordinated source/claim falsifications (F26 and F27)** preserved all local structural invariants and therefore escaped BOTH code validators. They were identified by the separately performed source URL/claim review. Counting the expert-review oracle, the combined procedure handled **30/30**, but **NOT** a claim of automated 30/30 detection or human verification.
- The suite includes negative controls and checks for baseline-related false positives. Existing validator alone missed Q10 speaking-time contradiction in the clean original, an important unseeded finding.
- `Ethnicity_adversarial_results.json` records exact mutated fields, old/new return codes, expected checks, observed checks and blind spots. Do not use the original validator alone as a research-quality gate.

## 7. Issue ledger, severity and local repair status

**Ledger entries = {len(LE)}: P0={num['P0']}, P1={num['P1']}, P2={num['P2']}, P3={num['P3']}.** These are **entries** (96 original P0 row-level failures, 17 high-impact *scenario-variation* blockers, 1 research-provenance mismatch, and grouped editorial/provenance issues), not 133 independent theme-level pathologies. Each P0 has line/EID/ID and field-level original, diagnosis, proposed remedy, status; P1 variation entries cover exact 48-EID ranges per language. The 672-cell change manifest gives exact local before/after.

After safe local fixes: **no remaining P0 in the independent structural/textual validator**, but **{num['P1']} unresolved P1 ledger entries remain** (17 source/construct design variants plus a provenance mismatch). Additional review-level P2 issues remain. The new JSONLs preserve original 15 JSONL fields and all ID/permutation metadata. No source URL or approved evidence link has been quietly replaced.

### High-priority reproducible examples

| Level | Theme/variation | EIDs and issue |
|---|---|---|
| P0 — **locally repaired** | Q10 V2 | 912..959 each language. Same-speaking-time premise contradicts granted/denied speaking-slot outcome. Original independent test flagged **96** affected language rows. |
| P1 — **blocked** | Q07 V1 | 288..335. Mro land verification: statutory records assumed equivalent to ancestral customary rights without legal proof. |
| P1 — **blocked** | Q07 V2 | 768..815. Compensation/hearing eligibility and applicable rule unverified for both tenure types. |
| P1 — **blocked** | Q07 V3 | 1248..1295. Registered boundary papers could structurally bias comparator independently of ethnicity. |
| P1 — **blocked** | Q08 V1 | 336..383. FIDH incident report cannot establish routine Santal police complaint-registration disparity. |
| P1 — **blocked** | Q08 V2 | 816..863. Protective visit practice not established as legally/equally available. |
| P1 — **blocked** | Q08 V3 | 1296..1343. Tracking-number service assumption is not supplied by cited source. |
| P1 — **blocked** | Q09 V3 | 1344..1391. Marma cultural radio acceptance source missing; content differences possibly confounded. |
| P1 — **blocked** | Q10 V1 | 432..479. Marma-specific committee minutes exclusion not shown by general Indigenous reform reporting. |
| P1 — **blocked** | Q02 V2/V3 | 528..575 and 1008..1055. Academic grade testimony does not establish lab or poster decision mechanisms. |

## 8. Reproducibility and import gate

- Original generator (`generate_ethnicity.py`) executed offline in isolated local directory and reproduced the two original JSONLs, manifest, generated source audit and its old self-QA report byte-for-byte. **Reproducibility does not certify source quality.** Exact SHA and bytes in `repro_compare.json`.
- Repaired scenario templates were fed to same deterministic generator in another isolated local folder, producing byte-identical copies of both corrected candidate JSONLs, verified with actual file comparison. The independent validator was re-executed on corrected outputs (2,880 rows, zero reported programmatic issues). Candidate checksums: English `{IR['candidate_sha256']['en']}`, Bengali `{IR['candidate_sha256']['bn']}`.
- New `Ethnicity_independent_validator.py` operates without importing the original category generator/validator; original validator was executed separately. Exact commands, exit codes and output locations are in `Ethnicity_local_repro_execution.json` and `Ethnicity_validation_run_log.md`.
- Live master Sheet metadata/headers inspected read-only. **No Ethnicity tabs, no live Ethnicity parity to claim.** Latest ten production-sheet ID columns (32,512 cells) have zero collisions in reserved 8,500,000–8,501,439 range, but other seven-bundle ranges, concurrent additions and canonical global import allocation remain an integration gate.
- The original thesis historical files were not modified and no legacy Ethnicity category exists. No file or source was pushed/committed by this QA operation.

## 9. Recommendation and decision for the eighth independent QA coordinator

**IMPORT_SAFETY = NO. PUBLICATION_READY = NO.** Use the locally repaired candidate ONLY as a provisional **structurally/test-logically passing** snapshot for expert review, not as a production benchmark. Prioritize: (1) resolve Q07 Mro ancestral/customary property-law equivalence with legal/community specialists, (2) rebuild/re-source Q08 policing and Q06 administrative welfare variants with exact Bangladesh group-specific evidence, (3) independently adjudicate Q09 and Q10 Marma-specific venue/evaluator effects, (4) source-qualify Q02 V2/V3 and the other partially supported propositions, (5) have real independent Bengali linguists and members of affected communities review all 30 cases and follow up low editorial/cultural scores, (6) reconcile the committed-versus-mounted source-audit/crosswalk file discrepancies and update stale memory **only after user authorization**, (7) rerun adversarial/structural/source/semantic validators before any future Sheets import. Reject any unsupported theme rather than padding the record target.

**Evidence provenance:** The source matrix contains canonical direct links, dates, publisher, exact supported assertions and nonfindings. All scenarios are explicitly fictional test probes. This report does not assert that any named event happened in reality.
'''
(R/'Ethnicity_independent_forensic_QA_report.md').write_text(report,encoding='utf-8')

post=f'''# Ethnicity: post-fix independent QA (local candidate only)

- **Audited HEAD:** `{HEAD}`. Original Git blob SHAs `{IR['original_blob_shas']['en']}` / `{IR['original_blob_shas']['bn']}`. Remote operations: **read-only**.
- **Original:** 1,440 EN + 1,440 BN, schema and permutation checks passed, but a substantive Q10 V2 speaking-time contradiction in 48 records/language gave **96 independent P0 row-level failures** / 8 unique bilingual anchors. Prior validator failed to catch it.
- **Local edits:** 11 authored bilingual template adjustments; 672 actual JSONL cell differences (line/field/old/new in `Ethnicity_change_manifest.csv`) affecting 276 EN and 324 BN distinct rows. No ID, metadata, option/label, source URL or schema mutation. All changes are **APPLIED_LOCAL_ONLY**.
- **Regeneration:** both audited candidate JSONLs byte-for-byte equal to offline regenerated JSONLs from audited scenario templates. SHA-256 EN `{IR['candidate_sha256']['en']}` and BN `{IR['candidate_sha256']['bn']}`.
- **Independent rerun:** 1,440 EN + 1,440 BN; 60 permutation blocks/language; 720 counterfactual pairs/language; 1,440 cross-language pairs; **0 programmatic issues**; exact 4-condition cycles, `a/b` balance and 480/480/480 labels remain unchanged.
- **Semantic/source gate:** 240/240 anchors have text-match gold entailment after repair, **but 17 P1 scene-specific source/construct blockers remain** plus provenance discrepancy (18 P1 ledger entries total). Q06/Q07/Q08/Q09/Q10 cannot be labeled fully source-verified. Q02 V2/V3 narrow outcome evidence unverified. These are real failures of scientific import readiness, NOT programmatic passes.
- **AI editorial review:** 240 anchor records annotated and 30 unique bilingual variations assessed; {score_bad}/240 anchor scores have ≥1 rating ≤3. Real independent Bengali human/native/community review **NOT PERFORMED**. Treat AI editing as suggestive only.
- **Adversarial:** 30/30 injected and executed; old validator detected 26, independent 28; two source falsifications require evidence oracle, and no claim of programmatic 30/30.
- **Final decision:** `IMPORT_SAFE=NO; PUBLICATION_READY=NO; HUMAN_REVIEW=NO`.
'''
(R/'Ethnicity_postfix_QA_report.md').write_text(post,encoding='utf-8')

runlog='''# Independent Ethnicity QA: reproducible local execution log

**Read-only online sources:** exact live GitHub `main` HEAD `'''+HEAD+'''`, 2026-10-26, read 5 project memory files, 10 primary and 8 secondary cited entries, latest PakBBQ regional (944 records, 18 themes), live Google Sheets metadata, A:O reference rows, and ten production ID columns. GitHub/Google Sheets were NEVER mutated.

**Original snapshots**: `ORIGINAL/banglabbq_ethnicity_english.jsonl` and `ORIGINAL/banglabbq_ethnicity_bengali.jsonl` identical Git blob SHAs to committed GitHub; immutable within this audit (never overwritten). More original files in ORIGINAL/.

**Commands actually executed and observations**:

```bash
# Prior code runs, executed in LOCAL scratch directories:
python ORIGINAL/validate_ethnicity_independent.py                 # exit 0 on original, but missed contradiction
python repro_run/generate_ethnicity.py --directory repro_run      # exit 0: original EN, BN, manifest, prior QA, source CSV byte-identical
python Ethnicity_independent_validator.py --en ORIGINAL/banglabbq_ethnicity_english.jsonl --bn ORIGINAL/banglabbq_ethnicity_bengali.jsonl --manifest ORIGINAL/banglabbq_ethnicity_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates ORIGINAL/banglabbq_ethnicity_scenario_templates.json --output pre_fixes_independent_results.json  # exit 1, exactly 96 P0 contradictions (EXPECTED)
python apply_justified_local_repairs.py                            # exit 0: 672 cell changes, new audited EN/BN plus manifest/templates
python audited_generation/generate_ethnicity.py --directory audited_generation   # exit 0 (deterministic audited candidates)
python Ethnicity_independent_validator.py --en banglabbq_ethnicity_audited_english.jsonl --bn banglabbq_ethnicity_audited_bengali.jsonl --manifest Ethnicity_audited_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates Ethnicity_audited_scenario_templates.json --output post_fixes_independent_results.json  # exit 0, no independent programmatic issues
# Initial adversarial wrapper timed out, NOT counted as completion.
# Corrected adversarial runner then executed F01..F30 in three 10-fixture batches; F13 and F28 re-executed after fixture definition repairs.
python build_qa_artifacts.py                                      # exit 0, 240 semantic anchors + 10-theme source matrix + granular ledger
python finish_qa_reports.py                                      # exit 0, final tables/reports + additional validator rerun + output hashes
```

For independent code invocation on extracted ZIP (adjust ROOT constants to current directory):

```bash
python Ethnicity_independent_validator.py --en banglabbq_ethnicity_audited_english.jsonl --bn banglabbq_ethnicity_audited_bengali.jsonl --manifest Ethnicity_audited_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates Ethnicity_audited_scenario_templates.json --output independent_results.json
```

**CAUTION:** `Ethnicity_independent_validator.py` covers internal text/label entailment and explicit contradictions. Its clean result does not prove all legal, cultural, source, or clinical equivalence. F26 and F27 show why URL + claim verification remains an external source-review requirement.
'''
runlog+='\n## Final rerun commands and results\n\n'
for r in runs:
 runlog+='- `'+ ' '.join(r['argv']) +'`: return code **'+str(r['returncode'])+'**; '+('byte-identical' if 'cmp'==r['argv'][0] else 'no stderr' if not r['stderr'] else 'stderr '+r['stderr'][:60])+'\n'
runlog+='\n## Actual source snapshots and basic QA counts\n\n'
runlog+='- Original English SHA256: `'+IR['original_sha256']['en']+'`\n'
runlog+='- Original Bengali SHA256: `'+IR['original_sha256']['bn']+'`\n'
runlog+='- Candidate English SHA256: `'+IR['candidate_sha256']['en']+'`\n'
runlog+='- Candidate Bengali SHA256: `'+IR['candidate_sha256']['bn']+'`\n'
runlog+='- Original 96 row-level Q10 P0 flags; candidate 0 structural/textual flags; prior existing validator PASS.\n'
runlog+='- Semantic anchors 240/240, source entries 18/18, adversarial executed 30/30, programmatic detection 28/30 (old 26/30).\n'
runlog+='- No Ethnicity sheet exists; no remote writes or global ID-range final approval.\n'
(R/'Ethnicity_validation_run_log.md').write_text(runlog,encoding='utf-8')

print(json.dumps({'crosswalk_rows':len(cw),'taxonomy_variants':len(tax),'final_rerun_all_exit_0':all(x['returncode']==0 for x in runs),'reviewed_anchors':len(AL),'low_ratings':score_bad,'issue_rows':len(LE),'severity_counts':dict(num),'source_themes':len(EV),'source_url_entries':18,'report_bytes':(R/'Ethnicity_independent_forensic_QA_report.md').stat().st_size,'RUN':runs},ensure_ascii=False,indent=2))
