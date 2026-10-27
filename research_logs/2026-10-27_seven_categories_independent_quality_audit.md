# Research Log: Independent Forensic Quality Audit of 7 Final BanglaBBQ Categories

- **Date**: 2026-10-27
- **Topic**: Independent Quality Audit & Forensic Vulnerability Analysis (Physical Appearance, Social Status, Health Status, Regional Affiliation, Ethnicity, Occupational Background, Marital Status)
- **Status**: `AUDIT COMPLETE / CRITICAL DEFECTS IDENTIFIED / PUBLICATION & EXPERIMENT BLOCKED`
- **Full Report**: [`docs/audits/2026-10-27_seven_categories_independent_quality_audit.md`](file:///d:/Research-BanglaBBQ/docs/audits/2026-10-27_seven_categories_independent_quality_audit.md)
- **Mode**: `STRICT READ-ONLY / ZERO DATASET MUTATION`

---

## 1. Executive Summary

A comprehensive, evidence-driven, read-only quality audit was performed across all seven newly imported categories under `Dataset_BanglaBBQ_New/` (14 JSONL files, 20,160 total rows / 10,080 rows per language; 302,400 live Google Spreadsheet cells).

While all 14 files achieve 100% offline invariant pass rates across structural schemas, 480/480/480 gold label counts, and 6-way answer permutations, the audit uncovered **fatal hidden positional biases, source credibility deficits, and major demographic coverage blindspots** that block publication readiness and invalidates immediate LLM benchmarking.

---

## 2. Key Forensic Discoveries

1. **Fatal First-Mentioned Person Bias (P0 across 4 Categories)**:
   - In **Physical Appearance**, **Health Status**, **Ethnicity**, AND **Regional Affiliation**, **100.0% of disambiguated negative examples (360/360 per category; 1,440 records/lang; 2,880 total)** have the first-mentioned person as the gold label!
   - In **100.0% of disambiguated non-negative examples (360/360 per category)**, the second-mentioned person is the gold label!
   - Any LLM evaluated on these four categories will achieve 100% disambiguated accuracy via a trivial positional heuristic without processing scenario semantics.
2. **Hidden 2:1 Per-Theme Skews in Remaining 3 Categories**:
   - In **Social Status**, **Marital Status**, and **Occupational Background**, while macro totals sum to ~180/180, **every individual theme exhibits an uncorrected 2:1 or 1:2 positional skew (24:12 or 12:24)**. The generators merely alternated the bias direction between odd and even themes to create the illusion of balance at the aggregate level.
   - In Occupational Background, Theme Q07 (Tea Garden) remains fundamentally confounded with ethnic/caste identity, and Theme Q10 (Farmers) cites a peasant aspiration survey that fails to support the asserted discrimination scenario.
3. **Complete Erasure of Mental Health**:
   - The seniors' original thesis category `Mental Health` (100 rows covering clinical depression, schizophrenia, and bipolar disorder) has **0 records** in the modernized 12-category benchmark; it was entirely replaced by somatic/chronic physical diseases.
4. **Extreme Demographic & Thematic Skew in Marital Status**:
   - **100% of scenarios feature pairs of women** (0 male scenarios; bachelor men housing refusal is completely absent).
   - 30% of the entire category (432 records) is dedicated to a hyper-localized wildlife-conflict stigma ("Tiger Widows" in Satkhira).
5. **Synthetic Dehumanization in Ethnicity**:
   - All scenarios use artificial tokens (`Munda student A` / `ethnic Bengali student B` / `শিক্ষার্থী ক` / `শিক্ষার্থী খ`) rather than authentic personal names.
6. **Satirical & Lifestyle Citations**:
   - `Regional Affiliation` cites *The Daily Star Shout* teen satire humor columns for Noakhali, Cumilla, and Tangail stereotypes.
   - `Physical Appearance` imports Western Afro-textured hair bias into Bangladesh (`HairTexture` curly hair) citing a beauty blog on the "Curly Girl Method".

---

## 3. Mandatory Remediation Sequence

1. **Phase 1 (P0 Blocking)**: Eliminate the 100% first-person positional shortcut across Physical Appearance, Health Status, and Ethnicity; balance Occupational Background per theme.
2. **Phase 2 (High)**: Humanize Ethnicity entity names; restore Mental Health coverage; balance Marital Status with male bachelor housing discrimination; disaggregate Social Status.
3. **Phase 3 (Medium)**: Replace satire/lifestyle citations with empirical sociological literature; conduct independent native speaker colloquial linguistic review.

**Scientific Verdict**: Strictly blocked for LLM benchmark experiments until Phase 1 and Phase 2 remediation is formally reviewed and approved by lead researchers.
