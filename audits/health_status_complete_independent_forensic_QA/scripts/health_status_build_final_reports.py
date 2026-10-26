#!/usr/bin/env python3
"""Create final forensic reports from executed local test evidence; no remote writes."""
import collections,csv,hashlib,json,textwrap
from pathlib import Path
P=Path('/mnt/data')
def J(n):return json.loads((P/n).read_text(encoding='utf-8'))
pre=J('health_forensic_work/independent_validator_results.json');post=J('health_forensic_work/postfix/independent_validator_results.json');adv=J('health_status_adversarial_results.json');ledger=J('health_status_issue_ledger_summary.json');repair=J('health_status_local_repair_summary.json');repro=J('health_status_reproducibility_log.json');imp=J('health_status_import_readiness.json')
base=list(csv.DictReader((P/'health_status_semantic_anchor_review.csv').open(encoding='utf-8-sig')))
fixed=list(csv.DictReader((P/'health_status_semantic_anchor_review_postfix.csv').open(encoding='utf-8-sig')))
sources=list(csv.DictReader((P/'health_status_source_evidence_matrix.csv').open(encoding='utf-8-sig')))
urls=list(csv.DictReader((P/'health_status_source_url_audit.csv').open(encoding='utf-8-sig')))
severities=collections.Counter(ledger['counts_by_severity_unique_issue_id']); sourcecounts=collections.Counter(s['forensic_tier'] for s in sources)
assert len(base)==len(fixed)==240
assert sum(row['semantic_equivalence']=='FAIL' for row in base)==40
assert all(row['blind_gold_match']=='PASS' for row in base+fixed)
assert all(row['semantic_equivalence']=='PASS' for row in fixed)
assert pre['summary']['num_row_findings']==post['summary']['num_row_findings']==0
assert len(pre['checks'])==len(post['checks'])==47
assert len(urls)==12 and len(sources)==10

def sha(filename):return hashlib.sha256((P/filename).read_bytes()).hexdigest()
FILES=['banglabbq_health_status_english.jsonl','banglabbq_health_status_bengali.jsonl','health_status_audited_english.jsonl','health_status_audited_bengali.jsonl','health_status_audited_expansion_manifest.json','health_status_change_manifest.csv','health_status_issue_ledger.csv','health_status_source_evidence_matrix.csv','health_status_semantic_anchor_review.csv','health_status_semantic_anchor_review_postfix.csv','health_status_source_url_audit.csv','health_status_adversarial_results.json']
checks='''| Test group | Original | Candidate | Actually tested / evidence |
|---|---|---|---|
| JSONL UTF-8, 15 keys in canonical JSONL order, metadata types, blank/control characters | PASS | PASS | 2,880 parsed original + 2,880 candidate; 47-gate independent script with row failures exported |
| 10 themes x 3 variations x 48 | PASS | PASS | 60 variation blocks (30/language), 2,880 records |
| 2 orientations x 2 contexts x 2 polarities x 6 permutations, four-condition ordering | PASS | PASS | 60 oriented blocks/language, 6 x 4 records each |
| Answer-info roles, gold positions, no unintended complete duplicates | PASS | PASS | All 2,880 original and 2,880 candidate; gold positions 480/480/480 per language |
| Provisional ID range, examples 0..1439 | PASS (provisional) | PASS (provisional) | All 2,880 records; live workbook and six new bundles read-only sentinel checks |
| English-Bengali metadata and role alignment | PASS | PASS | 1,440 paired records; textual meaning assessed separately |
| Blind algorithmic context/question entailment anchor check | PASS | PASS | 240 anchors (30 x 2 x 4) per bilingual pair; role extraction uses explicit event sequence, not full semantic adjudication |
| AI base-variation language/construct review | FAIL | PARTIAL | 30 bilingual authored base cases (120 context condition forms per language) with derived 240-anchor scorecard; five families had semantic/procedural mismatch, plus grammar; local patches repair five |
| Cross-theme and variant leakage/independence | PARTIAL | PARTIAL | 30 authored settings; Q08V3/Q10V3 newsletter design overlap; Q02 booking variants correlated; all 6 other bundle EN files had 0 exact context+question collisions |
| Source support for narrow physical-health mechanism | FAIL | FAIL | Ten themes, 12 distinct opened/indexed source URLs; DIRECT=5 PARTIAL=4 UNSUPPORTED=1; Q04 blocked |
| Clinically meaningful category isolation | PARTIAL | PARTIAL | 30 base scenarios; Q04 leprosy/disability, Q07 arsenicosis/appearance, Q09 cancer/treatment-stage confounds unresolved |
| Original author validator | PASS | PASS | 32/32 on each, but missed fault injections; cannot establish independent review |
| Independent author-unrelated structural validator | PASS | PASS | 47/47 each; zero row failures; candidate uses corrected manifest |
| Adversarial fault injection | FAIL | FAIL (validator blind spot persists) | 26 injected distinct local mutants: author FLAGGED 17, CRASHED 2, MISSED 7; independent flagged 25, missed source-tier tamper F21 |
| Author generator / byte reproducibility | PARTIAL | LOCAL PATCH REPRODUCIBLE | Prior isolated regen matches all 7 local seed files; 5/7 local artifact Git blobs match current committed files, two CSVs differ; local patch run twice byte-identical |
| Actual independent human review | NOT PERFORMED | NOT PERFORMED | No person hired or reviewed; AI_SELF_REVIEW only |
| Google Sheets import and live-parity verification | NOT IMPORTED | NOT IMPORTED | No Health tabs; 2,880 prospective rows = 43,200 cells, never written |
'''
provenance=f'''## 1. Snapshot and source-of-truth protocol

- **Category:** `Health_status` (PHYSICAL HEALTH). Proposed new extension to BRAC University seniors' nine-category BanglaBBQ, not the existing `Mental_health_status` and not the Disability/Physical Appearance category. Historical seniors' data unchanged, with zero legacy physical-health records reused.
- **Live GitHub `main` HEAD at read-only audit:** `e186b283fa5b184058e2cb395273e9968a893b20` (2026-10-26 06:18:04 UTC). Bundle push: `214795f628a34ece8deb23a65c6bf35ac0ce7157` at 06:17:25 UTC. Later commit only modified memory/state. Audit fetched latest `main` memory files and 7 Health bundle files via GitHub connector; no commits/pushes/issues/PRs modified.
- English `banglabbq_health_status_complete/banglabbq_health_status_english.jsonl` **Git blob** `a637d6ac18ac901c7a22356dbf47d244230e63b2`, **SHA256** `{sha('banglabbq_health_status_english.jsonl')}`.
- Bengali `banglabbq_health_status_complete/banglabbq_health_status_bengali.jsonl` **Git blob** `525d72db59ad609d07cf855f128aa09a6da936da`, **SHA256** `{sha('banglabbq_health_status_bengali.jsonl')}`.
- Original generator Git blob `4c107612d5c9b043b8e229aa5ef3c95939aa4399`; manifest Git blob `d9a16b6635461d48522e07f58669bffd093d4b66`; QA report blob `ca8e7b30caede493a4ac6fef824884a19a285b99`.
- **Two auxiliary-provenance discrepancies:** Current committed `source_audit.csv` Git blob `236be8fbe941839c61e55be1357a3549b166bdb1` vs local regenerated blob `7f2abf51a1dbedb2df2e65ffb277c3fbb3db85ce`; committed `pakbbq_theme_crosswalk.csv` blob `bf80053cdbf13acb253330c03456339a2c36275a` vs local regenerated blob `4c1ca3919e21fd0dcb0bcc2fcb450c4026db9019`. Both local files regenerate byte-identically, but their hashes are **not** committed blob hashes. The actual committed CSV text was read using the GitHub connector, not materialized as bytes; therefore no byte-diff or row-by-row equivalence claim is made. This is a reproducibility blocker for auxiliary CSVs, not a statement that the JSONLs differ.
- Shared memory `README/purpose/state/index/history` read live. `history.md` describes the October 26 seven-bundle push; `state.md` dashboard and `index.md` file tree still describe nine original categories and omit seven proposed new bundle directories. They require **separate authorized synchronization**, not an edit by this auditor.
- Master Google Sheet metadata and Education A1:O2 read-only; no Health sheet exists. GitHub snapshot is the only input to this audit.

## 2. Exactly what was checked

**Input totals:** 1,440 English + 1,440 Bengali = 2,880 original records. `question_index` integers 1..10, exactly 144 per theme per language, 3 waves of 480 records (V1 Q01-Q10, V2 Q01-Q10, V3 Q01-Q10), one 48-row scenario per theme/wave. Orientation `a` rows 0..23 and `b` rows 24..47 within each block, six full option permutations with 4 order states `ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`. Counts 720/720 for contexts and polarities, 720 `a`/720 `b`, 360 of each of four condition/polarity pairs and 480 label positions 0/1/2 **per language**. Zero invalid JSONL lines, control-character leaks, duplicate complete QA tuples, schema failures, or broken role/metadata parity in all examined records.

- JSONL 15 ordered keys `example_id,question_index,question_polarity,context_condition,category,answer_info,additional_metadata,context,question,ans0,ans1,ans2,label,type,id` are exactly preserved.
- **Google Sheets 15-column A:O order differs**: `example_id,question_index,context_condition,question_polarity,type,context,question,ans0,ans1,ans2,label,answer_info,additional_metadata,category,id`. The two nested dictionaries must be `json.dumps`-serialized into sheet cells, not placed as raw Python mappings.
- `id` values are **provisional** `8,300,000..8,301,439`. Scanned all 10 active production Sheets' column-O sentinel results: only unrelated value 8300 in both Gender sheets; six other new category bundles' 1,440 English rows each have non-overlapping reserved ranges. Exact cross-category context+question overlaps across all six *new* English bundles were **0**; similarity/semantic leakage cannot be excluded from exact matching. The global collision search is not a final all-repository exhaustive audit; IDs not approved for import.
- Distinct authored text: 60 ambiguous and 60 disambiguated contexts per language, and 60 unique question strings per language; the 6 answer-position variants per case are legitimate, not duplicates. The **60 counterfactual orientation contexts** are different only in health-status assignments with fixed person names/qualification backgrounds; event outcomes mirror the named roles, not physical health.

'''
source_table='| Q | Disease/history and decision | Forensic support | Exact source limitation |\n|---|---|---|---|\n'
for x in sources:
 source_table+=f"| {x['theme_id']} | {x['theme']}; {x['forensic_decision']} | **{x['forensic_tier']}** | {x['evidence_strength_limits']} |\n"

report=f'''# BanglaBBQ Health Status — Independent Forensic QA Report

**Run date:** October 26, 2026 (Asia/Dhaka). **Audit mode:** read-only GitHub/Google Sheets, local code and files only. **Human linguistic/clinical review:** NOT PERFORMED. **Publication/import status:** **NOT SAFE**. **Methodology:** adversarial AI self-review, independent structural implementation, source re-opening, 30 bilingual base variations with 240 instantiated bipolar-context anchors.

{provenance}
## 3. Major test-group verdicts (not a retrospective checklist)

{checks}

Independent validator executed: 47/47 PASS on original and corrected JSONLs with 0 row-level automated failures on **each 2,880-record set**; original author-supplied generator's validator 32/32 PASS on each. Neither proves source fitness or natural language correctness. Original `independent_row_failures.csv` and corrected `postfix/independent_row_failures.csv` contain headers only, proving zero findings **under those tests**.

## 4. Blind gold inference and bilingual/editorial examination

The AI reviewed **all 30 distinct EN/BN base scenario families**, including role names, illness-state assignments, matching of qualifications, decisive action predicates, and Bangla grammar. For traceability, `health_status_semantic_anchor_review.csv` enumerates **240 anchors** (30 variations × 2 orientations × 4 context/polarity states), with both full language texts and answer options, literal decision excerpt, independent programmatic inferred answer computed before accessing `label`, gold comparison, and inherited base-case editorial scores. Each anchor was computed from the actual committed JSONL; the **qualitative score is a base-family AI judgment expanded to all 8 anchors**, not 240 separately employed human reviewers. Unique answer permutations were separately checked across all 2,880 records. Exactly **240/240 anchors** have explicit evidence-based gold positions under the implemented role-order test; ambiguous Unknown is retained. The original bilingual audit flags **40/240 anchor rows** across **5 family-level semantic/procedural mismatches**: Q03V3, Q04V2, Q06V1, Q06V3, Q09V2. Candidate local corrections bring scored semantic-equivalence flags to **0/240**, with no label changes or new sources.

Additional Bengali quality issues in Q05V1–V3 (missing correct possessive/case form), Q08V1 (student newspaper phrasing), Q08V3/Q10V3 (ungrammatical বার্তাপত্রর), and Q09V3 (unidiomatic বসে করা যায় responsibility phrase) were corrected locally. Editorial/meaning parity is **AI_SELF_REVIEW_BASE30_PLUS_ANCHOR_DERIVATION**; **AI_LINGUISTIC_REVIEW_COMPLETED_BASE_LEVEL=YES**, **INDEPENDENT_HUMAN_REVIEW=NOT_PERFORMED**. Bengali score ≤3 in original triggers rewrite, not a certificate of cultural authenticity. **Do not report this as independently human-reviewed Bengali**. All scenarios remain **fictional hypothetical benchmark probes**; cited sources do not prove those exact choices occurred.

**Counterfactual conclusion:** Every `a`/`b` pair of 24-row blocks mechanically swaps only which named person has the physical-health condition, leaving eligibility, measured work and evaluator choices fixed. This was tested over all original and corrected bilingual rows. But a medically suitable comparison is not guaranteed merely because the text asserts conditions equal: healthcare-admin and treatment-stage confounds need specialist input. Clinically appropriate precautions must not be categorized as unjustified bias; the tasks are written as non-clinical administrative/remote/desk cases, but not independently certified by a clinician.

## 5. Twelve linked publications and evidence scope

Each of **12 distinct source URLs** appearing in the original metadata and/or source-audit CSV was opened or checked by indexed publisher/primary-document records during the current 2026-10-26 audit. `health_status_source_url_audit.csv` states accessibility per exact URL: **6 publisher full-text sources**, **1 PMC full-text source**, **1 publisher abstract**, and **4 indexed/blocked primary records** (leprosy study/correction, arsenicosis and hepatitis B). These are link-access statuses, not evidence-tier ratings (the precise breakdown should be read from the 12-row CSV). Access not assumed as full-text when cache failed. No facts imported from PakBBQ as evidence for Bangladesh.

**Forensic theme tiers:** DIRECT **{sourcecounts['DIRECT']}/10**, PARTIAL **{sourcecounts['PARTIAL']}/10**, UNSUPPORTED **{sourcecounts['UNSUPPORTED']}/10** for the **narrow fictional mechanism**. DIRECT means the Bangladesh-specific source actually documents the relevant stigma or attitude mechanism, **not** that a controlled causal demonstration of the fictional event exists. Q02, Q07, Q08 downgraded from originally marked DIRECT to PARTIAL; Q04 downgraded PARTIAL to UNSUPPORTED. Q09 remained PARTIAL. These decisions are reflected in candidate manifest's local `evidence_tier`, NOT the original committed metadata.

{source_table}

**Examples of independently located evidence (quoted numbers carefully):** A Bangladesh PLHIV qualitative study describes a respondent being dismissed from an office job after HIV disclosure and also discriminatory provider behavior (PLOS ONE DOI `10.1371/journal.pone.0276575`); neither proves fictional clerk appointment refusals (Q02). A TB online sample reports **648 of 1,180** unwilling to work with someone previously treated for TB (54.92%; PMC9553051; nonrepresentative sampling). A Jamalpur student thalassemia survey interviews 1,578 students and records friendship hesitancy in its relevant familiar subgroup (Orphanet DOI `10.1186/s13023-020-1323-y`). A leprosy disability study relies on specialist samples with substantial physical impairment; October 16, 2026 correction changes study site description (PLOS DOI `10.1371/journal.pone.0361054`), so it cannot substantiate the isolated *treated but no impairment* construct. The 2019 Dhaka breast-cancer source reports community neglect among *patients*, not independently identified fully recovered survivors; the 2025 JMIR source includes **both Bangladesh and West Bengal, India**. HBV survey 440 student responses document perceived discrimination and social discomfort, not observed editor choices. Detailed source link and evidence caveats appear in the accompanying 10-theme matrix and 12-URL audit.

**Clinical guardrails:** The benchmark is deliberately separated from Mental Health, Physical Appearance and Disability. The problem cases explicitly concern treatment/disclosure, not a medical judgment or valid infection-control recommendation. For TB, the vignette states clinical clearance. For COVID, the vignettes are historically set in 2022/2023 after isolation and recovery. For HBV, scenarios are remote or non-exposure tasks. Even so, independent medical review of the disease-specific framing has **not** occurred. The leprosy/arsenicosis/cancer themes remain potentially compounded with visible changes, treatment history or disability and are currently not independently identifiable social-bias constructs.

## 6. Methodological PakBBQ crosswalk / originality

The live PakBBQ `main` English `PakBBQ/PakBBQ_ENG/Disability_status.jsonl`, Git blob `1a4b58cb5e56a7a9d52130e9f0103b2262e60b0b` at baseline commit `c079dbae2d676f4e3bb82982144d6d4ac10436d4` contains **1,380 rows over 33 distinct question_index values**, covering disabilities, blindness, deafness, cognitive and developmental differences and mental-health content. There is no direct physical-illness disclosure/treatment-history category: **NO_DIRECT_EQUIVALENT**. The prior crosswalk has 33 real upstream theme entries and 10 independent Bangladesh replacements. None of the 30 new situations copies Pakistani place names (Karachi/Lahore/etc.) or Pakistan-specific laws. Histories must be academically cited as methodological inspiration, not evidence of social prevalence.

## 7. Every issue and local repair scope

`health_status_issue_ledger.csv` contains **{ledger['ledger_rows']:,} row-/field-level evidence entries representing {ledger['unique_issues']} distinct issue IDs**: **P0 {severities.get('P0',0)}; P1 {severities.get('P1',0)}; P2 {severities.get('P2',0)}; P3 {severities.get('P3',0)}**. Severity counts are by **unique issue ID**; row entries include 840 applied field-cell change rows and 1,440 source-critical per-row blocker records across five themes. No previous QA claim is treated as validation.

| Issue | Severity | Example IDs (original JSONL line = EID+1) | Problem | Action |
|---|---|---|---|---|
| HS-P01 | P1 | Q04V2 EID 624–671 | EN “electing” vs Bengali committee-chair selection | Changed EN to “selecting”, local only |
| HS-P02 | P1 | Q09V2 EID 864–911 | EN “score written descriptions” vs BN “verify/review” | EN “review”, local only |
| HS-P03 | P1 | Q06V3 EID 1200–1247 | Three-person study “pair” contradictory | EN study “group”, local only |
| HS-P04 | P1 | Q03V3 EID 1056–1103 | “peer mentor” vs “সহশিক্ষক”/co-teacher | EN “assistant trainer” / BN “সহপ্রশিক্ষক”, local only |
| HS-P05 | P2 | Q06V1 EID 240–287 | Indoor vs informal/ঘরোয়া group descriptor | EN “informal”, local only |
| HS-P06 | P2 | Q05V1 EID 192–239; V2 672–719; V3 1152–1199 | BN missing genitive for COVID-negative applicant | BN “আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি”, local only |
| HS-P07 | P2 | Q08V3 EID 1296–1343 and Q10V3 EID 1392–1439 | BN malformed বার্তাপত্রর suffix | Corrected to বার্তাপত্রের, local only |
| HS-P08 | P2 | Q09V3 EID 1344–1391 | BN defective “এ বসে করা যায়” | Natural ability parity sentence, local only |
| HS-P09 | P2 | Q08V1 EID 336–383 | BN possessive and gerund syntax | Corrected, local only |
| HS-S01..S05 | P1 each | Q02 EID 48–95/528–575/1008–1055; Q04 EID 144–191/624–671/1104–1151; Q07 EID 288–335/768–815/1248–1295; Q08 EID 336–383/816–863/1296–1343; Q09 EID 384–431/864–911/1344–1391 | Source-mechanism or treatment/disability/appearance confounds | BLOCKED: retain originals/candidates, obtain expert decision |
| HS-X01, HS-X02 | P2 | Q08V3+Q10V3; Q02V1–V3 | Same newsletter decision or repeated booking-only variants can leak between splits | Family-aware holdout or redesign, unresolved |
| HS-QA01 | P1 | All; fixture F21 | Source-tier falsification missed by both automated validators | Expert evidence gate and source-tier tests required |
| HS-QA02 | P2 | 2 committed auxiliary CSVs | Not byte-identical with generator output | Reconcile committed CSV vs generated CSV source, unresolved |

**Local patch footprint:** {repair['change_count']} field-level edits across {repair['distinct_changed_language_rows']} unique `(language,example_id)` pairs: {repair['english_changes']} English field edits, {repair['bengali_changes']} Bengali edits. No top-level keys, record counts, labels, IDs, group-role metadata, source URLs or category string changed. All originals preserved. The candidate's **separate updated expansion manifest** is required for lineage: when corrected JSONLs were compared against the unchanged original manifest, 576 expected text-lineage mismatches appeared, correctly exposing that the original manifest had not yet been updated. After locally patching the manifest, **47/47** gates PASS and **0** row failures. Candidate manifest/source tier calibrated; original GitHub snapshot unchanged. Original author validator still reports 32/32 on the candidate, illustrating its weak language/construct coverage.

## 8. Adversarial tests executed, not hypothetical

**26/26** distinct local mutants were constructed and individually passed into both validators in memory, preserving originals. Author/generator validator results: **{adv['author_flagged']} FLAGGED, {adv['author_crashed']} CRASHED, {adv['author_missed']} MISSED**; crash is not a controlled successful rejection. Separate independent validator: **{adv['independent_automatic_detected']}/26 automatically detected; {len(adv['independent_automatic_false_negatives'])} missed**. The undetected mutant **F21** changes Q04 evidence tier PARTIAL → DIRECT in manifest without new proof; metadata structural tests cannot verify source-relevance truth. Another fault F14 alters only a Bengali answer name and shows the difficulty of detecting bilingual referent mismatch from role tags alone; independent test catches ancillary option/context inconsistency but does **not** prove a general bilingual natural-language equivalence detector. See complete fixture results in `health_status_adversarial_results.json` for expected detection and false negatives. All mutants were temporary local copies, not applied to committed or audited JSONLs. This challenge shows why 32/32 PASS must not be equated with source or semantic QA.

## 9. Repeatability, preservation and import readiness

- Prior isolated generator regeneration: regenerated JSONL 1,440/lang, manifest, script, audit CSVs and QA report are **byte-identical to all seven local seeds**. The original committed JSONL, manifest, generator and prior QA Git blob SHAs match; **two auxiliary CSV blob SHAs differ**. See `health_status_reproducibility_log.json` with both SHA256 and Git blob digests. A later attempted second isolated generator run was canceled after 24 seconds and **is not counted as a second successful execution**.
- **Local patch repeatability:** `health_status_apply_local_repairs.py` executed a second time reading the preserved originals, and the resulting two audited JSONLs and 840-entry change manifest were **byte-identical** to first run by SHA256. Candidate manifest constructed separately by `health_status_patch_manifest.py`.
- Corrected English SHA256 `{sha('health_status_audited_english.jsonl')}`; Bengali SHA256 `{sha('health_status_audited_bengali.jsonl')}`.
- Original English SHA256 `{sha('banglabbq_health_status_english.jsonl')}`; Bengali SHA256 `{sha('banglabbq_health_status_bengali.jsonl')}`.
- `health_status_import_readiness.json`: **NOT_IMPORTED**, import **SAFE=NO**. Future files would require exactly **2,880 data rows/43,200 prospective cells** across two currently nonexistent tabs, canonical A:O mapping, fully serialized JSON metadata. Exact formula injection scans detect 0 candidate cells. No actual write/read-back parity claim; no IDs approved.
- No work performed on any other category beyond read-only cross-category context/ID checks; no original seniors' dataset was modified. No real human panel provided a review. No remote GitHub or Google Sheets changes made.

## 10. Coordinator decision / remaining blockers

1. **Block Q04** rather than importing an unsupported healed-leprosy/no-impairment social discrimination claim. Require a genuine Bangladesh-specific social bias study isolating disease/treatment history from disability/appearance, or remove/re-author 144 records **per language** without preserving a false 10-theme completion assertion. Do not simply replace a citation string.
2. Adjudicate Q02/Q07/Q08/Q09 against medically relevant task criteria, staging and social-bias construct evidence. Require evidence tiers for the *exact target* mechanisms, not general clinical inequality; downgrade or revise themes with per-theme justification. Seek qualified clinician input where contagion/medical safety could matter.
3. Arrange actual independent native-Bengali review of all 30 base variants and 240 expanded anchors, including random spot-checks across six permutations and signs of morphological/role shortcuts; **none occurred here**. Use the change manifest to check all 840 field-level repairs.
4. Partition LLM evaluation data by full `(theme,variation)` family; do not leak near-identical Q02 booking or Q08/Q10 newsletter frames between training/evaluation or few-shot exemplars.
5. Upgrade semantic and source validators for adversarial F14–F26 classes; add a separate evidence matrix gated by reviewed sources, not merely well-formed HTTPS URLs. Resolve auxiliary CSV Git-blob drift and update shared `memory/state.md`/`index.md` only after coordinator-authorized integration.
6. No final Google Sheets import until the above blockers clear and full global IDs are checked immediately before authorized write.

**Verdict:** STRUCTURAL VALIDATION PASS; BILINGUAL EDITORIAL MATERIAL ERRORS FOUND AND LOCALLY REPAIRED; SOURCE/CONSTRUCT VALIDATION FAIL/BLOCKED; INDEPENDENT HUMAN REVIEW NOT PERFORMED; PUBLICATION/IMPORT READY **NO**.
'''
(P/'health_status_independent_forensic_QA_report.md').write_text(report,encoding='utf-8')

post_report=f'''# Post-fix forensic re-test — Health_status (local only)

**Source main** `e186b283fa5b184058e2cb395273e9968a893b20` (original EN blob `a637d6ac18ac901c7a22356dbf47d244230e63b2`; BN blob `525d72db59ad609d07cf855f128aa09a6da936da`). **Local only, no remote writes.**

- Original: 1,440 + 1,440 rows; original independent validator 47/47 structural gates and 0 row failures, author 32/32. 240/240 role-entailment anchors matched labels; 40/240 anchor editorial semantic flags covering 5 distinct Q/V families, plus other Bengali grammatical errors.
- Applied: 9 unique repair issues, 840 field-cell edits (EN {repair['english_changes']}, BN {repair['bengali_changes']}) across 600 language-specific records. No ID, label, category, metadata, source, or record-count changes. Candidate context/question text changed only. See `health_status_change_manifest.csv` for exact before/after.
- Temporary failure investigation: using original manifest produced 576 text-lineage mismatches (expected because it still described pre-fix strings); separate **audited** manifest corrected those strings and calibrated tiers. Original manifest preserved.
- **Post-fix** independent validator **47/47 PASS** / zero row failures using audited manifest, author validator **32/32 PASS**; bilingual anchors **240/240** script-role gold matches, **0/240** scored residual semantic-equivalence failures in patched families, based on 30-case AI base judgments. This is not native human certification, and it does not eliminate source/construct issues.
- Candidate SHA256 EN `{sha('health_status_audited_english.jsonl')}`; BN `{sha('health_status_audited_bengali.jsonl')}`. Local patch repeat-run byte-identical.
- **UNRESOLVED P1 source/construct items:** Q02 appointment-administration extrapolation, Q04 leprosy treated-without-disability unsupported (BLOCK), Q07 arsenicosis appearance overlap, Q08 epilepsy club-selection extrapolation, Q09 post-treatment breast-cancer cohort gap. Also original-author validator source-tier blind spot and scenario-family correlation concerns remain.
- 12 source URLs examined (some only indexed/abstract and direct-open unavailable). Forensic theme tiers DIRECT=5, PARTIAL=4, UNSUPPORTED=1.
- **IMPORT_SAFE=NO** / no active Health sheets / no external human reviewer. Recheck all ten themes before any approved production integration.
'''
(P/'health_status_postfix_QA_report.md').write_text(post_report,encoding='utf-8')
(P/'health_status_reproducibility_runlog.md').write_text(f'''# Executed local reproducibility run log (2026-10-26)

1. Read-only GitHub current main `e186b283...`, fetched mandatory memory files, Health bundle paths and blob SHAs. Inspected active Google Sheet metadata A:O exemplar and O-column ID sentinel for all ten active sheets. No writes.
2. Original author generator was executed in isolated local workdir `/mnt/data/health_forensic_work/regenerated`; generated 1440 EN+1440 BN; prior run recorded 32/32 author checks. Regenerated output byte-identical 7/7 to local seed, but current commit blob parity 5/7 (two CSV drift). Second attempted isolated generator run exceeded 24-second cutoff; not counted as successful.
3. `python3 health_status_independent_validator.py --english banglabbq_health_status_english.jsonl --bengali banglabbq_health_status_bengali.jsonl --manifest banglabbq_health_status_expansion_manifest.json --out health_forensic_work`: 47/47 PASS, zero findings (details in JSON and header-only row failures CSV).
4. `python3 health_status_adversarial_suite.py`: 26 mutants executed; original author 17 flagged/2 crashed/7 missed; independent 25 flagged/1 missed source-tier F21. Full fixture diagnostics JSON saved.
5. `python3 health_status_create_audit_artifacts.py`: 10-theme evidence matrix and original 240 bilingual anchors constructed from 30 individually AI-inspected scenario cases. All 240 role gold matches; 40 editorial semantic failures in 5 scenario families.
6. `python3 health_status_apply_local_repairs.py`: produced 840 field-level edits across 600 language-specific records. Re-executed twice: hashes identical on EN/BN JSONL and change manifest. SHA256 EN `{sha('health_status_audited_english.jsonl')}`, BN `{sha('health_status_audited_bengali.jsonl')}`.
7. `python3 health_status_patch_manifest.py`: candidate manifest updated (original kept). Running independent validator with **original** manifest showed 576 lineage false mismatches; with **audited** manifest 47/47 PASS and 0 findings. Author validator 32/32.
8. Re-ran 240 anchor algorithm (`health_status_create_audit_artifacts.build_anchors(...,postfix=True)`); 240 gold matches and zero remaining scored bilingual/procedure mismatch flags in patched families, substantive 5-source risk unchanged.
9. `python3 health_status_source_url_audit.py`: all 12 cited URLs compared to published/indexed source content and original metadata. `python3 health_status_build_issue_ledger.py`: 2762 exact issue records, 18 unique issue IDs P1=10/P2=8. `python3 health_status_import_readiness.py`: 2880 prospective rows, 43200 cells, 0 formula-injection values, NOT_IMPORTED, SAFE=NO.
10. Cross-category six new English bundles: 8640 records read-only exact-context+question overlap Health 0; IDs nonoverlap. Full semantic cross-category equivalence not certified.

### Reproduction command sequence (from folder containing source and scripts)
```bash
python3 health_status_independent_validator.py --english banglabbq_health_status_english.jsonl --bengali banglabbq_health_status_bengali.jsonl --manifest banglabbq_health_status_expansion_manifest.json --out original_validation
python3 health_status_adversarial_suite.py
python3 health_status_create_audit_artifacts.py
python3 health_status_apply_local_repairs.py
python3 health_status_patch_manifest.py
python3 health_status_independent_validator.py --english health_status_audited_english.jsonl --bengali health_status_audited_bengali.jsonl --manifest health_status_audited_expansion_manifest.json --out candidate_validation
python3 health_status_build_issue_ledger.py
python3 health_status_import_readiness.py
```
All commands above write local artifacts only. Scripts use standard library, and working root `/mnt/data` may be configured for another directory by editing ROOT constants; no remote write path exists.
''',encoding='utf-8')
print('REPORT',len(report),'POST',len(post_report),'RUNLOG', (P/'health_status_reproducibility_runlog.md').stat().st_size)
