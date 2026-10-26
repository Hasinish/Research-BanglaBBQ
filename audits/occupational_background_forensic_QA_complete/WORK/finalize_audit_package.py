import json,collections,csv,hashlib,sys,subprocess,shlex,os,zipfile
from pathlib import Path
D=Path('/mnt/data/occupational_forensic_audit');W=D/'WORK';BASE=Path('/mnt/data');C='e186b283fa5b184058e2cb395273e9968a893b20'
meta={
 'category':'Occupational_background','repository':'Hasinish/Research-BanglaBBQ','latest_main_commit_sha':C,
 'bundle_push_commit':'214795f628a34ece8deb23a65c6bf35ac0ce7157',
 'source_Git_blob_sha':{'english':'5980485457379e3e91d1cd667b9c1b8004aa8e44','bengali':'d257262a9d2a4dd9df8ed100fe4694e611835145'},
 'source_paths':{'english':'banglabbq_occupational_background_readonly_bundle/banglabbq_occupational_background_english.jsonl','bengali':'banglabbq_occupational_background_readonly_bundle/banglabbq_occupational_background_bengali.jsonl'},
 'audit_execution_date_utc':'2026-10-26','read_only_remote':True,'originals_immutable':True,
 'human_review':'NOT_PERFORMED','ai_editorial':'AI_SELF_REVIEW','source_audit_status':'PARTIAL / CONTEXTUAL for 7 themes; three direct limited mechanisms',
}
orig=json.loads((W/'original_independent_validation_sources.json').read_text());post=json.loads((W/'postfix_independent_validation_sources.json').read_text());adv=json.loads((D/'occupational_background_adversarial_results.json').read_text());advpost=json.loads((D/'occupational_background_postfix_adversarial_results.json').read_text())
issues=list(csv.DictReader((D/'occupational_background_issue_ledger.csv').open(encoding='utf-8')))
sources=list(csv.DictReader((D/'occupational_background_source_evidence_matrix.csv').open(encoding='utf-8')))
anchors=list(csv.DictReader((D/'occupational_background_semantic_anchor_review.csv').open(encoding='utf-8')));postanchors=list(csv.DictReader((D/'occupational_background_postfix_semantic_anchor_review.csv').open(encoding='utf-8')))
changes=list(csv.DictReader((D/'occupational_background_change_manifest.csv').open(encoding='utf-8')))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
identity={}
for lang in ('english','bengali'):
 src=D/'ORIGINAL'/f'banglabbq_occupational_background_{lang}.jsonl'
 fixed=D/f'occupational_background_audited_{lang}.jsonl'
 identity[lang]={'source_SHA256':sha(src),'audited_SHA256':sha(fixed),'source_bytes':src.stat().st_size,'audited_bytes':fixed.stat().st_size,'new_lines_checked':sum(1 for line in fixed.open()),'changed_records':len({x['example_id'] for x in changes if x['language']==lang})}
# Construct explicit stage gates: safe only if all are true, zero source-critical decisions etc.
readiness={
 **meta,
 'status':'NOT_IMPORTED', 'safe_to_import':False, 'import_approval':'DENIED_PENDING_RESEARCH_DECISIONS',
 'reason':'Local P0 repairs do not resolve first-name answer shortcut (60/60), Q07 ancestry/ethnicity construct confound, Q10 unsupported source mechanism, or missing independent human review.',
 'headers_in_sheets_A_to_O':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','answer_info','additional_metadata','category','id'],
 'jsonl_key_order':['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id'],
 'serialized_sheet_columns':['example_id','question_index','context_condition','question_polarity','type','context','question','ans0','ans1','ans2','label','JSON.stringify(answer_info)','JSON.stringify(additional_metadata)','category','id'],
 'planned_workbook_url':'https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit',
 'occupational_worksheets_exist':False,'occupational_worksheets_imported':False,
 'provisional_id_range_inclusive':[8600000,8601439],
 'active_production_worksheets_read_only_checked':10,
 'active_production_id_cells_checked':32512,
 'other_six_new_category_jsonls_read_only_checked':12,
 'other_six_new_category_id_cells_checked':17280,
 'collisions_in_checked_active_and_new':0,
 'hidden_sheet_and_legacy_complete_global_inventory':'NOT_EXHAUSTIVELY_SCANNED',
 'current_own_category_id_unique':True,
 'bilingual_record_parity':True,
 'source_provenance_comparison':'local auxiliary source audit and crosswalk differ from committed byte SHAs; use committed GitHub metadata and independent findings',
 'formula_injection_scan':'PASS automated negative-leading-cell tests 2880 JSONL records; Sheets import not tested',
 'json_columns_ready_for_explicit_serialization':True,
 'postfix_structural_errors':post['errors_count'],
 'semantic_review':{'original_paired_anchors_enumerated':240,'original_anchor_verdicts':dict(collections.Counter(a['semantic_verdict'] for a in anchors)), 'postfix_paired_anchors_enumerated':240,'postfix_anchor_verdicts':dict(collections.Counter(a['semantic_verdict'] for a in postanchors)),'independent_human_review':False},
 'unresolved_gate_failures':['P1 systematic adverse-first-person leakage','P1 Q07 ethnicity/ancestry confounding','P1 Q10 digital incompetence insufficient direct evidence','P1 partial-source transfer across several themes','Independent Bangladeshi Bengali and impacted community review absent','Project-level schema/taxonomy decision on proposed Occupational_background extension','Master import/approval not performed'],
}
(D/'occupational_background_import_readiness.json').write_text(json.dumps(readiness,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Real execution log extracted from results, not estimated.
log=f'''# Occupational Background local forensic QA run log

- Audit date: 2026-10-26 UTC; GitHub `main`: `{C}`; original English/Bengali blobs exact to committed raw files.
- Connected GitHub READ operations: current branch SHA; five memory files; contents directory + exact blob SHAs; PakBBQ full SES blob (5384 parsed/35 themes) and Regional (944/18); six other bundles x2 JSONL files (12 x1440 parsed).
- Connected Google Sheets READ operations: metadata, canonical Education EN/BN A1:O3, active Age/Politics/Religion/Gender/Education EN/BN ID column O2:Oend. Scanned **32,512** active ID cells; **0** occupational ID collisions. Cross-bundle GitHub **17,280** records, **0** occupational collision. Hidden sheets not enumerated by content.
- Original generator invoked in separate directory:
  `python /mnt/data/banglabbq_occupational_background_generator.py --out /mnt/data/occupational_forensic_audit/WORK/regenerated_original`
  Execution: **PASS**, source English/Bengali JSONLs byte-identical; manifest and old QA report byte-identical; source and crosswalk CSV byte-identical to *locally supplied generator reference* but not to corresponding live committed Git blob SHA (see below).
- Author validator directly called via Python on original records and 60 manifest orientations: **0 failures**. Repeated on local repaired pair: **0 failures**. This validator **MISSED** 132 original sentence-level P0 row defects.
- Independent validator invoked:
  `python occupational_background_independent_validator.py --english ORIGINAL/banglabbq_occupational_background_english.jsonl --bengali ORIGINAL/banglabbq_occupational_background_bengali.jsonl --manifest /mnt/data/banglabbq_occupational_background_expansion_manifest.json --source-map /mnt/data/banglabbq_occupational_background_source_audit.csv --json-out WORK/original_independent_validation_sources.json`
  Result: **{orig['errors_count']} issues** (original) out of **2,880 total rows**.
- Local repairs through `WORK/patch_semantics_and_fix.py` (fixed literal-scoped text only): **{len(changes)} field edits** (English {sum(x['language']=='english' for x in changes)}; Bengali {sum(x['language']=='bengali' for x in changes)}), 2 audited JSONL files, diff CSV. The patch script is local and does not contact any remote service.
- Independent validator on revised pair, same source-map and manifest: **{post['errors_count']} automated row-level failures**, all 2,880 rows; all 240 post-fix paired semantic anchors regenerated with original judge notes adjusted only where repairs actually changed text.
- Adversarial mutation fixture runner actually executed **{adv['metrics']['fixtures_executed']}** distinct mutations on original and **{advpost['metrics']['fixtures_executed']}** on audited pair; existing original validator detected {adv['metrics']['existing_validator_detected']}/30, independent validator detected {adv['metrics']['independent_validator_detected']}/30. IMPORTANT: many detections were *indirect consistency failures*, not true understanding of the injected cultural/semantic defect. `editorial_fault_oracle_detected` is specified by human-written fixture expectation, not automatic human adjudication or generic semantic correctness.
- Source verification: **14 URL audit entries** across 10 themes, independently scoped and tier-calibrated in source matrix. All URLs were attempted as original or indexed/canonical alternatives; publisher direct access can be 403 or abstract-only; no claim all full texts opened.
- Semantic/editorial: 30 pairwise variations × 2 orientations × 4 context/polarity states = **240 paired EN/BN anchor entries**, with textual reasoning and editorial/cultural scores; six permutations then mechanically validated across **1,440 records per language**. Language assessment is **AI_SELF_REVIEW**, not independently human certified.
- No git write/push/issue/PR, Google Sheets write/update or remote mutation. Local immutable ORIGINAL snapshots retained unchanged.

## Reference-vs-commit divergence discovered

Two pre-existing local auxiliary files (not JSONLs) have Git blob SHA mismatches with committed `main`:

| Artifact | Local Git blob SHA | Committed SHA | Consequence |
|---|---|---|---|
| source_audit.csv | `9d1002c2db205253ed9531f551be74275b371762` | `7614cefbc78a299e73284606f56730e83ac61278` | Original auxiliary not byte-identical; use independent evidence matrix, committed source names read via connector |
| pakbbq_theme_crosswalk.csv | `815c59e68d64cc8acacdd439d08fba6b65a5906c` | `469b19383171987d065790f7baaf93b04940f00b` | Old local crosswalk needed SES correction and not a verified committed byte snapshot |

The generator/manifest/English/Bengali/old QA report DID match their committed Git blobs. Local auxiliary mismatches may be serialization differences and were not silently normalized.

## Checksums

| Artifact | SHA-256 |
|---|---|
| immutable source English | `{identity['english']['source_SHA256']}` |
| immutable source Bengali | `{identity['bengali']['source_SHA256']}` |
| local audited English | `{identity['english']['audited_SHA256']}` |
| local audited Bengali | `{identity['bengali']['audited_SHA256']}` |
'''
(D/'occupational_background_local_reproducibility_log.md').write_text(log,encoding='utf-8')
print('LOG_BYTES',len(log),'GATES',readiness['safe_to_import'],'IDENTITY',json.dumps(identity,indent=2),'SOURCES',collections.Counter(x['independent_evidence_tier'] for x in sources))
