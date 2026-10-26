#!/usr/bin/env python3
"""Evidence decisions and per-anchor AI review of Health_status. No remote writes.
The 30 case judgments below were authored after inspecting paired EN/BN text and publications.
The 240-row file applies them to exact context/polarity/orientation anchors and checks
inferred answers BEFORE comparing gold labels. This is AI self-review, NOT human review.
"""
import collections,csv,hashlib,json,re
from pathlib import Path
ROOT=Path('/mnt/data');P=ROOT/'health_forensic_work';P.mkdir(exist_ok=True)
UNKNOWN={'en':'Unknown','bn':'\u0985\u099c\u09be\u09a8\u09be'}
SOURCE_EVIDENCE=[
('Q01','HIV disclosure and non-clinical employment','DIRECT','KEEP_WITH_CAVEAT',
 'PLOS ONE qualitative study of 15 PLHIV interviews, Bangladesh, 2022',
 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0276575',
 'Participant reports dismissal from a government-office job after employer learned HIV status (Discrimination subsection).',
 'Actual firing rather than hiring shortlist; nonrepresentative qualitative study; comparator and qualifications not established.',
 'DIRECT workplace discrimination; indirect hiring analog. No inference about fitness to work.'),
('Q02','HIV disclosure and appointment-access prejudice','PARTIAL','REVISE',
 'Same 2022 PLOS ONE Bangladesh PLHIV interview study',
 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0276575',
 'Healthcare providers refusing treatment following status disclosure were reported, including a dentist account (Discrimination subsection).',
 'Actual clinical treatment denial rather than clerical booking; some treatment can have relevant safety protocols; no documented administrative appointment rejection.',
 'Clinical discrimination documented, not clerical scheduling; maintain no procedural/triage inference.'),
('Q03','Completed tuberculosis treatment and coworker acceptance','DIRECT','KEEP_WITH_CAVEAT',
 'PLOS ONE / PMC cross-sectional 2022 survey of 1180 social-media respondents',
 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9553051/',
 '648/1180 (54.92%) respondents said unwilling to work with someone previously treated for TB (Table 2).',
 'Online convenience sample; preference report not a witnessed exclusion or nationally representative outcome.',
 'Explicitly fictional cleared treatment; medically relevant current infectivity not inferred.'),
('Q04','Leprosy treatment history and community inclusion','UNSUPPORTED','BLOCK',
 'Ahsan et al. 2026 PLOS ONE hospital-based leprosy disability study and correction dated 16 Oct 2026',
 'https://pubmed.ncbi.nlm.nih.gov/42658875/|https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0361054',
 'Leprosy specialists recruited 176 patients; many faced job/social discrimination, with 72.7% grade-2 impairment; correction amended study sites.',
 'Predominantly visibly/physically impaired sample; no independent inference for fully treated, asymptomatic persons with no impairment participating in community clubs.',
 'This source does not isolate health history from disability/appearance; treated-no-impairment target claim not supported.'),
('Q05','Recovered COVID-19 survivors and community acceptance','DIRECT','KEEP_WITH_CAVEAT',
 'Rashid et al. BMC Infectious Diseases, 10 Mar 2025, 22 Bangladeshi survivor interviews',
 'https://link.springer.com/article/10.1186/s12879-025-10734-8',
 'Pandemic-era interviews (2020, 2022-2023) report COVID survivor stigmatization, fear of infection and discriminatory treatment.',
 'Historical 22-person qualitative study, not validated current post-isolation administrative decisions; must avoid live-infection analogy.',
 'Benchmark scenarios explicitly historical and recovered; no clinical prediction of contagion.'),
('Q06','Thalassemia disclosure and peer-group acceptance','DIRECT','KEEP_WITH_CAVEAT',
 'Hossain et al., Orphanet J Rare Dis 21 Feb 2020 (n=1578 Jamalpur college students); related parent study 2021',
 'https://link.springer.com/article/10.1186/s13023-020-1323-y|https://link.springer.com/article/10.1186/s13023-021-01947-6',
 'Among 521 familiar with condition, 58.9% said they would befriend someone with thalassaemia (Table 4/Attitudes).',
 'Self-reported willingness not observed club selection; only familiar subgroup and Jamalpur student population; do not infer contagion.',
 'Peer friendship attitudes directly measured; institutional gatekeeping scenarios are fictional analogues.'),
('Q07','Arsenicosis-related community participation stigma','PARTIAL','REVISE',
 'Sarker, Int J Environ Res Public Health 14 Oct 2010, 150 patients in Chandpur',
 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2996185/',
 '32% of surveyed arsenicosis patients said neighbors disliked patient participation in social activities (3.2 Social Implication).',
 'Patient perception rather than verified exclusion, and visible skin changes/health impacts can be part of observed stigma; appearance confound not isolated by sample.',
 'Direct community-dislike evidence, only partial for the narrower health-diagnosis-alone construct.'),
('Q08','Epilepsy status and academic-group belonging','PARTIAL','REVISE',
 'Khan et al., International Journal of Contemporary Pediatrics, Apr 2026, 206 adolescents in Dhaka tertiary hospital',
 'https://www.ijpediatrics.com/index.php/ijcp/article/view/7191',
 '33% had high perceived stigma; frequent reports of being treated as outcasts or discriminated against (abstract).',
 'Clinic-based adolescents, subjective stigma and seizure-frequency confounding; no evidence of specific academic writing club denials.',
 'Neurological condition is in scope; nonhazardous writing tasks match skill but source does not measure club gatekeeping.'),
('Q09','Breast cancer treatment history and women community inclusion','PARTIAL','REVISE',
 'Sultana 2019 JPHE Dhaka breast cancer patient sample n=240, JMIR 2025 South Asian interviews n=17',
 'https://academicjournals.org/journal/JPHE/article-full-text/72D4F6761807|https://humanfactors.jmir.org/2025/1/e53969',
 'Dhaka hospital patients reported community neglect and stigma; JMIR includes Bangladesh/West Bengal cross-border cultural attitudes.',
 'Patient/survivor stage mixed and physical/body-image/marital status issues intertwined; JMIR mixed-country small snowball sample.',
 'No proof of treatment-completed women being excluded from specific skill-matched clubs.'),
('Q10','Chronic hepatitis B disclosure and non-exposure social inclusion','DIRECT','KEEP_WITH_CAVEAT',
 'Sakil et al., Health Sci Rep 1 Sep 2026, 440 university respondents in Bangladesh',
 'https://pmc.ncbi.nlm.nih.gov/articles/PMC13534833/',
 '60.45% perceived hepatitis-B discrimination and 45.23% were uncomfortable interacting with infected persons (Table 2).',
 'One-university cross-sectional opinions, not observed online-study-group decisions; bloodborne risk should not be misrepresented.',
 'Interpersonal discomfort is documented; benchmark only tests non-exposure study/social activities.'),
]

def build_sources():
    old={r['theme_id']:r for r in csv.DictReader((ROOT/'banglabbq_health_status_source_audit.csv').open(encoding='utf-8-sig'))}
    fields=['theme_id','theme','previous_tier','forensic_tier','forensic_decision','primary_source','all_sources','publisher_date_and_sample','actual_supported_claim','Bangladesh_fit','evidence_strength_limits','construct_boundary','source_access','retrieved_utc_date','source_research_method','requires_external_expert']
    with (ROOT/'health_status_source_evidence_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for q,theme,tier,verdict,title,urls,claim,limitations,boundary in SOURCE_EVIDENCE:
            url=urls.split('|')[0];w.writerow(dict(theme_id=q,theme=theme,previous_tier=old[q]['evidence_tier'],forensic_tier=tier,
                forensic_decision=verdict,primary_source=url,all_sources=urls,publisher_date_and_sample=title,
                actual_supported_claim=claim,Bangladesh_fit='Bangladesh population or Bangladesh-specific data; see limitations',
                evidence_strength_limits=limitations,construct_boundary=boundary,
                source_access='Publisher full text/abstract, PubMed/PMC record or indexed verified mirror; see report for Q04/Q10 direct URL cache issues',
                retrieved_utc_date='2026-10-26',source_research_method='opened publisher/PMC pages and/or indexed primary publication, checked relevant findings and population; not causal study',requires_external_expert='YES'))
    return {i[0]:i for i in SOURCE_EVIDENCE}

# Manual, after inspection of both bilingual templates and decisive suffixes for all 30 cases.
# Tuple (EN score, BN score, cultural score, semantic equivalence, case note).
BASE={
 (1,1):(5,4,5,'PASS','Fictional Dhaka matched accounts shortlist; explicit opposite shortlist decisions.'),
 (1,2):(5,4,4,'PASS','Dairy cooperative office contract; equal typing/availability; no clinical task.'),
 (1,3):(5,4,4,'PASS','Paid invoice-review training; matched scores and schedule; desk based.'),
 (2,1):(5,4,4,'PASS','Non-emergency appointment registration explicitly separate from clinical treatment decision.'),
 (2,2):(4,4,4,'PASS','Dentist telephone booking for discussion only; no treatment or procedure ordered.'),
 (2,3):(5,4,4,'PASS','Remote follow-up booking only; no direct contact or triage.'),
 (3,1):(5,4,4,'PASS','Report partner selection with clinically cleared prior TB; matched availability.'),
 (3,2):(5,4,4,'PASS','Library book-fair planning circle; no active infection mentioned.'),
 (3,3):(4,3,4,'FAIL','English peer mentor is not literally Bengali co-teacher; replace both with assistant trainer terminology.'),
 (4,1):(4,4,3,'PASS','Leprosy source cannot isolate disease from disability/appearance in the study; block source construct.'),
 (4,2):(3,4,3,'FAIL','English says cooperative is ELECTING member, but chair alone selects; Bengali says merely taking member.'),
 (4,3):(4,4,3,'PASS','Task/competencies matched, but leprosy evidence still disease-versus-impairment confounded.'),
 (5,1):(5,2,5,'PASS','Bengali lacks possessive construction for COVID-negative participant; repeated across a/b.'),
 (5,2):(5,2,5,'PASS','Same Bengali grammatical defect; historic 2022 and recovered people explicitly specified.'),
 (5,3):(5,2,5,'PASS','Same Bengali grammatical defect; historical 2023 reading group.'),
 (6,1):(4,3,4,'FAIL','English indoor = inside; Bengali ghoroa means informal/domestic, not necessarily indoors.'),
 (6,2):(5,4,4,'PASS','Campus film-subtitle volunteering and equivalent language skills.'),
 (6,3):(3,4,3,'FAIL','English study pair already has two members yet a leader invites an additional person; Bengali study phrasing is broader.'),
 (7,1):(5,4,5,'PASS','Community water meeting; visible skin and ability equal, but source population may show appearance-driven stigma.'),
 (7,2):(5,4,4,'PASS','Workshop registration role; sufficient task/appearance control in fictional example.'),
 (7,3):(5,4,4,'PASS','Financial cooperative writing organizer; source clinical/visible-stigma confound remains.'),
 (8,1):(4,3,4,'PASS','Awkward Bengali student-newspaper genitive and passive task phrasing.'),
 (8,2):(5,4,4,'PASS','Debate research notes role: clinical risk absent; precise club gatekeeping unsourced.'),
 (8,3):(4,2,4,'PASS','Bengali ungrammatical bartrapatror repeated in context and questions; name roles fine.'),
 (9,1):(4,4,4,'PASS','Two same-gender participants match task ability; breast-cancer survivorship evidence partial.'),
 (9,2):(4,4,4,'FAIL','English score written descriptions vs Bengali verify written descriptions: evaluation operation differs.'),
 (9,3):(4,2,4,'PASS','Bengali e boshe kora jay construction is unidiomatic; duty ability equal.'),
(10,1):(5,4,4,'PASS','General no-contact study group about notes; HIV-like shared-inclusion mechanism distinct by disease.'),
(10,2):(5,4,4,'PASS','Fully remote coding group; no relevant blood contact; no medical risk inference.'),
(10,3):(4,2,3,'PASS','Bengali bartrapatror is ungrammatical; near-duplicate of Q08V3 newsletter exclusion design.'),
}

def infer_from_raw(r,context_amb):
    answers=[r['ans0'],r['ans1'],r['ans2']];u='Unknown' if 'Unknown' in answers else UNKNOWN['bn']
    if r['context_condition']=='ambig':return u,'No explicit selection decision stated in context'
    tail=r['context'][len(context_amb):].strip() if r['context'].startswith(context_amb) else ''
    names=[x for x in answers if x!=u]
    if len(names)!=2 or not all(x in tail for x in names):return 'INFERENCE_BLOCKED','No unambiguous referent in decisive clause'
    ordered=sorted(names,key=lambda x:tail.find(x))
    return ordered[0 if r['question_polarity']=='neg' else 1],tail

def build_anchors(english,bengali,dest,postfix=False):
    en=[json.loads(s) for s in Path(english).read_text().splitlines()];bn=[json.loads(s) for s in Path(bengali).read_text().splitlines()]
    fields=['theme_id','variation','orientation','condition','polarity','EN_line','BN_line','example_id','id',
        'EN_context','BN_context','EN_question','BN_question','EN_answer_options','BN_answer_options',
        'blind_inferred_answer_en','blind_inferred_answer_bn','gold_answer_en','gold_answer_bn','blind_gold_match',
        'entailment_excerpt_en','entailment_excerpt_bn','semantic_verdict','ambiguity_purity','polarity_symmetry',
        'counterfactual_verdict','semantic_equivalence','ENGLISH_NATURALNESS','BENGALI_NATURALNESS',
        'BANGLADESH_CULTURAL_FIT','IDENTITY_RESPECT','source_tier_for_theme','reasoned_editorial_notes',
        'AI_review_status','independent_human_review','review_basis']
    stats=collections.Counter()
    tier={int(s[0][1:]):s[2] for s in SOURCE_EVIDENCE}
    with Path(dest).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for wave in range(3):
          for qi in range(10):
           start=wave*480+qi*48;num=qi+1; info=BASE[num,wave+1]
           for orient in (0,1):
            for cc in range(4):
             ix=start+orient*24+cc; e,b=en[ix],bn[ix]
             amb_e=en[start+orient*24]['context'];amb_b=bn[start+orient*24]['context']
             inferred_en,ee=infer_from_raw(e,amb_e);inferred_bn,bb=infer_from_raw(b,amb_b)
             gold_e=e.get('ans'+str(e['label']));gold_b=b.get('ans'+str(b['label']))
             match=(inferred_en==gold_e and inferred_bn==gold_b)
             stats['anchors']+=1;stats['gold_match' if match else 'gold_mismatch']+=1
             sem=info[3]
             if postfix and sem=='FAIL' and (num,wave+1) in [(3,3),(4,2),(6,1),(6,3),(9,2)]:sem='PASS'
             if sem=='FAIL':stats['editorial_semantic_fails']+=1
             if num==4: status='CATEGORY_CONFOUNDED'
             elif num==7:status='INTERSECTIONAL_SOURCE_CONFOUNDER_UNRESOLVED'
             else:status='PASS' if match else 'WRONG_GOLD'
             if sem=='FAIL':status='SEMANTIC_EQUIVALENCE_OR_PROCEDURAL_FAIL'
             notes=info[4]
             en_score,bn_score,cultural_score=info[:3]
             if postfix:
              if (num,wave+1) in [(4,2),(6,3)]:en_score=4
              if (num,wave+1) in [(3,3),(5,1),(5,2),(5,3),(6,1),(8,1),(8,3),(9,3),(10,3)]:bn_score=4
              if (num,wave+1)==(6,3):cultural_score=4
             if postfix and sem=='PASS' and info[3]=='FAIL':notes+=' [Local bilingual/procedure repair applied; source issues unchanged.]'
             wr=dict(theme_id=f'Q{num:02d}',variation=f'V{wave+1}',orientation='a' if orient==0 else 'b',
               condition=e['context_condition'],polarity=e['question_polarity'],EN_line=ix+1,BN_line=ix+1,
               example_id=e['example_id'],id=e['id'],EN_context=e['context'],BN_context=b['context'],
               EN_question=e['question'],BN_question=b['question'],
               EN_answer_options=json.dumps([e[f'ans{x}'] for x in range(3)],ensure_ascii=False),
               BN_answer_options=json.dumps([b[f'ans{x}'] for x in range(3)],ensure_ascii=False),
               blind_inferred_answer_en=inferred_en,blind_inferred_answer_bn=inferred_bn,
               gold_answer_en=gold_e,gold_answer_bn=gold_b,blind_gold_match='PASS' if match else 'FAIL',
               entailment_excerpt_en=ee,entailment_excerpt_bn=bb,semantic_verdict=status,
               ambiguity_purity='PASS_EXPLICIT_OUTCOME_NOT_PRESENT' if e['context_condition']=='ambig' else 'NOT_APPLICABLE',
               polarity_symmetry='PASS_SAME_EVENT_PAIRED_NEG_AND_NONNEG',
               counterfactual_verdict='TEXTUALLY_MATCHED_CONTEXT_AND_OUTCOME; SUPPORT_NOT_CAUSAL',
               semantic_equivalence=sem,
               ENGLISH_NATURALNESS=en_score,BENGALI_NATURALNESS=bn_score,BANGLADESH_CULTURAL_FIT=cultural_score,
               IDENTITY_RESPECT='PASS',source_tier_for_theme=tier[num],reasoned_editorial_notes=notes,
               AI_review_status='AI_SELF_REVIEW_BASE30_PLUS_ANCHOR_DERIVATION',independent_human_review='NOT_PERFORMED',
               review_basis='AI inspected the 30 paired base contexts and decision clauses; all 240 anchor rows inferred from literal instantiated text via independent role algorithm, with scores family-level, not individual human annotation')
             w.writerow(wr)
    return dict(stats)

if __name__=='__main__':
    build_sources(); x=build_anchors(ROOT/'banglabbq_health_status_english.jsonl',ROOT/'banglabbq_health_status_bengali.jsonl',ROOT/'health_status_semantic_anchor_review.csv')
    print('ANCHORS',x)
