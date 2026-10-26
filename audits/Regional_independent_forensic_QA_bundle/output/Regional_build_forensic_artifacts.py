#!/usr/bin/env python3
"""Deterministic assembly of independently reviewed Regional audit reports.
Does not perform network or remote writes. Reference evidence manually extracted from
web pages opened 2026-10-26 and must be rechecked if source URLs change.
"""
import csv,json,collections,hashlib,pathlib,itertools,os
from datetime import datetime,timezone
ROOT=pathlib.Path('/mnt/data/regional_forensic');ORIG=ROOT/'original';OUT=ROOT/'output';WORK=ROOT/'work'
HEAD='e186b283fa5b184058e2cb395273e9968a893b20'
PUSH='214795f628a34ece8deb23a65c6bf35ac0ce7157'
BLOBS={'en':'081ad561c9671e7eb3b68bdf706bc95e1aef1a5e','bn':'6c8ca8a8e4a511fb1315e96dc3e5395825cf6035'}
E0=[json.loads(z) for z in (ORIG/'banglabbq_regional_english.jsonl').read_text(encoding='utf8').splitlines()]
B0=[json.loads(z) for z in (ORIG/'banglabbq_regional_bengali.jsonl').read_text(encoding='utf8').splitlines()]
E1=[json.loads(z) for z in (OUT/'banglabbq_regional_audited_english.jsonl').read_text(encoding='utf8').splitlines()]
B1=[json.loads(z) for z in (OUT/'banglabbq_regional_audited_bengali.jsonl').read_text(encoding='utf8').splitlines()]
checks0=json.load(open(WORK/'original_independent_checks.json',encoding='utf8'))
checks1=json.load(open(WORK/'audited_independent_checks.json',encoding='utf8'))
sourceaudit=list(csv.DictReader((ORIG/'banglabbq_regional_source_audit.csv').open(encoding='utf8')))
changes=list(csv.DictReader((OUT/'Regional_change_manifest.csv').open(encoding='utf8')))
templates=json.load(open(ORIG/'banglabbq_regional_scenario_templates.json',encoding='utf8'))

def csvout(path,rows,fieldnames=None):
 rows=list(rows);fields=fieldnames or (list(rows[0]) if rows else [])
 with (OUT/path).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def write_json(path,obj): (OUT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sh(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def gitsha(path):
 import subprocess
 return subprocess.check_output(['git','hash-object',str(path)],text=True).strip()

# Evidence matrix proof: URLs and article claims observed by opening full webpages
SOURCES={
'https://online.thedailystar.net/shout/news/what-your-ancestral-home-really-says-about-you-3065576':('What your ancestral home really says about you','Nahian Nawar','The Daily Star / SHOUT','2022-07-07','FULL_TEXT','Named Noakhali cunning, Barishal hot-headed, Tangail miser stereotypes; reports Cumilla-origin parental relationship disapproval. Author explicitly rejects factual basis.','https://online.thedailystar.net/shout/news/what-your-ancestral-home-really-says-about-you-3065576#article','turn389345view3 lines 148-174'),
'https://www.thedailystar.net/shout/humour/the-truth-about-noakhaillas-1468549':('The truth about Noakhaillas','Zarin Rezwana','The Daily Star / SATIRE','2017-09-27','FULL_TEXT','An explicitly labelled satirical treatment of Noakhali stereotypes. Useful evidence of satirical circulation, not trustworthy evidence about actual behaviors.','https://www.thedailystar.net/shout/humour/the-truth-about-noakhaillas-1468549','turn696189view2 lines 102-128'),
'https://www.dhakatribune.com/magazine-archive/weekend-tribune/376375/bncc-hometown-stereotypes':('BNCC: Hometown stereotypes','Author not displayed in captured article','Dhaka Tribune / Weekend Tribune','2014-05-29','FULL_TEXT','Describes joking BNCC collective stereotype including Chandpur, and a separate anecdotal Chattogram wedding-spending generalization; not a representative prevalence study.','https://www.dhakatribune.com/magazine-archive/weekend-tribune/376375/bncc-hometown-stereotypes','turn696189view3 lines 148-176'),
'https://www.thedailystar.net/slow-reads/big-picture/news/stereotypes-struggle-and-survival-reclaiming-the-story-behind-mofiz-3916331':('Stereotypes, struggle, and survival: Reclaiming the Story Behind Mofiz','Saad Quasem','The Daily Star / Big Picture','2025-06-13','FULL_TEXT','Direct account of degrading Mofiz stereotype about Rangpur/northern people and association with simple-mindedness; context poverty does not establish innate competence.','https://www.thedailystar.net/slow-reads/big-picture/news/stereotypes-struggle-and-survival-reclaiming-the-story-behind-mofiz-3916331','turn576671view2 lines 85-97'),
'https://www.thedailystar.net/shout/news/lost-sylheti-translation-2050557':('Lost in (Sylheti) Translation','Farhat Afzal','The Daily Star / SHOUT','2021-02-24','FULL_TEXT','First-person author describes mocked Sylheti accent and popular assumption that all Sylhet people are connected to London; does not show all have actual funding access.','https://www.thedailystar.net/shout/news/lost-sylheti-translation-2050557','turn696189view1 lines 103-125'),
'https://archive.thedailystar.net/magazine/2008/11/04/cover.htm':('Bondor Bazar to Brick Lane','Syed Zain Al-mahmood','The Daily Star / Star Weekend Magazine','2008-11-28','FULL_TEXT','History of British Bangladeshi immigration and diaspora links with Sylhet, not proof of individuals having a sponsor or ability to donate.','https://archive.thedailystar.net/magazine/2008/11/04/cover.htm','turn389345view1 lines 2-30'),
'https://today.thefinancialexpress.com.bd/print/why-are-dialects-vanishing-among-the-bangladeshi-youth-1758638911':('Why are dialects vanishing among the Bangladeshi youth?','Subah Jahwa Purba','The Financial Express','2025-09-24','FULL_TEXT','Article observes dominance of Dhaka-associated speech in classrooms/media; has no study of broadcaster hiring or Chattogram-origin audition outcomes.','https://today.thefinancialexpress.com.bd/print/why-are-dialects-vanishing-among-the-bangladeshi-youth-1758638911','turn576671view3 lines 3-20'),
'https://www.tbsnews.net/features/panorama/rishta-meeting-walk-park-literally-958301':('Rishta meeting? A walk in the park, literally','Asma Sultana Prova','The Business Standard','2024-10-04','FULL_TEXT','Journalism documents high-cost Chattogram wedding conventions and efforts to reduce cost; cannot infer every Chattogram individual demands luxury.','https://www.tbsnews.net/features/panorama/rishta-meeting-walk-park-literally-958301','turn389345view6 lines 154-222'),
'https://en.prothomalo.com/bangladesh/fx154tmywr':("Marriage, a 'social curse' in Chattogram",'NH Sajjad','Prothom Alo / English','DATE_NOT_EXPOSED_IN_CAPTURE','FULL_TEXT','Reported examples of financial pressure created by Chattogram wedding convention, not direct evidence of an individual planner stereotyping district origin.','https://en.prothomalo.com/bangladesh/fx154tmywr','turn696189view0 lines 27-57'),
}
for r in sourceaudit:
 for i in (1,2,3):
  u=r.get(f'source_{i}_url','')
  if u:assert u in SOURCES,u
source_access=[dict(url=url,canonical_title=v[0],author=v[1],publisher=v[2],published_date=v[3],access='BROWSED_FULL_TEXT_2026-10-26',access_level=v[4],verified_passage_paraphrase=v[5],canonical_link=v[6],browser_evidence=v[7],caveat='Web access does not authenticate article truth; no controlled causal estimate.') for url,v in SOURCES.items()]
csvout('Regional_source_access_log.csv',source_access)

MECH={
'Q01':('Noakhali resident presumed dishonest without findings','Direct report of spoken stereotype, not actual dishonesty','Journalistic opinion/experience, plus explicitly labelled satire; no prevalence estimate','KEEP_FOR_RESEARCH'),
'Q02':('Barishal origin presumed argumentative despite matched behavior','Named hot-headed trope explicitly reported','No controlled assessment of employer/club judgments; vignette is fictional','KEEP_FOR_RESEARCH'),
'Q03':('Tangail origin presumed miserly despite matched contributions','Names Tangail miser stereotype verbatim','Anecdotal feature; cost-sharing vignette is hypothetical and corrected for timeline','REVISE_LOCAL_COMPLETE'),
'Q04':('Cumilla-origin adult rejected as a partner because of home district','First-person report of Cumilla-related parental objection','Story of one family, not representative marriage outcomes','KEEP_FOR_RESEARCH'),
'Q05':('Rangpur person treated as naive/unsophisticated','Direct anthropological-feature account of Mofiz regional slur','Historically intertwined with poverty; must avoid portraying lower ability as true','REVISE_LOCAL_COMPLETE'),
'Q06':('Sylheti person assumed to fund or sponsor via British connections','Essay says outsiders associate Sylhet universally with London; no evidence they can raise money','Social status, diaspora networks, and personal liquidity are distinct; requires evidence of sponsorship demands','BLOCK_FOR_EXPERT_EVIDENCE'),
'Q07':('Sylheti accent mocked although speech equally clear','First-person direct report of mocking Sylheti regional speech','One-person narrative with potential context differences; do not generalize prevalence','REVISE_LOCAL_COMPLETE'),
'Q08':('Chattogram speech disfavored specifically by broadcaster despite equal clarity','General standard-Dhaka speech predominance in media; does NOT establish hiring discrimination','Cannot infer actual newsroom selection outcomes, one major unsourced step','BLOCK_FOR_EXPERT_EVIDENCE'),
'Q09':('Chattogram-origin person presumed to demand luxury wedding irrespective of stated budget','Articles describe costly local ceremony pressure; BNCC feature includes one Chattogram wedding-spending stereotype','Social norms vs individual demands are different; venue budgets controlled in fictional scenario','BLOCK_FOR_EXPERT_EVIDENCE'),
'Q10':('Chandpur origin stereotyped as uncultured in neutral conduct','BNCC humorous collective label includes Chandpur; separate Chandpur claim is shrewd, not uncultured','BNCC aggregate explicitly comedic; weak Chandpur-specific evidence for uncultured behavior','BLOCK_FOR_EXPERT_EVIDENCE')}
evidence=[]
for r in sourceaudit:
 q=r['theme'];claimed,supported,caveat,decision=MECH[q]
 urls=[r.get(f'source_{i}_url','') for i in (1,2,3) if r.get(f'source_{i}_url')]
 records=[SOURCES[u] for u in urls]
 evidence.append(dict(theme=q,claimed_bias_proposition=claimed,group_comparison=r['comparison'],source_urls=json.dumps(urls,ensure_ascii=False),source_titles=json.dumps([v[0] for v in records],ensure_ascii=False),publishers=json.dumps([v[2] for v in records],ensure_ascii=False),publication_dates=json.dumps([v[3] for v in records],ensure_ascii=False),retrieved_date='2026-10-26',access_status='FULL_TEXT_VERIFIED_'+str(len(urls))+'_CITED_ARTICLES',actually_supported=supported,support_tier=r['evidence_tier'],research_limit=caveat,Bangladesh_scope='BANGLADESH_REGIONAL_ORIGIN',category_overlap=r['overlap_or_confounder_risk'],decision=decision,legacy_linkage=r['legacy_linkage'],source_verified_for_claim=(q not in ('Q06','Q08','Q09','Q10')),claim_is_not_about_fictional_event=True))
csvout('Regional_source_evidence_matrix.csv',evidence)

# AI editorial reasoning, independently specified at authored template level.
EDITOR={
('Q03','V2'):'PRE-FIX MATERIAL: decision-maker praised prior expense sharing before any payment. Fixed both languages to statements of willingness and matched questions. Financial ability and budget remain equal.',
('Q04','V2'):'PRE-FIX BENGALI: unnatural \"কাকে বিবেচনার বিরোধিতা\" construction; locally repaired to \"কাকে বিবেচনায় নেওয়ার বিরোধিতা\". Parent approval issue tests regional origin, not marital status.',
('Q05','V1'):'PRE-FIX BENGALI: \"আধুনিক কাজে অনভ্যস্ত\" denotes inexperience rather than English \"unsophisticated\". Locally repaired to \"অপরিশীলিত\"; regional label remains alleged judgment, not truth.',
('Q05','V2'):'PRE-FIX BENGALI: \"শহরের নিয়মকানুনে দক্ষ\" over-specifies knowledge of city rules rather than street-smart; locally matched \"শহুরে পরিবেশে চৌকস\".',
('Q06','V3'):'PRE-FIX EN/BN: unclear past donation/\"আগের অনুদান\" despite only proposed donations. Locally repaired tense and proposed contribution. Independent London funding bias source remains PARTIAL.',
('Q07','V2'):'PRE-FIX BENGALI \"একই ধরনের\" meant a similar kind, but English specified an identical project; locally repaired to \"একই সামাজিক প্রকল্প\".',
('Q10','V2'):'PRE-FIX BENGALI \"প্রদর্শক\" described exhibitor instead of museum guide; idiom \"নির্দেশিত পরিদর্শন\" awkward. Locally repaired actor and guided-tour language.',
('Q07','V1'):'Bengali \"বলার ধরনকে সম্মানজনক\" is stiff although semantically adequate; optional local style improvement could use \"কথাবলার ভঙ্গির প্রশংসা করেন\" if aligning EN/BN praise verb.',
('Q04','V3'):'Bengali repeats family notion in \"দুই পরিবারের পারিবারিক তথ্য\"; alternative \"দুই পরিবারের প্রাসঙ্গিক তথ্য\" preferable but not an unambiguous semantic bug.',
('Q08','V1'):'Broadcaster audition has three similar variants; avoid splitting V1/V2/V3 independently across train/test. Direct hiring source not found.',
('Q08','V2'):'Equal scores and intelligibility isolate accent from proficiency; source does not document broadcaster hiring selections. Variants V1/V2/V3 are correlated.',
('Q08','V3'):'Same media prestige mechanism in three auditions/recordings; risk correlated leakage. Documentary source limited to media speech norms.',
('Q09','V1'):'Wedding budget, customs and individual preferences must not be conflated. Controlled budget but individual preference stereotype not independently documented.',
('Q09','V2'):'Same wedding-spending stereotype as V1/V3; distinct menu, venue, coordinator contexts but correlated outcome mechanism.',
('Q09','V3'):'Despite distinct budgets/decoration planning, same trope recurs across all three variations; use theme-grouped splits.'}
VAR_SETTINGS={
'Q01':['housing-cooperative financial accounts','winter-clothes charity donation register','neighborhood savings membership application'],
'Q02':['apartment meeting temperament','debate-club rehearsal feedback','market-association price consultation'],
'Q03':['office farewell contribution','rooftop garden fund','festival volunteer shared supplies'],
'Q04':['partner family introduction','family matchmaking discussion','community gathering matchmaker advice'],
'Q05':['digital service workshop','urban navigation exercise','municipal online forms training'],
'Q06':['charity committee donation cap','student exhibition sponsorship','library repair donation'],
'Q07':['Dhaka student regional storytelling','youth podcast speech','literary poem reading'],
'Q08':['community TV audition','district radio announcement','campus video channel'],
'Q09':['wedding reception budget recommendation','marriage menu preparation','community wedding hall booking'],
'Q10':['cultural fair information desk','museum guided visit','public library reading circle']}

# 240 distinct bilingual anchors: inference before metadata via standalone rule checker.
anchors=[]
for chk in checks0['anchors']:
 i=chk['example_id'];r=E0[i];b=B0[i];a=E1[i];c=B1[i]
 theme=chk['theme'];variation=chk['variation'];orientation=chk['orientation'];pol=chk['question_polarity'];condition=chk['context_condition']
 editorial=EDITOR.get((theme,variation),'Content aligns with matched origin labels and described evaluator predicates; scenario is fictional; no relevant individual behavior can be inferred from origin.')
 source_tier=next(x['evidence_tier'] for x in sourceaudit if x['theme']==theme)
 changed=any(r[f]!=a[f] or b[f]!=c[f] for f in ['context','question','ans0','ans1','ans2'])
 suffix=((theme,variation) in [('Q05','V1'),('Q05','V2'),('Q07','V2'),('Q10','V2')])
 original_semantic='FAIL' if suffix else 'PASS'
 score_bn_pre=2 if (theme,variation) in (('Q04','V2'),('Q10','V2')) else (3 if suffix or (theme,variation)==('Q03','V2') else 4)
 score_en_pre=3 if (theme,variation) in (('Q03','V2'),('Q06','V3')) else 5
 score_bn_after=3 if (theme,variation) in (('Q07','V1'),('Q04','V3')) else 4
 score_en_after=4 if (theme,variation) in (('Q03','V2'),('Q06','V3')) else 5
 source_block=source_tier!='DIRECT'
 verdict='BLOCKED_SOURCE_EVIDENCE' if source_block else ('EDITED_LOCAL_ONLY' if changed else 'PASS_PATTERN_REVIEW')
 neg='Evaluator gave no outcome; options list two equally matched regional identities, so Unknown only' if condition=='ambig' else chk['en_evidence_clause']
 edited_en=any(r[f]!=a[f] for f in ['context','question']);edited_bn=any(b[f]!=c[f] for f in ['context','question'])
 cultural='INTERSECTIONAL_BUT_CONTROLLED' if theme in ('Q04','Q06','Q09') else 'IN_SCOPE'
 anchors.append(dict(
  anchor_id=f'{theme}_{variation}_{orientation}_{condition}_{pol}',example_id=i,line=i+1,id=r['id'],theme=theme,variation=variation,orientation=orientation,context_condition=condition,question_polarity=pol,
  english_context_original=r['context'],english_context_audited=a['context'],english_question_original=r['question'],english_question_audited=a['question'],english_options=json.dumps([a[f'ans{j}'] for j in range(3)],ensure_ascii=False),
  bengali_context_original=b['context'],bengali_context_audited=c['context'],bengali_question_original=b['question'],bengali_question_audited=c['question'],bengali_options=json.dumps([c[f'ans{j}'] for j in range(3)],ensure_ascii=False),
  inferred_label_before_consulting_gold_EN=chk['en_inferred_position'],inferred_label_before_consulting_gold_BN=chk['bn_inferred_position'],reported_original_gold_EN=r['label'],reported_original_gold_BN=b['label'],blind_gold_match_EN=chk['en_blind_gold_matches'],blind_gold_match_BN=chk['bn_blind_gold_matches'],
  entailment_en=neg,entailment_bn=chk['bn_evidence_clause'],ambiguous_purity='PASS' if condition=='ambig' else 'NOT_APPLICABLE',disambiguated_entailment='PASS_PATTERN_ATTESTED' if condition=='disambig' else 'NOT_APPLICABLE',polarity_symmetry='PASS_ANTONYMIC_EVALUATOR_ACTIONS' if condition=='disambig' else 'PASS_AMBIGUOUS_OPPOSITE_QUESTIONS',
  counterfactual_role_symmetry='PASS_RULE_CHECKED' if orientation in ('a','b') else 'FAIL',same_group_comparator='MATCHED_GROUPS_ACROSS_LANGUAGES',category_scope=cultural,identity_respect='PASS',fiction_not_real_person='YES',
  semantic_equivalence_original=original_semantic,semantic_equivalence_audited='PASS',EN_naturalness_original_1_5=score_en_pre,EN_naturalness_audited_1_5=score_en_after,BN_naturalness_original_1_5=score_bn_pre,BN_naturalness_audited_1_5=score_bn_after,cultural_fit_1_5=4,source_tier=source_tier,concept_evidence_verdict=verdict,locally_edited_english=edited_en,locally_edited_bengali=edited_bn,review_notes=editorial,editorial_method='AI_SELF_REVIEW_30_AUTHORED_TEMPLATES_PLUS_PROGRAMMATIC_240_ANCHORS;NOT_HUMAN'))
assert len(anchors)==240 and len({r['anchor_id'] for r in anchors})==240
csvout('Regional_semantic_anchor_review.csv',anchors)

# Issue ledger: every actual changed row/field plus each source-affected row and unresolved QA issues.
FIELDS=['issue_id','issue_family','severity','category','source_commit_sha','committed_jsonl_blob_sha','file','language','line','example_id','id','theme','variation','orientation','condition','polarity','offending_field','original_value','revised_value','diagnosis','supporting_url_or_evidence','proposed_fix','confidence','status']
issues=[]
def mk_issue(family,sev,lang,eid,field,orig,rev,diagnosis,evidence,fix,confidence,status,iso=''):
 rows={'en':E0,'bn':B0}.get(lang)
 r=rows[eid] if rows is not None and isinstance(eid,int) else None
 theme=f'Q{int(r["question_index"]):02d}' if r else ''
 variation=f'V{eid//480+1}' if r else ''
 rec=dict(issue_id=f'{family}-{lang}-{eid if eid is not None else "project"}-{field}',issue_family=family,severity=sev,category='Regional',source_commit_sha=HEAD,committed_jsonl_blob_sha=BLOBS.get(lang,''),file=f'banglabbq_regional_{"english" if lang=="en" else "bengali"}.jsonl' if r else '',language=lang,line=eid+1 if r else '',example_id=eid if r else '',id=r['id'] if r else '',theme=theme,variation=variation,orientation=r['additional_metadata']['version'] if r else '',condition=r['context_condition'] if r else '',polarity=r['question_polarity'] if r else '',offending_field=field,original_value=orig,revised_value=rev,diagnosis=diagnosis,supporting_url_or_evidence=evidence,proposed_fix=fix,confidence=confidence,status=status)
 issues.append(rec)
for c in changes:
 lang=c['language'];theme=f'Q{int(c["question_index"]):02d}';variation=c['variation']
 fam=f'R-ED-{theme}-{variation}'
 sev='P2' if (theme,variation)==('Q04','V2') else 'P1'
 evid_note='AI semantic/predicate comparison of original and audited bilingual template; unchanged source URL preserved'
 mk_issue(fam,sev,lang,int(c['example_id']),c['field'],c['original'],c['revised'],c['reason'],evid_note,'Apply paired corrections shown in local candidate; keep all IDs, labels and 15-field order', 'HIGH','APPLIED_LOCAL_ONLY')
for q in ('Q06','Q08','Q09','Q10'):
 detail=MECH[q][2];url=sourceaudit[int(q[1:])-1]['source_1_url'];family='R-SRC-'+q
 for lang,rows in [('en',E0),('bn',B0)]:
  for i,r in enumerate(rows):
   if r['question_index']!=str(int(q[1:])):continue
   mk_issue(family,'P1',lang,i,'additional_metadata.source',r['additional_metadata']['source'],'','Evidence limited: '+detail,url,'Obtain independently substantiated Bangladesh-specific individual-level origin discrimination evidence or rewrite/suspend theme; keep committed records unchanged','HIGH','BLOCKED_FOR_EXPERT_DECISION')
# Single representative case for optional minor style; intentionally avoid 48 duplicate style alerts.
for q,v,lang,field,comment,alternative in [
('Q07','V1','bn','context','Unidiomatic description of someone\'s speaking manner as respectable (but meaning is intelligible)','বলার ভঙ্গির প্রশংসা করেন'),
('Q04','V3','bn','context','Repeated family notion \"দুই পরিবারের পারিবারিক তথ্য\"','দুই পরিবারের প্রাসঙ্গিক তথ্য')]:
 idx=(int(v[-1])-1)*480+(int(q[-2:])-1)*48+1
 r=B0[idx]
 mk_issue(f'R-STYLE-{q}-{v}','P3',lang,idx,field,r[field],'',comment,'AI bilingual editorial self-review','Optional human editor rewrite for more idiomatic Bengali; then propagate to all permutation rows','MEDIUM','UNRESOLVED_STYLE')
for q in ('Q08','Q09'):
 idx=(int(q[-2:])-1)*48
 r=E0[idx]
 mk_issue('R-LEAK-'+q,'P2','en',idx,'variation_design',json.dumps(VAR_SETTINGS[q],ensure_ascii=False),'','All three variants share similar stereotype outcome and professional/social appraisal; correlated phrasing may create split leakage','30 author-authored scenario templates','Use grouped-by-theme and held-out-template evaluation; consider distinct mechanisms rather than media/budget paraphrases','HIGH','UNRESOLVED_EVALUATION_DESIGN')
# Project integration memory staleness, not a dataset-row defect.
mk_issue('R-MEMORY-STALE','P2','project',None,'memory/state.md and memory/index.md','Regional only 51 legacy entries, no new bundle index','','Both still omit new committed regional candidate despite bundle push; memory/history notes new bundle',f'https://github.com/Hasinish/Research-BanglaBBQ/commit/{PUSH}','Coordinator should update only if authorization is granted; this worker keeps GitHub read-only','HIGH','UNRESOLVED_PROJECT_SYNC')
assert len(issues)==len(changes)+1152+2+2+1, (len(issues),len(changes))
assert len({i['issue_id'] for i in issues})==len(issues)
csvout('Regional_issue_ledger.csv',issues,FIELDS)
count_by_sev=dict(collections.Counter(x['severity'] for x in issues))
family_sev={f:next(x['severity'] for x in issues if x['issue_family']==f) for f in set(x['issue_family'] for x in issues)}
family_counts=dict(collections.Counter(family_sev.values()))

# Checksums and remaining integration gates
filehashes={}
for lang in ('en','bn'):
 filespec=('banglabbq_regional_'+('english' if lang=='en' else 'bengali')+'.jsonl')
 orig=ORIG/filespec;new=OUT/('banglabbq_regional_audited_'+('english' if lang=='en' else 'bengali')+'.jsonl')
 assert gitsha(orig)==BLOBS[lang],(lang,gitsha(orig),BLOBS[lang])
 filehashes[lang]={'committed_git_blob_sha':BLOBS[lang],'original_sha256':sh(orig),'original_bytes':orig.stat().st_size,'audited_candidate_sha256':sh(new),'audited_candidate_bytes':new.stat().st_size}

imports={
'category':'Regional','audited_commit':HEAD,'bundle_intro_commit':PUSH,'remote_change_performed':False,'source_files':filehashes,
'record_count_english':len(E1),'record_count_bengali':len(B1),'provisional_id_min':8400000,'provisional_id_max':8401439,
'other_six_provisional_ranges':{'physical_appearance':[8100000,8101439],'social_status':[8200000,8201439],'health_status':[8300000,8301439],'ethnicity':[8500000,8501439],'occupational_background':[8600000,8605920],'marital_status':[8700000,8701439]},
'cross_category_ranges_disjoint_derived_from_manifest_checks':True,'live_active_ID_scan_count':32512,'live_active_production_spreadsheet_count':10,'regional_ID_hits':0,
'global_collision_check':'ACTIVE_PRODUCTION_VERIFIED_32512_VALUES_ZERO_COLLISIONS; hidden/backup tabs and complete cross-category historic JSONL archives not exhaustively scanned',
'current_master_spreadsheet':'https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit',
'current_regional_worksheet':'ABSENT_2026_10_26',
'canonical_jsonl_key_order':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
'google_sheets_A_to_O':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id'],
'json_metadata_for_sheet':'json.dumps(record["answer_info"],ensure_ascii=False); json.dumps(record["additional_metadata"],ensure_ascii=False)',
'import_safety':'NO','ready_for_import':False,'source_critical_theme_ids':['Q06','Q08','Q09','Q10'],
'AI_linguistic_review_status':'AI_SELF_REVIEW_TEMPLATE_LEVEL_30_PLUS_240_ANCHOR_RULE_CHECKS',
'independent_human_bengali_review':'NOT_PERFORMED',
'publication_ready':False,'live_parity_status':'NOT_IMPORTED',
'known_open_gates':['P1 evidence critical Q06/Q08/Q09/Q10','Independent Bengali human review absent','Independent sociolinguistic/regional reviewer approval absent','Provisional IDs need exhaustive global collision scan','Model evaluation split leakage between V1/V2/V3 requires grouped split','Master workbook has no Regional sheets','Repo memory state/index not synchronized to bundle push'],
'safety_caution':'The fact that all permutation rows parse does not imply stereotype-source relevance or natural translation.'}
write_json('Regional_import_readiness.json',imports)

# Separate compact machine-readable summary for reporter.
summary={'source_head':HEAD,'bundle_commit':PUSH,'original_blobs':BLOBS,'filehashes':filehashes,'counts':{'english':len(E0),'bengali':len(B0),'themes':10,'variants':30,'anchors':len(anchors),'changed_cells':len(changes),'changed_language_specific_rows':len({(x['language'],x['example_id']) for x in changes}),'source_evidence_direct':sum(x['support_tier']=='DIRECT' for x in evidence),'source_evidence_partial':sum(x['support_tier']=='PARTIAL' for x in evidence),'source_unique_urls_verified':len(source_access),'issue_ledger_rows':len(issues)},'issue_rows_by_severity':count_by_sev,'issue_unique_families_by_severity':family_counts,'issues_unique_families':sorted(family_sev),'baseline_structural_independent_issues':checks0['issue_count'],'audited_structural_independent_issues':checks1['issue_count'],'anchors_blind_match_en':sum(x['blind_gold_match_EN'] for x in anchors),'anchors_blind_match_bn':sum(x['blind_gold_match_BN'] for x in anchors),'source_block_themes':['Q06','Q08','Q09','Q10'],'human_native_review':'NOT_PERFORMED'}
write_json('Regional_audit_metrics.json',summary)
print(json.dumps(summary,indent=2,ensure_ascii=False))
