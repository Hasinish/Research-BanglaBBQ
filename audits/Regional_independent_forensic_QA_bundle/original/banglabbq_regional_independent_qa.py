#!/usr/bin/env python3
"""Independent post-generation Regional JSONL/CSV/manifest consistency checks.
Python stdlib only, local files only; not a substitute for a Bengali human panel.
Run: python3 banglabbq_regional_independent_qa.py --outdir /mnt/data
"""
import argparse,collections,csv,hashlib,itertools,json,pathlib,re

def inspect(directory):
    p=pathlib.Path(directory)
    en=[json.loads(s) for s in (p/'banglabbq_regional_english.jsonl').read_text(encoding='utf-8').splitlines()]
    bn=[json.loads(s) for s in (p/'banglabbq_regional_bengali.jsonl').read_text(encoding='utf-8').splitlines()]
    manifest=json.loads((p/'banglabbq_regional_expansion_manifest.json').read_text(encoding='utf-8'))
    themes=json.loads((p/'banglabbq_regional_scenario_templates.json').read_text(encoding='utf-8'))['themes']
    audit=list(csv.DictReader((p/'banglabbq_regional_source_audit.csv').open(encoding='utf-8')))
    crosswalk=list(csv.DictReader((p/'banglabbq_regional_pakbbq_theme_crosswalk.csv').open(encoding='utf-8')))
    qa_text=(p/'banglabbq_regional_qa_report.md').read_text(encoding='utf-8')
    results={}
    def check(name,cond):results[name]=bool(cond)
    check('record count and sequential paired identifiers',len(en)==len(bn)==1440 and all(a['example_id']==b['example_id']==i and a['id']==b['id']==8400000+i for i,(a,b) in enumerate(zip(en,bn))))
    check('one-to-one question polarity, condition, gold and metadata',all(all(a[k]==b[k] for k in ('question_index','question_polarity','context_condition','label','category','additional_metadata','type')) for a,b in zip(en,bn)))
    check('all source references present and syntactically HTTPS',all(u['source_1_url'].startswith('https://') for u in audit) and all(r['additional_metadata']['source'].startswith('https://') for r in en+bn))
    check('exactly ten approved/provisionally accepted topics and 30 scenarios',len(audit)==10 and len(themes)==10 and len(manifest['scenarios'])==30)
    check('18 original PakBBQ upstream indices crosswalked',len([x for x in crosswalk if x['origin_status']=='PAK_THEME_AUDIT'])==18 and {x['upstream_index'] for x in crosswalk if x['origin_status']=='PAK_THEME_AUDIT'}=={str(i) for i in range(1,19)})
    check('correct PakBBQ source theme counts sum to 944',sum(int(x['upstream_record_count']) for x in crosswalk if x['origin_status']=='PAK_THEME_AUDIT')==944)
    check('unique base scenes across 3 variations per theme',all(len({c['scene_en'] for c in t['variations']})==3 and len({c['scene_bn'] for c in t['variations']})==3 for t in themes))
    check('all base scenes and verdicts include both swappable origin slots',all(all(c[k].count('{a}')>0 and c[k].count('{b}')>0 for k in ('scene_en','scene_bn','verdict_en','verdict_bn')) for t in themes for c in t['variations']))
    real_swap_errors=[]
    for wave in range(3):
      for j,t in enumerate(themes):
       case=t['variations'][wave]
       start=wave*480+j*48
       for orientation,offset in [('a',0),('b',24)]:
        for lang,records in [('en',en),('bn',bn)]:
         a,b=(t['target_'+lang],t['other_'+lang]) if orientation=='a' else (t['other_'+lang],t['target_'+lang])
         expected_amb=case['scene_'+lang].replace('{a}',a).replace('{b}',b)
         expected_dis=expected_amb+' '+case['verdict_'+lang].replace('{a}',a).replace('{b}',b)
         for r in records[start+offset:start+offset+24]:
          expected_context=expected_amb if r['context_condition']=='ambig' else expected_dis
          if r['context']!=expected_context:
           real_swap_errors.append((t['theme'],wave+1,orientation,lang,r['example_id']))
    check('both 30-scenario regional swaps exactly match bilingual authored base strings',not real_swap_errors)
    errors=[]
    for wave in range(3):
      for j,t in enumerate(themes):
       start=wave*480+j*48
       for ori_i in range(2):
        for k in range(0,24,4):
         for rows in (en,bn):
          four=rows[start+ori_i*24+k:start+ori_i*24+k+4]
          if [(r['context_condition'],r['question_polarity']) for r in four] != [('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]:errors.append('incorrect canonical quartet')
          if four[0]['context']!=four[2]['context'] or four[1]['context']!=four[3]['context']:errors.append('context differs by question polarity')
          if not four[1]['context'].startswith(four[0]['context']):errors.append('disambig does not include ambiguous context')
          if four[0]['label']!=four[2]['label']:errors.append('ambiguous answers differ by question polarity')
          if four[1]['label']==four[3]['label']:errors.append('disambiguated outcomes not opposed')
          if any(len(set(four[q]['ans'+str(i)] for q in range(4)))!=1 for i in range(3)):errors.append('permutation changed inside canonical quartet')
    check('all 720 canonical 4-record quartets coherent',not errors)
    latin=[(r['example_id'],k) for r in bn for k in ('context','question','ans0','ans1','ans2') if re.search(r'\b[A-Za-z]{3,}\b',r[k])]
    check('zero Latin-script English words in Bengali QA text',not latin)
    check('all locally generated file SHA-256 match QA report',all(hashlib.sha256((p/name).read_bytes()).hexdigest()==digest for name,digest in re.findall(r'`(banglabbq_regional_[^`]+)`\s+—\s+`([a-f0-9]{64})`',qa_text)))
    # Verify every line's answer_info fields agree with displayed answer and each of the 3 roles is distinct.
    check('answer-info role and displayed text consistency',all(all(r['answer_info']['ans'+str(i)][0]==r['ans'+str(i)] for i in range(3)) and len(set(r['answer_info']['ans'+str(i)][1] for i in range(3)))==3 for r in en+bn))
    failures=[k for k,v in results.items() if not v]
    print(json.dumps({'independent_checks_passed':len(results)-len(failures),'total':len(results),'failures':failures,'candidate_themes':len(themes),'per_language':len(en),'upstream_themes':18,'latin_leaks':len(latin),'quartet_issues':len(errors)},indent=2))
    if failures:raise SystemExit(1)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--outdir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);args=ap.parse_args();inspect(args.outdir)
