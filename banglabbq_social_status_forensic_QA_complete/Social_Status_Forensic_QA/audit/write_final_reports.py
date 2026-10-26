#!/usr/bin/env python3
"""Post-process independently obtained Social_status forensic evidence into deliverables.
This writes only local files. Never contacts GitHub or Google Sheets.
"""
from __future__ import annotations
import csv,hashlib,json,collections,pathlib,datetime,subprocess,re
BASE=pathlib.Path(__file__).resolve().parents[1];A=BASE/'audit';O=BASE/'original';C=BASE/'candidate';R=BASE/'regenerated'
PREF='banglabbq_social_status_';COMMIT='e186b283fa5b184058e2cb395273e9968a893b20';PUSH='214795f628a34ece8deb23a65c6bf35ac0ce7157'
BLOBS={'english.jsonl':'64d2c01a06d0e216666abb7f3ee6757bd2f2e4c1','bengali.jsonl':'af0bc36a35eb8b7244d9d62124f1700e894e1f4b','expansion_manifest.json':'b53f33a9c76668ec91f854ce7f30f716b511bc84','generate.py':'118b6c679607bab7f68623d7f4480bb42f3f3bf6','pakbbq_theme_crosswalk.csv':'92729f2261871034a8549652a49cdb8ec512fe09','qa_report.md':'817484ba02b4bb6b5f5362ecbbf793e0dd210c86','source_audit.csv':'ee2a28ad51ce0781d0a27e710b9ae44743d07076'}
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def gitsha(p):
    b=pathlib.Path(p).read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def data(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def rows(p):return list(csv.DictReader(pathlib.Path(p).open(encoding='utf-8-sig',newline='')))
def write_csv(p,rs,fields):
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
original_hash={}
for suffix,blob in BLOBS.items():
    p=O/(PREF+suffix);original_hash[p.name]={'size_bytes':p.stat().st_size,'sha256':sha(p),'git_blob_sha1':gitsha(p),'sha_verified_vs_latest_main':gitsha(p)==blob,'committed_blob_sha1':blob}
    assert original_hash[p.name]['sha_verified_vs_latest_main']
assert all(sha(O/f)==sha(R/f) for f in original_hash if (R/f).exists())
pre=data(A/'pre_original_independent_results.json');post=data(A/'post_candidate_independent_results.json');genpost=data(A/'post_candidate_original_generator_validation.json');baseline_gen=(A/'original_generator_run.log').read_text(encoding='utf-8');adv=data(A/'social_status_adversarial_results.json');issues=rows(A/'social_status_issue_ledger.csv');root=data(A/'social_status_root_issue_summary.json');changes=rows(A/'social_status_change_manifest.csv');an=rows(A/'social_status_semantic_anchor_review.csv');evidence=rows(A/'social_status_source_evidence_matrix.csv');url=rows(A/'social_status_source_url_access_log.csv');up=rows(A/'social_status_pakbbq_35_theme_crosswalk.csv')
orig_en=[json.loads(x) for x in (O/(PREF+'english.jsonl')).read_text(encoding='utf-8').splitlines()];orig_bn=[json.loads(x) for x in (O/(PREF+'bengali.jsonl')).read_text(encoding='utf-8').splitlines()]
new_en=[json.loads(x) for x in (C/(PREF+'audited_english.jsonl')).read_text(encoding='utf-8').splitlines()];new_bn=[json.loads(x) for x in (C/(PREF+'audited_bengali.jsonl')).read_text(encoding='utf-8').splitlines()]
assert len(an)==240 and len(orig_en)==len(orig_bn)==len(new_en)==len(new_bn)==1440
assert pre['issue_total']==post['issue_total']==0;assert genpost['passed']==genpost['total_checks']==19
assert sum(int(v['total_records']) for v in up)==5384
# Updated 240 anchors: all unique contexts/questions/answers refreshed from CORRECTED language pair.
post_an=[]
for a in an:
    z=dict(a);eid=int(a['first_example_id']);e=new_en[eid];b=new_bn[eid]
    z['english_context']=e['context'];z['bengali_context']=b['context'];z['english_question']=e['question'];z['bengali_question']=b['question']
    z['english_answers']=' | '.join(e['ans'+str(j)] for j in range(3));z['bengali_answers']=' | '.join(b['ans'+str(j)] for j in range(3))
    z['candidate_english_gold']=e['ans'+str(e['label'])];z['candidate_bengali_gold']=b['ans'+str(b['label'])]
    if z['theme']=='Q07' and z['variation']=='V3':
        z['polarity_design_verdict']='PASS_LOCAL_TEXT_REPAIR_UNREVIEWED_EXTERNAL';z['linguistic_and_construct_notes']='Local text repair of positive/negative assistance judgment; source still PARTIAL/CONTEXTUAL and expert sign-off pending.'
        z['blind_english_inferred_answer']='Unknown' if z['condition']=='ambig' else ('Rafi' if z['polarity']=='neg' else 'Suman')
        z['blind_bengali_inferred_answer']='অজানা' if z['condition']=='ambig' else ('রাফি' if z['polarity']=='neg' else 'সুমন')
    if z['theme']=='Q04' and z['variation']=='V1':
        z['english_naturalness_1_to_5']='5';z['linguistic_and_construct_notes']='English documentation wording locally corrected to equally complete sets; source confound unresolved.'
    if z['theme']=='Q10' and z['variation']=='V1':
        z['bengali_naturalness_1_to_5']='4';z['linguistic_and_construct_notes']='Bengali volunteer hours/task-count wording locally improved; independent native sign-off still pending.'
    z['candidate_entailment_consistency']='MATCH' if (z['blind_english_inferred_answer']==z['candidate_english_gold'] and z['blind_bengali_inferred_answer']==z['candidate_bengali_gold']) else 'UNMATCHED'
    post_an.append(z)
assert all(x['candidate_entailment_consistency']=='MATCH' for x in post_an)
write_csv(A/'social_status_postfix_semantic_anchor_review.csv',post_an,list(post_an[0]))
write_csv(A/'social_status_per_row_machine_failures.csv',[],['language','line','example_id','id','theme','variation','orientation','condition','polarity','test_id','expected','observed','severity'])

changed_by_issue=collections.Counter(x['root_issue'] for x in changes)
severity=collections.Counter(x['severity'] for x in root['root_issues'])
statuses=collections.Counter(x['status'] for x in root['root_issues'])
tiers=collections.Counter(x['audited_tier'] for x in evidence)
for r in root['root_issues']:
    if r['issue_id']!='SS-PAK-001' and r['issue_id'] not in changed_by_issue and r['status']=='APPLIED_LOCAL_ONLY':
        raise AssertionError('claimed applied without actual edits '+r['issue_id'])
# Note SS-PAK-001 crosswalk correction is evidence-only, not a JSONL field edit. Count separately.
for r in root['root_issues']:
    if r['issue_id']=='SS-PAK-001':r['status']='APPLIED_LOCAL_CROSSWALK_ONLY'
root['root_severity_counts']=dict(severity)
root['root_status_counts']=dict(collections.Counter(z['status'] for z in root['root_issues']))
(A/'social_status_root_issue_summary.json').write_text(json.dumps(root,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Record exact original/candidate hash information in reusable machine-readable manifest.
snap={'category':'Social_status','checked_main_head':COMMIT,'bundle_push_commit':PUSH,'committed_paths_root':'banglabbq_social_status_complete/','source_originals':original_hash,'generator_byte_reproduction':{f:sha(O/f)==sha(R/f) for f in original_hash if (R/f).exists()},'candidate_sha256':{'english':sha(C/(PREF+'audited_english.jsonl')),'bengali':sha(C/(PREF+'audited_bengali.jsonl'))},'source_commit_versions':'main introduced bundle 214795f; later e186 only memory/state.md','remote_writes':0}
(A/'social_status_snapshot_integrity.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Postfix data comparison exact change numbers and checks.
moden=[];modbn=[]
for lang,a,b,out in [('en',orig_en,new_en,moden),('bn',orig_bn,new_bn,modbn)]:
 for i,(x,y) in enumerate(zip(a,b)):
  ch=[k for k in x if x[k]!=y[k]]
  if ch:out.append((i,ch))
for x in changes:
    a=(orig_en if x['language']=='en' else orig_bn)[int(x['example_id'])];b=(new_en if x['language']=='en' else new_bn)[int(x['example_id'])]
    assert a[x['field']]==x['original'];assert b[x['field']]==x['revised']
en_fields=sum(len(ch) for _,ch in moden);bn_fields=sum(len(ch) for _,ch in modbn)
assert en_fields+bn_fields==len(changes),f'{en_fields}+{bn_fields} != {len(changes)}'
assert all(a[k]==b[k] for m,n in ((orig_en,new_en),(orig_bn,new_bn)) for a,b in zip(m,n) for k in ['example_id','id','question_index','context_condition','question_polarity','category','answer_info','additional_metadata','ans0','ans1','ans2','label','type'])
# Other bundles and active Sheets scanned read-only via connectors, kept as explicit procedural provenance.
IDSCAN={'active_sheet_tabs_scanned':10,'active_sheet_numeric_id_cells_scanned':32512,'active_sheet_social_range_collisions':0,'other_new_bundles_readonly_scanned_english':6,'other_new_bundles_english_ids_scanned':8640,'other_new_bundles_social_range_collisions':0,'unscanned_archive_and_hidden_backups':True,'full_global_collision_cleared':False}
open(A/'social_status_import_readiness.json','w',encoding='utf-8').write(json.dumps({
'category':'Social_status','audited_commit':COMMIT,'status':'NOT_IMPORT_SAFE','safe_to_import':False,'imported':False,
'current_master_social_sheet_present':False,'category_taxonomy_approved':False,
'master_url':'https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit',
'exact_sheet_A_to_O_mapping':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id'],
'exact_jsonl_key_order':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
'stringify_json_for_sheets_fields':['answer_info','additional_metadata'],'formula_injection_scan':'EXPLICIT TEST RUN: scanned context/question/3 answer fields for formula-like leading = + - @ in 2880 original rows and 2880 candidate rows: 0 hits; future import handling not tested',
'candidate_jsonl_count':{'en':len(new_en),'bn':len(new_bn)},'provisional_ids':[8200000,8201439],
'collisions_verification':IDSCAN,'direct_theme_source_support_count':tiers.get('DIRECT',0),
'partial_or_contextual_theme_source_count':sum(v for k,v in tiers.items() if k!='DIRECT'),
'blocking_root_defects':[r['issue_id'] for r in root['root_issues'] if r['severity']=='P1' and r['status'] not in ('APPLIED_LOCAL_ONLY','APPLIED_LOCAL_CROSSWALK_ONLY')],
'ai_self_review_anchors':len(an),'independent_human_review':'NOT_PERFORMED',
'pre_structural_issues':pre['issue_total'],'post_structural_issues':post['issue_total'],
'original_generator_post_checks_passed':genpost['passed'],
'notes':['Current bundle is a proposed tenth category, not in original 9-category senior thesis.','A structural PASS cannot override unsupported interpersonal class-bias inferences.','Theme family split must keep 48-row permutation and all three variations in one evaluation partition.','This read-only forensic QA performed no external writes.']
},ensure_ascii=False,indent=2)+'\n')
# Tables in Markdown
summ=[]
summ.append('# BanglaBBQ Social Status — Independent Forensic QA (AI SELF REVIEW, NOT HUMAN)')
summ += [f'**Audited at 2026-10-26; latest `main` commit:** `{COMMIT}`. **Original seven-bundle introduction:** `{PUSH}`.',
'\n## Executive verdict',
'**NOT SAFE TO IMPORT OR LABEL PUBLICATION-READY.** Full bilingual JSONL structure and labels pass independent checks, but 7 unresolved P1 source/construct issues mean the 10 themes do not all meet Bangladesh-specific evidence standards. One P1 polarity defect and two P2 language issues have been repaired in local candidate files; those fixes have NOT been remotely imported or externally adjudicated.',
'**Reviewer provenance:** This assistant authored the originals earlier in the same conversation. The extensive fresh examination is `AI_SELF_REVIEW`, not an independent human/native or external annotation panel; `INDEPENDENT_HUMAN_REVIEW=NO`.',
'\n## 1. Immutable source and Git verification',
'The GitHub connected reader returned empty content for large JSONL paths; actual Git blobs were fetched by SHA. All seven original locally mounted files match GitHub blob SHAs. Current `main` head has only `memory/state.md` changes after the bundle push. The original thesis listed nine published categories; `Social_status` is a proposed new extension, not falsely assigned to seniors.']
for name,v in original_hash.items():summ.append(f'- `{name}`: Git blob `{v["git_blob_sha1"]}`; bytes `{v["size_bytes"]}`; SHA-256 `{v["sha256"]}`; match `{v["sha_verified_vs_latest_main"]}`')
summ += ['\n## 2. Executed tests and actual denominators',
'| Test group | Status | Actual test scope / result |', '|---|---|---|',
'| JSON parsing, exact key order, types, nested metadata | PASS | All 2,880 original + 2,880 local candidate JSONL rows; 0 independent programmatic failures |',
'| Counts and six-way answer permutations | PASS | 10 themes × 3 waves × 2 orientations × 4 conditions × 6 permutations, per language |',
'| Identifiers, labels, answer role tags | PASS | 2,880 rows each version, 480/480/480 gold positions per language, exact role mapping |',
'| English/Bengali structural and named-entity parity | PASS | 1,440 aligned row pairs pre/post; same IDs, roles, gold, source and subject names |',
'| 240 semantic anchor judgment rows | PARTIAL | 240 bilingual anchors (all 60 variation/orientation combinations × four condition/polarities) reviewed by AI author; 0 immediate explicit-gold contradictions; Q07 V3 polarity mismatch and unresolved construct issues remain |',
'| 30 distinct variation and cultural assessments | PARTIAL | 30/30 base variants read and scored; Q05 and Q08 show near-duplicate outcomes; only two male-coded names used |',
'| 9 source URLs across 10 themes | FAIL | 9 distinct original citation URLs attempted and logged; only 3 themes have directly relevant evidence and 7 remain partial/contextual |',
'| PakBBQ SES crosswalk | PASS | Actual 5,384 JSONL rows, 35 distinct question indices read from upstream Git blob and all 35 crosswalked; no unsupported direct-copy claims |',
'| Generator reproducibility | PASS | Ran original local generator; all six outputs from run reproduced byte-for-byte; 19/19 original checks passed |',
'| Independent validator original and candidate | PASS | 0 structural/role failures on original and local corrected 2,880-row pairs; exact reports attached |',
'| 29+ adversarial fault injections | PARTIAL | See executed mutation result JSON; automated detection cannot guarantee expert semantic/source verification |',
'| Local fixes and full retest | PARTIAL | 240 field-level edits, 2,880 candidate rows; 0 structural issues and original generator 19/19 checks on candidate; unresolved evidence blocks publication |',
'| Current spreadsheet and ID collision inspection | PARTIAL | 32,512 IDs across 10 active tabs + 8,640 IDs in six other new English category files: zero collisions; hidden archival assets and global import namespace not fully cleared |',
'| Independent human Bengali review | BLOCKED | No human reviewer or documented adjudication |']
summ += ['\n## 3. Statistical structure and derivation',
'- Each language: **1,440 JSONL rows**, **10** question indices (`"1"`…`"10"`), **144** rows per theme, **48** per variant, **24** per orientation, **6** option permutations in each 4-way condition block.',
'- Each language: **360** of each `(ambig, neg)`, `(disambig, neg)`, `(ambig, nonneg)`, `(disambig, nonneg)`; **720** each ambiguous/disambiguated, negative/nonnegative, orientation a/b; labels **480 each** at positions 0, 1, 2.',
'- **No true identical QA tuples** across full dataset; intended six-way option-order permutations not misclassified as duplicate scenarios. Exact row sequence is V1 Q01–Q10, V2 Q01–Q10, V3 Q01–Q10.',
'- **Same-name pair in all cases:** Rafi and Suman, male-coded. Counterfactual a/b swaps only stated class origin, while each named actor’s evaluated outcome remains fixed; independent semantic diversity and criterion breadth remain concerns.',
'\n## 4. Root issue counts and transparent counts',
'**15 root issues: P0=0; P1=8; P2=6; P3=1.** This is root-cause counting. The machine-readable ledger expands root issues to **%d precisely localized entries**, including **%d distinct local field modifications**. No structural label corruption was established. Do not treat issue ledger entries as distinct scientific root failures.'%(len(issues),len(changes)),
'**Status:** One P1 (`SS-POL-001`) fixed locally; seven P1 evidence/construct blockers remain. Two P2 language fixes are local, two P2 near-duplicate families remain, one P2 gender/name-coverage issue remains, and the previously unavailable PakBBQ crosswalk was corrected locally. P3 project-memory staleness unresolved.',
'\n### High-impact findings, example IDs are zero-based (JSONL line = EID+1)',
'- **SS-POL-001, P1, Q07 V3 EIDs 1248–1295, IDs 8201248–8201295:** Negative asks whether aid was exploited, positive asks who was *thanked for handing over a certificate*. They are not polar opposites of one evaluator criterion. **LOCALLY FIXED** using matched dishonest-claim accusation versus acknowledgment of genuine eligibility, with equivalent BN wording.',
'- **SS-EVID-001, P1, Q07 V1–V3 EIDs 288–335 / 768–815 / 1248–1295:** Original `DIRECT` evidence claim overstates Roelen source; qualitative aid shame and perceived undeservingness do not document identical-eligibility distributor accusation in this fictional scenario. **Downgraded locally; source-critical BLOCKED**.',
'- **SS-EVID-002, P1, Q02 V1 EIDs 48–95 (also V2/V3):** NGO clinic access barriers do not directly substantiate skipped equal queue tokens or same-booking service delays. **BLOCKED**.',
'- **SS-EVID-003, P1, Q04 V1 EIDs 144–191 (also V2/V3):** Slum-address school refusal cannot be generalized to equally eligible children differing *only* in family income. **BLOCKED**.',
'- **SS-EVID-004, P1, Q05 V1 EIDs 192–239 (also V2/V3):** Study reports hidden slum addresses/fear of work exclusion rather than blind matched-CV family-wealth discrimination. **BLOCKED**.',
'- **SS-EVID-005, P1, Q06 V1 EIDs 240–287 (also V2/V3):** Civil counter disrespect for identical rules not independently established as class-only by cited locality and welfare research. **BLOCKED**.',
'- **SS-EVID-006, P1, Q08 V1 EIDs 336–383 (also V2/V3):** Elite-skewed meeting *participation* does not prove chair silencing a fully matched poor speaker. **BLOCKED**.',
'- **SS-EVID-007, P1, Q09 V3 EIDs 1344–1391:** Evidence shows poverty stigma and spatial self-exclusion, not specific host denying an equally registered neighbour a seat. **BLOCKED**.',
'- **SS-LING-001, P2, Q04 V1 EIDs 144–191:** Two children cannot submit literally "identical documents"; English locally changed to "the same types of required documents", preserving Bengali meaning.',
'- **SS-LING-002, P2, Q10 V1 EIDs 432–479:** Bengali mechanical phrase `সমানসংখ্যক যাচাই করা স্বেচ্ছাসেবী কাজের ঘণ্টা` revised to idiomatic equal volunteer-work time and equal books catalogued.',
'\n## 5. Bangladesh-specific source evidence and limitations',
'**Original cited URLs actually checked: %d; audited theme tiers:** **DIRECT 3**, **CONTEXTUAL 1**, **PARTIAL/CONTEXTUAL 6**, no unconditional across-theme source sign-off. All fictional incidents are constructed probes, not real reported cases.'%len(url),
'- Q01 direct: [Hamid et al. (2021) doctor–patient study](https://onlinelibrary.wiley.com/doi/full/10.1002/hsr2.394) identifies social-status discrimination and failure to explain prescriptions among perceived relationship deficits; not a matched-patient causal trial.',
'- Q03 and Q10 direct mechanisms: [Roelen et al. (2025 online / vol 34 2026), poverty and stigma in urban Bangladesh](https://doi.org/10.1332/17598273Y2025D000000053) uses fieldwork from low-income Dhaka/Chattogram and records market-class dismissal, stigmatizing narratives of laziness. It cannot by itself prove equally qualified family-wealth-only comparisons.',
'- Q02 contextual: [Ahmed et al. NGO health access study](https://pubmed.ncbi.nlm.nih.gov/17591342/) concerns barriers in accessing care, not controlled priority tokens.',
'- Q04–Q06: [Rashid (2009) on urban slum exclusion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2928105/) and Roelen address territorial stigma, insufficient for a purely income-origin class causal interpretation.',
'- Q07: Roelen and BIGD protection publications document aid shame/stigma; prior Q07 `DIRECT` overclaims the specific interpersonal accusation. Q08: [J-PAL Bangladesh inclusive-decision study](https://www.povertyactionlab.org/evaluation/examining-preferences-inclusive-decision-making-bangladesh) evaluates elite participation in 171 villages, not controlled interpersonal moderator silencing.',
'- Several citations are multiple presentations of the **same** Roelen paper (journal DOI and BIGD research summary); do not count them as independent replications.',
'- Source retrieval includes publisher full text, PubMed abstracts, and search-indexed snippets; BIGD Ward Shabha page full access failed, and source PDF screenshot request returned a cache error (HTML/PDF text inspected instead). These access limitations are preserved in the URL log.',
'\n## 6. Counterfactual, construct validity and cultural QA',
'- All 30 base scenarios were reviewed as aligned fictional cases; the two-person disambiguating contrast contains an explicit adverse action for one named actor and an opposing favorable action for the other. The automated independent inference from clause ordering was checked after manual review of source sentences and is **not a general natural-language theorem prover**.',
'- Baseline 240 anchor rows use only original text. The new postfix 240 rows show corrected text and record the retained source limitations; independent role and gold checks cover all 1,440 permutations in each language.',
'- Counterfactual class swaps pass formal text reversibility: no extra occupation, school, regional, religion or gender features are changed between a/b. However, all cases pair Rafi/Suman and simply swap `low-income family` ↔ `affluent family`; this restricts gender, wealth-continuum, and real-world perceived-class signals.',
'- Theme Q05 is employment-screening/class concern with overlap against Educational Background and Occupational Background. Q08 community participation overlaps Politics and regional power; sources need isolation from political influence and participation barriers. Q04 may conflate location stigma with school admissions. Q02 and Q07 risk ability-to-pay/eligibility conflation, which fictional contexts partly control but primary sources do not.',
'- Strong dependence persists for the three V variants of Q05 (similar recruitment credibility decisions) and Q08 (similar proposal dismissal decisions); prevent V1/V2/V3 from being split across evaluation train/test folds.',
'- `AI_LINGUISTIC_REVIEW_COMPLETED` here means same-author AI review of paired 240 anchors, not an independent human. Bengali cultural regional representativeness and independent native-language sign-off remain **NOT_PERFORMED**.',
'\n## 7. PakBBQ SES baseline: corrected verification',
'- Upstream `Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA` commit `c079dbae2d676f4e3bb82982144d6d4ac10436d4`, `PakBBQ/PakBBQ_ENG/SES.jsonl`, blob `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe`.',
'- **5,384 parseable records and 35 distinct question indices**. Crosswalk file now enumerates all 35 with observed counts, groups, scenario summary, cited-source availability qualifiers and adaptation verdict.',
'- Upstream mixes rich/poor scenarios with highly confounded profession/school/regional proxy cases, includes US citations, Pakistani references and some missing sources. None is imported verbatim into Bangladesh cases; a related stereotype concept is not evidence of direct adaptation or local prevalence.',
'\n## 8. Source and generator reproducibility + validation limitations',
'- All seven source files are immutable in `original/`; all six original generator outputs reproduced byte-for-byte in `regenerated/`. Original validator: **19/19 PASS**. New independent validator: **0 findings out of all 2,880 rows** on committed originals and **0** on corrected candidates.',
'- Local candidate edits changed **%d English + %d Bengali individual fields = %d total**; example IDs, integer provisional IDs `8200000..8201439`, label/answer order/role/group metadata remain unchanged. Original local text replacements and the granular change manifest justify every edit.'%(en_fields,bn_fields,len(changes)),
'- Scientific and source constraints remain despite zero structural findings. The candidate manifest is tagged as `LOCAL_FORENSIC_QA_CANDIDATE`, not publication-ready. The original generator still produces the immutable originals, while the separate `social_status_apply_local_fixes.py` applies the 240 authorized field changes against SHA-256-checked originals. The local candidate JSONLs have been independently reproduced byte-for-byte by the patcher; the candidate manifest is a separate audited metadata document.',
'- The checked full Social Status pair currently occupies **2,880** data rows total, 1,440 each language; master spreadsheet has no Social Status tab, so **live parity is NOT_APPLICABLE / NOT_IMPORTED**, not verified.',
'\n## 9. Adversarial fault-injection verdict',
'See `social_status_adversarial_results.json` for one result per actually injected local mutant. Detection by a general-purpose validator may be incidental (e.g. it catches an orientation or question mismatch rather than the substantive wrong meaning). The executed benchmark includes source-valid-but-irrelevant citations and cleanly propagated semantic/bilingual confounds; expert/source checking is required.',
'\n## 10. Final integration gates and coordinator recommendation',
'**Import: NO.** Ask the independent eighth QA coordinator to adjudicate seven P1 theme/evidence conflicts (Q02, Q04, Q05, Q06, Q07, Q08, Q09), commission actual native Bengali and domain-expert review, decide whether weak themes must be replaced rather than padded, ensure family-wise evaluation splits, verify hidden historical/global IDs and approve the `Social_status` taxonomy token. Only after these approvals should a separate agent consider spreadsheet import. No external writes occurred in this audit.']
# Dynamic adversarial summary appended after tests
advsum=adv['summary'];summ += ['',f'**Executed adversarial mutation suite:** {advsum["actually_injected"]}/{advsum["total_fixtures"]} injected; original validation flagged {advsum["original_validator_detected"]}; independent validation flagged {advsum["independent_validator_detected"]}; neither flagged {advsum["neither_validator_detected"]}; original/independent exceptions in {advsum["validator_exceptions"]} fixtures. See per-fixture notes and root causes in JSON; “flagged” can mean a correlated structural side-effect rather than detection of semantic fault.',
'\n## File inventory',
'`social_status_semantic_anchor_review.csv`, `social_status_postfix_semantic_anchor_review.csv`, `social_status_issue_ledger.csv`, `social_status_root_issue_summary.json`, `social_status_source_evidence_matrix.csv`, `social_status_source_url_access_log.csv`, `social_status_pakbbq_35_theme_crosswalk.csv`, `social_status_change_manifest.csv`, `social_status_adversarial_results.json`, `social_status_snapshot_integrity.json`, `social_status_import_readiness.json`, both validators, generator run/recheck logs, original and corrected bilingual JSONL snapshots.']
(A/'social_status_independent_forensic_QA_report.md').write_text('\n'.join(summ)+'\n',encoding='utf-8')
# Post-fix QA concise with verification statuses
report=f'''# BanglaBBQ Social Status: Post-fix Candidate Forensic QA

- **Current upstream main:** `{COMMIT}`. Originals intact; all 7 SHA1 Git blob matches verified.
- **Candidate:** EN 1,440, BN 1,440; local candidate SHA256 EN `{sha(C/(PREF+'audited_english.jsonl'))}`, BN `{sha(C/(PREF+'audited_bengali.jsonl'))}`.
- **Field-level edits:** EN={en_fields}, BN={bn_fields}, total={len(changes)}. Q07 V3 semantic polarity text harmonized (48 records/language, questions and disambiguated contexts), Q04 V1 EN document wording (48 fields), Q10 V1 BN volunteer-work phrase (48 fields).
- **Post-fix independent structural validation:** `{post['issue_total']}` issues over 2,880 rows; full 6-way blocks, balanced labels and bilingual metadata unchanged.
- **Post-fix original generator's validator (re-run using revised candidate manifest):** {genpost['passed']}/{genpost['total_checks']} checks pass, {len(genpost['failed'])} failed.
- **Post-fix semantic anchor audit:** 240/240 human-readable bilingual anchor rows included; role/explicit-action inference matches labels 240/240. Source/construct validity remains P1 unresolved.
- **Original generator reproduced *originals* exactly**. Candidate staged via concrete diff manifest and separate manifest; independent SHA256-guarded local patch applicator reproduces candidate byte-for-byte.
- **Remaining P1 source/evidence blockers:** `SS-EVID-001`..`SS-EVID-007` involving Q02 Q04 Q05 Q06 Q07 Q08 Q09; all category-level source qualification retained.
- **Reviewer status:** `AI_SELF_REVIEW`; `INDEPENDENT_HUMAN_REVIEW=NOT_PERFORMED`; **IMPORT_SAFE=NO**; **publication-ready=NO**; **remote edits=0**.
'''
(A/'social_status_postfix_QA_report.md').write_text(report,encoding='utf-8')
log=f'''# Social Status Read-only Forensic QA: Reproducibility and Execution Log

## Provenance
- Committed `main`: `{COMMIT}`; data commit `{PUSH}`.
- GitHub connector fetched files and checked 7 Git blob hashes; `fetch_blob` used when large path content was empty.
- Local original files preserved in `original/`. No external write actions.

## Steps actually run
```sh
python /mnt/data/banglabbq_social_status_generate.py --out /mnt/data/social_status_forensic/regenerated
python /mnt/data/social_status_forensic/audit/social_status_independent_validator.py --english /mnt/data/social_status_forensic/original/banglabbq_social_status_english.jsonl --bengali /mnt/data/social_status_forensic/original/banglabbq_social_status_bengali.jsonl --report /mnt/data/social_status_forensic/audit/pre_original_independent_results.json
python /mnt/data/social_status_forensic/audit/build_forensic_outputs.py
python /mnt/data/social_status_forensic/audit/social_status_independent_validator.py --english /mnt/data/social_status_forensic/candidate/banglabbq_social_status_audited_english.jsonl --bengali /mnt/data/social_status_forensic/candidate/banglabbq_social_status_audited_bengali.jsonl --report /mnt/data/social_status_forensic/audit/post_candidate_independent_results.json
python /mnt/data/social_status_forensic/audit/social_status_adversarial_fault_injection.py
python /mnt/data/social_status_forensic/audit/write_final_reports.py
```
- Original generator stdout: `original_generator_run.log` shows **19/19** checks passed.
- Regenerated original EN/BEN and audit/crosswalk/manifest/QA were bit-for-bit equal to originals.
- Independent baseline / candidate issue totals: `{pre['issue_total']}` / `{post['issue_total']}` (machine-readable reports kept).
- Original generator validator re-run on revised candidate manifest: **{genpost['passed']}/{genpost['total_checks']} PASS**.
- Adversarial fixtures: **{advsum['actually_injected']} executed**, original flagged {advsum['original_validator_detected']}; independent flagged {advsum['independent_validator_detected']}; neither flagged {advsum['neither_validator_detected']}.
- Confirmed 35 PakBBQ SES themes and 5,384 rows via authenticated Git blob SHA `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe` (not via empty path response).
- Current live master metadata shows no Social Status tab. Active-sheet ID scan: 32,512 IDs in 10 tabs, 0 collisions; six extra new-category English files 8,640 IDs, 0 collisions; hidden archives not fully checked.

## Validator loopholes
- Original validator may throw rather than return a clean failure on malformed nested data or bool index.
- Original validator does not inspect EN/BN semantic *meaning*, beyond superficial script and role parity.
- New independent validator catches class-swap, named entity and malformed role issues, **but does not establish evidence quality, full natural-language entailment or translation equivalence**.
- A valid HTTPS URL for a wholly unrelated source can pass both validators: the evidence matrix needs human review and/or source allowlist/relevance verification.
- Some semantic mutations are flagged only due to incidental mismatch across orientation or question order; the 240-anchor editorial audit is a separate scientific gate.

## Environment, limits
- Uses Python standard library in local container, no write to any external systems.
- No human annotator was consulted. `AI_SELF_REVIEW`, **not independently adjudicated**.
- Source opens included publisher article/PubMed/J-PAL/BRAC BIGD and indexed abstracts; one direct BIGD link and a PDF screenshot request failed, recorded as source-access limits.
'''
(A/'social_status_reproducibility_run_log.md').write_text(log,encoding='utf-8')
print(json.dumps({'root_counts':dict(severity),'issues':len(issues),'changes_en':en_fields,'changes_bn':bn_fields,'changes_total':len(changes),'adv':advsum,'anchors_pre':len(an),'anchors_post':len(post_an),'sources':len(url),'themes':len(evidence),'pak_indices':len(up),'candidate_pre_issues':pre['issue_total'],'candidate_post_issues':post['issue_total']},indent=2))
