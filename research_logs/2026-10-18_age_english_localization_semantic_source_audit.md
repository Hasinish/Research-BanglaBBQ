# Age English Localization, Bilingual QA, and Source-Relevance Audit — 2026-10-18

## Scope and preservation

- **Working spreadsheet**: [BanglaBBQ master](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit), \`BanglaBBQ_ENG_Age\` (gid \`0\`), 2,920 data records, 15-column schema.
- **Immutable original English source**: \`PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl\` (blob \`471a50fe7487a3200bb87b5c0a556a05ade208b7\`); seniors' \`Dataset_ BanglaBBQ_Old/Age/Age_Eng.jsonl\` is also preserved, byte-identical to that source.
- **Unchanged canonical Bengali reference**: \`BanglaBBQ_BEN_New/Age.jsonl\` (blob \`d5956f524f1fc42bddcf4ea52df95f7b29f3e990\`), spreadsheet \`BanglaBBQ_BEN_Age\` (gid \`1006819770\`).
- **Backup worksheets**: \`Backup_PakBBQ_ENG_Age_preRename_20261018\` (gid \`124282477\`, hidden) and \`Backup_BanglaBBQ_ENG_Age_preLocalization_20261018\` (gid \`1622078680\`, hidden). Full pre-localization backup audited against original GitHub: **0 discrepancies in 43,800 cells**.
- **New canonical English working export**: \`BanglaBBQ_ENG_New/Age.jsonl\`. Reproduction/structural validator: \`scripts/apply_age_english_localization_20261018.py\`.
- **Review tab**: \`Review_Age_Source_Audit_20261018\` (gid \`1613882208\`), 20 theme assessments, original cited URLs, supplemental Bangladeshi evidence, and open decisions.

## Applied corrections (English only)

| Q index | Modified rows | Change |
| --- | ---: | --- |
| Q9 | 144 | Correct 'whole processing' to 'whole process' in disambiguated technology-adaptation contexts. |
| Q10 | 168 | Correct grammatically broken 'They followed that was examples' wording in disambiguated responsibility contexts. |
| Q13 | 32 | Match established Bengali localization: Imtiaz → Shwapno supermarket, InDrive → Pathao car; fix 'listening to the advice'. |
| Q14 | 32 | Jalal Sons → Tasty Treat, matching Bengali. |
| Q15 | 128 | 'Chai Dhaba' → 'tea stall', matching Bengali. |
| Q16 | 12 | Fix 'a 18-year-old' → 'an 18-year-old'. |
| Q18 | 72 | Lahore/Karachi → Chattogram/Dhaka, matching Bengali; repair malformed 'moved ... a newly renovated' clause. |
| Q20 | 280 | 'chowk' → 'crossroads', fix duplicated 'going going' and 'zone zone', 18-year-old article, and ambiguous 'when he' pronoun. **This does not cure the underage-driver confound below.** |
| **Total** | **868** | Only the English **context** cell (column F) was changed; all other fields preserved. |

Google Sheets \`batchUpdate\` succeeded across all eight theme ranges. Full post-write readback compared the 2,920-row English working worksheet to the deterministically corrected source and yielded **0 discrepancies across all 43,800 cells**. Other 2,052 English records are unchanged against immutable PakBBQ English. Bengali working worksheet readback matched canonical Bengali GitHub in **all 43,800 cells** and was **not edited**.

## Bilingual structural / semantic review

- 2,920/2,920 paired IDs 0–2919, complete 15-field schema; 20 source question themes.
- **Zero bilingual mismatches** for \`example_id\`, \`question_index\`, \`question_polarity\`, \`context_condition\`, \`category\`, \`answer_info\`, \`additional_metadata\`, \`label\`, \`type\`, \`id\`.
- 1,460 English ambiguous and 1,460 disambiguated QA rows; all ambiguous gold labels point to \`Unknown\`.
- All 868 contextual edits were verified against corresponding Bengali place names/meaning at the template and substitution level. This is **automated structural + targeted bilingual review only**; independent full-record native-speaker linguistic and entailment certification remains outstanding.
- QA counterfactual caveat: retained source-family paraphrases are not independent bias incidents; do not randomly split correlated records across evaluation partitions without grouping.

## Source checks: theme-level verdicts

**Sources are evidence of stereotype mechanisms or broad social patterns, not documentation of invented vignette events.** The 14 original unique source strings were catalogued. Selected accessible source texts and bibliographic identities were checked against their claimed theme, and supplementary Bangladesh sources were separately assessed. **This is not exhaustive independent source certification for every vignette.**

| Theme | Source-mechanism verdict | Limit / action |
| --- | --- | --- |
| Q1 | Broad global evidence | Generic age-memory stereotype; fictional park dialogue, not Bangladesh observation. |
| Q2 | Broad global evidence | Generic forgetfulness discussion; grandparent/son comparison not experimentally supported by citation. |
| Q3 | Broad global evidence | APA's generational-work stereotypes, not professor grading or Bangladesh evidence. |
| Q4 | Broad global evidence | US-centered ageism textbook, not a specific political argument. |
| Q5 | Broad global evidence | Dionigi review plus Hong Kong age-stereotype memory experiment, not a meeting report. |
| Q6 | Weak / indirect | NCBI stigma chapter does not directly establish who works overtime. |
| Q7 | Weak / indirect | General ageism source is not direct evidence for age-related hiring creativity decisions. |
| Q8 | Original not confirmed accessible | Youthwork source could not be retrieved; avoid 'source verified'. |
| Q9 | Original not confirmed accessible | PsycNet record not inspected; supplemental Bangladesh digital-use evidence is only broad. |
| Q10 | Broad global evidence | Qu et al., \`10.1111/cdev.13156\`, examined teen irresponsibility stereotypes and counterstereotyping, **not** this fictional newspaper comparison. |
| Q11–Q12 | Broad global evidence | ScienceDaily article reports research on adolescent stereotype expectations/risk-taking, not specific fighting pairs. |
| Q13 | Broad + localized business evidence | Stanford discusses older adult tech skills; Shwapno and Pathao car service are real Bangladesh services, but not vignette evidence. |
| Q14 | Broad + localized business evidence | Age-related physical-function stereotypes discussed generally; Tasty Treat is a Bangladesh retail brand, not proof of the walking anecdote. |
| Q15 | **Source-mechanism mismatch** | TechRepublic technology-skills survey cannot establish which age group works in customer service versus product release. |
| Q16 | Broad global source bibliographic match | \`10.1159/000439349\` is 'Stereotype Threat Lowers Older Adults' Self-Reported Hearing Abilities'; it does **not** document the qawwali scenario. |
| Q17 | Broad global evidence | Age memory stereotypes, not the fictional religious mehfil details. |
| Q18 | **Source-mechanism mismatch** | Kunze et al. studied employees' resistance to workplace change, not residential moves between Bangladeshi cities. |
| Q19 | Original not confirmed accessible | Youthwork original inaccessible; the fictional Eid charity episode remains uncited as an event. |
| Q20 | **Blocking demographic/legal confound** | See below; original Conversation URL not independently retrievable during audit. |

### Bangladesh-specific corroboration (scope-limited)

1. Rahman and Afrin, *Ageing and Ageism: Myths and Realities in Selected Rural and Urban Areas of Bangladesh*, *Journal of Bangladesh Studies* 23(2), 2021, university-hosted [PDF](https://www.jkkniu.edu.bd/uploads/publication/2024-05-11-6d6aed_113987307.pdf). Study compares general ageism in Dhaka and Barguna; it **does not** validate these specific fictional incidents.
2. Mahzabeen et al., *Usability and Adoption of Smartwatches by Older Adults in Bangladesh: User Study*, *JMIR Aging* (2026), [DOI 10.2196/76404](https://aging.jmir.org/2026/1/e76404). Relevant to technology adoption/user support, but **not** an actual Pathao booking comparison.
3. [Shwapno's official company page](https://www.shwapno.com/AboutUs?lang=en), [Pathao's official car service](https://pathao.com/car/?lang=en), and [Tasty Treat's Bangladesh presence](https://www.tastytreatbd.com/) support local referent validity, **not** age-bias mechanisms.
4. [Bangladesh Road Transport Act, 2018](https://bdlaws.minlaw.gov.bd/act-print-1262.html) and [BRTA licensing requirements](https://brta.gov.bd/site/page/4258fc8f-8aec-4895-b11d-a0b33b489af2/) establish a nonprofessional driving licence minimum of 18 years.

### Important: Q20 is **not** cleared for publication

**112 Q20 records** refer to **15- or 17-year-old car drivers** in an apparently public-road collision. Since Bangladesh requires nonprofessional drivers to be at least 18, this injects a legality/risk confound into a test ostensibly comparing age groups. In particular, some ambiguous items labeled Unknown can prompt a reader to infer unlawfulness from age alone. The 280 English Q20 rows received **only safe place-name/typo/anaphora fixes**; no driver's age, Bengali record, gold label, or scenario mechanism was silently altered. A controlled bilingual redesign and counterfactual QA are required before publication.

## Verified end state vs outstanding

**Structurally validated**: All 2,920 English + 2,920 Bengali record pairs, schema, IDs, conditions, gold indices, 43,800-cell working readback per language, 43,800-cell backup parity, and exactly 868 authorized English context edits.

**Targeted bilingual localization reviewed**: Q9/Q10/Q13/Q14/Q15/Q16/Q18/Q20 edits align with existing Bengali at the relevant template/phrase level.

**Evidence audit (partial, source-boundary labeled)**: 20 theme verdicts and 14 inherited sources catalogued; supplemental Bangladesh evidence recorded. Exact-vignette sourcing and inaccessible citation retrieval remain open; mismatches in Q15 and Q18 and the Q20 legal confound are identified.

**Not publication-ready**: independent native Bengali/language QA, full item-level logical-entailment review, Bangladesh-specific source relevance for weak themes, and Q20 bilingual redesign are required.
