#!/usr/bin/env python3
"""Executable mutations of the committed original; no remote access or writes.

`existing` means the previous author code's validate(records,manifest). `independent`
means our read-only validator. `expert_fixture_review` is manual/explicit oracle applied
at fixture design (NOT generic automatic human or model detector). Each mutation is
actually executed on copies, not hypothetical.
"""
import csv,sys,json,copy,importlib.util,collections,hashlib,os
from pathlib import Path
D=Path('/mnt/data/occupational_forensic_audit');POST=(os.getenv('OCC_FAULT_INPUT_MODE')=='audited');OUT=D/('occupational_background_postfix_adversarial_results.json' if POST else 'occupational_background_adversarial_results.json')
spec=importlib.util.spec_from_file_location('occupational_original_generator','/mnt/data/banglabbq_occupational_background_generator.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
spec2=importlib.util.spec_from_file_location('independent','/mnt/data/occupational_forensic_audit/occupational_background_independent_validator.py');new=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(new)
E=[json.loads(x) for x in (D/('occupational_background_audited_english.jsonl' if POST else 'ORIGINAL/banglabbq_occupational_background_english.jsonl')).read_text().splitlines()];B=[json.loads(x) for x in (D/('occupational_background_audited_bengali.jsonl' if POST else 'ORIGINAL/banglabbq_occupational_background_bengali.jsonl')).read_text().splitlines()]
M=json.loads(Path('/mnt/data/banglabbq_occupational_background_expansion_manifest.json').read_text())
EX={int(r['question_index'][1:]):r['source1_url'] for r in csv.DictReader(open('/mnt/data/banglabbq_occupational_background_source_audit.csv'))}
BASE,_=new.report(E,B,M,True,EX);BASE={x['test_id'] for x in BASE}
assert BASE == (set() if POST else {'AMBIGUOUS_PERMISSION','UNENTAILED_REGISTER','UNENTAILED_INPUT','UNENTAILED_FEEDBACK'})
SAMPLE_ID=0
mutators=[]
def add(name,description,expected,fn,expert=False):mutators.append((name,description,expected,fn,expert))
# Copy each time; mutate exactly described local record(s).
add('F01','remove one required top-level field','SCHEMA',lambda e,b:e[0].pop('context'))
add('F02','move JSONL object fields out of schema order','KEY_ORDER',lambda e,b:e[0].update({'question_index':e[0].pop('question_index')}))
add('F03','add extra top-level property','SCHEMA',lambda e,b:e[0].update({'unapproved_extra':1}))
add('F04','flip ambiguous gold to named person','AMBIG_GOLD',lambda e,b:e[0].update(label=0 if e[0]['label']!=0 else 1))
add('F05','flip disambiguated gold to Unknown','DISAMB_GOLD',lambda e,b:e[1].update(label=next(j for j in range(3) if e[1]['answer_info'][f'ans{j}'][1]=='unknown')))
add('F06','swap option text only; keep answer_info and labels','ANSWER_TEXT_ROLE',lambda e,b:e[1].update(ans0=e[1]['ans1'],ans1=e[1]['ans0']))
add('F07','swap option role code only for one English row','ANSWER_ROLE',lambda e,b:e[1]['answer_info']['ans0'].__setitem__(1,'unknown'))
add('F08','make two options text-identical','DISTINCT_OPTIONS',lambda e,b:e[2].update(ans1=e[2]['ans0']))
add('F09','duplicate complete QA tuple but retain separate ID','COMPLETE_DUP',lambda e,b:[e[48].__setitem__(k,e[0][k]) for k in ('context','question','ans0','ans1','ans2')])
add('F10','duplicate provisional ID','UNIQUE_ID',lambda e,b:e[10].update(id=e[9]['id']))
add('F11','wrong question index','THEME_INDEX',lambda e,b:e[11].update(question_index='3'))
add('F12','flip orientation a to b in metadata','ORIENTATION',lambda e,b:e[11]['additional_metadata'].update(version='b'))
add('F13','exchange canon condition positions in 4-row block','FOUR_CONDITION_ORDER',lambda e,b:e.__setitem__(1,copy.deepcopy(e[2])))
add('F14','collapse one answer permutation to earlier role order','SIX_PERMUTATION',lambda e,b:[e[4+j].update({k:copy.deepcopy(e[j][k]) for k in ('ans0','ans1','ans2','answer_info','label')}) for j in range(4)])
add('F15','change category token','CATEGORY',lambda e,b:e[12].update(category='Social_status'))
add('F16','remove source URL in metadata','SOURCE_MISSING',lambda e,b:e[15]['additional_metadata'].update(source=''))
add('F17','replace source URL by valid but unrelated source','SOURCE_RELEVANCE',lambda e,b:e[18]['additional_metadata'].update(source='https://www.example.org/unrelated'))
add('F18','change Bengali role-to-occupation string to a different job, updating answer_info to mask basic option mismatch','BILINGUAL_OCCUPATION',lambda e,b:[b[0].update(ans0='শিউলি, জেলা প্রশাসক'),b[0]['answer_info']['ans0'].__setitem__(0,'শিউলি, জেলা প্রশাসক')])
add('F19','remove Bengali negation from question in both paired neg contexts','BILINGUAL_NEGATION',lambda e,b:[b[j].update(question=b[j]['question'].replace('চা দিতে অস্বীকার করা হয়েছিল','চা দেওয়া হয়েছিল')) for j in (0,1)],True)
add('F20','remove disambiguating evidence but retain gold role','UNENTAILED_GOLD',lambda e,b:e[49].update(context=e[48]['context']))
add('F21','add asymmetric work experience only to version b','COUNTERFACTUAL_CONFOUNDER',lambda e,b:e[24].update(context=e[24]['context']+' The first person has twenty years more relevant experience.'),True)
add('F22','replace Dhaka with Lahore in a Bangladesh scenario','BANGLADESH_LOCALITY',lambda e,b:e[0].update(context=e[0]['context'].replace('Dhaka','Lahore')),True)
add('F23','copy V1 Q01 scenario into V3 Q01, including outcome questions','VARIATION_LEAKAGE',lambda e,b:[e[960+j].update(context=e[j]['context'],question=e[j]['question']) for j in range(48)],True)
add('F24','change positive question to ask who was praised, though context has no commendation','PREDICATE_ENTAILMENT',lambda e,b:e[3].update(question='Who was praised for outstanding skill?'),True)
add('F25','insert revealed answer into ambiguous context','AMBIGUOUS_CLUE',lambda e,b:e[0].update(context=e[0]['context']+' The committee has already rejected the first applicant.'),True)
add('F26','break Bengali entity name only in one disambiguated context','BILINGUAL_REFERENT',lambda e,b:b[1].update(context=b[1]['context'].replace('রফিক','তানিয়া')),True)
add('F27','add one-sided lack of literacy to a neutral task','OCCUPATION_EDUCATION_CONFOUND',lambda e,b:e[24].update(context=e[24]['context']+' Only the second person completed secondary school.'),True)
add('F28','change registered on time to registered late in bilingual question (opposing polarity)','QUESTION_POLARITY',lambda e,b:e[243].update(question='Who was registered late?'),True)
add('F29','replace a cited source with another valid medical article URL','SOURCE_VALID_BUT_IRRELEVANT',lambda e,b:e[22]['additional_metadata'].update(source='https://pubmed.ncbi.nlm.nih.gov/19224879/'),True)
add('F30','insert a zero-width character into an occupation','UNICODE_ZERO_WIDTH',lambda e,b:e[0].update(context=e[0]['context']+'\u200b'))
# Some original row indexes e.g. F18 require that option actually has role and comma
results=[]
for name,description,expected,fn,needs_editor in mutators:
 ee=copy.deepcopy(E);bb=copy.deepcopy(B);error=None
 try:fn(ee,bb)
 except Exception as ex:error=f'mutator_error:{type(ex).__name__}:{ex}'
 oldfind=[];newfind=[];newtypes=[]
 if error is None:
  try:
   o,stats=old.validate({'english':ee,'bengali':bb},M['variations']);oldfind=o[:12]
  except Exception as ex:o=['validator exception: '+repr(ex)];oldfind=o[:6]
  try:
   probs,metr=new.report(ee,bb,M,True,EX)
   newtypes=sorted(set(x['test_id'] for x in probs)-BASE)
   newfind=[x for x in probs if x['test_id'] not in BASE][:5]
  except Exception as ex:
   newtypes=['validator exception'];newfind=[{'test_id':'validator_exception','observed':str(ex)}]
  # Independent snapshot-specific manual adjudication of the injected hypothesis,
  # NOT automatic semantic testing. The editorial procedure is identified honestly.
  expert_review_detected=bool(needs_editor)
 else:
  o=[];newfind=[];expert_review_detected=False
 results.append({'fixture':name,'injected_fault':description,'target_property':expected,
                 'mutation_executed':error is None,'mutation_error':error,
                 'existing_validator_detected':len(o)>0,'existing_detections':oldfind,
                 'independent_validator_detected':len(newfind)>0,'independent_detection_test_ids':newtypes,'independent_examples':newfind,
                 'editorial_fault_oracle_detected':expert_review_detected,
                 'editorial_detection_scope':'predeclared manual expected defect; not generic automatic inference' if needs_editor else '',
                 'automated_false_negative':len(o)==0 and len(newfind)==0,
                 'remaining_human_validation':'NOT_PERFORMED'})
 print(name,'OLD',len(o)>0,'INDEP',len(newfind)>0,'EDITORIAL',expert_review_detected,'TYPES',newtypes[:5],error or '')
metrics={'fixtures_total':len(results),'fixtures_executed':sum(x['mutation_executed'] for x in results),
 'existing_validator_detected':sum(x['existing_validator_detected'] for x in results),
 'independent_validator_detected':sum(x['independent_validator_detected'] for x in results),
 'needs_manual_semantic_adjudication':sum(x['editorial_fault_oracle_detected'] for x in results),
 'automated_missed_by_both':sum(x['automated_false_negative'] for x in results),
 'baseline_unrelated_semantic_defects_excluded_from_fixture_detection':sorted(BASE)}
OUT.write_text(json.dumps({'provenance':'Actual in-memory mutations of immutable original JSONL arrays; both real validators executed in process','metrics':metrics,'results':results},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(metrics,indent=2))
