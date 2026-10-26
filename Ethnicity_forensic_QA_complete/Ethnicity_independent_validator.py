#!/usr/bin/env python3
"""New independent forensic validator for the BanglaBBQ Ethnicity GitHub snapshot.

Reads saved JSONL and provenance. It DOES NOT import or execute the generator.
Separately infers labels from disambiguated textual clauses and the question,
BEFORE consulting gold labels. It also checks bilingual pairs, identity swaps,
combinatorics, and predictable failure signatures. It is not a substitute for
source review or human native-language adjudication.
"""
import argparse
import collections
import csv
import hashlib
import itertools
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

KEYS=('example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id')
CONDITIONS=(('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg'))
META=('subcategory','stereotyped_groups','version','source')
TEXT=('context','question','ans0','ans1','ans2')
CONTROL=re.compile(r'[\u200b-\u200f\ufeff\u202a-\u202e\x00-\x08\x0b\x0c\x0e-\x1f]')
ORIGINAL_START=8500000
GROUP_MAP={'munda':'মুণ্ডা','chakma':'চাকমা','garo_mandi':'গারো (মান্দি)','santal':'সাঁওতাল','mro':'ম্রো','marma':'মারমা','ethnic_bengali':'বাঙালি'}
PAK_CARRYOVER=re.compile(r'\b(?:Karachi|Lahore|Rawalpindi|Islamabad|InDrive|Pakistani)\b|করাচি|লাহোর|ইসলামাবাদ|রাওয়ালপিন্ডি',re.IGNORECASE)
MAX_ISSUES=25000


def load_jsonl(path, language, add):
    if not pathlib.Path(path).is_file():
        add('FILE_MISSING',language,-1,'file','present',str(path),'P0')
        return []
    data=[]
    raw=pathlib.Path(path).read_bytes()
    try: text=raw.decode('utf-8','strict')
    except UnicodeDecodeError as e:
        add('FILE_UTF8',language,-1,'file','valid UTF8',str(e),'P0');return []
    if text.startswith('\ufeff'):
        add('FILE_BOM',language,0,'file','no BOM','BOM present','P0')
    if raw and not raw.endswith(b'\n'):
        add('FILE_NEWLINE',language,-1,'file','newline terminated','not terminated','P2')
    for i,line in enumerate(text.splitlines()):
        if not line.strip():
            add('BLANK_LINE',language,i,'JSONL','JSON object','blank line','P0')
            data.append(None)
            continue
        if CONTROL.search(line):
            add('CONTROL_CHAR',language,i,'JSONL','no zero-width/control chars',repr(CONTROL.search(line).group(0)),'P0')
        try: x=json.loads(line)
        except Exception as e:
            add('MALFORMED_JSON',language,i,'JSONL','valid object',str(e),'P0');x=None
        data.append(x)
    return data


def answer_entity(x,pos,lang):
    a=x.get(f'ans{pos}')
    if not isinstance(a,str):return 'INVALID'
    if a in ('Unknown','অজানা','তথ্য অপর্যাপ্ত'):return 'U'
    # Entity letters A/B are matched from answer strings, not metadata.
    if lang=='en':
        if a.endswith(' A'):return 'A'
        if a.endswith(' B'):return 'B'
    else:
        if a.endswith(' ক'):return 'A'
        if a.endswith(' খ'):return 'B'
    return 'INVALID'


def extract_predicates(context,lang):
    """Return contextual outcome clauses and a reason, with NO gold label access."""
    if lang=='en':
        if ' recorded that ' not in context or ', whereas ' not in context:
            return None,'no explicit independent A/B reporting clauses'
        tail=context.rsplit(' recorded that ',1)[-1]
        a,b=tail.split(', whereas ',1)
        a_match=re.search(r'\bA\s+(.+)$',a)
        b_match=re.search(r'\bB\s+(.+?)\.?$',b)
    else:
        if ' জানান, ' not in context or '; অন্যদিকে ' not in context:
            return None,'no explicit independent Bengali A/B reporting clauses'
        tail=context.rsplit(' জানান, ',1)[-1]
        a,b=tail.split('; অন্যদিকে ',1)
        a_match=re.search(r' ক\s+(.+)$',a)
        b_match=re.search(r' খ\s+(.+?)।?$',b)
    if not a_match or not b_match:return None,'A/B agent or patient missing'
    return (a_match.group(1).rstrip(' .।'),b_match.group(1).rstrip(' .।')),'EXPLICIT'


def blind_infer(x,lang):
    """Blind answer inference using only the displayed context/question/options.

    Does NOT access x['label'], version or source; infer role from explicit clauses.
    """
    ctx=x.get('context','');q=x.get('question','')
    if not isinstance(ctx,str) or not isinstance(q,str):return 'INVALID','missing text',None
    pred,reason=extract_predicates(ctx,lang)
    if pred is None:
        # Context without explicit outcomes: a stereotype is not evidence.
        # If ambiguous text literally includes a question outcome applied to A/B,
        # treat it as a leak rather than assuming Unknown.
        pat='was ' if lang=='en' else 'পায়নি'
        if ' recorded that ' in ctx or ' জানান, ' in ctx:
            return 'INVALID','partially disambiguating evidence',None
        if lang=='en':
            m=re.search(r'\b(?:was|received)\s+(.+)\?',q)
            core=m.group(0)[:-1] if m else ''
            if core and ((' A '+core in ctx) or (' B '+core in ctx)):
                return 'INVALID','outcome leaked into ambiguous context',None
        return 'U','no decisive outcome for either entity',None
    a,b=pred
    q=q.rstrip(' ?।')
    hits=[]
    if q.endswith(a):hits.append('A')
    if q.endswith(b):hits.append('B')
    if len(hits)==1:return hits[0],'exact predicate directly entailed',pred
    return 'INVALID',f'question outcome does not uniquely match explicit clauses; A={a!r}, B={b!r}',pred


def validate(en_path,bn_path,manifest_path=None,source_path=None,templates_path=None):
    issues=[]
    counts=collections.Counter()
    def add(t,lang,i,field,expected,observed,severity='P1'):
        if len(issues)>=MAX_ISSUES:return
        issues.append({'test_id':t,'language':lang,'row_index':i,'line_number':i+1 if i>=0 else '',
                       'offending_field':field,'expected':str(expected),'observed':str(observed),'severity':severity})
    R={'en':load_jsonl(en_path,'en',add),'bn':load_jsonl(bn_path,'bn',add)}
    sources={}
    if source_path and pathlib.Path(source_path).exists():
        with open(source_path,encoding='utf-8',newline='') as f:
            for row in csv.DictReader(f):
                k=row.get('theme_id','');sources[k]=row.get('source_1_url','')
        if len(sources)!=10:add('SOURCE_AUDIT_COUNT','both',-1,'source_audit',10,len(sources),'P1')
        for q,u in sources.items():
            if urlparse(u).scheme!='https' or not urlparse(u).netloc:
                add('SOURCE_AUDIT_MISSING_URL','both',-1,q,'valid source URL',u,'P1')
    manifest=None
    if manifest_path and pathlib.Path(manifest_path).is_file():
        try:manifest=json.loads(pathlib.Path(manifest_path).read_text(encoding='utf-8'))
        except Exception as e:add('MANIFEST_JSON','both',-1,'manifest','valid',e,'P1')
    for lang,rows in R.items():
        if len(rows)!=1440:add('TOTAL_RECORD_COUNT',lang,-1,'rows',1440,len(rows),'P0')
        seen_ids=set();seen_qa={};themes=collections.Counter();conds=collections.Counter();gold=collections.Counter();versions=collections.Counter()
        for i,x in enumerate(rows):
            counts[f'{lang}_parsed_or_attempted_rows']+=1
            if not isinstance(x,dict):continue
            if tuple(x)!=KEYS:add('KEY_ORDER_SCHEMA',lang,i,'keys',KEYS,tuple(x),'P0')
            for field,kind in [('example_id',int),('id',int),('label',int),('question_index',str),('category',str),('question_polarity',str),('context_condition',str),('type',str),('answer_info',dict),('additional_metadata',dict)]:
                if type(x.get(field)) is not kind:add('SCHEMA_TYPE',lang,i,field,kind.__name__,type(x.get(field)).__name__,'P0')
            for field in TEXT:
                val=x.get(field)
                if not isinstance(val,str) or not val.strip():add('TEXT_NONEMPTY',lang,i,field,'nonempty string',repr(val),'P0')
                if isinstance(val,str) and CONTROL.search(val):add('TEXT_CONTROL',lang,i,field,'no controls',repr(val),'P0')
                if lang=='bn' and isinstance(val,str) and re.search('[A-Za-z]',val):add('BENGALI_ENGLISH_LEAK',lang,i,field,'Bengali prose only',val[:140],'P2')
                if isinstance(val,str) and PAK_CARRYOVER.search(val):add('PAKISTANI_CULTURAL_LEAK',lang,i,field,'Bangladesh scenario only',val[:180],'P1')
                if isinstance(val,str) and re.match(r'^[=+@\t\r]',val):add('SPREADSHEET_FORMULA_INJECTION',lang,i,field,'safe first character',val[:30],'P0')
            eid=x.get('example_id');idnum=x.get('id')
            if eid!=i:add('EXAMPLE_ID_SEQUENCE',lang,i,'example_id',i,eid,'P0')
            if idnum!=ORIGINAL_START+i:add('RESERVED_ID_SEQUENCE',lang,i,'id',ORIGINAL_START+i,idnum,'P0')
            if idnum in seen_ids:add('DUPLICATE_ID',lang,i,'id','unique',idnum,'P0')
            seen_ids.add(idnum)
            if x.get('category')!='Ethnicity':add('CATEGORY_TOKEN',lang,i,'category','Ethnicity',x.get('category'),'P1')
            if x.get('type')!='NA':add('TEMPLATE_TYPE',lang,i,'type','NA',x.get('type'),'P1')
            if x.get('question_index') not in set(map(str,range(1,11))):add('QUESTION_INDEX_RANGE',lang,i,'question_index','1..10',x.get('question_index'),'P0')
            if x.get('question_polarity') not in ('neg','nonneg'):add('POLARITY_ENUM',lang,i,'question_polarity','neg/nonneg',x.get('question_polarity'),'P0')
            if x.get('context_condition') not in ('ambig','disambig'):add('CONTEXT_ENUM',lang,i,'context_condition','ambig/disambig',x.get('context_condition'),'P0')
            themes[x.get('question_index')]+=1
            conds[(x.get('context_condition'),x.get('question_polarity'))]+=1
            gold[x.get('label')]+=1
            ai=x.get('answer_info',{})
            if not isinstance(ai,dict):ai={}
            if set(ai)!=set(('ans0','ans1','ans2')):add('ANSWERINFO_KEYS',lang,i,'answer_info',('ans0','ans1','ans2'),list(ai),'P0')
            tags=[]
            for pos in range(3):
                val=ai.get(f'ans{pos}')
                if not isinstance(val,list) or len(val)!=2 or not all(isinstance(z,str) for z in val):
                    add('ANSWERINFO_SHAPE',lang,i,f'answer_info.ans{pos}','[text, role]',val,'P0');continue
                tags.append(val[1])
                if val[0]!=x.get(f'ans{pos}'):add('ANSWERINFO_TEXT_PARITY',lang,i,f'answer_info.ans{pos}',x.get(f'ans{pos}'),val[0],'P0')
            if len(tags)==3 and (len(set(tags))!=3 or tags.count('unknown')!=1):add('ANSWER_ROLES_COLLIDE',lang,i,'answer_info.tags','three unique including unknown',tags,'P0')
            forms=[x.get(f'ans{j}') for j in range(3)]
            if len(set(forms))!=3:add('DUPLICATE_OPTIONS',lang,i,'ans0..2','three different options',forms,'P0')
            entities=tuple(answer_entity(x,j,lang) for j in range(3))
            if set(entities)!={'A','B','U'}:add('ANSWER_ENTITY_IDENTIFICATION',lang,i,'ans0..2','A/B/Unknown',entities,'P0')
            if isinstance(x.get('label'),int) and 0<=x['label']<=2:
                goldentity=entities[x['label']]
            else:
                goldentity='INVALID';add('LABEL_ENUM',lang,i,'label',0,x.get('label'),'P0')
            m=x.get('additional_metadata',{})
            if not isinstance(m,dict):m={}
            if set(m)!=set(META):add('META_KEYS',lang,i,'additional_metadata',META,tuple(m),'P1')
            if not isinstance(m.get('stereotyped_groups'),list) or len(m.get('stereotyped_groups',[]))!=1:
                add('META_STEREOTYPED_GROUP',lang,i,'stereotyped_groups','one target-group string',m.get('stereotyped_groups'),'P1')
            ver=m.get('version')
            if ver not in ('a','b'):add('VERSION_ENUM',lang,i,'additional_metadata.version','a/b',ver,'P0')
            versions[ver]+=1
            url=m.get('source')
            if not isinstance(url,str) or urlparse(url).scheme!='https' or not urlparse(url).netloc:
                add('SOURCE_URL_FORMAT',lang,i,'additional_metadata.source','https valid URL',url,'P1')
            official_source=sources.get(f'Q{int(x.get("question_index","0")):02d}') if str(x.get('question_index','')).isdigit() else None
            if official_source and url!=official_source:
                add('SOURCE_URL_THEME_CONSISTENCY',lang,i,'additional_metadata.source',official_source,url,'P1')
            if i<1440:
                wave,theme,rem=i//480,(i%480)//48,i%48
                expq=str(theme+1); expv='a' if rem<24 else 'b'
                if x.get('question_index')!=expq:add('WAVE_THEME_ORDER',lang,i,'question_index',expq,x.get('question_index'),'P0')
                if ver!=expv:add('ORIENTATION_ORDER',lang,i,'version',expv,ver,'P0')
                c=CONDITIONS[(i%24)%4]
                if (x.get('context_condition'),x.get('question_polarity'))!=c:
                    add('FOUR_CONDITION_CANONICAL_ORDER',lang,i,'condition+polarity',c,(x.get('context_condition'),x.get('question_polarity')),'P0')
            inferred, why, clauses=blind_infer(x,lang)
            counts[f'{lang}_blind_anchor_all_records']+=1
            if inferred=='INVALID':add('BLIND_CONTEXT_ENTAILMENT',lang,i,'context+question','unambiguous inferable',why,'P0')
            if inferred!='INVALID' and inferred!=goldentity:
                add('BLIND_GOLD_LABEL',lang,i,'label',f'entity {inferred}',f'{goldentity}; context={why}','P0')
            # Additional independently observed contradiction: already equal speaking time
            # is not compatible with one participant being denied speaking access.
            if (lang=='en' and 'speaking time' in x.get('context','') and 'speaking slot' in x.get('question','')) or (lang=='bn' and 'বক্তব্য দেওয়ার সময়' in x.get('context','') and 'বক্তব্য দেওয়ার সুযোগ' in x.get('question','')):
                add('SPEAKING_TIME_CONTRADICTION',lang,i,'context','no already-granted equal speaking time in refusal scenario',x.get('context','')[:140],'P0')
            qa=tuple(x.get(z) for z in TEXT)
            if qa in seen_qa:add('EXACT_QA_DUPLICATE',lang,i,'QA tuple',f'not repeat line {seen_qa[qa]+1}',qa[1][:90],'P0')
            else:seen_qa[qa]=i
        for field,observed,expected in [('themes',themes,{str(n):144 for n in range(1,11)}),('conditions',conds,{x:360 for x in CONDITIONS}),('gold',gold,{n:480 for n in range(3)}),('versions',versions,{'a':720,'b':720})]:
            if dict(observed)!=expected:add('GLOBAL_DISTRIBUTION',lang,-1,field,expected,dict(observed),'P0')
        counts[f'{lang}_gold_distribution']=dict(gold)
        counts[f'{lang}_condition_distribution']={str(k):v for k,v in conds.items()}
        # Every orientation is 24 rows: 6 distinct permutations, 4 conditions each.
        for block in range(min(60,len(rows)//24)):
            chunk=rows[block*24:block*24+24]
            if len(chunk)!=24 or any(not isinstance(x,dict) for x in chunk):continue
            p=[]
            for pi in range(6):
                z=chunk[pi*4:pi*4+4]
                if len(z)!=4:continue
                perms=[tuple(answer_entity(x,j,lang) for j in range(3)) for x in z]
                if len(set(perms))!=1:add('PERM_WITHIN_BLOCK_INCONSISTENT',lang,block*24+pi*4,'answers','identical position within 4 canonical conditions',perms,'P0')
                p.append(perms[0]);
            if len(p)!=6 or set(p)!=set(itertools.permutations(('A','B','U'))):
                add('SIX_WAY_PERMUTATIONS',lang,block*24,'answer_options','six complete permutations',p,'P0')
            contexts=collections.defaultdict(set);questions=collections.defaultdict(set)
            for x in chunk:
                if not isinstance(x,dict):continue
                contexts[x.get('context_condition')].add(x.get('context'))
                questions[x.get('question_polarity')].add(x.get('question'))
            if len(contexts['ambig'])!=1 or len(contexts['disambig'])!=1 or len(questions['neg'])!=1 or len(questions['nonneg'])!=1:
                add('PERMUTATION_TEXT_INVARIANCE',lang,block*24,'context/question','one each per condition/polarity',str((list(map(len,contexts.values())),list(map(len,questions.values())))),'P0')
            counts[f'{lang}_checked_24_row_orientation_blocks']+=1
        # Counterfactuals swapping ONLY group identity in A/B; all non-protected text preserved.
        for block in range(min(30,len(rows)//48)):
            z=rows[block*48:block*48+48]
            if len(z)!=48 or any(not isinstance(x,dict) for x in z):continue
            for sub in range(24):
                a,b=z[sub],z[24+sub]
                if (a.get('question')!=b.get('question') or a.get('context_condition')!=b.get('context_condition') or a.get('question_polarity')!=b.get('question_polarity')):
                    add('COUNTERFACTUAL_NONETHNIC_ATTRIBUTE',lang,block*48+24+sub,'question/condition/polarity','same',str((a.get('question'),b.get('question'))),'P1')
                opta={answer_entity(a,j,lang):a.get(f'ans{j}','') for j in range(3)}
                optb={answer_entity(b,j,lang):b.get(f'ans{j}','') for j in range(3)}
                na=a.get('context','');nb=b.get('context','')
                for role in ('A','B'):
                    if opta.get(role):na=na.replace(opta[role],f'__{role}__')
                    if optb.get(role):nb=nb.replace(optb[role],f'__{role}__')
                if na!=nb:add('COUNTERFACTUAL_CONTEXT_NONETHNIC_CHANGE',lang,block*48+24+sub,'context','identical after group-name normalization',nb[:145],'P1')
                counts[f'{lang}_counterfactual_compared_pairs']+=1
    A=R['en'];B=R['bn']
    for i,(x,y) in enumerate(zip(A,B)):
        if not isinstance(x,dict) or not isinstance(y,dict):continue
        for k in ('example_id','question_index','question_polarity','context_condition','category','additional_metadata','type','label','id'):
            if x.get(k)!=y.get(k):add('CROSS_LANGUAGE_METADATA', 'both',i,k,x.get(k),y.get(k),'P1')
        for pos in range(3):
            a=x.get('answer_info',{});b=y.get('answer_info',{})
            if isinstance(a,dict) and isinstance(b,dict):
                try:ra=a[f'ans{pos}'][1];rb=b[f'ans{pos}'][1]
                except Exception:continue
                if ra in GROUP_MAP and rb in GROUP_MAP and ra==rb and ra!='unknown':
                    en_str=x.get(f'ans{pos}','');bn_str=y.get(f'ans{pos}','')
                    expected_en={'munda':'Munda','chakma':'Chakma','garo_mandi':'Garo (Mandi)','santal':'Santal','mro':'Mro','marma':'Marma','ethnic_bengali':'ethnic Bengali'}[ra]
                    if expected_en not in en_str or GROUP_MAP[ra] not in bn_str:
                        add('CROSS_LANGUAGE_ETHNIC_NAME','both',i,f'ans{pos}',f'{expected_en} | {GROUP_MAP[ra]}',f'{en_str} | {bn_str}','P1')
                if ra!=rb:add('CROSS_LANGUAGE_ROLE_TAG','both',i,f'ans{pos}',ra,rb,'P0')
            if answer_entity(x,pos,'en')!=answer_entity(y,pos,'bn'):
                add('CROSS_LANGUAGE_ANSWER_ENTITY','both',i,f'ans{pos}',answer_entity(x,pos,'en'),answer_entity(y,pos,'bn'),'P0')
        # Independently inferred gold roles must align between languages, not labels alone.
        en_inferred,en_reason,_=blind_infer(x,'en')
        bn_inferred,bn_reason,_=blind_infer(y,'bn')
        if en_inferred!=bn_inferred:
            add('CROSS_LANGUAGE_INFERRED_MEANING','both',i,'context+question',en_inferred,bn_inferred,'P1')
        counts['bilingual_row_pairs_checked']+=1
    if manifest is not None:
        blocks=manifest.get('blocks',[])
        if len(blocks)!=60:add('MANIFEST_BLOCK_COUNT','both',-1,'blocks',60,len(blocks),'P1')
        for bi,block in enumerate(blocks):
            start=block.get('row_index_0_based_start');end=block.get('row_index_0_based_end_inclusive')
            expected=(bi*24,bi*24+23)
            if (start,end)!=expected:add('MANIFEST_RANGE','both',bi*24,'row ranges',expected,(start,end),'P1')
            if bi*24<len(A) and isinstance(A[bi*24],dict):
                x=A[bi*24]
                if block.get('question_index')!=x.get('question_index') or block.get('orientation')!=x.get('additional_metadata',{}).get('version'):
                    add('MANIFEST_RECORD_PARITY','both',bi*24,'theme/version',(x.get('question_index'),x.get('additional_metadata',{}).get('version')),(block.get('question_index'),block.get('orientation')),'P1')
            counts['manifest_blocks_verified']+=1
    if templates_path and pathlib.Path(templates_path).is_file():
        try:
            ts=json.loads(pathlib.Path(templates_path).read_text(encoding='utf-8'))
            if len(ts)!=10 or any(len(t.get('variants',[]))!=3 for t in ts):
                add('TEMPLATE_COUNT','both',-1,'templates','10 x 3',[len(t.get('variants',[])) for t in ts],'P2')
            # Only an inventory check; template was authored by the generator's author.
        except Exception as e:add('TEMPLATE_PARSE','both',-1,'templates','valid JSON',e,'P1')
    counts['number_of_issues']=len(issues)
    counts['issue_severity_frequency']=dict(collections.Counter(x['severity'] for x in issues))
    counts['issue_type_frequency']=dict(collections.Counter(x['test_id'] for x in issues))
    counts['input_bytes']={'en':pathlib.Path(en_path).stat().st_size,'bn':pathlib.Path(bn_path).stat().st_size}
    return {'summary':dict(counts),'issues':issues,'pass':len(issues)==0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--en',required=True);p.add_argument('--bn',required=True)
    p.add_argument('--manifest');p.add_argument('--source-audit');p.add_argument('--templates');p.add_argument('--output');p.add_argument('--quiet',action='store_true')
    a=p.parse_args()
    result=validate(a.en,a.bn,a.manifest,a.source_audit,a.templates)
    if a.output:pathlib.Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not a.quiet:print(json.dumps({'summary':result['summary'],'examples':result['issues'][:12]},ensure_ascii=False,indent=2))
    sys.exit(0 if result['pass'] else 1)
if __name__=='__main__':main()
