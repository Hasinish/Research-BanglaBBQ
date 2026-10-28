#!/usr/bin/env python3
"""Read-only audit for saved BanglaBBQ Marital_status Q11-Q20 bilingual JSONL.

Usage:
  python marital_male_validation.py --directory /mnt/data --selftest --json-out /mnt/data/marital_male_validation_results.json

Source existence / Bangladesh-specific relevance and idiomatic Bengali still require
substantive research judgement. These cannot be certified by invariant tests.
"""
import argparse
import collections
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from marital_male_specs import SCENARIOS, SOURCES, STATUSES, GITHUB_SHA
from marital_male_generate import EN_FILE,BN_FILE,FIELDS,PERMUTATIONS,CONDITIONS,build_context

SPEC={(s['q'],s['v']):s for s in SCENARIOS}
EXPECTED_IDS=list(range(1440,2880))

class Problems:
    def __init__(self):self.errors=[]
    def require(self,condition,message):
        if not condition and len(self.errors)<120:self.errors.append(message)

def load_rows(path):
    rows=[]
    with Path(path).open(encoding='utf-8') as f:
      for line_num,line in enumerate(f,1):
        if not line.strip():raise ValueError(f'{path}:{line_num}: blank JSONL line')
        try:rows.append(json.loads(line))
        except Exception as exc:raise ValueError(f'{path}:{line_num}: invalid JSON {exc}') from exc
    return rows

def context_gold_oracle(s,lang,orientation,cond,pol):
    """Independent of saved label: explicit authored decision text fixes adverse/beneficial receiver.
    Conditional contexts omit any such decision; the correct answer is Unknown.
    """
    if cond=='ambig':return 'U'
    base=build_context(s,lang,orientation,False)
    full=build_context(s,lang,orientation,True)
    if not full.startswith(base+' '):raise AssertionError('authored decision is not a factual disambiguation')
    adverse=s['bad'];favorable='B' if adverse=='A' else 'A'
    names={'A':s['A'] if lang=='en' else s['AB'],'B':s['B'] if lang=='en' else s['BB']}
    tail=full[len(base)+1:]
    decision=s['decision_'+lang].format(bad=names[adverse],good=names[favorable])
    if lang=='bn':decision=decision.replace('-কে','কে').replace('-এর','এর')
    assert tail==decision
    assert names[adverse] in tail and names[favorable] in tail
    return adverse if pol=='neg' else favorable

def validate_rows(eng,bn,strict=True):
  err=Problems()
  summary={'rows_english':len(eng),'rows_bengali':len(bn),'schema_fields':len(FIELDS),
           'unique_semantic_cases_per_language':0,'mutation_tests':{},'evidence_tiers':collections.Counter(s['tier'] for s in SOURCES.values())}
  expected_states=set((q,v,o,co,pol) for q in range(11,21) for v in (1,2,3) for o in ('a','b') for co,pol in CONDITIONS)
  all_by_lang=[]
  for lang,rows in [('en',eng),('bn',bn)]:
    err.require(len(rows)==1440,f'{lang}: wrong record count {len(rows)}')
    ids=[r.get('example_id') for r in rows]
    err.require(ids==EXPECTED_IDS,f'{lang}: example_id sequence must be 1440..2879')
    err.require([r.get('id') for r in rows]==[8700000+i for i in EXPECTED_IDS],f'{lang}: numeric id sequence wrong')
    err.require(len(ids)==len(set(ids)),f'{lang}: example_id duplicates')
    err.require(len(set(r.get('id') for r in rows))==len(rows),f'{lang}: numeric id duplicates')
    cases=collections.defaultdict(list)
    for idx,r in enumerate(rows):
      if len(err.errors)>100:break
      ident=f'{lang}:row={idx+1}:example_id={r.get("example_id")}'
      err.require(list(r)==FIELDS,ident+': 15 exact field keys/order incorrect')
      err.require(type(r.get('example_id')) is int and type(r.get('id')) is int,ident+': invalid integer ID type')
      err.require(type(r.get('label')) is int and r['label'] in (0,1,2),ident+': invalid gold label type/value')
      err.require(type(r.get('question_index')) is str and r['question_index'] in [str(x) for x in range(11,21)],ident+': question_index must be STRING 11-20')
      err.require(r.get('category')=='Marital_status' and r.get('type')=='NA',ident+': category or type incorrect')
      err.require(r.get('context_condition') in ('ambig','disambig') and r.get('question_polarity') in ('neg','nonneg'),ident+': condition or polarity invalid')
      md=r.get('additional_metadata',{})
      err.require(type(md) is dict and set(md)=={'subcategory','stereotyped_groups','version','source'},ident+': metadata keys unexpected')
      o=md.get('version')
      err.require(o in ('a','b') and md.get('subcategory')=='None',ident+': metadata version or subcategory invalid')
      info=r.get('answer_info',{})
      err.require(type(info) is dict and set(info)=={'ans0','ans1','ans2'},ident+': answer_info invalid')
      options=[r.get(f'ans{i}') for i in range(3)]
      err.require(all(isinstance(x,str) and x for x in options),ident+': empty/nonstring answer')
      for j in range(3):
        val=info.get(f'ans{j}')
        err.require(isinstance(val,list) and len(val)==2 and val[0]==options[j],ident+f': answer_info ans{j} exact text mismatch')
      unknown='Unknown' if lang=='en' else 'অজানা'
      err.require(options.count(unknown)==1,ident+': expected exactly one Unknown option')
      q=int(r.get('question_index','0')); v=((r['example_id']-1440)//480)+1 if isinstance(r.get('example_id'),int) else -1
      if q not in range(11,21) or v not in (1,2,3):continue
      s=SPEC[q,v]
      st=STATUSES[q]
      err.require(md.get('source')==SOURCES[q]['url'],ident+': source mismatch')
      err.require(md.get('stereotyped_groups')==[st[6]],ident+': stereotyped_groups mismatch')
      base=1440+(v-1)*480+(q-11)*48
      x=r['example_id']-base
      err.require(0<=x<48,ident+': wrong variation/theme block position')
      if not 0<=x<48:continue
      expected_o='a' if x<24 else 'b'
      expected_perm=PERMUTATIONS[((x%24)//4)]
      expected_cond,expected_pol=CONDITIONS[x%4]
      err.require(o==expected_o,ident+': wrong counterfactual orientation')
      err.require((r['context_condition'],r['question_polarity'])==(expected_cond,expected_pol),ident+': broken four-condition order')
      role_names={'A':s['A'] if lang=='en' else s['AB'],'B':s['B'] if lang=='en' else s['BB'],'U':unknown}
      for i,role in enumerate(expected_perm):
        err.require(options[i]==role_names[role],ident+': missing/wrong six-way answer permutation')
        actual_group=info[f'ans{i}'][1]
        target='A' if expected_o=='a' else 'B'
        group='unknown' if role=='U' else st[4] if role==target else st[5]
        err.require(actual_group==group,ident+': semantic group/status swap incorrect')
      check_context=build_context(s,lang,expected_o,expected_cond=='disambig')
      err.require(r.get('context')==check_context,ident+': context mismatch, bilingual text, swapped marital status, decision recipient, or ambig leakage')
      question=s[('neg_' if expected_pol=='neg' else 'pos_')+lang]
      err.require(r.get('question')==question,ident+': question mismatch (possibly polarity/negation error)')
      oracle=context_gold_oracle(s,lang,expected_o,expected_cond,expected_pol)
      expected_gold=expected_perm.index(oracle)
      err.require(r.get('label')==expected_gold,ident+f': wrong gold label, expected {expected_gold}')
      if expected_cond=='ambig':err.require(options[r['label']]==unknown,ident+': ambiguous answer leaked')
      if expected_cond=='disambig':err.require(oracle in ('A','B'),ident+': disambiguated one-answer entailment missing')
      cases[q,v,expected_o,expected_cond,expected_pol].append((expected_perm,r))
    err.require(len(cases)==len(expected_states),f'{lang}: expected 240 unique semantic states, found {len(cases)}')
    err.require(set(cases)==expected_states,f'{lang}: missing/extra semantic state(s)')
    for key,six in cases.items():
      err.require(len(six)==6,f'{lang}: semantic case {key} has {len(six)} answer permutations instead of 6')
      err.require(set(p for p,r in six)==set(PERMUTATIONS),f'{lang}: semantic case {key} missing complete answer permutations')
      err.require(len(set(r['context'] for p,r in six))==1,f'{lang}: semantic case {key} not context-consistent')
      err.require(len(set(r['question'] for p,r in six))==1,f'{lang}: semantic case {key} not question-consistent')
    err.require(len(set((r['context'],r['question'],r['ans0'],r['ans1'],r['ans2']) for r in rows))==len(rows),f'{lang}: unintended duplicate QA tuples')
    labels=collections.Counter(r['label'] for r in rows)
    err.require(labels=={0:480,1:480,2:480},f'{lang}: expected 480/480/480 balanced labels, got {dict(labels)}')
    err.require(set(r['question_index'] for r in rows)==set(str(x) for x in range(11,21)),f'{lang}: not ten themes')
    for q in range(11,21):
      err.require(sum(r['question_index']==str(q) for r in rows)==144,f'{lang}: Q{q} not 144 records')
    position=collections.Counter()
    role_counts=collections.Counter()
    for s in SCENARIOS:
      start=1440+(s['v']-1)*480+(s['q']-11)*48
      seg=rows[start-1440:start-1440+48]
      err.require(len(seg)==48,f'{lang}: Q{s["q"]}V{s["v"]} has wrong block count')
      for pol in ('neg','nonneg'):
        first_count=0; second_count=0
        for r in seg:
          if r['context_condition']!='disambig' or r['question_polarity']!=pol:continue
          opt=r['answer_info'][f'ans{r["label"]}']
          name=opt[0]
          a_name=s['A'] if lang=='en' else s['AB']
          b_name=s['B'] if lang=='en' else s['BB']
          person='A' if name==a_name else 'B' if name==b_name else 'U'
          ori=r['additional_metadata']['version']
          introduction_first='A' if ori=='a' else 'B'
          intro='first' if person==introduction_first else 'second'
          position[pol,intro]+=1
          position['Q'+str(s['q']),pol,intro]+=1
          if intro=='first':first_count+=1
          else:second_count+=1
          group=r['answer_info'][f'ans{r["label"]}'][1]
          role_counts[pol, 'target' if group==STATUSES[s['q']][4] else 'comparator']+=1
        err.require((first_count,second_count)==(6,6),f'{lang}: Q{s["q"]}V{s["v"]} {pol} introduction position {(first_count,second_count)} not 6/6')
    for pol in ('neg','nonneg'):
      err.require((position[pol,'first'],position[pol,'second'])==(180,180),f'{lang}: {pol} global intro position imbalance')
      for q in range(11,21):
        err.require((position['Q'+str(q),pol,'first'],position['Q'+str(q),pol,'second'])==(18,18),f'{lang}: Q{q} {pol} theme position imbalance')
      err.require((role_counts[pol,'target'],role_counts[pol,'comparator'])==(180,180),f'{lang}: {pol} target/comparator gold imbalance')
    all_by_lang.append(dict(lang=lang,counts={'questions':dict(collections.Counter(r['question_index'] for r in rows)),
              'labels':dict(labels),'disambig_intro_positions':{'neg':{'first':position['neg','first'],'second':position['neg','second']},
                  'nonneg':{'first':position['nonneg','first'],'second':position['nonneg','second']}},
              'disambig_gold_groups':{p:{'target':role_counts[p,'target'],'comparator':role_counts[p,'comparator']} for p in ('neg','nonneg')}}))
  err.require(len(eng)==len(bn), 'bilingual file row counts mismatch')
  for i,(e,b) in enumerate(zip(eng,bn)):
    ident=f'bilingual:row={i+1}'
    for f in ('example_id','question_index','question_polarity','context_condition','category','label','type','id'):
      err.require(e.get(f)==b.get(f),ident+': '+f+' differs')
    err.require(e.get('additional_metadata')==b.get('additional_metadata'),ident+': metadata differs')
    err.require([e.get('answer_info',{}).get(f'ans{k}',[None,None])[1] for k in range(3)]==
      [b.get('answer_info',{}).get(f'ans{k}',[None,None])[1] for k in range(3)],ident+': group-tag mismatch')
    err.require([e.get(f'ans{k}')=='Unknown' for k in range(3)]==
      [b.get(f'ans{k}')=='অজানা' for k in range(3)],ident+': unknown position mismatch')
    if re.search(r'[A-Za-z]{3,}',b.get('context','')+' '+b.get('question','')):
      err.require(False,ident+': Latin-letter leak in Bengali context/question')
  summary['unique_semantic_cases_per_language']=len(expected_states)
  summary['per_language']=all_by_lang
  summary['errors']=err.errors
  summary['passed']=not bool(err.errors)
  return summary

def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run_mutation_fixtures(eng,bn):
  fixtures={}
  mutations={}
  def clone():return copy.deepcopy(eng),copy.deepcopy(bn)
  a,b=clone();a[0]['example_id']=1439;mutations['broken_example_id']=(a,b)
  a,b=clone();del a[0:4];mutations['omitted_answer_permutation']=(a,b)
  a,b=clone();a[0]['context']=a[0]['context'].replace('has never married','is divorced');mutations['incorrect_marital_status']=(a,b)
  a,b=clone();a[1]['label']=(a[1]['label']+1)%3;mutations['swapped_disambiguated_gold_label']=(a,b)
  a,b=clone();b[0]['context']=b[0]['context'].replace('কখনো বিয়ে করেননি','বিয়ে করেছেন');mutations['bengali_negation_corruption']=(a,b)
  a,b=clone();a[0]['context']=a[1]['context'];mutations['ambiguous_context_outcome_leakage']=(a,b)
  a,b=clone();base=build_context(SPEC[11,1],'en','a',False);tail=a[1]['context'][len(base)+1:];tail=tail.replace('Mahin','__TMP__').replace('Rashed','Mahin').replace('__TMP__','Rashed');a[1]['context']=base+' '+tail;mutations['incorrect_disambig_outcome_recipient']=(a,b)
  for label,(ee,bb) in mutations.items():
    summary=validate_rows(ee,bb)
    fixtures[label]={'rejected':not summary['passed'],'detected_diagnostics':summary['errors'][:3]}
  return fixtures

def validate_saved(directory,selftest=False):
  directory=Path(directory)
  en=load_rows(directory/EN_FILE);bn=load_rows(directory/BN_FILE)
  results=validate_rows(en,bn)
  results['git_source_sha']=GITHUB_SHA
  results['file_sha256']={EN_FILE:sha256(directory/EN_FILE),BN_FILE:sha256(directory/BN_FILE)}
  results['source_tier_counts']={k:sum(1 for s in SOURCES.values() if s['tier']==k) for k in set(s['tier'] for s in SOURCES.values())}
  if selftest:
    results['mutation_tests']=run_mutation_fixtures(en,bn)
    results['mutation_tests_all_rejected']=all(v['rejected'] for v in results['mutation_tests'].values())
    results['passed']=results['passed'] and results['mutation_tests_all_rejected']
    with tempfile.TemporaryDirectory() as work:
      gen=Path(__file__).with_name('marital_male_generate.py')
      p=subprocess.run([sys.executable,str(gen),'--output-dir',work],check=True,capture_output=True,text=True)
      results['deterministic_regeneration_byte_identical']=all(
        sha256(directory/name)==sha256(Path(work)/name) for name in (EN_FILE,BN_FILE,'marital_male_theme_manifest.csv','marital_male_sources.csv','marital_male_import_manifest.json'))
    results['passed']=results['passed'] and results['deterministic_regeneration_byte_identical']
  return results

def main():
  ap=argparse.ArgumentParser();ap.add_argument('--directory',default='.')
  ap.add_argument('--selftest',action='store_true');ap.add_argument('--json-out')
  args=ap.parse_args()
  res=validate_saved(args.directory,args.selftest)
  if args.json_out:Path(args.json_out).write_text(json.dumps(res,ensure_ascii=False,indent=2,default=dict)+'\n',encoding='utf-8')
  print(json.dumps({'passed':res['passed'],'rows_en':res['rows_english'],'rows_bn':res['rows_bengali'],
       'unique_semantic_cases_per_language':res['unique_semantic_cases_per_language'],
       'evidence_tier_counts':res['source_tier_counts'],
       'mutation_tests_all_rejected':res.get('mutation_tests_all_rejected'),
       'deterministic_regeneration_byte_identical':res.get('deterministic_regeneration_byte_identical'),
       'errors':res['errors'][:12]},ensure_ascii=False,indent=2))
  return 0 if res['passed'] else 1

if __name__=='__main__':sys.exit(main())
