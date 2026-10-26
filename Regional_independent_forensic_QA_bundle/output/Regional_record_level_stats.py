#!/usr/bin/env python3
import csv,collections,itertools,json,pathlib,hashlib
ROOT=pathlib.Path('/mnt/data/regional_forensic');O=ROOT/'original';D=ROOT/'output'
res={'category':'Regional','script':'Regional_record_level_stats.py','languages':{},'original_vs_audited_non_text_changes':[]}
for lang,short in [('english','en'),('bengali','bn')]:
 old=[json.loads(s) for s in (O/f'banglabbq_regional_{lang}.jsonl').read_text(encoding='utf-8').splitlines()]
 new=[json.loads(s) for s in (D/f'banglabbq_regional_audited_{lang}.jsonl').read_text(encoding='utf-8').splitlines()]
 s={'count':len(old),'themes':dict(collections.Counter('Q'+str(r['question_index']).zfill(2) for r in old)),'conditions':{f'{k[0]}_{k[1]}':v for k,v in collections.Counter((r['context_condition'],r['question_polarity']) for r in old).items()},'orientations':dict(collections.Counter(r['additional_metadata']['version'] for r in old)),'labels':dict(sorted(collections.Counter(r['label'] for r in old).items())),'answer_tag_sets':[{'roles':list(k),'count':v} for k,v in collections.Counter(tuple(sorted(r['answer_info']['ans'+str(i)][1] for i in range(3))) for r in old).items()],'id_min':min(r['id'] for r in old),'id_max':max(r['id'] for r in old),'formula_injection_prefix_count':0,'zero_width_or_BOM_rows':0,'nonempty_valid_urls':0,'permutation_subblock_errors':0,'other_fields_changed':0,'text_fields_changed':0,'full_qa_duplicates':0}
 triples=set();dims={}
 for i,(a,b) in enumerate(zip(old,new)):
  for k in a:
   if a[k]!=b[k]:
    if k not in ('context','question'):
     s['other_fields_changed']+=1;res['original_vs_audited_non_text_changes'].append((lang,i,k))
    else:s['text_fields_changed']+=1
  for fld in ('context','question','ans0','ans1','ans2'):
   text=a[fld];
   if text.lstrip().startswith(('=','+','-','@')):s['formula_injection_prefix_count']+=1
   if any(c in text for c in ('\ufeff','\u200b','\u200c','\u200d','\u2060')):s['zero_width_or_BOM_rows']+=1
  if a['additional_metadata']['source'].startswith('https://'):s['nonempty_valid_urls']+=1
  key=(a['context'],a['question'],a['ans0'],a['ans1'],a['ans2'])
  if key in triples:s['full_qa_duplicates']+=1
  triples.add(key)
 for wave in range(3):
  for theme in range(10):
   block=old[wave*480+theme*48:wave*480+theme*48+48]
   if len(block)!=48:s['permutation_subblock_errors']+=1;continue
   for ori in (0,1):
    rows=block[ori*24:(ori+1)*24];got=set()
    for p in range(6):
     quartet=rows[p*4:p*4+4]
     x=quartet[0]
     roles=tuple(x['answer_info'][f'ans{j}'][1] for j in range(3))
     got.add(roles)
     if len(quartet)!=4 or any(tuple(z['answer_info'][f'ans{j}'][1] for j in range(3))!=roles for z in quartet):s['permutation_subblock_errors']+=1
     if [(z['context_condition'],z['question_polarity']) for z in quartet]!=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]:s['permutation_subblock_errors']+=1
    if len(got)!=6:s['permutation_subblock_errors']+=1
 res['languages'][lang]=s
assert not res['original_vs_audited_non_text_changes']
(D/'Regional_record_level_statistics.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:{q:v for q,v in z.items() if q!='answer_tag_sets'} for k,z in res['languages'].items()},indent=2))
