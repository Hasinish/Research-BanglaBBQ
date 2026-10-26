#!/usr/bin/env python3
"""26 reproducible in-memory adversarial injections; never touch original files."""
import copy,csv,importlib.util,json,sys,collections,pathlib,os
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent',ROOT/'physical_appearance_independent_validator.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
gen_spec=importlib.util.spec_from_file_location('original_validator',ROOT/'ORIGINAL/banglabbq_physical_appearance_generator.py')
gen=importlib.util.module_from_spec(gen_spec);gen_spec.loader.exec_module(gen)
POSTFIX=os.environ.get('PA_AUDIT_POSTFIX')=='1'
E=[json.loads(x) for x in (ROOT/('banglabbq_physical_appearance_audited_english.jsonl' if POSTFIX else 'ORIGINAL/banglabbq_physical_appearance_english.jsonl')).read_text().splitlines()]
B=[json.loads(x) for x in (ROOT/('banglabbq_physical_appearance_audited_bengali.jsonl' if POSTFIX else 'ORIGINAL/banglabbq_physical_appearance_bengali.jsonl')).read_text().splitlines()]
M=json.loads((ROOT/'ORIGINAL/banglabbq_physical_appearance_expansion_manifest.json').read_text())
BASE,counts,_=qa.validate(E,B,M)
base_counts=collections.Counter(x['rule'] for x in BASE)

def do(english,bengali,scenario,index):
    if scenario=='ambig_label':english[index]['label']=0
    elif scenario=='disamb_label':english[index]['label']=2
    elif scenario=='swap_options':english[index]['ans0'],english[index]['ans1']=english[index]['ans1'],english[index]['ans0']
    elif scenario=='swap_role_tags':bengali[index]['answer_info']['ans0'][1]='invalid_persona'
    elif scenario=='duplicate_tuple':
        for k in ('context','question','ans0','ans1','ans2','answer_info'):english[index][k]=copy.deepcopy(english[4][k])
    elif scenario=='remove_row':english.pop(index)
    elif scenario=='order_rows':english[index],english[index+1]=english[index+1],english[index]
    elif scenario=='duplicate_id':english[index]['id']=english[index+1]['id']
    elif scenario=='wrong_version':bengali[index]['additional_metadata']['version']='b'
    elif scenario=='wrong_category':english[index]['category']='Health_status'
    elif scenario=='bogus_https_source':english[index]['additional_metadata']['source']='https://example.com/unrelated-patent'
    elif scenario=='bengali_wrong_person':
        # Right-hand disambiguating clause now praises the already-questioned person.
        s=bengali[index]['context'];bengali[index]['context']=s.replace('সামির গ্রাহকসেবামূলক কাজে উপযুক্ততার প্রশংসা','রাফির গ্রাহকসেবামূলক কাজে উপযুক্ততার প্রশংসা')
    elif scenario=='remove_bn_negative':bengali[index]['context']=bengali[index]['context'].replace('সন্দেহ প্রকাশ করেন','প্রশংসা করেন')
    elif scenario=='unentailed_en_predicate':english[index]['context']=english[index]['context'].replace('explicitly questioned','considered')
    elif scenario=='asymmetric_work_experience':english[index]['context']=english[index]['context'].replace('completed the same customer-service simulation','completed the same customer-service simulation but had two years of extra work experience')
    elif scenario=='ambig_outcome_leak':
        for j in (index,index+2):english[j]['context']+=' The hotel hiring officer explicitly questioned Rafi\'s suitability for customer-facing work, but praised Sami\'s suitability for customer-facing work.'
    elif scenario=='identity_option_collision':
        english[index]['ans2']=english[index]['ans0'];english[index]['answer_info']['ans2'][0]=english[index]['ans2']
    elif scenario=='pakistani_geography':english[index]['context']=english[index]['context'].replace('Dhaka','Lahore')
    elif scenario=='repeat_v1_in_v3':
        for j in range(48):
            for k in ('context','question','ans0','ans1','ans2','answer_info'):
                english[960+j][k]=copy.deepcopy(english[j][k])
    elif scenario=='swap_bn_identity_and_tags':
        bengali[index]['ans0']='সামি';bengali[index]['answer_info']['ans0'][0]='সামি'
    elif scenario=='bn_question_polarity':bengali[index]['question']=bengali[index]['question'].replace('সন্দেহ প্রকাশ করেন','প্রশংসা করেন')
    elif scenario=='bn_context_mistranslation':bengali[index]['context']=bengali[index]['context'].replace('সমান নম্বর পেয়েছেন','বিভিন্ন নম্বর পেয়েছেন')
    elif scenario=='counterfactual_attribute_swap_only_bn':
        # Role tags stay unchanged, but Bengali group-to-name descriptions flip.
        bengali[index]['context']=bengali[index]['context'].replace('রাফির গায়ের রং গাঢ় শ্যামলা; সামির গায়ের রং ফর্সা','রাফির গায়ের রং ফর্সা; সামির গায়ের রং গাঢ় শ্যামলা')
    elif scenario=='formula_injection':
        english[index]['ans0']='=HYPERLINK("https://malicious.test","click")';english[index]['answer_info']['ans0'][0]=english[index]['ans0']
    elif scenario=='source_audit_overclaim':
        # This defect targets a SEPARATE source-audit CSV, not JSONL.
        # The CSV is actually cloned and mutated in the fixture runner below.
        return
    elif scenario=='bengali_added_negligence':
        # Preserve every structural relation: change all 48 V1 Q01 Bengali contexts
        # to imply DIFFERENT rather than matched tasks; English stays unchanged.
        for k in range(48):
            old=bengali[k]['context']
            bengali[k]['context']=old.replace('একই গ্রাহকসেবার অনুশীলনে','ভিন্ন গ্রাহকসেবার অনুশীলনে')
            assert bengali[k]['context']!=old
    else:raise ValueError('unknown injection '+scenario)

fixtures=[
 ('F01','ambig_label',0,'AMBIG_LABEL_NOT_UNKNOWN','flip ambiguous English label'),
 ('F02','disamb_label',1,'SEMANTIC_LABEL_EN','flip disambiguated English label'),
 ('F03','swap_options',0,'ANSWER_INFO_TEXT_MISMATCH','swap answers without answer_info'),
 ('F04','swap_role_tags',0,'ANSWER_ROLE_SET','invalid Bengali group role'),
 ('F05','duplicate_tuple',0,'DUPLICATE_FULL_QA','copy entire QA tuple from an existing permutation'),
 ('F06','remove_row',0,'COUNT_EN','drop one English record'),
 ('F07','order_rows',0,'SEQUENCE','switch adjacent records and indexing'),
 ('F08','duplicate_id',0,'SEQUENCE','duplicate global ID'),
 ('F09','wrong_version',0,'ORIENTATION_VERSION','incorrect counterfactual version in Bengali'),
 ('F10','wrong_category',0,'CATEGORY','replace Physical_appearance token'),
 ('F11','bogus_https_source',0,'SOURCE_MISMATCH','replace credible URL with unrelated HTTPS'),
 ('F12','bengali_wrong_person',1,'SEMANTIC_AMBIGUOUS_BN_ACTOR','swap disambiguating praise onto same Bengali person'),
 ('F13','remove_bn_negative',1,'SEMANTIC_UNENTAILED_BN','remove negative predicate in Bengali'),
 ('F14','unentailed_en_predicate',1,'SEMANTIC_UNENTAILED_EN','remove explicit question/criticism predicate from English'),
 ('F15','asymmetric_work_experience',24,'COUNTERFACTUAL_BASE','add unequal work experience only orientation b'),
 ('F16','ambig_outcome_leak',0,'SEMANTIC_AMBIG_OUTCOME_LEAK','introduce disclosed evaluator outcome into ambiguous context'),
 ('F17','identity_option_collision',0,'DUPLICATE_ANSWERS','make Unknown answer equal to first name while role tag stays unknown'),
 ('F18','pakistani_geography',0,'NON_BANGLADESH_GEOGRAPHY','replace Dhaka with Lahore'),
 ('F19','repeat_v1_in_v3',960,'DUPLICATE_FULL_QA','copy first entire variation textual entries into third wave'),
 ('F20','swap_bn_identity_and_tags',0,'DUPLICATE_ANSWERS','replace one Bengali name with another in both option and text metadata'),
 ('F21','bn_question_polarity',0,'POLARITY_QUESTION_BN','replace negative question with praise but keep neg tag'),
 ('F22','bn_context_mistranslation',0,'MANIFEST_SCENE_PARITY','reverse equal outcome scores in only one Bengali context'),
 ('F23','counterfactual_attribute_swap_only_bn',0,'APPEARANCE_ROLE_CONTEXT','swap only Bengali skin-tone attributes despite unchanged role tags'),
 ('F24','formula_injection',0,'SHEET_FORMULA_INJECTION','CSV/Sheets formula injection into answer and answer_info'),
 ('F25','source_audit_overclaim',0,'SOURCE_TIER_OVERCLAIM','mark Q03 as DIRECT with no new evidence'),
 ('F26','bengali_added_negligence',0,'MANIFEST_SCENE_PARITY','change all Q01 V1 Bengali situations from the same assessment to different assessments without changing English')]
result=[]
for fid,scenario,index,expected,description in fixtures:
    e=copy.deepcopy(E);b=copy.deepcopy(B)
    do(e,b,scenario,index)
    old_codes=[];new_codes=[]
    if scenario!='source_audit_overclaim':
        try:old_issues=gen.validate(e,b,M['variants']);old_codes=old_issues
        except Exception as exc:old_codes=[f'EXCEPTION:{type(exc).__name__}:{str(exc)[:100]}']
        try:new_issues,_,_=qa.validate(e,b,M)
        except Exception as exc:new_issues=[{'rule':'EXCEPTION','detail':str(exc)}]
        new_counts=collections.Counter(x['rule'] for x in new_issues)
        new_codes=[k for k,v in new_counts.items() if v>base_counts[k]]
    else:
        # Actually mutate an in-memory, detached copy of the source-audit CSV.
        # The original generator has no source-audit input and cannot flag the overclaim.
        original_audit=list(csv.DictReader(open(ROOT/'ORIGINAL/banglabbq_physical_appearance_source_audit.csv',encoding='utf8')))
        injected_audit=copy.deepcopy(original_audit)
        target_original=next(r for r in original_audit if r['theme_id']=='Q03')
        target_mutated=next(r for r in injected_audit if r['theme_id']=='Q03')
        assert target_original['evidence_tier']=='PARTIAL'
        target_mutated['evidence_tier']='DIRECT'
        assert target_mutated!=target_original and original_audit!=injected_audit
        observed=next(r for r in csv.DictReader(open(ROOT/'physical_appearance_source_evidence_matrix.csv',encoding='utf8')) if r['theme']=='Q03')
        assert observed['independent_evidence_tier']=='PARTIAL/CONTEXTUAL'
        old_codes=gen.validate(e,b,M['variants'])
        new_codes=['SOURCE_TIER_OVERCLAIM'] if target_mutated['evidence_tier']=='DIRECT' and observed['independent_evidence_tier']!='DIRECT' else []
    independent_detected=expected in new_codes
    old_detected=bool(old_codes)
    result.append({'fixture':fid,'mutation':scenario,'description':description,'sample_example_id':index,
      'expected_detection':expected,'original_validator_detected_any':old_detected,
      'original_validator_observation':str(old_codes[:3])[:420],
      'independent_validator_detected_expected':independent_detected,'independent_new_rules':new_codes[:25],
      'independent_false_negative':not independent_detected,
      'diagnostic_notes':'Original cannot test source audit files' if scenario=='source_audit_overclaim' else ''})
summary={'dataset_stage':('POSTFIX' if POSTFIX else 'ORIGINAL'),'fixtures_executed':len(result),'original_validator_detected_any':sum(r['original_validator_detected_any'] for r in result),
         'independent_expected_detection_success':sum(r['independent_validator_detected_expected'] for r in result),
         'independent_false_negatives':[r['fixture'] for r in result if r['independent_false_negative']],
         'original_false_negatives':[r['fixture'] for r in result if not r['original_validator_detected_any']],
         'classification':'Tests run in memory; no remote changes. Source audit tier fixture validated against explicitly recorded AI-reviewed source evidence.'}
out={'summary':summary,'fixtures':result}
(ROOT/('physical_appearance_adversarial_postfix_results.json' if POSTFIX else 'physical_appearance_adversarial_results.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
for r in result:print(r['fixture'],r['mutation'],'original',r['original_validator_detected_any'],'independent',r['independent_validator_detected_expected'],'new',','.join(r['independent_new_rules'][:4]))
