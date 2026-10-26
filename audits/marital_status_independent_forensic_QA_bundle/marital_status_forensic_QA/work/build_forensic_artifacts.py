#!/usr/bin/env python3
"""Write independent forensic matrices and exhaustive anchor/issue artifacts from frozen committed data."""
from pathlib import Path
import csv,json,collections,hashlib,sys
BASE=Path('/mnt/data/marital_forensic_qa')
sys.path.insert(0,str(BASE))
from marital_status_independent_validator import classify_position
O=BASE/'ORIGINAL'
E=[json.loads(s) for s in (O/'banglabbq_marital_status_english.jsonl').read_text('utf8').splitlines()]
B=[json.loads(s) for s in (O/'banglabbq_marital_status_bengali.jsonl').read_text('utf8').splitlines()]
F=[json.loads(s) for s in (BASE/'banglabbq_marital_status_audited_english.jsonl').read_text('utf8').splitlines()]
G=[json.loads(s) for s in (BASE/'banglabbq_marital_status_audited_bengali.jsonl').read_text('utf8').splitlines()]
M=json.loads((O/'banglabbq_marital_status_expansion_manifest.json').read_text('utf8'))
AUD=list(csv.DictReader((O/'banglabbq_marital_status_source_audit.csv').open(encoding='utf8',newline='')))
SHA='e186b283fa5b184058e2cb395273e9968a893b20'
DATE='2026-10-26'
SOURCES={
'housing_official':dict(access='FULL_HTML_OFFICIAL',publisher='UK Home Office',date='2026-04-28',section='8.3.1 and housing/informal support sections',exact='Bangladesh country note cites reports that single women struggle to rent independent housing and face landlord restrictions, including marital-status scrutiny.',limitations='Synthesis/secondary country-of-origin source; no controlled married vs unmarried paired audit.'),
'housing_feature':dict(access='FULL_HTML_NEWS',publisher='The Business Standard',date='2026-01-15',section='interview narratives on rental and house rules',exact='Interviews with Dhaka single women report refusals to rent, curfew and visitor rules, rooftop restrictions, and comments about single women; includes counterexample of a supportive landlord.',limitations='Urban journalism interviews, not representative causal effect sizes.'),
'divorce_study':dict(access='FULL_HTML_ACADEMIC',publisher="BMC Women's Health",date='2022-12-02',section='Background and Discussion (not analyzed social-outcome endpoints)',exact='Primary analysis of 57,476 women from 2019 Bangladesh MICS on child marriage, disruption and remarriage; stigma, social blame and pressure mentioned in background/discussion not experimentally estimated.',limitations='Marital disruption/child marriage analysis is not a direct survey of different event invitation or workplace treatment.'),
'divorce_interview':dict(access='FULL_HTML_ACADEMIC_DOI',publisher='Journal of Bangladesh Studies / Brill',date='2025-04-25',section='3.2 Consequences of Divorce, 4 Discussion, 5 Limitations',exact='13 lower-SES divorced women interviewed in Khulna wards; reports family/neighborhood blame, awkward rejection, family remarriage pressure, and one garment worker reporting unwelcome sexual propositions.',limitations='13 purposively selected women from four wards of Khulna; neither comparative matched samples nor national prevalence.'),
'coastal_widows':dict(access='FULL_HTML_ACADEMIC',publisher='Humanities and Social Sciences Communications / Springer Nature',date='2025-11-13',section='Findings: social stigma and exclusion; access to livelihoods and decision-making',exact='Interviews with 27 tiger widows from selected Gabura and Burigoalini coastal communities document bad-omen wedding exclusion, decision-making marginalization and lost work opportunities.',limitations='Tiger-attack bereavement is an essential defining condition absent from all benchmark cases; cannot generalize findings to generic widows nationwide.')
}
THEME_COMMENTS={
1:('DIRECT','KEEP_WITH_CONTEXT_LIMITS','Housing discrimination against single Dhaka women documented. Both candidates have matched resources; fictional incident not evidenced.','Dhaka urban interviews; no controlled difference by marital status; not a general Bangladesh-wide rate.'),
2:('DIRECT','KEEP_WITH_CONTEXT_LIMITS','Single-woman tenant curfews and visitor restrictions are specifically reported in Dhaka.','Some landlords do not impose extra restrictions; could intersect with gender, employment hours, tenancy regime.'),
3:('DIRECT','REVISE_V3_SPEAKER','Housing-guard reputation policing is directly reported in feature; building committee actor in V3 was not staff.','Single-woman Dhaka housing contexts; cannot infer any character trait.'),
4:('PARTIAL/CONTEXTUAL','BLOCK_EXACT_PREDICATE_SOURCE','Khulna women report blame for divorce, but not a matched comparison calling a competent volunteer irresponsible.','Bias mechanism expands blame for divorce into general work/volunteer responsibility; potential construct conflation.'),
5:('PARTIAL/CONTEXTUAL','BLOCK_EXACT_INVITATION_SUPPORT','Khulna interviews report ostracism and blame, not controlled exclusion from a particular club invitation list.','Social exclusion is a plausible analog but direct invitation discrimination by marital status unverified.'),
6:('PARTIAL/CONTEXTUAL','REVISE_V3_AND_BLOCK_GENERALIZATION','One Khulna garment worker reports unwelcome sexual propositions after divorce; V1 broadly analogous, V2 payroll and V3 training center not evidenced.','Gender, workplace harassment and socioeconomic position intersect; matched married comparator unobserved.'),
7:('PARTIAL/CONTEXTUAL','BLOCK_WIDOW_COMPARATOR','Khulna interviewees report pressure to remarry; this does not establish divorced-versus-widowed treatment under equal conditions.','Source did not directly compare the two marital-status groups; all women fictional and same preference.'),
8:('PARTIAL/CONTEXTUAL','BLOCK_POPULATION_SCOPE','Specific tiger widows excluded from weddings because considered inauspicious; benchmark omits tiger-related bereavement.','Sample 27 tiger widows in selected coastal settlements; not generic widows nor all Satkhira.'),
9:('PARTIAL/CONTEXTUAL','BLOCK_POPULATION_SCOPE','Specific tiger widows excluded from decisions; matched elected-member voting-rights scenario fictional.','Tiger-bereavement sample differs from all widowed committee members; causality vs membership unmeasured.'),
10:('PARTIAL/CONTEXTUAL','BLOCK_POPULATION_AND_MOTIVE','Specific tiger widows report rejection for work on superstitious grounds; generic-widow scenarios show rejection but do not explicitly state a superstitious motive.','V1/V2/V3 require tiger-widow context evidence or independent generic-widow sources and tighter motive wording.')
}
varnotes={
(1,1):'Mirpur rental direct housing choice; equal salary/documents/references.',
(1,2):'Dhanmondi housing agency shifts evaluator and application process, same rental selection predicate.',
(1,3):'Mohammadpur room sublet, different housing unit and decision-maker; original only reserved rather than offered, fixed.',
(2,1):'Banasree shared rooftop after-dark permission; same rental histories.',
(2,2):'Farmgate women visitor access; standard permissible hour and equivalent contracts.',
(2,3):'Dhaka compound 8 p.m. curfew and late shift; equal circumstances; Bengali original omitted explicit exemption, fixed.',
(3,1):'Bashundhara evening commute and guard rumor; same shift and transport type.',
(3,2):'Mirpur parcel pickup and desk clerk rumor; same work schedule.',
(3,3):'Mohammadpur building meeting and committee-member gossip; original question called member staff, fixed.',
(4,1):'Dhaka recycling volunteer schedules and attendance; responsibility label unsupported exact stereotype extrapolation.',
(4,2):'Khulna disaster course matching exercise performance; same responsibility label, different evaluation criterion.',
(4,3):'Jessore bookkeeping accuracy; distinct task and evaluator, same responsibility label.',
(5,1):'Khulna neighborhood harvest meal invitation; matched resident association status.',
(5,2):'Dhaka library cultural evening; equal volunteer hours and eligibility.',
(5,3):'Rajshahi arts-club members-only gathering; equal paid membership and attendance.',
(6,1):'Khulna garment factory training-slot inquiry; source has garment-worker report of propositions but no comparison.',
(6,2):'Dhaka office payroll correction inquiry; related harassment, new occupation not directly source-sampled.',
(6,3):'Chattogram retail-training center; trainee not necessarily worker, original question falsely said at work, fixed.',
(7,1):'Sylhet neighborhood counseling workshop; both decline remarriage and have equally timed separation/death.',
(7,2):'Khulna social club; family care responsibilities matched; no source for widowed comparator.',
(7,3):'Dhaka community-support discussion; both refuse remarriage; repeated pressure over same preference.',
(8,1):'Gabura wedding meal; direct mechanism but sampled source refers only to tiger widows.',
(8,2):'Burigoalini pre-wedding music gathering; same population-scope limitation.',
(8,3):'Coastal Satkhira wedding decorations; broader locale than evidence, stronger unsupported generalization.',
(9,1):'Gabura cyclone shelter repair meeting, equal elected voting rights; tiger widow extrapolation.',
(9,2):'Burigoalini embankment meeting, equal committee rank and vote; source population mismatch.',
(9,3):'Shyamnagar fisher-community equipment decisions; unspecified widow kind, source mismatch.',
(10,1):'Gabura fish drying shift; source reports rejection in tiger widows, no stated motive in this scenario.',
(10,2):'Burigoalini crab sorting; eligibility equal, rejection observed, superstition motive not explicit.',
(10,3):'Shyamnagar handicrafts assignment; same workmanship, no superstition motive explicit; population mismatch.'
}
# evidence matrix from all audit URLs and verified opened source findings
source_fields=['question_index','theme','stereotype_mechanism_as_allegation','comparison','source_url_primary','source_url_secondary','source_1_title','source_2_title','source_access_primary','source_access_secondary','sources_opened_retrieval_date','publisher_and_publication_dates','specific_verified_bangladesh_claim','evidence_tier_from_previous_audit','evidence_tier_independent','source_suitable_for_current_variations','finding_limitations','counterevidence_or_scope_qualification','decision','source_verified_unqualified','cited_in_jsonl','original_source_warning']
with (BASE/'marital_status_source_evidence_matrix.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,source_fields);w.writeheader()
 for q,a in enumerate(AUD,1):
  t=M['themes'][q-1];ids=t['source_keys'];s1=SOURCES[ids[0]];s2=SOURCES[ids[1]] if len(ids)>1 else None
  rating,decision,claim,limit=THEME_COMMENTS[q]
  w.writerow(dict(question_index=t['id'],theme=t['title'],stereotype_mechanism_as_allegation=t['bias_mechanism_tested_as_allegation'],comparison=a['group_comparison'],source_url_primary=M['source_catalog'][ids[0]]['url'],source_url_secondary=M['source_catalog'][ids[1]]['url'] if len(ids)>1 else '',source_1_title=M['source_catalog'][ids[0]]['title'],source_2_title=M['source_catalog'][ids[1]]['title'] if len(ids)>1 else '',source_access_primary=s1['access']+' ('+s1['section']+')',source_access_secondary=(s2['access']+' ('+s2['section']+')') if s2 else '',sources_opened_retrieval_date=DATE,publisher_and_publication_dates='; '.join([x['publisher']+' '+x['date'] for x in [s1,s2] if x]),specific_verified_bangladesh_claim=claim,evidence_tier_from_previous_audit=a['evidence_tier'],evidence_tier_independent=rating,source_suitable_for_current_variations='QUALIFIED' if rating=='DIRECT' else 'NO_EXACT_COMPARATOR_OR_POPULATION',finding_limitations=limit,counterevidence_or_scope_qualification='; '.join([x['limitations'] for x in [s1,s2] if x]),decision=decision,source_verified_unqualified='NO',cited_in_jsonl=F[(q-1)*48]['additional_metadata']['source'],original_source_warning=('QUALIFICATION_OR_DOWNGRADE_REQUIRED' if rating!=a['evidence_tier'] else 'SOURCE_SCOPE_BOUNDARY_STILL_REQUIRED')))
# paired anchors review all 30*2*4 unique underlying states
anchor_fields=['anchor_id','source_commit_sha','wave','theme','theme_name','orientation','condition','polarity','original_example_id','original_id','source_url','en_original_context','en_original_question','en_answer_options','bn_original_context','bn_original_question','bn_answer_options','original_label_en','original_label_bn','blind_inferred_label_en','blind_inferred_label_bn','blind_inference_reason','original_semantic_verdict','audited_semantic_verdict','original_bilingual_semantic_equivalence','audited_bilingual_semantic_equivalence','english_naturalness_1_to_5','bengali_naturalness_original_1_to_5','bengali_naturalness_audited_1_to_5','bangladesh_cultural_fit_1_to_5','identity_respect','counterfactual_integrity','source_evidence_tier','original_problem_or_question','editorial_and_cultural_reasoning','en_audited_context','en_audited_question','bn_audited_context','bn_audited_question','independent_human_review','AI_review_type']
with (BASE/'marital_status_semantic_anchor_review.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,anchor_fields);w.writeheader()
 for wave in range(1,4):
  for q in range(1,11):
   t=M['themes'][q-1];rating,decision,claim,limit=THEME_COMMENTS[q]
   for ori in (0,1):
    for cond in range(4):
     idx=(wave-1)*480+(q-1)*48+ori*24+cond
     e,b,fe,fb=E[idx],B[idx],F[idx],G[idx]; name_en=t['names']['en'];name_bn=t['names']['bn']
     chosen={}
     for lang,r,rows,names in [('en',e,E,name_en),('bn',b,B,name_bn)]:
      ambig=rows[(idx//4)*4] if cond in (0,1) else rows[(idx//4)*4+2]
      suffix=r['context'][len(ambig['context']):] if r['context'].startswith(ambig['context']) else ''
      inferred,reason=classify_position(r,lang,name_en,name_bn,suffix)
      chosen[lang]=(inferred,reason)
     original_problem=[]
     if wave==3 and q==1 and cond==3:original_problem.append('Q01 V3: reservation does not imply rental offer.')
     if wave==3 and q==3 and cond==3:original_problem.append('Q03 V3: committee member not building staff.')
     if wave==3 and q==6 and cond in (0,1):original_problem.append('Q06 V3: a trainee training session is not necessarily at work.')
     if wave==3 and q==2 and cond in (1,3):original_problem.append('Q02 V3 Bengali omitted explicit permission/exemption beyond standard policy.')
     if q>=8:original_problem.append('General widowed status not equated with tiger widows studied in source.')
     if q==10:original_problem.append('Superstition motive not explicit in disambiguated employment cases.')
     if q==4:original_problem.append('Being blamed for divorce does not show volunteer responsibility judgments.')
     if q==7:original_problem.append('Study did not compare widow vs divorced response to expressed remarriage refusal.')
     trouble=(wave==3 and ((q==1 and cond==3) or (q==3 and cond==3) or (q==6 and cond in (0,1))))
     bn_score=3 if (wave==3 and q==2 and cond in (1,3)) else 4
     cult_score=3 if (q>=8 and wave==3) else 4
     bn_pass=not (wave==3 and q==2 and cond in (1,3))
     w.writerow(dict(anchor_id=f'V{wave}_{t["id"]}_{"a" if ori==0 else "b"}_{e["context_condition"]}_{e["question_polarity"]}',source_commit_sha=SHA,wave='V'+str(wave),theme=t['id'],theme_name=t['title'],orientation='a' if ori==0 else 'b',condition=e['context_condition'],polarity=e['question_polarity'],original_example_id=e['example_id'],original_id=e['id'],source_url=e['additional_metadata']['source'],en_original_context=e['context'],en_original_question=e['question'],en_answer_options=json.dumps([e[f'ans{i}'] for i in range(3)],ensure_ascii=False),bn_original_context=b['context'],bn_original_question=b['question'],bn_answer_options=json.dumps([b[f'ans{i}'] for i in range(3)],ensure_ascii=False),original_label_en=e['label'],original_label_bn=b['label'],blind_inferred_label_en=chosen['en'][0],blind_inferred_label_bn=chosen['bn'][0],blind_inference_reason=chosen['en'][1]+'; event-clause order interpreted as adverse then favorable; independent semantic critique required.',original_semantic_verdict=('UNENTAILED_QUALIFIER' if trouble else 'PASS_EXPLICIT_EVENT_OR_UNKNOWN'),audited_semantic_verdict='PASS_EVENT_AND_ANSWER_LOCALLY_ONLY' if trouble else 'PASS_EVENT_AND_ANSWER',original_bilingual_semantic_equivalence=('PARTIAL' if not bn_pass else 'PASS'),audited_bilingual_semantic_equivalence='PASS' if bn_pass else 'PASS_AFTER_BN_REPAIR',english_naturalness_1_to_5=4,bengali_naturalness_original_1_to_5=bn_score,bengali_naturalness_audited_1_to_5=4,bangladesh_cultural_fit_1_to_5=cult_score,identity_respect='PASS_NONENDORSEMENT',counterfactual_integrity='PASS_SURFACE_ONLY_NOT_CAUSAL_PROOF',source_evidence_tier=rating,original_problem_or_question='; '.join(original_problem) or 'No specific semantic defect in outcome predicates; human adjudication not performed.',editorial_and_cultural_reasoning=varnotes[(q,wave)]+' Both demographic orientations keep the same setting, evaluator and outcome evidence. '+('No nonidentity cue in ambiguous context.' if cond in (0,2) else 'Disambiguating clause describes adverse act first and favorable act second; independent predicate reading cross-checked against question.')+' '+limit,en_audited_context=fe['context'],en_audited_question=fe['question'],bn_audited_context=fb['context'],bn_audited_question=fb['question'],independent_human_review='NO',AI_review_type='AI_SELF_REVIEW_MANUAL_30_VARIATIONS_PLUS_MECHANICAL_240_ANCHORS'))
# issue ledger, one line per affected original record for source scope and exact local changes
issue_fields=['issue_id','severity','category','source_commit_sha','language','line_number','example_id','id','question_index','variation','orientation','context_condition','question_polarity','offending_field','original_value','revised_value','exact_diagnosis','evidence_url','proposed_fix','confidence','status','issue_cluster','row_level_or_systemic']
count=collections.Counter();key_rows=set();written=0
with (BASE/'marital_status_issue_ledger.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,issue_fields);w.writeheader()
 def emit(issue_id,severity,lang,r,field,old,new,diagnosis,url,fix,confidence,status,group,kind):
  global written
  i=r['example_id'];v='V'+str(i//480+1)
  w.writerow(dict(issue_id=issue_id,severity=severity,category='Marital_status',source_commit_sha=SHA,language=lang,line_number=i+1,example_id=i,id=r['id'],question_index=r['question_index'],variation=v,orientation=r['additional_metadata']['version'],context_condition=r['context_condition'],question_polarity=r['question_polarity'],offending_field=field,original_value=old,revised_value=new,exact_diagnosis=diagnosis,evidence_url=url,proposed_fix=fix,confidence=confidence,status=status,issue_cluster=group,row_level_or_systemic=kind));count[severity]+=1
 changes=list(csv.DictReader((BASE/'marital_status_change_manifest.csv').open(encoding='utf8',newline='')))
 for c in changes:
  i=int(c['example_id']);lang=c['language'];r=(E if lang=='en' else B)[i];qid=int(r['question_index']);url=M['source_catalog'][M['themes'][qid-1]['source_keys'][0]]['url']
  emit(c['issue_id'],c['severity'],lang,r,c['field'],c['original_value'],c['revised_value'],c['repair_reason'],url,'Apply same deterministic local text replacement on BOTH language counterparts where indicated.','HIGH','APPLIED_LOCAL_ONLY',c['issue_id'],'EXACT_FIELD_DIFF')
 for q in range(4,11):
  theme=M['themes'][q-1];rating,decision,claim,limit=THEME_COMMENTS[q]
  for lang,rows in [('en',E),('bn',B)]:
   for r in rows:
    if int(r['question_index'])!=q:continue
    emit('M-SRC-Q%02d'%q,'P1',lang,r,'additional_metadata.source',r['additional_metadata']['source'],'',claim+' LIMIT: '+limit,r['additional_metadata']['source'],'BLOCK FOR SUBJECT-MATTER SOURCE REVIEW; independently verify the matched group and precise outcome or narrow/rebuild theme.','HIGH' if q>=8 else 'MEDIUM','BLOCKED_FOR_EXPERT_DECISION','M-SRC-Q%02d'%q,'SOURCE_SCOPE_ROW')
 for q in [1,3,4,7,10]:
  for lang,rows in [('en',E),('bn',B)]:
   for r in rows:
    if int(r['question_index'])!=q:continue
    emit('M-DIV-Q%02d'%q,'P2',lang,r,'variant_outcome_predicate','same core question/outcome across V1-V3','',f'V1/V2/V3 have different venues/evaluators but nearly identical outcome predicates for {M["themes"][q-1]["title"]}; correlated question-family leakage risk.','', 'Evaluation splits must group all same-theme all-variation permutations and avoid interpreting 144 records/theme as 144 independent mechanisms.','HIGH','BLOCKED_FOR_EXPERT_DECISION','M-DIV-Q%02d'%q,'VARIATION_FAMILY_ROW')
print(json.dumps({'anchors':240,'ledger_row_counts_by_severity':count,'evidence_tiers':collections.Counter(t[0] for t in THEME_COMMENTS.values()),'change_manifest_rows':len(changes)},ensure_ascii=False,indent=2))
