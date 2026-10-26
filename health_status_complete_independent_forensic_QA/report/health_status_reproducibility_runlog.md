# Executed local reproducibility run log (2026-10-26)

1. Read-only GitHub current main `e186b283...`, fetched mandatory memory files, Health bundle paths and blob SHAs. Inspected active Google Sheet metadata A:O exemplar and O-column ID sentinel for all ten active sheets. No writes.
2. Original author generator was executed in isolated local workdir `/mnt/data/health_forensic_work/regenerated`; generated 1440 EN+1440 BN; prior run recorded 32/32 author checks. Regenerated output byte-identical 7/7 to local seed, but current commit blob parity 5/7 (two CSV drift). Second attempted isolated generator run exceeded 24-second cutoff; not counted as successful.
3. `python3 health_status_independent_validator.py --english banglabbq_health_status_english.jsonl --bengali banglabbq_health_status_bengali.jsonl --manifest banglabbq_health_status_expansion_manifest.json --out health_forensic_work`: 47/47 PASS, zero findings (details in JSON and header-only row failures CSV).
4. `python3 health_status_adversarial_suite.py`: 26 mutants executed; original author 17 flagged/2 crashed/7 missed; independent 25 flagged/1 missed source-tier F21. Full fixture diagnostics JSON saved.
5. `python3 health_status_create_audit_artifacts.py`: 10-theme evidence matrix and original 240 bilingual anchors constructed from 30 individually AI-inspected scenario cases. All 240 role gold matches; 40 editorial semantic failures in 5 scenario families.
6. `python3 health_status_apply_local_repairs.py`: produced 840 field-level edits across 600 language-specific records. Re-executed twice: hashes identical on EN/BN JSONL and change manifest. SHA256 EN `db0d3daea69d2d088e2aeb7a7c624f039c804478ca3af308a7d7f8191ea93eae`, BN `0d506d37dc58b50f663df0a054a502c390324d8e4e04cb4dab7d980ce28b3c90`.
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
