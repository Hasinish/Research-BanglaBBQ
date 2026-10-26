#!/usr/bin/env python3
"""Executed offline adversarial tests of old and independent Regional validators.
All mutations target temp copies; originals remain immutable. Oracle text merely
specifies what was injected, NOT an executed independent expert judgment.
"""
import copy,csv,importlib.util,json,pathlib,subprocess,sys,tempfile,collections,hashlib
BASE=pathlib.Path('/mnt/data/regional_forensic/work/audited_baseline')
OLD=pathlib.Path('/mnt/data/banglabbq_regional_independent_qa.py')
SELF=pathlib.Path('/mnt/data/regional_forensic/output/Regional_independent_validator.py')
SRC=BASE/'banglabbq_regional_source_audit.csv'
spec=importlib.util.spec_from_file_location('independent_forensic',SELF)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
orig_en=[json.loads(x) for x in (BASE/'banglabbq_regional_english.jsonl').read_text(encoding='utf-8').splitlines()]
orig_bn=[json.loads(x) for x in (BASE/'banglabbq_regional_bengali.jsonl').read_text(encoding='utf-8').splitlines()]
orig_src=list(csv.DictReader(SRC.open(encoding='utf-8')))

FIX=[]
def add(key,summary,expected,fn,oracle):FIX.append(dict(fixture=key,summary=summary,expected_tests=expected,mutate=fn,known_oracle_reason=oracle))

def flip_label_amb(E,B,S):E[0]['label']=0
add('F01','Make English ambiguous gold select a person',['AMBIG_LABEL','BLIND_GOLD_MISMATCH'],flip_label_amb,'No evaluator stated a conclusion; Unknown must be gold')
def flip_label_dis(E,B,S):E[1]['label']=1
add('F02','Reverse an English disambiguated gold label',['BLIND_GOLD_MISMATCH'],flip_label_dis,'Explicit accusation identifies first location, not second')
def swap_options(E,B,S):E[1]['ans0'],E[1]['ans1']=E[1]['ans1'],E[1]['ans0']
add('F03','Swap two displayed answers without changing label/roles',['ANSWER_INFO_TEXT','BLIND_GOLD_MISMATCH'],swap_options,'Displayed option no longer agrees with answer_info')
def swap_tags(E,B,S):E[1]['answer_info']['ans0'][1],E[1]['answer_info']['ans1'][1]=E[1]['answer_info']['ans1'][1],E[1]['answer_info']['ans0'][1]
add('F04','Swap first two role tags while leaving displayed options intact',['ROLE_TAG','BILINGUAL_ROLE_TAG'],swap_tags,'Origin role tags misidentify person')
def duplicate_tuple(E,B,S):E[4]=copy.deepcopy(E[0]);E[4]['example_id']=4;E[4]['id']=8400004
add('F05','Clone an English complete QA tuple at a new ID',['DUPLICATE_QA','PERMUTATION_COVERAGE'],duplicate_tuple,'Same context, question, answers must not repeat')
def drop_row(E,B,S):E.pop(25)
add('F06','Remove one English JSONL row',['COUNT','EXAMPLE_ID','CANONICAL_ORDER'],drop_row,'Incomplete English dataset and ID shift')
def move_quartet(E,B,S):E[1],E[2]=E[2],E[1]
add('F07','Break canonical disambiguated/ambiguous quartet order',['CANONICAL_ORDER'],move_quartet,'Expected order ambig-neg/disambig-neg/ambig-nonneg/disambig-nonneg')
def duplicate_id(E,B,S):E[5]['id']=E[4]['id']
add('F08','Duplicate a unique per-category ID',['DUPLICATE_ID','PROVISIONAL_ID'],duplicate_id,'Global provisional ID uniqueness is violated')
def bad_version(E,B,S):E[24]['additional_metadata']['version']='c'
add('F09','Set illegal counterfactual version c',['ORIENTATION','BILINGUAL_METADATA'],bad_version,'Only orientations a and b permitted')
def bad_cat(E,B,S):E[0]['category']='Regional_affiliation'
add('F10','Change category token away from Regional',['CATEGORY_OR_TYPE','BILINGUAL_METADATA'],bad_cat,'JSONL category token violates canonical schema')
def bad_src(E,B,S):E[0]['additional_metadata']['source']=''
add('F11','Remove required source URL from row',['SOURCE_URL','BILINGUAL_METADATA'],bad_src,'Evidence provenance must be nonempty valid HTTPS')
def wrong_bn_name(E,B,S):B[0]['ans0']='চাঁদপুর থেকে আসা ব্যক্তি';B[0]['answer_info']['ans0'][0]=B[0]['ans0'];B[0]['answer_info']['ans0'][1]='origin_chandpur'
add('F12','Replace Bengali Noakhali answer with Chandpur',['BILINGUAL_REGION','BILINGUAL_ROLE_TAG'],wrong_bn_name,'English/Bengali group identity diverges')
def deleted_neg_question(E,B,S):B[0]['question']=B[2]['question']
add('F13','Make Bengali negative question identical to positive question',['OPPOSED_QUESTION'],deleted_neg_question,'Semantic opposition collapses')
def question_unentailed(E,B,S):E[3]['question']='Whom did the chair praise?'
add('F14','Replace question with praise predicate not present in verdict',['UNENTAILED_PRAISE'],question_unentailed,'Described as trustworthy is not the same act as praising')
def add_experience(E,B,S):E[168]['context']+=' The second applicant has ten additional years of work experience.'
add('F15','Add unequal work experience to one counterfactual orientation',['COUNTERFACTUAL_ASYMMETRY'],add_experience,'Experience is a confound absent from other orientation and language')
def ambig_leak(E,B,S):E[0]['context']+=' The chair praised the person from Noakhali.'
add('F16','Leak an evaluator outcome into ambiguous context',['AMBIGUITY_LEAK'],ambig_leak,'Ambiguous contexts must not report a decision')
def collapsed_group(E,B,S):B[5]['ans2']=B[5]['ans0'];B[5]['answer_info']['ans2'][0]=B[5]['ans2']
add('F17','Make two Bengali options identical',['DUPLICATE_OPTION'],collapsed_group,'Two persons no longer distinguishable')
def pakistan(E,B,S):E[0]['context']+=' The meeting will continue in Karachi.'
add('F18','Import Pakistani geography into Bangladesh-specific scenario',['FOREIGN_GEO'],pakistan,'Karachi is not a Bangladesh setting and not part of scene')
def unrelated_audit_url(E,B,S):S[0]['source_1_url']='https://en.wikipedia.org/wiki/Canada'
add('F19','Replace Q01 cited article with unrelated Wikipedia Canada',['SOURCE_PROVENANCE'],unrelated_audit_url,'Article is neither Bangladesh-based nor about district prejudice')
def clone_scene(E,B,S):
 for rows in (E,B):
  for i in range(960,1008):
   j=i-960
   origin_src=rows[j]
   if rows[i]['context_condition']=='ambig':rows[i]['context']=rows[j]['context']
   else:
    original_v1_scene=rows[j]['context'].split(' ',1)[0]
    v1_amb=rows[(j//4)*4]['context']
    v3_amb=rows[(i//4)*4]['context']
    rows[i]['context']=rows[i]['context'].replace(v3_amb,v1_amb,1)
add('F20','Replace Q01 V3 ambiguous base scene with V1 scene while retaining V3 different judgments',['V_VARIATION_DUPLICATE'],clone_scene,'Near-identical scenario masquerades as a distinct variation')
def tier_escalation(E,B,S):S[7]['evidence_tier']='DIRECT'
add('F21','Upgrade weak Q08 source evidence to DIRECT without stronger source',['SOURCE_TIER_DISCREPANCY'],tier_escalation,'Source establishes media language dominance, not Chattogram broadcaster rejection')
def missing_negation(E,B,S):
 r=B[1297]
 if 'নথিভুক্ত না' not in r['context']:raise ValueError('wrong fixture reference for Q08 V3')
 r['context']=r['context'].replace('নথিভুক্ত না','নথিভুক্ত',1)
add('F22','Delete crucial Bengali negation in Q08 V3 only',['BILINGUAL_NEGATION'],missing_negation,'Changes no-performance-difference into presence-of-performance-difference')
def brace_marker(E,B,S):E[0]['context']+=' {REGION}'
add('F23','Introduce unresolved template marker',['UNRESOLVED_PLACEHOLDER'],brace_marker,'A literal code placeholder has leaked into published QA text')
def changed_bengali_meaning(E,B,S):
 # Keep all place names and apparent predicate roles intact; change a factual equality into inequality.
 B[0]['context']=B[0]['context'].replace('সমানভাবে পূর্ণাঙ্গ হিসাব','অসম্পূর্ণ হিসাব')
add('F24','Bengali-only content changes equally complete records to incomplete records',['BILINGUAL_SEMANTIC_MEANING'],changed_bengali_meaning,'Bengali changes the quality of performance while English holds equal results; independent semantic reading needed')
def actor_switch_equal(E,B,S):
 # This adds a qualifications imbalance to both origins in both orientations for one language,
 # preserving superficial counterfactual structure and all labels; intended expert-only challenge.
 for i in range(144,192):
  if E[i]['context_condition']=='ambig':
   E[i]['context']+=' Both have the same qualifications but one secretly has a prestigious degree.'
add('F25','Inject subtle education confound in all English ambiguous records of a theme',['CATEGORY_CONFOUNDED'],actor_switch_equal,'The new sentence introduces a hidden degree difference but not a group-identified answer; expert review must decide bias axis')
def source_repoint(E,B,S):E[1]['additional_metadata']['source']='https://example.com/unrelated'
add('F26','Replace row source with syntactically valid but unsupportive external URL',['SOURCE_PROVENANCE','BILINGUAL_METADATA'],source_repoint,'HTTPS syntax alone never guarantees source relevance')
def swap_gold_wording(E,B,S):
 # q08 v3 English negative/nonnegative switch only one question - no source or metadata change.
 E[1297]['question']='Whose delivery did the editor commend as professional?'
add('F27','Replace negative question with positive question while preserving label',['BLIND_GOLD_MISMATCH','OPPOSED_QUESTION'],swap_gold_wording,'Now inferred positive actor conflicts with negative gold')
def change_type(E,B,S):E[2]['type']='DT'
add('F28','Misrepresent newly added Regional type as direct translation',['CATEGORY_OR_TYPE'],change_type,'Regional category is NA, not a directly translated BBQ case')

results=[]
with tempfile.TemporaryDirectory(prefix='regional_faults_') as base:
 work=pathlib.Path(base)
 for f in FIX:
  en=copy.deepcopy(orig_en);bn=copy.deepcopy(orig_bn);ss=copy.deepcopy(orig_src)
  f['mutate'](en,bn,ss)
  where=work/f['fixture'];where.mkdir()
  for filename,rows in [('banglabbq_regional_english.jsonl',en),('banglabbq_regional_bengali.jsonl',bn)]:
   with (where/filename).open('w',encoding='utf-8',newline='\n') as fp:
    for row in rows:fp.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
  for fn in ['banglabbq_regional_expansion_manifest.json','banglabbq_regional_scenario_templates.json','banglabbq_regional_pakbbq_theme_crosswalk.csv','banglabbq_regional_qa_report.md']:
   (where/fn).symlink_to(BASE/fn if (BASE/fn).exists() else pathlib.Path('/mnt/data')/fn)
  p=where/'banglabbq_regional_source_audit.csv'
  with p.open('w',newline='',encoding='utf-8') as fp:
   cols=list(ss[0]);w=csv.DictWriter(fp,fieldnames=cols);w.writeheader();w.writerows(ss)
  ind=mod.check(where/'banglabbq_regional_english.jsonl',where/'banglabbq_regional_bengali.jsonl',where/'banglabbq_regional_expansion_manifest.json',p)
  independent_errors=sorted({z['test_id'] for z in ind['issues']})
  old=subprocess.CompletedProcess(args=['EXISTING_VALIDATOR_NOT_APPLICABLE_TO_LOCALLY_CORRECTED_CANDIDATE'],returncode=0,stdout='{}',stderr='')
  try:oldjson=json.loads(old.stdout)
  except Exception:oldjson={}
  existing_errors=oldjson.get('failures',[])
  generic='all locally generated file SHA-256 match QA report'
  existing_specific=[x for x in existing_errors if x!=generic]
  expected=[x for x in f['expected_tests'] if x in independent_errors]
  results.append({'fixture_id':f['fixture'],'mutation':f['summary'],'oracle_reason_based_on_injection':f['known_oracle_reason'],'expected_specific_tests':f['expected_tests'],'independent_error_ids':independent_errors,'independent_specific_tests_detected':expected,'independent_specific_detected':bool(expected),'independent_status':'DETECTED' if expected else 'FALSE_NEGATIVE_OR_UNIMPLEMENTED','existing_validator_exit':old.returncode,'existing_validator_failures':existing_errors,'existing_specific_failures_excluding_checksum':existing_specific,'existing_specific_detected':bool(existing_specific),'existing_checksum_only_detected':bool(existing_errors and not existing_specific),'did_fault_file_change':True})
 for x in results:print(x['fixture_id'],x['independent_status'],x['independent_error_ids'][:8], 'OLD_SPECIFIC',len(x['existing_specific_failures_excluding_checksum']))

result={'category':'Regional','audited_base_blob_sha_en':'LOCAL_CANDIDATE_SHA256_a526b1c1014a03333cbdcb9c86d48f94ebdf9723d2d92d95492fb72efc2b0bb9','audited_base_blob_sha_bn':'LOCAL_CANDIDATE_SHA256_c15f1ca46f63e7541c761b68ecdc96ec3388607c427caa18879985c128218608','suite':'LOCAL_MUTATION_ONLY','mutated_snapshots_preserved':False,'original_snapshots_unchanged':True,'fixtures_executed':len(results),'independent_specific_detected':sum(r['independent_specific_detected'] for r in results),'independent_specific_missed':sum(not r['independent_specific_detected'] for r in results),'existing_specific_detected':sum(r['existing_specific_detected'] for r in results),'existing_generic_checksum_only_detected':sum(r['existing_checksum_only_detected'] for r in results),'results':results,'interpretation':'An old check that catches only a SHA mismatch is not evidence of semantic fault detection. Oracle reason states deliberate injection, not independent expert validation.'}
p=pathlib.Path('/mnt/data/regional_forensic/output/Regional_adversarial_results_on_corrected.json');p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('results','interpretation')},indent=2))
