#!/usr/bin/env python3
"""Complete local issue ledger: per-field fixes + per-row unresolved source/construct issues.
Counts unique issue_ids (not the 2800+ affected row references).
"""
import collections,csv,json
from pathlib import Path
P=Path('/mnt/data')
ENG=[json.loads(s) for s in (P/'banglabbq_health_status_english.jsonl').open()]
BN=[json.loads(s) for s in (P/'banglabbq_health_status_bengali.jsonl').open()]
SRC={r['theme_id']:r for r in csv.DictReader((P/'health_status_source_evidence_matrix.csv').open(encoding='utf-8-sig'))}
FIELD=['severity','issue_id','category','source_commit_sha','file_language','jsonl_line','example_id','id','theme','variation','orientation','context_condition','question_polarity','offending_field','original_value','corrected_value','diagnosis','supporting_evidence_or_citation','proposed_fix','confidence','resolution_status','affected_record_scope']
SHA='e186b283fa5b184058e2cb395273e9968a893b20';out=[]
with (P/'health_status_change_manifest.csv').open(encoding='utf-8-sig',newline='') as f:
 for ch in csv.DictReader(f):
  out.append(dict(severity=ch['severity'],issue_id=ch['issue_id'],category='Health_status',source_commit_sha=SHA,file_language=ch['language'],jsonl_line=ch['line'],example_id=ch['example_id'],id=ch['id'],theme=ch['theme'],variation=ch['variation'],orientation=ch['orientation'],context_condition=ch['condition'],question_polarity=ch['polarity'],offending_field=ch['field'],original_value=ch['original_value'],corrected_value=ch['revised_value'],diagnosis=ch['reason'],supporting_evidence_or_citation='Direct original EN-BN scenario reading; text-level entailment comparison',proposed_fix=ch['revised_value'],confidence='HIGH',resolution_status='APPLIED_LOCAL_ONLY',affected_record_scope='Individual field change in audited candidate, source original unchanged'))

UNRESOLVED=[
 ('HS-S01','P1',2,'EVIDENCE_MECHANISM_OVERREACH','Q02 claims administrative appointment denial although cited HIV qualitative source demonstrates provider clinical mistreatment/denial, not clerical refusal.','Obtain independent Bangladesh source documenting administrative booking refusal or redesign to documented nonclinical support mechanism; needs clinical ethics review.','BLOCKED_FOR_EXPERT_DECISION'),
 ('HS-S02','P1',4,'CATEGORY_CONFOUNDED_AND_EVIDENCE_UNSUPPORTED','Q04 cured leprosy participant with no visible impairment not supported by study of leprosy patients with high disability/visible complications; unsupported health-only comparison.','BLOCK all Q04 pending independent cured-without-impairment source or replace with defensible new theme; do not carry as publication-ready.','BLOCKED_FOR_EXPERT_DECISION'),
 ('HS-S03','P1',7,'APPEARANCE_CATEGORY_CONFOUNDER','Q07 arsenicosis stigma paper concerns patients whose disease often has visible cutaneous signs; no isolation of health disclosure from appearance.','Acquire diagnosis-disclosure-only Bangladeshi evidence/controlled construct or reclassify to appearance intersectionality after oversight.','BLOCKED_FOR_EXPERT_DECISION'),
 ('HS-S04','P1',8,'EXTRAPOLATED_EDITORIAL_GROUP_REJECTION','Q08 epilepsy paper documents perceived social stigma among tertiary-hospital adolescents, not observed student newspaper/debate club exclusions.','Acquire institution-specific social exclusion evidence or recast outcome to documented interpersonal stereotype.','BLOCKED_FOR_EXPERT_DECISION'),
 ('HS-S05','P1',9,'TREATMENT_STAGE_AND_APPEARANCE_CONFOUND','Q09 hospital patient stigma source does not distinguish fully recovered survivor cohort; surgery/appearance, gender and possible task limits overlap.','Obtain evidence specifically on post-treatment survivor rejection independently of health/body-image confound or redesign.','BLOCKED_FOR_EXPERT_DECISION')]
for issue_id,sev,q,kind,diagnosis,fix,status in UNRESOLVED:
 for lang,rows in (('english',ENG),('bengali',BN)):
  for i,r in enumerate(rows):
   if r['question_index']!=q:continue
   m=SRC[f'Q{q:02d}']
   out.append(dict(severity=sev,issue_id=issue_id,category='Health_status',source_commit_sha=SHA,file_language=lang,jsonl_line=i+1,example_id=r['example_id'],id=r['id'],theme=f'Q{q:02d}',variation=f'V{i//480+1}',orientation=r['additional_metadata']['version'],context_condition=r['context_condition'],question_polarity=r['question_polarity'],offending_field='additional_metadata.source / scenario construct',original_value=r['additional_metadata']['source'],corrected_value='NO CHANGE; source/construct unresolved',diagnosis=f'{kind}: {diagnosis}',supporting_evidence_or_citation=m['all_sources']+' ; '+m['actual_supported_claim'],proposed_fix=fix,confidence='HIGH for source mismatch; MODERATE for design decision',resolution_status=status,affected_record_scope='Every affected QA record included; 144 per language for this theme'))
# Related low-severity/robustness risks, flagged per case rather than as structural defects.
EXTRA=[
 ('HS-X01','P2',[ (8,3),(10,3)],'Cross-theme evaluation leakage: Q08 V3 and Q10 V3 both newsletter/editorial membership decision in campus student clubs, differentiated mainly by health condition.','Design independent outcome/decision architecture for one variation or group-aware train/test partition.','UNRESOLVED'),
 ('HS-X02','P2',[(2,1),(2,2),(2,3)],'Q02 three V1/V2/V3 variants remain appointment/consultation-slot gatekeeping and may yield correlated template leakage despite distinct venue and modality.','Do not split V1/V2/V3 across evaluation folds independently; consider better differentiated action in new research revision.','UNRESOLVED')]
for issue_id,sev,pairs,diagnosis,fix,status in EXTRA:
 for lang,rows in (('english',ENG),('bengali',BN)):
  for i,r in enumerate(rows):
   q=r['question_index'];v=i//480+1
   if (q,v) not in pairs:continue
   out.append(dict(severity=sev,issue_id=issue_id,category='Health_status',source_commit_sha=SHA,file_language=lang,jsonl_line=i+1,example_id=r['example_id'],id=r['id'],theme=f'Q{q:02d}',variation=f'V{v}',orientation=r['additional_metadata']['version'],context_condition=r['context_condition'],question_polarity=r['question_polarity'],offending_field='scenario diversity / cross-theme overlap',original_value=r['context'][:260],corrected_value='NO CHANGE - requires substantive theme design',diagnosis=diagnosis,supporting_evidence_or_citation='Cross-case manual AI comparison of authored Q/V templates; see semantic-anchor review and case diversity audit',proposed_fix=fix,confidence='MODERATE',resolution_status=status,affected_record_scope='Variation family warning, intentionally not classified as unintended exact duplicate'))
META=[
 ('HS-QA01','P1','Original validator missed 7 of 26 fault injections and crashed on 2; independently coded test missed unsupported source-tier falsification F21 (25/26 automated detection).','Add evidence-tier consistency and human source-review gate, explicit semantic fixtures, graceful exceptions.','ADDITIONAL_TEST_REQUIRED','validator.py','Adversarial results F14 F15 F16 F17 F18 F20 F21 F22 F24'),
 ('HS-QA02','P2','The committed source-audit and PakBBQ-crosswalk CSV Git blobs do not match regenerated local artifact Git hashes while JSONL and manifest do.','Preserve committed CSV snapshots, compare normalized row-by-row content before accepting regenerated lineage.','UNRESOLVED','CSV provenance','Committed blob SHAs 236be8fb..., bf80053c...; generated repo local blobs differ')]
for issue_id,sev,diagnosis,fix,status,field,cit in META:
 out.append(dict(severity=sev,issue_id=issue_id,category='Health_status',source_commit_sha=SHA,file_language='BOTH/METADATA',jsonl_line='',example_id='',id='',theme='Q01-Q10',variation='',orientation='',context_condition='',question_polarity='',offending_field=field,original_value=diagnosis,corrected_value='NOT APPLICABLE',diagnosis=diagnosis,supporting_evidence_or_citation=cit,proposed_fix=fix,confidence='HIGH',resolution_status=status,affected_record_scope='Audit pipeline or evidence provenance, not a single row'))

with (P/'health_status_issue_ledger.csv').open('w',newline='',encoding='utf-8-sig') as f:
 wr=csv.DictWriter(f,fieldnames=FIELD);wr.writeheader();wr.writerows(out)
unique={x['issue_id']:x['severity'] for x in out};c=collections.Counter(unique.values());res=collections.Counter(r['resolution_status'] for r in out)
summ={'ledger_rows':len(out),'unique_issues':len(unique),'counts_by_severity_unique_issue_id':dict(c),'counts_by_status_rows':dict(res),'fixes':len([q for q in unique if q.startswith('HS-P')]),'unresolved':len([q for q in unique if not q.startswith('HS-P')]),'source_theme_blockers':['Q02','Q04','Q07','Q08','Q09']}
(P/'health_status_issue_ledger_summary.json').write_text(json.dumps(summ,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summ,indent=2))
