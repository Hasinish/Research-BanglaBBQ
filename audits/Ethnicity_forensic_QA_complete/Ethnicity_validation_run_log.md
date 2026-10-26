# Independent Ethnicity QA: reproducible local execution log

**Read-only online sources:** exact live GitHub `main` HEAD `e186b283fa5b184058e2cb395273e9968a893b20`, 2026-10-26, read 5 project memory files, 10 primary and 8 secondary cited entries, latest PakBBQ regional (944 records, 18 themes), live Google Sheets metadata, A:O reference rows, and ten production ID columns. GitHub/Google Sheets were NEVER mutated.

**Original snapshots**: `ORIGINAL/banglabbq_ethnicity_english.jsonl` and `ORIGINAL/banglabbq_ethnicity_bengali.jsonl` identical Git blob SHAs to committed GitHub; immutable within this audit (never overwritten). More original files in ORIGINAL/.

**Commands actually executed and observations**:

```bash
# Prior code runs, executed in LOCAL scratch directories:
python ORIGINAL/validate_ethnicity_independent.py                 # exit 0 on original, but missed contradiction
python repro_run/generate_ethnicity.py --directory repro_run      # exit 0: original EN, BN, manifest, prior QA, source CSV byte-identical
python Ethnicity_independent_validator.py --en ORIGINAL/banglabbq_ethnicity_english.jsonl --bn ORIGINAL/banglabbq_ethnicity_bengali.jsonl --manifest ORIGINAL/banglabbq_ethnicity_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates ORIGINAL/banglabbq_ethnicity_scenario_templates.json --output pre_fixes_independent_results.json  # exit 1, exactly 96 P0 contradictions (EXPECTED)
python apply_justified_local_repairs.py                            # exit 0: 672 cell changes, new audited EN/BN plus manifest/templates
python audited_generation/generate_ethnicity.py --directory audited_generation   # exit 0 (deterministic audited candidates)
python Ethnicity_independent_validator.py --en banglabbq_ethnicity_audited_english.jsonl --bn banglabbq_ethnicity_audited_bengali.jsonl --manifest Ethnicity_audited_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates Ethnicity_audited_scenario_templates.json --output post_fixes_independent_results.json  # exit 0, no independent programmatic issues
# Initial adversarial wrapper timed out, NOT counted as completion.
# Corrected adversarial runner then executed F01..F30 in three 10-fixture batches; F13 and F28 re-executed after fixture definition repairs.
python build_qa_artifacts.py                                      # exit 0, 240 semantic anchors + 10-theme source matrix + granular ledger
python finish_qa_reports.py                                      # exit 0, final tables/reports + additional validator rerun + output hashes
```

For independent code invocation on extracted ZIP (adjust ROOT constants to current directory):

```bash
python Ethnicity_independent_validator.py --en banglabbq_ethnicity_audited_english.jsonl --bn banglabbq_ethnicity_audited_bengali.jsonl --manifest Ethnicity_audited_expansion_manifest.json --source-audit ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates Ethnicity_audited_scenario_templates.json --output independent_results.json
```

**CAUTION:** `Ethnicity_independent_validator.py` covers internal text/label entailment and explicit contradictions. Its clean result does not prove all legal, cultural, source, or clinical equivalence. F26 and F27 show why URL + claim verification remains an external source-review requirement.

## Final rerun commands and results

- `python -m py_compile /mnt/data/ethnicity_forensic/Ethnicity_independent_validator.py /mnt/data/ethnicity_forensic/apply_justified_local_repairs.py /mnt/data/ethnicity_forensic/build_qa_artifacts.py /mnt/data/ethnicity_forensic/run_adversarial_ethnicity.py`: return code **0**; no stderr
- `python /mnt/data/ethnicity_forensic/Ethnicity_independent_validator.py --en /mnt/data/ethnicity_forensic/banglabbq_ethnicity_audited_english.jsonl --bn /mnt/data/ethnicity_forensic/banglabbq_ethnicity_audited_bengali.jsonl --manifest /mnt/data/ethnicity_forensic/Ethnicity_audited_expansion_manifest.json --source-audit /mnt/data/ethnicity_forensic/ORIGINAL/banglabbq_ethnicity_source_audit.csv --templates /mnt/data/ethnicity_forensic/Ethnicity_audited_scenario_templates.json --quiet --output /mnt/data/ethnicity_forensic/postfix_final_rerun_validator_results.json`: return code **0**; no stderr
- `cmp -s /mnt/data/ethnicity_forensic/audited_generation/banglabbq_ethnicity_english.jsonl /mnt/data/ethnicity_forensic/banglabbq_ethnicity_audited_english.jsonl`: return code **0**; byte-identical
- `cmp -s /mnt/data/ethnicity_forensic/audited_generation/banglabbq_ethnicity_bengali.jsonl /mnt/data/ethnicity_forensic/banglabbq_ethnicity_audited_bengali.jsonl`: return code **0**; byte-identical

## Actual source snapshots and basic QA counts

- Original English SHA256: `8c783c202fcacdcaddb841873d68e4a6bba1db72e8867ad41ccaa05ee332f81b`
- Original Bengali SHA256: `db801f8274b804c66457f4a4818d2a7e25ae427ebafe51353aecaa3e7fc8d997`
- Candidate English SHA256: `dd91720d462f1ee51091cdf19cfd9edeff2843fe9dc01adfac886d6082ec6489`
- Candidate Bengali SHA256: `49f4a6a131094f6f7366843111c3c3cb5db44084882bb65b2f5911e7a37a031f`
- Original 96 row-level Q10 P0 flags; candidate 0 structural/textual flags; prior existing validator PASS.
- Semantic anchors 240/240, source entries 18/18, adversarial executed 30/30, programmatic detection 28/30 (old 26/30).
- No Ethnicity sheet exists; no remote writes or global ID-range final approval.
