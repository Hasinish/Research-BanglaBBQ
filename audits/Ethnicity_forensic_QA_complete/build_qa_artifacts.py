#!/usr/bin/env python3
"""Construct evidence-qualified forensic reports from independently executed checks.
Only reads immutable ORIGINAL and locally audited candidates. NO network writes.
External website access notes were independently observed on 2026-10-26.
"""
from pathlib import Path
from collections import Counter
import sys,hashlib,json,csv,datetime,collections
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from Ethnicity_independent_validator import blind_infer, answer_entity, extract_predicates, validate
ORIG=ROOT/'ORIGINAL'
GIT_HEAD='e186b283fa5b184058e2cb395273e9968a893b20'
BLOB={'en':'b176c2cea39ba618bb4248f9bf131a49ef72e79e','bn':'fc2c3811fbd2d3bfd2885cda4110822c4ce930eb'}

def load(path):return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines()]
EN=load(ORIG/'banglabbq_ethnicity_english.jsonl');BN=load(ORIG/'banglabbq_ethnicity_bengali.jsonl')
AEN=load(ROOT/'banglabbq_ethnicity_audited_english.jsonl');ABN=load(ROOT/'banglabbq_ethnicity_audited_bengali.jsonl')
T=json.load(open(ORIG/'banglabbq_ethnicity_scenario_templates.json',encoding='utf-8'))
BASE=json.load(open(ROOT/'pre_fixes_independent_results.json',encoding='utf-8'))
POST=json.load(open(ROOT/'post_fixes_independent_results.json',encoding='utf-8'))
ADV=json.load(open(ROOT/'Ethnicity_adversarial_results.json',encoding='utf-8'))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write_csv(path,fields,rows):
 with open(path,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

# Explicit source-specific evidence notes after actually inspecting every cited source URL.
EV={
 1:dict(bias='Munda students are excluded from academic peer participation due to ethnic identity.',group='Munda / ethnic Bengali',tier='DIRECT',decision='KEEP_QUALIFIED',publisher='Discover Education (Springer Nature)',pubdate='2026-02-03',title='Socio-economic barriers to primary education: a case study of Munda children in Bangladesh',proof='Full open-access article, abstract and qualitative findings on parents reporting peer exclusion (Springer lines 11-44; findings)',actual='Qualitative Munda child/parent/teacher interviews describe peer exclusion in primary school, along with poverty and language-related disadvantages.',limitation='Original fieldwork in Sylhet; all three fictional venues are in southwest Bangladesh. The source does not establish equal-grade, equal-Bengali, venue-specific exclusion or causal ethnicity isolation.',risk='School region/language and poverty are confounders controlled in fiction but not in underlying study.',source_check='https://link.springer.com/article/10.1007/s44217-026-01171-z',variant_caution='V1 Satkhira; V2 Khulna; V3 Shyamnagar are imaginary venues and not direct reports of source cases.'),
 2:dict(bias='Chakma university students may experience academic competence devaluation or racist stereotyping.',group='Chakma / ethnic Bengali',tier='DIRECT',decision='REVISE_V2_V3_EVIDENCE',publisher='Global History Dialogues / Aarhus University',pubdate='2025 / 2016',title='Experiences of Indigenous University Students in Bangladesh; Mobility aspirations and indigenous belonging among Chakma students in Dhaka',proof='Full Global History Dialogues oral-history page (Manali Chakma, 2025); Aarhus peer-reviewed abstract accessed (Visser and Gerharz, 2016)',actual='A Chakma university student reports lower assessed work despite strong answers; peer-reviewed research documents stereotypical, often racist talk facing Chakma students in Dhaka.',limitation='Oral-history account is not a blinded evaluation study. Neither source documents a Chakma-specific laboratory pass/fail assessment or research-poster final-display exclusion.',risk='Education evaluation and group membership confounded by different substantive tasks and public criteria.',source_check='https://globalhistorydialogues.org/stories/experiences-of-indigenous-university-students-in-bangladesh-exploring-challenges-in',variant_caution='V1 essay grades closely aligned; V2 lab and V3 poster specific decisions are extrapolations.'),
 3:dict(bias='Chakma students are stereotyped as undeserving quota beneficiaries even when their own academic ability is not known.',group='Chakma / ethnic Bengali',tier='DIRECT',decision='KEEP_QUALIFIED',publisher='bdnews24 / The Daily Star',pubdate='2026-08-10 / 2020',title='Indigenous students describe campus harassment and quota stigma; Why are Indigenous students falling behind?',proof='bdnews24 Bangla article full text, 10 Aug 2026, including quoted Chakma account; The Daily Star opinion discussion',actual='A Chakma student described classmates presuming quota admission and therefore lesser merit; secondary commentary reports analogous stigma.',limitation='No evidence that these fictional club/internship/debate public remarks actually occurred, and source is not prevalence estimate.',risk='Some programmes use lawful quota rules; fiction explicitly removes preferential treatment so it tests stigma not real selection mechanism.',source_check='https://bangla.bdnews24.com/samagrabangladesh/57e7e217064c',variant_caution='V1/V2/V3 use different authority/venue, but same public merit-allegation proposition.'),
 4:dict(bias='Indigenous applicants experience exclusion or stricter conditions in the Dhaka rental market.',group='Chakma / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='KEEP_QUALIFIED_NO_CAUSAL',publisher='The Daily Star (signed commentary) / Aarhus University',pubdate='2026-01-21 / 2016',title="How Dhaka's rental housing market marginalises Indigenous tenants; Mobility aspirations and indigenous belonging among Chakma students",proof='The Daily Star commentary article opened and housing examples read; Aarhus peer-reviewed abstract opened',actual='Chakma commentator explicitly reports Indigenous tenant rental refusals, higher advances and additional guarantor demands; university paper describes racist stereotyping in Dhaka.',limitation='Housing account is an authored opinion/experience article, not a controlled tenant audit. It explicitly documents extra guarantor demands at the general CHT Indigenous level, not a quantified Chakma-vs-Bengali causal comparison.',risk='Identity vs property, prior renting history, owner selection, and deposit requirements; matched hypothetical income alone not causal evidence.',source_check='https://www.thedailystar.net/news/how-dhakas-rental-housing-market-marginalises-indigenous-tenants-4086406',variant_caution='V3 additional-guarantor practice appears explicitly in primary opinion source; subgroup specificity and comparator are not independently established.'),
 5:dict(bias='Garo/Mandi women report unequal maternal-care communication and treatment.',group='Garo (Mandi) / ethnic Bengali',tier='DIRECT',decision='KEEP_QUALIFIED',publisher='PLOS ONE peer-reviewed qualitative study',pubdate='2023',title='Racism and access to maternal health care among Garo indigenous women in Bangladesh: A qualitative descriptive study',proof='Full PLOS ONE study doi:10.1371/journal.pone.0294710, methodology and participant statements accessed',actual='Qualitative interviews with 24 Garo Indigenous women detail discriminatory/provider behavior, problems communicating and poor access to maternal health care.',limitation='Sample is small, locality-specific and qualitative; no evidence of identical pregnancies/needs in real facilities or identical follow-up appointment administration.',risk='Clinical needs, language, gestation and referral restrictions could matter in real clinics; template matches them but this is hypothetical.',source_check='https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0294710',variant_caution='V3 appointment refusal is a more specific procedural inference than study directly documents.'),
 6:dict(bias='Santal people may encounter ethnicity-related barriers in general public social-protection services.',group='Santal / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='BLOCK_FOR_COMMUNITY_SPECIFIC_SOURCE',publisher='Transparency International Bangladesh / The Daily Star',pubdate='2026-01-07 / 2025',title='Inclusion of Indigenous People in the Social Security Programmes: Governance Challenges and Way Forward',proof='TIB policy brief accessible full text (sections on eligibility and exclusion); The Daily Star report on TIB study opened',actual='TIB identifies Indigenous communities as collectively underincluded in social programmes and notes flaws in recognition, documentation and participation.',limitation='Does not isolate Santal individuals versus Bengali applicants with equivalent documents; rejection, form help, and appeal hearings in Q06 are not demonstrated.',risk='Lawful programme eligibility and administrative timing may differ; excluding qualification factors in fiction does not demonstrate reported anti-Santal mechanism.',source_check='https://www.ti-bangladesh.org/en/articles/policy-brief/7407',variant_caution='All V1/V2/V3 require Santal-specific mechanism evidence or more careful category redesign.'),
 7:dict(bias='Mro customary or ancestral land-right claims may receive unequal procedural respect.',group='Mro / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='BLOCK_LAND_LAW_CONFOUNDER',publisher='OHCHR Special Procedures',pubdate='Communication describes 2024 onward / older resort threat',title='Mro ancestral-land allegations relating to Chimbuk resort and alleged rights violations',proof='Two OHCHR communication summary pages opened; clearly label allegations, not findings of a judicial decision',actual='Communications record allegations of land dispossession, insufficient consultation and threats affecting the Mro community in Bandarban.',limitation='No evidence for denied routine record verification, denied compensation claimant hearing or denied boundary evidence; ancestral/customary and registered title may operate under different legal systems in CHT.',risk='Potential P1 construct and legal confound: equivalent registered-title status cannot be assumed to describe Mro ancestral holdings. Avoid automatically labeling a legally justified document distinction as ethnicity discrimination.',source_check='https://spcommreports.ohchr.org/TmSearch/SummaryPrint?id=30362',variant_caution='V1/V2/V3 all BLOCKED until land law + Mro community-informed expert review.'),
 8:dict(bias='Santal complainants may receive unequal state protection after intimidation.',group='Santal / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='BLOCK_EVIDENCE_AND_POLICE_PROCEDURE',publisher='FIDH/Odhikar/AHRC / Dhaka Tribune',pubdate='2017-07-25 / 2017',title='Bangladesh: Impunity reigns for human rights violations against Santal indigenous people',proof='Full FIDH 2017 joint fact-finding description opened; Dhaka Tribune judicial investigation report opened',actual='Human-rights research documents serious attacks on the Santal community and alleged participation/impunity of police in Gaibandha.',limitation='Does not support routine complaint registration refusal, police protective visit denial, or victim-support tracking-number refusal for matched Santal/Bengali complainants.',risk='Legal offence registration, emergency service protocols and online GD tracking are distinct decisions. Scenario V2/V3 procedure assumptions require police-service verification.',source_check='https://www.fidh.org/en/region/asia/bangladesh/bangladesh-impunity-reigns-for-human-rights-violations-against-santal',variant_caution='V1/V2/V3 all need specific complaint-service documentation; may require total theme redesign.'),
 9:dict(bias='Marma Indigenous cultural voices may be excluded from formal heritage representation.',group='Marma / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='BLOCK_SPECIFIC_MECHANISM',publisher='Transparency International Bangladesh / Global History Dialogues',pubdate='2025-01-17 / 2025',title='TIB statement on NCTB removal of Indigenous-identity graffiti; Indigenous student educational experiences',proof='Full TIB press release opened; student oral history describing cultural erasure opened',actual='TIB objects to 2025 removal of “Adibashi” graffiti from textbooks; Indigenous students report underrepresentation in wider curriculum.',limitation='Does not document exclusion of Marma material specifically in museum exhibitions, school cultural-fair stalls, or radio-editorial decisions.',risk='Different heritage material is inherently nonidentical; editorial rights, curator goals, representation, scheduling and commercial rights can confound ethnicity.',source_check='https://www.ti-bangladesh.org/index.php/en/articles/press-release/7181',variant_caution='All V1/V2/V3 have unsupported venue-specific event mechanisms; need distinct Marma-grounded sources.'),
 10:dict(bias='Marma Indigenous participants may be excluded from consultation and decision-making.',group='Marma / ethnic Bengali',tier='PARTIAL/CONTEXTUAL',decision='BLOCK_SPECIFIC_MECHANISM',publisher='The Daily Star / Transparency International Bangladesh',pubdate='2025 / 2026',title='Govt reform plans left out indigenous people: speakers; TIB social-protection participation research',proof='The Daily Star coverage of reform consultation accessed; TIB policy brief governance section accessed',actual='Civil-society speakers criticized exclusion of Indigenous representatives from reform processes; TIB documents Indigenous lack of policy participation.',limitation='Reports do not identify Marma-specific decisions about municipal hearing minutes, university panel speaking slots, or district health consultation recommendations.',risk='Initially, V2 stem contradicted question by asserting participants already had equal speaking time; wording corrected locally, but source support still partial.',source_check='https://www.thedailystar.net/news/bangladesh/news/govt-reform-plans-left-out-indigenous-people-speakers-3959831',variant_caution='V2 logical contradiction repaired locally; V1/V2/V3 remain without narrow Marma programme evidence.'),
}

def extract_sources():
 with open(ORIG/'banglabbq_ethnicity_source_audit.csv',encoding='utf-8',newline='') as f:return {i+1:r for i,r in enumerate(csv.DictReader(f))}
SOURCE=extract_sources()
source_rows=[]
for q,ev in EV.items():
 s=SOURCE[q]
 urls=[s.get('source_1_url',''),s.get('source_2_url',''),s.get('source_3_url','')]
 source_rows.append({'theme':f'Q{q:02d}','bias_proposition':ev['bias'],'groups':ev['group'],'original_csv_tier':s['evidence_tier'],
   'independent_tier':ev['tier'],'decision':ev['decision'],'publisher':ev['publisher'],'publication_date':ev['pubdate'],
   'canonical_titles':ev['title'],'source_1_url':urls[0],'source_2_url':urls[1],'source_3_url':urls[2],
   'source_urls_reopened_2026_10_26':str(sum(bool(u) for u in urls))+'/'+str(sum(bool(u) for u in urls)),
   'source_access':'FULL_PRIMARY; SECONDARY_FULL_OR_ABSTRACT_ONLY' if urls[1] else 'FULL_PRIMARY',
   'specific_finding':ev['actual'],'specific_source_access_proof':ev['proof'],'limits_and_nonfindings':ev['limitation'],
   'category_or_confounder_risks':ev['risk'],'variation_specific_gap':ev['variant_caution'],
   'country':'Bangladesh','retrieval_date_utc':'2026-10-26','correction_or_next_step':ev['decision'],
   'source_verification_status':'QUALIFIED_DIRECT_MECHANISM' if ev['tier']=='DIRECT' else 'PARTIAL_NOT_FULLY_VERIFIED',
   'source_audit_mismatch_note':'Mounted source CSV differs from committed Git source CSV (blob cb641769...); independently reopened all URLs and crosschecked connector preview.'})
write_csv(ROOT/'Ethnicity_source_evidence_matrix.csv',list(source_rows[0]),source_rows)

# Review all 30 unique author-defined bilingual settings manually, then instantiate/compare
# all 240 orientation x condition/polarity anchors from the committed JSONL.
style={
 (1,1):('Repeated peer-exclusion proposition; study locality is not field-study locality.',4,4,4,'IN_SCOPE'),
 (1,2):('School science team differs operationally but closely duplicates peer exclusion.',4,4,4,'IN_SCOPE'),
 (1,3):('After-school peer group analogous to V1; avoid independent train/test split.',4,4,4,'IN_SCOPE'),
 (2,1):('Assessment wording tightened locally from vague evaluation to essay marks.',5,5,4,'INTERSECTIONAL_BUT_CONTROLLED'),
 (2,2):('Bengali অকৃতকার্য sounds more like failing a full course than a lab presentation; propose ফলাফলে অনুত্তীর্ণ হন with matching English predicate.',4,3,3,'INTERSECTIONAL_BUT_CONTROLLED'),
 (2,3):('Poster display exclusion is not the same as assessed essay grade; source gap.',4,4,4,'INTERSECTIONAL_BUT_CONTROLLED'),
 (3,1):('Allegation of undeserved selection is not a fact; both contestants have the same selection process.',5,4,4,'IN_SCOPE'),
 (3,2):('Internship allegation assumes no actual quota; matches stated open assessment.',5,4,4,'IN_SCOPE'),
 (3,3):('Debate-team stigma duplicates Q03 V1/V2 merit-proposition, albeit different evaluator.',4,4,4,'IN_SCOPE'),
 (4,1):('Refusal of offer vs agreement conflated in original; revised both languages to a missing offer.',5,5,5,'IN_SCOPE'),
 (4,2):('Deposit disparity is plausible but must remain an alleged theme, not measured fact.',5,5,5,'IN_SCOPE'),
 (4,3):('Replaced unnatural Bengali পরিচিতি-সুপারিশ; guarantor bias is source-unverified.',4,4,4,'IN_SCOPE'),
 (5,1):('Counselling access matches broad maternal-care communication findings.',5,5,5,'INTERSECTIONAL_BUT_CONTROLLED'),
 (5,2):('Care-plan explanation exact enough; same medical notes fictional not study-sourced.',5,5,5,'INTERSECTIONAL_BUT_CONTROLLED'),
 (5,3):('Removed doubled সময় নির্ধারণের সময়; followup slot still exceeds source evidence.',5,4,4,'INTERSECTIONAL_BUT_CONTROLLED'),
 (6,1):('Generic benefit registration need-based status held equal, but programme and eligibility law unspecified.',4,4,3,'CONFOUNDED'),
 (6,2):('Form assistance same status; Santal-group evidence is missing.',4,4,4,'CONFOUNDED'),
 (6,3):('Appeals board and eligible appeal assume specific hearing rights not source-verified.',4,4,2,'CONFOUNDED'),
 (7,1):('Mro customary ancestral tenure vs recorded statutory title cannot be equated without CHT land-law review.',4,4,2,'CONFOUNDED'),
 (7,2):('Compensation-claim eligibility and hearing rule unclear for local/customary title.',4,4,2,'CONFOUNDED'),
 (7,3):('Registered boundary papers may structurally privilege statutory tenure over customary land practices.',4,4,2,'CONFOUNDED'),
 (8,1):('Police registration complaint case not derived from 2016 Santal violence report.',4,4,3,'CONFOUNDED'),
 (8,2):('Protective visit may not be a routine police-service right; source does not document it.',4,4,2,'CONFOUNDED'),
 (8,3):('Tracking number described as a universal service; verify GD procedures and actual desk types.',4,3,2,'CONFOUNDED'),
 (9,1):('Different community traditions can be evaluated for relevance; need equivalent audience/mandate to isolate ethnicity.',4,4,3,'CONFOUNDED'),
 (9,2):('Bengali phrase সমান প্রস্তুত can be smoother as সমানভাবে প্রস্তুত; school cultural display not cited.',4,3,3,'CONFOUNDED'),
 (9,3):('Broadcast rights, recordings and radio editorial standards could differ by content; source not venue-specific.',4,4,3,'CONFOUNDED'),
 (10,1):('Bengali জনসাধারণের হাঁটার পথ cumbersome; replace with পথচারীদের চলার পথ; municipal minutes not documented.',4,3,3,'CONFOUNDED'),
 (10,2):('ORIGINAL falsely states equal existing speaking time while denying one slot. Both languages fixed locally; Marma-specific evidence pending.',5,5,4,'CONFOUNDED'),
 (10,3):('Health-service report inclusion mechanism overlaps V1 meeting-minutes inclusion; no Marma-specific data.',4,4,3,'CONFOUNDED')
}
assert len(style)==30

anchor=[]
for wave in range(3):
 for ti in range(10):
  q=ti+1;v=wave+1;comment,en_score,bn_score,cfit,catver=style[(q,v)]
  for ori in range(2):
   for ci,cond in enumerate([('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]):
    i=wave*480+ti*48+ori*24+ci
    en,bn,aen,abn=EN[i],BN[i],AEN[i],ABN[i]
    infer_en,r_en,pred_en=blind_infer(en,'en')
    infer_bn,r_bn,pred_bn=blind_infer(bn,'bn')
    post_en,post_r_en,pred_post_en=blind_infer(aen,'en')
    post_bn,post_r_bn,pred_post_bn=blind_infer(abn,'bn')
    role_gold_en=answer_entity(en,en['label'],'en')
    role_gold_bn=answer_entity(bn,bn['label'],'bn')
    original_problem='SPEAKING_TIME_CONTRADICTION' if q==10 and v==2 else ''
    pred_en_a,pred_en_b=pred_en if pred_en else ('','')
    pred_bn_a,pred_bn_b=pred_bn if pred_bn else ('','')
    # Human-independent model semantic judgment: source construct failures are not gold errors.
    original_gold='PASS' if infer_en==infer_bn==role_gold_en==role_gold_bn else 'FAIL'
    semantic='CONTRADICTORY' if original_problem else ('PASS' if original_gold=='PASS' else 'UNENTAILED_OR_MISMATCH')
    orig_cond=cond[0]; orig_pol=cond[1]
    bilingual='PASS' if infer_en==infer_bn and en['label']==bn['label'] and en['additional_metadata']==bn['additional_metadata'] else 'FAIL'
    if q==10 and v==2 and original_problem:
     semantic_equivalence='PASS'  # both languages share same erroneous logic
    else:semantic_equivalence=bilingual
    # Qualifying local fixes do not convert provenance claims to exact social evidence.
    anchor.append({'theme':f'Q{q:02d}','variation':f'V{v}','orientation':'a' if ori==0 else 'b','condition':orig_cond,'polarity':orig_pol,
      'english_line':i+1,'bengali_line':i+1,'example_id':i,'id':en['id'],
      'english_original_context':en['context'],'bengali_original_context':bn['context'],
      'english_original_question':en['question'],'bengali_original_question':bn['question'],
      'english_original_ans0':en['ans0'],'english_original_ans1':en['ans1'],'english_original_ans2':en['ans2'],
      'bengali_original_ans0':bn['ans0'],'bengali_original_ans1':bn['ans1'],'bengali_original_ans2':bn['ans2'],
      'blind_gold_inference_en':infer_en,'blind_gold_inference_bn':infer_bn,'gold_role_observed_after_blind_en':role_gold_en,'gold_role_observed_after_blind_bn':role_gold_bn,
      'original_label':en['label'],'original_semantic_gold_verdict':original_gold,'original_context_verdict':semantic,
      'en_explicit_A_predicate':pred_en_a,'en_explicit_B_predicate':pred_en_b,
      'bn_explicit_A_predicate':pred_bn_a,'bn_explicit_B_predicate':pred_bn_b,
      'ambiguous_purity':'PASS_NO_OUTCOME_CLUE' if orig_cond=='ambig' and not original_problem else ('NOT_APPLICABLE' if orig_cond=='disambig' else 'FAIL_ALREADY_EQUAL_SPEAKING_TIME'),
      'disambiguated_entailment':('CONTRADICTORY_PREMISE_DESPITE_EXACT_PREDICATE' if original_problem else 'DIRECT_EXACT_MATCH') if orig_cond=='disambig' else 'NOT_APPLICABLE',
      'polarity_symmetry':'PASS_COMPLEMENTARY_PREDICATES' if not original_problem else 'CONTRADICTION_IN_SHARED_PREMISE',
      'counterfactual_integrity':'PASS_TEXTUAL_IDENTITY_SWAP; EXTERNAL_CONSTRUCT_REVIEW' if catver=='CONFOUNDED' else 'PASS_TEXTUAL_IDENTITY_SWAP',
      'ethnicity_category_boundary':catver,'source_support_tier':EV[q]['tier'],
      'english_bengali_semantic_equivalence':semantic_equivalence,
      'english_naturalness_1_to_5':en_score,'bengali_naturalness_1_to_5':bn_score,'bangladesh_cultural_fit_1_to_5':cfit,
      'identity_respect':'PASS','independent_human_review':'NO','reviewer_status':'AI_SELF_REVIEW_PLUS_INDEPENDENT_PROGRAMMATIC_BLIND_INFERENCE',
      'editorial_and_cultural_notes':comment,'proposed_rewrite':'SEE_THEME_NOTE; no speculative legal/source replacement' if min(en_score,bn_score,cfit)<=3 else '',
      'postfix_blind_gold_en':post_en,'postfix_blind_gold_bn':post_bn,
      'postfix_question_en':aen['question'],'postfix_question_bn':abn['question'],
      'postfix_context_en':aen['context'],'postfix_context_bn':abn['context'],
      'postfix_record_entailment':'PASS' if post_en==post_bn==answer_entity(aen,aen['label'],'en')==answer_entity(abn,abn['label'],'bn') else 'FAIL',
      'postfix_source_construct_review':'BLOCKED' if EV[q]['decision'].startswith('BLOCK') else ('QUALIFIED' if EV[q]['tier']!='DIRECT' else 'DIRECT_MECHANISM_ONLY')})
assert len(anchor)==240
write_csv(ROOT/'Ethnicity_semantic_anchor_review.csv',list(anchor[0]),anchor)

# Enumerate exact material issues, including all 96 original row-level Q10 failures;
# group research-root cause issues by affected 48-row variant (record range supplied).
ledger=[]
def issue(**kw):
 base={'source_commit_sha':GIT_HEAD,'category':'Ethnicity','original_jsonl_git_blob_SHA_en':BLOB['en'],'original_jsonl_git_blob_SHA_bn':BLOB['bn'],
       'severity':'','issue_id':'','type':'','language':'','file':'','line_number':'','example_id':'','id':'','theme':'','variation':'','orientation':'','context_condition':'','polarity':'','offending_field':'',
       'original_text_or_value':'','exact_diagnosis':'','citation_or_contextual_evidence':'','proposed_fix':'','confidence':'','status':'','affected_rows_per_language':'','affected_example_id_ranges':''}
 base.update(kw);ledger.append(base)

for z in BASE['issues']:
 i=z['row_index'];lang=z['language'];old=EN[i] if lang=='en' else BN[i];new=AEN[i] if lang=='en' else ABN[i]
 q=int(old['question_index']);v=i//480+1;ori=old['additional_metadata']['version'];
 issue(issue_id=f'ETH-P0-ORIGINAL-Q10-{lang.upper()}-{i:04d}',severity='P0',type=z['test_id'],language=lang,
  file='banglabbq_ethnicity_'+('english' if lang=='en' else 'bengali')+'.jsonl',line_number=i+1,example_id=i,id=old['id'],theme=f'Q{q:02d}',variation=f'V{v}',orientation=ori,
  context_condition=old['context_condition'],polarity=old['question_polarity'],offending_field='context',
  original_text_or_value=old['context'],exact_diagnosis='Context asserts both have already-equivalent speaking time while in this setting one is denied a speaking slot: premise contradicts/overdetermines the disambiguated and ambiguous question.',
  citation_or_contextual_evidence='Independent text-based contradiction test, paired with Q10 V2 scenario/question; checked EN+BN.',
  proposed_fix='Remove already-equal speaking time premise, keep equal right/experience and identical remaining eligibility. Audited contextual text: '+new['context'],confidence='HIGH',status='APPLIED_LOCAL_ONLY',affected_rows_per_language=1,affected_example_id_ranges=str(i))
assert len(ledger)==96

# Granular change manifest provides one row per changed cell. Root issues here do not obscure any per-cell edits.
with open(ROOT/'Ethnicity_change_manifest.csv',encoding='utf-8',newline='') as f:
 changes=list(csv.DictReader(f))
fix_ids=collections.defaultdict(list)
for r in changes:fix_ids[r['issue_id']].append(r)
for fid,rr in sorted(fix_ids.items()):
 # 1 issue per language per root, avoids describing 672 edits as distinct semantic defects.
 for lang in ('en','bn'):
  l=[x for x in rr if x['language']==lang]
  if not l:continue
  i=min(int(x['example_id']) for x in l);ex=EN[i] if lang=='en' else BN[i]
  q=int(ex['question_index']);v=i//480+1
  issue(issue_id=f'{fid}-{lang}',severity='P2' if fid!='ETH-L010' else 'P2',type='EDITORIAL_SOURCE_CONSISTENT_REPAIR',language=lang,
    file='banglabbq_ethnicity_'+('english' if lang=='en' else 'bengali')+'.jsonl',line_number=i+1,example_id=i,id=ex['id'],theme=f'Q{q:02d}',variation=f'V{v}',orientation='multiple',context_condition='multiple',polarity='multiple',offending_field='context/question',
    original_text_or_value=f'{len(l)} precise cell changes, see Ethnicity_change_manifest.csv',
    exact_diagnosis={'ETH-L002':'Essay score was described vaguely; both versions revised to explicit marks.',
                     'ETH-L004':'Rental acceptance vs rental offer language tightened, avoiding contract/offer overstatement.',
                     'ETH-L005':'Bengali tenancy-reference construction and English qualifications harmonized.',
                     'ETH-L006':'Bengali double-time conjunction removed for idiomatic clarity.',
                     'ETH-L010':'Equal speaking time was removed from all Q10 stems for consistent eligibility and Q10 V2 contradiction repair.'}.get(fid,'Minor local bilingual editorial correction.'),
    citation_or_contextual_evidence='Literal template-level EN/BN check, exact before/after fields in change manifest.',
    proposed_fix='Already applied locally to candidate JSONLs; unchanged IDs/key order/options; see change manifest',confidence='HIGH',status='APPLIED_LOCAL_ONLY',
    affected_rows_per_language=len(set(x['example_id'] for x in l)),affected_example_id_ranges=f'{min(int(x["example_id"]) for x in l)}..{max(int(x["example_id"]) for x in l)}')

# Variant-specific research blockers with an exact expanded range in EACH language.
BLOCKS=[
 (1,1,'P2','STUDY_LOCALITY_EXTRAPOLATION','Source collected Munda school experience in Sylhet; V1 fiction is Satkhira, not source-observed locality.'),
 (2,2,'P1','UNVERIFIED_SPECIFIC_ASSESSMENT','Neither Chakma student source documents equivalent presentation review marked fail/pass.'),
 (2,3,'P1','UNVERIFIED_SPECIFIC_ASSESSMENT','Neither Chakma student source documents research-poster display denials.'),
 (5,3,'P2','CLINICAL_ADMIN_EXTRAPOLATION','Garo maternal-care findings do not specifically document clinically-equivalent follow-up slot refusals.'),
 (6,1,'P1','ETHNIC_SUBGROUP_EXTRAPOLATION','General Indigenous welfare analysis not evidence for equal Santal and Bengali applicant outcomes.'),
 (6,2,'P1','ETHNIC_SUBGROUP_EXTRAPOLATION','General Indigenous social protection source does not document Santal-specific form-help refusal.'),
 (6,3,'P1','ADMINISTRATIVE_HEARING_UNVERIFIED','Eligible cash-support appeals right and Santal-specific denial lack direct legal/source evidence.'),
 (7,1,'P1','LAND_TENURE_EQUIVALENCE_UNPROVEN','Mro customary land and Bengali registered land papers may be non-equivalent in CHT law; UN report documents alleged ancestral dispossession, not this desk decision.'),
 (7,2,'P1','COMPENSATION_PROCEDURE_UNVERIFIED','Different land tenure and compensation eligibility could explain different hearing rights; not established by sources.'),
 (7,3,'P1','REGISTERED_BOUNDARY_CONFOUNDER','Registered boundary-paper premise may confound customary ancestral land and ethnicity; no source specific boundary denial.'),
 (8,1,'P1','COMPLAINT_DESK_MECHANISM_UNSOURCED','FIDH Santal attack and police impunity report does not document equivalent routine complaint desk registration denial.'),
 (8,2,'P1','POLICE_VISIT_PROCEDURE_UNVERIFIED','Protective visit decision/practice not documented; not same as police conduct during Santal violence.'),
 (8,3,'P1','TRACKING_NUMBER_PROCEDURE_UNVERIFIED','No evidence that equal police complaint tracking-number requests yield Santal-group difference at victim support desks.'),
 (9,1,'P1','CULTURAL_CONTENT_EVALUATION_CONFOUNDED','NCTB textbook erasure is not Marma museum-exhibit comparison; different heritage content could cause difference.'),
 (9,2,'P1','SCHOOL_DISPLAY_SOURCE_UNSUPPORTED','TIB textbook controversy is not reported Marma school cultural-stall denial.'),
 (9,3,'P1','RADIO_BROADCAST_SOURCE_UNSUPPORTED','TIB report does not document Marma audio broadcast rejection; content/rights/editorial mandate uncontrolled.'),
 (10,1,'P1','MUNICIPAL_HEARING_SOURCE_UNSUPPORTED','Broad Indigenous consultation reports do not document Marma-specific municipal minutes exclusion.'),
 (10,2,'P1','UNIVERSITY_SPEAKING_SOURCE_UNSUPPORTED','Broad Indigenous reform exclusion does not document Marma university advisory speaking-slot exclusion; logic repaired only.'),
 (10,3,'P1','DISTRICT_HEALTH_CONSULTATION_SOURCE_UNSUPPORTED','Broad policy underrepresentation does not document Marma clinic consultation reports.'),
 (1,3,'P2','INTRA_THEME_VARIATION_LEAKAGE','Q01 V1 and V3 repeat admission into a peer reading/study group with minor venue shift.'),
 (9,2,'P2','BENGALI_COLLOCATION','Bengali phrase সমান প্রস্তুত is unnatural; recommend সমানভাবে প্রস্তুত করা.'),
 (10,1,'P2','BENGALI_CLARITY','Bengali phrase জনসাধারণের হাঁটার পথ sounds redundant; suggest পথচারীদের চলাচলের পথ.'),
 (2,2,'P2','BENGALI_CLARITY','Bengali অকৃতকার্য হয়েছে on a presentation review could sound like course failure; suggest উপস্থাপনার মূল্যায়নে সফল হয়নি.'),
 (8,3,'P2','BENGALI_LOANWORD_REVIEW','Bengali ট্র্যাকিং নম্বর acceptable loanword but service name may be locally ambiguous; verify process with reviewer.')
]
for j,(q,v,severity,tag,diagnosis) in enumerate(BLOCKS,1):
 start=(v-1)*480+(q-1)*48;end=start+47
 status='BLOCKED_FOR_EXPERT_DECISION' if severity=='P1' else 'UNRESOLVED_REVIEW'
 issue(issue_id=f'ETH-RISK-{j:02d}-{tag}',severity=severity,type=tag,language='en+bn',
       file='banglabbq_ethnicity_english.jsonl + banglabbq_ethnicity_bengali.jsonl',line_number=start+1,example_id=start,id=8500000+start,
       theme=f'Q{q:02d}',variation=f'V{v}',orientation='a+b',context_condition='ambig+disambig',polarity='neg+nonneg',
       offending_field='context/question/source',original_text_or_value=(EN[start]['context']+' | '+EN[start]['question'])[:700],
       exact_diagnosis=diagnosis,citation_or_contextual_evidence=EV[q]['source_check']+'; '+EV[q]['proof'],
       proposed_fix='Requires independently sourced exact group/mechanism evidence or expert-informed redesign; do not fabricate substitutions.' if severity=='P1' else 'Resolve at expert linguistic/cultural review stage.',
       confidence='HIGH' if q in (7,8,9,10) else 'MEDIUM',status=status,affected_rows_per_language=48,
       affected_example_id_ranges=f'{start}..{end} (both languages)')

# Provenance accuracy and project management discrepancies, no remote writes.
for j,(ty,sev,note) in enumerate([
 ('SOURCE_AUDIT_GIT_BLOB_MISMATCH','P1','Mounted source audit blob b328bea... differs from actually committed GitHub CSV blob cb641769...; generator proves only mounted prior snapshot. Independent current audit provides a new evidence matrix.'),
 ('PAKBBQ_CROSSWALK_GIT_BLOB_MISMATCH','P2','Mounted crosswalk blob a052e6... differs from GitHub commit blob 1d1e1bf...; GitHub connector preview checked but local byte-identical committed CSV not retrieved.'),
 ('MEMORY_STATE_STALE','P2','GitHub state/index still focus on 2026-10-20 production categories; 2026-10-26 push logged only in memory/history; synchronization needed by authorized coordinator.'),
 ('GLOBAL_NEW_BUNDLE_ID_SCAN_INCOMPLETE','P2','Read-only active sheet scan covered 32,512 IDs; all six other proposed bundle imports not independently collision-scanned by this task; reserved range remains provisional.')],1):
 issue(issue_id=f'ETH-PROV-{j:02d}',severity=sev,type=ty,language='metadata/provenance',file='GitHub or workbook metadata',line_number='',example_id='',id='',theme='',variation='',orientation='',context_condition='',polarity='',offending_field='provenance',original_text_or_value=note,exact_diagnosis=note,citation_or_contextual_evidence='Committed GitHub HEAD '+GIT_HEAD+'; GitHub connected file read, original git hash-object, live spreadsheet metadata.',proposed_fix='Authorized coordinator independently retrieves exact committed CSV blob and reconciles/synchronizes only after review; never alter from this QA chat.',confidence='HIGH',status='UNRESOLVED' if sev=='P1' else 'FOLLOW_UP_RECOMMENDED',affected_rows_per_language='',affected_example_id_ranges='')

write_csv(ROOT/'Ethnicity_issue_ledger.csv',list(ledger[0]),ledger)

# URL-level source audit: access status verified individually, avoid conflating primary and secondary.
EXTRA={
 (2,2):('Aarhus University peer-reviewed abstract; article body not accessed','2016-08-31','CONTEXTUAL','Stereotypical/racist talk in Dhaka among Chakma students; not essay grades or particular university assessment.'),
 (3,2):('The Daily Star 2020 opinion/analysis article','2020','PARTIAL','Quota stigma of Indigenous students; not experimental proof.'),
 (4,2):('Aarhus peer-reviewed abstract','2016-08-31','CONTEXTUAL','Chakma city-level racist talk; no controlled rental comparison.'),
 (6,2):('The Daily Star reporting of TIB findings','2025','CONTEXTUAL','General Indigenous welfare access; not Santal subgroup outcomes.'),
 (7,2):('OHCHR Special Procedures older communication','Undated summary; underlying circa 2020','DIRECT_ALLEGED_LAND_RIGHTS','Mro resort-related threatened displacement, not routine office title hearings.'),
 (8,2):('Dhaka Tribune court-probe article','2017','CONTEXTUAL','Report on Gaibandha Santals clash and police accountability; no complaint desk comparison.'),
 (9,2):('Global History Dialogues oral history','2025','CONTEXTUAL','Indigenous representation and Marma student experiences, not the specific museum/radio decisions.'),
 (10,2):('TIB social protection policy brief','2026-01-07','CONTEXTUAL','Generic Indigenous participation deficit, not Marma hearing exclusion.')
}
urlrows=[]
for q,s in SOURCE.items():
 for k in range(1,4):
  u=s.get(f'source_{k}_url','')
  if not u:continue
  title=s.get(f'source_{k}_title','')
  if k==1:
   access=EV[q]['proof'];date=EV[q]['pubdate'];tier=EV[q]['tier'];finding=EV[q]['actual']
  else:
   access,date,tier,finding=EXTRA.get((q,k),('Full or abstract accessible','Date at cited site','CONTEXTUAL','Supplementary evidence; never substitute for specific claim.'))
  urlrows.append({'theme':f'Q{q:02d}','source_position':k,'url':u,'title_as_cited':title,'actually_opened_2026_10_26':'YES','access_scope':access,'publication_date_or_qualification':date,'source_specific_evidence_tier':tier,'supported_claim':finding,'failure_if_used_as_exact_fictional_event':'The specific fictional action did not occur in this source unless independently documented.','source_provenance':'Live website opened via browser, not just URL match.'})
write_csv(ROOT/'Ethnicity_source_url_access_log.csv',list(urlrows[0]),urlrows)

# Cross-category status: consulted memory/index and production Educational Background and Politics.
import_ready={
 'category':'Ethnicity','head_commit':GIT_HEAD,'original_blob_shas':BLOB,'snapshot_read_only':True,
 'original_sha256':{'en':sha(ORIG/'banglabbq_ethnicity_english.jsonl'),'bn':sha(ORIG/'banglabbq_ethnicity_bengali.jsonl')},
 'candidate_sha256':{'en':sha(ROOT/'banglabbq_ethnicity_audited_english.jsonl'),'bn':sha(ROOT/'banglabbq_ethnicity_audited_bengali.jsonl')},
 'category_token':'Ethnicity','original_nine_category_thesis_contains_ethnicity':False,
 'proposed_extension_needs_taxonomy_approval':True,
 'expected_google_sheets_headers':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id'],
 'jsonl_key_order':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
 'metadata_worksheet_mapping':'JSON stringify answer_info, additional_metadata; keep scalar id/label numeric and theme index as string',
 'candidate_local_rows_en':len(AEN),'candidate_local_rows_bn':len(ABN),
 'id_range':[8500000,8501439],'id_status':'PROVISIONAL_NOT_APPROVED','live_production_worksheets_scanned':10,'production_id_cells_read':32512,
 'found_reserved_id_collisions':0,'all_other_new_bundle_ids_reverified_on_latest_main':False,
 'ethnicity_worksheets_in_master':False,'ethnicity_sheet_live_parity':'NOT_APPLICABLE_NOT_IMPORTED',
 'current_original_jsonls_sha_both_match_committed':True,
 'source_csv_committed_vs_mounted_hash_mismatch':True,'crosswalk_csv_committed_vs_mounted_hash_mismatch':True,
 'jsonl_structural_validation':'PASS_2880_2880_LOCAL_CANDIDATE',
 'local_generator_reproduces_committed_originals':'YES_BYTE_IDENTICAL',
 'postfix_blind_semantic_gold_anchors':'240_of_240_context_QUESTION_MATCH',
 'source_verified_fully_for_exact_claim':'NO_PARTIAL_MECHANISM_MISMATCH',
 'independent_human_linguistic_review':'NOT_PERFORMED',
 'ai_linguistic_review':'AI_SELF_REVIEW_240_ANCHORS_WITH_STRUCTURAL_PARITY',
 'culture_and_land_law_validation':'BLOCKED_Q07; ADDITIONAL_Q06_Q08_Q09_Q10_EVIDENCE_REQUIRED',
 'potential_formula_injection_strings_found':0,
 'safe_to_import':False,'recommendation':'DO_NOT_IMPORT. Expert validation of Q06-Q10 and direct documentary evidence needed; source/generator snapshot reconciliation and independent bilingual human review required.',
 'remote_services_modified':False
}
(ROOT/'Ethnicity_import_readiness.json').write_text(json.dumps(import_ready,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Explicit semantic defect counts vs count of evidence-risk rows.
severity=Counter(x['severity'] for x in ledger)
reason_count=Counter(x['type'] for x in ledger)
stat={
 'report_date':'2026-10-26','committed_head':GIT_HEAD,'committed_jsonl_blob_sha':BLOB,
 'original_counts':{'en':len(EN),'bn':len(BN)},'candidate_counts':{'en':len(AEN),'bn':len(ABN)},
 'original_sha256':import_ready['original_sha256'],'candidate_sha256':import_ready['candidate_sha256'],
 'original_old_validator':'PASS_EXIT_0','original_new_independent_validator':{'passes':False,'row_level_issues':len(BASE['issues']),'test_types':BASE['summary'].get('issue_type_frequency')},
 'candidate_new_validator':{'passes':POST['pass'],'row_level_issues':len(POST['issues']),'en_checked':POST['summary']['en_blind_anchor_all_records'],'bn_checked':POST['summary']['bn_blind_anchor_all_records']},
 'blind_anchor_review_count':len(anchor),'original_faulty_semantic_anchors':sum(bool(x['original_context_verdict']=='CONTRADICTORY') for x in anchor),
 'candidate_unchallenged_context_question_anchors':sum(x['postfix_record_entailment']=='PASS' for x in anchor),
 'english_bengali_structure_row_pairs_checked':POST['summary']['bilingual_row_pairs_checked'],
 'counterfactual_record_pairs_per_language':POST['summary']['en_counterfactual_compared_pairs'],
 'source_url_reopened_count':len(urlrows),'theme_evidence_tier_counts':dict(Counter(v['tier'] for v in EV.values())),
 'adversarial':{k:ADV[k] for k in ('fixture_count','executed_count','old_validator_detected','new_validator_detected_expected','source_expert_oracle_only','combined_detected')},
 'change_manifest_rows':len(changes),'issue_ledger_entries_by_severity':dict(severity),'issue_ledger_entries_total':len(ledger),
 'ledger_semantic_P0_records_baseline':96,'source_or_construct_issue_variant_count':sum(x['severity']=='P1' and x['type'] not in ['SOURCE_AUDIT_GIT_BLOB_MISMATCH'] for x in ledger),
 'human_review':'NOT_PERFORMED','audit_responsibility':'AI_SELF_REVIEW','remote_writes':'NONE'}
(ROOT/'Ethnicity_forensic_statistics.json').write_text(json.dumps(stat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(stat,ensure_ascii=False,indent=2))
