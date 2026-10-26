#!/usr/bin/env python3
"""Verify the already-executed isolated local generator run against original GitHub blobs.
To perform a new regen run, execute original banglabbq_health_status_generate.py
in a separate directory; generation may be slow. This script does NOT rerun it.
"""
import hashlib,json
from pathlib import Path
R=Path('/mnt/data');G=R/'health_forensic_work/regenerated'
files=['banglabbq_health_status_english.jsonl','banglabbq_health_status_bengali.jsonl','banglabbq_health_status_expansion_manifest.json','banglabbq_health_status_generate.py','banglabbq_health_status_source_audit.csv','banglabbq_health_status_pakbbq_theme_crosswalk.csv','banglabbq_health_status_qa_report.md']
blobs={'banglabbq_health_status_english.jsonl':'a637d6ac18ac901c7a22356dbf47d244230e63b2','banglabbq_health_status_bengali.jsonl':'525d72db59ad609d07cf855f128aa09a6da936da','banglabbq_health_status_expansion_manifest.json':'d9a16b6635461d48522e07f58669bffd093d4b66','banglabbq_health_status_generate.py':'4c107612d5c9b043b8e229aa5ef3c95939aa4399','banglabbq_health_status_source_audit.csv':'236be8fbe941839c61e55be1357a3549b166bdb1','banglabbq_health_status_pakbbq_theme_crosswalk.csv':'bf80053cdbf13acb253330c03456339a2c36275a','banglabbq_health_status_qa_report.md':'ca8e7b30caede493a4ac6fef824884a19a285b99'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
records=[]
for n in files:
 a=R/n;g=G/n
 records.append({'file':n,'exists_regenerated':g.exists(),'original_sha256':sha(a),'regenerated_sha256':sha(g) if g.exists() else None,'byte_equal_to_local_seed':a.read_bytes()==g.read_bytes() if g.exists() else None,'local_git_blob':blob(a),'regenerated_git_blob':blob(g) if g.exists() else None,'committed_git_blob':blobs[n],'original_seed_equals_committed_blob':blob(a)==blobs[n],'regenerated_equals_committed_blob':blob(g)==blobs[n] if g.exists() else None})
run_stdout=R/'health_forensic_work/regenerate_stdout.txt';s=run_stdout.read_text() if run_stdout.exists() else ''
info={'commit':'e186b283fa5b184058e2cb395273e9968a893b20','bundle_push_commit':'214795f628a34ece8deb23a65c6bf35ac0ce7157','run_utc':'2026-10-26','generation_record':'Prior isolated local generator execution stored under health_forensic_work/regenerated and its captured stdout; this script independently hashes/re-reads those exact artifacts. A second attempted isolated generator run exceeded a 24-second test limit and is not claimed as a second successful run.','prior_generation_report_json':json.loads(s) if s.strip().startswith('{') else {'raw_stdout':s},'regeneration_status':'PRIOR_RUN_OUTPUT_AVAILABLE','files':records,'original_jsonl_byte_reproducible':all(r['regenerated_equals_committed_blob'] for r in records if r['file'].endswith('.jsonl')),'source_csv_discrepancy':'Committed source-audit/crosswalk blob hashes differ from local reproducible generated CSV files. Committed CSV bytes were read by connector but not materialized to container: no record-by-record diff calculated.'}
(R/'health_status_reproducibility_log.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('local regeneration equal',sum(bool(x['byte_equal_to_local_seed']) for x in records),'/',len(records),'matched committed blobs',sum(x['original_seed_equals_committed_blob'] for x in records),'/',len(records))
