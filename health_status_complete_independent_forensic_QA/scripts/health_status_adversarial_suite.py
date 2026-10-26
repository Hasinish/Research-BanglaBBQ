#!/usr/bin/env python3
"""Executable in-memory adversarial mutations. Mutations never alter original files.
Existing generator's validator is executed for comparison, even if it crashes.
Editorial-only cases are explicitly marked independent automatic false negatives.
"""
import copy,csv,importlib.util,json,hashlib
from collections import Counter
from pathlib import Path
from health_status_independent_validator import independent_check
ROOT=Path('/mnt/data');EN=list(map(json.loads,(ROOT/'banglabbq_health_status_english.jsonl').open()));BN=list(map(json.loads,(ROOT/'banglabbq_health_status_bengali.jsonl').open()));MAN=json.loads((ROOT/'banglabbq_health_status_expansion_manifest.json').read_text())
spec=importlib.util.spec_from_file_location('author',str(ROOT/'banglabbq_health_status_generate.py')); author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
F=[]
def fixture(fid,kind,detail,mutator,expected,expert_note=''):
    F.append((fid,kind,detail,mutator,expected,expert_note))
# 26 distinct faults. Mutations intentionally small so diagnostic coverage is interpretable.
fixture('F01','gold','Flip ambiguous gold EN row 0',lambda e,b,m:setattr_dummy(e[0],'label',0),'AMBIG_GOLD')
fixture('F02','gold','Flip disambiguated gold EN row 1 to opposite person',lambda e,b,m:setattr_dummy(e[1],'label',1),'BLIND_DISAMBIG_GOLD')
fixture('F03','gold','Make BN disambiguated label point to Unknown',lambda e,b,m:setattr_dummy(b[1],'label',2),'DISAMBIG_GOLD')
fixture('F04','answer','Swap first two EN options without updating answer_info',lambda e,b,m:swap(e[0],'ans0','ans1'),'ANSWER_INFO_TEXT')
fixture('F05','answer','Swap two EN answer_info role tags only',lambda e,b,m:swap_roles(e[0]),'COUNTERFACTUAL_ROLE_SWAP')
fixture('F06','duplicate','Duplicate entire QA tuple of row 0 into row 4 while retaining IDs',lambda e,b,m:copy_tuple(e[4],e[0]),'DUPLICATE_COMPLETE_TUPLE')
fixture('F07','order','Change disambiguated EN row to ambiguous marker',lambda e,b,m:setattr_dummy(e[1],'context_condition','ambig'),'CANONICAL_ORDER')
fixture('F08','permutation','Repeat EN first permutation in next 4-row permutation block',lambda e,b,m:repeat_option_order(e,4,0),'MISSING_PERMUTATION')
fixture('F09','id','Duplicate EN provisional id',lambda e,b,m:setattr_dummy(e[12],'id',e[11]['id']),'PROVISIONAL_ID_SEQUENCE')
fixture('F10','id','Shift BN example_id',lambda e,b,m:setattr_dummy(b[12],'example_id',23),'EXAMPLE_ID_SEQUENCE')
fixture('F11','metadata','Change version b to a in EN row 24',lambda e,b,m:e[24]['additional_metadata'].__setitem__('version','a'),'ORIENTATION')
fixture('F12','category','Change EN Health_status to Physical_appearance',lambda e,b,m:setattr_dummy(e[0],'category','Physical_appearance'),'CATEGORY_TOKEN')
fixture('F13','source','Clear source URL from EN metadata',lambda e,b,m:e[0]['additional_metadata'].__setitem__('source',''),'SOURCE_URL')
fixture('F14','bilingual','Change Bengali answer name to another valid Bengali person in option and answer_info only',lambda e,b,m:translate_name_only(b[0]),'BILINGUAL_ENTITY_NAME','Requires cross-language semantic name audit, not role-only structural parity')
fixture('F15','polarity','Remove BN negative event marker from disambiguated sentence',lambda e,b,m:remove_bn_negative(b,1),'DISAMBIG_NEGATIVE_PREDICATE')
fixture('F16','semantic','Replace factual EN negative question by unentailed praise question',lambda e,b,m:setattr_dummy(e[1],'question','Who was praised for honesty?'),'QUESTION_LINEAGE')
fixture('F17','confound','Add unequal work experience to orientation a, all four conditions of first answer block',lambda e,b,m:unmatched_qualification(e),'COUNTERFACTUAL_HEALTH_MIRROR','Independent clinical/semantic audit also identifies unequal work experience')
fixture('F18','ambiguity','Leak decision into BN ambiguous context',lambda e,b,m:setattr_dummy(b[0],'context',b[0]['context']+' The clerk rejected one applicant.'),'COUNTERFACTUAL_CONTEXT_PREFIX')
fixture('F19','role','Conflate both identities into same health role tag',lambda e,b,m:e[0]['answer_info']['ans1'].__setitem__(1,e[0]['answer_info']['ans0'][1]),'ROLES_DISTINCT')
fixture('F20','geography','Replace Dhaka with Karachi in EN context',lambda e,b,m:setattr_dummy(e[0],'context',e[0]['context'].replace('Dhaka','Karachi')),'FOREIGN_GEO_context')
fixture('F21','source_tier','Replace Q04 tier PARTIAL by DIRECT without new evidence',lambda e,b,m:m['variations'][3].__setitem__('evidence_tier','DIRECT'),'SOURCE_TIER_TAMPER','Requires reviewed evidence matrix; generator validator does not evaluate this')
fixture('F22','variation','Replace V3 Q1 scenario contexts with V1 scenario contexts, both orientations',lambda e,b,m:duplicate_v3(e),'SCENARIO_LINEAGE')
fixture('F23','bilingual','Flip BN question to ask who was accepted instead of rejected',lambda e,b,m:setattr_dummy(b[0],'question',b[2]['question']),'QUESTION_LINEAGE')
fixture('F24','schema','Remove one answer key from EN row 0',lambda e,b,m:e[0].pop('ans1'),'SCHEMA_KEY_ORDER')
fixture('F25','counterfactual','Assign same BN health context to both orientations',lambda e,b,m:overwrite_bn_identity(b),'COUNTERFACTUAL_HEALTH_MIRROR')
fixture('F26','evidence','Replace an EN health citation with unrelated astronomy URL',lambda e,b,m:e[0]['additional_metadata'].__setitem__('source','https://science.nasa.gov/solar-system/'),'SOURCE_LINEAGE')

def setattr_dummy(r,k,v): r[k]=v

def swap(r,a,b):r[a],r[b]=r[b],r[a]

def swap_roles(r):
    r['answer_info']['ans0'][1],r['answer_info']['ans1'][1]=r['answer_info']['ans1'][1],r['answer_info']['ans0'][1]

def copy_tuple(dst,src):
    for k in ('context','question','ans0','ans1','ans2'):dst[k]=src[k]

def repeat_option_order(rows,first,source):
    for j in range(4):
        for k in ('ans0','ans1','ans2','answer_info','label'):
            rows[first+j][k]=copy.deepcopy(rows[source+j][k])

def translate_name_only(r):
    old=r['ans0'];new='\\u0985\\u09a8\\u09cd\\u09af'  # placeholder, resolved below
    new=new.encode().decode('unicode_escape') if False else ''.join(chr(x) for x in [0x0986,0x09a8,0x09a8,0x09cd,0x09af])
    r['ans0']=new;r['answer_info']['ans0'][0]=new

def remove_bn_negative(rows,i):
    bad=rows[i]['context'];negative=''.join(chr(x) for x in [0x09ac,0x09be,0x09a6,0x0020,0x09a6,0x09c7,0x09a8])
    # Fallback: very first decisive negative phrase from this specific item.
    old=''.join(chr(x) for x in [0x09ac,0x09be,0x09a6,0x0020,0x09a6,0x09c7,0x09a8])
    yes=''.join(chr(x) for x in [0x09b0,0x09be,0x0996,0x09c7,0x09a8])
    rows[i]['context']=bad.replace(old,yes,1)

def unmatched_qualification(e):
    suffix=' The first applicant also has seven additional years of accounting experience.'
    for i in (0,1,2,3):e[i]['context']+=suffix

def duplicate_v3(e):
    for i in range(960,1008):e[i]['context']=e[i-960]['context']

def overwrite_bn_identity(b):
    for i in range(24,48):b[i]['context']=b[i-24]['context']

def run():
    outcomes=[]
    for fid,kind,detail,mutator,expected,expert_note in F:
        e=copy.deepcopy(EN);b=copy.deepcopy(BN);m=copy.deepcopy(MAN)
        try:mutator(e,b,m)
        except Exception as ex:
            outcomes.append({'fixture':fid,'injected':False,'error':str(ex)});continue
        ind=independent_check(e,b,m)
        ids=sorted(set(x['test_id'] for x in ind['errors']))
        independent_detected=bool(ids)
        try:
            original_checks,original_messages=author.validate(e,b,m)
            author_failed=[k for k,v in original_checks.items() if not v['passed']]
            author_status='FLAGGED' if author_failed else 'MISSED'
            author_exceptions=[]
        except Exception as ex:
            author_failed=[];author_status='CRASHED';author_exceptions=[type(ex).__name__+': '+str(ex)[:240]]
        expected_detected=(expected in ids or any(expected in x for x in ids))
        # Source tier and lexical bilingual edits have no fully independent semantic automatic certification.
        manual='NOT_EXECUTED' if kind in ('bilingual','source_tier') else 'N/A'
        outcomes.append({'fixture':fid,'injected':True,'type':kind,'mutation':detail,'expected_detection':expected,
            'author_validator_status':author_status,'author_failed_checks':author_failed[:20],
            'author_exceptions':author_exceptions,
            'independent_detected':independent_detected,'independent_expected_check_detected':expected_detected,
            'independent_diagnostic_tests':ids[:25],
            'independent_false_negative':not independent_detected,
            'expert_review_required':kind in ('bilingual','source_tier','semantic','confound','ambiguity'),
            'expert_note':expert_note,'manual_detection_status':manual})
    out={'category':'Health_status','fixtures_executed':len(outcomes),'injection_count':sum(x.get('injected',False) for x in outcomes),
        'author_flagged':sum(x.get('author_validator_status')=='FLAGGED' for x in outcomes),
        'author_crashed':sum(x.get('author_validator_status')=='CRASHED' for x in outcomes),
        'author_missed':sum(x.get('author_validator_status')=='MISSED' for x in outcomes),
        'independent_automatic_detected':sum(x.get('independent_detected',False) for x in outcomes),
        'independent_automatic_false_negatives':[x['fixture'] for x in outcomes if x.get('independent_false_negative')],
        'caveat':'No model-based or human semantic adjudication was run as an automated detector. Source-tier and lexical equivalence require expert checks.',
        'fixtures':outcomes}
    p=ROOT/'health_status_adversarial_results.json';p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='fixtures'},indent=2))
    for x in outcomes:print(x['fixture'],x.get('author_validator_status'),x.get('independent_detected'),x.get('independent_expected_check_detected'),','.join(x.get('independent_diagnostic_tests',[])[:5]))

if __name__=='__main__':run()
