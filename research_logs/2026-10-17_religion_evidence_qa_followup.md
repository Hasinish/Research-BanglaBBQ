# Religion evidence QA follow-up — 2026-10-17

## Scope and authorization
User requested fixes for Religion Q3, Q8, Q9, Q10, Q12, Q13, Q18, and the Q7 research-log mismatch. Scope restricted to Religion working tabs, canonical English JSONL, audit descriptions and project memory. Politics, Age, and the original thesis baseline were not modified.

## Pre-edit backups
- Git branch `backup/religion-pre-evidence-qa-20261017`, created from commit `a992c9f5ad2c7f5929c4d4dba34643b26e1fc400`.
- Hidden live sheet `Backup_Religion_ENG_preEvidenceQA_20261017`, sheet ID 834378694.
- Hidden live sheet `Backup_Religion_BEN_preEvidenceQA_20261017`, sheet ID 2123905285.
- Both hidden sheets verified at 961 rows (one header + 960 records) with zero cell differences against the production sheets before editing.

## Verified production data corrections
- **Q18 English, IDs 816–863**: 24 disambiguated English records had `gave assistance to Muslim resident` or `gave assistance to Hindu resident`. Repaired to `gave assistance to the Muslim resident` and `gave assistance to the Hindu resident`. Only `context` field changed. All answer options, labels, metadata, IDs, Bengali records and other themes preserved.
- Live sheet: `BanglaBBQ_ENG_Religion` (sheet ID 804112545). The write returned 24 replies and targeted row read-back confirmed expected text.
- Canonical branch path: `BanglaBBQ_Religion/Religion_eng.jsonl`.

## Documentation corrections
- Q7 live records (all 48) describe equally detailed community-service proposals at a **cultural festival**. Previous research log incorrectly said an upazila union health-campaign proposal. Research documentation corrected to reflect the live data without making an unauthorized substantive scenario rewrite.
- Q8 `https://www.ecoi.net/en/document/2071164.html` is a **US Department of State 2021 report hosted on ecoi.net**, not a report authored by the Austrian Federal Office for Immigration and Asylum. Audit notes corrected.
- Q20 historical admission restrictions must not be described as independently verified government quotas.
- Audit source descriptions refined to distinguish broad thematic evidence from proof of a particular fictional event.

## Unresolved methodological/source items — NOT verified complete
- Q3: caste and religious status are confounded in the current Dalit Hindu/Dalit Muslim comparison. The IDSN/IIDS source supports caste discrimination broadly, but the precise comparative effect is not established.
- Q8: a country religious-freedom report cannot directly establish the specific factory clerical-hiring mechanism.
- Q9–Q10: a Dhaka classroom-inclusion study is not direct evidence for religious exclusion in debate leadership or speaking slots.
- Q12–Q13: the MRG minority report supports broad marginalization; wedding-hall rejection and omission from invitations are not established as the particular cited mechanisms.
- Independent native-Bengali linguistic review across all 20 themes remains outstanding.

These themes were not silently replaced with unrelated or unsupported vignettes. They require separate source-backed redesign with aligned counterfactuals and full bilingual review before claims of source verification or publication readiness.

## Validation targets
- 960 English + 960 Bengali records; 20 themes x 48, IDs 0–959, 15 columns.
- Label balance 320/320/320, 480 ambiguous and 480 disambiguated, full six-way permutations, no exact duplicate QA tuples.
- Zero live Sheets / committed JSONL differences after the new Q18 repair.
- No other production categories changed.
