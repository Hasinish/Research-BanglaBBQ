# BanglaBBQ Social Status: Post-fix Candidate Forensic QA

- **Current upstream main:** `e186b283fa5b184058e2cb395273e9968a893b20`. Originals intact; all 7 SHA1 Git blob matches verified.
- **Candidate:** EN 1,440, BN 1,440; local candidate SHA256 EN `cf37a71ed4c0ef4f81c12fac9d2b83993d3a34a09609d2b50c2ecb9fd7959cea`, BN `a65466ea984220951ae393d48b5d7c1cd413089f937cfe66a245e2dc100fc3f2`.
- **Field-level edits:** EN=120, BN=120, total=240. Q07 V3 semantic polarity text harmonized (48 records/language, questions and disambiguated contexts), Q04 V1 EN document wording (48 fields), Q10 V1 BN volunteer-work phrase (48 fields).
- **Post-fix independent structural validation:** `0` issues over 2,880 rows; full 6-way blocks, balanced labels and bilingual metadata unchanged.
- **Post-fix original generator's validator (re-run using revised candidate manifest):** 19/19 checks pass, 0 failed.
- **Post-fix semantic anchor audit:** 240/240 human-readable bilingual anchor rows included; role/explicit-action inference matches labels 240/240. Source/construct validity remains P1 unresolved.
- **Original generator reproduced *originals* exactly**. Candidate staged via concrete diff manifest and separate manifest; independent SHA256-guarded local patch applicator reproduces candidate byte-for-byte.
- **Remaining P1 source/evidence blockers:** `SS-EVID-001`..`SS-EVID-007` involving Q02 Q04 Q05 Q06 Q07 Q08 Q09; all category-level source qualification retained.
- **Reviewer status:** `AI_SELF_REVIEW`; `INDEPENDENT_HUMAN_REVIEW=NOT_PERFORMED`; **IMPORT_SAFE=NO**; **publication-ready=NO**; **remote edits=0**.

- **Candidate reproducibility independent patcher:** 120 EN + 120 BN field replacements, byte-identical recreation against SHA256-pinned sources (`candidate_reconstruction_run.log`).
- **Evidentiary status unchanged by local edits:** seven unresolved P1 issues; not import-safe.
