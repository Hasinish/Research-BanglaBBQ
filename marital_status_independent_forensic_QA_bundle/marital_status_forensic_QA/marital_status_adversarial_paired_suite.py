#!/usr/bin/env python3
"""Paired and label-balanced deliberate defects; tests actual semantic gaps beyond EN/BN parity checks."""
import copy,csv,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE))
import marital_status_adversarial_suite as s

def mutate(fx,r):
 en,bn=r['en'],r['bn']; ix=s.ix
 if fx==32:
  i=ix(1,1,0,0,1); j=next(k for k in range(ix(1,1),ix(1,2)) if en[k]['context_condition']=='disambig' and en[k]['label']==1)
  assert en[i]['label']==0 and en[j]['label']==1
  for a in (en,bn):a[i]['label'],a[j]['label']=a[j]['label'],a[i]['label']
 elif fx==33:
  i,j=ix(1,1),ix(1,4)
  for a in (en,bn):a[i]['additional_metadata']['source'],a[j]['additional_metadata']['source']=a[j]['additional_metadata']['source'],a[i]['additional_metadata']['source']
 elif fx==34:
  i=ix(1,1,0,0,1)
  en[i]['context']=en[i]['context'].replace('rejects Nasima for the flat and offers it to Rupa','rejects Rupa for the flat and offers it to Nasima')
  bn[i]['context']=bn[i]['context'].replace('নাসিমার আবেদন নাকচ করেন এবং রূপাকে','রূপার আবেদন নাকচ করেন এবং নাসিমাকে')
 elif fx==35:
  for k in range(ix(1,1),ix(1,2)):
   en[k]['context']=en[k]['context'].replace('two 31-year-old employed women','a 31-year-old man and a 31-year-old employed woman')
   bn[k]['context']=bn[k]['context'].replace('দুজনই ৩১ বছর বয়সী কর্মজীবী নারী','নাসিমা ৩১ বছরের পুরুষ এবং রূপা ৩১ বছরের কর্মজীবী নারী')
 elif fx==36:
  i=ix(1,8,0,0,3)
  en[i]['question']='Who was praised for planning the wedding?'
  bn[i]['question']='বিয়ের পরিকল্পনার জন্য কাকে প্রশংসা করা হয়েছিল?'
 elif fx==37:
  for k in range(ix(1,1),ix(1,2)):
   en[k]['context']=en[k]['context']+' Nasima has a criminal conviction, while Rupa does not.'
   bn[k]['context']=bn[k]['context']+' নাসিমার অপরাধের সাজা আছে, কিন্তু রূপার নেই।'
 elif fx==38:
  for k in range(ix(3,2),ix(3,3)):
   if en[k]['context_condition']=='disambig':
    en[k]['context']=en[k]['context'].replace('8 p.m.','3 p.m.')
 elif fx==39:
  for k in range(ix(1,1),ix(1,2)):
   en[k]['context']=en[k]['context']+' Nasima earns twice as much as Rupa, despite the matched-income statement.'
   bn[k]['context']=bn[k]['context']+' আয় সমান বলা হলেও নাসিমার আয় রূপার দ্বিগুণ।'
 else:raise ValueError(fx)

def expert(fx,r):
 en,bn=r['en'],r['bn'];ix=s.ix
 if fx==35:return ('a 31-year-old man and' in en[ix(1,1)]['context'] and 'পুরুষ' in bn[ix(1,1)]['context']),'Gender confound directly violates same-gender marital-status comparison despite paired text.'
 if fx==36:return ('praised for planning' in en[ix(1,8,0,0,3)]['question'] and 'prais' not in en[ix(1,8,0,0,3)]['context']),'No explicit praise or wedding-planning act; entailment missing despite correct identity position.'
 if fx==37:return ('criminal conviction' in en[ix(1,1)]['context'] and 'equal income' in en[ix(1,1)]['context']),'Irrelevant invented criminal background creates material tenant-risk confound not sourced.'
 if fx==38:return ('3 p.m.' in en[ix(3,2,0,0,1)]['context'] and 'রাত আটটার' in bn[ix(3,2,0,0,1)]['context']),'Numeric time mismatch 3 p.m. vs 8 p.m. in EN and BN.'
 if fx==39:return ('earns twice as much' in en[ix(1,1)]['context'] and 'equal income' in en[ix(1,1)]['context']),'Contradiction: narrative asserts both matched and unequal incomes, inducing class confound.'
 return False,''
D={32:'swap two disambig labels 0 and 1 in BOTH languages while preserving global balance',33:'swap valid HTTPS source URLs between Q01 and Q04 in BOTH languages',34:'reverse the adverse/favorable actors in the disambiguated context BOTH languages but leave gold unchanged',35:'make two tenant candidates different genders in BOTH languages, same counterfactual text',36:'replace welcome question with unentailed praise in BOTH languages',37:'add asymmetric criminal conviction qualification across BOTH orientations and languages',38:'change EN curfew 8 p.m. to 3 p.m. in both orientations, retain BN 8 p.m.',39:'add contradictory twice-income wealth confound consistently in BOTH orientations and languages'}

def main():
 file=BASE/'marital_status_adversarial_results.json'
 data=json.loads(file.read_text('utf8'));out=data['fixtures'];t=BASE/'work'/'paired_mutants_tmp';t.mkdir(exist_ok=True)
 for fx in D:
  rows={'en':copy.deepcopy(s.E),'bn':copy.deepcopy(s.B)};mutate(fx,rows)
  for lang in ('en','bn'):
   with (t/(lang+'.jsonl')).open('w',encoding='utf8',newline='\n') as f:
    for r in rows[lang]:f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
  try:
   x=s.generator.check(s.manifest,rows,s.audit,s.cross);orig=bool(x['failures']);orig_count=len(x['failures']);orig_ex=x['failures'][:5]
  except Exception as e:orig=True;orig_count=1;orig_ex=[type(e).__name__+':'+str(e)]
  try:
   z=s.independent(str(t/'en.jsonl'),str(t/'bn.jsonl'),s.manifest);ind=bool(z['row_failures']);ind_count=len(z['row_failures']);ind_ids=sorted({a['test_id'] for a in z['row_failures']})[:12]
  except Exception as e:ind=True;ind_count=1;ind_ids=[type(e).__name__+':'+str(e)]
  exp,reason=expert(fx,rows)
  out.append(dict(fixture_id=f'FX{fx}',mutation=D[fx],category='Marital_status',inj_target='paired / balanced temporary copies',expected_detection='MUST_DETECT',legacy_generator_detected=orig,legacy_generator_failure_count=orig_count,legacy_generator_failure_examples=orig_ex,independent_validator_detected=ind,independent_validator_failure_count=ind_count,independent_validator_codes=ind_ids,AI_expert_probe_detected=exp,AI_expert_probe_explanation=reason,combined_detected=ind or exp,validator_loophole=not ind,verdict=('INDEPENDENT_CODE_DETECTED' if ind else ('AI_EXPERT_TARGETED_PROBE_ONLY' if exp else 'UNDETECTED_LIMITATION'))))
  print(f'FX{fx}: original={orig}, independent={ind}, AI_expert={exp}')
 data['executed_fixture_count']=len(out)
 data['aggregate_detection']={k:sum(bool(z[k]) for z in out) for k in ['legacy_generator_detected','independent_validator_detected','AI_expert_probe_detected','combined_detected']}
 data['legacy_false_negatives']=sum(not z['legacy_generator_detected'] for z in out)
 data['independent_automated_false_negatives']=sum(not z['independent_validator_detected'] for z in out)
 data['combined_undetected']=sum(not z['combined_detected'] for z in out)
 file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('FINAL',json.dumps({k:v for k,v in data.items() if k in ['executed_fixture_count','aggregate_detection','legacy_false_negatives','independent_automated_false_negatives','combined_undetected']}))
 for x in t.glob('*'):x.unlink()
 t.rmdir()
if __name__=='__main__':main()
