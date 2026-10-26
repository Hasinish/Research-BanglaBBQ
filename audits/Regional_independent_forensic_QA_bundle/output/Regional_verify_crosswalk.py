#!/usr/bin/env python3
"""Checks current upstream PakBBQ Regional theme tallies against captured crosswalk.
The upstream counts were retrieved from the current main GitHub JSONL on 2026-10-26;
no network access or modification is made here.
"""
import csv,json,pathlib,collections
ROOT=pathlib.Path('/mnt/data/regional_forensic')
BASE=ROOT/'original';OUT=ROOT/'output'
expected=[80,64,64,64,64,64,16,16,64,48,64,80,80,32,32,32,32,48]
assert sum(expected)==944
rows=list(csv.DictReader((BASE/'banglabbq_regional_pakbbq_theme_crosswalk.csv').open(encoding='utf8')))
a=[r for r in rows if r['upstream_index'].isdigit()];b=[r for r in rows if not r['upstream_index'].isdigit()]
result=[]
for i,r in enumerate(a):
 k=i+1;source=int(r['upstream_record_count']);match=(r['upstream_index']==str(k) and source==expected[i])
 result.append({'index':k,'current_upstream_main':'c079dbae2d676f4e3bb82982144d6d4ac10436d4','upstream_path':r['upstream_dataset_path'],'verified_record_count':expected[i],'crosswalk_count':source,'record_count_matches':match,'reported_decision':r['decision'],'reported_BD_mapping':r['mapping_to_banglabbq_theme'],'scientific_verdict':'PROVISIONAL_STRUCTURE_ONLY_BD_MEDIA_HIRING_EVIDENCE_PARTIAL' if k==1 else ('NO_BANGLADESH_EVIDENCE_IMPORTED' if r['decision'] in ('REJECT','NOT_RELEVANT') else 'REPLACED_WITH_INDEPENDENT_BANGLADESH_THEME'),'caution':'PakBBQ group ethnic/regional confounds are methodology, never evidence of Bangladeshi stereotype'})
assert len(a)==18 and len(b)==10 and sum(x['record_count_matches'] for x in result)==18
with (OUT/'Regional_pakbbq_crosswalk_verification.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
(OUT/'Regional_pakbbq_crosswalk_verification.json').write_text(json.dumps({'main_sha':'c079dbae2d676f4e3bb82982144d6d4ac10436d4','official_upstream_path':'PakBBQ/PakBBQ_ENG/Regional.jsonl','blob_sha':'c6d0a7a1b1ed9370eba23a2ec4c52369968fab87','upstream_total_records':944,'upstream_theme_count':18,'matched_upstream_counts':18,'crosswalk_proposed_new_themes':len(b),'regional_Q08_adaptation':'STRUCTURAL_ONLY; Bangladesh-specific broadcaster hiring not proven','all_rows':result},indent=2)+'\n')
print('18/18 upstream theme counts matched; 944 records total; 10 new/theme decisions present')
