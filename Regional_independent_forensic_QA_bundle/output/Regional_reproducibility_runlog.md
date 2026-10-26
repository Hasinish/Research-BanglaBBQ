# Executed offline reproduction log — Regional, 2026-10-26

The following command families were actually executed in the local container; exact paths refer to the included zip structure or audit working directory. Outputs and SHA comparisons are summarized below. Scripts never call remote write APIs.

## 1. Verify immutable original Git blobs

```bash
git hash-object original/banglabbq_regional_english.jsonl
git hash-object original/banglabbq_regional_bengali.jsonl
sha256sum original/banglabbq_regional_english.jsonl original/banglabbq_regional_bengali.jsonl
```

**Observed Git blob SHAs:** `081ad561c9671e7eb3b68bdf706bc95e1aef1a5e` and `6c8ca8a8e4a511fb1315e96dc3e5395825cf6035`; byte hashes as recorded in reports.

## 2. Replay creator generator (executed)

```bash
python3 original/banglabbq_regional_generator.py --outdir work/regenerate
python3 original/banglabbq_regional_independent_qa.py --outdir /mnt/data
```

Generator **20/20 PASS**, old checker **13/13 PASS** on originals. Ran `cmp -s` on generated EN/BN JSONL, manifest, templates, audit CSV, crosswalk, screening; all byte-matched original copies. Machine-specific pathname in generated QA report was excluded from identity comparison.

## 3. Independent checker on original and audited data (executed)

```bash
python3 output/Regional_independent_validator.py --english original/banglabbq_regional_english.jsonl --bengali original/banglabbq_regional_bengali.jsonl --manifest original/banglabbq_regional_expansion_manifest.json --source-audit original/banglabbq_regional_source_audit.csv --output-json output/Regional_original_independent_check_results.json
python3 output/Regional_independent_validator.py --english output/banglabbq_regional_audited_english.jsonl --bengali output/banglabbq_regional_audited_bengali.jsonl --manifest original/banglabbq_regional_expansion_manifest.json --source-audit original/banglabbq_regional_source_audit.csv --output-json output/Regional_audited_independent_check_results.json
```

**Observed:** 0 detected independent automated issues in each, 240 paired anchors in each. Test coverage excludes arbitrary natural-language entailment and human cultural certification. During improving the checker a first version of a Bengali "equally complete" heuristic created **48 false positives** for idiomatic "সমানভাবে দেওয়া হয়েছে" in Q04 V3; the equivalence mapping was repaired and re-run, leaving **0 baseline false positives**. This is documented to avoid overclaiming validator generality.

## 4. Local repairs and independent replay (executed)

```bash
python3 output/Regional_local_patch.py --input-dir original --outdir output
python3 output/Regional_local_patch.py --input-dir original --outdir work/patch_replay
cmp -s output/banglabbq_regional_audited_english.jsonl work/patch_replay/banglabbq_regional_audited_english.jsonl
cmp -s output/banglabbq_regional_audited_bengali.jsonl work/patch_replay/banglabbq_regional_audited_bengali.jsonl
cmp -s output/Regional_change_manifest.csv work/patch_replay/Regional_change_manifest.csv
cmp -s output/Regional_template_edit_manifest.json work/patch_replay/Regional_template_edit_manifest.json
cmp -s output/Regional_audited_scenario_templates.json work/patch_replay/Regional_audited_scenario_templates.json
```

**Observed:** five/five files byte-identical after replay. Exact counts 19 template edits, 480 changed cells, 348 affected language-specific rows.

## 5. Executed adversarial tests, including post-fix rerun

```bash
python3 output/Regional_adversarial_suite.py
python3 output/Regional_adversarial_suite_on_audited.py
```

The first script was executed first against unmodified original committed copies with independent validator v1 (26/28 specific); then again with the enhanced checker (28/28 specific). The previously bundled checker had 21/28 specific detections, 6 generic SHA-only, one unstructured crash/error. The second script was executed against locally corrected candidate files: 28/28 known fixtures specifically detected using the enhanced independent checker. Mutation directories were ephemeral and discarded after every run.

## 6. Live read-only collision scan

Google Sheets metadata and exact O1:Olast ranges were read through the connected Google Drive API for 10 active production tabs (ENG+BEN for Age, Politics, Religion, Gender and Education). **32,512 ID values inspected; zero within 8,400,000..8,401,439.** No hidden tab, write request, or Regional sheet was involved.

## 7. All 9 distinct citation URLs checked

Webpage title/author/date/access levels and passage-level paraphrases are in `Regional_source_access_log.csv`. All 9 returned readable article content. These checks do not prove independent prevalence estimates, and source-critical Q06/Q08/Q09/Q10 remain blocked.

## 8. Integrity and limitations

- Historical 51/51-row BRAC legacy untouched.
- GitHub and Google Sheets untouched.
- New scripts run Python standard library only.
- AI reviewer is not independent from initial authorship and is not a human native-language certifier.
- Original 10-theme structure and per-category provisional IDs retained; **production import not performed**.
