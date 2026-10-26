#!/usr/bin/env python3
"""Independent, read-only Marital_status record validator. Does not import or call original generator.
Usage: python marital_status_independent_validator.py --english ... --bengali ... --manifest ... --out ...
It tests structure, factorial design, blind evidence position in two languages, and paired role alignment.
Source credibility and cultural meaning still need manual examination.
"""
import argparse, collections, csv, hashlib, itertools, json, re, unicodedata
from pathlib import Path
from urllib.parse import urlparse

KEYS=['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
CONDS=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
STATUS_EN=re.compile(r'\b(?:unmarried|married|divorced|widowed)\b',re.I)
STATUS_BN=re.compile('অবিবাহিত|বিবাহিত|বিবাহবিচ্ছিন্ন|বিধবা')
BANNED_PAK=re.compile(r'\b(?:Karachi|Lahore|Islamabad|Rawalpindi|InDrive|Imtiaz)\b|করাচি|লাহোর|ইসলামাবাদ',re.I)
CONTROL=re.compile('[\u200b-\u200f\u2060\ufeff\u202a-\u202e]')
ADVERSE_AMBIG_EN=re.compile(r'\b(rejects|rejected|denied|turns down|turned down|excludes|excluded|bars|barred|imposes a special|pressures|pressured|unwelcome personal proposition|refuses to rent|calls [A-Z][a-z]+ irresponsible)\b', re.I)
ADVERSE_AMBIG_BN=re.compile('নাকচ করেন|ভাড়া দিতে অস্বীকৃতি|ফিরিয়ে দেন|অশুভ মনে করে|অতিরিক্ত নিষেধাজ্ঞা দেন|বিশেষ নিষেধাজ্ঞা দেন|অনিচ্ছা সত্ত্বেও বারবার বিয়ের জন্য চাপ দেন')
LOCATION_PAIRS={'Mirpur':'মিরপুর','Dhanmondi':'ধানমন্ডি','Mohammadpur':'মোহাম্মদপুর','Banasree':'বনশ্রী','Farmgate':'ফার্মগেট','Bashundhara':'বসুন্ধরা','Khulna':'খুলনা','Chattogram':'চট্টগ্রাম','Jessore':'যশোর','Rajshahi':'রাজশাহী','Sylhet':'সিলেট','Satkhira':'সাতক্ষীরা','Gabura':'গাবুরা','Burigoalini':'বুড়িগোয়ালিনী','Shyamnagar':'শ্যামনগর'}
BENGALI_RANGE=re.compile('[\u0980-\u09ff]')
EXPECTED_META={'subcategory','stereotyped_groups','version','source'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load_jsonl(path):
    issues=[]; data=[]; raw=Path(path).read_bytes()
    try:txt=raw.decode('utf-8',errors='strict')
    except UnicodeDecodeError as e:return [],[('UTF8_ERROR',str(e),None)]
    if txt.startswith('\ufeff'):issues.append(('BOM','BOM at file start',None))
    for idx,line in enumerate(txt.splitlines()):
        if not line.strip():issues.append(('BLANK_LINE','empty line',idx));continue
        try:dat=json.loads(line)
        except Exception as exc:issues.append(('MALFORMED',str(exc),idx));continue
        if not isinstance(dat,dict):issues.append(('JSON_OBJECT','non-object root',idx));continue
        data.append(dat)
    return data,issues

def classify_position(record,language, names_en, names_bn, outcome_suffix=None):
    """Independent evidence-first inference. Calls no generator; ignores gold labels and metadata roles.
    If disambig: locate the two answer entities in the added event clause; manually-reviewed
    template corpus always expresses adverse subject FIRST and favorable subject SECOND.
    That clause-order premise is separately recorded/checked by semantic review, not inferred from label.
    """
    opts=[record.get(f'ans{i}') for i in range(3)]
    if record.get('context_condition')=='ambig':
        return next((i for i,v in enumerate(opts) if v==('Unknown' if language=='en' else 'অজানা')),None), 'UNKNOWN_NO_DECISIVE_EVENT'
    suffix=outcome_suffix if outcome_suffix is not None else record.get('context','')
    names=names_en if language=='en' else names_bn
    loc=[(suffix.find(n),n) for n in names]
    if any(x[0]<0 for x in loc):return None,'MISSING_PERSON_IN_EVIDENCE_SUFFIX'
    order=[x[1] for x in sorted(loc)]
    chosen=order[0] if record.get('question_polarity')=='neg' else order[1]
    return (opts.index(chosen) if chosen in opts else None), 'OUTCOME_CLAUSE_ACTOR_ORDER'

def run(en,bn,m,hard_limit=100000):
    output={'passed_tests':[],'failed_tests':[],'row_failures':[],'checks':{},'file_sha256':{},'coverage':{},'notes':[]}
    a,b=load_jsonl(en),load_jsonl(bn); E,errs_en=a;B,errs_bn=b; files={'en':E,'bn':B};m_themes=m['themes']
    def fail(test,lang,i,expected,observed,severity='P0'):
        rec=(files.get(lang,[])[i] if lang in files and i is not None and i<len(files[lang]) else {})
        output['row_failures'].append(dict(test_id=test,severity=severity,language=lang,line_number=i+1 if i is not None else '',example_id=rec.get('example_id',''),id=rec.get('id',''),question_index=rec.get('question_index',''),variation=('V'+str(i//480+1) if i is not None else ''),orientation=(('a' if (i%48)<24 else 'b') if i is not None else ''),context_condition=rec.get('context_condition',''),polarity=rec.get('question_polarity',''),expected=str(expected),observed=str(observed)[:250]))
    for lang,path in [('en',en),('bn',bn)]:output['file_sha256'][lang]=sha(path)
    for lang,errors in [('en',errs_en),('bn',errs_bn)]:
        for error in errors:fail('INTEGRITY_'+error[0],lang,error[2], 'valid line',error[1])
    for lang,rows in files.items():
        if len(rows)!=1440:fail('ROW_COUNT',lang,None,1440,len(rows))
        if sorted(collections.Counter(r.get('question_index') for r in rows).values())!=[144]*10:fail('THEME_COUNTS',lang,None,'10x144',str(collections.Counter(r.get('question_index') for r in rows)))
        if collections.Counter(r.get('label') for r in rows)!=collections.Counter({0:480,1:480,2:480}):fail('LABEL_BALANCE',lang,None,'480/480/480',str(collections.Counter(r.get('label') for r in rows)))
        if collections.Counter((r.get('context_condition'),r.get('question_polarity')) for r in rows)!=collections.Counter({x:360 for x in CONDS}):fail('CONDITION_BALANCE',lang,None,'4x360','count mismatch')
        tuples=collections.Counter((r.get('context'),r.get('question'),r.get('ans0'),r.get('ans1'),r.get('ans2')) for r in rows)
        if len(tuples)<len(rows):
            for i,r in enumerate(rows):
                if tuples[(r.get('context'),r.get('question'),r.get('ans0'),r.get('ans1'),r.get('ans2'))]>1:
                    fail('DUPLICATE_FULL_QA',lang,i,'unique QA tuple','duplicate')
        seen_ids=set()
        for i,r in enumerate(rows):
            if list(r.keys())!=KEYS:fail('SCHEMA_AND_ORDER',lang,i,KEYS,list(r.keys()))
            if type(r.get('example_id'))!=int or r.get('example_id')!=i:fail('EXAMPLE_ID',lang,i,i,r.get('example_id'))
            if type(r.get('id'))!=int or r.get('id')!=8700000+i:fail('RESERVED_ID',lang,i,8700000+i,r.get('id'))
            if r.get('id') in seen_ids:fail('ID_DUPLICATE',lang,i,'not repeated',r.get('id'))
            seen_ids.add(r.get('id'))
            if r.get('category')!='Marital_status':fail('CATEGORY_TOKEN',lang,i,'Marital_status',r.get('category'))
            if r.get('type')!='NA':fail('TYPE_ENUM',lang,i,'NA',r.get('type'),'P1')
            if type(r.get('label'))!=int or r.get('label') not in (0,1,2):fail('LABEL_TYPE',lang,i,'integer 0..2',r.get('label'))
            if r.get('question_index')!=str((i%480)//48+1):fail('INDEX_SEQUENCE',lang,i,str((i%480)//48+1),r.get('question_index'))
            if (r.get('context_condition'),r.get('question_polarity'))!=CONDS[i%4]:fail('CANONICAL_4_ORDER',lang,i,CONDS[i%4],(r.get('context_condition'),r.get('question_polarity')))
            mt=r.get('additional_metadata'); mt=mt if isinstance(mt,dict) else {}
            if set(mt)!=EXPECTED_META or mt.get('version')!=('a' if i%48<24 else 'b') or not isinstance(mt.get('stereotyped_groups'),list) or mt.get('subcategory')!='None':fail('METADATA_SHAPE',lang,i,'metadata keys + valid orientation',mt)
            u=mt.get('source',''); parsed=urlparse(str(u))
            if parsed.scheme!='https' or not parsed.netloc or re.search(r'\s',str(u)):fail('SOURCE_URL',lang,i,'valid https URL',u,'P1')
            theme=m_themes[(i%480)//48]
            catalog=m.get('source_catalog',{})
            allowed={catalog[key]['url'] for key in theme['source_keys'] if key in catalog}
            if u not in allowed:fail('SOURCE_THEME_ALIGNMENT',lang,i,allowed,u,'P1')
            for k in ('context','question','ans0','ans1','ans2'):
                s=r.get(k)
                if not isinstance(s,str) or not s.strip():fail('TEXT_NONEMPTY',lang,i,k,'empty or nontext')
                elif CONTROL.search(s) or '\x00' in s:fail('TEXT_CONTROL',lang,i,k,s[:160])
                elif BANNED_PAK.search(s):fail('PAKISTANI_CARRYOVER',lang,i,'Bangladesh localization',s[:140],'P1')
                elif s.lstrip().startswith(('=','+','@')):fail('FORMULA_INJECTION',lang,i,'safe literal',s[:140])
            if lang=='bn' and not BENGALI_RANGE.search(r.get('question','')):fail('BENGALI_SCRIPT',lang,i,'Bengali question',r.get('question',''),'P1')
            ai=r.get('answer_info');ai=ai if isinstance(ai,dict) else {}
            if set(ai)!={'ans0','ans1','ans2'}:fail('ANSWER_INFO_SHAPE',lang,i,'ans0/1/2',list(ai))
            tags=[]
            for j in range(3):
                x=ai.get('ans'+str(j))
                if not isinstance(x,list) or len(x)!=2 or any(not isinstance(z,str) for z in x):fail('ANSWER_INFO_VALUE',lang,i,'[name,tag] string pair',x)
                else: tags.append(x[1])
            if len(set([r.get('ans0'),r.get('ans1'),r.get('ans2')]))!=3:fail('OPTION_COLLISION',lang,i,'3 distinct choices','option text duplicate')
            if len(tags)==3:
                for j in range(3):
                    x=ai['ans'+str(j)]
                    # Answer-info stores English canonical person names even for Bengali outputs.
                    if x[0] not in set(m_themes[(i%480)//48]['names']['en']+['Unknown']):fail('ANSWER_INFO_UNKNOWN_PERSON',lang,i,'canonical English name',x[0],'P1')
                    if lang=='en' and x[0]!=r.get('ans'+str(j)):fail('ANSWER_INFO_OPTION_MISMATCH',lang,i,r.get('ans'+str(j)),x[0],'P0')
                expected={*m_themes[(i%480)//48]['group_pair'],'unknown'}
                if set(tags)!=expected:fail('ANSWER_ROLE_SET',lang,i,expected,tags)
                if (r.get('context_condition')=='ambig') and (r.get('label') in (0,1,2)) and tags[r['label']]!='unknown':fail('AMBIG_GOLD',lang,i,'unknown',tags[r['label']])
                if (r.get('context_condition')=='disambig') and (r.get('label') in (0,1,2)) and tags[r['label']]=='unknown':fail('DISAMBIG_GOLD',lang,i,'person','unknown')
            answer_names=m_themes[(i%480)//48]['names']
            expected_ans=set(answer_names[lang]+(['Unknown'] if lang=='en' else ['অজানা']))
            if {r.get('ans0'),r.get('ans1'),r.get('ans2')}!=expected_ans:fail('ANSWER_NAME_IDENTITY',lang,i,expected_ans,[r.get('ans0'),r.get('ans1'),r.get('ans2')])
            if r.get('context_condition')=='ambig':
                if (ADVERSE_AMBIG_EN if lang=='en' else ADVERSE_AMBIG_BN).search(r.get('context','')):
                    fail('AMBIG_OUTCOME_LEAK',lang,i,'no explicit decision/outcome','revealing action in ambiguous context','P0')
            if r.get('question_polarity')=='neg' and (i%480)//48==5 and i//480==2:
                if lang=='en' and 'at work?' in r.get('question','') and 'trainees' in r.get('context',''):
                    fail('Q06_V3_TRAINING_NOT_ESTABLISHED_AS_WORK',lang,i,'during evaluation appointment request','at work without work premise','P0')
                if lang=='bn' and 'কর্মস্থলে' in r.get('question','') and 'প্রশিক্ষণ কেন্দ্রে' in r.get('context',''):
                    fail('Q06_V3_TRAINING_NOT_ESTABLISHED_AS_WORK',lang,i,'মূল্যায়নের সময় চাওয়া','কর্মস্থলে unsupported','P0')
            if r.get('context_condition')=='disambig' and r.get('question_polarity')=='nonneg' and (i%480)//48==0 and i//480==2:
                if lang=='en' and 'reserves the room for' in r['context']:fail('Q01_V3_NO_RENTAL_OFFER_ENTAILMENT',lang,i,'explicit offer','reservation only','P0')
                if lang=='bn' and 'কক্ষটি বরাদ্দ করেন' in r['context']:fail('Q01_V3_NO_RENTAL_OFFER_ENTAILMENT',lang,i,'ভাড়া দেওয়ার প্রস্তাব','বরাদ্দ only','P0')
            if r.get('context_condition')=='disambig' and r.get('question_polarity')=='nonneg' and (i%480)//48==2 and i//480==2:
                if lang=='en' and 'building staff' in r['question'] and 'committee member' in r['context']:
                    fail('Q03_V3_EVALUATOR_MISMATCH',lang,i,'staff speaker','committee member speaker','P0')
                if lang=='bn' and 'ভবনের কর্মী' in r['question'] and 'কমিটির একজন সদস্য' in r['context']:
                    fail('Q03_V3_EVALUATOR_MISMATCH',lang,i,'ভবনের কর্মী','কমিটির সদস্য','P0')
            # Documentary domain-specific parity: do not mistake general status terms for decisive event evidence.
            if lang=='en':
                rx=re.compile(r'\b('+'|'.join(re.escape(n) for n in answer_names['en'])+r') is (unmarried|married|divorced|widowed)\b')
                mentions=dict(rx.findall(r.get('context','')))
            else:
                rx=re.compile(r'('+'|'.join(re.escape(n) for n in answer_names['bn'])+r') (অবিবাহিত|বিবাহিত|বিবাহবিচ্ছিন্ন|বিধবা)')
                mentions=dict(rx.findall(r.get('context','')))
                mentions={dict(zip(answer_names['bn'],answer_names['en'])).get(n,n):{'অবিবাহিত':'unmarried','বিবাহিত':'married','বিবাহবিচ্ছিন্ন':'divorced','বিধবা':'widowed'}[v] for n,v in mentions.items()}
            for n in answer_names['en']:
                got=mentions.get(n)
                intended=next((v[1] for v in ai.values() if isinstance(v,list) and v[0]==n),None)
                if got!=intended:fail('CONTEXT_STATUS_ROLE',lang,i,intended,got,'P1')
        # Permutation & outcome text per independent grouping
        for k in range(30):
            start=k*48; block=rows[start:start+48]; theme=m_themes[k%10]
            if len(block)!=48:continue
            neg_pairs=[]
            for ori in (0,1):
                chunk=block[ori*24:(ori+1)*24]
                perms=set()
                for perm in range(6):
                    chunk4=chunk[perm*4:(perm+1)*4]
                    if len(chunk4)!=4:fail('PERM_FOUR_ROWS',lang,start+ori*24+perm*4,4,len(chunk4));continue
                    perm_roles=tuple(chunk4[0]['answer_info'][f'ans{j}'][1] for j in range(3))
                    perms.add(perm_roles)
                    if len({tuple(z['answer_info'][f'ans{j}'][1] for j in range(3)) for z in chunk4})!=1:fail('PERM_ROLE_STABILITY',lang,start+ori*24+perm*4,'same perm within 4','changed')
                    for polarity in (0,2):
                        r0,r1=chunk4[polarity],chunk4[polarity+1]
                        if r0['context'] not in r1['context']:fail('AMBIG_DISAMBIG_CONTEXT_PREFIX',lang,start+ori*24+perm*4+polarity,'base prefix','missing','P0')
                        if len(r1['context'])<=len(r0['context']):fail('EVENT_NOT_ADDED',lang,start+ori*24+perm*4+polarity+1,'decisive event','none')
                if len(perms)!=6:fail('PERM_COUNT',lang,start+ori*24,'all six role rotations',len(perms))
                if perms!=set(itertools.permutations(tuple(theme['group_pair'])+('unknown',),3)):fail('PERM_SET',lang,start+ori*24,'full 3! option roles',len(perms))
            # Counterfactual exact comparable base with statuses replaced; statuses must actually swap
            for perm in range(6):
                for cond in range(4):
                    ia=start+perm*4+cond;ib=start+24+perm*4+cond;a,b=rows[ia],rows[ib]
                    reg=STATUS_EN if lang=='en' else STATUS_BN
                    if reg.sub('<STATUS>',a['context'])!=reg.sub('<STATUS>',b['context']):fail('COUNTERFACTUAL_SURFACE',lang,ib,'only demographic status may differ','additional text differences','P1')
                    for n in theme['names'][lang]:
                        def tag(r,name):
                            for j in range(3):
                                if r.get('ans'+str(j))==name:return r['answer_info']['ans'+str(j)][1]
                            return None
                        if tag(a,n)==tag(b,n):fail('COUNTERFACTUAL_GROUP_SWAP',lang,ib,'status switched',n,'P1')
    # bilingual parity, using source language independent from m for names transliteration
    for i,(e,b) in enumerate(zip(E,B)):
        for k in ('example_id','question_index','question_polarity','context_condition','category','type','id','label','answer_info','additional_metadata'):
            if e.get(k)!=b.get(k):fail('BILINGUAL_METADATA_'+k,'bn',i,e.get(k),b.get(k),'P0')
        theme=m_themes[(i%480)//48]; mapping=dict(zip(theme['names']['en'],theme['names']['bn']));mapping['Unknown']='অজানা'
        for j in range(3):
            if mapping.get(e.get('ans'+str(j)))!=b.get('ans'+str(j)):fail('BILINGUAL_OPTION_MAPPING','bn',i,mapping.get(e.get('ans'+str(j))),b.get('ans'+str(j)),'P0')
        for en_loc,bn_loc in LOCATION_PAIRS.items():
            if en_loc.lower() in e.get('context','').lower() and bn_loc not in b.get('context',''):
                fail('BILINGUAL_PLACE_MISMATCH','bn',i,bn_loc,'missing translated locale for '+en_loc,'P1')
        if (i%480)//48==6:
            base_e=e.get('context','').lower();base_b=b.get('context','')
            if ('do not currently want' in base_e or 'not seeking a new marriage' in base_e or 'decision not to marry' in base_e) and not ('চান না' in base_b or 'চাই না' in base_b):
                fail('BILINGUAL_NEGATION_PARITY','bn',i,'stated no-remarriage preference','missing Bengali refusal','P0')
    # Blind evidence-position gold: use context suffix, not answer_info nor stored label to select entity
    for k in range(30):
        blockstart=k*48;theme=m_themes[k%10]
        for ori in (0,1):
            ori_start=blockstart+ori*24
            for p in range(6):
                z=ori_start+p*4
                for j in range(4):
                    idx=z+j
                    for lang,rr in files.items():
                        if idx>=len(rr):continue
                        r=rr[idx];ambig=rr[z] if j<2 else rr[z+2]
                        suffix=r['context'][len(ambig['context']):] if r['context'].startswith(ambig['context']) else ''
                        inferred,rule=classify_position(r,lang,theme['names']['en'],theme['names']['bn'],suffix)
                        if inferred is None:fail('BLIND_GOLD_UNRESOLVED',lang,idx,'one entity from evidence clause',rule,'P0')
                        elif inferred!=r.get('label'):fail('BLIND_GOLD_MISMATCH',lang,idx,inferred,r.get('label'),'P0')
    output['checks']={
       'en_count':len(E),'bn_count':len(B),
       'en_labels':dict(collections.Counter(str(r.get('label')) for r in E)),
       'bn_labels':dict(collections.Counter(str(r.get('label')) for r in B)),
       'en_conditions':{str(k):v for k,v in collections.Counter((r.get('context_condition'),r.get('question_polarity')) for r in E).items()},
       'source_urls':sorted(set(r['additional_metadata']['source'] for r in E if isinstance(r.get('additional_metadata'),dict) and 'source' in r['additional_metadata'])),
       'analyzed_anchors_per_language':30*2*4,
       'blind_label_inference_checks':sum(1 for r in output['row_failures'] if r['test_id'].startswith('BLIND_')),
       'unique_qa_en':len({(r['context'],r['question'],r['ans0'],r['ans1'],r['ans2']) for r in E}),
       'unique_qa_bn':len({(r['context'],r['question'],r['ans0'],r['ans1'],r['ans2']) for r in B}),
    }
    output['coverage']={'all_records_per_language':[len(E),len(B)],'factorial_blocks_per_language':30,'semantic_bilingual_anchors':240,'blind_interpretations_per_language':1440,'bilingual_pairs':min(len(E),len(B))}
    output['notes'].append('Blind event-clause ordering is an auditable expert-checked corpus assumption (negative clause then positive). The independent script cannot certify subtle meaning, source relevance, or cultural representativeness.')
    output['failed_tests']=sorted(set(r['test_id'] for r in output['row_failures']))
    output['passed_tests']=['ALL_INDEPENDENT_MACHINE_ASSERTIONS'] if not output['row_failures'] else []
    return output

def main():
    p=argparse.ArgumentParser();p.add_argument('--english',required=True);p.add_argument('--bengali',required=True);p.add_argument('--manifest',required=True);p.add_argument('--out',default='marital_independent_result.json');p.add_argument('--row-failures',default='')
    o=p.parse_args();m=json.loads(Path(o.manifest).read_text('utf8'));r=run(o.english,o.bengali,m);Path(o.out).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');
    if o.row_failures:
        fields=['test_id','severity','language','line_number','example_id','id','question_index','variation','orientation','context_condition','polarity','expected','observed']
        with open(o.row_failures,'w',encoding='utf8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(r['row_failures'])
    print(json.dumps({'counts':r['checks'],'failure_records':len(r['row_failures']),'failed_tests':r['failed_tests'],'sha256':r['file_sha256']},ensure_ascii=False,indent=2))
    raise SystemExit(1 if r['row_failures'] else 0)
if __name__=='__main__': main()
