#!/usr/bin/env python3
"""Executed mutation tests against ORIGINAL and INDEPENDENT Social_status validators.
Each fixture operates on fresh local in-memory copies; source files untouched.
Manual-review-required findings are NOT claimed to be automatically detected.
"""
from __future__ import annotations
import copy, importlib.util, json, pathlib, collections, datetime, hashlib
P=pathlib.Path(__file__).resolve().parent; ROOT=P.parent

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,str(path)); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod);return mod
old=load_module('original_repro_generator',pathlib.Path('/mnt/data/banglabbq_social_status_generate.py'))
new=load_module('independent_validator',P/'social_status_independent_validator.py')
orig={lang:[json.loads(s) for s in (ROOT/'original'/f'banglabbq_social_status_{name}.jsonl').read_text(encoding='utf-8').splitlines()] for lang,name in [('en','english'),('bn','bengali')]}
manifest=json.loads((ROOT/'original'/'banglabbq_social_status_expansion_manifest.json').read_text(encoding='utf-8'))
expected_sources={str(q):orig['en'][(q-1)*48]['additional_metadata']['source'] for q in range(1,11)}

def mutate(f):
    en,bn=f['en'],f['bn']; x=en[0];y=bn[0];

def fixture(name,kind,what,should,fn,expect_detected=True): return {'id':f'FX{len(FIX)+1:02d}', 'fault':name,'domain':kind,'mutation':what,'expected_detectors':should,'injector':fn,'auto_expected':expect_detected}
FIX=[]
def add(name,kind,what,should,fn,exp=True):FIX.append(fixture(name,kind,what,should,fn,exp))

def m_same(f,i,fn):
    for lang in ('en','bn'):fn(f[lang][i],lang)

def wrong_ambig_label(f):m_same(f,0,lambda r,l:r.__setitem__('label',(r['label']+1)%3))
add('ambiguous_gold_flipped','gold','Flip gold choice on EID 0 in both languages','GOLD_ROLE + distribution',wrong_ambig_label)
def wrong_disambig_label(f):m_same(f,1,lambda r,l:r.__setitem__('label',(r['label']+1)%3))
add('disambiguated_gold_flipped','gold','Flip gold on EID 1 (explicit named answer)','BLIND_GOLD_ENTAILMENT',wrong_disambig_label)
def option_swap_missing_label(f):
    for lang in ('en','bn'):
        r=f[lang][0];r['ans0'],r['ans1']=r['ans1'],r['ans0'];r['answer_info']['ans0'],r['answer_info']['ans1']=r['answer_info']['ans1'],r['answer_info']['ans0']
add('options_swapped_without_label','gold','Swap A/B text+role pair, leave gold unchanged','GOLD_ROLE + POSITION_BALANCE',option_swap_missing_label)
def bad_role_tag(f):m_same(f,0,lambda r,l:r['answer_info']['ans0'].__setitem__(1,'unknown'))
add('answer_role_collision','structure','Assign unknown role to a named answer','ANSWER_ROLES + NAME_ROLE_MISMATCH',bad_role_tag)
def duplicate_qa(f):
    for lang in ('en','bn'):
        src=f[lang][0];t=f[lang][4];
        for k in ('context','question','ans0','ans1','ans2','answer_info','label'):t[k]=copy.deepcopy(src[k])
add('complete_QA_duplicate','duplicate','Copy complete 5-field QA tuple from EID 0 to EID 4','DUPLICATE_FULL_QA',duplicate_qa)
def miss_perm(f):
    for lang in ('en','bn'):
        src=f[lang][0];dst=f[lang][4]
        for key in ('ans0','ans1','ans2','answer_info','label'):dst[key]=copy.deepcopy(src[key])
add('missing_sixth_answer_permutation','combinatorial','Duplicate one 4-row answer permutation within 48 block','PERMUTATION + ROLE_PERMUTATION',miss_perm)
def wrong_order(f):
    for lang in ('en','bn'):f[lang][0],f[lang][1]=f[lang][1],f[lang][0]
add('broken_four_condition_cycle','combinatorial','Swap EID 0 and 1 objects','CONDITION_ORDER',wrong_order)
add('duplicate_provisional_id','ids','Copy ID on EID 0 to EID 1','DUPLICATE_ID',lambda f:m_same(f,1,lambda r,l:r.__setitem__('id',8200000)))
add('duplicate_example_id','ids','Duplicate example_id 0 at position 1','DUPLICATE_EXAMPLE_ID',lambda f:m_same(f,1,lambda r,l:r.__setitem__('example_id',0)))
add('illegal_category_token','schema','Set Social_status->Occupational_background','CATEGORY',lambda f:m_same(f,0,lambda r,l:r.__setitem__('category','Occupational_background')))
add('illegal_orientation_version','schema','Set a->b for EID 0','ORIENTATION',lambda f:m_same(f,0,lambda r,l:r['additional_metadata'].__setitem__('version','b')))
add('blank_source_citation','provenance','Remove HTTPS source on EID 0','SOURCE_URL',lambda f:m_same(f,0,lambda r,l:r['additional_metadata'].__setitem__('source','')))
add('wrong_theme_index','schema','Reassign Q01->Q02 on EID 0','INDEX',lambda f:m_same(f,0,lambda r,l:r.__setitem__('question_index','2')))
def drop_nested_ans(f):m_same(f,0,lambda r,l:r['answer_info'].pop('ans2'))
add('missing_answer_info_pair','schema','Remove answer_info.ans2','ANSWER_INFO_KEYS',drop_nested_ans)
def option_collision(f):m_same(f,0,lambda r,l:r.__setitem__('ans0',r['ans1']))
add('answer_text_collision','schema','Set ans0 equal ans1','OPTION_COLLISION',option_collision)
add('missing_question_text','schema','Blank question field on EID 0','EMPTY_TEXT',lambda f:m_same(f,0,lambda r,l:r.__setitem__('question','')))
add('invisible_unicode_marker','unicode','Inject U+200B zero-width marker into context','UNICODE_ARTIFACT',lambda f:m_same(f,0,lambda r,l:r.__setitem__('context',r['context']+'\u200b')))
add('Pakistani_place_leak','cultural','Replace Dhaka with Lahore in same context','FOREIGN_PLACE',lambda f:m_same(f,0,lambda r,l:r.__setitem__('context',r['context'].replace('Dhaka','Lahore').replace('ঢাকা','লাহোর'))))
add('Bengali_name_actor_drift','bilingual','BN Rafi->Rafik only in EID 0 context','BILINGUAL_NAMED_ENTITIES',lambda f:f['bn'][0].__setitem__('context',f['bn'][0]['context'].replace('রাফি','রাফিক')))
def bn_wrong_option(f):
    r=f['bn'][0];r['ans0']='একজন অচেনা মানুষ';r['answer_info']['ans0'][0]=r['ans0']
add('Bengali_option_reference_mismatch','bilingual','BN answer entity replaced but metadata role remains','BILINGUAL_NAME',bn_wrong_option)
add('bool_as_gold_label','typing','Python bool true disguised as 1 (int subclass)','TYPE_EXACT',lambda f:m_same(f,0,lambda r,l:r.__setitem__('label',True)))
def unentailed_question(f):
    f['en'][1]['question']='Who was arrested for theft?';f['bn'][1]['question']='চুরির দায়ে কাকে গ্রেপ্তার করা হয়েছিল?'
add('question_unentailed_new_predicate','semantic','Disambig question now asks an arrest never described','EXPERT_SEMANTIC_PREDICATE_AUDIT',unentailed_question,False)
def ambig_clue(f):
    f['en'][0]['context']+=' The official rejected Rafi.';f['en'][2]['context']+=' The official rejected Rafi.'
    f['bn'][0]['context']+=' কর্মকর্তা রাফিকে প্রত্যাখ্যান করেন।';f['bn'][2]['context']+=' কর্মকর্তা রাফিকে প্রত্যাখ্যান করেন।'
add('ambiguous_context_reveals_answer','semantic','Add explicitly decisive fact to both ambig polarities, leave Unknown gold','EXPERT_AMBIGUITY_AUDIT',ambig_clue,False)
def asymmetric_experience(f):
    for lang in ('en','bn'):
        for i in (24,25,26,27):
            r=f[lang][i];r['context']+=(' Rafi alone has ten extra years of experience.' if lang=='en' else ' শুধু রাফির দশ বছরের বাড়তি অভিজ্ঞতা আছে।')
add('counterfactual_work_experience_confound','counterfactual','Only orientation b gets asymmetric experience','COUNTERFACTUAL',asymmetric_experience)
add('role_stereotyped_group_reversal','schema','Invert low-income target metadata to affluent','GROUPS',lambda f:m_same(f,0,lambda r,l:r['additional_metadata'].__setitem__('stereotyped_groups',['Wealthy people'])))
def irrelevant_valid_source(f):m_same(f,0,lambda r,l:r['additional_metadata'].__setitem__('source','https://example.org/astrology-prediction'))
add('irrelevant_but_syntactically_valid_citation','source','Replace source URL with valid HTTPS but unrelated site','SOURCE_RELEVANCE_AND_WHITELIST_REVIEW',irrelevant_valid_source,False)
def duplicate_v3(f):
    for lang in ('en','bn'):
        for j in range(48):
            s=f[lang][j];d=f[lang][960+j]
            for k in ('context','question','ans0','ans1','ans2','label','answer_info'):d[k]=copy.deepcopy(s[k])
add('variation_3_copied_from_variation_1','duplicates','Replicate all V1 Q01 QA text/labels in V3 Q01, preserving IDs','DUPLICATE_FULL_QA + FAMILY_REVIEW',duplicate_v3)
def latin_in_bn(f):f['bn'][0]['question']='Who is the poor person?'
add('Latin_English_leak_into_Bengali','linguistic','Replace Bengali question with English text','ENGLISH_LEAK',latin_in_bn)
def author_judgment_mismatch(f):
    f['en'][1]['question']='Who was accepted although everyone thought they were ill?'
    f['bn'][1]['question']='সবাই অসুস্থ মনে করা সত্ত্বেও কাকে গ্রহণ করা হয়েছিল?'
add('medical_unfounded_trait_into_social_probe','category','Change question to healthcare/disease assumption, no supporting context','EXPERT_CATEGORY_AND_ENTAILMENT_AUDIT',author_judgment_mismatch,False)

# Four clean adversarial fixtures deliberately preserve row order, roles, bilingual metadata,
# six permutations and counterfactual structure. Their remaining failure is SEMANTIC only.
def clean_unentailed_all_neg(f):
    for lang in ('en','bn'):
        for i in range(0,48):
            if f[lang][i]['question_polarity']=='neg':
                f[lang][i]['question']=('Who was fined by the doctor?' if lang=='en' else 'চিকিৎসক কাকে জরিমানা করেছিলেন?')
add('systematic_unentailed_negative_question','semantic','Change all Q01 V1 neg questions, both orientations/languages to unmentioned fine','EXPERT_NATURAL_LANGUAGE_ENTAILMENT',clean_unentailed_all_neg,False)
def clean_ambig_explicit_action(f):
    for lang in ('en','bn'):
        for i in range(0,48):
            r=f[lang][i]
            if lang=='en':
                flag=' Rafi comes from';ins=" The doctor dismissed Rafi's question without explanation."
            else:
                flag=' রাফি স্বল্প';ins=' চিকিৎসক রাফির প্রশ্নের কোনো ব্যাখ্যা না দিয়ে এড়িয়ে যান।'
            if flag not in r['context']:flag=' Rafi comes from' if lang=='en' else ' রাফি সচ্ছল'
            assert flag in r['context']
            r['context']=r['context'].replace(flag,ins+flag,1)
add('full_block_ambiguous_answer_leak','semantic','Introduce decisive negative predicate inside both ambig/disambig prefix for Q01 V1, all permutations/versions','EXPERT_AMBIGUITY_INFERENCE',clean_ambig_explicit_action,False)
def clean_skewed_experience(f):
    for lang in ('en','bn'):
        for i in range(192,240):
            r=f[lang][i]
            flag=(' Rafi comes from' if lang=='en' else ' রাফি স্বল্প')
            if flag not in r['context']:flag=' Rafi comes from' if lang=='en' else ' রাফি সচ্ছল'
            assert flag in r['context']
            r['context']=r['context'].replace(flag,(' Rafi alone also has a specialist credential.' if lang=='en' else ' শুধু রাফির বাড়তি বিশেষজ্ঞ সনদ রয়েছে।')+flag,1)
add('symmetric_counterfactual_but_biased_qualifications','semantic','Make Rafi alone additionally credentialed in BOTH orientations (counterfactual passes; construct fails)','EXPERT_CREDENTIAL_CONFOUNDER_REVIEW',clean_skewed_experience,False)
def clean_bengali_numerical_divergence(f):
    for i in range(912,960):
        r=f['bn'][i]
        before='সমানসংখ্যক অনুশীলনে'
        assert before in r['context']
        r['context']=r['context'].replace(before,'ভিন্নসংখ্যক অনুশীলনে',1)
add('entire_Bengali_variant_meaning_drift','bilingual','Flip attendance-equivalence to different attendance in all 48 BN Q10 V2 records','AI_BILINGUAL_SEMANTIC_ALIGNMENT_REVIEW',clean_bengali_numerical_divergence,False)

base_issues,base_stats=new.validate(orig['en'],orig['bn'])
assert not base_issues,('independent validator baseline has defects',len(base_issues))
base_old=old.validate(orig,manifest)
assert len(base_old[1])==0
results=[]
for fixture in FIX:
    f={lang:copy.deepcopy(orig[lang]) for lang in ('en','bn')}
    try:
        fixture['injector'](f)
        changed=[(lang,i) for lang in ('en','bn') for i,(a,b) in enumerate(zip(orig[lang],f[lang])) if a!=b]
        assert changed,fixture['id']
        inj_ok=True;inject_error=None
    except Exception as exc:
        inj_ok=False;inject_error=repr(exc);changed=[]
    if not inj_ok:
        results.append({**{k:v for k,v in fixture.items() if k!='injector'},'injection_executed':False,'error':inject_error});continue
    try:
        cc,errors,_=old.validate(f,manifest);existing_detected=bool(errors);old_checks=[k for k,v in cc.items() if not v.get('pass')];old_error=None
    except Exception as exc:
        existing_detected=False;old_checks=[];old_error=repr(exc)
    try:
        got,st=new.validate(f['en'],f['bn']);ind_detected=bool(got);ind_tests=list(sorted(set(x.get('test','?') for x in got)));ind_error=None
    except Exception as exc:
        ind_detected=False;ind_tests=[];ind_error=repr(exc)
    # Explicitly score source/semantic mutations as still requiring independent expert review,
    # not as programmatically detected by the two general-purpose validators.
    observed_semantic_gap=not existing_detected and not ind_detected
    results.append(dict(fixture_id=fixture['id'],injection=fixture['fault'],domain=fixture['domain'],injected_change=fixture['mutation'],expected_detection=fixture['expected_detectors'],injection_executed=inj_ok,modified_rows=len(changed),modified_record_refs=[f'{l}:{i}' for l,i in changed[:12]],existing_validator_detected=existing_detected,existing_validator_failed_checks=old_checks,existing_validator_exception=old_error,independent_validator_detected=ind_detected,independent_validator_failed_tests=ind_tests,independent_validator_exception=ind_error,semantic_or_source_oversight=observed_semantic_gap,expert_review_required=fixture['domain'] in ('semantic','source','category','linguistic','cultural'),notes='Both scripts need coverage enhancement for this expert-review-only mutation' if observed_semantic_gap else 'At least one validator flags mutant; expert review may still be required'))
summary={
    'executed_at_utc':'2026-10-26 (local run; wall-clock omitted)',
    'category':'Social_status',
    'source':'immutable committed originals',
    'total_fixtures':len(results),
    'actually_injected':sum(x.get('injection_executed',False) for x in results),
    'original_validator_detected':sum(x.get('existing_validator_detected',False) for x in results),
    'independent_validator_detected':sum(x.get('independent_validator_detected',False) for x in results),
    'neither_validator_detected':sum(x.get('injection_executed',False) and not x.get('existing_validator_detected',False) and not x.get('independent_validator_detected',False) for x in results),
    'validator_exceptions':sum(bool(x.get('existing_validator_exception') or x.get('independent_validator_exception')) for x in results),
    'expert_required_not_auto_detected':[x['fixture_id'] for x in results if x.get('semantic_or_source_oversight')],
    'important_caveat':'Expert reviewer expected-detection labels are a specified verification procedure, NOT execution of a human review; no manual expert was hired.',
}
output=P/'social_status_adversarial_results.json'
output.write_text(json.dumps({'summary':summary,'fixtures':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
for x in results:
    print(x['fixture_id'],x['injection'],f'old={x.get("existing_validator_detected")}',f'new={x.get("independent_validator_detected")}',f'exception={bool(x.get("existing_validator_exception") or x.get("independent_validator_exception"))}')
