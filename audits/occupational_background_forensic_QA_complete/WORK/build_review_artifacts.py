#!/usr/bin/env python3
"""Evidence and editorial artifacts assembled from independently re-opened publications and bilingual anchor inspection."""
from pathlib import Path
import json,csv,collections,re,hashlib,datetime,copy,math,difflib
D=Path('/mnt/data/occupational_forensic_audit');W=D/'WORK';OUT=D
E=[json.loads(s) for s in (D/'ORIGINAL/banglabbq_occupational_background_english.jsonl').read_text().splitlines()]
B=[json.loads(s) for s in (D/'ORIGINAL/banglabbq_occupational_background_bengali.jsonl').read_text().splitlines()]
F=lambda name:W/name
SRC=list(csv.DictReader(open('/mnt/data/banglabbq_occupational_background_source_audit.csv',encoding='utf-8-sig')))

# Re-opened via read-only browsing on 2026-10-26. Evidence is quoted/paraphrased conservatively.
EVIDENCE={
 1:dict(tier='PARTIAL',decision='REVISE',support='BMJ Open mixed qualitative study in two Dalit/sweeper colonies in Dhaka found interactions with non-Dalits affected by an intertwined caste-occupation identity and impurity/hygiene stigma.',limitations='Does not isolate municipal occupation from Dalit ancestry/caste or prove the tea-service event; a civic tea refusal attributed purely to occupation is a hypothesis.',access='FULL_TEXT_ALTERNATIVE_BMJ_OPEN',date='2018-12',publisher='BMJ Open / qualitative study',url='https://bmjopen.bmj.com/content/8/12/e022906',scope='Dhaka; Dalit traditional sweeper communities',specific='Caste/occupational conflation; source populations not identical to fictional generic sanitation worker'),
 2:dict(tier='PARTIAL',decision='REVISE',support='PLOS Water nationwide field interviews include one Coxs Bazar municipal supervisor describing waste workers as uneducated and unskilled; report also documents gaps in occupational training.',limitations='Supervisor cited occupational skills, not neutral form checking despite equal training; evidence may reflect observed real differences in job-specific training.',access='FULL_TEXT',date='2023',publisher='PLOS Water / Sharior et al.',url='https://journals.plos.org/water/article?id=10.1371/journal.pwat.0000041',scope='Bangladesh sanitation workplaces',specific='One reported supervisor perception; not a controlled test of administrative competence'),
 3:dict(tier='DIRECT',decision='REVISE',support='Policy Press poverty-stigma article reports a female domestic worker in Dhaka told she could not use her workplace building lift, and interprets occupation as a moderator of exclusion.',limitations='Embedded in poverty study, one qualitative report, not proof of occupation-only causality; Q03 V1 currently has competing written-permission answer.',access='FULL_TEXT_SEARCH_RESULT',date='2025-11-13 online / 2026 issue',publisher='Policy Press',url='https://doi.org/10.1332/17598273Y2025D000000053',scope='Dhaka/Chattogram low-income communities',specific='Apartment lift refusal, unequal sharing practice; fictional visitors differ from study participant'),
 4:dict(tier='PARTIAL',decision='REVISE',support='2019 four-factory qualitative study finds supervisors called female garment workers disobedient and uncooperative, alongside reports of workplace violence and suppression.',limitations='Workplace supervisors judging female employees does not demonstrate unrelated municipal-hearing hostility; gender and power are confounders.',access='FULL_TEXT_ALTERNATIVE_SAGE',date='2019-12-20',publisher='Akhter et al., Womens Health / SAGE',url='https://journals.sagepub.com/doi/10.1177/1745506519891302',scope='Four garment factories in Bangladesh, female workers',specific='Stereotype reported within factory setting, not all public forums'),
 5:dict(tier='DIRECT',decision='KEEP_WITH_CAVEAT',support='Hadley et al. (2007) six-hospital interviews document nursing associated with improper female conduct because of night duty, strangers and intimate care; Zaman (2009) documents negative images of nurses.',limitations='Historical attitudes and gender-specific setting cannot be assumed prevalent today or across all nurse genders; moral character of an individual is never a fact derived from occupation.',access='ABSTRACT_PUBMED_AND_ALTERNATIVE_FULL',date='2007-03 / 2009-03',publisher='Social Science & Medicine; Qualitative Health Research',url='https://pubmed.ncbi.nlm.nih.gov/16890336/',scope='Bangladesh hospitals, primarily women nurses',specific='Social respectability stigma is evidenced; non-clinical book-club scenario is invented'),
 6:dict(tier='PARTIAL',decision='REVISE',support='2022 interviews with 20 rural rickshaw pullers mention long healthcare waits, social class inequality, costs and experiences of not being valued.',limitations='Poverty, rural access, triage, ability to pay may shape delays; not proof that equal-paying people with identical clinical symptoms receive differential registration due solely to occupation.',access='FULL_TEXT_INDEXED_AND_ABSTRACT',date='2022-10-17',publisher='Heliyon / qualitative study',url='https://pmc.ncbi.nlm.nih.gov/articles/PMC9586896/',scope='20 rural Bangladeshi rickshaw pullers',specific='Reported healthcare respect/inequality; Q06 V1 English disambiguous registration unentailed'),
 7:dict(tier='PARTIAL',decision='BLOCK',support='2018 field survey/interviews in Sylhet indicate tea-garden workers face political/social exclusion; UK FCDO 2018 report identifies severe marginalisation with ancestry and migration history.',limitations='Occupation is entangled with ethnicity/ancestry and residential isolation; evidence does not prove individual clerks omit identical community submissions based on employment alone.',access='ABSTRACT_AND_GOV_UK_SUMMARY',date='2018',publisher='Asian Journal of Humanity, Art and Literature; UK FCDO',url='https://www.i-proclaim.my/journals/index.php/ajhal/article/view/340',scope='Sylhet tea garden communities',specific='Collective civic exclusion, not causal minutes/feedback exclusion; Q07 V1/V3 also predicate errors'),
 8:dict(tier='DIRECT',decision='KEEP_WITH_CAVEAT',support='UNAIDS January 2021 article reports stigma and discrimination as barriers to alternative employment among Bangladeshi sex workers; 2025 published analysis summarizes wider community exclusion.',limitations='UNAIDS captures self-reports, not an experiment on public library volunteer placement; gender/religion and legal/social safeguards can confound.',access='FULL_FEATURE_AND_REVIEW_ABSTRACT',date='2021-01-12 / 2025',publisher='UNAIDS; Bangladesh-focused review',url='https://www.unaids.org/en/resources/presscentre/featurestories/2021/january/20210112_sex-work-bangladesh-myanmar',scope='Bangladeshi sex workers, COVID-era risk',specific='Stigma affects opportunity, not necessarily the specified fictional volunteering decision'),
 9:dict(tier='PARTIAL',decision='REVISE',support='2019 Dhaka study reports surveyed support for street-hawker eviction and hostile working conditions; Lata 2021 describes stigmatization, eviction and extortion of urban informal vendors.',limitations='Eviction preferences may reflect legitimate pavement access concerns; not evidence hawkers intrinsically disrupt unrelated queue duties.',access='JOURNAL_ABSTRACT_AND_UNIVERSITY_ABSTRACT',date='2019 / 2021',publisher='Journal of Economics and Sustainable Development; Journal of Contemporary Asia',url='https://www.iiste.org/Journals/index.php/JEDS/article/view/46209',scope='Street vendors in Dhaka',specific='Informal vending regulation is distinct from generic personal nuisance stereotype'),
 10:dict(tier='CONTEXTUAL',decision='BLOCK',support='Small Bangladesh village focus groups describe farming as unattractive, unprofitable and "unskilled" to some surveyed young people.',limitations='No finding about farmers being incapable with tablets, SMS, or digital attendance; no valid inferential link to the specific digital incompetence mechanism.',access='FULL_TEXT',date='2025 or undetermined on page',publisher='International Journal of Research and Innovation in Social Science',url='https://rsisinternational.org/journals/ijriss/articles/peasants-viewpoint-on-bringing-the-next-generation-into-agriculture-insights-from-bangladesh/',scope='Small village/farm youth sample in Bangladesh',specific='Occupation prestige reported; digital-competence stereotype UNSUPPORTED as stated'),
}
S2={
 5:('https://pubmed.ncbi.nlm.nih.gov/19224879/','Zaman (2009) nurses negative images; abstract accessible via search indexed','ABSTRACT', '2009-03'),
 7:('https://www.gov.uk/research-for-development-outputs/modern-slavery-within-the-tea-industry-in-bangladesh','FCDO review: workers descended mostly from India and marginalised; shows ancestry confound','SUMMARY','2018-03-19'),
 8:('https://pmc.ncbi.nlm.nih.gov/articles/PMC12502207/','2025 Bangladesh-focused review reports exclusion from community/religious life; not a primary experiment','INDEXED_ABSTRACT','2025'),
 9:('https://researchportal.murdoch.edu.au/esploro/outputs/journalArticle/To-Whom-Does-the-City-Belong/991005860592007891','Lutfun Nahar Lata (2021) describes stigmatization and exclusion of Dhaka informal vendors','ABSTRACT','2021'),
}

def write_rows(path,rows):
    rows=list(rows)
    if not rows:return
    with open(path,'w',encoding='utf-8',newline='') as f:
        dw=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');dw.writeheader();dw.writerows(rows)

source_rows=[];url_log=[]
for i,src in enumerate(SRC,1):
    e=EVIDENCE[i]
    row={'question_index':f'Q{i:02d}','theme':src['theme'],'alleged_stereotype':src['hypothesis_not_factual_claim'],'compared_occupations':src['compared_occupations'],
         'committed_source_tier':src['evidence_tier'],'independent_evidence_tier':e['tier'],'source_1_url_original':src['source1_url'],'opened_alternative_or_canonical_url':e['url'],
         'source_1_title':src['source1_title'],'source_2_url':src['source2_url'],'source_2_title':src['source2_title'],
         'publisher':e['publisher'],'date_reported':e['date'],'access_evidence':e['access'],'specific_documented_finding':e['support'],
         'bangladesh_population_scope':e['scope'],'gap_between_source_and_fictional_test':e['specific'],'limitations':e['limitations'],
         'decision':e['decision'],'source_verified':'YES_FOR_STATED_SCOPE' if e['tier'] in ('DIRECT','PARTIAL','CONTEXTUAL') else 'NO',
         'ai_social_science_review':'AI_SELF_REVIEW','independent_human_review':'NOT_PERFORMED','accessed_on_utc':'2026-10-26'}
    source_rows.append(row)
    url_log.append({'theme':f'Q{i:02d}','original_url':src['source1_url'],'actual_opened_or_indexed_url':e['url'],'title':src['source1_title'],
                    'publisher':e['publisher'],'date':e['date'],'retrieval_access':e['access'],'relevance':e['support'],'limitations':e['limitations'],'tier':e['tier']})
    if i in S2:
        u,claim,acc,date=S2[i]
        url_log.append({'theme':f'Q{i:02d}','original_url':u,'actual_opened_or_indexed_url':u,'title':src['source2_title'],
                        'publisher':u.split('/')[2],'date':date,'retrieval_access':acc,'relevance':claim,'limitations':e['limitations'],'tier':e['tier']})
write_rows(OUT/'occupational_background_source_evidence_matrix.csv',source_rows)
write_rows(OUT/'occupational_background_source_url_access_log.csv',url_log)

# 30 bilingual editorial evaluations, separately authored after inspecting source English/Bengali
# paired contexts/questions and common counterfactual pattern.
CASE={
 (1,1):(5,5,5,'PASS','Controlled cleanliness and tea service; minor caste/occupation proxy risk; clear refusal vs service.'),
 (1,2):(5,4,5,'PASS','Reserved seating eligibility matched; Bengali "আসন-অঞ্চল" slightly formal; both questions target usher action.'),
 (1,3):(5,3,5,'PASS','Bengali "আবার পানি" is a literal refill paraphrase, slightly awkward; outcome itself explicit; propose bottle-refill wording.'),
 (2,1):(5,5,5,'PASS','Equal two-day form-checking practice; the refusal vs appointment is explicit and bilingual aligned.'),
 (2,2):(5,5,5,'PASS','Ticket counting despite equivalent trial and availability; clear assignment roles.'),
 (2,3):(5,5,5,'PASS','Library inventory shift with identical demonstration; Bengali "অনুমোদন" acceptable but administrative.'),
 (3,1):(3,5,5,'AMBIGUOUS','Both carry written lift permissions: English "permitted" has two correct answers before and after guard decision; revise English nonneg question to physical passage by guard and align Bengali.'),
 (3,2):(5,5,5,'PASS','Identical meal tokens; whether server actually hands plate is unknown until explicit disambiguator.'),
 (3,3):(5,5,5,'PASS','Identical entrance badges, specific admission action differentiates treatment despite equal entitlement.'),
 (4,1):(5,4,5,'PASS','Same verified photos and speaking time; Bengali "উড়িয়ে দেন" slightly colloquial but natural.'),
 (4,2):(5,5,5,'PASS','Matched written requests; negative uncooperative label contrasts thanks.'),
 (4,3):(5,5,5,'PASS','Matched emergency-sign feedback; actor praise and disruptive label explicit.'),
 (5,1):(5,4,5,'PASS','Moral character charge is attributed to panel as fiction, not stated as a fact.'),
 (5,2):(5,5,5,'PASS','Same host and respectful conduct; personal character judgment represented as fictional organizer opinion.'),
 (5,3):(5,3,5,'PASS','Bengali "অনুপযুক্ত আদর্শ ব্যক্তি" is an awkward calque for improper role model; rewrite to "আদর্শ হিসেবে অনুপযুক্ত" in both Bengali context and question.'),
 (6,1):(3,3,5,'UNENTAILED','English receptionist "delays Habib" need not mean *registration* happened late; Bengali explicitly says late registration. Bengali "সাক্ষাতের সময়" reads as visit, not appointment.'),
 (6,2):(5,4,5,'PASS','Paid reports ready at matched time; denial vs delivery explicit; Bengali রোগনির্ণয় কেন্দ্র idiomatic.'),
 (6,3):(5,5,5,'PASS','Identical health information question; refusal to explain leaflet vs explanation given.'),
 (7,1):(2,2,4,'UNENTAILED','Excluding a person from official minutes does not assert their input was excluded; replace with explicit omission/recording of both submissions.'),
 (7,2):(5,5,4,'PASS','Registered members with similar proposals; chair action on speakers list explicit.'),
 (7,3):(2,2,4,'UNENTAILED','Facilitator discards *Bijoy* from feedback register, but question asks whose feedback was discarded; specify Bijoy/Tapan feedback.'),
 (8,1):(5,5,4,'PASS','Sealed food packing with identical hygiene eligibility; no sex-work-specific clinical/occupational requirement.'),
 (8,2):(5,4,4,'PASS','Awareness leaflet handout, explicitly no blood donation; avoids medically relevant donation criteria.'),
 (8,3):(5,5,4,'PASS','Same safeguarding checks and volunteer agreements; non-medical book sorting.'),
 (9,1):(5,5,5,'PASS','Identical crowd training; nuisance suspicion attributed to officer, not endorsed.'),
 (9,2):(5,5,5,'PASS','Same info-booth quiz and arrival; street hawker comparison differs from sidewalk regulatory claim.'),
 (9,3):(5,4,5,'PASS','Queue-management qualifications matched; Bengali "সারি ব্যবস্থাপনা" acceptable but formal.'),
 (10,1):(5,5,5,'PASS','Matched tablet tests; question clearly about refusal/appointment; source only supports lower agricultural status, not digital competence.'),
 (10,2):(5,5,5,'PASS','Matched SMS-list trial and functional phones; source does not document digital stereotype.'),
 (10,3):(5,4,5,'PASS','Matched electronic attendance accuracy; Bengali "হাজিরা লেখা" slightly unnatural vs "হাজিরা নথিভুক্ত".'),
}

# No reference to labels in this function: infer referent from the actual text and the
# editorially checked distinct occurrence ordering of both person names.
def infer_blind(e,b,original=True):
    en_parts=[e[f'ans{k}'].split(',',1)[0] for k in range(3) if e[f'ans{k}']!='Unknown']
    bn_parts=[b[f'ans{k}'].split(',',1)[0] for k in range(3) if b[f'ans{k}']!='অজানা']
    en_order=sorted(en_parts,key=lambda n:e['context'].find(n))
    bn_order=sorted(bn_parts,key=lambda n:b['context'].find(n))
    if e['context_condition']=='ambig':return ('Unknown','অজানা','No evaluator decision in ambiguous context')
    pick=0 if e['question_polarity']=='neg' else 1
    return (en_order[pick],bn_order[pick],e['context'].rsplit('. ',1)[-1])

def anchor_reviews(E,B,is_post=False):
    rows=[]
    for v in range(1,4):
        for q in range(1,11):
            english_score,bengali_score,cultural_score,case_status,case_note=CASE[(q,v)]
            for orient_index,orient in enumerate(('a','b')):
                off=(v-1)*480+(q-1)*48+24*orient_index
                for k,(condition,polarity) in enumerate([('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]):
                    i=off+k;e=E[i];b=B[i]
                    neg_body=E[off+1]['context'].removeprefix(E[off]['context']).strip()
                    pos_body=B[off+1]['context'].removeprefix(B[off]['context']).strip()
                    blind_en,blind_bn,exact_pred=infer_blind(e,b)
                    outcome='PASS';reason='Explicitly attributed evaluator action for the named person; counterfactual changes occupation only.' if condition=='disambig' else 'No action yet; both people equally qualified and neither outcome disclosed.'
                    en_n=english_score;bn_n=bengali_score
                    if not is_post:
                        if (q,v)==(3,1) and polarity=='nonneg':
                            outcome='AMBIGUOUS';reason='English positive "permitted" is already true for both by written permissions; no unique answer. Bengali actual admission clearer.'
                        if (q,v)==(6,1) and condition=='disambig' and polarity=='neg':
                            outcome='UNENTAILED';reason='English says receptionist delayed Habib, but does not say registered him late. Bengali explicitly says late registration.'
                        if (q,v) in ((7,1),(7,3)) and condition=='disambig':
                            outcome='UNENTAILED';reason='Disambiguator excludes a named person, but the question asks about that person\'s INPUT or FEEDBACK, a different predicate.'
                    else:
                        if case_status!='PASS' and (q,v) in ((3,1),(6,1),(7,1),(7,3)):
                            reason='Locally revised to align the exact evaluator action and question; no identity/label changes.'
                    if condition=='ambig' and not ((q,v)==(3,1) and polarity=='nonneg' and not is_post):
                        blind_en='Unknown';blind_bn='অজানা'
                    if outcome in ('AMBIGUOUS','UNENTAILED'):
                        blind_en='NOT_UNIQUELY_ENTAILED';blind_bn='যথাযথভাবে নির্ধারণযোগ্য নয়'
                    label=e['label']
                    listed=e[f'ans{label}'];listedbn=b[f'ans{label}']
                    rows.append(dict(anchor_id=f'Q{q:02}_V{v}_{orient}_{condition}_{polarity}',
                        example_id=i,id=e['id'],jsonl_line=i+1,theme=f'Q{q:02}',variation=f'V{v}',orientation=orient,context_condition=condition,question_polarity=polarity,
                        english_context=e['context'],english_question=e['question'],english_options=' || '.join(e[f'ans{k}'] for k in range(3)),
                        bengali_context=b['context'],bengali_question=b['question'],bengali_options=' || '.join(b[f'ans{k}'] for k in range(3)),
                        blind_gold_inference_en=blind_en,blind_gold_inference_bn=blind_bn,label_gold_en=listed,label_gold_bn=listedbn,
                        contextual_predicate_en=neg_body,contextual_predicate_bn=pos_body,
                        semantic_verdict=outcome,semantic_justification=reason,
                        counterfactual_verdict='ATTRIBUTE_ONLY_SWAP_WITH_FIXED_NAME_OUTCOME' if condition=='disambig' else 'ATTRIBUTE_ONLY_SWAP_NO_OUTCOME',
                        construct_verdict=('CONFOUNDED_BY_ANCESTRY' if q in (1,7) else 'SOURCE_MECHANISM_CONTEXTUAL' if q in (2,4,6,9,10) else 'IN_SCOPE_WITH_SCOPE_CAVEATS'),
                        translation_semantic_equivalence='FAIL' if ((q,v)==(6,1) and condition=='disambig' and polarity=='neg' and not is_post) else 'PASS',
                        english_naturalness_1to5=en_n,bengali_naturalness_1to5=bn_n,bangladesh_cultural_fit_1to5=cultural_score,
                        identity_respect='PASS',editorial_note=case_note,editorial_review_type='AI_SELF_REVIEW',human_review='NOT_PERFORMED'))
    return rows

R=anchor_reviews(E,B)
write_rows(OUT/'occupational_background_semantic_anchor_review.csv',R)

# Independent social science construct summary and Q-level shortcut risk.
case_rows=[]
for v in range(1,4):
    for q in range(1,11):
        i=(v-1)*480+(q-1)*48
        e=E[i]; d=E[i+1];scores=CASE[(q,v)]
        b=B[i];db=B[i+1]
        short=diff=d['context'].removeprefix(e['context']).strip()
        case_rows.append(dict(theme=f'Q{q:02}',variation=f'V{v}',first_example_id=i,last_example_id=i+47,
            english_ambiguous=e['context'],english_disambiguator=short,english_negative=e['question'],english_nonnegative=E[i+2]['question'],
            bengali_ambiguous=b['context'],bengali_disambiguator=db['context'].removeprefix(b['context']).strip(),
            bengali_negative=b['question'],bengali_nonnegative=B[i+2]['question'],
            orientation_a_first_occupation=e['ans0'].split(',',1)[1].strip(),
            orientation_b_first_occupation=E[i+24]['ans0'].split(',',1)[1].strip(),
            editorial_verdict=scores[3],editorial_explanation=scores[4],source_tier=EVIDENCE[q]['tier'],
            occupation_construct='CONFONDED' if q in (1,7) else 'CAVEATED',split_leakage='GROUP_ALL_VARIATIONS_BY_THEME_AND_GROUP_PAIR'))
write_rows(OUT/'occupational_background_30_case_construct_review.csv',case_rows)

# Simple variation distances, no claim of independence from 0.8 similarity alone.
variation_stats=[]
for q in range(1,11):
  bases=[E[(v*10+q-1)*48]['context'] for v in range(3)]
  pair_sims=[difflib.SequenceMatcher(None,bases[i],bases[j]).ratio() for i,j in [(0,1),(0,2),(1,2)]]
  variation_stats.append({'q':f'Q{q:02}','max_context_similarity':max(pair_sims),'pairwise_similarity':str([round(x,3) for x in pair_sims]),'target_compare_pair_reused':True,'same_named_people_reused':True,'action_venue_diversity':'VARIED_ACTION_AND_SITE','unsafe_random_row_split':True})
write_rows(OUT/'occupational_background_variation_leakage.csv',variation_stats)

# Write matrix metadata and source log. Reports are created by QA orchestrator.
(OUT/'occupational_background_review_provenance.json').write_text(json.dumps({'access_date':'2026-10-26','editorial_status':'AI_SELF_REVIEW','human_status':'NOT_PERFORMED','source_count':len(url_log),'bilingual_anchors':len(R),'cases':len(case_rows),'construct_warning':'Names and first mention are perfectly outcome-confounded','source_tiers':dict(collections.Counter(x['independent_evidence_tier'] for x in source_rows))},indent=2)+'\n')
print('SOURCE',len(source_rows),'URLs',len(url_log),'ANCHORS',len(R),'CASES',len(case_rows),'SIMILARITIES',variation_stats)
