#!/usr/bin/env python3
"""Creates QA release report, import gate, and reproducibility run log from actual local test files."""
import csv,hashlib,json,pathlib,collections,subprocess,sys,datetime,shutil,tempfile
R=pathlib.Path(__file__).resolve().parents[1]
load=lambda n:json.loads((R/n).read_text())
initial=load('original_validation.json');final=load('postfix_validation.json');fi=load('physical_appearance_adversarial_results.json');fip=load('physical_appearance_adversarial_postfix_results.json');gb=load('generator_reproducibility.json');rep=load('local_repair_summary.json');issues=load('work/issue_summary.json');metrics=load('physical_appearance_structural_metrics.json')
source=list(csv.DictReader((R/'physical_appearance_source_evidence_matrix.csv').open()))
anchors=list(csv.DictReader((R/'physical_appearance_semantic_anchor_review.csv').open()))
ledger=list(csv.DictReader((R/'physical_appearance_issue_ledger.csv').open()))
assert len(source)==10 and len(anchors)==240 and len(ledger)==1078
assert initial['finding_total']==288 and final['finding_total']==0
assert fi['summary']['fixtures_executed']==26 and fip['summary']['fixtures_executed']==26
assert fi['summary']['independent_expected_detection_success']==26 and fip['summary']['independent_expected_detection_success']==26

# Verify candidate repair script deterministically reproduces the local files across two executions.
hashes=[];keys=['banglabbq_physical_appearance_audited_english.jsonl','banglabbq_physical_appearance_audited_bengali.jsonl','physical_appearance_change_manifest.csv']
for run in range(2):
    p=subprocess.run([sys.executable,str(R/'physical_appearance_local_repair.py')],cwd=str(R),capture_output=True,text=True,timeout=30)
    if p.returncode:raise AssertionError(f'local repair rerun {run} failed {p.stderr[:200]}')
    hashes.append({k:hashlib.sha256((R/k).read_bytes()).hexdigest() for k in keys})
assert hashes[0]==hashes[1]
# Assert exact manifest-cell changes and completely unchanged 15-key structure, IDs, labels, metadata, EN.
E=[json.loads(s) for s in (R/'ORIGINAL/banglabbq_physical_appearance_english.jsonl').read_text().splitlines()]
B=[json.loads(s) for s in (R/'ORIGINAL/banglabbq_physical_appearance_bengali.jsonl').read_text().splitlines()]
EE=[json.loads(s) for s in (R/'banglabbq_physical_appearance_audited_english.jsonl').read_text().splitlines()]
BB=[json.loads(s) for s in (R/'banglabbq_physical_appearance_audited_bengali.jsonl').read_text().splitlines()]
assert E==EE
changed_eids=[];changes=[]
for i,(x,y) in enumerate(zip(B,BB)):
  if x!=y:changed_eids.append(i)
  for k in x:
    if x[k]!=y[k]:changes.append((i,k))
assert len(changes)==rep['field_changes']==1008 and len(changed_eids)==rep['records_modified']==720
assert all(k in ('context','question') for _,k in changes)
assert all(x['answer_info']==y['answer_info'] and x['additional_metadata']==y['additional_metadata'] and x['label']==y['label'] and x['example_id']==y['example_id'] and x['id']==y['id'] for x,y in zip(B,BB))

# The final version has no source-specific evidence adjudication by a human.
TIER=collections.Counter(x['independent_evidence_tier'] for x in source)
STATUS=collections.Counter(x['decision'] for x in source)
quant={
 'category':'Physical_appearance','audited_commit':'e186b283fa5b184058e2cb395273e9968a893b20','audited_commit_utc':'2026-10-26T06:18:04Z',
 'english_original_git_blob':'f765b998a90b0abb02526615f01fe023d0e39242','bengali_original_git_blob':'a39f9156da45a8b3b8bda021d3d839eeddfef879',
 'per_language_rows':1440,'source_theme_counts':dict(TIER),'source_theme_decisions':dict(STATUS),
 'original_automated_findings':initial['finding_total'],'postfix_automated_findings':final['finding_total'],
 'original_per_row_semantic_anchors_reviewed':len(anchors),'original_semantic_anchor_bilingual_failures':issues['semantic_anchor_original_failures'],
 'postfix_semantic_anchor_bilingual_failures':issues['semantic_anchor_local_after_failures'],
 'original_validator_adversarial_detection':fi['summary']['original_validator_detected_any'],
 'independent_validator_adversarial_detection':fi['summary']['independent_expected_detection_success'],
 'adversarial_fixtures':fi['summary']['fixtures_executed'],'postfix_adversarial_detection':fip['summary']['independent_expected_detection_success'],
 'issue_ledger_row_counts_by_severity':issues['severity_row_counts'],'issue_ledger_row_counts_by_status':issues['resolution_status'],
 'local_modified_BN_records':len(changed_eids),'local_changed_BN_fields':len(changes),'local_modified_EN_records':0,
 'original_blind_gold_rows_tested':initial['checked']['blind_gold_all_rows_English']+initial['checked']['blind_gold_all_rows_Bengali'],
 'postfix_blind_gold_rows_tested':final['checked']['blind_gold_all_rows_English']+final['checked']['blind_gold_all_rows_Bengali'],
 'independent_human_review':'NOT_PERFORMED','import_safe':False,'github_or_sheet_writes':0
}
(R/'physical_appearance_quantitative_results.json').write_text(json.dumps(quant,ensure_ascii=False,indent=2)+'\n')

# ID gate findings from verified live connector results earlier this session.
readiness={
 'category':'Physical_appearance','source_of_truth':'GitHub current main e186b283fa5b184058e2cb395273e9968a893b20',
 'working_master':'https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit',
 'live_physical_appearance_sheets':'ABSENT_IN_LIVE_METADATA_37_TABS','import_status':'NOT_IMPORTED',
 'jsonl_canonical_15_top_level_keys':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
 'google_sheets_A_to_O':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id'],
 'metadata_cell_conversion':{'answer_info':'json.dumps(...,ensure_ascii=False), string cell','additional_metadata':'json.dumps(...,ensure_ascii=False), string cell'},
 'per_language_rows':1440,'new_sheet_rows_including_header_per_language':1441,'new_sheet_count_needed':2,
 'candidate_id_range':[8100000,8101439],'id_status':'RESERVED_PROVISIONAL_NOT_APPROVED',
 'id_collision_other_six_new_bundle_en_bn':'ZERO_DETECTED_12_JSONL_17280_RECORDS_SCAN',
 'id_collision_live_active_10_sheets':'ZERO_DETECTED_BY_STRING_PREFIX_810_IN_ACTIVE_ID_COLUMN',
 'id_collision_global_legacy_and_hidden_backups':'NOT_FULLY_AUDITED; DO_NOT_CALL APPROVED',
 'formula_injection_scan':'PASS_FOR_CURRENT_CANDIDATE_CONTEXT_QUESTIONS_OPTIONS_BY_INDEPENDENT_VALIDATOR',
 'utf8_valid_jsonl_and_15_field_schema':'PASS',
 'six_way_and_gold_label_balance':'PASS',
 'bilingual_automated_postfix_parity':'PASS_FOR_IMPLEMENTED_RULES',
 'semantic_human_adjudication':'NOT_PERFORMED',
 'source_evidence_critical_issues':'UNRESOLVED: Q02/Q03/Q04/Q05/Q06/Q07/Q08/Q10 and Q02 full-text access limitation',
 'source_tier_calibration_required':'Q06 and Q08 were overstated DIRECT, independent evidence judged PARTIAL/CONTEXTUAL',
 'lineage_inclusion':'NEW LOCAL 10 THEME EXTENSION; LEGACY RECORDS NOT RETAINED BYTE FOR BYTE IN OUTPUT; original seniors baseline preserved separately',
 'automated_validation_pass_not_equal_to_scientific_validation':True,
 'safe_to_import':False,'safe_for_publication':False,
 'next_steps':['Require independent Bangladesh social-science source adjudication of theme-mechanism match','Decide whether Q02/Q03/Q04/Q05/Q06/Q07/Q08/Q10 must be rewritten or excluded','Resolve Q03 V1 Bengali editorial phrase and synchronize generator/manifest before candidate changes','Obtain separate bilingual native-speaker reviewer signoff','Re-run full cross-category/global IDs and production import QA; do not append candidate until approved'],
 'remote_writes':0
}
(R/'physical_appearance_import_readiness.json').write_text(json.dumps(readiness,ensure_ascii=False,indent=2)+'\n')

runlog={'run_date_utc':'2026-10-26','project_commit':quant['audited_commit'],
 'commands_executed':[
 'python physical_appearance_independent_validator.py --english ORIGINAL/..english.jsonl --bengali ORIGINAL/..bengali.jsonl --manifest ORIGINAL/..manifest.json --result original_validation.json --anchors work/anchor_baseline.csv',
 'python physical_appearance_adversarial_runner.py [ORIGINAL]',
 'python physical_appearance_local_repair.py [local candidates, only Bengali]',
 'python physical_appearance_independent_validator.py --english banglabbq_physical_appearance_audited_english.jsonl --bengali banglabbq_physical_appearance_audited_bengali.jsonl --manifest ORIGINAL/..manifest.json --result postfix_validation.json --anchors work/anchor_postfix.csv',
 'PA_AUDIT_POSTFIX=1 python physical_appearance_adversarial_runner.py',
 'Original generator validation called using importlib on both baseline and local candidates (0 original-generator errors both times)',
 'Original generator CLI executed twice in isolated temporary directories (both exited 0; generated EN,BN,manifest,source_audit,crosswalk byte-identical with downloaded prior chat copies)',
 'Local repair executed twice; candidate EN/BN and diff manifest SHA-256 identical between local reruns'
 ],
 'source_blobs_confirmed':{'en':initial['github_blob_english'],'bn':initial['github_blob_bengali']},
 'original_generator_reproduction':gb['local_reproduction'],
 'local_repair_sha256_runs':hashes,
 'candidate_exact_changes':{'eng_rows_changed':0,'bn_rows_changed':len(changed_eids),'bn_fields_changed':len(changes),'modified_fields':['context','question']},
 'independent_validator_result_files':['original_validation.json','postfix_validation.json'],
 'fault_injection_result_files':['physical_appearance_adversarial_results.json','physical_appearance_adversarial_postfix_results.json'],
 'original_vs_patched_script_validator_differences':['Original validator missed 288 baseline row-level BN meaning deviations','Independent validator found them; both pass patched candidates at structural layer','Original validator misses five deliberate adversarial cases; independent expected-check detector flagged 26/26'],
 'not_performed':['Actual external human evaluation','Full text access to Q02 PMC/PubMed pages beyond indexed abstract','Full global ID crosswalk with every hidden Sheet and all historical snapshots','Raw entire GitHub source/crosswalk CSV files re-downloaded into runtime; current source audit values checked via connected GitHub, previous local copies have slightly differing byte hashes'],
 'remote_writes':0}
(R/'physical_appearance_reproducibility_run_log.json').write_text(json.dumps(runlog,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(quant,ensure_ascii=False,indent=2))
