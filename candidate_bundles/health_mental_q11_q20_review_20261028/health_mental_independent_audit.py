#!/usr/bin/env python3
"""Independent-from-generator semantic and structural audit of SAVED files.
Derives gold recipients from the rendered outcome clause, not from scenario adverse/label spec.
For bilingual name transliterations uses manifest only (not label gold oracle).
Limitations: does not emulate a native-speaker or psychiatric clinical review.
"""
import collections,csv,hashlib,itertools,json,re,sys,unicodedata
from pathlib import Path
D=Path(__file__).resolve().parent
files={l:D/f'BanglaBBQ_Health_Mental_Q11_Q20_{l}.jsonl' for l in ['english','bengali']}
rows={l:[json.loads(x) for x in p.read_text('utf-8').splitlines()] for l,p in files.items()}
M=list(csv.DictReader((D/'health_mental_theme_manifest.csv').open(encoding='utf-8',newline='')))
lookup={(int(m['q']),int(m['variation'])):m for m in M}
errors=[]; find=[]; counts=collections.Counter(); outcome_parses=collections.Counter()
def flag(ok,label,eid=None):
    if not ok:errors.append((eid,label))
def answers(r):return [r[f'ans{x}'] for x in range(3)]
def unknown(l):return 'Unknown' if l=='english' else 'অজানা'
def last_outcome(r,l):
    if l=='english': return r['context'].split('The selection decision was subsequently finalized. ')[-1]
    return r['context'].split(unicodedata.normalize('NFC','পরে বাছাইয়ের সিদ্ধান্ত চূড়ান্ত করা হয়। '))[-1]

def masked_intro(r,l,m):
    if l=='english':names=(m['p0_name_en'],m['p1_name_en']); marker=' Both voluntarily shared their diagnosis'
    else:names=(m['p0_name_bn'],m['p1_name_bn']);marker=unicodedata.normalize('NFC',' দুজনই স্বেচ্ছায় শুধু বাছাইয়ের')
    intro=r['context'].split(marker)[0]
    firsts=[intro.find(name) for name in names]
    if any(x<0 for x in firsts):return None,None
    return names[0] if firsts[0]<firsts[1] else names[1],intro

for lang, recs in rows.items():
    flag(len(recs)==1440,lang+' exact count')
    un=unknown(lang)
    for i,r in enumerate(recs):
        eid=1440+i; q=r['question_index']; v=(i//480)+1; m=lookup[(q,v)]
        flag(r['example_id']==eid,lang+' ID',eid)
        flag(r['id']==8300000+eid,lang+' global ID',eid)
        flag(len(r)==15,lang+' keys',eid)
        flag(r['category']=='Health_status' and r['type']=='NA',lang+' category',eid)
        opts=answers(r)
        flag(len(set(opts))==3 and opts.count(un)==1,lang+' unknown/unique',eid)
        flag(all(r['answer_info'][f'ans{j}'][0]==opts[j] for j in range(3)),lang+' answer_info text',eid)
        flag(set(r['answer_info'][f'ans{j}'][1] for j in range(3))=={'unknown',next(tag for tag in (r['answer_info'][f'ans{j}'][1] for j in range(3)) if tag!='unknown' and not tag.startswith('no_')),next(tag for tag in (r['answer_info'][f'ans{j}'][1] for j in range(3)) if tag.startswith('no_'))},lang+' group tag set',eid)
        guess=None
        if r['context_condition']=='ambig':
            guess=un
            # Ensure outcome clause absent and future selection never shown.
            flag(('The selection decision was subsequently finalized. ' if lang=='english' else unicodedata.normalize('NFC','পরে বাছাইয়ের সিদ্ধান্ত চূড়ান্ত করা হয়। ')) not in r['context'],lang+' ambig outcome leakage',eid)
        else:
            s=last_outcome(r,lang)
            names=[o for o in opts if o!=un]
            occur=[(s.find(n),n) for n in names]
            flag(all(p>=0 for p,n in occur),lang+' outcome includes two names',eid)
            if all(p>=0 for p,n in occur):
                ordered=[n for p,n in sorted(occur)]
                flag(ordered[0]!=ordered[1],lang+' outcomes assign different people',eid)
                guess=ordered[0] if r['question_polarity']=='neg' else ordered[1]
                outcome_parses[(lang,r['question_polarity'])]+=1
            # Ensure negative/favorable action markers in actual outcome, not only names.
            if lang=='english':
                negative=re.search(r'reject|turned down|pass(?:ed)? over|exclud|left .* off|not |withheld|declin|omit|kept .* off|refus|denied|turn(?:ed)? down',s,re.I)
                positive=re.search(r'approved|accept|appoint|assign|selected|select|hired|hire|included|include|added|add|gave|given|offered|offer|put |placed|place|retained',s,re.I)
            else:
                negative=re.search(unicodedata.normalize('NFC',r'রাখেননি|নেননি|নেয়নি|দেননি|বাছেননি|বাদ|নাকচ|গ্রহণ করেনি|গ্রহণ করেননি|নিয়োগ দেননি|দায়িত্ব দেওয়া হয়নি'),s)
                positive=re.search(unicodedata.normalize('NFC',r'নিয়েছেন|নিয়েছে|রেখেছেন|দিয়েছেন|গ্রহণ করেছে|গ্রহণ করেছেন|অনুমোদন|নিযুক্ত|যুক্ত|বেছে নিয়েছেন|নিয়োগ দিয়েছেন|দায়িত্ব দিয়েছেন'),s)
            flag(bool(negative),lang+' negative explicit predicate',eid)
            flag(bool(positive),lang+' positive explicit predicate',eid)
        if guess is not None:flag(opts[r['label']]==guess,lang+' independent textual outcome/gold',eid)
        counts[(lang,r['context_condition'],r['question_polarity'])]+=1
        # Intro person names from context rather than answer permutation.
        first,intro=masked_intro(r,lang,m)
        flag(first is not None,lang+' intro names',eid)
        if first and r['context_condition']=='disambig':
            gold=opts[r['label']]
            counts[(lang,'intro',r['question_polarity'],'first' if gold==first else 'second')]+=1
        # For pair ensure the protected-group group has affirmative disclosed diagnosis/care.
        non_unknown=[(opts[j],r['answer_info'][f'ans{j}'][1]) for j in range(3) if opts[j]!=un]
        tag_pers={name:tag for name,tag in non_unknown}
        target=[name for name,tag in non_unknown if not tag.startswith('no_')]
        comp=[name for name,tag in non_unknown if tag.startswith('no_')]
        flag(len(target)==1 and len(comp)==1,lang+' protected comparator',eid)
        if len(target)==1 and len(comp)==1:
            ctx=r['context']
            if lang=='english':
                clause=ctx.split('with the decision-maker: ')[-1].split('. The selection decision')[0]
                # Status language is explicit positive and explicit negative.
                flag(target[0] in clause and comp[0] in clause and ('has not' in clause or 'has never' in clause),lang+' role disclosures',eid)
            else:
                clause=ctx.split(unicodedata.normalize('NFC','স্বাস্থ্যসংক্রান্ত তথ্য জানান। '))[-1].split(unicodedata.normalize('NFC','। পরে বাছাইয়ের'))[0]
                flag(target[0] in clause and comp[0] in clause and (unicodedata.normalize('NFC','নির্ণয় হয়নি') in clause or 'অভিজ্ঞতা নেই' in clause),lang+' role disclosures',eid)
    for k,v0 in counts.items():
        if isinstance(k,tuple) and len(k)==4 and k[0]==lang and k[1]=='intro':
            flag(v0==180,lang+' intro total balanced '+str(k))
    # Check FULL permutation closure grouping solely by actual context and question.
    gr=collections.defaultdict(set)
    for r in recs:
        gr[(r['context'],r['question'])].add(tuple(answers(r)))
    flag(len(gr)==240,lang+' independent context-question equivalence groups')
    for key,perm in gr.items():
        opts=next(iter(perm))
        flag(len(perm)==6 and perm==set(itertools.permutations(opts)),lang+' six-permutation group: '+key[0][:60])

# Independent cross-lingual alignment using names in the manifest, no original gold spec.
en=rows['english'];bn=rows['bengali']
for i,(e,b) in enumerate(zip(en,bn)):
    eid=1440+i;q=e['question_index'];v=(i//480)+1;m=lookup[(q,v)]
    names={m['p0_name_en']:m['p0_name_bn'],m['p1_name_en']:m['p1_name_bn'],'Unknown':'অজানা'}
    for k in ['example_id','id','question_index','question_polarity','context_condition','category','type','label']:
        flag(e[k]==b[k],'bilingual metadata '+k,eid)
    for j in range(3):flag(b[f'ans{j}']==names[e[f'ans{j}']],'bilingual name permutation',eid)
    for key in ['additional_metadata']:
        flag(e[key]==b[key],'bilingual metadata '+key,eid)
    for j in range(3):flag(e['answer_info'][f'ans{j}'][1]==b['answer_info'][f'ans{j}'][1],'bilingual group tags',eid)
    # independently infer first and second adverse from each actual disambiguated text
    if e['context_condition']=='disambig':
        ee=last_outcome(e,'english');bb=last_outcome(b,'bengali')
        es=sorted(((ee.find(n),n) for n in names if n!='Unknown'))
        bs=sorted(((bb.find(t),t) for t in names.values() if t!='অজানা'))
        flag([names[n] for _,n in es]==[n for _,n in bs],'bilingual outcome recipient order',eid)

# Crossfactual: same outcome recipients, group tags swapped, names in intro order reversed, qualifications equal
for lang,recs in rows.items():
    for i in range(0,1440,48):
        a=recs[i:i+24];b=recs[i+24:i+48];q=a[0]['question_index'];v=i//480+1;m=lookup[(q,v)]
        for j in range(24):
            ra,rb=a[j],b[j]
            flag(answers(ra)==answers(rb),lang+' counterfactual answer texts unchanged',ra['example_id'])
            flag(ra['label']==rb['label'],lang+' counterfactual same named outcomes',ra['example_id'])
            t0=[ra['answer_info'][f'ans{k}'][1] for k in range(3)]
            t1=[rb['answer_info'][f'ans{k}'][1] for k in range(3)]
            flag(all(x=='unknown' and y=='unknown' or x!='unknown' and y!='unknown' and (x.startswith('no_') != y.startswith('no_')) for x,y in zip(t0,t1)),lang+' protected group swaps only',ra['example_id'])
        intro_a,scene_a=masked_intro(a[0],lang,m);intro_b,scene_b=masked_intro(b[0],lang,m)
        flag(intro_a!=intro_b,lang+' intro reversed',a[0]['example_id'])
        # English and Bengali baseline descriptions should differ ONLY because first/second names swap.
        if scene_a is not None and scene_b is not None:
            x,y=(m['p0_name_en'],m['p1_name_en']) if lang=='english' else (m['p0_name_bn'],m['p1_name_bn'])
            def normalize(st):return st.replace(x,'XPERSON').replace(y,'YPERSON').replace('XPERSON and YPERSON','PAIR').replace('YPERSON and XPERSON','PAIR').replace('XPERSON ও YPERSON','PAIR').replace('YPERSON ও XPERSON','PAIR')
            flag(normalize(scene_a)==normalize(scene_b),lang+' matched qualifications, aside intro',a[0]['example_id'])

report={
 'audit_name':'blind_saved_file_parser_plus_crossfactual_and_bilingual_checks',
 'uses_generator_truth_spec':False,
 'exceptions':len(errors),
 'first_20_errors':errors[:20],
 'rows_per_language':{l:len(r) for l,r in rows.items()},
 'outcome_parser_rows':{f'{l}:{p}':n for (l,p),n in outcome_parses.items()},
 'label_distribution':{l:dict(collections.Counter(r['label'] for r in recs)) for l,recs in rows.items()},
 'intro_balance':{':'.join(map(str,k)):v for k,v in counts.items() if k[1]=='intro'},
 'source_urls':sorted(set(r['additional_metadata']['source'] for r in en)),
 'sha256':{l:hashlib.sha256(p.read_bytes()).hexdigest() for l,p in files.items()},
}
(D/'health_mental_independent_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:sys.exit(1)
