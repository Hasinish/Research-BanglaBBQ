# Post-fix forensic re-test — Health_status (local only)

**Source main** `e186b283fa5b184058e2cb395273e9968a893b20` (original EN blob `a637d6ac18ac901c7a22356dbf47d244230e63b2`; BN blob `525d72db59ad609d07cf855f128aa09a6da936da`). **Local only, no remote writes.**

- Original: 1,440 + 1,440 rows; original independent validator 47/47 structural gates and 0 row failures, author 32/32. 240/240 role-entailment anchors matched labels; 40/240 anchor editorial semantic flags covering 5 distinct Q/V families, plus other Bengali grammatical errors.
- Applied: 9 unique repair issues, 840 field-cell edits (EN 360, BN 480) across 600 language-specific records. No ID, label, category, metadata, source, or record-count changes. Candidate context/question text changed only. See `health_status_change_manifest.csv` for exact before/after.
- Temporary failure investigation: using original manifest produced 576 text-lineage mismatches (expected because it still described pre-fix strings); separate **audited** manifest corrected those strings and calibrated tiers. Original manifest preserved.
- **Post-fix** independent validator **47/47 PASS** / zero row failures using audited manifest, author validator **32/32 PASS**; bilingual anchors **240/240** script-role gold matches, **0/240** scored residual semantic-equivalence failures in patched families, based on 30-case AI base judgments. This is not native human certification, and it does not eliminate source/construct issues.
- Candidate SHA256 EN `db0d3daea69d2d088e2aeb7a7c624f039c804478ca3af308a7d7f8191ea93eae`; BN `0d506d37dc58b50f663df0a054a502c390324d8e4e04cb4dab7d980ce28b3c90`. Local patch repeat-run byte-identical.
- **UNRESOLVED P1 source/construct items:** Q02 appointment-administration extrapolation, Q04 leprosy treated-without-disability unsupported (BLOCK), Q07 arsenicosis appearance overlap, Q08 epilepsy club-selection extrapolation, Q09 post-treatment breast-cancer cohort gap. Also original-author validator source-tier blind spot and scenario-family correlation concerns remain.
- 12 source URLs examined (some only indexed/abstract and direct-open unavailable). Forensic theme tiers DIRECT=5, PARTIAL=4, UNSUPPORTED=1.
- **IMPORT_SAFE=NO** / no active Health sheets / no external human reviewer. Recheck all ten themes before any approved production integration.
