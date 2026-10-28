#!/usr/bin/env python3
"""Deterministically generate append-only Q11-Q20 BanglaBBQ marital-status JSONLs.

Usage: python marital_male_generate.py --output-dir /mnt/data
Source-specific human/peer validation is NOT replaced by this generator.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from marital_male_specs import GITHUB_SHA, SCENARIOS, SOURCES, STATUSES

EN_FILE='BanglaBBQ_Marital_Male_Q11_Q20_english.jsonl'
BN_FILE='BanglaBBQ_Marital_Male_Q11_Q20_bengali.jsonl'
PERMUTATIONS=[('A','B','U'),('A','U','B'),('B','A','U'),('B','U','A'),('U','A','B'),('U','B','A')]
CONDITIONS=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
FIELDS=['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
BN_DIGITS=str.maketrans('0123456789','০১২৩৪৫৬৭৮৯')

def build_context(spec, lang, orientation, disambig):
    q=spec['q']
    target_en,comp_en,target_bn,comp_bn,*_=STATUSES[q]
    is_a=orientation=='a'
    target_person='A' if is_a else 'B'
    statuses_en={target_person:target_en,('B' if is_a else 'A'):comp_en}
    statuses_bn={target_person:target_bn,('B' if is_a else 'A'):comp_bn}
    first,second=('A','B') if is_a else ('B','A')
    name_en={'A':spec['A'],'B':spec['B']}
    name_bn={'A':spec['AB'],'B':spec['BB']}
    if lang=='en':
        base=(f"In this fictional situation, {name_en[first]} and {name_en[second]}, "
              f"both {spec['age']}-year-old men, {spec['scene_en']}. "
              f"{name_en[first]} {statuses_en[first]}, while {name_en[second]} {statuses_en[second]}.")
    else:
        base=(f"ধরা যাক, {str(spec['age']).translate(BN_DIGITS)} বছর বয়সী দুই পুরুষ "
              f"{name_bn[first]} ও {name_bn[second]} {spec['scene_bn']}। "
              f"{name_bn[first]} {statuses_bn[first]}, আর {name_bn[second]} {statuses_bn[second]}।")
    if not disambig:
        return base
    bad=spec['bad']
    good='B' if bad=='A' else 'A'
    template=spec['decision_en'] if lang=='en' else spec['decision_bn']
    names=name_en if lang=='en' else name_bn
    outcome=template.format(bad=names[bad],good=names[good])
    if lang=='bn':
        # Bengali postpositions/suffixes attach to proper names without an ASCII hyphen.
        outcome=outcome.replace('-কে','কে').replace('-এর','ের')
    return base+' '+outcome

def construct_record(spec,lang,orientation,permutation,context_condition,polarity,example_id):
    q=spec['q']; t_en,c_en,t_bn,c_bn,t_tag,c_tag,stereotyped=STATUSES[q]
    target='A' if orientation=='a' else 'B'
    group={'A':(t_tag if target=='A' else c_tag),'B':(t_tag if target=='B' else c_tag),'U':'unknown'}
    names={'A':spec['A'] if lang=='en' else spec['AB'],
           'B':spec['B'] if lang=='en' else spec['BB'],
           'U':'Unknown' if lang=='en' else 'অজানা'}
    bad=spec['bad']; good='B' if bad=='A' else 'A'
    gold='U' if context_condition=='ambig' else (bad if polarity=='neg' else good)
    texts=[names[x] for x in permutation]
    answer_info={f'ans{i}':[names[role],group[role]] for i,role in enumerate(permutation)}
    source=SOURCES[q]['url']
    question=spec[('neg_' if polarity=='neg' else 'pos_')+lang]
    record={
      'example_id':example_id,
      'question_index':str(q),
      'question_polarity':polarity,
      'context_condition':context_condition,
      'category':'Marital_status',
      'answer_info':answer_info,
      'additional_metadata':{'subcategory':'None','stereotyped_groups':[stereotyped], 'version':orientation,'source':source},
      'context':build_context(spec,lang,orientation,context_condition=='disambig'),
      'question':question,
      'ans0':texts[0],'ans1':texts[1],'ans2':texts[2],
      'label':permutation.index(gold),
      'type':'NA',
      'id':8700000+example_id,
    }
    assert list(record)==FIELDS
    return record

def create_rows(lang):
    spec_lookup={(s['q'],s['v']):s for s in SCENARIOS}
    result=[]
    for variation in (1,2,3):
      for q in range(11,21):
        s=spec_lookup[q,variation]
        start=1440+(variation-1)*480+(q-11)*48
        for o_i,orient in enumerate(('a','b')):
          for perm_i,perm in enumerate(PERMUTATIONS):
            for c_i,(cond,pol) in enumerate(CONDITIONS):
              result.append(construct_record(s,lang,orient,perm,cond,pol,start+o_i*24+perm_i*4+c_i))
    assert len(result)==1440
    return result

def write_jsonl(p,rows):
    with p.open('w',encoding='utf-8',newline='\n') as f:
       for r in rows:
          f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')

def write_csv(p,header,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
      writer=csv.DictWriter(f,fieldnames=header)
      writer.writeheader();writer.writerows(rows)

def file_sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',default='.')
    args=ap.parse_args()
    out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    english=create_rows('en');bengali=create_rows('bn')
    write_jsonl(out/EN_FILE,english);write_jsonl(out/BN_FILE,bengali)
    manifest=[]
    for s in sorted(SCENARIOS,key=lambda x:(x['q'],x['v'])):
      begin=1440+(s['v']-1)*480+(s['q']-11)*48
      src=SOURCES[s['q']]
      status=STATUSES[s['q']]
      manifest.append(dict(theme_id='Q'+str(s['q']),variation='V'+str(s['v']),
        example_id_start=begin,example_id_end=begin+47,
        person_A_english=s['A'],person_B_english=s['B'],person_A_bengali=s['AB'],person_B_bengali=s['BB'],
        age_both=s['age'],target_group_tag=status[4],comparison_group_tag=status[5],
        adverse_outcome_anchored_to=s['bad'],scene_english=s['scene_en'],scene_bengali=s['scene_bn'],
        negative_question_english=s['neg_en'],nonnegative_question_english=s['pos_en'],
        negative_question_bengali=s['neg_bn'],nonnegative_question_bengali=s['pos_bn'],
        source_evidence_tier=src['tier'],primary_source_url=src['url']))
    write_csv(out/'marital_male_theme_manifest.csv',list(manifest[0]),manifest)
    sources=[]
    for q,s in sorted(SOURCES.items()):
        sources.append(dict(question_index='Q'+str(q),**s))
    write_csv(out/'marital_male_sources.csv',list(sources[0]),sources)
    d={
      'project':'BanglaBBQ existing Marital_status append-only male-themed expansion Q11-Q20',
      'status':'CANDIDATE_OFFLINE_STRUCTURAL_QA; NOT PUBLICATION_READY',
      'source_github_repository':'https://github.com/Hasinish/Research-BanglaBBQ',
      'source_github_commit_sha':GITHUB_SHA,
      'source_english_repo_path':'Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_english.jsonl',
      'source_bengali_repo_path':'Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl',
      'append_only':True,
      'explicit_do_not_overwrite_original_1440_records':True,
      'no_external_writes_performed':True,
      'existing_example_id_range':[0,1439],
      'existing_id_range':[8700000,8701439],
      'new_example_id_range':[1440,2879],
      'new_id_range':[8701440,8702879],
      'question_indices_as_strings':[str(q) for q in range(11,21)],
      'category':'Marital_status',
      'schema_fields':FIELDS,
      'records_to_append_per_language':1440,
      'expected_post_import_total_per_language':2880,
      'variation_order':'V1 all Q11-Q20, V2 all Q11-Q20, V3 all Q11-Q20',
      'orientation_records_per_variation':{'a':24,'b':24},
      'source_evidence_tiers_by_theme':{'Q'+str(q):s['tier'] for q,s in sorted(SOURCES.items())},
      'human_language_review':'NOT PERFORMED',
      'human_source_relevance_adjudication':'NOT PERFORMED',
      'import_instruction':'Append JSONL rows only after human approval; do not alter original IDs 0-1439 or any Google Sheets rows without new authorization.',
      'files':{},
    }
    for filename in (EN_FILE,BN_FILE,'marital_male_theme_manifest.csv','marital_male_sources.csv'):
        p=out/filename
        d['files'][filename]={'records':len(english) if filename==EN_FILE else len(bengali) if filename==BN_FILE else 30 if 'theme_manifest' in filename else 10,
                              'size_bytes':p.stat().st_size,'sha256':file_sha(p)}
    # The manifest's own digest cannot be included inside itself without circularity.
    (out/'marital_male_import_manifest.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output_dir':str(out),'english':len(english),'bengali':len(bengali),'first_id':english[0]['example_id'],'last_id':english[-1]['example_id'],
      'english_sha256':d['files'][EN_FILE]['sha256'],'bengali_sha256':d['files'][BN_FILE]['sha256']},indent=2))

if __name__=='__main__':main()
