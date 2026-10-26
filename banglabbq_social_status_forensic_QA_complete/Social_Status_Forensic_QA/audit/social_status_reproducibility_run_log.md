# Social Status Read-only Forensic QA: Reproducibility and Execution Log

## Provenance
- Committed `main`: `e186b283fa5b184058e2cb395273e9968a893b20`; data commit `214795f628a34ece8deb23a65c6bf35ac0ce7157`.
- GitHub connector fetched files and checked 7 Git blob hashes; `fetch_blob` used when large path content was empty.
- Local original files preserved in `original/`. No external write actions.

## Steps actually run
```sh
python /mnt/data/banglabbq_social_status_generate.py --out /mnt/data/social_status_forensic/regenerated
python /mnt/data/social_status_forensic/audit/social_status_independent_validator.py --english /mnt/data/social_status_forensic/original/banglabbq_social_status_english.jsonl --bengali /mnt/data/social_status_forensic/original/banglabbq_social_status_bengali.jsonl --report /mnt/data/social_status_forensic/audit/pre_original_independent_results.json
python /mnt/data/social_status_forensic/audit/build_forensic_outputs.py
python /mnt/data/social_status_forensic/audit/social_status_independent_validator.py --english /mnt/data/social_status_forensic/candidate/banglabbq_social_status_audited_english.jsonl --bengali /mnt/data/social_status_forensic/candidate/banglabbq_social_status_audited_bengali.jsonl --report /mnt/data/social_status_forensic/audit/post_candidate_independent_results.json
python /mnt/data/social_status_forensic/audit/social_status_adversarial_fault_injection.py
python /mnt/data/social_status_forensic/audit/write_final_reports.py
```
- Original generator stdout: `original_generator_run.log` shows **19/19** checks passed.
- Regenerated original EN/BEN and audit/crosswalk/manifest/QA were bit-for-bit equal to originals.
- Independent baseline / candidate issue totals: `0` / `0` (machine-readable reports kept).
- Original generator validator re-run on revised candidate manifest: **19/19 PASS**.
- Adversarial fixtures: **33 executed**, original flagged 23; independent flagged 28; neither flagged 5.
- Confirmed 35 PakBBQ SES themes and 5,384 rows via authenticated Git blob SHA `93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe` (not via empty path response).
- Current live master metadata shows no Social Status tab. Active-sheet ID scan: 32,512 IDs in 10 tabs, 0 collisions; six extra new-category English files 8,640 IDs, 0 collisions; hidden archives not fully checked.

## Validator loopholes
- Original validator may throw rather than return a clean failure on malformed nested data or bool index.
- Original validator does not inspect EN/BN semantic *meaning*, beyond superficial script and role parity.
- New independent validator catches class-swap, named entity and malformed role issues, **but does not establish evidence quality, full natural-language entailment or translation equivalence**.
- A valid HTTPS URL for a wholly unrelated source can pass both validators: the evidence matrix needs human review and/or source allowlist/relevance verification.
- Some semantic mutations are flagged only due to incidental mismatch across orientation or question order; the 240-anchor editorial audit is a separate scientific gate.

## Environment, limits
- Uses Python standard library in local container, no write to any external systems.
- No human annotator was consulted. `AI_SELF_REVIEW`, **not independently adjudicated**.
- Source opens included publisher article/PubMed/J-PAL/BRAC BIGD and indexed abstracts; one direct BIGD link and a PDF screenshot request failed, recorded as source-access limits.

## Additional verified commands and outputs
```sh
python /mnt/data/social_status_forensic/audit/enrich_upstream_crosswalk.py
python /mnt/data/social_status_forensic/audit/enrich_editorial_review.py
python /mnt/data/social_status_forensic/audit/social_status_apply_local_fixes.py --original-dir /mnt/data/social_status_forensic/original --changes /mnt/data/social_status_forensic/audit/social_status_change_manifest.csv --out /mnt/data/social_status_forensic/repatched --expected-out-sha-json /mnt/data/social_status_forensic/audit/social_status_snapshot_integrity.json
python /mnt/data/social_status_forensic/audit/finalize_audit_package.py
```
- Crosswalk exact source URL presence: 864 uncited records in indices 26-32; `enrich_upstream_crosswalk.py` uses per-index aggregates calculated by connected upstream Git blob parser rather than silently inventing evidence.
- Candidate patch script successfully verified exact output hashes in `candidate_reconstruction_run.log`.
- Source and semantic review gaps remain explicitly open despite machine checks passing.
