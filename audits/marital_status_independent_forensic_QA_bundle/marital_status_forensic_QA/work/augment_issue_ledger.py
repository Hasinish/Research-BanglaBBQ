import csv,json,collections
from pathlib import Path
P=Path('/mnt/data/marital_forensic_qa');O=P/'ORIGINAL';path=P/'marital_status_issue_ledger.csv'
E=[json.loads(z) for z in (O/'banglabbq_marital_status_english.jsonl').read_text('utf8').splitlines()]
B=[json.loads(z) for z in (O/'banglabbq_marital_status_bengali.jsonl').read_text('utf8').splitlines()]
with path.open(encoding='utf8',newline='') as f:r=csv.DictReader(f);cols=r.fieldnames;existing=list(r)
NEW=[]
def add(t,lang,issue,sev,field,old,problem,fix,status='BLOCKED_FOR_EXPERT_DECISION',scope='SYSTEMIC_ROW',url=''):
 i=t['example_id'];NEW.append(dict(issue_id=issue,severity=sev,category='Marital_status',source_commit_sha='e186b283fa5b184058e2cb395273e9968a893b20',language=lang,line_number=i+1,example_id=i,id=t['id'],question_index=t['question_index'],variation='V'+str(i//480+1),orientation=t['additional_metadata']['version'],context_condition=t['context_condition'],question_polarity=t['question_polarity'],offending_field=field,original_value=old,revised_value='',exact_diagnosis=problem,evidence_url=url,proposed_fix=fix,confidence='HIGH',status=status,issue_cluster=issue,row_level_or_systemic=scope))
for lang,rows in [('en',E),('bn',B)]:
 for x in rows:
  q=int(x['question_index']);v=x['example_id']//480+1
  if q==10:
   add(x,lang,'M-CONSTRUCT-Q10','P1','theme title and context','job refusal justified by widowhood superstition','All Q10 variations show workplace acceptance/refusal but do not specify the superstition as the evaluator motive; construct title overclaims what answer entails.','Do not infer motive; obtain source-backed legal/cultural clarification and author evidence-proportional question or relabel theme with expert approval.',url='https://www.nature.com/articles/s41599-025-05988-1')
  if q==2:
   add(x,lang,'M-WORDING-Q02','P2','question.nonneg',x['question'] if x['question_polarity']=='nonneg' else '', 'Generic contrast Who was allowed to follow only the standard rules is somewhat artificial. Exact rooftop/visitor/curfew action differs by variant.', 'After external approval, tighten English and Bengali nonnegative wording to the exact standard-rule permission per variant, preserving paired labels; avoid removing valid ambiguous choice.')
  if (x['example_id']%24)==0:
   add(x,lang,'M-COVERAGE-GENDER','P2','scope / demographic sampling','both candidates women','All 10 themes compare women only (unmarried, divorced, widowed, married). Findings do not generalize to unmarried/divorced/widowed men or separated/remarried people.','Treat as explicit population scope; expand later only with independent source-supported mixed-gender samples, not via assumption.',scope='REPRESENTATIVE_OF_24_PERMUTATION_ROWS')
# candidate JSONL repaired but original generator would regress when run without the patch
add(E[961],'en','M-REPRO-PATCH_REQUIRED','P1','manifest scenario templates','original frozen generator template Q01-V3 lacks offer entailment','Original manifest/generator regenerate committed UNREPAIRED files; import must use the separate deterministic local patch script, not generator alone.', 'Keep original reproducible, but version a revised manifest and generator branch only AFTER expert approval; document apply_local_repairs.py as mandatory.',scope='REPRO_INTEGRATION_EXEMPLAR')
with path.open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(existing);w.writerows(NEW)
print(json.dumps({'existing':len(existing),'added':len(NEW),'overall':len(existing)+len(NEW),'severities':dict(collections.Counter(v['severity'] for v in existing+NEW)),'unique_clusters':{k:len({z['issue_id'] for z in existing+NEW if z['severity']==k}) for k in 'P0 P1 P2 P3'.split()}},indent=2))
