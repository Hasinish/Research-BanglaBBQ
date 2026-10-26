#!/usr/bin/env python3
"""Execute real, isolated, local-only fault injections against two QA suites.

The original dataset files in ORIGINAL are never modified. Detects new validator
failures by subtracting its known baseline defects, to avoid counting baseline
Q10 contradictions as detections of injected faults.
"""
import copy,csv,hashlib,importlib.util,json,pathlib,subprocess,sys,tempfile,shutil,collections
ROOT=pathlib.Path(__file__).resolve().parent;O=ROOT/'ORIGINAL'
spec=importlib.util.spec_from_file_location('ethnicity_independent',ROOT/'Ethnicity_independent_validator.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
E=[json.loads(s) for s in (O/'banglabbq_ethnicity_english.jsonl').read_text(encoding='utf-8').splitlines()]
B=[json.loads(s) for s in (O/'banglabbq_ethnicity_bengali.jsonl').read_text(encoding='utf-8').splitlines()]
baseline=mod.validate(O/'banglabbq_ethnicity_english.jsonl',O/'banglabbq_ethnicity_bengali.jsonl',O/'banglabbq_ethnicity_expansion_manifest.json',O/'banglabbq_ethnicity_source_audit.csv',O/'banglabbq_ethnicity_scenario_templates.json')
def key(z):return (z['test_id'],z['language'],z['row_index'],z['offending_field'])
known=set(map(key,baseline['issues']))
F=[]
def register(id,descr,fn,expect,review=False):F.append((id,descr,fn,expect,review))
register('F01','Flip ambiguous gold label',lambda e,b,m,s:e[0].update(label=0),'BLIND_GOLD_LABEL')
register('F02','Flip disambiguated gold label',lambda e,b,m,s:e[1].update(label=1),'BLIND_GOLD_LABEL')
def swap_no_relabel(e,b,m,s):e[1]['ans0'],e[1]['ans1']=e[1]['ans1'],e[1]['ans0']
register('F03','Swap two English answers without remapping labels or tags',swap_no_relabel,'ANSWERINFO_TEXT_PARITY')
register('F04','Corrupt semantic group tag',lambda e,b,m,s:e[1]['answer_info']['ans0'].__setitem__(1,'ethnic_bengali'),'ANSWER_ROLES_COLLIDE')
def duplicate_full(e,b,m,s):
 for f in ('context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','context_condition','question_polarity'):e[4][f]=copy.deepcopy(e[0][f])
register('F05','Make a complete QA tuple duplicate with new ID',duplicate_full,'EXACT_QA_DUPLICATE')
register('F06','Delete last English record',lambda e,b,m,s:e.pop(),'TOTAL_RECORD_COUNT')
register('F07','Swap two row positions and break canonical order',lambda e,b,m,s:e.__setitem__(slice(0,2),list(reversed(e[:2]))),'FOUR_CONDITION_CANONICAL_ORDER')
register('F08','Duplicate numeric provisional ID',lambda e,b,m,s:e[15].update(id=e[14]['id']),'DUPLICATE_ID')
register('F09','Invalid counterfactual version c',lambda e,b,m,s:e[20]['additional_metadata'].update(version='c'),'VERSION_ENUM')
register('F10','Replace category with Regional',lambda e,b,m,s:e[20].update(category='Regional'),'CATEGORY_TOKEN')
register('F11','Remove theme source URL',lambda e,b,m,s:e[20]['additional_metadata'].update(source=''),'SOURCE_URL_FORMAT')
register('F12','Replace citation with unrelated valid HTTPS string',lambda e,b,m,s:e[20]['additional_metadata'].update(source='https://example.org/another-topic'),'SOURCE_URL_THEME_CONSISTENCY')
def bng_entity_swap(e,b,m,s):
 for field in ('ans0',):b[0][field]=b[0][field].replace('মুণ্ডা','চাকমা')
 b[0]['answer_info']['ans0'][0]=b[0]['ans0']
register('F13','Swap only Bengali ethnic name while keeping same role tags',bng_entity_swap,'CROSS_LANGUAGE_ETHNIC_NAME')
register('F14','Remove Bengali negative outcome from question',lambda e,b,m,s:b[0].update(question=b[0]['question'].replace('পায়নি','পেয়েছে')),'PERMUTATION_TEXT_INVARIANCE')
register('F15','Replace explicit outcome with unentailed praise question',lambda e,b,m,s:e[1].update(question='Which student was praised as a genius?'),'BLIND_CONTEXT_ENTAILMENT')
register('F16','Add unequal work experience to only one counterfactual orientation',lambda e,b,m,s:e[24].update(context=e[24]['context']+' Student B has five years of extra experience.'),'COUNTERFACTUAL_CONTEXT_NONETHNIC_CHANGE')
register('F17','Leak explicit adverse/favorable outcome into ambiguous context',lambda e,b,m,s:e[0].update(context=e[0]['context']+' The coordinator recorded that student A was denied a place in the reading circle, whereas student B was given a place in the reading circle.'),'BLIND_GOLD_LABEL')
def collide_options(e,b,m,s):e[0]['ans0']=e[0]['ans1'];e[0]['answer_info']['ans0'][0]=e[0]['ans0']
register('F18','Conflate both English answer identities',collide_options,'DUPLICATE_OPTIONS')
register('F19','Replace Satkhira with Lahore in one English context',lambda e,b,m,s:e[0].update(context=e[0]['context'].replace('Satkhira','Lahore')),'PAKISTANI_CULTURAL_LEAK')
def audit_source_blank(e,b,m,s):
 s[1]['source_1_url']=''
register('F20','Remove Q02 source URL from independent audit table',audit_source_blank,'SOURCE_AUDIT_MISSING_URL')
def clone_v1_as_v3(e,b,m,s):
 for i in range(960,1008):
  a=e[i];x=e[(i-960) % 48];
  for k in ('context','question'):a[k]=x[k]
register('F21','Duplicate V1 theme-Q01 texts as V3 without updating metadata',clone_v1_as_v3,'EXACT_QA_DUPLICATE')
register('F22','Inject asymmetric age/competence confound',lambda e,b,m,s:e[24].update(context=e[24]['context']+' Student B is twenty years older and has professional training.'),'COUNTERFACTUAL_CONTEXT_NONETHNIC_CHANGE')
register('F23','Remove Bengali disambiguated outcome negation',lambda e,b,m,s:b[1].update(context=b[1]['context'].replace('জায়গা পায়নি','জায়গা পেয়েছে')),'BLIND_CONTEXT_ENTAILMENT')
register('F24','Insert invisible U+200B into question',lambda e,b,m,s:e[2].update(question=e[2]['question']+'\u200b'),'TEXT_CONTROL')
register('F25','Set integer gold label to boolean',lambda e,b,m,s:e[0].update(label=True),'SCHEMA_TYPE')
def fake_source_everywhere(e,b,m,s):
 url='https://example.org/unrelated-study'
 for seq in (e,b):
  for x in seq:
   if x['question_index']=='7':x['additional_metadata']['source']=url
 s[6]['source_1_url']=url
register('F26','Coordinated false source substitution across both JSONLs and audit CSV',fake_source_everywhere,'EXPERT_SOURCE_REOPEN',True)
def overstate_sources(e,b,m,s):
 # Keep 4 DIRECT overall so count-only checks will miss inflated evidence strength.
 s[6]['evidence_tier']='DIRECT';s[4]['evidence_tier']='PARTIAL'
register('F27','Swap source tiers (Q07 falsely DIRECT and Q05 falsely PARTIAL)',overstate_sources,'EXPERT_EVIDENCE_TIER_REVIEW',True)
def remove_negation_in_question(e,b,m,s):
 b[1]['question']=b[1]['question'].replace('পায়নি','পেয়েছে')
register('F28','Flip Bengali disambiguated polarity by removing negation',remove_negation_in_question,'BLIND_GOLD_LABEL')
register('F29','Corrupt manifest row range while retaining JSONL',lambda e,b,m,s:m['blocks'][0].update(row_index_0_based_end_inclusive=700),'MANIFEST_RANGE')
def add_religion_confound(e,b,m,s):
 b[24]['context']=b[24]['context'].replace('মুণ্ডা জনগোষ্ঠীর','হিন্দু মুণ্ডা জনগোষ্ঠীর',1)
register('F30','Add one-sided religious qualifier in Bengali counterfactual',add_religion_confound,'COUNTERFACTUAL_CONTEXT_NONETHNIC_CHANGE')

results=[]
with tempfile.TemporaryDirectory(prefix='eth_forensic_injections_') as tmp:
 t=pathlib.Path(tmp)
 for fid,description,mutate,expected,expert in F[int(sys.argv[1]):int(sys.argv[2])]:
  e=copy.deepcopy(E);b=copy.deepcopy(B);m=json.loads((O/'banglabbq_ethnicity_expansion_manifest.json').read_text(encoding='utf-8'))
  with (O/'banglabbq_ethnicity_source_audit.csv').open(encoding='utf-8',newline='') as f:
   reader=csv.DictReader(f);fields=reader.fieldnames;s=list(reader)
  try:mutate(e,b,m,s)
  except Exception as exc:results.append({'fixture':fid,'injection':description,'injection_execution':'FAILED','error':str(exc)});continue
  d=t/fid;d.mkdir()
  for lang,data,fn in [('en',e,'banglabbq_ethnicity_english.jsonl'),('bn',b,'banglabbq_ethnicity_bengali.jsonl')]:
   with (d/fn).open('w',encoding='utf-8',newline='\n') as f:
    for x in data:f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
  (d/'banglabbq_ethnicity_expansion_manifest.json').write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8')
  (d/'banglabbq_ethnicity_scenario_templates.json').symlink_to(O/'banglabbq_ethnicity_scenario_templates.json')
  (d/'banglabbq_ethnicity_pakbbq_theme_crosswalk.csv').symlink_to(O/'banglabbq_ethnicity_pakbbq_theme_crosswalk.csv')
  with (d/'banglabbq_ethnicity_source_audit.csv').open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(s)
  shutil.copy2(O/'validate_ethnicity_independent.py', d/'validate_ethnicity_independent.py')
  original=subprocess.run([sys.executable,str(d/'validate_ethnicity_independent.py')],capture_output=True,text=True,cwd=d,timeout=35)
  independent=mod.validate(d/'banglabbq_ethnicity_english.jsonl',d/'banglabbq_ethnicity_bengali.jsonl',d/'banglabbq_ethnicity_expansion_manifest.json',d/'banglabbq_ethnicity_source_audit.csv',d/'banglabbq_ethnicity_scenario_templates.json')
  newissues=[z for z in independent['issues'] if key(z) not in known]
  det=any(z['test_id']==expected for z in newissues) if not expert else False
  manual=bool(expert and (fid in ('F26','F27')))  # Outside-source expert verification, not automation.
  res={'fixture_id':fid,'description':description,'executed':True,'expected_detection':expected,
       'existing_validator_detected_any_failure':original.returncode!=0,
       'existing_validator_returncode':original.returncode,
       'existing_validator_failure_excerpt':(original.stderr or original.stdout)[-200:][:180],
       'independent_detected_expected_check':det,
       'independent_detected_any_NEW_failure':len(newissues)>0,
       'independent_new_issue_count':len(newissues),
       'independent_new_test_ids':dict(collections.Counter(z['test_id'] for z in newissues)),
       'expert_review_oracle_detects':manual,
       'detected_by_combined_procedure':det or manual,
       'injection_execution':'SUCCESS'}
  results.append(res)
report={'baseline_existing_returncode':0,'baseline_independent_issues':len(known),
        'fixture_count':len(results),'executed_count':sum(z.get('executed',False) for z in results),
        'existing_validator_detected_count':sum(z.get('existing_validator_detected_any_failure',False) for z in results),
        'independent_expected_detection_count':sum(z.get('independent_detected_expected_check',False) for z in results),
        'combined_detected_count':sum(z.get('detected_by_combined_procedure',False) for z in results),
        'undetected_fixture_ids':[z['fixture_id'] for z in results if not z.get('detected_by_combined_procedure',False)],
        'false_positive_baseline_qa':False,
        'fixtures':results}
(ROOT/f'Ethnicity_adversarial_results_{sys.argv[1]}_{sys.argv[2]}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='fixtures'},ensure_ascii=False,indent=2))
for r in results:print(r.get('fixture_id'),r.get('existing_validator_detected_any_failure'),r.get('independent_new_test_ids'),r.get('detected_by_combined_procedure'))
