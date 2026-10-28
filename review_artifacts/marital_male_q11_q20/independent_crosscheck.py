#!/usr/bin/env python3
"""Independent row-based crosscheck with no generator/specification imports."""
import json,re,collections,sys
from pathlib import Path
root=Path(__file__).resolve().parent
names=('BanglaBBQ_Marital_Male_Q11_Q20_english.jsonl','BanglaBBQ_Marital_Male_Q11_Q20_bengali.jsonl')
rows=[[json.loads(line) for line in (root/n).open(encoding='utf-8')] for n in names]
issues=[];checked=0
for lang,rs in zip(('ENG','BEN'),rows):
  for i,r in enumerate(rs):
    if not isinstance(r['question_index'],str):issues.append(f'{lang} id {r["example_id"]} nonstring question index')
    if r['ans0']==r['ans1'] or r['ans1']==r['ans2'] or r['ans0']==r['ans2']:issues.append(f'{lang} id {r["example_id"]} duplicate answer options')
    if r['answer_info'][f'ans{r["label"]}'][0]!=r[f'ans{r["label"]}']:issues.append(f'{lang} id {r["example_id"]} bad gold info mapping')
    if r['context_condition']=='ambig':
      if r[f'ans{r["label"]}']!=('Unknown' if lang=='ENG' else '\u0985\u099c\u09be\u09a8\u09be'):issues.append(f'{lang} id {r["example_id"]} failed ambig unknown')
    else:
      if r[f'ans{r["label"]}']==('Unknown' if lang=='ENG' else '\u0985\u099c\u09be\u09a8\u09be'):issues.append(f'{lang} id {r["example_id"]} disambig unknown')
    if lang=='BEN':
      for candidate in [r['ans0'],r['ans1'],r['ans2']]:
        if candidate!='\u0985\u099c\u09be\u09a8\u09be' and candidate+'\u098f\u09b0' in r['context']:
          issues.append(f'BN name+er incorrect at example_id={r["example_id"]}')
  for v in (1,2,3):
    for q in range(11,21):
      st=1440+(v-1)*480+(q-11)*48-1440
      block=rs[st:st+48]
      if len(block)!=48:issues.append(f'{lang} q{q}v{v} wrong block count');continue
      if len({r['question'] for r in block})!=30//30+1:issues.append(f'{lang} q{q}v{v} no binary question pair')
      if len({r['context'] for r in block})!=4:issues.append(f'{lang} q{q}v{v} context should be 4 unique (a/b x ambig/disambig)')
      for o in ('a','b'):
        orientation=[r for r in block if r['additional_metadata']['version']==o]
        negs=[r for r in orientation if r['context_condition']=='disambig' and r['question_polarity']=='neg']
        pos=[r for r in orientation if r['context_condition']=='disambig' and r['question_polarity']=='nonneg']
        for rn,rp in zip(negs,pos):
          if rn['context']!=rp['context']:issues.append(f'{lang} q{q}v{v} changed evidence between neg and nonneg')
          if rn[f'ans{rn["label"]}']==rp[f'ans{rp["label"]}']:issues.append(f'{lang} q{q}v{v} same person both polarities')
        a=orientation[0]; d=orientation[1]
        if not d['context'].startswith(a['context']+' '):issues.append(f'{lang} q{q}v{v} {o} disambig does not extend ambiguous')
        tail=d['context'][len(a['context'])+1:]
        option_people=[z for z in [a['ans0'],a['ans1'],a['ans2']] if z!=('Unknown' if lang=='ENG' else '\u0985\u099c\u09be\u09a8\u09be')]
        if any(p not in tail for p in option_people):issues.append(f'{lang} q{q}v{v} {o} missing one decision recipient')
        checked+=8
      for x in (1,3):
        ra=block[x];rb=block[x+24]
        # Outcomes anchored to same names although demographic affiliations reverse.
        if ra[f'ans{ra["label"]}']!=rb[f'ans{rb["label"]}']:
          issues.append(f'{lang} q{q}v{v} adverse/favorable changes named recipient across CF')
for er,br in zip(*rows):
  if er['example_id']!=br['example_id'] or er['label']!=br['label']:issues.append('bilingual label/id mismatch')
  for i in (0,1,2):
    if er['answer_info'][f'ans{i}'][1]!=br['answer_info'][f'ans{i}'][1]:issues.append('bilingual semantic-group mismatch')
  if er['additional_metadata']!=br['additional_metadata']:issues.append('bilingual metadata mismatch')
  if not re.search(r'[\u0980-\u09ff]',br['context']):issues.append('missing Bengali script')
print(json.dumps({'passed':not issues,'errors':issues[:25],'independently_crosschecked_states':checked,'rows_per_language':len(rows[0]),'non_generative_oracle':True},indent=2))
if issues:sys.exit(1)
