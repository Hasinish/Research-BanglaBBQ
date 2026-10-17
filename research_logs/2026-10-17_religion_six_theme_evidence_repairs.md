# Religion V1/V2/V3: Six-Theme Evidence-Alignment Repair

**Date:** 2026-10-17  
**Category:** Religion  
**Status:** **PRODUCTION REPAIR STRUCTURALLY VERIFIED; NOT CERTIFIED PUBLICATION-READY**  
**Scope:** Q3, Q8, Q9, Q10, Q12, Q13; **144 records per theme per language** (48 V1 + 48 V2 + 48 V3), total **864 English + 864 Bengali** records.

## Authoritative baseline, sources, and provenance

- GitHub pre-repair main: `bba8ef471ebe0bc53fcd116ada1b16849a4a6b14`.
- Pre-repair canonical Git blobs: English `1906da452060d6e2393d200cc4d32b7d8addae75`; Bengali `e04e9d7d473f26c63e8f14ba7bfecfc34ff14610`.
- New backup Git branch: `backup/religion-pre-evidence-redesign-20261017` (points to unchanged pre-repair main).
- Hidden live Google Sheets backups: `Backup_Religion_ENG_preSixTheme_20261017` (gid `1200536192`) and `Backup_Religion_BEN_preSixTheme_20261017` (gid `479677031`). Each has 2,881 rows and 15 columns; prior to edits all **43,200 data cells** matched the corresponding production tab.
- Production tabs: `BanglaBBQ_ENG_Religion` gid `804112545`; `BanglaBBQ_BEN_Religion` gid `860941009`.
- Previously published original thesis dataset and pre-expansion V1 snapshots/hashed V2–V3 shards were not altered.

## Source-grounding and exact methodological changes

All revised paired stories are **fictional controls**, not documentary accounts of real named people or incidents. Counterfactual version B inverts the disadvantaged identity. No source is claimed to prove religion-only causation.

| Q | New controlled mechanism | Evidence / limit |
|---|---|---|
| 3 | Equal-permission access to a privately managed irrigation pond for a Dalit Hindu and Dalit Muslim farmer; caretaker lets one draw water | IIDS/Chowdhury working paper, pp.27–29, discusses private-pond discrimination and conflicting results on public water. Comparison remains intersectional; no universal religious direction. |
| 8 | Same-gender, equally qualified Hindu/Muslim male applicants for one private-company legal-affairs job; **initial religion-based eligibility screening** (not appointment/hiring) | The Daily Star, 24 Feb 2026, court-ordered investigation into a reported Muslim-only male legal-affairs job advert; **allegation, not a court finding of actual applicant rejection**. |
| 9 | Dalit Hindu/Muslim school pupils matched on grades, attendance, need and applications; school scholarship selection | IIDS pp.42–43 describes discrimination in scholarship awards for Dalit children. Case-level religious reversal is hypothetical, not proven community-wide effect. |
| 10 | Dalit Hindu/Muslim pupils matched on a **nonreligious** school cultural performance audition and identical scores; performance participation | IIDS p.43 directly notes exclusion of Dalit children of both religions from school cultural activities; specific audition/paired outcome fictional. |
| 12 | Hindu/Muslim festival committees apply for a neutral municipal ground on separate available dates, with matching field-use permissions, fees, stage/crowd duration and security | AP 12 Oct 2024 and Dhaka Tribune 25 Sep 2024 document Uttara Hindu festival venue disputes; **not** proof of an equivalent Muslim event being approved or purely religious motive. Site/ritual differences are contextual limitations. |
| 13 | Non-Dalit host considers two Dalit Hindu/Muslim neighbours with matched familiarity/availability for a **wedding reception meal only**, not worship | IIDS pp.30–31 documents Dalit exclusion at private/marriage feasts; survey comparison is intersectional and not a controlled causal test. |

**Evidence URLs**

- IIDS / Iftekhar Uddin Chowdhury: https://idsn.org/wp-content/uploads/user_folder/pdf/New_files/Bangladesh/Caste-based_Discrimination_in_Bangladesh__IIDS_working_paper_.pdf
- The Daily Star (Q8): https://www.thedailystar.net/news/bangladesh/news/probe-ibn-sina-job-circular-hc-4113301
- Associated Press (Q12): https://apnews.com/article/3e87b4d3702308687aeee43854da03eb
- Dhaka Tribune venue corroboration: https://www.dhakatribune.com/bangladesh/359747/restriction-on-durga-puja-in-uttara-stirs

The source for Q3 remains IIDS. Source metadata is updated for Q8, Q9, Q10, Q12 and Q13. Subcategory marks caste/religion intersectionality for Q3, Q9, Q10, Q13; stereotyped group names are made specific to **Dalit Hindus** for those themes.

## Record edits and gold-label logic

- The 15 columns and ordering were preserved for all 5,760 records.
- All six themes were revised across V1, V2 and V3 in English and Bengali, including ambiguous/disambiguated contexts, both negative/nonnegative questions, both counterfactual orientations and full six-way answer-choice permutations.
- Fields changed for each language: `context` (864), `question` (864), `additional_metadata` (864), `ans0` (480), `ans1` (480), `ans2` (480), and `answer_info` (720); unchanged fields were not rewritten.
- **IDs and original gold-label positions unchanged.** Correct answer roles explicitly checked: ambiguous ⇒ Unknown/অজানা; disambiguated orientation a/negative and b/nonnegative ⇒ Hindu target; a/nonnegative and b/negative ⇒ Muslim target. Every accepted/rejected action is named in the English and corresponding Bengali disambiguated context.
- Group- and question-specific answer options were rewritten where the mechanism changed: e.g. `The Hindu debater` ⇒ `The Dalit Hindu student` (Q9/Q10), and `The Hindu family` ⇒ `The Hindu festival committee` (Q12).
- No exact duplicate question/context/answer tuple among the full 2,880 rows per language.
- Unaffected fourteen theme blocks were compared against full pre-repair native backups with **zero differences**. Original V1 960 records are protected by dated pre-repair snapshots; modifications to six V1 themes were explicitly authorized by the user's current request.

## Reproducibility without historical rewriting

- `BanglaBBQ_Religion/evidence_revisions_20261017.json`: fully versioned 6 × 3 bilingual controlled-context designs, source URLs, questions and answer labels.
- `scripts/apply_religion_evidence_revisions.py`: idempotent patcher with role/gold checks; applies to each of 2,880 records, touching only the six themes.
- `scripts/assemble_religion_expansion.py`: validates **unchanged SHA-pinned pre-expansion baseline and 16 original shards**, then applies the evidence correction layer to produce approved canonical files.
- Updated auditor documentation reflects what each source actually supports; full independent Bengali/native human review remains a separate gate.
- The original `review_v2v3_20261017.json` is retained as historical proposal; the live `Review_Religion_20_Variations` worksheet and `Review_Religion_Source_Audit_20261017` have updated exemplars and statuses, verified by readback (18 bilingual exemplar cells; 6 audit rows).

## Completed checks and outcomes

- The repair branch's GitHub Actions Religion assembly run `39055253658` completed **successfully**, materializing canonical files at new Git blob SHAs:
  - EN `99115ab39bd12b403960c22498059254e6751325`
  - BEN `a08ee46feb3a41160c3960a4a274bfef36aa69dd`.
- Read back every edited 48-record block after Google Sheets writes (18 theme/wave blocks per language; 864 revised records each).
- **Entire production parity**: 2,880 × 15 = **43,200 cells per language**, **zero differences** from the corrected GitHub repair branch.
- Per language: exactly 864 changed records = 6 themes × 144; **0 changes** in the other 14 themes against snapshots.
- 20 × 144 theme counts; labels [960,960,960]; full six-way option permutations in each 6-record group; sequential IDs 0–2879; no duplicate exact tuples; all 10 shared bilingual structural/metadata fields match; zero incorrect Unknown/disambiguated label-role checks.
- This is machine/bilingual consistency QA, **not a native-speaker or independent human factual review**.

## Remaining research limitations

1. The IIDS study is historical and uses non-probability/purposive sampling; it cannot prove religion-only causation from the fictional pairings in Q3, Q9, Q10, and Q13.
2. Q8 source is reported employment-discrimination allegations and court directions, not a final judgment proving actual hiring-screen rejection.
3. Q12 source directly addresses a Hindu festival venue dispute, but not the hypothetical, closely matched Hindu-versus-Muslim comparative case or all possible site constraints.
4. Additional independent native Bengali linguistic review, human counterfactual/entailment audit and paraphrase-family-aware evaluation design remain needed.
5. **Not publication-ready.**

## Synchronization notes

Production GSheets and GitHub repair branch matched completely at verification. Merge only with fast-forward/lease and CI check; after merge, refresh `memory/state.md` with actual final SHA and do not claim independent semantic human certification.
