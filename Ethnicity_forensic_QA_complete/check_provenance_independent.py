#!/usr/bin/env python3
"""Check original and candidate source strings against independently web-verified URL table.
No code from generator is imported and there are no network writes.
"""
from pathlib import Path
import csv,json,hashlib,collections
R=Path(__file__).resolve().parent
with (R/'Ethnicity_source_evidence_matrix.csv').open(encoding='utf-8',newline='') as f:
 urls={row['theme']:row['source_1_url'] for row in csv.DictReader(f)}
assert len(urls)==10
stats={}
for version in ('ORIGINAL','audited'):
 for lang in ('english','bengali'):
  f=(R/'ORIGINAL'/f'banglabbq_ethnicity_{lang}.jsonl') if version=='ORIGINAL' else R/f'banglabbq_ethnicity_audited_{lang}.jsonl'
  good=bad=0;examples=[];cc=collections.Counter()
  with f.open(encoding='utf-8') as stream:
   for lineidx,line in enumerate(stream):
    row=json.loads(line);q=f'Q{int(row["question_index"]):02d}';observed=row['additional_metadata']['source'];expected=urls[q]
    cc[q]+=1
    if observed==expected:good+=1
    else:bad+=1;examples.append({'eid':row['example_id'],'observed':observed,'expected':expected})
  stats[f'{version}_{lang}']={'checked':good+bad,'matching_independently_opened_primary_URL':good,'mismatches':bad,'per_theme_records':dict(cc),'file_SHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'examples':examples[:10]}
  assert bad==0 and good==1440 and sorted(cc.values())==[144]*10
R.joinpath('Ethnicity_independent_provenance_crosscheck.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{x:v for x,v in val.items() if x in ('checked','matching_independently_opened_primary_URL','mismatches')} for k,val in stats.items()},ensure_ascii=False,indent=2))
