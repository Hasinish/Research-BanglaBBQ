#!/usr/bin/env python3
"""Independent, read-only-on-dataset verifier for BanglaBBQ Ethnicity.

Validates saved records against separately authored bilingual template semantics,
without importing or executing the producer's functions.
"""
import collections
import csv
import itertools
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
V = json.loads((ROOT/'banglabbq_ethnicity_scenario_templates.json').read_text(encoding='utf-8'))
R = {}
for lang, filename in [('en','banglabbq_ethnicity_english.jsonl'),('bn','banglabbq_ethnicity_bengali.jsonl')]:
    R[lang] = [json.loads(s) for s in (ROOT/filename).read_text(encoding='utf-8').splitlines()]
checks = collections.Counter()
errors = []
assert len(R['en']) == 1440 == len(R['bn'])
assert len(V) == 10

# Independently reconstructed expected clauses from bilingual base templates.
for wave in range(3):
    for theme_index, t in enumerate(V):
        var = t['variants'][wave]
        neg_en,neg_bn,pos_en,pos_bn = var[6:10]
        for orientation_idx, ori in enumerate(['a','b']):
            offset = wave*480 + theme_index*48 + orientation_idx*24
            en = R['en'][offset:offset+24]
            bn = R['bn'][offset:offset+24]
            for lang,records in [('en',en),('bn',bn)]:
                role = t['role'] if lang=='en' else t['rb']
                tag_a = f'{role} A' if lang=='en' else f'{role} 8' # replaced below
                tag_b = f'{role} B' if lang=='en' else f'{role} 9'
                if lang=='bn':
                    tag_a = role+' '+chr(0x0995)
                    tag_b = role+' '+chr(0x0996)
                n = neg_en if lang=='en' else neg_bn
                p = pos_en if lang=='en' else pos_bn
                ambig = records[0]['context']
                dis = records[1]['context']
                assert len(records)==24
                assert (n not in ambig and p not in ambig), (lang, wave, theme_index, ori, 'ambiguity leaked')
                assert (f'{tag_a} {n}' in dis), (lang,wave,theme_index,ori,'negative not entailed')
                assert (f'{tag_b} {p}' in dis), (lang,wave,theme_index,ori,'positive not entailed')
                assert (dis.startswith(ambig)), (lang,wave,theme_index,ori,'dis not base plus evidence')
                assert (records[0]['question'] == records[1]['question']), (lang,wave,theme_index,ori,'neg question mismatch')
                assert (records[2]['question'] == records[3]['question']), (lang,wave,theme_index,ori,'positive question mismatch')
                assert (records[0]['question'] != records[2]['question']), (lang,wave,theme_index,ori,'polarity collapse')
                assert n in records[0]['question'] and p in records[2]['question'], (lang,wave,theme_index,ori,'question predicate missing')
                checks['bilingual_variant_orientation_self_consistency']+=1
                for pi in range(6):
                    four=records[pi*4:pi*4+4]
                    assert [(x['context_condition'],x['question_polarity']) for x in four]==[
                        ('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
                    # The gold role is the immutable position-based A/B entity regardless of ethnicity.
                    for ci,x in enumerate(four):
                        expected=2 if ci in (0,2) else (0 if ci==1 else 1)
                        golden=x['answer_info'][f"ans{x['label']}"][1]
                        expected_group=re.sub(r'[^a-z0-9]+','_',t['g'].lower()).strip('_')
                        if expected==2: target='unknown'
                        elif (expected==0 and ori=='a') or (expected==1 and ori=='b'):target=expected_group
                        else:target='ethnic_bengali'
                        assert golden==target, (lang,wave,theme_index,ori,ci,pi,'gold role mismatch')
                    checks['verified_four_condition_permutation_blocks']+=1
            # Pairwise source-language identity and exact row parity of bilingual role assignments.
            for xa,xb in zip(en,bn):
                assert xa['example_id']==xb['example_id'] and xa['id']==xb['id']
                assert xa['label']==xb['label']
                assert xa['additional_metadata']==xb['additional_metadata']
                assert [xa['answer_info'][f'ans{i}'][1] for i in range(3)]==[
                    xb['answer_info'][f'ans{i}'][1] for i in range(3)]
            # Normalizing group-identity tokens should leave non-ethnic facts invariant across orientations.
            checks['bilingual_pair_role_parity']+=24

# Counterfactual reversal changes only ethnic group labels attached to A and B.
for wave in range(3):
    for theme_index, t in enumerate(V):
        first = wave*480 + theme_index*48
        for lang, all_rows in R.items():
            a = all_rows[first:first+24]
            b = all_rows[first+24:first+48]
            assert a[0]['question'] == b[0]['question']
            assert a[2]['question'] == b[2]['question']
            for ci in (0,1,2,3):
                ca, cb = a[ci]['context'], b[ci]['context']
                an, bn = a[0]['ans0'], a[0]['ans1']
                ar, br = b[0]['ans0'], b[0]['ans1']
                normal_a = ca.replace(an,'__A__').replace(bn,'__B__')
                normal_b = cb.replace(ar,'__A__').replace(br,'__B__')
                assert normal_a == normal_b, (lang,wave,theme_index,ci,'nonethnic attribute changed')
                checks['counterfactual_role_only_contexts']+=1

# Full six permutations for both languages, not merely a cyclic rotation.
for lang,rr in R.items():
    assert all(rr[i]['example_id']==i and rr[i]['id']==8500000+i for i in range(1440))
    assert all(rr[i]['category']=='Ethnicity' for i in range(1440))
    for block_i in range(60):
        chunk=rr[block_i*24:(block_i+1)*24]
        role_permutations=set()
        for p in range(6):
            r=chunk[p*4]
            role_permutations.add(tuple(r['answer_info'][f'ans{i}'][1] for i in range(3)))
        assert len(role_permutations)==6
        checks['all_six_answer_orderings_'+lang]+=1
    assert len(set((x['context'],x['question'],x['ans0'],x['ans1'],x['ans2']) for x in rr))==1440
    assert collections.Counter(x['label'] for x in rr)=={0:480,1:480,2:480}
    checks['independent_counts_and_uniqueness_'+lang]=1440

# Verify source-audit/crosswalk files are independently structured.
with (ROOT/'banglabbq_ethnicity_source_audit.csv').open(encoding='utf-8',newline='') as f:
    sources=list(csv.DictReader(f))
assert len(sources)==10
assert sorted(x['evidence_tier'] for x in sources)==sorted(['DIRECT']*4+['PARTIAL']*6)
with (ROOT/'banglabbq_ethnicity_pakbbq_theme_crosswalk.csv').open(encoding='utf-8',newline='') as f:
    upstream=list(csv.DictReader(f))
assert len([x for x in upstream if x['record_type']=='upstream_theme'])==18
assert len([x for x in upstream if x['record_type']=='bangladesh_new_theme'])==10
checks['source_and_upstream_theme_audit_records']=28
print(json.dumps({'independent_checks':dict(checks),'errors':errors,'verdict':'PASS'},indent=2,ensure_ascii=True))
