# Health_status forensic audit — READ THIS FIRST

Current GitHub main examined: e186b283fa5b184058e2cb395273e9968a893b20
Health JSONL blob SHAs: EN a637d6ac18ac901c7a22356dbf47d244230e63b2 ; BN 525d72db59ad609d07cf855f128aa09a6da936da

**IMPORTANT: IMPORT_SAFE=NO, PUBLICATION_READY=NO.** All generated files are research candidates, without independent human/clinical adjudication.

Start with report/health_status_independent_forensic_QA_report.md. The full row-level issue ledger and 240 bilingual anchor cases are under evidence/. The locally corrected candidate JSONLs and manifest are under fixes/, alongside the per-field diff manifest. Originals remain unchanged under original_committed_health_jsonl/. The original health source/crosswalk CSV local seeds are NOT byte-identical to current GitHub blob SHAs, so are deliberately separated under local_auxiliary_seed_NOT_GITHUB_BYTE_IDENTICAL/.

Code in scripts/ runs locally using Python 3 standard library; most scripts assume /mnt/data root, edit the ROOT path before using outside that environment.

Main tests: independent validator 47/47; author validator 32/32; 240/240 role-entailment anchors; 26 injected adversarial faults (author flags 17, crashes 2, misses 7; independent automatic detector flags 25/26). Despite this, the Q04 health-only stigma source remains unsupported; Q02/Q07/Q08/Q09 need more precise evidence and expert approval. Do not import the candidate.

This archive was created by automated local code. No GitHub, Google Sheets, or external account was edited.
