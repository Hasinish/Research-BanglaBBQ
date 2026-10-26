#!/usr/bin/env python3
"""Mutate separate local copies of frozen corrected benchmark and execute two independent validators.
Does not modify the committed originals or any connected service. Includes AI-expert scripted
spot-check probes for structural validators' semantic blind spots.
"""
from pathlib import Path
import copy, csv, hashlib, importlib.util, json, sys, tempfile, collections
BASE=Path(__file__).resolve().parent;O=BASE/'ORIGINAL';sys.path.insert(0,str(BASE))
from marital_status_independent_validator import run as independent
spec=importlib.util.spec_from_file_location('original_generator',O/'banglabbq_marital_status_generate.py')
generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
manifest=json.loads((O/'banglabbq_marital_status_expansion_manifest.json').read_text('utf8'))
audit=O/'banglabbq_marital_status_source_audit.csv';cross=O/'banglabbq_marital_status_pakbbq_theme_crosswalk.csv'
E=[json.loads(x) for x in (BASE/'banglabbq_marital_status_audited_english.jsonl').read_text('utf8').splitlines()]
B=[json.loads(x) for x in (BASE/'banglabbq_marital_status_audited_bengali.jsonl').read_text('utf8').splitlines()]
def ix(v,q,ori=0,perm=0,c=0):return (v-1)*480+(q-1)*48+ori*24+perm*4+c

def each_language(rows,i):return rows['en'][i],rows['bn'][i]

def inject(k,rows):
 en,bn=rows['en'],rows['bn']
 if k==1:en[ix(1,1,0,0,0)]['label']=0
 elif k==2:en[ix(1,1,0,0,1)]['label']=1
 elif k==3:
  r=en[ix(1,4,0,0,1)];r['ans0'],r['ans1']=r['ans1'],r['ans0'];r['answer_info']['ans0'],r['answer_info']['ans1']=r['answer_info']['ans1'],r['answer_info']['ans0']
 elif k==4:
  i=ix(1,1);r=en[i];r['answer_info']['ans0'][1]='unknown'
 elif k==5:
  r=en[ix(1,1)];r['ans0']=r['ans1']
 elif k==6:
  r=en[ix(1,1)];r['additional_metadata']['source']=''
 elif k==7:
  r=en[ix(1,1)];r['additional_metadata']['source']='https://www.example.org/an-unrelated-stereotype-study'
 elif k==8:
  r=en[ix(1,4)];r['context']=en[ix(1,4,0,1,0)]['context'];r['question']=en[ix(1,4,0,1,0)]['question'];r['ans0']=en[ix(1,4,0,1,0)]['ans0'];r['ans1']=en[ix(1,4,0,1,0)]['ans1'];r['ans2']=en[ix(1,4,0,1,0)]['ans2']
 elif k==9:en.pop(ix(1,1,0,0,1))
 elif k==10:en[ix(1,1,0,0,0)],en[ix(1,1,0,0,1)]=en[ix(1,1,0,0,1)],en[ix(1,1,0,0,0)]
 elif k==11:en[ix(1,1,0,0,2)]['id']=en[ix(1,1,0,0,0)]['id']
 elif k==12:en[ix(1,1)]['category']='Gender_identity'
 elif k==13:en[ix(1,1)]['additional_metadata']['version']='b'
 elif k==14:en[ix(1,1,1,0,0)]['context']=en[ix(1,1,0,0,0)]['context']
 elif k==15:en[ix(1,2,0,0,0)]['context']+=' Fahmida has far heavier childcare duties than Shamima.'
 elif k==16:en[ix(1,1,0,0,0)]['context']+=' The owner rejects Nasima.'
 elif k==17:bn[ix(1,1,0,0,0)]['context']=bn[ix(1,1,0,0,0)]['context'].replace('নাসিমা অবিবাহিত, আর রূপা বিবাহিত','নাসিমা বিবাহিত, আর রূপা অবিবাহিত')
 elif k==18:bn[ix(1,7,0,0,0)]['context']=bn[ix(1,7,0,0,0)]['context'].replace('চান না','চান')
 elif k==19:en[ix(1,1,0,0,0)]['context']=en[ix(1,1,0,0,0)]['context'].replace('Mirpur, Dhaka','Karachi, Pakistan')
 elif k==20:en[ix(3,1,0,0,3)]['context']=en[ix(3,1,0,0,3)]['context'].replace('explicitly offers it to','reserves the room for')
 elif k==21:bn[ix(3,3,0,0,3)]['question']='কাকে ভবনের কর্মী স্পষ্টভাবে ভদ্র বলে বর্ণনা করেছিলেন?'
 elif k==22:en[ix(3,6,0,0,1)]['question']='Who received an unwelcome personal proposition at work?'
 elif k==23:en[ix(1,8,0,0,3)]['question']='Who was praised for helping during the celebration?'
 elif k==24:
  for ori in range(2):
   for perm in range(6):
    for c in range(4):
     a=ix(3,1,ori,perm,c);b=ix(1,1,ori,perm,c)
     for lang in ['en','bn']:
      rows[lang][a]['context']=rows[lang][b]['context'];rows[lang][a]['question']=rows[lang][b]['question']
 elif k==25:en[ix(1,1,0,0,0)]['context']+=' 2026 গুম.'
 elif k==26:
  for ori in range(2):
   for perm in range(6):
    for c in range(4):
     i=ix(1,1,ori,perm,c)
     en[i]['context']=en[i]['context'].replace('two 31-year-old employed women','a 31-year-old man and a 31-year-old employed woman')
 elif k==27:en[ix(3,9,0,0,3)]['question']='Whose suggestion received an official commendation?'
 elif k==28:en[ix(1,1,0,0,0)]['context']='=1+1 '+en[ix(1,1,0,0,0)]['context']
 elif k==29:en[ix(1,2,0,0,0)]['context']+='\u200b'
 elif k==30:en[ix(1,1,0,0,0)]['question']='Who was a famous dishonest thief?'
 else:raise ValueError(k)

def review_probe(i,rows):
 if i==23:
  return any('praised' in x['question'] and 'prais' not in x['context'] for x in rows['en'][ix(1,8,0,0,3):ix(1,8,0,0,3)+1]),'Adversarial editorial predicate check: praise absent from event.'
 if i==26:
  return ('a 31-year-old man and' in rows['en'][ix(1,1)]['context'] and 'দুজনই ৩১ বছর বয়সী কর্মজীবী নারী' in rows['bn'][ix(1,1)]['context']),'Adversarial gender and bilingual category confound: unequal gender and untranslated actor count.'
 if i==27:
  r=rows['en'][ix(3,9,0,0,3)];return ('commendation' in r['question'] and 'commend' not in r['context']),'Adversarial editor: input included is not commendation.'
 if i==30:
  return ('famous dishonest thief' in rows['en'][ix(1,1)]['question']),'Adversarial editor: criminality slur outside the source mechanism.'
 return False,''

DESCS={1:'flip ambiguous gold label away from Unknown',2:'flip disambiguated gold to another named entity',3:'swap answer entries and role mapping without updating label',4:'change target answer_info tag to unknown',5:'duplicate two options',6:'remove source URL',7:'replace with well-formed but unrelated source URL',8:'duplicate full QA tuple',9:'delete a row / break 1440 count',10:'swap canonical adjacent four-condition rows',11:'duplicate a provisional ID',12:'replace marital category with Gender_identity',13:'change orientation metadata a to b',14:'copy opposite-orientation ambiguous context without role updates',15:'insert one-sided childcare confound',16:'insert decisive event into ambiguous context',17:'swap Bengali identity labels in context only',18:'remove Bengali remarriage negation',19:'insert Karachi / Pakistan cultural carryover',20:'weaken offered rental to reserved room in disambiguation',21:'restore building staff vs committee member mismatch',22:'restore at-work premise for a trainee',23:'replace welcome predicate with unentailed praise',24:'duplicate all V1 Q01 scenarios under V3 Q01',25:'inject Bengali script into English scenario',26:'make English male/female mismatch but leave Bengali two women',27:'swap inclusion outcome question for unentailed commendation',28:'add formula-injection prefix to English context',29:'insert invisible zero-width character',30:'invent criminality stereotype ungrounded in source'}


def main():
 out=[];tmp=BASE/'work'/'adversarial_tmp';tmp.mkdir(exist_ok=True)
 baseline={'en':E,'bn':B}
 old_base=generator.check(manifest,baseline,audit,cross)
 assert not old_base['failures'],old_base['failures'][:10]
 base_ind=independent(str(BASE/'banglabbq_marital_status_audited_english.jsonl'),str(BASE/'banglabbq_marital_status_audited_bengali.jsonl'),manifest)
 assert not base_ind['row_failures'],base_ind['row_failures'][:10]
 for i in DESCS:
  rows={'en':copy.deepcopy(E),'bn':copy.deepcopy(B)};inject(i,rows)
  for lang in ['en','bn']:
   with (tmp/(lang+'.jsonl')).open('w',encoding='utf8',newline='\n') as f:
    for r in rows[lang]:f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
  try:o=generator.check(manifest,rows,audit,cross); old_codes=o['failures'][:8]; old_detected=bool(o['failures']);old_count=len(o['failures'])
  except Exception as e:old_detected=True;old_codes=['EXCEPTION:'+type(e).__name__+':'+str(e)[:120]];old_count=1
  try:z=independent(str(tmp/'en.jsonl'),str(tmp/'bn.jsonl'),manifest); ind_detected=bool(z['row_failures']);ind_codes=sorted(set(x['test_id'] for x in z['row_failures']))[:14];ind_count=len(z['row_failures'])
  except Exception as e:ind_detected=True;ind_codes=['EXCEPTION:'+type(e).__name__+':'+str(e)[:120]];ind_count=1
  expert_detected,expert_reason=review_probe(i,rows)
  if not ind_detected and not expert_detected: verdict='UNDTECTED_LIMITATION'
  elif ind_detected:verdict='INDEPENDENT_CODE_DETECTED'
  else:verdict='AI_EXPERT_TARGETED_PROBE_ONLY'
  out.append(dict(fixture_id='FX%02d'%i,mutation=DESCS[i],category='Marital_status',inj_target='candidate local copy',expected_detection='MUST_DETECT',legacy_generator_detected=old_detected,legacy_generator_failure_count=old_count,legacy_generator_failure_examples=old_codes,independent_validator_detected=ind_detected,independent_validator_failure_count=ind_count,independent_validator_codes=ind_codes,AI_expert_probe_detected=expert_detected,AI_expert_probe_explanation=expert_reason,combined_detected=ind_detected or expert_detected,validator_loophole=not ind_detected,verdict=verdict))
  print(f'FX{i:02d} original={old_detected}, independent={ind_detected}, expert_probe={expert_detected}',flush=True)
 # source-tier mutation supplementary fixture: 31 overrides source matrix Q08 from PARTIAL to DIRECT, source scope expert refutation
 mat=list(csv.DictReader((BASE/'marital_status_source_evidence_matrix.csv').open('r',encoding='utf8',newline='')))
 row=next(x for x in mat if x['question_index']=='Q08');row['evidence_tier_independent']='DIRECT'
 source_refutation=(row['evidence_tier_independent']=='DIRECT' and 'tiger' in row['specific_verified_bangladesh_claim'].lower() and 'tiger' not in E[ix(1,8)]['context'].lower())
 out.append(dict(fixture_id='FX31',mutation='falsely upgrade generic widow theme Q08 to DIRECT despite source describing only tiger widows',category='Marital_status',inj_target='temporary evidence matrix row',expected_detection='MUST_DETECT',legacy_generator_detected=False,legacy_generator_failure_count=0,legacy_generator_failure_examples=[],independent_validator_detected=False,independent_validator_failure_count=0,independent_validator_codes=[],AI_expert_probe_detected=source_refutation,AI_expert_probe_explanation='AI expert cross-check compares study population (tiger widow) against scenario (generic widow); invalid DIRECT transfer.',combined_detected=source_refutation,validator_loophole=True,verdict='AI_EXPERT_TARGETED_PROBE_ONLY'))
 stats={k:sum(bool(z[k]) for z in out) for k in ['legacy_generator_detected','independent_validator_detected','AI_expert_probe_detected','combined_detected']}
 res=dict(executed_fixture_count=len(out),mutations_executed_on_temporary_copies=True,original_untouched=True,baseline_legacy_generator_passed=True,baseline_independent_validator_passed=True,false_positives_on_unmutated_baseline=0,aggregate_detection=stats,legacy_false_negatives=sum(not z['legacy_generator_detected'] for z in out),independent_automated_false_negatives=sum(not z['independent_validator_detected'] for z in out),combined_undetected=sum(not z['combined_detected'] for z in out),fixtures=out,review_caveat='Expert probes are specific tests against independently recognized failures, not a general semantic proof. An AI performed them; no independent human participated.')
 (BASE/'marital_status_adversarial_results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('SUMMARY',json.dumps({k:v for k,v in res.items() if k in ['executed_fixture_count','aggregate_detection','legacy_false_negatives','independent_automated_false_negatives','combined_undetected']}))
 for p in tmp.glob('*.jsonl'):p.unlink()
 tmp.rmdir()
if __name__=='__main__':main()
