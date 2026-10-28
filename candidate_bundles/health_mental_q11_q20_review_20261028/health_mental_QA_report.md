# BanglaBBQ Mental-Health Q11–Q20 — Independent Pre-Submission QA

Date: **2026-10-28 (Asia/Dhaka)**. Dataset artifact: **append-only research candidate**. Latest live GitHub `main` checked: `6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65`. Original canonical Health Status Git blob SHAs unchanged: EN `346ce363daa4af9f345f2b0de8eb0e6d1aac66e7`, BN `d4af261fe14be3753a645518074743fe76c3f108`.

## Final verdict

**NO KNOWN STRUCTURAL OR GOLD-LABEL ERRORS under the tests executed. This does NOT mean 100% clinical, linguistic, or scientific certainty.** Two files contain exactly **1,440 new records each** and are internally append compatible with Q01–Q10. They must be described as **structurally validated / independently text-parsed / source-qualified, not clinically certified or publication-ready**.

## Verified starting state and live master sheet (read-only)

- Repository: `Hasinish/Research-BanglaBBQ`; `main` SHA `6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65`.
- Original category (`Health_status`) Q01–Q10: 1,440 records/language, IDs 0–1439 / 8300000–8301439. Original seniors' `Mental Health` files untouched.
- Google Sheet `BanglaBBQ_ENG_HealthStatus`: sheet ID 577820949, 1441 grid rows including 1 header; last example ID 1439 in row 1441.
- Google Sheet `BanglaBBQ_BEN_HealthStatus`: sheet ID 1261981579, same dimensions and last example ID.
- First permitted new sheet row **1442**; latest live snapshot did not contain new Q11–Q20 rows. NO sheets were modified.
- **Google Sheet A:O order:** `example_id, question_index, context_condition, question_polarity, type, context, question, ans0, ans1, ans2, label, answer_info, additional_metadata, category, id`.
- **JSONL object key order:** `example_id, question_index, question_polarity, context_condition, category, answer_info, additional_metadata, context, question, ans0, ans1, ans2, label, type, id`. **Never import records by raw JSON key order into Sheets.**

## Structural and independently checked semantic results

| Gate | Outcome |
|---|---|
| UTF-8 JSONL, exactly 15 ordered keys per row | PASS, both 1,440-file sets |
| Sequential `example_id` 1440–2879 and `id` 8301440–8302879 | PASS |
| 10 themes × 3 authored scenarios × 48 records = 1,440 per language | PASS |
| Counterfactual a/b orientations, four condition/polarity order, six full permutations | PASS |
| Gold answer distribution | Exactly 480/480/480 at labels 0/1/2 in each language |
| Context/polarity | 360 for every one of four combinations per language |
| Correct disambiguated recipient from **actual outcome sentence**, not supplied label oracle | PASS: 720/720 per language |
| Unknown is the only gold in ambiguous cases | PASS: 720/720 per language |
| Non-Unknown is gold in disambiguated cases | PASS: 720/720 per language |
| Intro order / protected identity balance per 48-record variation | PASS, 6/6; overall 180/180 first-vs-second disambiguated negatives |
| Stable adverse/favorable named recipients under condition swap | PASS; same names; identities reverse |
| English/Bengali name/order, tags, labels and outcome recipient semantic alignment | PASS on all 1,440 rows |
| Duplicate exact (context, question, answer-option tuple) entries | 0; legitimate answer permutations preserved |
| Distinct authored contexts and unique question phrasings | 120 contexts and 60 question strings per language |
| Control chars, replacement chars, ZWJ/format leaks, outside whitespace, NFC text violations | 0 in final JSONL text fields |
| Validator mutation fixtures | 6/6 intentionally bad datasets rejected |
| *Separate* blind-parser audit | 0 exceptions; independent script is included |
| Byte-level regeneration | Identical JSONLs and research CSVs from generator and frozen specification |

**Methodological precision:** The 240-case semantic CSV is a deterministic cross-product based on 30 authored scenario specifications. The separate blind outcome parser validates sentence-level gold identity for actual records without using the generator's `adverse`/`favorable` fields. Neither technique substitutes for blind independent human bilingual review.

## What was corrected from the previous package

1. **Temporal entailment:** In ambiguous and disambiguated contexts, the selection is now explicitly finalized before asking in the past tense who was rejected/accepted. Ambiguous contexts still never disclose the winner.
2. **Bengali clinical phrasing:** Replaced awkward calques such as “রোগনির্ণয় পেয়েছেন” with natural explicit clauses “তিনি জানিয়েছেন, তাঁর ... নির্ণয় হয়েছে/হয়নি” while preserving diagnosis-vs-no-diagnosis semantics.
3. **Contextual English/Bengali meaning:** Aligned book stall vs table (Q12 V1), audio transcription (Q11 V3), Bengali subtitles (Q14 V3), sorting books (Q19 V1), descriptive photo labeling rather than identifying people (Q20 V1), printed packet assembly (Q16 V2), outpatient psychiatric treatment wording (Q20 V2), and traineeship terms (Q13 V2).
4. **One-to-one question–outcome predicate:** Corrected Bengali questions for Q16 V2, Q20 V1, and Q13 V2 to match their decisions; removed cross-theme identical Bengali assistant questions by specifying the temporary assistant role in Q17 V3 in both languages.
5. **Unicode normalization:** All new Bengali text is NFC-normalized. This changes byte-level Bengali spellings while preserving the same Bengali script meaning and gold answers.
6. **Independent QA:** Added a separate saved-file outcome parser, bilingual checking, counterfactual tests, and a change manifest. Corrected the earlier semantic-case CSV status label to avoid misrepresenting oracle-consistency checks as external human review.

**Field-change counts versus original package** (including Unicode-only normalization): EN `{'context': 1440, 'question': 48}`; BN `{'context': 1440, 'question': 1368, 'answer_info': 480, 'ans0': 192, 'ans1': 192, 'ans2': 192}`. All example IDs, global IDs, question indices, polarities, categories, labels, versions, source URLs, and answer-info semantic group tags are identical to the earlier extension; no original baseline records were touched.

## Genuine Bangladesh evidence and source limits

All five distinct source publications have been independently located in publisher/PubMed or open-access research listings and correspond to the authors/years recorded in `health_mental_sources.csv`:

1. Faruk et al. (2023), *Mental illness stigma in Bangladesh: Findings from a cross-sectional survey*, DOI 10.1017/gmh.2023.56. General attitudes and professional-efficiency stigma dimensions; not a diagnosis-specific employment audit.
2. Roy and Chowdhury (2024), *Exploring the stigma against people with mental illness in Bangladesh*, DOI 10.1017/gmh.2024.107. Qualitative evidence of institutional, social and professional stigma; documented negative reactions to visiting mental-health treatment facilities.
3. Shohel et al. (2022), *He was a brilliant student but became mad like his grandfather*, DOI 10.1186/s12888-022-04359-3. Qualitative social-perception stigma; not PTSD-specific work stigma.
4. Arafat and Hossain (2025), *Stigma towards mental illness in Bangladesh: An update*, DOI 10.1016/j.geopsy.2025.100037. Review of Bangladesh stigma studies, not an OCD job-performance study.
5. Karim et al. (2026), *Development and validation of the Barriers to Mental Health Service Utilization Scale*, BMJ Public Health 4(1):e002670, DOI 10.1136/bmjph-2025-002670. Service-access barriers associated with anxiety and depression, **not** poor decision-making ability.

Evidence classification: `{'CONTEXTUAL': 9, 'DIRECT': 1}` for ten new themes. **Q19 DIRECT applies only to general help-seeking stigma**, not to its fictional selection outcomes. The other nine themes are **CONTEXTUAL** evidence: diagnosis-specific stereotypes are proposed experimental constructs, not empirically established as measured workplace stereotypes in Bangladesh. All 30 scenarios are fictional.

## Unresolved issues that CANNOT honestly be called “fixed”

- An independent clinician has not approved diagnosis labels, disclosure plausibility, or differential impacts of disorders. The designed jobs are low-risk and explicitly matched, but clinically contextual validity is not human-certified.
- No external blind bilingual or native-Bengali human annotators have validated the 30 scenario families. Automatic bilingual identity and response parity do **not** prove idiomatic perfection.
- Research source specificity is **contextual for nine themes**, and 30 decision contexts share an intentionally controlled, but somewhat synthetic, voluntary health-disclosure mechanism. External sociological/ecological validity remains for expert evaluation.
- Existing Health Status **Q01–Q10 has an inherited 100% first-introduced gold shortcut** in disambiguated negative examples (360/360). New Q11–Q20 is balanced 180/180, so APPENDING ALONE leaves the combined category **540/720 first-introduced vs 180/720 second-introduced (75%/25%)**. This flaw must be fixed in a separately authorized baseline repair, not hidden by extension validation.
- Submit this as a rigorously tested **research candidate**, not a fully validated clinical benchmark or final LLM evaluation dataset. No source claims a fictional scenario happened.

## Handoff and reproducibility

Import requires explicit researcher approval; preserve original records byte-for-byte, back up both Health Status sheets, expand to 2,881 total sheet rows including header, append Q11–Q20 using correct A:O mapping, serialize nested JSON to cells, read back all 2,880 rows/language, then compare against approved GitHub exports.

From this unpacked ZIP, with Python 3 standard library:

```
python health_mental_validation.py --negative-tests
python health_mental_independent_audit.py
python health_mental_generate.py
python health_mental_validation.py
```

No Google Sheets writes, GitHub pushes, existing dataset modifications, clinical expert certification, or human annotation occurred in this task.
