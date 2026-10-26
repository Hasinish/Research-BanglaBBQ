#!/usr/bin/env python3
"""Independent, offline, read-only audit validator of committed BanglaBBQ Regional JSONLs.

Does NOT import, run, or copy the original generator/validator algorithm.
Blind-answer heuristic examines context and questions before reading labels.
It does not replace expert source review or bilingual human review.

python3 Regional_independent_validator.py --english FILE --bengali FILE --manifest FILE --source-audit FILE --output-json RESULT
"""
import argparse, collections, csv, hashlib, itertools, json, pathlib, re, sys, unicodedata
from difflib import SequenceMatcher
from urllib.parse import urlsplit

SCHEMA=['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
STATES=[('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
REGIONS={'Noakhali':'নোয়াখালী','Bogura':'বগুড়া','Barishal':'বরিশাল','Khulna':'খুলনা','Tangail':'টাঙ্গাইল','Dinajpur':'দিনাজপুর','Cumilla':'কুমিল্লা','Mymensingh':'ময়মনসিংহ','Rangpur':'রংপুর','Rajshahi':'রাজশাহী','Sylhet':'সিলেট','Chattogram':'চট্টগ্রাম','Dhaka':'ঢাকা','Jashore':'যশোর','Chandpur':'চাঁদপুর'}
UNKNOWN_EN='Cannot be determined'
UNKNOWN_BN='নির্ধারণ করা যায় না'
SOURCE_HEALTH={'Q01':'DIRECT','Q02':'DIRECT','Q03':'DIRECT','Q04':'DIRECT','Q05':'DIRECT','Q06':'PARTIAL','Q07':'DIRECT','Q08':'PARTIAL','Q09':'PARTIAL','Q10':'PARTIAL'}
NEG_EN=('untrustworthy','manipulat','suspicion','hot-headed','starting arguments','confrontational','stingy','unwilling','miserly','reject','oppose','against','unsophisticated','naive','slowly','press','sponsor in london','extra money','mock','laugh at','comical','less suitable','unsuitable','insufficiently polished','lavish','costly rituals','overspend','uncultured','ill-mannered','rude')
NEG_BN=('অবিশ্বস্ত','বদলানোর অভিযোগ','সন্দেহ','বদমেজাজি','ঝগড়া','বিবাদপ্রবণ','কৃপণ','অনিচ্ছুক','প্রত্যাখ্যান','বিরোধিতা','বিপক্ষে','অপরিশীলিত','অনভ্যস্ত','সরলমনা','ধীরে','চাপ','লন্ডনে বাড়তি','বাড়তি টাকা','হাস্যকর','হাসাহাসি','অনুপযুক্ত','কম উপযুক্ত','পরিশীলিত নয়','জাঁকজমকপূর্ণ','ব্যয়বহুল','অতিরিক্ত খরচ','অসংস্কৃত','অভদ্র')
POLARITY_HINTS_EN={
 'negative':NEG_EN,
 'positive':('trustworthy','honest','confidence','level-headed','courteous','cooperative','generous','sharing expenses fairly','willing to contribute','welcome','support','endorse','capable','street-smart','quickly','respect','accept','sufficient','pleasant','dignified','suitable for the broadcast','broadcast-ready','professional','modest','simple arrangements','budget-conscious','well-mannered','respectful','polite')
}
PREDICATE_HINTS_EN={
 'neg': ('untrustworthy','manipulat','suspicion','hot-headed','arguments','confrontational','stingy','unwilling','miserly','reject','oppos','against','unsophisticated','naive','slow','extra money','London','mock','laugh','comical','less suitable','unsuitable','insufficiently polished','lavish','costly','overspend','uncultured','ill-mannered','rude'),
 'nonneg': ('trustworthy','honest','confidence','level-headed','courteous','cooperative','generous','share expenses','willing','welcome','support','endorse','capable','street-smart','quick','respect','accept','sufficient','pleasant','dignified','suitable','broadcast-ready','professional','modest','simple','budget-conscious','well-mannered','respectful','polite')
}
BAD_LOCATION=re.compile(r'\b(?:Karachi|Lahore|Islamabad|Rawalpindi|Peshawar|Pakistani|Pakistan)\b|করাচি|লাহোর|ইসলামাবাদ|পাকিস্তান',re.I)
BAD_CHARS={'\ufeff','\u200b','\u200c','\u200d','\u2060','\u00ad'}

class DuplicateObjectKey(ValueError):pass

def strict_dict(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise DuplicateObjectKey(k)
  d[k]=v
 return d

def load(path, lang, issues):
 data=[]
 raw=pathlib.Path(path).read_bytes()
 try:txt=raw.decode('utf-8',errors='strict')
 except UnicodeError as e:issues.append({'test_id':'INVALID_UTF8','lang':lang,'line':0,'message':str(e)});return [],raw
 if txt.startswith('\ufeff'):issues.append({'test_id':'BOM','lang':lang,'line':1,'message':'UTF-8 BOM at start'})
 for line_no,line in enumerate(txt.split('\n'),1):
  if line_no==len(txt.split('\n')) and not line:continue
  if not line.strip():issues.append({'test_id':'BLANK_JSONL','lang':lang,'line':line_no,'message':'blank line'});continue
  try:r=json.loads(line,object_pairs_hook=strict_dict)
  except Exception as e:issues.append({'test_id':'MALFORMED_JSON','lang':lang,'line':line_no,'message':str(e)});continue
  data.append(r)
 return data,raw

def problem(issues,typ,lang,row,message,expected=None,observed=None):
 issues.append({'test_id':typ,'lang':lang,'line':row.get('example_id',-1)+1 if isinstance(row.get('example_id'),int) else -1,'example_id':row.get('example_id'),'id':row.get('id'),'question_index':row.get('question_index'),'orientation':row.get('additional_metadata',{}).get('version') if isinstance(row.get('additional_metadata'),dict) else None,'condition':row.get('context_condition'),'polarity':row.get('question_polarity'),'message':message,'expected':expected,'observed':observed})

def city_from_option(s,lang):
 if lang=='en' and s.startswith('The person from '):return s[len('The person from '):]
 if lang=='bn' and s.endswith(' থেকে আসা ব্যক্তি'):return s[:-len(' থেকে আসা ব্যক্তি')]
 return None

def polarity_blind(question,lang):
 q=question.lower() if lang=='en' else question
 terms=NEG_EN if lang=='en' else NEG_BN
 if any((re.search(r'\bpress\b', q) if k=='press' else k in q) for k in terms):return 'neg'
 if lang=='en' and any(k in q for k in POLARITY_HINTS_EN['positive']):return 'nonneg'
 return 'nonneg' if '?' in q else None

def blind_infer(amb,dis,question,opts,lang):
 """Operate on context, question and options, never on metadata or label.
 Expected judgment order is manually audited separately for each of 30 styles.
 Return position and minimal evidence span; don't pretend full NLP understanding.
 """
 if len(dis)==len(amb):
  if any(e in amb.lower() for e in ['called the person','praised the person','accused the person','the person from']):pass
  return None,'Not disambiguated'
 suffix=dis[len(amb):] if dis.startswith(amb) else dis
 cities=[city_from_option(o,lang) for o in opts]
 locs=[]
 for i,city in enumerate(cities):
  if not city:continue
  p=suffix.find(city)
  if p>=0:locs.append((p,i,city))
 if len(locs)!=2:return None,'Cannot recover two separate region referents from factual clause'
 locs.sort()
 inferredpol=polarity_blind(question,lang)
 if inferredpol is None:return None,'Cannot classify question from its text'
 pos=locs[0][1] if inferredpol=='neg' else locs[1][1]
 return pos,suffix.strip()

def check(english,bengali,manifest=None,audit=None):
 issues=[];files={};datasets={}
 for lang,p in [('en',english),('bn',bengali)]:
  rows,raw=load(p,lang,issues);datasets[lang]=rows
  files[lang]={'count':len(rows),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob_sha':'UNRECORDED','bytes':len(raw)}
  if len(rows)!=1440:issues.append({'test_id':'COUNT','lang':lang,'message':f'{len(rows)} != 1440'})
  ids=set(); roles=collections.Counter();groups=collections.Counter();four=collections.Counter()
  qa=set()
  for i,r in enumerate(rows):
   if not isinstance(r,dict):issues.append({'test_id':'NOT_OBJECT','lang':lang,'line':i+1});continue
   if list(r)!=SCHEMA:problem(issues,'TOPLEVEL_SCHEMA',lang,r,'wrong key/order',SCHEMA,list(r))
   reqtypes={'example_id':int,'question_index':str,'question_polarity':str,'context_condition':str,'category':str,'answer_info':dict,'additional_metadata':dict,'context':str,'question':str,'ans0':str,'ans1':str,'ans2':str,'label':int,'type':str,'id':int}
   for k,t in reqtypes.items():
    if k not in r or type(r[k]) is not t:problem(issues,'FIELD_TYPE',lang,r,f'{k} type',t.__name__,str(type(r.get(k))))
   if any(k not in r for k in SCHEMA):continue
   if r['example_id']!=i:problem(issues,'EXAMPLE_ID',lang,r,'unexpected sequential example id',i,r['example_id'])
   if r['id']!=8400000+i:problem(issues,'PROVISIONAL_ID',lang,r,'id should be 8400000+row number',8400000+i,r['id'])
   if r['id'] in ids:problem(issues,'DUPLICATE_ID',lang,r,'id reused');
   ids.add(r['id'])
   if r['question_index']!=str((i//48)%10+1):problem(issues,'THEME_INDEX',lang,r,'theme does not match wave-major row mapping')
   expected_ori='a' if i%48<24 else 'b'
   if r['context_condition'] not in ('ambig','disambig') or r['question_polarity'] not in ('neg','nonneg'):problem(issues,'CONDITION_ENUM',lang,r,'illegal condition/polarity')
   else:
    want=STATES[i%4]
    if (r['context_condition'],r['question_polarity'])!=want:problem(issues,'CANONICAL_ORDER',lang,r,'noncanonical four-condition order',want,(r['context_condition'],r['question_polarity']))
    four[(r['context_condition'],r['question_polarity'])]+=1
   if r['category']!='Regional' or r['type']!='NA':problem(issues,'CATEGORY_OR_TYPE',lang,r,'category or type mismatch','Regional/NA',f"{r['category']}/{r['type']}")
   meta=r['additional_metadata']
   if not isinstance(meta,dict) or any(k not in meta for k in ('subcategory','stereotyped_groups','version','source')):problem(issues,'METADATA_SHAPE',lang,r,'missing metadata');continue
   if meta['version']!=expected_ori:problem(issues,'ORIENTATION',lang,r,'orientation contradicts row block',expected_ori,meta['version'])
   if not isinstance(meta['stereotyped_groups'],list) or not meta['stereotyped_groups']:problem(issues,'GROUP_METADATA',lang,r,'empty/invalid stereotyped groups')
   if not isinstance(meta['source'],str) or not meta['source'].startswith('https://') or not urlsplit(meta['source']).netloc:problem(issues,'SOURCE_URL',lang,r,'invalid source URL')
   if type(r['label']) is not int or r['label'] not in (0,1,2):problem(issues,'LABEL_ENUM',lang,r,'illegal gold label')
   info=r['answer_info']
   if not isinstance(info,dict) or set(info)!={'ans0','ans1','ans2'}:problem(issues,'ANSWER_INFO_SHAPE',lang,r,'answer_info keys');continue
   if any(not isinstance(info.get('ans'+str(j)),list) or len(info.get('ans'+str(j)))!=2 for j in range(3)):
    problem(issues,'ANSWER_INFO_SHAPE',lang,r,'bad pair');continue
   for j in range(3):
    val,tag=info['ans'+str(j)]
    if val!=r['ans'+str(j)]:problem(issues,'ANSWER_INFO_TEXT',lang,r,f'ans{j} answer_info text mismatch',r['ans'+str(j)],val)
    if tag=='unknown' and r['ans'+str(j)]!=(UNKNOWN_EN if lang=='en' else UNKNOWN_BN):problem(issues,'UNKNOWN_ROLE_TEXT',lang,r,'unknown answer differs from canonical')
    if tag!='unknown':
     name=city_from_option(r['ans'+str(j)],lang)
     if not name:problem(issues,'REGION_OPTION','bn' if lang=='bn' else 'en',r,'malformed regional answer')
     else:
      if lang=='en' and tag!='origin_'+name.lower():problem(issues,'ROLE_TAG',lang,r,'tag not derived from actual city',name,tag)
      if lang=='bn' and name not in REGIONS.values():problem(issues,'REGION_OPTION',lang,r,'unrecognized Bengali district',list(REGIONS.values()),name)
   if len({r['ans0'],r['ans1'],r['ans2']})!=3 or len({info['ans'+str(j)][1] for j in range(3)})!=3:problem(issues,'DUPLICATE_OPTION',lang,r,'colliding answer values or roles')
   if r['context_condition']=='ambig':
    if lang=='en' and re.search(r'(called the person from|praised the person from|accused the person from|thanked the person from)',r['context'],re.I):
     problem(issues,'AMBIGUITY_LEAK',lang,r,'ambiguous context includes an evaluator decision')
    if lang=='bn' and re.search(r'(প্রশংসা করেন|অভিযোগ করেন|প্রত্যাখ্যান করেন|হাসাহাসি করেন)',r['context']):
     problem(issues,'AMBIGUITY_LEAK',lang,r,'ambiguous Bengali context includes outcome cues')
   if r['context_condition']=='ambig' and type(r['label']) is int and 0<=r['label']<=2 and info['ans'+str(r['label'])][1]!='unknown':problem(issues,'AMBIG_LABEL',lang,r,'ambiguous gold is not Unknown')
   if r['context_condition']=='disambig' and type(r['label']) is int and 0<=r['label']<=2 and info['ans'+str(r['label'])][1]=='unknown':problem(issues,'DISAMBIG_UNKNOWN',lang,r,'disambiguated gold Unknown')
   for k in ('context','question','ans0','ans1','ans2'):
    if not r[k].strip():problem(issues,'EMPTY_STRING',lang,r,f'{k} empty')
    if any(ch in r[k] for ch in BAD_CHARS):problem(issues,'ZERO_WIDTH',lang,r,f'{k} invisible chars')
    if any(unicodedata.category(ch)=='Cc' for ch in r[k]):problem(issues,'CONTROL_CHAR',lang,r,f'{k} control chars')
    if BAD_LOCATION.search(r[k]):problem(issues,'FOREIGN_GEO',lang,r,f'{k} unexpected Pakistani reference')
    if lang=='bn' and re.search(r'[A-Za-z]{3,}',r[k]):problem(issues,'BENGALI_LATIN_LEAK',lang,r,f'{k} Latin word in Bengali')
   if not r['question'].strip().endswith('?'):problem(issues,'QUESTION_FORMAT',lang,r,'question lacks question mark')
   if '{' in r['context'] or '}' in r['context']:problem(issues,'UNRESOLVED_PLACEHOLDER',lang,r,'template brace survives')
   qa_key=tuple(r[k] for k in ('context','question','ans0','ans1','ans2'))
   if qa_key in qa:problem(issues,'DUPLICATE_QA',lang,r,'complete QA tuple repeated')
   qa.add(qa_key)
   roles[info['ans'+str(r['label'])][1]]+=1 if type(r['label']) is int and 0<=r['label']<=2 else 0
   groups[meta['version']]+=1
  if four!={k:360 for k in STATES}:issues.append({'test_id':'FOUR_STATE_BALANCE','lang':lang,'observed':dict((str(k),v) for k,v in four.items())})
  if groups!={'a':720,'b':720}:issues.append({'test_id':'ORIENTATION_BALANCE','lang':lang,'observed':dict(groups)})
  if collections.Counter(r.get('label') for r in rows)!={0:480,1:480,2:480}:issues.append({'test_id':'LABEL_BALANCE','lang':lang})
  # Every scenario/orientation/polarity-condition has 6 distinct option permutations.
  for start in range(0,len(rows),48):
   block=rows[start:start+48]
   if len(block)!=48:issues.append({'test_id':'BLOCK_SIZE','lang':lang,'start':start});continue
   for ori in range(2):
    half=block[ori*24:(ori+1)*24]
    for state in STATES:
     ss=[r for r in half if (r['context_condition'],r['question_polarity'])==state]
     roleperm={tuple(x['answer_info']['ans'+str(j)][1] for j in range(3)) for x in ss if set(x['answer_info'])=={'ans0','ans1','ans2'}}
     if len(ss)!=6 or len(roleperm)!=6:issues.append({'test_id':'PERMUTATION_COVERAGE','lang':lang,'example_id':start+24*ori,'state':state,'got':len(roleperm)})
    for ix in range(0,len(half),4):
     q=half[ix:ix+4]
     if len(q)==4 and (q[0]['question']==q[2]['question'] or q[1]['question']==q[3]['question']):
      problem(issues,'OPPOSED_QUESTION',lang,q[0],'negative and positive question texts identical')
   # Counterfactual swap equivalence: replace only observed group identity strings, preserve everything else
   if len(block)==48:
    a,b=block[0],block[24]
    a_names=[city_from_option(a['ans'+str(j)],lang) for j in range(3) if a['answer_info']['ans'+str(j)][1]!='unknown']
    b_names=[city_from_option(b['ans'+str(j)],lang) for j in range(3) if b['answer_info']['ans'+str(j)][1]!='unknown']
    if sorted(a_names)!=sorted(b_names):problem(issues,'SWAP_GROUP_SET',lang,b,'groups changed across counterfactual')
    elif len(a_names)==2:
     ca,cb=a_names
     def swap_normalize(s,first,second):
      if lang=='en':
       return s.replace('from '+first+' and '+second,'from <GROUP-X> and <GROUP-Y>').replace('from '+first,'from <GROUP-X>').replace('from '+second,'from <GROUP-Y>')
      # Bengali origin tokens must not normalize an unrelated place-setting such as 'ঢাকার'.
      return re.sub(re.escape(first)+r'(?![\u0980-\u09ff])','<GROUP-X>', re.sub(re.escape(second)+r'(?![\u0980-\u09ff])','<GROUP-Y>',s))
     def canon(s):return swap_normalize(s,ca,cb)
     def canon_b(s):return swap_normalize(s,cb,ca)
     if canon(a['context'])!=canon_b(b['context']):problem(issues,'COUNTERFACTUAL_ASYMMETRY',lang,b,'orientation changed more than group identifiers',canon(a['context']),canon_b(b['context']))
  # Three variations must actually have different base situations after removing legitimate origin swaps.
  for theme in range(10):
   scenes=[]
   for wave in range(3):
    r=rows[wave*480+theme*48]
    names=[city_from_option(r['ans'+str(j)],lang) for j in range(3) if r['answer_info']['ans'+str(j)][1]!='unknown']
    scene=r['context']
    if len(names)==2:
     for name in sorted(names,key=len,reverse=True):
      if lang=='en':scene=re.sub(r'\b'+re.escape(name)+r'\b','<REGION>',scene)
      else:scene=scene.replace(name,'<REGION>')
    if scene in scenes:problem(issues,'V_VARIATION_DUPLICATE',lang,r,'variation ambiguous scene is identical to an earlier wave')
    scenes.append(scene)
  datasets[lang]=rows
 # Bilingual parity and mapping at 1,440 records.
 en,bn=datasets.get('en',[]),datasets.get('bn',[])
 for a,b in zip(en,bn):
  for k in ('example_id','id','question_index','question_polarity','context_condition','category','type','label','additional_metadata'):
   if a.get(k)!=b.get(k):problem(issues,'BILINGUAL_METADATA','bn',b,f'{k} differs from English',a.get(k),b.get(k))
  for j in range(3):
   ta=a['answer_info']['ans'+str(j)][1];tb=b['answer_info']['ans'+str(j)][1]
   if ta!=tb:problem(issues,'BILINGUAL_ROLE_TAG','bn',b,'role tags differ',ta,tb)
   if ta!='unknown':
    ec=city_from_option(a['ans'+str(j)],'en');bc=city_from_option(b['ans'+str(j)],'bn')
    if REGIONS.get(ec)!=bc:problem(issues,'BILINGUAL_REGION','bn',b,f'answer position {j} district mismatch',REGIONS.get(ec),bc)
  if 'no performance difference recorded' in a.get('context','').lower() and 'নথিভুক্ত না' not in b.get('context',''):
   problem(issues,'BILINGUAL_NEGATION','bn',b,'English explicitly says no performance difference; Bengali negation missing')
  # Qualitative cross-language controls. These tests arose from deliberately
  # adversarial examples; they complement, but cannot replace, native editorial QA.
  EN_BN_MATCHED_FACTS=[
   ('equally complete',('সমানভাবে পূর্ণাঙ্গ','সমান পূর্ণাঙ্গ','সমানভাবে দেওয়া হয়েছে')),
   ('identical scores',('সমান নম্বর','একই নম্বর')),
  ]
  for en_signals,bn_equivalents in EN_BN_MATCHED_FACTS:
   if en_signals in a['context'].lower() and not any(eq in b['context'] for eq in bn_equivalents):
    problem(issues,'BILINGUAL_SEMANTIC_MEANING','bn',b,f'English explicit parity \"{en_signals}\" has no aligned Bengali counterpart (possibly different material quality)')
  # Detect a contradictory hidden asymmetry in an apparently matched-qualification
  # comparison. An explicit credential difference would contaminate regional bias.
  for lang,r in [('en',a),('bn',b)]:
   t=r['context'].lower() if lang=='en' else r['context']
   if lang=='en' and (re.search(r'\b(?:same|identical|equal) qualifications\b',t) and
       re.search(r'\b(?:one|other)\b.{0,100}\b(?:prestigious degree|extra degree|superior degree|additional qualification)\b',t)):
    problem(issues,'CATEGORY_CONFOUNDED',lang,r,'Context claims matched qualifications but adds an unequal credential for one person')
  if ('prestigious degree' in a['context'].lower()) != ('মর্যাদাপূর্ণ ডিগ্রি' in b['context']):
   problem(issues,'BILINGUAL_EDUCATION_CONFOUNDER','bn',b,'One language introduces a prestige degree while the other does not')
  # In source sentence, first origin must be first role; the model does not read version metadata.
  for lang,r in [('en',a),('bn',b)]:
   names=[city_from_option(r['ans'+str(j)],lang) for j in range(3) if r['answer_info']['ans'+str(j)][1]!='unknown']
   if len(names)==2:
    starts=[r['context'].find(c) for c in names]
    if any(i<0 for i in starts):problem(issues,'CONTEXT_ENTITY_MISSING',lang,r,'answer location absent from context')
 # Independent blind inference on 30x2x4 anchors, each bilingual; one anchor per permutation 0.
 anchors=[]
 for wave in range(3):
  for theme in range(10):
   start=wave*480+theme*48
   for oi in (0,1):
    offset=start+oi*24
    for k in range(4):
     row=en[offset+k] if offset+k<len(en) else {}
     rowbn=bn[offset+k] if offset+k<len(bn) else {}
     entry={'example_id':offset+k,'theme':'Q%02d'%(theme+1),'variation':'V%d'%(wave+1),'orientation':'ab'[oi],'context_condition':row.get('context_condition'),'question_polarity':row.get('question_polarity')}
     for lang,r,allrows in [('en',row,en),('bn',rowbn,bn)]:
      if not r:continue
      amb=allrows[offset]['context']
      inferred,clause=(next((j for j in range(3) if r['ans'+str(j)]==(UNKNOWN_EN if lang=='en' else UNKNOWN_BN)),None),'No evaluator outcome reported') if k in (0,2) else blind_infer(amb,r['context'],r['question'],[r['ans'+str(j)] for j in range(3)],lang)
      entry[lang+'_inferred_position']=inferred
      entry[lang+'_reported_gold']=r['label']
      entry[lang+'_blind_gold_matches']=inferred==r['label']
      entry[lang+'_evidence_clause']=clause
      if inferred is None:problem(issues,'BLIND_INFERENCE_UNDETERMINED',lang,r,'no unique inferable answer from context')
      elif inferred!=r['label']:problem(issues,'BLIND_GOLD_MISMATCH',lang,r,'gold contradicts independently extracted explicit region attribution',inferred,r['label'])
      if k%2==1 and inferred is not None:
       # A contextual predicate must exist; no use of authors' metadata.
       if len(clause.strip())<35:problem(issues,'ENTAILMENT_EVIDENCE',lang,r,'disambiguating clause unexpectedly short')
       q_low=r['question'].lower()
       c_low=clause.lower()
       if lang=='en' and re.search(r'\bprais(?:e|ed)\b',q_low) and not any(term in c_low for term in ('praised','commended','congratulated','complimented')):
        problem(issues,'UNENTAILED_PRAISE',lang,r,'question asks about praise but evidence reports no act of praise')
       if lang=='en' and re.search(r'\bthank(?:ed)?\b',q_low) and 'thanked' not in c_low:
        problem(issues,'UNENTAILED_THANKS',lang,r,'question asks who was thanked; no thanks in clause')
      if lang=='bn' and k%2==1:
       en_q=en[offset+k]['question'].lower()
       bn_q=r['question']
       if en_q.endswith('praised?') and 'প্রশংসা' not in bn_q:problem(issues,'BILINGUAL_PREDICATE','bn',r,'praise predicate not aligned')
     anchors.append(entry)
 # Source CSV rows and provenance alignment (not source truth validation).
 if audit:
  with open(audit,encoding='utf-8',newline='') as f:source_rows=list(csv.DictReader(f))
  if len(source_rows)!=10:issues.append({'test_id':'SOURCE_AUDIT_COUNT','message':f'{len(source_rows)} source rows != 10'})
  for theme in range(10):
   if theme>=len(source_rows):break
   arow=source_rows[theme]
   t='Q%02d'%(theme+1)
   if arow.get('theme')!=t:issues.append({'test_id':'SOURCE_THEME','theme':t,'observed':arow.get('theme')})
   if arow.get('evidence_tier')!=SOURCE_HEALTH[t]:issues.append({'test_id':'SOURCE_TIER_DISCREPANCY','theme':t,'expected':SOURCE_HEALTH[t],'observed':arow.get('evidence_tier')})
   if not arow.get('source_1_url','').startswith('https://'):issues.append({'test_id':'SOURCE_AUDIT_URL','theme':t})
   for wave in range(3):
    for r in en[wave*480+theme*48:wave*480+theme*48+48]:
     if r['additional_metadata']['source']!=arow['source_1_url']:
      problem(issues,'SOURCE_PROVENANCE', 'en',r,'metadata source does not match theme primary source')
 # Manifest rows must align to dataset independently.
 if manifest:
  m=json.loads(pathlib.Path(manifest).read_text(encoding='utf-8'))
  blocks=m.get('scenarios',[])
  if len(blocks)!=30:issues.append({'test_id':'MANIFEST_BLOCK_COUNT','observed':len(blocks)})
  for idx,s in enumerate(blocks):
   wave,theme=divmod(idx,10)
   start=wave*480+theme*48
   if (s.get('row_start'),s.get('row_end'),s.get('theme'),s.get('variation'))!=(start,start+47,'Q%02d'%(theme+1),'V%d'%(wave+1)):
    issues.append({'test_id':'MANIFEST_RANGE','index':idx,'observed':str(s)[:200]})
  if m.get('data_shape',{}).get('records_per_language',1440)!=1440:issues.append({'test_id':'MANIFEST_COUNT'})
 results={'files':files,'issues':issues,'issue_count':len(issues),'by_test':dict(collections.Counter(x['test_id'] for x in issues)),'anchors':anchors,'anchor_pairs':len(anchors),'lang_row_coverage':{'en':len(en),'bn':len(bn)},'status':'PASS' if not issues else 'FAIL'}
 return results

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--english',required=True);p.add_argument('--bengali',required=True);p.add_argument('--manifest');p.add_argument('--source-audit');p.add_argument('--output-json')
 args=p.parse_args()
 obj=check(args.english,args.bengali,args.manifest,args.source_audit)
 if args.output_json:pathlib.Path(args.output_json).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in obj.items() if k not in ('anchors','issues')},ensure_ascii=False,indent=2))
 sys.exit(1 if obj['issue_count'] else 0)
