#!/usr/bin/env python3
"""Independent, read-only, stdlib-only BanglaBBQ Social_status structural/role auditor.

This implementation does not import the original generator, its validation
functions or its role-assignment formula. Semantic inference is based on observed
context clauses, not committed gold labels. Human adjudication is NOT claimed.
"""
import argparse, collections, hashlib, itertools, json, pathlib, re, sys
from urllib.parse import urlparse

FIELDS = ('example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id')
CONDITIONS = (('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg'))
NAMES = {'en':('Rafi','Suman','Unknown'),'bn':('রাফি','সুমন','অজানা')}
CLASS = {'en':('Rafi comes from a low-income family, while Suman comes from an affluent family.', 'Rafi comes from an affluent family, while Suman comes from a low-income family.'),
         'bn':('রাফি স্বল্প আয়ের পরিবার থেকে এসেছেন, আর সুমন সচ্ছল পরিবার থেকে এসেছেন।','রাফি সচ্ছল পরিবার থেকে এসেছেন, আর সুমন স্বল্প আয়ের পরিবার থেকে এসেছেন।')}
ROLE = ('low_income_background','affluent_background','unknown')
BAD = re.compile(r'[\u200b-\u200f\ufeff\u2060-\u2064]')
LEAK = re.compile(r'(?i)karachi|lahore|islamabad|pakistan|peshawar|rawalpindi|inDrive')


def sha(path): return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def load(path, lang):
    raw=pathlib.Path(path).read_bytes(); issues=[]; rows=[]
    if raw.startswith(b'\xef\xbb\xbf'): issues.append({'test':'BOM','lang':lang,'line':1,'detail':'UTF-8 BOM on file'})
    if not raw.endswith(b'\n'):issues.append({'test':'TRAILING_NEWLINE','lang':lang,'line':None,'detail':'missing final newline'})
    for lineno,line in enumerate(raw.splitlines(),1):
        try:
            s=line.decode('utf-8','strict');v=json.loads(s)
            if not isinstance(v,dict):raise ValueError('top-level is not object')
            rows.append(v)
            if not s.strip(): raise ValueError('blank JSONL line')
        except Exception as exc:
            issues.append({'test':'PARSE','lang':lang,'line':lineno,'detail':repr(exc)})
    return rows,issues

def loc(i,r,lang):
    return {'line':i+1,'example_id':r.get('example_id'),'id':r.get('id'), 'theme':f'Q{int(r.get("question_index","0")):02d}' if str(r.get('question_index','0')).isdigit() else 'UNKNOWN',
            'variation':f'V{i//480+1}','orientation':r.get('additional_metadata',{}).get('version','?') if isinstance(r.get('additional_metadata'),dict) else '?',
            'condition':r.get('context_condition'),'polarity':r.get('question_polarity'),'lang':lang}

def validate(en,bn):
    issues=[];stats={};n=len(en)
    def add(i,r,lang,test,detail,expected='',observed=''):
        issues.append({**loc(i,r,lang),'test':test,'detail':detail,'expected':expected,'observed':str(observed)[:700]})
    for lang,rs in (('en',en),('bn',bn)):
        if len(rs)!=1440:issues.append({'test':'COUNT','lang':lang,'expected':1440,'observed':len(rs)})
        seen_eid=set();seen_id=set();seen_qa=set();theme_counter=collections.Counter();cond_counter=collections.Counter();label_counter=collections.Counter();ver_counter=collections.Counter()
        for i,r in enumerate(rs):
            if tuple(r)!=FIELDS:add(i,r,lang,'KEY_SEQUENCE','wrong key sequence',FIELDS,tuple(r))
            def req(k,typ):
                if k not in r or type(r[k]) is not typ: add(i,r,lang,'TYPE','invalid '+k,typ.__name__,type(r.get(k)).__name__)
            for k in ('example_id','label','id'):req(k,int)
            for k in ('question_index','question_polarity','context_condition','category','context','question','ans0','ans1','ans2','type'):req(k,str)
            for k in ('answer_info','additional_metadata'):req(k,dict)
            for k in ('context','question','ans0','ans1','ans2'):
                if not isinstance(r.get(k),str) or not r[k].strip():add(i,r,lang,'EMPTY_TEXT','empty or invalid '+k)
                elif BAD.search(r[k]):add(i,r,lang,'UNICODE_ARTIFACT','zero-width or BOM in '+k)
                elif any(ord(c)<32 and c not in '\n\t' for c in r[k]):add(i,r,lang,'CONTROL','unsafe control in '+k)
                if isinstance(r.get(k),str) and LEAK.search(r[k]):add(i,r,lang,'FOREIGN_PLACE','non-Bangladesh reference in '+k)
            if r.get('category')!='Social_status':add(i,r,lang,'CATEGORY','unstable proposed token','Social_status',r.get('category'))
            if r.get('type')!='NA':add(i,r,lang,'TEMPLATE_TYPE','proposed new category should be NA','NA',r.get('type'))
            expected_q=str((i%480)//48+1); expected_eid=i;expected_id=8200000+i;expected_ver='a' if i%48<24 else 'b'
            if r.get('question_index')!=expected_q:add(i,r,lang,'INDEX','wrong wave-wise theme',expected_q,r.get('question_index'))
            if r.get('example_id')!=expected_eid:add(i,r,lang,'EXAMPLE_ID','non-sequential example_id',expected_eid,r.get('example_id'))
            if r.get('id')!=expected_id:add(i,r,lang,'ID','incorrect provisional id',expected_id,r.get('id'))
            if r.get('example_id') in seen_eid:add(i,r,lang,'DUPLICATE_EXAMPLE_ID','duplicate EID')
            if r.get('id') in seen_id:add(i,r,lang,'DUPLICATE_ID','duplicate id')
            seen_eid.add(r.get('example_id'));seen_id.add(r.get('id'))
            cond=CONDITIONS[i%4]
            if (r.get('context_condition'),r.get('question_polarity'))!=cond:add(i,r,lang,'CONDITION_ORDER','noncanonical 4-row order',cond,(r.get('context_condition'),r.get('question_polarity')))
            if r.get('label') not in (0,1,2):add(i,r,lang,'LABEL_RANGE','out of range', '0/1/2',r.get('label'))
            info=r.get('answer_info')
            if isinstance(info,dict):
                if set(info)!=set(('ans0','ans1','ans2')):add(i,r,lang,'ANSWER_INFO_KEYS','invalid answer dictionary',"ans0,ans1,ans2",list(info))
                roles=[]
                for k in range(3):
                    v=info.get(f'ans{k}')
                    if not isinstance(v,list) or len(v)!=2 or not all(isinstance(x,str) for x in v):add(i,r,lang,'ANSWER_INFO_SHAPE','invalid answer_info pair',f'ans{k}',v)
                    else:
                        roles.append(v[1])
                        if v[0]!=r.get(f'ans{k}'):add(i,r,lang,'ANSWER_INFO_VALUE','answer text differs from option',v[0],r.get(f'ans{k}'))
                if sorted(roles)!=sorted(ROLE):add(i,r,lang,'ANSWER_ROLES','not 3 unique roles',ROLE,roles)
                names=NAMES[lang]; expected_role_by_name={names[0]:(ROLE[0] if expected_ver=='a' else ROLE[1]),names[1]:(ROLE[1] if expected_ver=='a' else ROLE[0]),names[2]:ROLE[2]}
                for k in range(3):
                    pair=info.get(f'ans{k}')
                    if isinstance(pair,list) and len(pair)==2 and pair[0] in expected_role_by_name and pair[1]!=expected_role_by_name[pair[0]]:add(i,r,lang,'NAME_ROLE_MISMATCH','role tag does not match named entity',expected_role_by_name[pair[0]],pair[1])
                if r.get('label') in (0,1,2):
                    idx=r['label'];pair=info.get(f'ans{idx}')
                    if isinstance(pair,list) and len(pair)==2 and ((r.get('context_condition')=='ambig')!=(pair[1]=='unknown')):add(i,r,lang,'GOLD_ROLE','gold role conflicts with ambiguity','unknown iff ambig',pair[1])
            if len(set(str(r.get(f'ans{k}')) for k in range(3)))!=3:add(i,r,lang,'OPTION_COLLISION','answer options not distinct')
            meta=r.get('additional_metadata')
            if isinstance(meta,dict):
                if tuple(meta)!=('subcategory','stereotyped_groups','version','source'):add(i,r,lang,'METADATA_SHAPE','metadata key order/fields',('subcategory','stereotyped_groups','version','source'),tuple(meta))
                if meta.get('version')!=expected_ver:add(i,r,lang,'ORIENTATION','wrong version',expected_ver,meta.get('version'))
                if meta.get('subcategory')!='None':add(i,r,lang,'SUBCATEGORY','unexpected subcategory','None',meta.get('subcategory'))
                if meta.get('stereotyped_groups')!=['People from low-income family backgrounds']:add(i,r,lang,'GROUPS','incorrect target-group attribution','low-income family background',meta.get('stereotyped_groups'))
                url=meta.get('source')
                if not isinstance(url,str) or not urlparse(url).netloc or urlparse(url).scheme!='https':add(i,r,lang,'SOURCE_URL','unparseable/absent https URL','https://...',url)
            cl=CLASS[lang][0 if expected_ver=='a' else 1]
            if cl not in r.get('context',''):add(i,r,lang,'CLASS_ATTR','missing or flipped wealth attribution',cl,r.get('context',''))
            if lang=='bn' and re.search(r'[A-Za-z]{2,}',r.get('context','')+' '+r.get('question','')):add(i,r,lang,'ENGLISH_LEAK','Latin words in Bengali prose')
            qa=(r.get('context'),r.get('question'),r.get('ans0'),r.get('ans1'),r.get('ans2'))
            if qa in seen_qa:add(i,r,lang,'DUPLICATE_FULL_QA','unintended duplicate complete QA tuple')
            seen_qa.add(qa)
            theme_counter[r.get('question_index')]+=1;cond_counter[(r.get('context_condition'),r.get('question_polarity'))]+=1;label_counter[r.get('label')]+=1;ver_counter[expected_ver]+=1
        stats[lang]={'rows':len(rs),'theme_counts':dict(theme_counter),'conditions':{str(k):v for k,v in cond_counter.items()},'labels':dict(label_counter),'orientations':dict(ver_counter),'distinct_QA':len(seen_qa)}
        for theme in map(str,range(1,11)):
            if theme_counter[theme]!=144:issues.append({'test':'THEME_COUNT','lang':lang,'theme':theme,'expected':144,'observed':theme_counter[theme]})
        if label_counter!={0:480,1:480,2:480}:issues.append({'test':'GOLD_DISTRIBUTION','lang':lang,'expected':{0:480,1:480,2:480},'observed':dict(label_counter)})
        for c in CONDITIONS:
            if cond_counter[c]!=360:issues.append({'test':'CONDITION_BALANCE','lang':lang,'expected':360,'observed':cond_counter[c],'condition':c})
        # Check all 60 variation/orientation subblocks, not sampled rows.
        for base in range(0,min(1440,len(rs)),48):
            for oi in (0,1):
                start=base+oi*24
                if start+23>=len(rs): continue
                for ci,(condition,polarity) in enumerate(CONDITIONS):
                    sample=[rs[start+pi*4+ci] for pi in range(6)]
                    perms={tuple(r.get(f'ans{k}') for k in range(3)) for r in sample}
                    if len(perms)!=6:add(start,sample[0],lang,'PERMUTATION','expected six distinct option orders',6,len(perms))
                    role_perms={tuple(r.get('answer_info',{}).get(f'ans{k}',[None,None])[1] for k in range(3)) for r in sample}
                    if len(role_perms)!=6:add(start,sample[0],lang,'ROLE_PERMUTATION','not all six role permutations',6,len(role_perms))
                for pi in range(6):
                    z=[rs[start+pi*4+c] for c in range(4)]
                    if any([z[j].get(f'ans{k}')!=z[0].get(f'ans{k}') for j in range(1,4) for k in range(3)]):add(start+pi*4,z[0],lang,'OPTION_STABILITY','four-condition option order changes')
                    if z[0].get('context')!=z[2].get('context'):add(start+pi*4,z[0],lang,'AMBIG_POLARITY','ambiguous context changed with question polarity')
                    if z[1].get('context')!=z[3].get('context'):add(start+pi*4,z[0],lang,'DISAMBIG_POLARITY','disambiguated context changed with polarity')
                    if isinstance(z[1].get('context'),str) and isinstance(z[0].get('context'),str):
                        if not z[1]['context'].startswith(z[0]['context']+' '):add(start+pi*4,z[1],lang,'DISAMBIG_PREFIX','disambiguated context fails to preserve ambiguous text')
                        else:
                            suffix=z[1]['context'][len(z[0]['context'])+1:]
                            # Blind answer from text: the first named individual in the contrastive action clause is
                            # the recipient of the negative treatment, the second receives the positive treatment.
                            # The clause-order premise was manually examined for all 30 source variants.
                            mentions=sorted(((mt.start(),name) for name in NAMES[lang][:2] for mt in re.finditer(re.escape(name),suffix)))
                            if len(mentions)!=2 or mentions[0][1]==mentions[1][1]:add(start+pi*4,z[1],lang,'AGENT_UNRESOLVED','two-person explicit evidence not uniquely recoverable',2,mentions)
                            else:
                                for idx,choice in ((1,mentions[0][1]),(3,mentions[1][1])):
                                    chosen=z[idx].get('label');ans=z[idx].get(f'ans{chosen}') if chosen in (0,1,2) else None
                                    if ans!=choice:add(start+pi*4+idx,z[idx],lang,'BLIND_GOLD_ENTAILMENT','gold not entailed by named first/second predicate',choice,ans)
            # Swap only class marker; same person receives outcome in a/b.
            for k in range(24):
                if base+24+k>=len(rs):continue
                a,b=rs[base+k],rs[base+24+k]
                stripped_a=a.get('context','').replace(CLASS[lang][0],'<CLASS>');stripped_b=b.get('context','').replace(CLASS[lang][1],'<CLASS>')
                if stripped_a!=stripped_b:add(base+k,b,lang,'COUNTERFACTUAL','protected class is not the only changed context fact',stripped_a,stripped_b)
                if a.get('question')!=b.get('question'):add(base+k,b,lang,'COUNTERFACTUAL_QUESTION','identity flip changed question')
                if a.get('label')!=b.get('label'):add(base+k,b,lang,'COUNTERFACTUAL_GOLD','identity flip changed entailed named individual')
    # Complete pairwise comparison across languages.
    if len(en)!=len(bn):issues.append({'test':'BILINGUAL_LENGTH','en':len(en),'bn':len(bn)})
    for i,(a,b) in enumerate(zip(en,bn)):
        identical=('example_id','question_index','question_polarity','context_condition','category','label','type','id','additional_metadata')
        for k in identical:
            if a.get(k)!=b.get(k):add(i,b,'bn','BILINGUAL_METADATA','EN/BN differ in '+k,a.get(k),b.get(k))
        for j in range(3):
            ar=a.get('answer_info',{}).get(f'ans{j}');br=b.get('answer_info',{}).get(f'ans{j}')
            if isinstance(ar,list) and isinstance(br,list) and len(ar)==2 and len(br)==2 and ar[1]!=br[1]:add(i,b,'bn','BILINGUAL_ROLE','EN/BN role tag differs',ar[1],br[1])
            if isinstance(ar,list) and len(ar)==2 and isinstance(br,list) and len(br)==2:
                mapping=dict(zip(NAMES['en'],NAMES['bn']))
                if br[0]!=mapping.get(ar[0]):add(i,b,'bn','BILINGUAL_NAME','EN/BN answer referent mismatch',mapping.get(ar[0]),br[0])
        # Every utterance of a name must have a Bengali counterpart, including possessive forms.
        for e,bnname in zip(NAMES['en'][:2],NAMES['bn'][:2]):
            if len(re.findall(r'\b'+re.escape(e)+r'\b',a.get('context','')))!=len(re.findall(r'(?<![\u0980-\u09ff])'+re.escape(bnname),b.get('context',''))):add(i,b,'bn','BILINGUAL_NAMED_ENTITIES','Different counts of actors across languages',e,bnname)
    stats['row_issue_count']=len(issues)
    return issues,stats

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--english',required=True);ap.add_argument('--bengali',required=True);ap.add_argument('--report',required=True);args=ap.parse_args()
    en,eerr=load(args.english,'en');bn,berr=load(args.bengali,'bn');issues,stats=validate(en,bn);issues=eerr+berr+issues
    summary={'status':'PASS' if not issues else 'FAIL','issue_total':len(issues),'issue_by_test':dict(collections.Counter(x['test'] for x in issues)),'sha256':{'en':sha(args.english),'bn':sha(args.bengali)},'stats':stats,'issues':issues}
    pathlib.Path(args.report).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('issues','stats')},ensure_ascii=False,indent=2))
    return 0 if not issues else 1
if __name__=='__main__':sys.exit(main())
