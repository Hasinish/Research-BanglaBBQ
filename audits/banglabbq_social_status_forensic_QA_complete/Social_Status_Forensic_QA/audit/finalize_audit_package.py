#!/usr/bin/env python3
"""Verify all forensic deliverables, append verified follow-up findings and package ZIP.
All changes are to LOCAL audit artifacts only.
"""
import csv,hashlib,json,pathlib,zipfile,collections,os
BASE=pathlib.Path(__file__).resolve().parents[1];A=BASE/'audit';O=BASE/'original';C=BASE/'candidate';R=BASE/'regenerated';PREF='banglabbq_social_status_'
def loadj(x):return json.loads((A/x).read_text(encoding='utf-8'))
def loadcsv(x):return list(csv.DictReader((A/x).open(encoding='utf-8-sig',newline='')))
rv=loadcsv('social_status_30_scenario_editorial_reviews.csv');anc=loadcsv('social_status_semantic_anchor_review.csv');post=loadcsv('social_status_postfix_semantic_anchor_review.csv');up=loadcsv('social_status_pakbbq_35_theme_crosswalk.csv');src=loadcsv('social_status_source_evidence_matrix.csv');ledger=loadcsv('social_status_issue_ledger.csv');changes=loadcsv('social_status_change_manifest.csv');adv=loadj('social_status_adversarial_results.json');snap=loadj('social_status_snapshot_integrity.json');ready=loadj('social_status_import_readiness.json');fit=loadj('social_status_formula_injection_scan.json')
checks={
'originals_all_7_match_live_git_blobs':all(v['sha_verified_vs_latest_main'] for v in snap['source_originals'].values()),
'generator_byte_reproduction_all_6':all(snap['generator_byte_reproduction'].values()) and len(snap['generator_byte_reproduction'])==6,
'crosswalk_35_upstream_indices':len(up)==35 and [int(x['question_index']) for x in up]==list(range(1,36)),
'crosswalk_5384_upstream_rows':sum(int(x['total_records']) for x in up)==5384,
'crosswalk_864_upstream_uncited':sum(int(x['missing_source_records']) for x in up)==864,
'crosswalk_7_unreferenced_indices':[int(x['question_index']) for x in up if int(x['missing_source_records'])>0]==list(range(26,33)),
'30_unique_scenario_editorial_cases':len(rv)==30 and len({(x['theme'],x['variation']) for x in rv})==30,
'240_unique_original_bilingual_anchors':len(anc)==240 and len({x['anchor_id'] for x in anc})==240,
'240_unique_postfix_bilingual_anchors':len(post)==240 and len({x['anchor_id'] for x in post})==240,
'anchor_case_notes_all_present':all(x['specific_30_variation_AI_editorial_note'].strip() for x in anc+post),
'9_attempted_original_citation_urls':len(loadcsv('social_status_source_url_access_log.csv'))==9,
'10_evidentiary_theme_reviews':len(src)==10,
'317_root_and_field_level_ledger_entries':len(ledger)==317,
'240_exact_field_changes':len(changes)==240,
'33_mutation_fixtures_executed':adv['summary']['actually_injected']==33,
'original_and_corrected_bilingual_independent_structural_pass':loadj('pre_original_independent_results.json')['issue_total']==0 and loadj('post_candidate_independent_results.json')['issue_total']==0,
'corrected_original_generator_19_of_19_pass':loadj('post_candidate_original_generator_validation.json')['passed']==19,
'no_formula_injection_orig_candidates':all(x['possible_formula_injection']==0 and x['checked']==2880 for x in fit.values()),
'patch_script_exact_candidate_reproduction':all(hashlib.sha256((BASE/'repatched'/(PREF+'audited_'+lang+'.jsonl')).read_bytes()).hexdigest()==snap['candidate_sha256'][lang] for lang in ('english','bengali')),
'not_safe_to_import':ready['safe_to_import']==False and ready['imported']==False,
}
assert all(checks.values()),{k:v for k,v in checks.items() if not v}
# Correct only ledger status of the documentation-only crosswalk repair (no JSONL edit).
for row in ledger:
 if row['issue_id']=='SS-PAK-001':row['status']='APPLIED_LOCAL_CROSSWALK_ONLY'
with (A/'social_status_issue_ledger.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(ledger[0]));w.writeheader();w.writerows(ledger)
# Report addendum, grounded exclusively in executed tests and authoritative raw inputs.
more='''
## 11. Additional forensic checks completed after initial report

- **Upstream source presence:** The 35-theme PakBBQ crosswalk now includes actual per-index citation status from the full Git blob. Exactly **864/5,384** upstream records in indices **26–32** have no source URL; 4,520 rows contain URLs, not necessarily reliable or Bangladesh-specific sources. Indices 20–21 contain a suspicious `.com` suffix after an article identifier; citation validity is not assumed.
- **Specific scenario editorial work:** `social_status_30_scenario_editorial_reviews.csv` lists 30 distinct real BN/EN cases with source/construct caveats, Bengali+English disambiguating predicates, explicit questions and venue-specific review notes; all **240** original and postfix anchor rows inherit their corresponding case-specific notes. These are **AI_SELF_REVIEW** findings and automated role/gold checks, not an independent 240-case human panel.
- **Formula-injection scan executed:** 2,880 original and 2,880 candidate rows, checking context, question, and all three options for spreadsheet formula-leading `=`, `+`, `-`, `@`: **zero hits**; actual Google Sheets import not performed.
- **Corrected candidate *independently reproducible*:** `social_status_apply_local_fixes.py` reads SHA-256-pinned immutable originals, applies precisely **120 EN and 120 BN field edits** from the granular manifest, and reproduces the local corrected JSONLs **byte-for-byte** (SHA-256 verified), without GitHub or Sheets writes. This supersedes an earlier statement that a candidate patcher did not yet exist.
- **Adversarial suite exact result:** **33** injections attempted/executed. Original validator gave controlled detection for **23**, independent implementation detected **28**; **five** cleanly propagated semantic/source defects escaped *both* automated validators (FX26, FX30, FX31, FX32, FX33). Two structurally malformed cases caused the original validator to throw exceptions rather than provide controlled failure statuses. See JSON for exact mutation, modified rows, failure tests, and exceptions. These are no human annotations.
- **Reviewer caveat:** The author AI manually examined all **30 distinct authored scenario variations**, while **240 anchors** were systematically instantiated, compared and assessed using case-specific notes and a constrained name/predicate inference heuristic. This is **not equivalent to 240 independently adjudicated human judgments** or full population linguistic certification.
'''
p=A/'social_status_independent_forensic_QA_report.md';s=p.read_text(encoding='utf-8');marker='## 11. Additional forensic checks completed after initial report';s=s.split(marker)[0].rstrip()+'\n'+more;p.write_text(s,encoding='utf-8')
p=A/'social_status_postfix_QA_report.md';s=p.read_text(encoding='utf-8');s+='\n- **Candidate reproducibility independent patcher:** 120 EN + 120 BN field replacements, byte-identical recreation against SHA256-pinned sources (`candidate_reconstruction_run.log`).\n- **Evidentiary status unchanged by local edits:** seven unresolved P1 issues; not import-safe.\n';p.write_text(s,encoding='utf-8')
p=A/'social_status_reproducibility_run_log.md';s=p.read_text(encoding='utf-8');s+='''
## Additional verified commands and outputs
```sh
python /mnt/data/social_status_forensic/audit/enrich_upstream_crosswalk.py
python /mnt/data/social_status_forensic/audit/enrich_editorial_review.py
python /mnt/data/social_status_forensic/audit/social_status_apply_local_fixes.py --original-dir /mnt/data/social_status_forensic/original --changes /mnt/data/social_status_forensic/audit/social_status_change_manifest.csv --out /mnt/data/social_status_forensic/repatched --expected-out-sha-json /mnt/data/social_status_forensic/audit/social_status_snapshot_integrity.json
python /mnt/data/social_status_forensic/audit/finalize_audit_package.py
```
- Crosswalk exact source URL presence: 864 uncited records in indices 26-32; `enrich_upstream_crosswalk.py` uses per-index aggregates calculated by connected upstream Git blob parser rather than silently inventing evidence.
- Candidate patch script successfully verified exact output hashes in `candidate_reconstruction_run.log`.
- Source and semantic review gaps remain explicitly open despite machine checks passing.
''';p.write_text(s,encoding='utf-8')
(A/'social_status_audit_artifact_integrity_checks.json').write_text(json.dumps({'checks':checks,'passed':sum(checks.values()),'total':len(checks),'final_status':'COMPLETE_STRUCTURAL_AUDIT_WITH_UNRESOLVED_SCIENTIFIC_BLOCKERS','no_remote_writes':True},indent=2)+'\n',encoding='utf-8')
# Final user-facing consolidated archive. Include ORIGINAL, original regenerated, corrected and repatched, all logs/scripts.
zip_path=pathlib.Path('/mnt/data/banglabbq_social_status_forensic_QA_complete.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for file in sorted(BASE.rglob('*')):
  if file.is_file() and file.name!='adversarial_pid.txt' and '__pycache__' not in file.parts:
   z.write(file,arcname='Social_Status_Forensic_QA/'+file.relative_to(BASE).as_posix())
with zipfile.ZipFile(zip_path) as z:
 bad=z.testzip();assert bad is None
 info={'archive_bytes':zip_path.stat().st_size,'members':len(z.namelist()),'zip_integrity':'PASS','archive_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
(A/'zip_delivery_integrity.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
# zip_delivery_integrity is created after ZIP by design; do not modify ZIP after test; external manifest is separate.
print(json.dumps({'checks_passed':sum(checks.values()),'checks_total':len(checks),'archive':str(zip_path),**info},indent=2))
