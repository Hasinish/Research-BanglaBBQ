from pathlib import Path
import csv,json,collections,hashlib,runpy
D=Path('/mnt/data/occupational_forensic_audit');W=D/'WORK';E=[json.loads(l) for l in (D/'ORIGINAL/banglabbq_occupational_background_english.jsonl').read_text().splitlines()];B=[json.loads(l) for l in (D/'ORIGINAL/banglabbq_occupational_background_bengali.jsonl').read_text().splitlines()]
AE=[json.loads(l) for l in (D/'occupational_background_audited_english.jsonl').read_text().splitlines()];AB=[json.loads(l) for l in (D/'occupational_background_audited_bengali.jsonl').read_text().splitlines()]
C='e186b283fa5b184058e2cb395273e9968a893b20';cat='Occupational_background'
BASE=json.loads((W/'original_independent_validation_sources.json').read_text());fixes=list(csv.DictReader((D/'occupational_background_change_manifest.csv').open()))
lookup=collections.defaultdict(list)
for f in fixes:lookup[(f['language'],int(f['example_id']))].append(f)
LED=[]
def base(lang,eid,issue_id,sev,field,diagnosis,original,proposal,status,source='',confidence='HIGH',affected='',revised=''):
 x=(E if lang=='english' else B)[eid] if isinstance(eid,int) else E[0]
 v=eid//480+1 if isinstance(eid,int) else ''
 k=f'Q{int(x["question_index"]):02d}'
 return dict(issue_id=issue_id,severity=sev,category=cat,source_commit_sha=C,language=lang,source_jsonl_line=eid+1 if isinstance(eid,int) else '',example_id=eid if isinstance(eid,int) else '',id=x['id'] if isinstance(eid,int) else '',question_index=k,variation=f'V{v}' if v else '',orientation=x['additional_metadata']['version'] if isinstance(eid,int) else '',context_condition=x['context_condition'] if isinstance(eid,int) else '',question_polarity=x['question_polarity'] if isinstance(eid,int) else '',affected_scope=affected or (str(eid) if isinstance(eid,int) else ''),offending_field=field,original_text_or_value=original,exact_diagnosis=diagnosis,citation_or_contextual_evidence=source,proposed_fix=proposal,confidence=confidence,local_revised_value=revised,status=status)
for z in BASE['errors']:
 lang=z['language'];eid=z['example_id'];tid=z['test_id']
 if not isinstance(eid,int) or tid not in {'AMBIGUOUS_PERMISSION','UNENTAILED_REGISTER','UNENTAILED_INPUT','UNENTAILED_FEEDBACK'}:continue
 fs=lookup[(lang,eid)]
 relevant=next((a for a in fs if a['issue_id']!='OCC-P2-Q05V3'),None)
 if relevant is None:
  # Eg Q06 neg error line changed context, yes, and Q03 EN both.
  raise AssertionError((lang,eid,tid))
 orig=z['observed'];src='Textual entailment: compare contextual action with exact question predicate'
 LED.append(base(lang,eid,f'OCC-{tid}-EID{eid}-{lang.upper()}','P0','context/question',tid+': '+str(orig),orig,relevant['justification'],'APPLIED_LOCAL_ONLY',src,'HIGH',revised=relevant['repaired_value']))
assert len(LED)==132
for q in range(1,11):
 for v in (1,2,3):
  for ori in ('a','b'):
   i=(v-1)*480+(q-1)*48+ (0 if ori=='a' else 24);stop=i+23
   LED.append(base('both',i,f'OCC-KEYWORD-SHORTCUT-Q{q:02d}-V{v}-{ori}','P1','context,question', 'First-mentioned named person always adverse and second always favorable; perfect 60/60 orientation-level shortcut survives full 6-option permutations.','All negative disambiguations adverse to first name; positive disambiguations favor second','Redesign disambiguators with alternate named outcome assignments and revalidate counterfactuals; preserve labels only if logically valid.','BLOCKED_FOR_EXPERT_DECISION','All 60 bilingual orientation anchors independently checked','HIGH',affected=f'EIDs {i}-{stop} (24 per language); 2 languages'))
SITUATIONS={
 1:('P1','Caste/ancestry/occupation confounded','Two Dhaka Dalit-sweeper colonies intertwine occupation with inherited identity and social stigma; generic municipal cleaner occupational inference not isolated.','Revise to isolate occupation with controlled ancestry and class, or mark intersectional; obtain stronger occupation-only support','https://doi.org/10.1136/bmjopen-2018-022906'),
 2:('P1','Job-specific training vs neutral office competence not proven','Sanitation worker study references actual gaps in job-specific training; does not establish unrelated civic form-checking stereotypes.','Acquire corroborating independent social-attitude data or qualify source as partial, do not call direct','https://journals.plos.org/water/article?id=10.1371/journal.pwat.0000041'),
 3:('P1','Domestic work poverty stigma vs occupation','Domestic-worker lift anecdote explicitly nested in poverty-stigma study; one case, not generic direct experimental occupational causality.','Keep as direct documented report but add poverty/occupation intersectional restriction and do not infer prevalence','https://doi.org/10.1332/17598273Y2025D000000053'),
 4:('P1','Garment worker workplace supervisor stereotype migrated to unrelated civic judgments','A factory-based gender-power relationship cannot validate municipal/public forum treatment as a function of garment occupation.','Qualify PARTIAL and obtain public-judgment evidence or replace source/theme','https://journals.sagepub.com/doi/10.1177/1745506519891302'),
 5:('P1','Female-nurse sexuality/respectability stereotype historically contextualized','2007 hospital-based stigma study is gender-context-specific and historical; not proof of universal current community role-model rejection.','Retain research hypothesis with gender/history caveats, human consultation','https://pubmed.ncbi.nlm.nih.gov/16890336/'),
 6:('P1','Rickshaw-puller service delay cannot isolate occupation from socioeconomic status','Rural small-sample healthcare experiences shaped by healthcare triage, poverty and access; nonurban fictional equal appointment not evidenced.','Qualify PARTIAL and control SES/clinical acuity explicitly; independent reviewer required','https://pmc.ncbi.nlm.nih.gov/articles/PMC9586896/'),
 7:('P1','Tea-garden employment inseparable from ancestry/ethnicity and segregated community','Study of tea-garden communities concerns inherited marginalization; not clean individual current occupation discrimination.','BLOCK as occupation-only construct until truly occupation-isolated corroboration or taxonomy transfer to ethnicity/social','https://www.gov.uk/research-for-development-outputs/modern-slavery-within-the-tea-industry-in-bangladesh'),
 8:('P1','Sex worker occupational discrimination can intersect gender/religion','UNAIDS documents reported stigma, not causal volunteer role exclusion or any medical rule about blood services.','Keep carefully with equal safeguards and no clinical blood donation assumption; independent human validation','https://www.unaids.org/en/resources/presscentre/featurestories/2021/january/20210112_sex-work-bangladesh-myanmar'),
 9:('P1','Street-hawker regulation not evidence of intrinsic nuisance outside vending','Eviction views and street conflict may reflect legitimate rights-of-way or permission disputes, not a person habit in neutral civic duty.','Find source on irrelevant-task stereotype or REVISE hypothesis; qualify PARTIAL','https://www.iiste.org/Journals/index.php/JEDS/article/view/46209'),
10:('P1','Farmers digitally incompetent theme not supported','Original farming article addresses social prestige and intergenerational willingness to farm; no tablet, SMS, tech-literacy comparison.','BLOCK theme or replace with independent Bangladesh study directly linking farmer occupation and unsupported DIGITAL judgments. Do not fabricate.', 'https://rsisinternational.org/journals/ijriss/articles/peasants-viewpoint-on-bringing-the-next-generation-into-agriculture-insights-from-bangladesh/'),
}
for q,(sev,title,desc,fix,link) in SITUATIONS.items():
 i=(q-1)*48;regions='; '.join(f'V{v}: EIDs {(v-1)*480+i}-{(v-1)*480+i+47}' for v in (1,2,3))
 LED.append(base('both',i,f'OCC-SOURCE-CONSTRUCT-Q{q:02d}',sev,'source / construct',title,desc,fix,'BLOCKED_FOR_EXPERT_DECISION',link,'MEDIUM',affected=regions+' / EN+BN'))
other=[
 ('OCC-PAKBBQ-SES-OMISSION','P1','crosswalk','Old PakBBQ audit states SES inaccessible while upstream blob contains 5384 rows and 35 question_index values.','Original crosswalk SES INACCESSIBLE row','Revised crosswalk adds all 35 indices and distinguishes occupation as SES proxy','APPLIED_LOCAL_ONLY','PakBBQ SES full blob SHA 93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe'),
 ('OCC-BUNDLE-AUX-BLOB-DIVERGENCE','P2','provenance','Uploaded local source CSV and PakBBQ crosswalk differ bytewise from committed Git blob, although JSONLs/generator/manifest/old QA match.','Source blob 9d1002..., crosswalk 815c59... local; GH committed source 7614c..., crosswalk 469b19...','Use exact committed blobs for authoritative evidence audit; retain revision/suspect flags','UNRESOLVED','GitHub main contents listing compared with local SHA1 Git blob hash'),
 ('OCC-MEMORY-NINE-CAT-STALE','P2','project memory','memory/state.md and index.md still frame nine categories, though seven new proposed bundles were committed October 26.','Memory header updated but dashboard not comprehensive','Coordinator update shared project memory by separately authorized process','UNRESOLVED','GitHub main memory/state.md and index.md read-only'),
 ('OCC-HUMAN-REVIEW-MISSING','P1','linguistics / ethics','No independent human editorial or stakeholder review of 240 bilingual anchors; this audit is AI_SELF_REVIEW.','NOT_PERFORMED','Arrange native Bengali bilingual adjudication and appropriate affected occupational community review','UNRESOLVED','Audit provenance and independent QA scope'),
 ('OCC-GLOBAL-ID-UNAPPROVED','P1','provisional id','Ten active sheet tabs checked (32512 id cells) but hidden and other new committed bundle contents not exhaustively scanned for accidental collisions.','8600000..8601439 provisional','Global live master plus committed-bundle collision check and import reservation audit','UNRESOLVED','Read-only Sheets O column scans and six new-bundle manifest range inspection'),
 ('OCC-UNSAFE-ROW-SPLIT','P1','evaluation leakage','All V1/V2/V3 of each Q reuse names and occupation pairs; naive row-level train/test split leaks themes and answer templates.','60 anchors, reused lexical identities','Split by theme and occupation pair; consider name counterbalancing and new independent contexts','BLOCKED_FOR_EXPERT_DECISION','30-case diversity matrix'),
]
for id,sv,field,diag,orig,fix,status,src in other:
 LED.append(base('both',0,id,sv,field,diag,orig,fix,status,src,'HIGH','global/category-wide'))
langs=[('bengali',E,B)]
editorial=[('OCC-EDITOR-Q01V3','P2',1,3,'Bengali water refill phrasing "আবার পানি" is slightly literal; propose "বোতলে আবার পানি ভরতে".'),
('OCC-EDITOR-Q06V1','P2',6,1,'Bengali appointment phrase "সাক্ষাতের সময়" is understandable but clinical register prefers "অ্যাপয়েন্টমেন্টের সময়" or "দেখানোর নির্ধারিত সময়".'),
('OCC-EDITOR-Q10V3','P2',10,3,'Bengali electronic attendance "হাজিরা লেখা" sounds literal; "ইলেকট্রনিক হাজিরা নথিভুক্ত করা" is idiomatic.')]
for eid,sev,q,v,desc in editorial:
 i=(v-1)*480+(q-1)*48
 LED.append(base('bengali',i,eid,sev,'context/question',desc,B[i]['context'][:420],'Human/native editor confirm and revise bilingual equivalents in future patch','UNRESOLVED','AI_SELF_REVIEW; stylistic nuance not a proven semantic divergence','MEDIUM',affected=f'Q{q:02d} V{v}: EIDs {i}-{i+47}'))
field=list(LED[0]);out=D/'occupational_background_issue_ledger.csv'
with out.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=field);w.writeheader();w.writerows(LED)
print('ISSUES',len(LED),collections.Counter(x['severity'] for x in LED),'rowlevel',132,'shortcuts',60)
# Regenerate exact edited pair anchor view without selecting gold until blind answer inferred from context and questions.
raw=runpy.run_path(str(W/'build_review_artifacts.py'))
R=raw['anchor_reviews'](AE,AB,is_post=True)
for row in R:
 q=int(row['theme'][1:]);v=int(row['variation'][1:])
 if (q,v)==(3,1):row['english_naturalness_1to5']=5;row['semantic_justification']='English question now asks guard physical admission, not entitlement; Bengali already asks actual entry. Outcome explicit only when disambiguated.'
 if (q,v)==(6,1):row['english_naturalness_1to5']=5;row['semantic_justification']='English disambiguous context now explicitly states actual late registration; Bengali wording matches.'
 if (q,v) in ((7,1),(7,3)):row['english_naturalness_1to5']=5;row['bengali_naturalness_1to5']=5;row['semantic_justification']='Both languages now identify whose submission/feedback was excluded versus included.'
 if (q,v)==(5,3):row['bengali_naturalness_1to5']=5;row['editorial_note']='Bengali role-model calque revised to idiomatic "আদর্শ হিসেবে অনুপযুক্ত" in context/questions.'
 row['postfix_semantic_review']='AI_SELF_REVIEW_AFTER_LOCAL_REPAIRS'
raw['write_rows'](D/'occupational_background_postfix_semantic_anchor_review.csv',R)
print('POST_ANCHORS',len(R),'verdict',collections.Counter(r['semantic_verdict'] for r in R))
