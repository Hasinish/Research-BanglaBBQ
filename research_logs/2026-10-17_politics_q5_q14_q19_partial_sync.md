# Politics Q5/Q14/Q19 targeted corrections — 2026-10-17 (partial synchronization)

## Authorization and scope
The researcher explicitly approved correcting the three preliminary Politics QA issues (Q5, Q14, Q19) in the existing 2,880-row/language production dataset. This note does not claim independent whole-benchmark linguistic or source certification.

## Preservation
- GitHub pre-fix snapshot branch: `backup/politics-pre-q5-q14-q19-fixes-20261017` at `6a1462f306ecad7198f8c795df73761e16e9c583`.
- Hidden live backups: `Backup_Politics_ENG_preQAfix_20261017` (gid 1744544726) and `Backup_Politics_BEN_preQAfix_20261017` (gid 1886409399).
- Historical thesis files and earlier pre-expansion 960-row backups were not edited.

## Applied to live Google Sheets (both languages)
1. Q5: qualified all 144 rows/language with the historical year 2022 in the context (48 original/V1, 48 V2, 48 V3). No claim that the vignette was a documented 2022 event.
2. Q14: replaced the negative question text in 72 rows/language to ask whose belongings were forcibly thrown out, without assuming expulsion of the student.
3. Q19: aligned the Bengali context and option terminology for government critic; 48 original/V1 contexts changed, 144 Bengali records had the relevant answer option updated (48 occurrences in each of ans0, ans1, ans2). V2/V3 contexts already used government critic terminology.

## Verification performed
- Before edits: 432 relevant records/language had live cell-by-cell 15-column parity with the earlier canonical GitHub blobs across six bounded theme ranges.
- After edits: all 432 relevant rows/language were read back for text columns F:J; no unexpected differences were found against the exact authorized transformation.
- No labels, IDs, answer_info, additional_metadata, category, or record order changed by the sheet updates.

## GitHub synchronization status: INCOMPLETE
- Branch: `fix/politics-q5-q14-q19-20261017`.
- English canonical 2,880-record JSONL was successfully edited on that branch (commit `b5ef5d6e2510cc1a2afbdd1b12790fc09d06cbda`).
- Two attempts to write the entire ~2.7MB Bengali canonical JSONL through the GitHub connector failed with HTTP/2 connection errors; Bengali canonical remains old on that branch. **DO NOT MERGE THE PARTIALLY SYNCHRONIZED BRANCH AS IS.**
- Idempotent script `scripts/apply_politics_q5_q14_q19_fixes.py` staged on repair branch at commit `7b68f438f887d1404c09633f9ab8f509edd76c9c`. The coding agent should run this locally after pulling, validate it, sync both canonical JSONL files, and resolve legacy-hash and V2/V3 assembler/manifest assumptions before merging safely.
- The source immutable 960-row pre-expansion backups, versioned shard manifests, and historically preserved legacy datasets must remain untouched. Make provenance explicit in a dated repair log and update memory only after actual synchronized validation.

## Pending
Independent native-Bengali review, independent source-relevance verification, and grouped paraphrase evaluation controls remain outstanding. Not publication-ready.
