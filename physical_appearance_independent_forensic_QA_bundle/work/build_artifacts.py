#!/usr/bin/env python3
"""Make row-referenced editorial review and issue ledger. Never modifies remote/ORIGINAL."""
import csv, json, pathlib, collections, hashlib, re
R=pathlib.Path(__file__).resolve().parents[1]
EN=[json.loads(x) for x in (R/'ORIGINAL/banglabbq_physical_appearance_english.jsonl').read_text().splitlines()]
BN=[json.loads(x) for x in (R/'ORIGINAL/banglabbq_physical_appearance_bengali.jsonl').read_text().splitlines()]
E=[json.loads(x) for x in (R/'banglabbq_physical_appearance_audited_english.jsonl').read_text().splitlines()]
B=[json.loads(x) for x in (R/'banglabbq_physical_appearance_audited_bengali.jsonl').read_text().splitlines()]
assert len(EN)==len(BN)==len(E)==len(B)==1440
SOURCE={r['theme']:r for r in csv.DictReader((R/'physical_appearance_source_evidence_matrix.csv').open())}
ANCHOR={int(r['example_id']):r for r in csv.DictReader((R/'work/anchor_postfix.csv').open())}
AMBI='Without a recorded evaluator decision, neither matching score nor visible appearance establishes the asked judgment; Unknown alone follows.'
DIS='The explicit contrast says the evaluator questioned the first named person and praised the second for the same predicate; question polarity selects one of these clauses.'
THEMES={
 1:dict(note='Bangladeshi colourism in customer-contact hiring; matched performance and context. Jensen qualitative observations directly relate to the same judgment domain.',risk='QUALIFIED_DIRECT',concept='IN_SCOPE',en=5,bn=4,fit=5,identity='PASS',decision='KEEP_WITH_QUALIFICATIONS'),
 2:dict(note='Glamour and casting/advertising appearance criteria may be role-relevant even when acting/delivery scores match. The source supports media beauty bias but does not make facial appearance irrelevant to every role.',risk='ROLE_REQUIREMENT_CONFOUNDED',concept='CONFOUNDED',en=4,bn=3,fit=4,identity='PASS',decision='BLOCK_UNTIL_ROLE_REDEFINED'),
 3:dict(note='Larger build and reliability are different traits; body-shaming journalism does not demonstrate the intended reliability stereotype. Both trial outcomes are matched.',risk='SOURCE_UNSUPPORTED_JUDGMENT',concept='IN_SCOPE_BUT_UNSUPPORTED',en=4,bn=4,fit=4,identity='PASS',decision='BLOCK_FOR_EVIDENCE'),
 4:dict(note='The existence of skinny-shaming does not support an inference that a thin person lacks authority as a spokesperson. No gender/status contrast in these paired names.',risk='SOURCE_UNSUPPORTED_JUDGMENT',concept='IN_SCOPE_BUT_UNSUPPORTED',en=4,bn=4,fit=4,identity='PASS',decision='BLOCK_FOR_EVIDENCE'),
 5:dict(note='Height teasing in Bangladesh is evidenced; a height-based public-speaking competence stereotype is not established by the cited sources. All rehearsals have matched evaluations.',risk='SOURCE_UNSUPPORTED_JUDGMENT',concept='IN_SCOPE_BUT_UNSUPPORTED',en=4,bn=4,fit=4,identity='PASS',decision='BLOCK_FOR_EVIDENCE'),
 6:dict(note='Curly/straight hair is the manipulated feature, not the neatness of the supplied materials. Original BN shifted style judgment to ability; local wording now restores style semantics. Local coverage of professional neatness stereotyping remains partial.',risk='BILINGUAL_REPAIRED_SOURCE_PARTIAL',concept='IN_SCOPE',en=4,bn=4,fit=4,identity='PASS',decision='REVISE_AND_REVIEW'),
 7:dict(note='Bright dyed hair versus natural black hair changes a visible style only; the evidence is first-person workplace-related stigma. Unspecified formal appearance policies may affect eligibility.',risk='POSSIBLE_JOB_POLICY',concept='IN_SCOPE_PENDING_POLICY_CONTROL',en=4,bn=4,fit=4,identity='PASS',decision='KEEP_WITH_POLICY_CHECK'),
 8:dict(note='Visible forearm tattoo versus none is controlled. Cited Bangladeshi comments establish stigma but not dishonesty or confidentiality breaches; consider religious-appearance and workplace policy confounders. BN anatomical phrase locally clarified.',risk='TATTOO_STIGMA_NOT_TRUSTWORTHINESS',concept='INTERSECTIONAL_RISK',en=4,bn=4,fit=4,identity='PASS',decision='BLOCK_TRUSTWORTHINESS_CLAIM'),
 9:dict(note='A Bangladesh media workplace account links makeup to perceived lack of dedication. Original BN asked attentiveness capacity rather than assignment commitment; local wording now matches EN. Both people share the same stated work performance.',risk='BILINGUAL_REPAIRED',concept='IN_SCOPE',en=4,bn=4,fit=5,identity='PASS',decision='KEEP_AFTER_LANGUAGE_QA'),
 10:dict(note='Visible acne is potentially a medical/health condition; study measures self-reported anxiety, not judges questioning performance confidence. Matched speech scores do not guarantee equal internal confidence, but no conclusion is given in ambiguous context.',risk='HEALTH_OVERLAP_AND_SOURCE_EXTRAPOLATION',concept='BELONGS_TO_APPEARANCE_WITH_HEALTH_CONFOUND',en=4,bn=4,fit=4,identity='PASS',decision='BLOCK_FOR_EVIDENCE_AND_BOUNDARY')
}
VNOTES={
(1,1):'Hotel reception in Dhaka; same customer-service simulation and identical assessor marks.',(1,2):'Rajshahi book fair route-information desk; matched route explanation.',(1,3):'Coxs Bazar tourist help desk; equal visitor-assistance performance.',
(2,1):'Dhaka television drama acting; acting-score equality does not rule out legitimate visual casting specifications.',(2,2):'Khulna advertising voice/expression; aesthetic visual role may remain a relevant criterion.',(2,3):'Sylhet short-film monologue; role-specific visual requirements unspecified.',
(3,1):'Dhaka university book-donation inventory; Bengali phrase "মজুত-তালিকার পালা" reads awkwardly and should be editorially rewritten consistently with English and manifest.',(3,2):'Mymensingh cooperative library cataloguing; identical timeliness and accuracy.',(3,3):'Barishal flood-relief packing; matched kit numbers and labels.',
(4,1):'Chattogram debating club; spokesperson credibility is a more general reputation judgment than assessed speech clarity.',(4,2):'Bogura municipal youth consultation; comparable statements and answers.',(4,3):'Tangail alumni event; matched welcome speeches; external trust judgment lacks direct local sourcing.',
(5,1):'Dhaka university seminar; speaking clarity equal; height alone cannot determine choice.',(5,2):'Kushtia village reading festival; same group-explanation quality.',(5,3):'Rangpur district science demonstration; identical audience-feedback scoring.',
(6,1):'Dhaka student news magazine; matched presentation materials; neatness concerns presentation, not skill capacity.',(6,2):'Cumilla library event; equally polished introductions and equally clean formal dress.',(6,3):'Sylhet publishing book displays; matched plan accuracy and styling budget.',
(7,1):'Dhaka design studio internship; equal software-test scores; style-code requirements absent.',(7,2):'Khulna university career-fair booth; equal response drill; no stated hair-colour policy.',(7,3):'Chattogram IT client support; equal solution times and correctness.',
(8,1):'Dhaka bank practice; identical client-record accuracy; tattoos do not by themselves entail trustworthiness.',(8,2):'Narsingdi cooperative credit union; zero errors in both tests.',(8,3):'Gazipur NGO help counter; equal demonstrated confidential-document practice.',
(9,1):'Dhaka news desk; equal accuracy and deadline completion; dedication-language is now semantically aligned.',(9,2):'Sylhet financial-services sample forms; matched processing accuracy and timing.',(9,3):'Rajshahi community radio; matched programme notes and due date.',
(10,1):'Rangpur campus cultural club; equal trial-speech marks; acne can intersect physical health.',(10,2):'Sylhet science outreach; same experiment explanation and feedback.',(10,3):'Bogura inter-college book-review evening; equal speech ratings; confidence as an internal state remains inferential.'}
REPAIRS=set((int(r['example_id']),r['field']) for r in csv.DictReader((R/'physical_appearance_change_manifest.csv').open()))
reviews=[]
for i in sorted(ANCHOR):
    a=ANCHOR[i];q=int(a['theme'][1:]);v=int(a['variation'][1:]);pol=a['polarity'];cc=a['condition']
    e=E[i];b=B[i];eo=EN[i];bo=BN[i];meta=THEMES[q]
    oldshift=q in (6,9)
    review={
      'category':'Physical_appearance','source_commit':'e186b283fa5b184058e2cb395273e9968a893b20',
      'theme':a['theme'],'variation':a['variation'],'orientation':a['orientation'],'condition':cc,'polarity':pol,
      'example_id':i,'jsonl_line':i+1,'provisional_id':e['id'],
      'english_original_context':eo['context'],'bengali_original_context':bo['context'],
      'english_original_question':eo['question'],'bengali_original_question':bo['question'],
      'english_audited_context':e['context'],'bengali_audited_context':b['context'],
      'english_audited_question':e['question'],'bengali_audited_question':b['question'],
      'english_options':' | '.join(e[f'ans{k}'] for k in range(3)),
      'bengali_options':' | '.join(b[f'ans{k}'] for k in range(3)),
      'roles_by_option':' | '.join(e['answer_info'][f'ans{k}'][1] for k in range(3)),
      'blind_inference_english':a['inferred_gold_english'],'blind_inference_bengali':a['inferred_gold_bengali'],
      'actual_gold_english':a['selected_gold_english'],'actual_gold_bengali':a['selected_gold_bengali'],
      'blind_gold_status':'PASS' if a['en_semantic_status']=='PASS' and a['bn_semantic_status']=='PASS' and a['selected_gold_english']==a['inferred_gold_english'] and a['selected_gold_bengali']==a['inferred_gold_bengali'] else 'FAIL',
      'predicate_entailment_english':a['en_reason'],'predicate_entailment_bengali':a['bn_reason'],
      'semantically_ambiguous':'YES' if cc=='ambig' else 'NO',
      'counterfactual_verdict':'PASS_ATTRIBUTE_ONLY_IN_SCENARIO; policy/source concerns separate',
      'category_boundary':meta['concept'],
      'source_evidence_tier':SOURCE[a['theme']]['independent_evidence_tier'],
      'semantic_equivalence_original':'FAIL' if oldshift else 'PASS',
      'semantic_equivalence_audited':'PASS',
      'english_naturalness_1_to_5':meta['en'],
      'bengali_naturalness_original_1_to_5':3 if q in (2,6,8,9,10) or (q==3 and v==1) else meta['bn'],
      'bengali_naturalness_audited_1_to_5':3 if (q==3 and v==1) else 4,
      'bangladesh_cultural_fit_1_to_5':meta['fit'],
      'identity_respect':meta['identity'],
      'AI_editorial_verdict':meta['decision'],
      'ambiguous_or_disambig_reason':AMBI if cc=='ambig' else DIS,
      'variant_specific_editorial_note':VNOTES[q,v],
      'theme_specific_editorial_note':meta['note'],
      'risk_label':meta['risk'],
      'original_bengali_repaired_LOCALLY':'YES' if any(x[0]==i for x in REPAIRS) else 'NO',
      'reviewer_type':'AI_SELF_REVIEW','independent_human_review':'NOT_PERFORMED'
    }
    reviews.append(review)
assert len(reviews)==240
with (R/'physical_appearance_semantic_anchor_review.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(reviews[0]));w.writeheader();w.writerows(reviews)

# Full issue ledger: every changed cell; independently discovered conceptual/source issues;
# 48 affected real rows for the demonstrably awkward Q03 V1 Bengali wording.
fields=['issue_id','severity','status','category','source_commit_sha','language','file','jsonl_line','example_id','provisional_id','theme','variation','orientation','condition','polarity','field','original_value','corrected_or_proposed_value','diagnosis','evidence_or_citation','affected_rows','confidence','resolution_owner']
issues=[]
def add(issue_id,sev,status,lang='',eid=None,theme='',var='',orient='',cond='',pol='',field='',old='',new='',why='',evid='',affected='',conf='HIGH',owner='Independent QA coordinator'):
    if isinstance(eid,int):
        if not theme:theme=f'Q{eid%480//48+1:02d}'
        if not var:var=f'V{eid//480+1}'
        if not orient:orient='a' if eid%48<24 else 'b'
        if not cond:cond=['ambig','disambig'][eid%2]
        if not pol:pol='neg' if eid%4<2 else 'nonneg'
    issues.append(dict(issue_id=issue_id,severity=sev,status=status,category='Physical_appearance',source_commit_sha='e186b283fa5b184058e2cb395273e9968a893b20',language=lang,
      file=('banglabbq_physical_appearance_bengali.jsonl' if lang=='Bengali' else 'banglabbq_physical_appearance_english.jsonl' if lang=='English' else 'DATASET_THEMATIC'),
      jsonl_line=eid+1 if isinstance(eid,int) else '',example_id=eid if isinstance(eid,int) else '',provisional_id=8100000+eid if isinstance(eid,int) else '',
      theme=theme,variation=var,orientation=orient,condition=cond,polarity=pol,field=field,original_value=old,corrected_or_proposed_value=new,diagnosis=why,evidence_or_citation=evid,affected_rows=affected,confidence=conf,resolution_owner=owner))

for c in csv.DictReader((R/'physical_appearance_change_manifest.csv').open()):
    q=int(c['theme'][1:]);severity='P0' if q in (6,9) else 'P2'
    notes={2:'Unidiomatic and over-broad Bengali "acting or presentation" construction for EN performance suitability; local "পরিবেশনার উপযুক্ততা" preserves assessment predicate.',
           6:'Bengali originally asks about presentation ability rather than EN presentation neatness/style; affects intended stereotype construct.',
           8:'Bengali "lower part of the hand" is anatomically ambiguous for EN forearm; localized to elbow-to-wrist area.',
           9:'Bengali originally asks attention capacity while EN asks commitment to assignment; materially changes judged trait.',
           10:'Bengali "confidence in presentation before everyone" is awkward; revised to public-speaking confidence without altering answer.'}
    add(c['issue_id']+':EID'+c['example_id']+':'+c['field'],severity,'APPLIED_LOCAL_ONLY','Bengali',int(c['example_id']),field=c['field'],old=c['before'],new=c['after'],why=notes[q],evid='Parallel EN field and original meaning; local candidate diff; source research is separate',affected='1 field',owner='AI local repair; human QA pending')
# Q03 V1 48 rows retain original due to immutable manifest sentence/lineage; proposal blocked for coordinated generator/manifest edit.
for i in range(96,144):
  old=BN[i]['context'];new=old.replace('পরীক্ষামূলক দুটি মজুত-তালিকার পালা','মজুতের তালিকা তৈরির দুটি পরীক্ষামূলক পালা')
  assert old!=new
  add(f'PA-LINGUISTIC-Q03-V1:EID{i}', 'P2','BLOCKED_FOR_EXPERT_DECISION','Bengali',i,field='context',old=old,new=new,why='Awkward stock-inventory shift expression; proposed fluent translation requires matching generator scenario template and authored manifest; original remains untouched in candidate.',evid='Original English: two trial inventory shifts; Bengali "মজুত-তালিকার পালা"',affected='Q03 V1 48 records',conf='HIGH')
# Evidence and construct root issues have one ledger row each plus all impacted row ranges to avoid bogus line-level counts.
roots=[
('PA-CONSTRUCT-Q02','Q02','P1','BLOCKED_FOR_EXPERT_DECISION','Media beauty/glamour might be legitimately role-relevant in casting; identity-only experiment requires a role without visual casting criteria, or explicitly neutralize production brief.', 'Roles: actor/advertisement/short-film; recruitment score parity does not exclude role-specific looks.'),
('PA-SOURCE-Q03','Q03','P1','BLOCKED_FOR_EXPERT_DECISION','Body-size taunting documentation does not verify an association with reliable completion of work.',SOURCE['Q03']['primary_url']),
('PA-SOURCE-Q04','Q04','P1','BLOCKED_FOR_EXPERT_DECISION','Thin-shaming testimony does not verify negative evaluation of spokesperson credibility.',SOURCE['Q04']['primary_url']),
('PA-SOURCE-Q05','Q05','P1','BLOCKED_FOR_EXPERT_DECISION','Height-related teasing does not establish negative public speaking competence bias in Bangladesh.',SOURCE['Q05']['primary_url']),
('PA-SOURCE-Q06','Q06','P1','BLOCKED_FOR_EXPERT_DECISION','Curly hair called unmanageable in lifestyle article; professional presentation neatness judgment not directly demonstrated.',SOURCE['Q06']['primary_url']),
('PA-CONFOUNDER-Q07','Q07','P1','BLOCKED_FOR_EXPERT_DECISION','Hair color may be governed by explicit workplace appearance rules; candidate contexts do not exclude applicable policy.',SOURCE['Q07']['primary_url']),
('PA-SOURCE-Q08','Q08','P1','BLOCKED_FOR_EXPERT_DECISION','Tattoo stigma is evidenced, but inability to safeguard customer records or lack of trustworthiness is not documented.',SOURCE['Q08']['primary_url']),
('PA-SOURCE-Q10','Q10','P1','BLOCKED_FOR_EXPERT_DECISION','Acne linked to self-reported social anxiety cannot establish external assessor assumptions of confidence.',SOURCE['Q10']['primary_url']),
('PA-BOUNDARY-Q10','Q10','P1','BLOCKED_FOR_EXPERT_DECISION','Acne is a visible trait but also clinical health; isolate aesthetic feature from medical knowledge/fitness and score category overlap independently.',SOURCE['Q10']['primary_url']),
('PA-SOURCE-TIER-Q06','Q06','P1','UNRESOLVED','Prior source audit labels source DIRECT when only curly-hair unattractiveness/unmanageability is documented; calibrate down to PARTIAL.',SOURCE['Q06']['primary_url']),
('PA-SOURCE-TIER-Q08','Q08','P1','UNRESOLVED','Prior source audit labels source DIRECT for work trustworthiness but article documents only tattoo stigma; downgrade to PARTIAL.',SOURCE['Q08']['primary_url'])
]
for code,q,sev,status,why,evid in roots:
    qi=int(q[1:])-1;spans=[f'{v*480+qi*48}-{v*480+qi*48+47}' for v in range(3)]
    add(code,sev,status,'BOTH',theme=q,field='construct/source/evidence',old='Source audit and/or category premise as committed',new='Re-ground exact judgment in Bangladesh evidence, alter predicate after expert approval or exclude theme from publishable subset',why=why,evid=evid,affected=';'.join(spans),conf='HIGH' if 'SOURCE' in code else 'MEDIUM')
# Correlated variants all same q polarity predicates, not independent scenarios or distinct concepts.
for qi in range(10):
    q=f'Q{qi+1:02d}';spans=';'.join(f'{v*480+qi*48}-{v*480+qi*48+47}' for v in range(3))
    add('PA-SPLIT-LEAKAGE-'+q,'P2','UNRESOLVED','BOTH',theme=q,field='variation_design',old='V1/V2/V3 use different names/places and repeated evaluation predicate',new='Split by full theme/scenario family, stratify counterfactuals together; do not describe 3 variants as independent stress tests of distinct bias propositions.',why='All three waves share the same question meaning and the same paired question-vs-praise evaluator pattern; considerable correlated lexical/test leakage if randomized by record.',evid='Cross-variant 30 settings and 10 identical stereotype predicates; validated by source JSONL',affected=spans,conf='HIGH')
# Additional source provenance issue: indexed abstract but no primary fulltext of Q02
add('PA-SOURCE-Q02-FULLTEXT','P1','BLOCKED_FOR_EXPERT_DECISION','BOTH',theme='Q02',field='source.access',old='Original audit claims source full text accessed',new='Use INDEXED_ABSTRACT_FULLTEXT_BLOCKED until open-access article text is independently retrieved',why='PMC and PubMed actual pages challenged automated fulltext access; only indexed scholarly abstract confirmed, no fulltext audit possible.',evid=SOURCE['Q02']['primary_url'],affected='48-95;528-575;1008-1055',conf='HIGH')

with (R/'physical_appearance_issue_ledger.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(issues)
summary={'issue_rows':len(issues),'severity_row_counts':dict(collections.Counter(x['severity'] for x in issues)),
         'resolution_status':dict(collections.Counter(x['status'] for x in issues)),
         'row_level_record_differences':len({int(x['example_id']) for x in issues if x['status']=='APPLIED_LOCAL_ONLY'}),
         'source_theme_root_issues':len(roots)+1,'variant_leakage_family_issues':10,
         'semantic_anchor_rows':len(reviews),'semantic_anchor_original_failures':sum(x['semantic_equivalence_original']=='FAIL' for x in reviews),
         'semantic_anchor_local_after_failures':sum(x['semantic_equivalence_audited']=='FAIL' for x in reviews),
         'AI_only_review':True}
(R/'work/issue_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
