#!/usr/bin/env python3
"""Add case-specific, AI-self-review-only notes to all 30 scenario variants and 240 anchor rows.
This is NOT a human review, and does not claim independent secondary annotation.
"""
import pathlib,csv,json
P=pathlib.Path(__file__).resolve().parent;BASE=P.parent
EN=[json.loads(x) for x in (BASE/'original/banglabbq_social_status_english.jsonl').read_text(encoding='utf-8').splitlines()]
BN=[json.loads(x) for x in (BASE/'original/banglabbq_social_status_bengali.jsonl').read_text(encoding='utf-8').splitlines()]
notes={
(1,1):'Dhaka outpatient: matched consultation fee and time; negative dismissal and positive clear prescription explanation are explicitly opposed. The published survey supports doctor social-status perception, not the fictional paired incident.',
(1,2):'Chattogram vaccination advice: both ask identical side-effect questions and have comparable medical records. The counsellor cuts off one while explaining to the other; no medically justified triage should be inferred from family class.',
(1,3):'Rajshahi follow-up reports: identical clarification, appointment and payment are specified. Physician refusal versus detailed discussion aligns in Bengali; staff awareness of family background is not established.',
(2,1):'Khulna NGO appointment tokens: both are equal priority, but a worker delays one. English beyond-assigned-slot maps to Bengali নির্ধারিত সময় পেরিয়ে; source only documents access barriers, not class-only matched-token priority.',
(2,2):'Bogura diagnostic bookings: same routine test/fee/session, postponement without clinical reason versus timely appointment. The source does not demonstrate class-based delay when formal bookings are equal.',
(2,3):'Mymensingh pharmacy counselling: equal-priority tickets for medicine safety advice; Bengali ঠিক পালায় matches correct turn. Context lacks evidence that staff perceive family class and cited evidence does not establish token skipping.',
(3,1):'Dhaka fish market: enough cash and identical order neutralize ability-to-pay; stated refusal and fish shown are opposed. Roelen records observed market exclusion, but class and neighborhood markers overlap.',
(3,2):'Dhaka New Market panjabi purchase: listed price and full ready payment control affordability; sales worker assumes inability to pay versus showing requested garment. Bengali পাঞ্জাবি/shop context is culturally natural.',
(3,3):'Sylhet phone shop: verified payment cards control resources; seller dismisses serious-buyer credibility versus device demonstration. Seller knowledge of those verified cards is unspecified; avoid inferring factual intent from observed acts.',
(4,1):'Gazipur school applications: literal English identical documents was false for different children; locally changed to same types of required documents, matching Bengali একই ধরনের. Source evidence concerns territorial slum-address stigma.',
(4,2):'Cumilla school transfer: comparable marks, available seats and fee capacity control eligibility; refusal to assess documents is contrasted with normal rule-based review. No direct independent family-income-only transfer evidence.',
(4,3):'Dhaka science-club registration: equal exam scores and club fee, rejection before review vs acceptance. This is an extracurricular eligibility test, not school admission; source link to school entry is weaker than V1/V2.',
(5,1):'Dhaka analyst recruitment: degrees, experience and interview scores matched; professionalism questioned vs endorsed by same recruiter. Real recruiter access to household class marker and evidence of class-only hiring are unestablished.',
(5,2):'Chattogram graphic-design hiring: matched skill scores/portfolios/salary/schedule; panel declares unsupported unsuitability versus suitability. Meaning aligns but reuses same hiring-validity mechanism as V1.',
(5,3):'Rajshahi research-assistant recruitment: qualifications, written test, working hours equal; interviewer labels one application less credible. V3 is still hiring credibility with minor surface shift; correlated test-family risk.',
(6,1):'Dhaka passport enquiry: equal fees, appointments and rules; attendant ignores one and respectfully answers other. Class background is given to narrator, not demonstrably known to desk worker; citation concerns place stigma.',
(6,2):'Jamalpur birth-record correction: equivalent spelling errors and complete documents; application set aside before checking versus accepted for checking. Could be public-service bias, but source does not support individual class-only treatment.',
(6,3):'Rangpur holding-tax counter: equal prescribed paperwork and payment; officer belittles one enquiry versus politely explains process. Holding-tax tasks and social class may covary, though specific documents are controlled.',
(7,1):'Kurigram flood package: same independently verified loss and no income-based priority; shame versus respectful handling clearly contrasted. Real sources show aid stigma, not matched claimant humiliation causally from class.',
(7,2):'Khulna market-fire relief: equal essential-supply losses and written criteria; clerk calls one undeserving without examining evidence and confirms the other. Source support is partial and not a paired administrative allegation.',
(7,3):'Barishal cyclone certificates: original POS thanked recipient for paperwork, not a positive judgment on eligibility; locally revised both languages to explicit verified eligibility acknowledgement versus unfounded dishonesty allegation. Source still indirect.',
(8,1):'Satkhira Union Parishad budget meeting: equal speaking rights and equal-strength path proposal; chair silences one versus invites full explanation. J-PAL documents skewed participation, not this matched moderator behavior.',
(8,2):'Dhaka ward drainage forum: equal survey evidence and same time allotment; moderator interrupts before evidence vs lets presentation finish. Distinct topic but repeats proposal-dismissal construct and socio-political power confound.',
(8,3):'Bogura village water planning: equal resident status and cost assumptions; suggestion dismissed unread versus fully reviewed. Third venue reuses the same hearing/ignoring action; source province and class mechanism require validation.',
(9,1):'Narayanganj cultural planning: equal volunteer tasks and event contribution; organiser excludes one and invites other. Private invitation is discretionary, and cited poverty-stigma study does not establish matched committee exclusion.',
(9,2):'Rajshahi book fair appreciation meal: equal shifts and attendance; organizer omits one from invitation. This is social inclusion but individual entitlement is not guaranteed; indirect source supports stigma only.',
(9,3):'Dhaka rooftop-garden workshop: same building, paid dues, timely registration; unexplained seat denial vs offered seat. Capacity/venue rules are not evidenced and Roelen findings cannot prove this exact host act.',
(10,1):'Chattogram community library: volunteer hours and cataloguing duties equal; supervisor ignores records and labels one lazy. Original Bengali hour/task construction was unnatural; local rewrite preserves equal number of cataloguing tasks.',
(10,2):'Cumilla sports training: identical sessions/drills and matching performance sheets; coach accuses one of low effort while commending other. Subjective effort is not perfectly measured by outcomes; stereotype mechanism documented broadly.',
(10,3):'Khulna canal cleaning: matched shifts, litter amount and logs; organizer accuses shirking versus praises work ethic. Same effort/laziness idea as other Q10 variations; avoid train/test leakage.',
}
assert len(notes)==30
byq={}
with open(P/'social_status_source_evidence_matrix.csv',encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f):byq[int(r['theme'][1:])]=r
out=[]
for v in range(1,4):
 for q in range(1,11):
  i=(v-1)*480+(q-1)*48;e=EN[i];b=BN[i];edis=EN[i+1];bdis=BN[i+1]
  out.append({'theme':f'Q{q:02d}','variation':f'V{v}','first_eid':i,'last_eid':i+47,'first_provisional_id':e['id'],'english_ambig_context':e['context'],'bengali_ambig_context':b['context'],'english_disambig_predicate':edis['context'][len(e['context']):].strip(),'bengali_disambig_predicate':bdis['context'][len(b['context']):].strip(),'negative_question_en':e['question'],'positive_question_en':EN[i+2]['question'],'negative_question_bn':b['question'],'positive_question_bn':BN[i+2]['question'],'semantic_gold_entailment':'PASS_NAME_ROLE_BASED','polarity_symmetry':'FAIL_ORIGINAL' if (q,v)==(7,3) else 'PASS_BASIC','counterfactual_reversibility':'PASS_TEXTUAL_CLASS_SWAP','bilingual_equivalence':'PASS_AI_SELF_REVIEW_BASIC','evidence_tier':byq[q]['audited_tier'],'source_construct_verdict':byq[q]['judgment'],'scenario_specific_AI_editorial_note':notes[(q,v)],'reviewer_status':'AI_SELF_REVIEW_2026-10-26','independent_human_review':'NO'})
with open(P/'social_status_30_scenario_editorial_reviews.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for fname in ('social_status_semantic_anchor_review.csv','social_status_postfix_semantic_anchor_review.csv'):
 path=P/fname
 with open(path,'r',encoding='utf-8-sig',newline='') as f:rs=list(csv.DictReader(f))
 for row in rs:
  q=int(row['theme'][1:]);v=int(row['variation'][1:]);row['specific_30_variation_AI_editorial_note']=notes[(q,v)]
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
print({'scenarios':len(out),'pre_anchors_enriched':240,'post_anchors_enriched':240})
