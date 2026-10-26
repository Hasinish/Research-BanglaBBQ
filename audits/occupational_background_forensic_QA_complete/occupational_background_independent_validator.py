#!/usr/bin/env python3
"""INDEPENDENT read-only forensic validator for the committed Occupational Background pair.

Does not import the original generator, and does not use its gold oracle.
For independent semantic probes, uses explicit editorial predicates (see SEMANTIC_FLAGS)
which are separately justified in the audit report. No network or remote writes.
Usage: python occupational_background_independent_validator.py --english EN --bengali BN --manifest M --json-out REPORT
"""
import argparse, collections, csv, itertools, json, re, sys, unicodedata, hashlib
from pathlib import Path
from urllib.parse import urlparse

KEYS=['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
PATTERN=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
ALLOWED_NESTED={'subcategory','stereotyped_groups','version','source'}
NEED_REVIEW=[(3,1,'AMBIGUOUS_PERMISSION','Written permission is held by both; EN positive question who was permitted is satisfied by both'),
             (6,1,'UNENTAILED_REGISTER','EN says receptionist delays Habib, not explicitly that Habib was registered late'),
             (7,1,'UNENTAILED_INPUT','Person excluded from minutes, but questions concern the input itself'),
             (7,3,'UNENTAILED_FEEDBACK','Person excluded from register, but questions concern feedback itself')]
SCRIPT_BAN='\u200b\u200c\u200d\ufeff\u2060\u202e\u202d'

def jsonl(path,lang,errors):
    result=[]
    raw=Path(path).read_bytes()
    try: txt=raw.decode('utf-8','strict')
    except UnicodeDecodeError as e:
        errors.append({'language':lang,'row':0,'test_id':'UTF8','severity':'P0','expected':'UTF-8','observed':str(e)})
        return [],raw
    if txt.startswith('\ufeff'):errors.append({'language':lang,'row':1,'test_id':'BOM','severity':'P2','expected':'No BOM','observed':'BOM present'})
    for n,line in enumerate(txt.splitlines(),1):
        if not line.strip():
            errors.append({'language':lang,'row':n,'test_id':'JSONL_BLANK','severity':'P0','expected':'One JSON object','observed':'blank'})
            continue
        try:r=json.loads(line,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('non-finite '+x)))
        except Exception as e:
            errors.append({'language':lang,'row':n,'test_id':'JSONL_PARSE','severity':'P0','expected':'valid JSON object','observed':str(e)})
            continue
        result.append(r)
    return result,raw

def report(en,bn,manifest=None,semantic=True,source_expected=None):
    errors=[]; metrics={}; perrow=[]
    def fail(lang,i,r,tid,severity,expected,observed,field=''):
        k=r if isinstance(r,dict) else {}
        rec={'language':lang,'jsonl_line':i+1,'example_id':k.get('example_id'), 'id':k.get('id'),
             'theme':k.get('question_index'),'variation':f'V{(i//480)+1}', 'orientation':k.get('additional_metadata',{}).get('version') if isinstance(k.get('additional_metadata'),dict) else None,
             'condition':k.get('context_condition'),'polarity':k.get('question_polarity'),
             'test_id':tid,'severity':severity,'field':field,'expected':str(expected),'observed':str(observed)}
        errors.append(rec)
    for lang,recs in [('english',en),('bengali',bn)]:
        if len(recs)!=1440:fail(lang,-1,{},'COUNT','P0',1440,len(recs))
        counts=collections.Counter();labels=collections.Counter();seen_ids=set();seen_tuples=set();seen_semm=set()
        for i,r in enumerate(recs):
            if not isinstance(r,dict):fail(lang,i,{},'OBJECT','P0','dictionary',type(r));continue
            if list(r)!=KEYS:fail(lang,i,r,'KEYS','P0',KEYS,list(r))
            mustint=('example_id','label','id')
            for f in mustint:
                if type(r.get(f)) is not int:fail(lang,i,r,'INT_TYPE','P0','int',type(r.get(f)).__name__,f)
            if r.get('example_id')!=i:fail(lang,i,r,'EXAMPLE_ID','P0',i,r.get('example_id'),'example_id')
            if r.get('id')!=8600000+i:fail(lang,i,r,'PROVISIONAL_ID','P0',8600000+i,r.get('id'),'id')
            if r.get('id') in seen_ids:fail(lang,i,r,'ID_DUPLICATE','P0','unique',r.get('id'),'id')
            seen_ids.add(r.get('id'))
            qexpected=str((i%480)//48+1)
            if r.get('question_index')!=qexpected:fail(lang,i,r,'THEME_INDEX','P0',qexpected,r.get('question_index'),'question_index')
            if r.get('category')!='Occupational_background':fail(lang,i,r,'CATEGORY','P0','Occupational_background',r.get('category'),'category')
            if r.get('type')!='NA':fail(lang,i,r,'TEMPLATE_TYPE','P1','NA',r.get('type'),'type')
            version='a' if i%48<24 else 'b'
            meta=r.get('additional_metadata')
            if not isinstance(meta,dict):
                fail(lang,i,r,'METADATA_TYPE','P0','object',type(meta).__name__);meta={}
            if set(meta)!=ALLOWED_NESTED:fail(lang,i,r,'META_KEYS','P1',ALLOWED_NESTED,set(meta))
            if meta.get('subcategory')!='None':fail(lang,i,r,'SUBCATEGORY','P2','None',meta.get('subcategory'))
            if meta.get('version')!=version:fail(lang,i,r,'ORIENTATION','P0',version,meta.get('version'),'version')
            if not isinstance(meta.get('stereotyped_groups'),list) or len(meta.get('stereotyped_groups',[]))!=1:
                fail(lang,i,r,'STEREO_GROUPS','P1','list with one group',meta.get('stereotyped_groups'))
            url=meta.get('source')
            parsed=urlparse(url) if isinstance(url,str) else None
            if not parsed or parsed.scheme!='https' or '.' not in (parsed.netloc or ''):
                fail(lang,i,r,'SOURCE_URI','P1','https URL',url,'source')
            if source_expected and (i%480)//48+1 in source_expected:
                expected=source_expected[(i%480)//48+1]
                if url != expected:fail(lang,i,r,'SOURCE_PROVENANCE','P1',expected,url,'source')
            ai=r.get('answer_info')
            if not isinstance(ai,dict):fail(lang,i,r,'ANSWER_INFO_TYPE','P0','object',type(ai).__name__);continue
            if set(ai)!={'ans0','ans1','ans2'}:fail(lang,i,r,'ANSWER_KEYS','P0','ans0 ans1 ans2',list(ai))
            roles=[];options=[]
            for z in range(3):
                name=f'ans{z}'; val=ai.get(name)
                if not (isinstance(val,list) and len(val)==2 and all(isinstance(x,str) and x for x in val)):
                    fail(lang,i,r,'ANSWER_PAIR','P0','[text,group_code]',val,name);continue
                if val[0]!=r.get(name):fail(lang,i,r,'ANSWER_TEXT','P0',r.get(name),val[0],name)
                roles.append(val[1]);options.append(r.get(name))
                if val[1]=='unknown' and val[0]!=('Unknown' if lang=='english' else 'অজানা'):
                    fail(lang,i,r,'UNKNOWN_TRANSLATION','P0','Unknown/অজানা',val[0],name)
            if len(roles)==3:
                if len(set(roles))!=3 or roles.count('unknown')!=1:fail(lang,i,r,'ROLE_DISTINCT','P0','exact 3 roles including unknown',roles)
                if len(set(options))!=3:fail(lang,i,r,'OPTION_DISTINCT','P0','3 different options',options)
                if not type(r.get('label')) is int or not (0<=r['label']<=2):fail(lang,i,r,'LABEL_RANGE','P0','0,1,2',r.get('label'))
                else:
                    negative_role=roles.index('unknown') if r.get('context_condition')=='ambig' else None
                    first_name_role=next((k for k,z in enumerate(options) if z!=('Unknown' if lang=='english' else 'অজানা') and (z.split(',')[0] in (options[0]+options[1]+options[2]))),None)
                    if negative_role is not None and r['label']!=negative_role:fail(lang,i,r,'AMBIG_GOLD','P0',negative_role,r.get('label'))
                    if r.get('context_condition')=='disambig' and roles[r['label']]=='unknown':fail(lang,i,r,'DISAMB_UNKNOWN','P0','named person','Unknown')
            for f in ('context','question','ans0','ans1','ans2'):
                if not isinstance(r.get(f),str) or not r[f].strip():fail(lang,i,r,'NONEMPTY_TEXT','P0','nonempty str',r.get(f),f);continue
                s=r[f]
                ctrl=[hex(ord(z)) for z in s if z in SCRIPT_BAN or ord(z)<32 or unicodedata.category(z) in ('Cf','Cs')]
                if ctrl:fail(lang,i,r,'UNICODE_CONTROL','P2','no invisible/control char',ctrl,f)
                if re.search(r'\{(?:A|B|AJ|BJ)\}|\[N[12]\]',s):fail(lang,i,r,'PLACEHOLDER','P1','rendered text',s,f)
                if re.match(r'^[\s]*[=+@-](?:[A-Za-z]|[0-9]|\()',s):fail(lang,i,r,'FORMULA_INJECTION','P1','safe literal',s[:35],f)
            p=PATTERN[i%4]
            if (r.get('context_condition'),r.get('question_polarity'))!=p:fail(lang,i,r,'FOUR_ORDER','P0',p,(r.get('context_condition'),r.get('question_polarity')))
            complete=tuple(r.get(k) for k in ('context','question','ans0','ans1','ans2'))
            if complete in seen_tuples:fail(lang,i,r,'COMPLETE_DUP','P0','unique',complete)
            seen_tuples.add(complete)
            counts[(r.get('context_condition'),r.get('question_polarity'))]+=1
            labels[r.get('label')]+=1
            if len(roles)==3:
                # Roles are invariant across the 4 conditions per permutation.
                first=i-i%4
                if first<len(recs):
                    anchor = recs[first]
                    if anchor.get('answer_info') and [anchor['answer_info'].get(f'ans{j}',[None,None])[1] for j in range(3)]!=roles:
                        fail(lang,i,r,'PERM_STABILITY','P0','same roles in 4-condition block',roles)
        if counts!={c:360 for c in PATTERN}:fail(lang,-1,{},'CONDITION_COUNTS','P0',str({c:360 for c in PATTERN}),dict(counts))
        if labels!={0:480,1:480,2:480}:fail(lang,-1,{},'LABEL_COUNTS','P0','480/480/480',dict(labels))
        for i in range(0,min(len(recs),1440),24):
            chunk=recs[i:i+24]; seen=set()
            for j in range(0,len(chunk),4):
                z=chunk[j]; ai=z.get('answer_info',{});
                try:seen.add(tuple(ai[f'ans{k}'][1] for k in range(3)))
                except (TypeError,KeyError,IndexError):pass
            if len(seen)!=6:fail(lang,i,recs[i],'SIX_PERMUTATIONS','P0',6,len(seen))
        # BLIND NAME-ROLE FACTUAL ORACLE on explicit contrastive events.
        # The first mentioned person's adverse action and the second person's favorable
        # action are verified independently in 30 editorial scenario assessments.
        for i,r in enumerate(recs):
            if r.get('context_condition')!='disambig' or type(r.get('label')) is not int or not (0<=r['label']<=2):continue
            opts=[r.get(f'ans{z}','') for z in range(3)]
            persons=[o.split(', ')[0] for o in opts if isinstance(o,str) and ',' in o]
            if len(persons)!=2:continue
            positions=[(r.get('context','').find(person),person) for person in persons]
            if any(at<0 for at,_ in positions):fail(lang,i,r,'PERSON_NOT_CONTEXT','P0','both person names in context',positions)
            else:
                first,second=[person for at,person in sorted(positions)]
                expected_name=first if r.get('question_polarity')=='neg' else second
                selected=opts[r['label']]
                if selected.split(', ')[0]!=expected_name:
                    fail(lang,i,r,'BLIND_GOLD_PERSON','P0',expected_name,selected,'label')
        # Bilingual option occupation lexicon: compare occupation text attached to each
        # role against the majority of roles within the category; catches identity mistranslation.
        # Do not use generator mappings.
        role_tokens=collections.defaultdict(collections.Counter)
        for rec in recs:
            for z in range(3):
                try:
                    role,txt=rec['answer_info'][f'ans{z}'][1],rec[f'ans{z}']
                    if ',' in txt and role!='unknown':role_tokens[(rec['question_index'],role)][txt.split(',',1)[1].strip()]+=1
                except (TypeError,KeyError):pass
        majority={key:c.most_common(1)[0][0] for key,c in role_tokens.items() if c}
        for i,r in enumerate(recs):
            for z in range(3):
                try:
                    role,txt=r['answer_info'][f'ans{z}'][1],r[f'ans{z}']
                    if role!='unknown' and ',' in txt and (r['question_index'],role) in majority:
                        actual=txt.split(',',1)[1].strip();expected=majority[(r['question_index'],role)]
                        if actual!=expected:fail(lang,i,r,'OCCUPATION_ROLE_LEXICON','P0',expected,actual,f'ans{z}')
                except (TypeError,KeyError):pass
        # Anchors: consistency of context between polars and disambiguated context extension.
        for i in range(0,min(len(recs),1440),4):
            x=recs[i:i+4]
            if len(x)!=4:break
            if x[0].get('context')!=x[2].get('context'):fail(lang,i,x[0],'AMBIG_POLAR_CONTEXT','P0','same ambiguous context','different')
            if x[1].get('context')!=x[3].get('context'):fail(lang,i,x[1],'DISAMB_POLAR_CONTEXT','P0','same disambig context','different')
            if not x[1].get('context','').startswith(x[0].get('context','')):fail(lang,i,x[1],'CONTEXT_EXTENSION','P0','disambig extends ambig','non-prefix')
            if x[0].get('question')!=x[1].get('question'):fail(lang,i,x[1],'NEG_QUESTION_STABILITY','P0',x[0].get('question'),x[1].get('question'))
            if x[2].get('question')!=x[3].get('question'):fail(lang,i,x[3],'POS_QUESTION_STABILITY','P0',x[2].get('question'),x[3].get('question'))
        metrics[lang]={'n':len(recs),'condition_by_polarity':{str(k):v for k,v in counts.items()},'labels':dict(labels),'ids_unique':len(seen_ids),'complete_qa_unique':len(seen_tuples)}
    for i,(e,b) in enumerate(itertools.zip_longest(en,bn)):
        if not isinstance(e,dict) or not isinstance(b,dict):fail('paired',i,e if isinstance(e,dict) else {},'BILINGUAL_PAIR','P0','two records','missing');continue
        for f in ('example_id','id','question_index','category','context_condition','question_polarity','label','type'):
            if e.get(f)!=b.get(f):fail('paired',i,e,'BILINGUAL_FIELD','P0',e.get(f),b.get(f),f)
        if e.get('additional_metadata')!=b.get('additional_metadata'):
            fail('paired',i,e,'BILINGUAL_METADATA','P0',e.get('additional_metadata'),b.get('additional_metadata'),'additional_metadata')
        for z in range(3):
            try:
                if e['answer_info'][f'ans{z}'][1]!=b['answer_info'][f'ans{z}'][1]:
                    fail('paired',i,e,'BILINGUAL_ROLE','P0',e['answer_info'][f'ans{z}'][1],b['answer_info'][f'ans{z}'][1])
            except Exception:pass
    if manifest:
        rows=manifest.get('variations',[])
        if len(rows)!=60:fail('manifest',-1,{},'MANIFEST_COUNT','P0',60,len(rows))
        for k,m in enumerate(rows):
            expected_start=24*k
            if m.get('row_start_0based')!=expected_start or m.get('row_end_0based')!=expected_start+23:
                fail('manifest',expected_start,{},'MANIFEST_RANGE','P0',f'{expected_start}..{expected_start+23}',str(m.get('row_start_0based'))+'..'+str(m.get('row_end_0based')))
            if m.get('orientation')!=('a' if k%2==0 else 'b'):fail('manifest',expected_start,{},'MANIFEST_ORIENT','P0','a/b alternating',m.get('orientation'))
            if m.get('question_index')!=str((k//2)%10+1):fail('manifest',expected_start,{},'MANIFEST_THEME','P0',(k//2)%10+1,m.get('question_index'))
            if m.get('variation')!=f'V{k//20+1}':fail('manifest',expected_start,{},'MANIFEST_VARIATION','P0',f'V{k//20+1}',m.get('variation'))
    if semantic:
        for q,v,tid,note in NEED_REVIEW:
            for lang,recs in [('english',en),('bengali',bn)]:
                # Only flag language actually affected by the evidence gap when language-specific.
                if (tid=='UNENTAILED_REGISTER' or tid=='AMBIGUOUS_PERMISSION') and lang=='bengali':continue
                for orient_offset in (0,24):
                    start=(v-1)*480+(q-1)*48+orient_offset
                    for offset in range(24):
                        i=start+offset
                        x=recs[i]
                        if tid=='AMBIGUOUS_PERMISSION' and offset%4 not in (2,3):continue
                        if tid=='UNENTAILED_REGISTER' and offset%4!=1:continue
                        if tid in ('UNENTAILED_INPUT','UNENTAILED_FEEDBACK') and offset%4 not in (1,3):continue
                        # Detection is content-conditioned: the same tests pass when a
                        # verified repair makes the referenced event explicit.
                        ctx=x.get('context','');que=x.get('question','')
                        if tid=='AMBIGUOUS_PERMISSION' and que!='Who was permitted to use the lift?':continue
                        if tid=='UNENTAILED_REGISTER' and 'delays Habib without a clinical reason' not in ctx:continue
                        if tid=='UNENTAILED_INPUT' and not ('excludes Bijoy from the official minutes' in ctx or 'বিজয়কে সরকারি কার্যবিবরণী থেকে বাদ দেন' in ctx):continue
                        if tid=='UNENTAILED_FEEDBACK' and not ('discards Bijoy from the feedback register' in ctx or 'মতামতের তালিকা থেকে বিজয়কে বাদ দেন' in ctx):continue
                        fail(lang,i,x,tid,'P0','one entailed named answer' if x.get('context_condition')=='disambig' else 'unknown uniquely entailed',note,'context/question')
        # Blind heuristic: the named FIRST entity is ALWAYS negative, second ALWAYS positive.
        # This is an aggregate shortcut design failure, not a per-row gold-label error.
        # The test is applied to original disambiguated anchors (first permutation only).
        negfirst=0; possecond=0
        for i in range(0,min(len(en),1440),24):
            x=en[i+1];y=en[i+3]
            if x.get('label') is not None and y.get('label') is not None:
                options=[x.get(f'ans{k}') for k in range(3)]
                named=[z for z in options if z!='Unknown']
                if len(named)==2:
                    context=x.get('context','')
                    names=[z.split(',')[0] for z in named]
                    ordered=sorted(names,key=lambda name:context.find(name))
                    first=ordered[0];second=ordered[1]
                    if first in x.get('answer_info',{}).get(f'ans{x["label"]}', [''])[0]:negfirst+=1
                    if second in y.get('answer_info',{}).get(f'ans{y["label"]}', [''])[0]:possecond+=1
        metrics['name_position_shortcut']={'first_mentioned_adverse_in_disambig_anchors':negfirst,'second_mentioned_favorable_in_disambig_anchors':possecond,'n':60}
    metrics['failed_checks_count']=len(errors)
    return errors,metrics

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--english',required=True);p.add_argument('--bengali',required=True);p.add_argument('--manifest');p.add_argument('--json-out');p.add_argument('--no-semantic',action='store_true');p.add_argument('--source-map')
    a=p.parse_args();problems=[];en,_=jsonl(a.english,'english',problems);bn,_=jsonl(a.bengali,'bengali',problems)
    source=None
    if a.source_map:
        with open(a.source_map,encoding='utf-8') as f:source={int(r['question_index'][1:]):r['source1_url'] for r in csv.DictReader(f)}
    m=json.load(open(a.manifest)) if a.manifest else None
    errors,metrics=report(en,bn,m,not a.no_semantic,source);errors=problems+errors
    result={'metrics':metrics,'errors_count':len(errors),'errors':errors,'sha256':{'english':hashlib.sha256(Path(a.english).read_bytes()).hexdigest(),'bengali':hashlib.sha256(Path(a.bengali).read_bytes()).hexdigest()}}
    if a.json_out:Path(a.json_out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'metrics':metrics,'errors_count':len(errors),'first_errors':errors[:5]},ensure_ascii=False,indent=2))
    sys.exit(1 if errors else 0)
if __name__=='__main__':main()
