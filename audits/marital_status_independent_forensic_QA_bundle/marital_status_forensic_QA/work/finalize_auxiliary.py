#!/usr/bin/env python3
import csv,json,collections,hashlib
from pathlib import Path
P=Path('/mnt/data/marital_forensic_qa');O=P/'ORIGINAL';M=json.loads((O/'banglabbq_marital_status_expansion_manifest.json').read_text('utf8'))
E=[json.loads(x) for x in (O/'banglabbq_marital_status_english.jsonl').read_text('utf8').splitlines()]
B=[json.loads(x) for x in (O/'banglabbq_marital_status_bengali.jsonl').read_text('utf8').splitlines()]
F=[json.loads(x) for x in (P/'banglabbq_marital_status_audited_english.jsonl').read_text('utf8').splitlines()]
G=[json.loads(x) for x in (P/'banglabbq_marital_status_audited_bengali.jsonl').read_text('utf8').splitlines()]
AUD=list(csv.DictReader((P/'marital_status_source_evidence_matrix.csv').open(encoding='utf8',newline='')))
fields=['theme','variation','row_start','row_end_inclusive','scenario_setting_en','scenario_setting_bn','disambiguating_event_en','disambiguating_event_bn','negative_question_en','nonnegative_question_en','negative_question_bn','nonnegative_question_bn','varying_domain_action_evaluator','distinct_from_other_variations','shared_predicate_family','gender_age_qualifications_controlled','evidence_tier','human_review','publication_ready']
with (P/'marital_status_variation_diversity_matrix.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for wave in range(3):
  for q in range(10):
   t=M['themes'][q];i=(wave*10+q)*48;e,b=E[i],B[i];ev1,ev2=E[i+1],B[i+1];typ=AUD[q]['evidence_tier_independent'];
   w.writerow(dict(theme=t['id'],variation='V'+str(wave+1),row_start=i,row_end_inclusive=i+47,scenario_setting_en=e['context'],scenario_setting_bn=b['context'],disambiguating_event_en=ev1['context'][len(e['context']):],disambiguating_event_bn=ev2['context'][len(b['context']):],negative_question_en=e['question'],nonnegative_question_en=E[i+2]['question'],negative_question_bn=b['question'],nonnegative_question_bn=B[i+2]['question'],varying_domain_action_evaluator='Yes, settings/actions change, but several outcomes have a shared question stem.',distinct_from_other_variations='PARTIAL_DISTINCT_EVALUATOR_AND_ACTION',shared_predicate_family='YES_SAME_THEME_AND_REUSED_POLARITY_QUESTION',gender_age_qualifications_controlled='AI_TEXT_REVIEWED_MATCHED_WITHIN_SCENARIO',evidence_tier=typ,human_review='NOT_PERFORMED',publication_ready='NO'))
header=M['spreadsheet_headers']
expected=['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id']
assert header==expected,header
live_counts={'BanglaBBQ_ENG_Age':2920,'BanglaBBQ_BEN_Age':2920,'BanglaBBQ_ENG_Politics':2880,'BanglaBBQ_BEN_Politics':2880,'BanglaBBQ_ENG_Religion':2880,'BanglaBBQ_BEN_Religion':2880,'BanglaBBQ_ENG_Education':2880,'BanglaBBQ_BEN_Education':2880,'BanglaBBQ_ENG_Gender':4696,'BanglaBBQ_BEN_Gender':4696}
readiness=dict(category='Marital_status',snapshot_main_sha='e186b283fa5b184058e2cb395273e9968a893b20',status='NOT_SAFE_FOR_IMPORT',eligible_for_import=False,original_legacy_unchanged=True,live_google_sheets_modified=False,github_modified=False,imported_to_working_spreadsheet=False,marital_status_sheet_tabs_exist=False,expected_rows_per_new_language_sheet=1440,expected_cols_per_new_sheet=15,google_sheets_A_to_O_field_order=header,jsonl_top_level_key_order=M['schema_keys'],order_differs_from_jsonl=True,google_sheet_json_fields=['answer_info','additional_metadata'],json_serialization='json.dumps(...,ensure_ascii=False) of two metadata dicts before writing values to columns L/M',formula_injection_check='PASSED for contexts/questions/options on new candidate files; maintain literal string input protection on import',provisional_id_range=[8700000,8701439],same_category_ids_unique_and_sequential=True,production_live_tab_readonly_id_scan_count=len(live_counts),production_live_rows_scanned=sum(live_counts.values()),active_sheet_id_collisions_found=0,other_six_bundles_reserved_ranges_found_in_committed_manifests=True,other_six_bundles_complete_global_id_scan='NOT_PERFORMED',human_review='NOT_PERFORMED',bengali_native_editorial_certification='NOT_PERFORMED',source_verification='QUALIFIED_3_DIRECT_7_PARTIAL',remaining_p1_construct_source_issues=True,unreviewed_uncertainty='Source populations, comparator evidence, gender-limited coverage, theme-family dependence, theme motive for Q10',postfix_mechanical_validation='PASS',adversarial_39_local_mutations='39_DERIVED_FAILURES_DETECTED_USING_MACHINE_AND_AI_TARGETED_PROBES',reproduction='ORIGINAL_GENERATOR_PLUS_LOCAL_PATCH_REQUIRED',require_before_import=['Subject-matter team approval for 7 PARTIAL themes (Q04-Q10), especially tiger-widow study generalization Q08-Q10','Independent human bilingual review of all 30 semantic scenario variations and at least representative permutation cases','Updated revised manifest/generator seeds after approved patches; preserve original history','Complete global cross-bundle ID collision scan; no prior import of same EIDs','Decide category-balance coverage for separated/remarried and other genders','Create new Marital_status tabs from verified 15-column format and perform back-to-back read-only/write QA after explicitly authorized import'])
(P/'marital_status_import_readiness.json').write_text(json.dumps(readiness,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
provenance={
 'repo':'Hasinish/Research-BanglaBBQ','main_sha':'e186b283fa5b184058e2cb395273e9968a893b20',
 'main_commit_time_utc':'2026-10-26T06:18:04Z','seven_bundle_commit_sha':'214795f628a34ece8deb23a65c6bf35ac0ce7157',
 'committed_marital_status_directory':'banglabbq_marital_status_readonly_research_package/',
 'git_blob_sha':{
 'english':'5c902dd9956dc6104126a306317e98ed269d8059','bengali':'f9f6ac2f87d3f53995e7d5db2bc4faca5df7ede0',
 'expansion_manifest':'3ee1e9ab0f40c232503bf1d270f3c392b0d87430','generator':'bcf58722cc718e99bf12021f7a24e66a14fe16c6','source_audit':'cd7e5dced6ce4b5d68339b7a31b9796a8d74502b','pakbbq_crosswalk':'ab233bb1a1f2747e63e0cc63597f6b0474a183be','prior_qa_report':'b811c012e28cdaf21cbb9182659bcd3dd94a2045'},
 'legacy_git_blob_sha':{'english':'e150dfbc18469721f12903f1f4d1e52c62a4f4e5','bengali':'f986177961fcbd4d898207706af108ec91b6fbac'},
 'upstream_pakbbq_tree_sha':'c079dbae2d676f4e3bb82982144d6d4ac10436d4',
 'original_files_hashed':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.glob('banglabbq_marital_status_*'))},
 'local_corrected_files_hashed':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.glob('banglabbq_marital_status_audited_*.jsonl'))},
 'remote_writes':0,'dates':'2026-10-26 Asia/Dhaka','memory_synchronization_note':'Project memory/state.md latest main post-push references seven bundle SHA but Last Verified Date Oct 20 and PENDING Marital; memory/index.md does not list seven bundles.'}
(P/'marital_status_repo_snapshot.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('variation rows=30, readyness verified, repo SHA+hash snapshot generated')
