#!/usr/bin/env python3
"""Local-only candidate manifest derived from committed manifest, with patch lineage and calibrated evidence tiers."""
import copy,hashlib,json
from pathlib import Path
from health_status_apply_local_repairs import PATCHES
ROOT=Path('/mnt/data')
original=json.loads((ROOT/'banglabbq_health_status_expansion_manifest.json').read_text(encoding='utf-8'))
audited=copy.deepcopy(original)
for (iid,sev,q,v,lang,field,old,new,why,condition) in PATCHES:
 t=audited['variations'][(v-1)*10+(q-1)]['base_bilingual_template']; c=0
 for k,val in t.items():
  if k.endswith('_en') and lang!='english': continue
  if k.endswith('_bn') and lang!='bengali':continue
  if isinstance(val,str):
   if old in val:t[k]=val.replace(old,new);c+=1
  elif isinstance(val,dict):
   for sk,sv in val.items():
    if old in sv:val[sk]=sv.replace(old,new);c+=1
 # Some patches apply to generated health/status phrases outside the base template.
 # Repeated separate orientation edits can be absent from template; Q05 exception only.
for var in audited['variations']:
 q=int(var['theme_id'][1:]);var['evidence_tier']=({2:'PARTIAL',4:'UNSUPPORTED',7:'PARTIAL',8:'PARTIAL'}.get(q,var['evidence_tier']))
audited['status']='LOCAL_FORENSIC_REPAIR_CANDIDATE_NOT_APPROVED_FOR_IMPORT'
audited['publication_ready']=False
audited['forensic_repair']={
 'date_utc':'2026-10-26',
 'source_commit':'e186b283fa5b184058e2cb395273e9968a893b20',
 'base_source_manifest_blob':'d9a16b6635461d48522e07f58669bffd093d4b66',
 'local_change_manifest':'health_status_change_manifest.csv',
 'repair_script':'health_status_apply_local_repairs.py',
 'evidence_tier_policy':'Q02/Q07/Q08 downgraded to PARTIAL; Q04 blocked UNSUPPORTED for health-history-only construct; others retained with limitations; no sources replaced',
 'source_review_is_human':'NO',
 'import_safe':'NO',
 'unmodified_committed_jsonl_sha256':{'english':hashlib.sha256((ROOT/'banglabbq_health_status_english.jsonl').read_bytes()).hexdigest(),'bengali':hashlib.sha256((ROOT/'banglabbq_health_status_bengali.jsonl').read_bytes()).hexdigest()}
}
out=ROOT/'health_status_audited_expansion_manifest.json'
out.write_text(json.dumps(audited,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('candidate manifest',out,'variations',len(audited['variations']),'bytes',out.stat().st_size)
