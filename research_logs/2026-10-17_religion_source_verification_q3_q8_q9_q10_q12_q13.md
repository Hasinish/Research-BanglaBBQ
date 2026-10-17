# Research Log: Religion Q3/Q8/Q9/Q10/Q12/Q13 Source Verification

**Date:** 2026-10-17  
**Researcher / Agent:** ChatGPT, live GitHub/Google Sheets and external-source audit  
**Category:** Religion  
**Milestone Scope:** 6 of 20 themes across V1, V2 and V3, 144 records per theme per language  
**Status:** SOURCE AUDIT COMPLETED; **SIX PRODUCTION THEME MECHANISMS STILL REQUIRE REPAIR OR SOURCE REPLACEMENT**. No publication-ready claims.

## 1. Research Objective & Context

Verify whether the existing citations actually substantiate the six flagged BanglaBBQ Religion bias mechanisms. The benchmark uses fictional controlled QA scenarios; sources substantiate *real-world mechanisms*, not fictitious individuals/events. A source mentioning discrimination generally is not evidence of an unrelated specific mechanism. The goal was to identify verified support, counterevidence, and justified redesigns, not silently invent or alter published datasets.

## 2. Source Files & Live Google Sheet References

- Live production: https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit
- English production tab `BanglaBBQ_ENG_Religion`, ID `804112545`; Bengali production `BanglaBBQ_BEN_Religion`, ID `860941009`.
- Audited source passages and candidate replacements, live review tab `Review_Religion_Source_Audit_20261017`, ID `1272448316`, range `A1:I7`.
- Canonical JSONL files: `BanglaBBQ_Religion/Religion_eng.jsonl` and `BanglaBBQ_Religion/Religion_bng.jsonl`.
- Verified committed baseline before audit: `70f4364e220f5576072cf40a90fb9f20692f70c4`.
- Canonical dataset stays at **2,880 records/language**. Each flagged question index has **144 per language** = 48 original V1 + 48 V2 + 48 V3; audited scope therefore covers **864 records/language** (1,728 bilingual records). This is scope identification, not a claim that each context was linguistically inspected.
- Canonical file blobs at audit: EN `1906da452060d6e2393d200cc4d32b7d8addae75`; BEN `e04e9d7d473f26c63e8f14ba7bfecfc34ff14610`. All 144 records per question index had the same original source URL in each language.

## 3. Original Issue and Primary-Source Verification

### Q3 — Public water pump, Dalit Hindu vs Dalit Muslim — FAIL / CONTRADICTORY

Current cited primary source, Iftekhar Uddin Chowdhury, *Caste-based Discrimination in South Asia: A Study of Bangladesh*, IIDS Working Paper Volume III, no. 7:
https://idsn.org/wp-content/uploads/user_folder/pdf/New_files/Bangladesh/Caste-based_Discrimination_in_Bangladesh__IIDS_working_paper_.pdf

- **Working-paper printed pp. 27–28 / PDF pp. 34–35, section 5.1:** states that discrimination was *not* found at government-provided water sources such as WASA/municipal/Union Parishad tube wells, whereas discrimination occurred at private ponds/lakes.
- **Printed p. 28 / PDF p. 35, section 5.2:** seemingly contradicts the previous prose by reporting survey discrimination at public water facilities; also says water-access hardship among Muslim Dalits is sometimes worse, including from private sources. Thus the same report is internally inconsistent and does **not** establish the present directional Hindu-Dalit-vs-Muslim-Dalit public-pump disparity.
- Current benchmark makes a fictional caretaker block the Hindu Dalit farmer at a government/public pump, while a Muslim Dalit farmer proceeds. **Do not describe this as documented in the source.**
- **Recommended substantive repair:** test access to a privately controlled shared irrigation pond/other water resource with explicit equally granted permission and matched eligibility. Even then, the study cannot be said to demonstrate a pure religion-only causal effect; the fictional reversal is the benchmark design, not historical evidence.

### Q8 — Factory clerical hiring — REPLACEMENT SOURCE IDENTIFIED, NOT APPLIED

Original citation:
https://www.ecoi.net/en/document/2071164.html
This is the *U.S. Department of State 2021 Country Report on Human Rights Practices: Bangladesh* mirrored by ecoi.net; it is not authored by the Austrian Federal Office. It does not document the fictional clerical job allocation.

**Stronger mechanism-matched reporting:** *The Daily Star*, 24 February 2026, “Probe Ibn Sina job circular: HC”:
https://www.thedailystar.net/news/bangladesh/news/probe-ibn-sina-job-circular-hc-4113301

The Daily Star reports that the High Court asked authorities to investigate allegations that a January 26 job advertisement from Ibn Sina Pharmaceutical Industry PLC restricted Executive/Senior Executive (Legal Affairs) positions to **male practising Muslim** candidates, and ordered consideration of non-discriminatory recruitment guidelines. This corroborates religious eligibility restrictions in employment, **not** a court's final factual finding or the benchmark's made-up factory clerk hiring decision. The real advertisement's gender restriction is an additional variable, not evidence of gender-neutral employer choice.

**Recommended repair:** either replace source with the newer recruitment story while explicitly marking illustrative context, or (more directly) redesign as equal-gender, equal-qualification applicant eligibility/screening. Do not imply that a court established discriminatory final hiring outcomes.

### Q9 — School debate team leadership — FAIL

Original source:
https://www.researchgate.net/publication/318201463_Practices_of_Social_Inclusion_in_the_Secondary_School_Classrooms_A_Look_into_Selective_Schools_from_Dhaka_City

Md Tariqul Islam and Farhana Rashid's 2015 study examines classroom inclusion in three Dhaka secondary schools and the existence of debating clubs, school policies and co-curricular participation. It does **not** establish a religion-based debate-team leadership decision. Indeed, it reports apparently religion-neutral admission policy at those sampled schools; selective quoting would be misleading.

**More specific alternate study** (also relevant to Q10), IIDS/Chowdhury working paper:
https://idsn.org/wp-content/uploads/user_folder/pdf/New_files/Bangladesh/Caste-based_Discrimination_in_Bangladesh__IIDS_working_paper_.pdf

**Printed pp. 41–43 / PDF pp. 48–50** document Dalit students' difficulties in school sports selection and institutional participation. They do **not** establish a universal Hindu-vs-Muslim student difference in debate leadership. A school sports-team selection vignette comparing **both Dalit Hindu and Dalit Muslim applicants** with identical performance would be closer to that evidence. Caste must be controlled and reported as an intersectional factor.

### Q10 — School debate audition speaking slot — FAIL

Same original classroom inclusion paper as Q9, which does not document discriminatory selection of Hindu and Muslim speakers with identical scores.

IIDS/Chowdhury working paper, printed **p. 43 / PDF p. 50**, reports that children of both Hindu and Muslim Dalit communities were sometimes excluded from school cultural activities, with uneven experiences. This can support an **intersectional school cultural participation/performer slot** theme, not a historical claim about a particular debate speaking audition. Maintain explicit equal eligibility, counterfactual role reversal and Unknown in ambiguous contexts.

### Q12 — Wedding community-hall booking — FAIL

Original MRG report, *Under threat: The challenges facing religious minorities in Bangladesh* (17 November 2016):
https://minorityrights.org/resources/under-threat-the-challenges-facing-religious-minorities-in-bangladesh/

The report documents long-term religious-minority exclusion and threats, but no specific passage verified here demonstrates a Hindu wedding family's community-hall reservation being rejected while an otherwise equivalent Muslim wedding reservation is accepted.

**Mechanism-adjacent contemporary evidence**:
- Associated Press, October 2024, report on Durga Puja organizers in Uttara holding celebrations at a smaller location amid objections to a field-based venue:
https://apnews.com/article/bangladesh-durga-puja-hindu-festival-violence-3e87b4d3702308687aeee43854da03eb
- Dhaka Tribune, 25 September 2024, reporting protests, negotiations and official mediation over Puja venues:
https://www.dhakatribune.com/bangladesh/359747/restriction-on-durga-puja-in-uttara-stirs
- Prothom Alo later fact-checks claims about the historic 2024 Uttara venue protest, clarifying a disputed **location** rather than an unqualified ban on worship:
https://www.prothomalo.com/bangladesh/gy7r8tzvvy

These reports concern **Hindu festival venue use**, NOT Muslim-versus-Hindu wedding-hall rental treatment. They also contain potential confounds (field's customary uses, site permissions, public safety). A new venue-access scenario must explicitly match such factors. **Do not replace the current wedding-hall citation with AP without changing the fictional scenario and documenting this nuance.**

### Q13 — Neighbour omitted from wedding invitation — FAIL AS WRITTEN; RELEVANT CASTE-WEDDING SOURCE FOUND

Original citation: the same MRG report used in Q12. It does not directly support religious identity selecting a generic Hindu neighbour rather than a generic Muslim neighbour for an individual wedding guest list.

**Directly relevant wedding invitation/feast mechanism source:** IIDS/Chowdhury working paper:
https://idsn.org/wp-content/uploads/user_folder/pdf/New_files/Bangladesh/Caste-based_Discrimination_in_Bangladesh__IIDS_working_paper_.pdf

**Printed pp. 30–31 / PDF p. 37**, section 5.3: invitations from non-Dalits to Dalits at private feasts are rare; describes segregated seating/menus at community and marriage events and states Hindu Dalits experience stronger exclusion in feasts than Muslim Dalits in the studied populations.

**Recommended revision:** specify **Dalit Hindu neighbour** and **Dalit Muslim neighbour** (both Dalit), with an explicitly non-Dalit host equally familiar with both, to make the fictional guest-list test closer to documented intersectional exclusion. Do not claim the paper documents the invented specific pair of neighbours or that caste/religion causality is cleanly separable.

## 4. Methodology and Decisions

Evidence grades used:
- **CURRENT SOURCE MATCH**: directly addresses the mechanism (not found for any of the six current fictional details).
- **ALTERNATE MECHANISM SOURCE FOUND**: stronger external evidence found for related mechanisms, but **not yet integrated** (Q8 and Q13; options for Q9/Q10/Q12).
- **FAIL / REDESIGN REQUIRED**: original citation does not support the particular comparison; need scenario plus possible answer text redesign (Q3, Q9, Q10, Q12, Q13).
- **Source internally inconsistent**: report contains seemingly conflicting qualitative/survey claims, to be interpreted rather than cherry-picked (Q3).

All sourced real-world evidence is distinguished from intentionally fictional BBQ counterfactual scenarios. Counterfactual orientations are benchmark constructs, not observed interventions; none of the sources provides randomized or controlled proof of religion causing those specific paired outcomes.

## 5. Exact Changes & Before/After

**Production changes: NONE.** Only a separate 7-row × 9-column review worksheet and versioned research documentation were created. Existing 2,880 records per language, the 15-field schema, IDs, answers, labels, source URLs and their hash-pinned expansion shards are untouched. Therefore there is no approved before/after change to a canonical Religion record in this audit.

**Proposed changes only**, to be formulated as coordinated English+Bengali V1/V2/V3 contexts, questions, choices and metadata. The public-water source issue (Q3) and wedding-invitation caste confound (Q13) cannot be repaired by a citation-only substitution.

## 6. Pre/Post Edit Backups

No production edits in this audit; no new dataset backup was needed. Existing immutable baseline snapshots from Religion V2/V3 expansion remain intact:
- `backup/religion-pre-v2v3-expansion-20261017`
- Hidden `Backup_Religion_ENG_preV2V3_20261017`
- Hidden `Backup_Religion_BEN_preV2V3_20261017`

Any later production redesign **must** create fresh pre-edit backups from the current 2,880-record source, and handle immutable expansion-shard hash changes explicitly.

## 7. Quality Assurance / Validation

- Verified the canonical EN and BEN JSONL blobs and grouped flagged themes by `question_index`, `wording_variant`, and `additional_metadata.source`: all six have **144 rows per language**, comprising **48 V1 / 48 V2 / 48 V3**.
- Verified the original cited URLs appear consistently across all 144 records per language for each flagged theme.
- Read exact live English exemplars (ambiguous/disambiguated) from Google Sheets for Q3/Q8/Q9/Q10/Q12/Q13.
- Opened and read specific passages of the relevant public reports; inspected authorship, methods, limitations, alternative evidence and (where found) internally contradictory statements.
- Read back `Review_Religion_Source_Audit_20261017!A1:I7`: 7 rows including 1 header, 9 columns, 6 expected theme entries, nonempty alternative URLs, no missing records; inspected header/body formatting.
- **Not claimed**: per-record bilingual entailment verification or a full new production Sheets-versus-GitHub parity run, since no production records were modified. Prior verified structural parity remains the baseline; do not infer publication readiness from it.

## 8. Remaining Issues / Gate

**Source-relevance triage is finished for all six themes, but source-verification approval is NOT finished for production.** Current scenarios in Q3/Q9/Q10/Q12/Q13 still require carefully sourced redesigns; Q8 has a credible source replacement that needs a precisely documented integration decision. After revision, regenerate/repair **all 144 records/language per affected question** (both orientations; all three wording variants; ambiguous and disambiguated; two polarities and six answer rotations) and re-verify bilingual alignment, V1 preservation policy (explicit authorization if changing originals), source URLs, gold labels, ID continuity, shard/historical hash traceability, and complete Google Sheets/GitHub parity.

Independent native Bengali linguistic review remains outstanding. This dataset is **not publication-ready**.

## 9. Git and Commit Tracking

- Source audit branch: `audit/religion-source-verification-q3-q8-q9-q10-q12-q13-20261017`
- Research log: this file.
- Review tab: `Review_Religion_Source_Audit_20261017` (gid `1272448316`).
- Final commit and CI state: verify on merge; do not invent a commit SHA.
