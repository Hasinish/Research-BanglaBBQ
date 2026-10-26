#!/usr/bin/env python3
import csv,json,pathlib,hashlib,collections
R=pathlib.Path(__file__).resolve().parents[1]
L=lambda path:json.loads((R/path).read_text())
q=L('physical_appearance_quantitative_results.json');src=list(csv.DictReader((R/'physical_appearance_source_evidence_matrix.csv').open()));issues=L('work/issue_summary.json');orig=L('original_validation.json');post=L('postfix_validation.json');adv=L('physical_appearance_adversarial_results.json');adp=L('physical_appearance_adversarial_postfix_results.json');rep=L('local_repair_summary.json');import_gate=L('physical_appearance_import_readiness.json')
assert orig['finding_total']==288 and post['finding_total']==0 and adv['summary']['independent_expected_detection_success']==26
rows=[]
for s in src:
  tier='DIRECT (abstract only)' if s['theme']=='Q02' else s['independent_evidence_tier']
  rows.append(f"| {s['theme']} | {s['original_theme_title']} | {tier} | {s['decision']} |")
rows='\n'.join(rows)
source_detail=[]
for s in src:
  urls=f"[primary]({s['primary_url']})" + (f", [secondary]({s['secondary_url']})" if s['secondary_url'] else '')
  source_detail.append(f"**{s['theme']} ({s['original_theme_title']}).** {urls}. Access: {s['primary_access']}{('/ '+s['secondary_access']) if s['secondary_url'] else ''}; observed: {s['actual_verified_claim']} Evidence boundary: {s['unverified_extrapolation_and_confounders']}")
source_detail='\n\n'.join(source_detail)
report=f'''# BanglaBBQ Physical Appearance — Independent forensic QA of committed bilingual JSONL

**Audit date:** 26 October 2026 (Asia/Dhaka)  
**Category scope:** `Physical_appearance` **ONLY**.  
**GitHub `main` head audited:** `{q['audited_commit']}` (committed 2026-10-26 06:18:04 UTC); the seven-category push is the immediately preceding `214795f628a34ece8deb23a65c6bf35ac0ce7157`.  
**Policy:** No GitHub, Google Sheets or third-party writes. Local artifacts only.  
**Review provenance:** `AI_SELF_REVIEW`; **independent human/native-speaker review: NOT_PERFORMED**.

## 1. Precise audited material and byte provenance

| Version | Repository path / bytes | Git blob SHA | SHA-256 |
|---|---|---|---|
| Committed EN | `banglabbq_physical_appearance_readonly_research_bundle/banglabbq_physical_appearance_english.jsonl` (1,307,874 bytes) | `{q['english_original_git_blob']}` | `{orig['sha256_english']}` |
| Committed BN | `banglabbq_physical_appearance_readonly_research_bundle/banglabbq_physical_appearance_bengali.jsonl` (2,167,074 bytes) | `{q['bengali_original_git_blob']}` | `{orig['sha256_bengali']}` |
| Local corrected EN (unchanged bytes) | `banglabbq_physical_appearance_audited_english.jsonl` | `{post['github_blob_english']}` | `{post['sha256_english']}` |
| Local corrected BN (not committed) | `banglabbq_physical_appearance_audited_bengali.jsonl` | `{post['github_blob_bengali']}` (calculated locally, **not a repository commit**) | `{post['sha256_bengali']}` |

The committed JSONL, generator, manifest and prior QA-report hashes were independently matched to local input snapshots. Separate source-audit and crosswalk CSV copies from the prior chat are **NOT byte-identical** to the latest GitHub blobs. The **current committed versions were inspected via the connected GitHub reader**: source-audit blob `188c9d30faed8060686c3aa7a6526ab93577bd0f` (10 themes); PakBBQ crosswalk blob `41c2eec0c6d94e58050c7b976f6514a8a46b28db` (23 upstream rows plus 10 local). The saved `ORIGINAL/` source CSVs are **earlier local copies, not verified Git-exact snapshots**; unlike the JSONLs, they must not be represented as authoritative byte-exact Git exports. The independent evidence matrix supersedes their unsupported tier assertions but does not alter GitHub.

The previously claimed clean QA report was treated as an untrusted baseline claim, not independent validation. The immutable local source JSONLs were not changed.

## 2. Summary of tests actually run

| Test group | Original status | Local candidate status | Tested denominator / precise finding |
|---|---|---|---|
| UTF-8 JSONL, 15 keys/types/enums and answer-info roles | PASS | PASS | 2,880/2,880 records; no parse/UTF-8/schema failures |
| Counts, four-condition order, six permutations | PASS | PASS | 10 × 3 × 48 per language; 360 four-row permutation blocks/language, 720 total |
| Example/global IDs | PASS within local category | PASS provisional | 2,880 IDs and counterfactual mappings; EN/BN agree, `example_id` 0–1439, reserved `id` 8,100,000–8,101,439 |
| Answer-option identity, role/tag and gold position | PASS | PASS | 2,880 option triples; label indices each 480 per language; no repeated full QA tuple |
| Explicit context-driven blind gold inference | PASS for implemented pattern | PASS for implemented pattern | All 2,880 rows plus 240 unique condition/polarity/orientation bilingual anchors (not a human judgment) |
| Bilingual structural/parity and assessed meaning | **FAIL** | PASS for coded concepts | Original 288 Bengali records had Q06/Q09 meaning shifts; 0 coded meaning failures after local repair |
| English/Bengali AI editorial | **FAIL/PARTIAL** | PARTIAL | 240 paired anchors; 48 original anchor meaning FAILs; 0 coded meaning FAILs locally. 8 candidate anchors (Q03 V1) still score 3/5 Bengali naturalness |
| Counterfactual property/qualification preservation | PASS for fixed scenario templates | PASS for implemented checks | All 60 oriented scenario pairs (30 variants × a/b); appearance descriptions swap while qualifications/outcome referents remain fixed |
| Source/theme evidence for precise stereotype | **FAIL** | **BLOCKED** | All 10 themes/12 unique cited URLs examined; 4 qualified DIRECT, 6 PARTIAL/CONTEXTUAL; full Q02 scholarly text not accessible |
| Scientific distinctiveness / split leakage | PARTIAL | PARTIAL | 30 setting/action variants, but **all 10 families** reuse one judgment predicate and the same opposed evaluator-action structure; record-level split leaks correlated variants |
| Genre/cultural/category boundary | PARTIAL | **BLOCKED** | 30 scenario variants reviewed; Q02 visual casting role relevance, Q07 potential appearance policy, Q08 tattoo/religion overlap, Q10 acne/health overlap |
| Upstream PakBBQ Physical Appearance inventory | PASS | PASS | HEAD `c079dbae2d676f4e3bb82982144d6d4ac10436d4`; 1,368 JSONL records, 23 actual indices, all represented in crosswalk |
| Original generator reproduced in two temp directories | PASS | N/A | 2 executions; 5 output file types matched the prior local snapshots bytewise; committed JSONL blob identity separately checked |
| Existing project generator validator | **MISSED SEMANTIC ERRORS** | PASS coded | 0 issues on original despite 288 BN shifts; 0 issues on corrected candidate |
| Independent checker | **FAIL** | PASS on implemented rules | 288 original independent findings vs 0 locally; logs preserve exact IDs/conditions |
| Adversarial fault injection | PARTIAL original | PASS independent | 26 genuinely mutated fixtures × two stages; independent 26/26 detected at both stages; old validator flags 21/26 in some form |
| Master Sheet import/read-back | **NOT_IMPORTED** | **NOT_IMPORTED / BLOCKED** | 37 live tabs inspected; no Physical Appearance working pair; no remote writes, no fictitious live parity claim |
| Independent human/native Bangla review | **NOT PERFORMED** | **NOT PERFORMED** | 0 actual human reviews |

Quantitative per-language checks: **1,440** records, **10** distinct `question_index`, **144** per theme, **48** per scenario variation, **720** `a` and **720** `b`, **720** ambiguous and **720** disambiguated, **720** negative and **720** nonnegative; four condition/polarity cells each **360**; labels positions 0/1/2 each **480**; **1,440** unique complete QA tuples. Both languages have only **120 distinct context texts** and **60 distinct question texts** before answer permutations, an expected consequence of the 2×2×6 expansion but a serious train/test-split design consideration.

## 3. Issue ledger scope, severity and exact counting semantics

**Every field-level local edit and every outstanding conceptual issue is logged** in `physical_appearance_issue_ledger.csv`. Severity follows the **uploaded prompt**, rather than the earlier self-review labels: systematically wrong bilingual stereotype predicates qualify as **P0**.

| Priority | Ledger entries | What this actually counts |
|---|---:|---|
| **P0** | **432** | 216 changed BN fields in Q06 and 216 in Q09; **288 distinct affected records** (not 432 separate independent case types); all repaired LOCALLY |
| **P1** | **12** | Ten construct/evidence/tier root issues plus independent Q02 full-text blocker and related theme-level decisions; not repaired by a spelling fix |
| **P2** | **634** | 576 local wording-field improvements (Q02/Q08/Q10), 48 Q03 V1 Bengali unresolved record-specific wording issues, 10 correlated-paraphrase / leakage family issues |
| **P3** | **0** | No trivial-only stand-alone issues added to inflate issue counts |
| **TOTAL** | **1,078** | **1,008 field changes applied locally; 58 blocked; 12 unresolved.** These counts are *ledger rows*, not distinct research hypotheses or deduplicated events. |

### Highest-priority reproducible examples

1. **P0, Q06, EID 240 / JSONL line 241** (also V2 EIDs 720–767, V3 1200–1247): original Bengali question `পরিপাটি উপস্থাপনার যোগ্যতা` asks about *ability*, while English asks about *neat presentation style*. The new Bengali question is about `উপস্থাপনার পরিপাট্য`. Original question changes across 144 BN records and matching disambiguated contexts in 72 BN records.
2. **P0, Q09, EID 384 / JSONL line 385** (V2 864–911, V3 1344–1391): original Bengali asks `দায়িত্বের প্রতি মনোযোগী থাকার সক্ষমতা` (*capacity to stay attentive*), while English concerns *commitment to assignment*. Locally replaced with `অর্পিত কাজের প্রতি নিষ্ঠা`; 144 BN questions + 72 disambiguated contexts corrected.
3. **P1, Q02, EIDs 48–95, 528–575, 1008–1055:** fashion/model glamour can be a **legitimate visual casting criterion** for some acting/advertising roles. A matched acting score does not establish that appearance is irrelevant to the fictional role. Theme requires role-criteria control or redesign; cited scholarly paper available here only as indexed abstract.
4. **P1, Q03, EIDs 96–143, 576–623, 1056–1103:** Bangladesh-specific *weight taunting* is not evidence of a stereotype that larger-bodied volunteers are less reliable when performing assigned work. BLOCKED for source/construct adjudication.
5. **P1, Q05, EIDs 192–239, 672–719, 1152–1199:** reports of height-related shaming do not verify judgments of public-speaking ability; a multi-country beauty-esteem study cannot be treated as a Bangladesh height experiment.
6. **P1, Q08, EIDs 336–383, 816–863, 1296–1343:** visible tattoo stigma in a Bangladeshi workplace does not substantiate lack of professional trustworthiness or confidentiality; original `DIRECT` evidence tier must become `PARTIAL`.
7. **P1, Q10, EIDs 432–479, 912–959, 1392–1439:** university students' acne-associated self-reported appearance anxiety is not proof of external judges' confidence judgments; **Health Status/Physical Appearance category boundary** requires human disciplinary ruling.
8. **P2, Q03 V1, EIDs 96–143, e.g. line 97:** `পরীক্ষামূলক দুটি মজুত-তালিকার পালা` is awkward Bengali for “two trial inventory shifts”. A proposed translation is recorded, **not applied**, because the original generator/manifest setting must be revised coherently, with approval.
9. **P2, Q08 V1, EID 336 / line 337:** `হাতের নিচের অংশে` is imprecise for EN “forearm”. Local text now uses `কনুই ও কবজির মাঝের অংশে` with the same appearance comparison and identity tags.
10. **P2, Q02 V1, EID 48 / line 49:** Bengali `অভিনয় বা উপস্থাপনায় উপযুক্ততা` is unnatural and weakly specified for EN “performance suitability”; local phrase `পরিবেশনার উপযুক্ততা` is more idiomatic, but Q02's role-relevance **P1 blocker remains**.

## 4. Independent source reopening and calibrations

**Evidence count:** **4 DIRECT** (Q01/Q02/Q07/Q09, all qualified), **6 PARTIAL/CONTEXTUAL** (Q03/Q04/Q05/Q06/Q08/Q10), **0 UNSUPPORTED as absence of any contextual material** and **0 wholly inaccessible themes**. *This does not mean any of the ten fictional incidents happened or each tested association was directly demonstrated.* For Q02 specifically, primary and secondary PMC/PubMed article endpoints challenged full-text access, while the scholarly abstract was retrieved from indexing; `DIRECT` covers the claim at **abstract level only**, with full-text source validation still pending. All **12 distinct source URLs** were attempted; 10 returned usable source text and two Q02 endpoints were verified only at the abstract/index level. Specific source findings, titles, dates, access statuses and evidence limits are in the evidence matrix.

| Theme | Bias mechanism | Independent evidence tier | Disposition |
|---|---|---|---|
{rows}

Two material downgrades from original source audit: **Q06 DIRECT→PARTIAL** because the article concerns curly hair described as unattractive/unmanageable, not a direct professional-neatness comparison; **Q08 DIRECT→PARTIAL** because tattoo stigma is documented but no adjudication of confidentiality or honesty is shown. Q03–Q05/Q10 already had PARTIAL labels; these do **not** provide theme-level publication clearance.

### Verified source-specific observations (source evidence is not proof of fictional QA incidents)

{source_detail}

No generalized measured discrimination rate, legal restriction, clinical judgment, or fictional hiring outcome has been fabricated from these sources. Contradictory-evidence searches were **limited and non-exhaustive**; absence of located contradictions must not be interpreted as confirmed consensus. Q01 qualitative observations, Q07 first-person experience, Q09 workplace anecdote and Q02 nonprobability qualitative samples do not establish national prevalence or a controlled causal effect. The apparent fit of Q08 tattoos to professional ethics may be confounded by unwritten appearance policy and religious objections. Q10 clinical acne must not be used as an unsupported proxy for mental health or capacity.

## 5. Independent bilingual, cultural and semantic review

`physical_appearance_semantic_anchor_review.csv` contains **240 actual rows**: 30 authored scenarios × 2 orientations × 4 condition/polarity combinations. Each includes the original *and* locally corrected bilingual context/question, option texts, role tags, **answer independently inferred without consulting gold label** by a separate explicit-predicate evaluator, asserted gold, exact contextual evidence, semantic-equivalence status, AI naturalness scores, Bangladesh setting score, identity-respect verdict, source tier, counterfactual status and a **variation-specific note**. Six answer permutations of each unique anchor were mechanically rechecked against the complete **2,880 records**. The evaluation is a **bounded AI_SELF_REVIEW plus deterministic logic tests**, *not* external independent human semantic verification.

- Original meaning discrepancies affected **48/240 bilingual anchor rows**; coded meaning discrepancies resolved to **0/240** in local candidates.
- Original Bengali naturalness <=3/5 in **128/240** anchors due to Q02/Q06/Q08/Q09/Q10 wording and Q03 V1. Local candidate still has **8/240** <=3/5 (Q03 V1), not hidden or marked publication-ready.
- Directly entailed negative/positive in disambiguated text: evaluator *questioned* one named person and *praised* the other for the **same criterion**. Ambiguous contexts contain matched performances and appearance differences, but **no evaluator outcome**, so neither identity can legitimately answer.
- Counterfactual `a`/`b` changes only the tagged visible appearance attribute across the two named people; exact worked evaluations and qualifications stay the same, so the group assigned to a negative evaluator judgment reverses. The asymmetry of *named* actors is intentional and not a gold-label reversal.
- Natural Bangladeshi place names, institutions and role contexts are generally plausible, but all questions recycle the identical *questioned/praised suitability* frame, limiting ecological validity. Split by **entire thematic family**, not records/answer permutations, when running later LLM experiments.
- Human adjudication and independent bilingual native-speaker sign-off: **NOT PERFORMED**.

## 6. Crosswalk, construct isolation, historical provenance

- Actual upstream PakBBQ Physical Appearance path: `PakBBQ/PakBBQ_ENG/Physical_appearance.jsonl` at `c079dbae2d676f4e3bb82982144d6d4ac10436d4`; **1,368** valid records across 23 distinct `question_index` values. The 23-row upstream crosswalk was compared to this actual inventory. PakBBQ is **not** Bangladesh stereotype evidence.
- The new category reuses methods, not original PakBBQ language. No copied Karachi/Lahore location in final records. Ten themes represent colourism, casting glamour, large-body responsibility, thin-body spokesperson credibility, height/speaking, curly-hair neatness, dyed-hair workplace presentation, tattoos/trust, makeup/dedication, facial acne/confidence. These are ten *candidate propositions*, **not ten equally source-verified mechanisms**.
- Legacy BRAC University thesis originals remain untouched: EN **1,106** valid nonblank records, Bengali **1,123**. Fresh GitHub blob-read audit reproduces **20 Bengali duplicate example IDs (842–861), absent Bengali IDs 557–559, and 59 shared-ID gold-label differences**. The 17-row count difference is 20 − 3; blank lines are not JSON corruption. These originals and the new expansion are not the same ID lineage; a full one-to-one legacy replacement/retention map has **not** been made. Publication integration must preserve this distinction.
- The original thesis Physical Appearance category exists. The new ten-theme extension therefore **does not replace the legacy baseline byte-for-byte**; it is a provisional alternative set requiring approval, historical traceability, and reconciliation.
- Cross-category checks: body size stays visual unless a true physical ability requirement enters; Q02 may be role-relevant rather than illegitimate appearance bias; Q07 hair dye may engage documented dress policies; Q08 tattoos can invoke religious/dress expectations; Q10 acne intersects medical health. All are explicitly logged; none silently folded into a different category.

## 7. Reproducibility, adversarial robustness and validator loopholes

`generator_reproducibility.json` records two **real** separate temporary-directory executions of the committed generator with zero execution errors; outputs matched the earlier byte-snapshotted generated data. The present audit independently confirmed committed English and Bengali **Git blob hashes** and SHA-256. `physical_appearance_reproducibility_run_log.json` records exact validations, two post-fix local repair reruns, and **identical SHA-256** of the corrected English/Bengali JSONLs and change manifest on both runs.

Fault-injection suite results: **26/26 intended injected conditions detected by independent checks on the original** and **26/26 detected on the local corrected candidate**. All fixtures were real mutations: JSONL structure, labels, answer roles, source URL, counterfactual qualifications, Bengali meaning, geography, CSV formula injection, and one in-memory deliberately overclaimed source-audit CSV. The old generator caught **21/26 in some form**, and missed:

- `F17`: two answer strings identical despite distinct tags.
- `F20`: one Bengali name/role text substitution creating an option collision.
- `F24`: spreadsheet formula-injection answer starting with `=HYPERLINK(...)`.
- `F25`: overrating unsupported Q03 source evidence to `DIRECT` in an actually mutated copy of source CSV (the generator never reads source audit).
- `F26`: coordinated Bengali-only shift from matched assessments to different assessments across Q01 V1 (not detected by original generator's shallow translation matcher).

**Important precision:** 26/26 is coverage for **the deliberately selected fixtures**, not a guarantee that every adversarial paraphrase or unknown semantic error would be detected. The independent test suite's rules are explicitly surfaced in its script; one regex-only reviewer cannot replace blind social-science/linguistic adjudication.

## 8. Local corrections and immutable comparison

- Corrected **720 of 1,440 Bengali candidate records** across Q02, Q06, Q08, Q09, Q10, comprising **1,008 altered `context`/`question` fields**.
- Q06/Q09 were P0 meaning alignments; Q02/Q08/Q10 were P2 naturalness/precision repairs. All corrections are traceable, by exact EID/line/orientation/field/before/after, in `physical_appearance_change_manifest.csv`.
- Candidate **English is byte-for-byte identical** to committed original; no candidate metadata, ID, gold label, source URL, answer options or answer_info group roles were changed. Source-related claims were **not** deceptively cured by merely updating citations.
- Independent post-fix validator: **0 implemented-rule failures** across 2,880 rows + 240 anchors + 720 permutation blocks + 1,440 bilingual pairs. Original generator's own validator also returns **0** on the candidates. **This is a structural/lexical QA PASS, not scientific source validation.**
- Q03 V1 Bengali `মজুত-তালিকার পালা` remains a documented unresolved P2 because a coordinated generator/manifest update requires explicit adjudication. Existing `ORIGINAL` files are not overwritten.

## 9. Import / publication decision

**SAFE TO IMPORT: NO. PUBLICATION READY: NO. HUMAN REVIEW: NO.** Current master Sheets has no Physical Appearance production pair; original and candidate files have **NOT_IMPORTED** status. All six other new category bundles were read-only scanned (12 JSONLs × 1,440 rows, no collisions within Appearance's reserved range), and current active Google Sheets ID columns were prefix-scanned with no new-range collisions. No exhaustive scan of hidden backups and every legacy ID path was performed; IDs stay **PROVISIONAL**. A:O Sheets column order is: `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`. This differs from canonical JSONL field order. Convert `answer_info` and `additional_metadata` to JSON strings only during an **authorized future** import. Never infer or assert live cell parity for absent tabs.

**Memory discrepancy:** latest `memory/state.md` still displays Physical Appearance as legacy-only `PENDING`; `memory/index.md` does not index the seven new bundle paths although `main` contains them. A later authorized coordinator should synchronize memory with the actual committed evidence (and preserve all research-quality caveats); this read-only worker **must not update it**.

### Priority hand-off to the eighth independent QA coordinator

1. **Reject immediate sheet import.** Send Q02/Q03/Q04/Q05/Q06/Q07/Q08/Q10 exact source-premise comparisons to an independent Bangladesh-focused social scientist; re-scope/re-source/reject weak candidates rather than padding ten.
2. Obtain independent native Bangla editor evaluation of all 30 scenario variants including the Q03 V1 phrase and Q02 role-specific terms; log adjudicator identity/consent separately outside this AI record.
3. Decide whether to integrate or quarantine each theme relative to the seniors' original category, maintaining a full legacy EID lineage map and no overwriting.
4. Once approved, regenerate from an updated scenario/manifest and re-run this **independent** validator and all 26 mutation fixtures; conduct full global ID & live Sheet crosswalk before any import.
5. Only after user-authorized modifications, synchronize versioned GitHub exports, live sheets and project memory; mark published only after external review and evaluation-leakage protections.
'''
(R/'physical_appearance_independent_forensic_QA_report.md').write_text(report,encoding='utf8')
postmd=f'''# Physical Appearance — Post-local-fix QA statement

Audited upstream main: `{q['audited_commit']}`. This is a **local candidate**, **not** a GitHub or Google Sheets update.

**Original JSONL:** 1,440 EN + 1,440 BN records. **Locally corrected:** 1,440 EN + 1,440 BN records. English byte-identical to source; Bengali changed in **{rep['records_modified']} unique records**, **{rep['field_changes']} fields**, all of them contexts/questions and none of them source metadata/labels/IDs.

**Original independent diagnostic:** {orig['finding_total']} P0 bilingual meaning findings, spread over Q06 and Q09. **Candidate independent diagnostic:** {post['finding_total']} implemented structural/semantic discrepancies across 2,880 per-row blind-gold checks and 240 bilingual anchor checks. Original generator validator returns 0 on candidate. **26/26 selected mutation types** still caught by independent adversarial suite on candidate.

**Remaining block:** source-premise mismatch and confounds (especially Q02/Q03/Q04/Q05/Q06/Q07/Q08/Q10), incomplete Q02 article full-text access, 10 correlated paraphrase families, Q03 V1 Bengali naturalness and no external human evaluation. **Not publication ready; SAFE_TO_IMPORT = false.**

**SHA-256 EN:** `{post['sha256_english']}`  
**SHA-256 BN:** `{post['sha256_bengali']}`

Always interpret full findings together with `physical_appearance_issue_ledger.csv`, `physical_appearance_source_evidence_matrix.csv`, the 240-anchor review and the unmodified committed snapshots.
'''
(R/'physical_appearance_postfix_QA_report.md').write_text(postmd,encoding='utf8')
print('created report bytes',len(report.encode('utf8')),'postfix',len(postmd.encode('utf8')))
