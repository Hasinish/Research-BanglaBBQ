#!/usr/bin/env python3
"""Read-only import preflight using verified live metadata snapshot and candidate JSONLs.
Never connects to or modifies Sheets or GitHub.
"""
import collections,json,re
from pathlib import Path
R=Path('/mnt/data')
LANGS={l:[json.loads(s) for s in (R/f'health_status_audited_{l}.jsonl').open()] for l in ('english','bengali')}
keys=['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id']
future=[]
for lang,rows in LANGS.items():
 for obj in rows:
  row=[]
  for k in keys:
   v=obj[k];row.append(json.dumps(v,ensure_ascii=False,separators=(',',':')) if k in ('answer_info','additional_metadata') else str(v) if k not in ('context','question','ans0','ans1','ans2') else v)
  future.append(row)
first=next(x for x in future if x[0]=='0')
inj=[]
for j,row in enumerate(future):
 for k,value in enumerate(row):
  if isinstance(value,str) and value.lstrip().startswith(('=','+','@')):inj.append((j,k,value[:50]))
notes={'original_main_commit':'e186b283fa5b184058e2cb395273e9968a893b20','evaluated_candidate_sha256':{},'category':'Health_status','current_workbook':'https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit','audited_date':'2026-10-26','spreadsheet_existing_health_tabs':'NONE; all 10 active original production tabs checked by read-only metadata','import_status':'NOT_IMPORTED','import_safe':'NO',
 'reason':'Q04 unsupported health-only theme, Q02/Q07/Q08/Q09 partial evidence/clinical or appearance confounds, no actual independent human review, unapproved provisional IDs, duplicated scenario family, no active Health tabs.',
 'provisional_id_range':'8300000..8301439','id_collision_check':'All six other new English JSONLs exact IDs nonoverlapping; 10 active ENG/BEN production Sheet O columns searched for 8300, only unrelated Gender 8300, zero current detected collision. Not a final exhaustive global row-by-row collision proof.',
 'rows_per_language':{x:len(v) for x,v in LANGS.items()},'prospective_data_rows':len(future),'prospective_cells':len(future)*len(keys),'expected_tabs':2,'expected_sheet_range_if_approved':'A1:O1441 per language including header',
 'sheet_header_order':keys,'jsonl_key_order':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
 'json_metadata_cells_stringified':all(first[k].startswith('{') for k in [11,12]),'formula_injection_cell_count':len(inj),'formula_injection_examples':inj[:5],
 'pending_checks':['Independent Bangladeshi Bengali human clinical/cultural editorial signoff','Q04 source replacement or theme removal and reviewed downstream row count','Q02/Q07/Q08/Q09 source scenario alignment','Escalated clinician confirmation of no legitimately necessary contact precautions','Final global id-collision recheck immediately before any approved import','Design-family holdout split and cross-category duplicate review','New live Health tabs creation and post-import row-level verification only after explicit authorization'],
 'write_access_invoked':'NO'}
import hashlib
for lang in LANGS:notes['evaluated_candidate_sha256'][lang]=hashlib.sha256((R/f'health_status_audited_{lang}.jsonl').read_bytes()).hexdigest()
(R/'health_status_import_readiness.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'import_safe':notes['import_safe'],'prospective_rows':len(future),'cells':len(future)*len(keys),'formula_injections':len(inj),'no_live_health_tab':True},indent=2))
