# Religion Q1–Q20: Original / V2 / V3 bilingual wording review

**Date:** 2026-10-17  
**Milestone:** Draft 40 new English–Bengali wording pairs for researcher review  
**Status:** REVIEW PROPOSAL ONLY — NOT PRODUCTION EXPANSION

## Grounded reference and destination

- Template style: existing `Review_Politics_20_Variations` (sheet ID `722176577`).
- New working review tab: [Review_Religion_20_Variations](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit#gid=1743426767), sheet ID `1743426767`.
- Canonical production source tabs: `BanglaBBQ_ENG_Religion` (ID `804112545`) and `BanglaBBQ_BEN_Religion` (ID `860941009`).
- Reproducible proposal snapshot: `BanglaBBQ_Religion/review_v2v3_20261017.json`.
- Committed production baseline when drafting began: `fff5d34d3d34f28d47199113f3d2566a6aa8c655`.

## Method

A native copy of the Politics review tab's layout/formatting was created in the **same master spreadsheet**. This is a separate review worksheet, not a rewrite or append operation in the production Religion tabs.

Each of the 20 data rows contains:
1. `Q1`–`Q20`.
2. The exact existing **version-a, disambiguated, negative-polarity** bilingual context from `example_id = 1 + 48×(question_index−1)`.
3. Newly drafted bilingual Version 2, preserving the same identities, qualifications, social setting, and explicitly resolved outcome.
4. Newly drafted bilingual Version 3, preserving the same substantive scenario with a distinct narrative structure.

Both new versions are **paraphrases of the same fictional BBQ probes, not new observed events or independently sourced bias examples**. No answer choices, gold labels, counterfactual orientations, citations, metadata or production records were changed.

## Verified checks (proposal review, not publication QA)

- Exactly 21 × 4 populated review cells: one header and 20 Q-numbered rows.
- Exactly 20 originals and **40 proposed bilingual wording pairs** (20 V2 + 20 V3).
- Every original review context matches the current live English/Bengali production source context for the documented source ID.
- All 40 draft cells contain both an English and a Bengali passage with the expected delimiters.
- Across 20 themes, no exact duplicate candidate bilingual pairs and no candidate identical to its original or sibling variant.
- Automated presence checks for paired group identities passed across original/V2/V3 for both languages (240 language/group anchor checks). These are **not** equivalent to an independent semantic/translation audit.
- Re-read all 960 production records/language after draft creation and compared 15 fields against the committed JSONL versions: **zero cell discrepancies** in English (14,400 cells) and Bengali (14,400 cells). Production category remains at 960/language.

The native Politics review tab formatting, frozen header, and four-column side-by-side layout were reused. Three small Bengali prose refinements were applied during review-only readback (Q4 V2, Q8 V3, Q10 V2).

## Existing source uncertainties carried forward

The following theme numbers are highlighted amber in the review tab's first column and include hover notes:

- **Q3:** The caste paper does not independently substantiate the specific Hindu Dalit vs Muslim Dalit differential.
- **Q8:** The cited US Department of State report hosted on ecoi.net provides broad background, not the particular factory clerical-hiring mechanism.
- **Q9–Q10:** The cited classroom-inclusion paper does not directly document religion-based school debate leadership/speaking selection.
- **Q12–Q13:** The MRG report does not directly establish the wedding hall or individual wedding-invitation mechanisms.

**Source-uncertain drafts remain proposals. Do not treat paraphrasing as resolving source relevance.**

## Expansion gate (not performed)

User requested the same *review stage* as `Review_Politics_20_Variations`; this milestone creates the proposed candidate contexts, **not 48-record expansions or final integration**.

If separately reviewed and approved, each version could be expanded as:
- V2: 20 themes × 48 records = 960 English + 960 Bengali.
- V3: 20 themes × 48 records = 960 English + 960 Bengali.
- Existing production V1: 960 English + 960 Bengali, retained unchanged.
- Potential final total: **2,880 records/language** (144 per theme), but currently **960/language**.

Before any append: resolve the six source-sensitive themes; independently review Bengali naturalness and semantic alignment; generate both counterfactual orientations, ambig/disambig, neg/nonneg, and all six answer permutations per condition; run entailment and label checks; guard against correlated paraphrase leakage; back up production sheets; verify all writes and GitHub parity; obtain user approval to integrate.

## Research integrity

The archived JSON review candidate artifact is not an authoritative production JSONL file. No experimental accuracy, translation quality score, source verification status, or publication readiness is asserted by this task.
