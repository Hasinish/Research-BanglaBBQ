# Gender translation QA checkpoint — 2026-10-18

Scope: live ENG/BEN Gender worksheets, 4,696 pairs, 34 themes. Initial main HEAD bb66c40f9684491d06b0049ddf84498b9655b89f.

Previous live scan: 2,321 distinct bilingual context pairs; 1,198 English-leak candidate fields; 1,220 suffix candidate fields (not adjudicated). Structural ID/label alignment passed; semantic validation NOT complete.

Confirmed samples: example_id 81 (supporter/recipient translation ambiguity); 1024 (মেয়ের-এর double suffix); 2625 (embedded repeated English sentence). Example 425 no longer exhibits the alleged full-sentence leakage on live.

Code-only commits:
- 21881e7362a9e801b02a740478ba3e7f3662c55a: group2 translator rejects unknown extracted names rather than silently leaking English; Q32 possessive construction repaired.
- 0f0e239bad3e80a0cbb76be404f1f1593f5160cb: group1 Q11 supporter vs. recipient rendering clarified.

Independent Google Sheet backup created and spot-checked (first two data records match source): https://docs.google.com/spreadsheets/d/1xRZuY0wbqJ7hzdYFJZWZGttBts6xfOTxPHD9afu3oSQ/edit
No production sheet cells or canonical JSONL records modified. No complete generator regression run was possible here because the original PakBBQ input and large canonical datasets are not available as local files and Git cloning is blocked. Therefore generator edits are NOT verified and require local regression testing, review, regeneration, sparse sheet changes, full live parity and formatting verification before release.

Status: IN PROGRESS; linguistically reviewed: no; source-verified: no; publication-ready: no.
