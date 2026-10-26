#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,zipfile
R=Path(__file__).resolve().parent
zip_path=R/'Ethnicity_forensic_QA_complete.zip'
artifacts=[
'Ethnicity_independent_forensic_QA_report.md',
'Ethnicity_issue_ledger.csv',
'Ethnicity_source_evidence_matrix.csv',
'Ethnicity_semantic_anchor_review.csv',
'Ethnicity_adversarial_results.json',
'Ethnicity_source_oracle_fault_injection_results.json',
'Ethnicity_independent_validator.py',
'Ethnicity_import_readiness.json',
'banglabbq_ethnicity_audited_english.jsonl',
'banglabbq_ethnicity_audited_bengali.jsonl',
'Ethnicity_change_manifest.csv',
'Ethnicity_postfix_QA_report.md',
'Ethnicity_audited_scenario_templates.json',
'Ethnicity_audited_expansion_manifest.json',
'Ethnicity_template_change_log.csv',
'Ethnicity_source_url_access_log.csv',
'Ethnicity_pakbbq_independent_crosswalk_audit.csv',
'Ethnicity_taxonomy_boundary_review.csv',
'Ethnicity_local_repro_execution.json',
'Ethnicity_forensic_statistics.json',
'Ethnicity_independent_provenance_crosscheck.json',
'Ethnicity_validation_run_log.md',
'pre_fixes_independent_results.json',
'post_fixes_independent_results.json',
'postfix_final_rerun_validator_results.json',
'repro_compare.json',
'local_corrections_summary.json',
'check_provenance_independent.py',
'verify_source_oracle_injections.py',
'apply_justified_local_repairs.py',
'build_qa_artifacts.py',
'finish_qa_reports.py',
'run_adversarial_ethnicity.py',
'package_forensic_ethnicity.py',
'adv_batch0.txt','adv_batch1.txt','adv_batch2.txt','adv_fix_F13.txt','adv_fix_F28.txt',
'ORIGINAL/banglabbq_ethnicity_english.jsonl',
'ORIGINAL/banglabbq_ethnicity_bengali.jsonl',
'ORIGINAL/banglabbq_ethnicity_expansion_manifest.json',
'ORIGINAL/banglabbq_ethnicity_scenario_templates.json',
'ORIGINAL/banglabbq_ethnicity_source_audit.csv',
'ORIGINAL/banglabbq_ethnicity_pakbbq_theme_crosswalk.csv',
'ORIGINAL/banglabbq_ethnicity_qa_report.md',
'ORIGINAL/generate_ethnicity.py',
'ORIGINAL/validate_ethnicity_independent.py'
]
for fn in artifacts:assert (R/fn).is_file(),fn
readme='''# Ethnicity independent forensic QA - package index

Created 2026-10-26 from GitHub main HEAD e186b283fa5b184058e2cb395273e9968a893b20.

START WITH: Ethnicity_independent_forensic_QA_report.md.
The ORIGINAL/banglabbq_ethnicity_{english,bengali}.jsonl copies match committed Git blob SHAs exactly.

IMPORTANT: The mounted ORIGINAL/source-audit and crosswalk CSVs are not byte-identical to the current committed GitHub ancillary CSV files. They are retained to reproduce the prior local generator; the newly independent source matrix/crosswalk and this caveat govern evidence conclusions.

The locally corrected JSONLs are candidates only, not approved, not publication-ready, and were not uploaded to any service.
No human independent linguistic review was performed. Q06-Q10 evidence/construct issues are unresolved.

The file Ethnicity_bundle_sha256_manifest.csv inventories exact exported ZIP contents.
For command lines and actual execution evidence, read Ethnicity_validation_run_log.md and Ethnicity_local_repro_execution.json.
'''
(R/'README_FIRST.md').write_text(readme,encoding='utf-8')
artifacts.insert(0,'README_FIRST.md')
manifest=[]
for name in artifacts:
 p=R/name
 manifest.append({'relative_path':name,'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (R/'Ethnicity_bundle_sha256_manifest.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=manifest[0].keys());w.writeheader();w.writerows(manifest)
artifacts.append('Ethnicity_bundle_sha256_manifest.csv')
if zip_path.exists():zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for fn in artifacts:z.write(R/fn,arcname=fn)
with zipfile.ZipFile(zip_path) as z:
 assert len(z.namelist())==len(artifacts)
 assert z.testzip() is None
 for row in manifest:
  assert hashlib.sha256(z.read(row['relative_path'])).hexdigest()==row['sha256']
print(json.dumps({'zip_file':str(zip_path),'zip_size_bytes':zip_path.stat().st_size,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'zipped_items':len(artifacts),'contents_crc_check':'PASS','sha256_contents_check':'PASS','essential':['Ethnicity_independent_forensic_QA_report.md','Ethnicity_issue_ledger.csv','Ethnicity_source_evidence_matrix.csv','Ethnicity_semantic_anchor_review.csv','Ethnicity_adversarial_results.json','Ethnicity_independent_validator.py','Ethnicity_import_readiness.json','banglabbq_ethnicity_audited_english.jsonl','banglabbq_ethnicity_audited_bengali.jsonl']},indent=2))
