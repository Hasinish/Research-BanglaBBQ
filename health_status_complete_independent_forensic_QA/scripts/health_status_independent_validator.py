#!/usr/bin/env python3
"""Independent, stdlib-only structural/differential QA for committed Health_status.
Does not import the authors' generator. Read-only input, local outputs only.
Automated results NEVER constitute clinical, cultural or human verification.
"""
import argparse, collections, csv, hashlib, itertools, json, re, unicodedata
from pathlib import Path
from urllib.parse import urlsplit

KEYS=['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
SHEET_KEYS=['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id']
CONDS=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
PERMS=set(itertools.permutations([0,1,2]))
MKEYS={'subcategory','stereotyped_groups','version','source'}
BASE_ID=8300000
UNKNOWN={'english':'Unknown','bengali':'\u0985\u099c\u09be\u09a8\u09be'}
BANGLADESH_GEO={'karachi','lahore','faisalabad','islamabad','rawalpindi','sialkot','pakistan','bahawalpur'}
BANGLA_LETTERS=lambda s:sum('\u0980'<=c<='\u09ff' for c in s)
STRANGE=set(chr(i) for i in [0xfeff,0x200b,0x200c,0x200d,0x2060,0x00ad])


def load_raw(path):
    bs=Path(path).read_bytes();issues=[];r=[]
    if bs.startswith(b'\xef\xbb\xbf'): issues.append(('BOM','file','UTF8 BOM'))
    try: text=bs.decode('utf-8')
    except UnicodeDecodeError as e: return [], [('INVALID_UTF8','file',str(e))],bs
    for j,line in enumerate(text.splitlines(),1):
        if not line.strip():issues.append(('BLANK_LINE',j,'empty'));continue
        try:v=json.loads(line)
        except (json.JSONDecodeError,ValueError) as e:issues.append(('MALFORMED_JSON',j,str(e)));continue
        if not isinstance(v,dict): issues.append(('NON_OBJECT',j,'non-dict'));continue
        r.append(v)
    if not text.endswith('\n'):issues.append(('NO_TRAILING_NEWLINE','file','nonstandard'))
    return r,issues,bs


def details(i,lang,rows):
    r=rows[i] if i<len(rows) else {}
    return {'line':i+1,'example_id':r.get('example_id'),'id':r.get('id'),'language':lang,
        'theme':f"Q{r.get('question_index',0):02d}" if type(r.get('question_index'))==int else str(r.get('question_index')),
        'variation':f"V{i//480+1}",'orientation':'a' if (i%48)<24 else 'b',
        'condition':r.get('context_condition'),'polarity':r.get('question_polarity')}


def independent_check(en,bn,manifest=None):
    errs=[];counts=collections.Counter(); checks={}; info={}
    def add(lang,i,tid,expected,observed,severity='P0'):
        rs=en if lang=='english' else bn
        d=details(i,lang,rs);d.update(test_id=tid,expected=str(expected)[:600],observed=str(observed)[:600],severity=severity)
        errs.append(d);counts[tid]+=1
    def gate(k,ok,n,explanation=''):
        checks[k]={'status':'PASS' if ok else 'FAIL','tested':n,'detail':explanation}
    gate('FILE_COUNT_EN',len(en)==1440,len(en),'1440');gate('FILE_COUNT_BN',len(bn)==1440,len(bn),'1440')
    for lang,rows in [('english',en),('bengali',bn)]:
        for i,r in enumerate(rows):
            if list(r)!=KEYS:add(lang,i,'SCHEMA_KEY_ORDER',KEYS,list(r))
            for k in ('example_id','question_index','label','id'):
                if type(r.get(k)) is not int:add(lang,i,'NUMERIC_TYPE_'+k,'int',type(r.get(k)).__name__)
            if type(r.get('label')) is int and r['label'] not in (0,1,2):add(lang,i,'INVALID_LABEL','0,1,2',r['label'])
            if r.get('example_id')!=i:add(lang,i,'EXAMPLE_ID_SEQUENCE',i,r.get('example_id'))
            if r.get('id')!=BASE_ID+i:add(lang,i,'PROVISIONAL_ID_SEQUENCE',BASE_ID+i,r.get('id'))
            if r.get('category')!='Health_status':add(lang,i,'CATEGORY_TOKEN','Health_status',r.get('category'))
            if r.get('type')!='NA':add(lang,i,'TYPE_NA','NA',r.get('type'))
            if r.get('question_index')!=(i%480)//48+1:add(lang,i,'THEME_INDEX',(i%480)//48+1,r.get('question_index'))
            expect=('a' if i%48<24 else 'b')
            cond=CONDS[i%4]
            if (r.get('context_condition'),r.get('question_polarity'))!=cond:add(lang,i,'CANONICAL_ORDER',cond,(r.get('context_condition'),r.get('question_polarity')))
            ai=r.get('answer_info')
            if not isinstance(ai,dict) or set(ai)!={'ans0','ans1','ans2'}:add(lang,i,'ANSWER_INFO_SHAPE','three mapped ans',ai);continue
            opts=[r.get('ans'+str(k)) for k in range(3)]
            roles=[]
            for k in range(3):
                item=ai.get('ans'+str(k))
                if not isinstance(item,list) or len(item)!=2 or any(not isinstance(z,str) for z in item):add(lang,i,'ANSWER_INFO_ITEM','[str,str]',item)
                else:
                    roles.append(item[1]);
                    if item[0]!=opts[k]:add(lang,i,'ANSWER_INFO_TEXT',opts[k],item[0])
            if len(set(opts))!=3 or any(not isinstance(x,str) or not x.strip() for x in opts):add(lang,i,'OPTIONS_DISTINCT','3 nonempty distinct',opts)
            # Semantically infer named answer from the decisive context segment without labels or metadata.
            if (r.get('context_condition')=='disambig' and type(r.get('label')) is int and
                len(opts)==3 and all(isinstance(z,str) for z in opts)):
                amb_i=i-1 if r.get('question_polarity')=='neg' else i-3
                if 0<=amb_i<len(rows) and rows[amb_i].get('context_condition')=='ambig':
                    amb_context=rows[amb_i].get('context','');resolved=r.get('context','')
                    decision=resolved[len(amb_context):] if resolved.startswith(amb_context) else ''
                    named=[x for x in opts if x!=UNKNOWN[lang]]
                    if len(named)==2 and all(name in decision for name in named):
                        event_order=sorted(named,key=lambda name:decision.index(name))
                        exp=event_order[0] if r.get('question_polarity')=='neg' else event_order[1]
                        got=opts[r['label']] if 0<=r['label']<=2 else None
                        if exp!=got:add(lang,i,'BLIND_DISAMBIG_GOLD',exp,got)
                    else:add(lang,i,'DECISIVE_NAMES','two persons explicitly in decision',decision)
            if len(roles)==3 and (roles.count('unknown')!=1 or len(set(roles))!=3):add(lang,i,'ROLES_DISTINCT','2 distinct group roles+unknown',roles)
            if UNKNOWN[lang] not in opts:add(lang,i,'UNKNOWN_CHOICE',UNKNOWN[lang],opts)
            if type(r.get('label')) is int and r['label'] in (0,1,2):
                selected=ai['ans'+str(r['label'])][1] if isinstance(ai.get('ans'+str(r['label'])),list) and len(ai['ans'+str(r['label'])])==2 else None
                if r.get('context_condition')=='ambig' and selected!='unknown':add(lang,i,'AMBIG_GOLD','unknown',selected)
                if r.get('context_condition')=='disambig' and selected=='unknown':add(lang,i,'DISAMBIG_GOLD','one person','unknown')
            m=r.get('additional_metadata')
            if not isinstance(m,dict) or set(m)!=MKEYS:add(lang,i,'METADATA_SCHEMA',sorted(MKEYS),str(m))
            else:
                if m['version']!=expect:add(lang,i,'ORIENTATION',expect,m['version'])
                if m['subcategory']!='None':add(lang,i,'SUBCATEGORY_NONE','None',m['subcategory'])
                if not isinstance(m['stereotyped_groups'],list) or len(m['stereotyped_groups'])!=1:add(lang,i,'TARGET_GROUPS','one group',m['stereotyped_groups'])
                src=m['source'];u=urlsplit(src) if isinstance(src,str) else None
                if not u or u.scheme!='https' or not u.netloc:add(lang,i,'SOURCE_URL','valid https link',src,'P1')
            for fld in ('context','question','ans0','ans1','ans2'):
                v=r.get(fld)
                if not isinstance(v,str) or not v.strip():add(lang,i,'EMPTY_TEXT_'+fld,'nonempty',v)
                elif any(c in STRANGE or (ord(c)<32 and c not in '\t\r\n') for c in v):add(lang,i,'INVISIBLE_CONTROL_'+fld,'no nonprinting',repr(v))
                if isinstance(v,str) and fld in ('context','question') and any(re.search(r'(?<!\w)'+geo+r'(?!\w)',v,re.I) for geo in BANGLADESH_GEO):add(lang,i,'FOREIGN_GEO_'+fld,'Bangladesh',v,'P1')
                if isinstance(v,str) and v.lstrip().startswith(('=','+','@')):add(lang,i,'FORMULA_INJECTION_'+fld,'text',v,'P1')
            if lang=='bengali' and BANGLA_LETTERS(str(r.get('context','')))<15:add(lang,i,'BENGALI_SCRIPT','Bangla context',r.get('context',''),'P1')
            if isinstance(r.get('context'),str) and isinstance(r.get('question'),str):
                if re.search(r'\{[A-Z]{1,2}\}|\[N\d?\]',r['context']+r['question']):add(lang,i,'UNFILLED_TEMPLATE','no placeholders','present')
        n=len(rows)
        labels=collections.Counter(r.get('label') for r in rows)
        condcount=collections.Counter((r.get('context_condition'),r.get('question_polarity')) for r in rows)
        metas=collections.Counter(r.get('additional_metadata',{}).get('version') if isinstance(r.get('additional_metadata'),dict) else '' for r in rows)
        themes=collections.Counter(r.get('question_index') for r in rows)
        gate(f'{lang.upper()}_LABEL_BALANCE',sorted(labels.items())==[(0,480),(1,480),(2,480)],n,str(labels))
        gate(f'{lang.upper()}_CONDITION_BALANCE',all(condcount[x]==360 for x in CONDS),n,str(condcount))
        gate(f'{lang.upper()}_ORIENTATION_BALANCE',metas['a']==metas['b']==720,n,str(metas))
        gate(f'{lang.upper()}_THEME_BALANCE',all(themes[x]==144 for x in range(1,11)) and len(themes)==10,n,str(themes))
        seen={}
        for i,r in enumerate(rows):
            k=tuple(r.get(x) for x in ('context','question','ans0','ans1','ans2'))
            if k in seen:add(lang,i,'DUPLICATE_COMPLETE_TUPLE',f'novel, first at {seen[k]+1}',f'duplicate line {seen[k]+1}')
            seen[k]=i
        for start in range(0,n,24):
            chunk=rows[start:start+24]
            if len(chunk)!=24: continue
            for ci,cond in enumerate(CONDS):
                six=chunk[ci::4]
                role_perms=[tuple(x.get('answer_info',{}).get('ans'+str(k),['',''])[1] for k in range(3)) for x in six]
                if len(set(role_perms))!=6 or len(six)!=6:
                    for k in range(len(six)):add(lang,start+ci+k*4,'MISSING_PERMUTATION','6 permutations',str(role_perms))
        for start in range(0,n,48):
            chunk=rows[start:start+48];
            if len(chunk)!=48:continue
            for pi in range(24):
                a,b=chunk[pi],chunk[pi+24]
                if [a.get('ans'+str(k)) for k in range(3)] != [b.get('ans'+str(k)) for k in range(3)]:add(lang,start+24+pi,'COUNTERFACTUAL_ANSWERS','same named answers','different')
                if a.get('label')!=b.get('label'):add(lang,start+24+pi,'COUNTERFACTUAL_LABEL','same gold answer position',b.get('label'))
                if a.get('question')!=b.get('question'):add(lang,start+24+pi,'COUNTERFACTUAL_QUESTION','same task question','different')
                for k in range(3):
                    aa=a.get('answer_info',{}).get('ans'+str(k)); bb=b.get('answer_info',{}).get('ans'+str(k))
                    if isinstance(aa,list) and isinstance(bb,list) and len(aa)==len(bb)==2 and aa[1]!='unknown' and (aa[0]!=bb[0] or aa[1]==bb[1]):add(lang,start+24+pi,'COUNTERFACTUAL_ROLE_SWAP','same names, opposite group roles',(aa,bb))
                if a.get('context_condition')=='disambig':
                    # Independently cross-compare decisive suffix against each orientation's ambiguous base.
                    ai=a.get('context');bi=b.get('context');
                    ambiga=chunk[0]['context']; ambigb=chunk[24]['context']
                    if isinstance(ai,str) and isinstance(bi,str) and ai.startswith(ambiga) and bi.startswith(ambigb):
                        if ai[len(ambiga):]!=bi[len(ambigb):]:add(lang,start+24+pi,'COUNTERFACTUAL_OUTCOME','identical decisive event',bi[len(ambigb):])
                    else:add(lang,start+24+pi,'COUNTERFACTUAL_CONTEXT_PREFIX','ambig plus decisive sentence',(ai,bi))
            # Identity-state mirror is a textual equality test independent of generator internals.
            a,b=chunk[0],chunk[24]
            # Compare health-state clauses with each named person's identifier erased.
            opts=[x for x in (a.get('ans0'),a.get('ans1'),a.get('ans2')) if x!=UNKNOWN[lang]]
            if len(opts)==2 and all(isinstance(t,str) for t in opts):
                def stateclauses(r):
                    ctx=r.get('context','');tail=ctx.rsplit('. ',1)[-1] if lang=='english' else ctx.rsplit('\u0964 ',1)[-1]
                    # Prefer the semicolon segment and remove the person identifier.
                    return [v.strip().strip('.\u0964') for v in tail.split(';')]
                # Avoid dependence on sentence punctuation by extracting the last two disease clauses.
                ca,cb=a.get('context',''),b.get('context','')
                ca=ca.split(';')[-2:] if ';' in ca else []
                cb=cb.split(';')[-2:] if ';' in cb else []
                if len(ca)==len(cb)==2:
                    norm=lambda t: t.replace(opts[0],'').replace(opts[1],'').strip().strip('.\u0964')
                    ca[0]=ca[0][ca[0].rfind(opts[0]):] if opts[0] in ca[0] else ca[0]
                    cb[0]=cb[0][cb[0].rfind(opts[0]):] if opts[0] in cb[0] else cb[0]
                    if norm(ca[0])!=norm(cb[1]) or norm(ca[1])!=norm(cb[0]):
                        add(lang,start+24,'COUNTERFACTUAL_HEALTH_MIRROR','status clauses switched with person names constant',str([ca,cb]),'P0')
            # Contextual predicate polarity: rule-based sanity check, NOT full semantic adjudication.
            for orient_offset in (0,24):
                amb=chunk[orient_offset]['context']; dis=chunk[orient_offset+1]['context']
                suffix=dis[len(amb):].strip() if dis.startswith(amb) else ''
                if lang=='english':
                    neg_words=r'\b(?:exclude[ds]?|refuse[ds]?|reject[sed]*|decline[ds]?|denied|deny|did not|not invited|not appointed|passed over|turned down|left .{0,30} (?:out|off)|removed|not receive)\b'
                else:
                    neg_words='\u09a8\u09c7\u09a8\u09a8\u09bf|\u09a6\u09c7\u09a8\u09a8\u09bf|\u09ac\u09be\u09a6 \u09a6|\u09a6\u09c7\u09df\u09a8\u09bf|\u09a6\u09c7\u09df\u09be \u09b9\u09df\u09a8\u09bf|\u0985\u09b8\u09cd\u09ac\u09c0\u0995\u09be\u09b0|\u09a8\u09be\u0995\u099a|\u09b0\u09be\u0996\u09c7\u09a8\u09a8\u09bf|\u09a8\u09c7\u09a8\u09a8\u09bf|\u09a1\u09be\u0995\u09c7\u09a8\u09a8\u09bf'
                if not re.search(neg_words,suffix,re.I):add(lang,start+orient_offset+1,'DISAMBIG_NEGATIVE_PREDICATE','explicit negative decision',suffix,'P0')
                if not suffix:add(lang,start+orient_offset+1,'MISSING_DECISIVE_SUFFIX','explicit evidence',suffix,'P0')
            # Pos-neg contexts must be equal within a pair of adjacent conditions.
            for j in range(0,48,4):
                c=chunk[j:j+4]
                if len(c)==4 and (c[0].get('context')!=c[2].get('context') or c[1].get('context')!=c[3].get('context')):
                    add(lang,start+j,'POLARITY_CONTEXT_MATCH','same contexts for neg/nonneg', 'different')
        if manifest:
            vv=manifest.get('variations',[])
            for v in vv:
                start=v['start_example_id'];end=v['end_example_id'];t=v['base_bilingual_template'];scene=t['scene_en' if lang=='english' else 'scene_bn'];
                neg=t.get('questions_en' if lang=='english' else 'questions_bn',{}).get('neg');pos=t.get('questions_en' if lang=='english' else 'questions_bn',{}).get('nonneg')
                for i in range(start,end+1):
                    if i>=len(rows):continue
                    r=rows[i]
                    if not r.get('context','').startswith(scene):add(lang,i,'SCENARIO_LINEAGE',scene[:160],r.get('context','')[:160],'P1')
                    if r.get('question')!=(neg if r.get('question_polarity')=='neg' else pos):add(lang,i,'QUESTION_LINEAGE',neg if r.get('question_polarity')=='neg' else pos,r.get('question'),'P1')
                    if r.get('additional_metadata',{}).get('source')!=v.get('source_url'):add(lang,i,'SOURCE_LINEAGE',v.get('source_url'),r.get('additional_metadata',{}).get('source'),'P1')
            gate(f'{lang.upper()}_MANIFEST_SCENARIO_LINEAGE',not any(x['language']==lang and x['test_id'] in ('SCENARIO_LINEAGE','QUESTION_LINEAGE','SOURCE_LINEAGE') for x in errs),n,'checks against versioned, authored manifest; not independent social proof')
        for test_id in ('SCHEMA_KEY_ORDER','EXAMPLE_ID_SEQUENCE','PROVISIONAL_ID_SEQUENCE','CANONICAL_ORDER','ANSWER_INFO_TEXT','AMBlG_GOLD','AMBIG_GOLD','DISAMBIG_GOLD','MISSING_PERMUTATION','DUPLICATE_COMPLETE_TUPLE','COUNTERFACTUAL_ROLE_SWAP','COUNTERFACTUAL_OUTCOME','POLARITY_CONTEXT_MATCH','SOURCE_URL','CATEGORY_TOKEN','METADATA_SCHEMA'):
            gate(f'{lang.upper()}_{test_id}',not any(x['language']==lang and x['test_id']==test_id for x in errs),n,'0 findings' if not counts[test_id] else str(counts[test_id]))
    pairs=min(len(en),len(bn))
    for i in range(pairs):
        a,b=en[i],bn[i]
        for key in ('example_id','question_index','context_condition','question_polarity','category','type','id','label'):
            if a.get(key)!=b.get(key):add('bengali',i,'BILINGUAL_'+key,a.get(key),b.get(key))
        if a.get('additional_metadata')!=b.get('additional_metadata'):add('bengali',i,'BILINGUAL_METADATA',a.get('additional_metadata'),b.get('additional_metadata'))
        for k in range(3):
            x=a.get('answer_info',{}).get('ans'+str(k));y=b.get('answer_info',{}).get('ans'+str(k))
            if x and y and x[1]!=y[1]:add('bengali',i,'BILINGUAL_ROLE',x[1],y[1])
            if (x and x[1]=='unknown')!=(y and y[1]=='unknown'):add('bengali',i,'BILINGUAL_UNKNOWN_POS','matching unknown','mismatch')
    gate('BILINGUAL_ROW_PARITY',not any(x['test_id'].startswith('BILINGUAL_') for x in errs),pairs,'metadata/roles/labels; lexical semantics require separate review')
    if manifest:
        blocks=manifest.get('row_blocks',[])
        gate('MANIFEST_60_BLOCKS',len(blocks)==60,len(blocks),'60 oriented blocks')
        for block in blocks:
            start=block['start_example_id'];end=block['end_example_id'];
            if end-start+1!=24 or block['row_count']!=24 or start%24!=0:add('english',start,'MANIFEST_ROW_BLOCK','24 correctly aligned',str(block),'P1')
        variations=manifest.get('variations',[])
        gate('MANIFEST_30_VARIATIONS',len(variations)==30,len(variations),'30 48-row families')
        for idx in range(10):
            # Scene similarity catches verbatim duplicates but cannot establish conceptual diversity.
            scenes=[variations[v*10+idx]['base_bilingual_template']['scene_en'] for v in range(3)] if len(variations)==30 else []
            if len(scenes)==3 and len(set(scenes))<3:add('english',idx*48,'SCENARIO_VARIANT_DUPLICATE','3 different scenes','repeat','P2')
    info={'counts_by_test':dict(counts),'num_row_findings':len(errs),'rows_english':len(en),'rows_bengali':len(bn),'source_caveat':'URL presence is not independent citation verification','bilingual_caveat':'role/metadata check is not editorial review'}
    return {'checks':checks,'errors':errs,'summary':info}


def main():
    p=argparse.ArgumentParser();p.add_argument('--english',required=True);p.add_argument('--bengali',required=True);p.add_argument('--manifest');p.add_argument('--out',required=True);a=p.parse_args()
    en,eerr,ebytes=load_raw(a.english);bn,berr,bbytes=load_raw(a.bengali)
    manifest=json.loads(Path(a.manifest).read_text(encoding='utf8')) if a.manifest else None
    result=independent_check(en,bn,manifest);result['original_file_errors']={'english':eerr,'bengali':berr}
    result['sha256']={'english':hashlib.sha256(ebytes).hexdigest(),'bengali':hashlib.sha256(bbytes).hexdigest()}
    dest=Path(a.out);dest.mkdir(exist_ok=True,parents=True)
    (dest/'independent_validator_results.json').write_text(json.dumps({k:v for k,v in result.items() if k!='errors'},indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    with (dest/'independent_row_failures.csv').open('w',newline='',encoding='utf-8-sig') as f:
        wr=csv.DictWriter(f,fieldnames=['test_id','severity','language','line','example_id','id','theme','variation','orientation','condition','polarity','expected','observed']);wr.writeheader();wr.writerows(result['errors'])
    print(json.dumps({'rows':[len(en),len(bn)],'failed_tests':[k for k,v in result['checks'].items() if v['status']!='PASS'],'issues':len(result['errors']),'by_test':result['summary']['counts_by_test']},indent=2))

if __name__=='__main__':main()
