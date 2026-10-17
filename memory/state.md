# state.md — Current Verified Progress Dashboard

**Last Verified Date**: 2026-10-17  
**Latest Verified Data/Research Commit**: `07d4b46edc69988a3572f10a6555825f6204b7bb` (Religion evidence QA follow-up: 24 English Q18 context grammar repairs; synchronization with live Google Sheets, corrected research documentation).  
**Latest Memory Synchronization**: 2026-10-17, through `07d4b46` (follow-up source-scope and language QA); this header refresh is committed subsequently.  
**Current Milestone**: Politics remains at 2,880 records per language; Religion remains at 960 per language with 40 new bilingual wording candidates drafted in a separate review tab (not integrated); Age accepted for current phase; other six categories pending.

---

## 1. Benchmark Status Dashboard across All 9 Categories

| Bias Category | English Count | Bengali Count | Status Marker | Current Working Status & Verification Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Politics** | 2,880 | 2,880 | `IN PROGRESS` | **20 themes, 144 records/theme/language** = original 48 + wording v2 (48) + wording v3 (48). Original IDs 0–959 preserved; appended IDs 960–2879. Full 6-way answer permutations, balanced labels 960/960/960, counterfactual reversals, zero exact QA duplicates and bilingual structural parity verified. Approved targeted QA content repairs applied and synchronized across live Google Sheets and canonical GitHub JSONL: Q5 (144 rows/lang qualified with year 2022), Q14 (72 neg rows/lang question text refined to remove false expulsion premise), Q19 (144 Bengali rows aligned to government critic terminology 'সরকার-সমালোচক'). Validator and assembler updated to support dual-hash verification (preserving historical baseline hashes as evidence) and 100% bit-for-bit parity confirmed (43,200 cells/lang). **Outstanding**: Independent natural Bengali translation/entailment review, source-relevance audit and correlated-paraphrase evaluation safeguards. Not publication-ready. |
| **Religion** | 960 | 960 | `IN PROGRESS` | **20 themes (Q1–Q20)**, 48 rows/theme, 1,920 total records. Approved targeted QA content repairs synchronized across live Google Sheets and canonical GitHub JSONL (528 ENG, 504 BEN rows patched across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20). Includes Q3 equal water access premise, Q5 nonreligious vs observant Muslim terminology, Q7 cultural-festival community-service proposal framing, Q8 Hindu/Muslim clerical job denial (source is the US Department of State 2021 report hosted by ecoi.net), Q9/Q10 secondary school academic source, Q12/Q13 MRG public exclusion source, Q18 Feni flood relief grounding, and Q20 Chittagong government high school admission restrictions. 100% bit-for-bit parity confirmed (14,400 cells/lang). 10/10 invariant checks passed. Pre-QA-fix backups preserved in hidden live sheets and Git branch `backup/religion-pre-qa-repair-20261017`. **Outstanding**: Q3 caste-vs-religion comparison; Q8 job-hiring evidence specificity; Q9/Q10 debate selection citations; Q12/Q13 wedding-specific evidence; independent native Bengali linguistic review. Q18 English article repair applied in live Sheets and repair branch on 2026-10-17. **Review-only V2/V3 proposal (2026-10-17):** `Review_Religion_20_Variations` (gid `1743426767`) and `BanglaBBQ_Religion/review_v2v3_20261017.json` now contain 20 source-context rows plus 40 bilingual paraphrase candidates; Q3, Q8, Q9–Q10, Q12–Q13 are flagged for source review. No V2/V3 records appended; counts remain 960/language, and live Sheets vs canonical GitHub JSONL still match all 14,400 cells/language. Candidate wording, bilingual entailment and sources require review before authorization to expand to 2,880/language. Not publication-ready. |
| **Age** | 2,920 | 2,920 | `IN PROGRESS` | **Accepted for Current Research Phase**. 2,920 English and 2,920 Bengali records across 20 themes in Google Sheet `BanglaBBQ_BEN_Age` and `BanglaBBQ_BEN_New/Age.jsonl`. 100% unique context parity with English across all 20 themes (1,460 unique contexts). All structural repairs and context alignments preserved: Q1 (16/16), Q3 (36/36), Q8 (100/100), Q9 (144/144), Q10 (168/168), Q11 (84/84), Q12 (84/84), and Q19 (140/140). Age Q2 (IDs 32–127, 96 rows/language) was reviewed for grandparent terms, age references, and phrasing; **the researcher explicitly decided to leave Q2 and the entire Age dataset unchanged for now**. No additional Age edits are authorized. **Outstanding for Publication Readiness**: Independent native Bengali linguistic naturalness review and cross-language cultural alignment decision for English source. Exemplar rows in `Review_Age_20_Templates` flagged for future update. |
| **Gender Identity** | 506 *(legacy)* | 506 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Gender_identity/` and `BBQ/BanBBQ_.../Gender_identity.jsonl`. Requires category-level forensic audit, permutation expansion, and Google Sheet integration. |
| **Physical Appearance** | 1,106 *(legacy)* | 1,123 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Physical_appearance/` and `P_A_E/`. **Known Defect**: 17-record mismatch between English and Bengali legacy sets. Requires category-level audit, reconciliation, and permutation balancing. |
| **Regional Affiliation** | 51 *(legacy)* | 51 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Regional/`. **Known Defect**: Severely underpowered sample size (only 51 entries). Requires comprehensive expansion across Bangladeshi district stereotypes with source backing. |
| **Educational Background** | 128 *(legacy)* | 128 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Educational background/`. Requires category-level audit, scenario expansion, 6-way answer permutation balancing, and source grounding. |
| **Marital Status** | 100 *(legacy)* | 100 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Marital Status/`. Requires category-level audit, expansion beyond 100 rows, permutation balancing, and cultural grounding. |
| **Mental Health** | 100 *(legacy)* | 100 *(legacy)* | `PENDING` | Baseline files in `Dataset_ BanglaBBQ_Old/Mental Health/`. Requires category-level audit, clinical/social scenario expansion, and permutation balancing. |

> **Status Marker Definitions**:
> - `VERIFIED COMPLETE`: Structurally and semantically validated, verified against pre-expansion baselines, synchronized between Google Sheets and GitHub, passing automated CI.
> - `IN PROGRESS`: Dataset expanded and structurally validated; pending secondary linguistic, cultural, or source verification.
> - `PENDING`: Baseline files cataloged; awaiting dedicated category audit and modernization.
> - `UNVERIFIED`: Claim or dataset not yet verified against primary evidence.
> - `BLOCKED`: Work halted due to dependencies or missing external artifacts.

---

## 2. Google Spreadsheet Working Tabs

**Master Spreadsheet ID**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`  
**Master Spreadsheet Link**: [https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)

| Sheet Title | Sheet ID | Tab Index | Active Rows | Description |
| :--- | :---: | :---: | :---: | :--- |
| `Review_Age_20_Templates` | `99887766` | 0 | Header + Samples | Executive 3-column review tab comparing PakBBQ English vs Legacy Thesis vs Hasin's Bengali translations. *(Contains older exemplar rows; do NOT modify without approval).* |
| `review_20_politics_templates` | `1636577158` | 1 | 21 (20 themes) | Existing Politics Q1–Q20 disambiguated context exemplars comparing current English, original thesis Bengali (Q1–Q5), and current Bengali. Review-only; production datasets untouched. |
| `Review_Politics_20_Variations` | `722176577` | 2 | 21 (20 themes) | Side-by-side original/V2/V3 bilingual contexts Q1–Q20; user authorized integration of 40 additional bilingual wording pairs into the active dataset on 2026-10-17. Independent linguistic/source review still outstanding. |
| `Review_Religion_20_Variations` | `1743426767` | 13 (verified 2026-10-17) | 21 (20 themes) | Original Religion disambiguated contexts plus proposed English/Bengali V2/V3 variants, 40 candidate pairs. **Review only**; amber source-relevance flags in Q3, Q8, Q9–Q10 and Q12–Q13. |
| `PakBBQ_ENG_Age` | `0` | 3 | 2,921 (2,920 data) | Complete English Age benchmark source pool imported from PakBBQ. |
| `BanglaBBQ_BEN_Age` | `1006819770` | 4 | 2,921 (2,920 data) | Complete Bengali Age benchmark updated with Q1 context alignment, Q9 technology alignment, Q19 semantic signer/youth repairs, and Q3, Q8, Q10, Q11, Q12 lexical distinctions. 100% unique context parity with English. |
| `BanglaBBQ_ENG_Politics` | `1888499205` | 5 | 2,881 (2,880 data) | Expanded active Politics English; exact live read-back against GitHub 480-row versioned shards, 144 records/theme. |
| `BanglaBBQ_BEN_Politics` | `2128232344` | 6 | 2,881 (2,880 data) | Expanded Bengali Politics benchmark, 144 records/theme, original answers and labels preserved, 100% structural and source-shard value read-back. |
| `BanglaBBQ_ENG_Religion` | `804112545` | 7 | 961 (960 data) | Active English Religion benchmark across 20 themes (formerly Phase 2, promoted after backup). |
| `BanglaBBQ_BEN_Religion` | `860941009` | 8 | 961 (960 data) | Active Bengali Religion benchmark across 20 themes (formerly Phase 2, promoted after backup). |
| `Backup_Politics_ENG_preV2V3_20261017` | `1140714802` | 9 (hidden) | 1,000 grid (960 data) | Untouched pre-expansion English Google Sheets snapshot, 15-column records and native formatting. |
| `Backup_Politics_BEN_preV2V3_20261017` | `1323539476` | 10 (hidden) | 1,000 grid (960 data) | Untouched pre-expansion Bengali Google Sheets snapshot. |

*Note: Worksheets for the remaining 6 categories will be created systematically as each category undergoes its dedicated audit and expansion.*

---

## 3. Active GitHub Dataset Directories

| Category | Canonical Directory | Primary Files | Record Count |
| :--- | :--- | :--- | :---: |
| **Politics** | [`BanglaBBQ_Politics/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Politics) | `banglabbq_politics_english.jsonl`<br/>`banglabbq_politics_bengali.jsonl` | 2,880 ENG<br/>2,880 BEN |
| **Religion** | [`BanglaBBQ_Religion/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion) | `Religion_eng.jsonl`<br/>`Religion_bng.jsonl` | 960 ENG<br/>960 BEN |
| **Age** | [`BanglaBBQ_BEN_New/`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New)<br/>Root | `Age.jsonl`<br/>`PakBBQ_Age_English.csv` | 2,920 BEN<br/>2,920 ENG |

---

## 4. Completed Work

- [x] Formally reviewed Age Q2 (IDs 32–127) for translation issues involving grandparent terminology, age references, and context phrasing; researcher explicitly decided to leave Q2 and the entire Age dataset unchanged for the current research phase.
- [x] Formally accepted Age benchmark for current research phase (2,920 records per language) with no further dataset modifications authorized.
- [x] Cloned and integrated official PakBBQ repository baseline (`PakBBQ_Repo`).
- [x] Generated Excel-ready CSV for Age (`PakBBQ_Age_English.csv`, 2,920 rows).
- [x] Created 3-column comparative review tab `Review_Age_20_Templates` in master Google Sheet.
- [x] Translated all 2,920 Age rows to conversational Bengali in Google Sheet `BanglaBBQ_BEN_Age` and exported to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Corrected Bengali family terms (Grandma/Grandpa -> নানা/নানি, Grandparent/Grandchild -> দাদু/নাতিটি) and Q7 comparative formulation.
- [x] Synchronized live Google Sheets updates for Age Q1 (IDs 0–31) context diversity (expanded from 11 to 16 unique contexts) to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Synchronized live Google Sheets updates for Age Q9 (IDs 912–1199) context diversity (expanded from 60 to 144 unique contexts) and aligned 272 answer choices in columns H–J to `BanglaBBQ_BEN_New/Age.jsonl`.
- [x] Repaired semantic mistranslation in Age Q19 (IDs 2360–2639) correcting 88 disambiguated rows where neighbor was incorrectly substituted for friend (48 rows) and someone else (40 rows).
- [x] Resolved lexical youth collapses in Age Q19 and Q8 distinguishing "The teen" (`কিশোরটি`) and "The teenager" (`কিশোরবয়সী ছেলেটি`).
- [x] Resolved lexical collapses in Age Q3 distinguishing "The Zoomer" (`জেন-জি প্রফেসর`) and "The Gen-Z kid" (`জেন-জি তরুণ প্রফেসর`).
- [x] Resolved lexical collapses in Age Q10, Q11, and Q12 distinguishing "The high schooler" (`স্কুলপড়ুয়া শিক্ষার্থীটি`) and "The high school student" (`হাই স্কুলের শিক্ষার্থীটি`).
- [x] Realigned "fights" (`মারামারিতে জড়ান/জড়ায় না`) vs. "confrontations" (`কারো সাথে ঝামেলায় জড়ান/জড়ায় না`) in Age Q11 and Q12 disambiguated contexts.
- [x] Achieved 100% unique context parity between English and Bengali across ALL 20 Age themes (Q1–Q20) with 332 total modified records.
- [x] Audited Pakistani cultural and geographic entities across TM records Q13–Q20 (IDs 1872–2919) and verified authentic Bangladeshi localizations in Bengali.
- [x] Developed and executed 10-invariant QA verification script `scripts/sync_and_validate_age.py` confirming 100% compliance across all 2,920 records.
- [x] Established permanent `research_logs/` infrastructure with dedicated logs for Q1, Q9, Q19 semantic repairs, Q3/Q8/Q10–Q12 lexical repairs, and the cultural localization audit.
- [x] Audited, corrected, and expanded Politics benchmark through multiple phases (112 -> 160 -> 120 -> 240 -> 960 records).
- [x] Created `review_20_politics_templates` as a 20-theme bilingual Politics reference worksheet. Original thesis Bengali contexts are available only for Q1–Q5.
- [x] Created `Review_Politics_20_Variations` (21 rows, 4 columns) with original Q1–Q20 bilingual contexts plus 40 English–Bengali wording candidate pairs; on explicit 2026-10-17 approval, generated two full 48-record blocks/theme/language and integrated them with the active Politics datasets. Original 960 records per language were preserved exactly.
- [x] Established 20 source-referenced Politics themes (Q1–Q20) with 48 records per wording block (144 records/theme after adding v2 and v3), preserving original Q1–Q5 unchanged.
- [x] Aligned 720 Bengali `answer_info` records and corrected Bengali administrative translations in Politics.
- [x] Built comprehensive 10-invariant offline test suites: `scripts/validate_politics_dataset.py` and `scripts/validate_religion_dataset.py`.
- [x] Configured GitHub Actions CI workflow (`.github/workflows/validate.yml`) validating both benchmarks on push/PR.
- [x] Preserved legacy baseline datasets in `Dataset_ BanglaBBQ_Old/` with byte-for-byte integrity.
- [x] Backed up all 4 Religion worksheets (Phase 1 & Phase 2) to versioned GitHub backup `backups/religion_sheets_backup_20261016/`.
- [x] Promoted Phase 2 Religion (20 themes * 48 records = 960 records each) as active benchmark in `BanglaBBQ_Religion/` and live Google Sheets.
- [x] Cleaned up master Google Sheet by safely deleting archived Phase 1 Religion sheets after backup verification.
- [x] Reconciled and documented all automated research, migration, and audit scripts in `scripts/`.
- [x] Verified live Google Sheets and versioned GitHub snapshots for Politics, Religion, and Age before expansion; afterward verified all 1,920 appended Politics rows/language against the 15-column GitHub expansion shards in 240-row batches and verified CI-assembled canonical snapshots with original baselines.
- [x] Synchronized approved Religion QA repairs across live Google Sheets (`BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion`) and canonical GitHub JSONL files (528 ENG, 504 BEN rows patched across Q2, Q3, Q4, Q5, Q7, Q8, Q9, Q10, Q12, Q13, Q18, Q20). Confirmed 100% bit-for-bit parity across all 960 rows x 15 columns (14,400 cells/lang) via Google Sheets API v4. Verified all 10 invariant checks and counterfactual reversibility. Authored `research_logs/2026-10-17_religion_qa_repair.md`.

---

## 5. In-Progress Work & Research-Quality Blockers

### A. Age Benchmark Phase Acceptance & Outstanding Publication Considerations
- **Accepted for Current Research Phase**: The 2,920-record bilingual Age benchmark is formally accepted for the current research phase. No further dataset edits are authorized.
- **Age Q2 Status**: Reviewed for grandparent terminology and context phrasing; explicitly left unchanged by researcher decision.
- **Independent Bengali Linguistic Review (Outstanding)**: Review Bengali phrasing across all 20 themes for authentic colloquial naturalness with independent native Bangladeshi speakers before final publication certification.
- **English Cultural Modernization Decision (Outstanding)**: Bengali benchmark is already localized (Shwapno, Pathao, Tasty Treat, Dhaka, Chittagong), while English retains Pakistani names (Imtiaz, InDrive, Jalal Sons, Lahore, Karachi). A final editorial decision is pending on whether to modernize the English source to match Bengali or preserve it as a cross-country baseline.
- **Review Worksheet Exemplar Outdated**: The `Review_Age_20_Templates` sheet currently holds older exemplar rows. Retained untouched per protocol; do not modify without separate authorization.

### B. Religion QA Repairs & Outstanding Publication Considerations
- **QA Repairs & Live Parity Complete**: Content repairs applied across Q2–Q20 (Q3 water access equal claim, Q5 nonreligious/devout alignment, Q7 civic project reframing, Q8 clerical job denial, Q9/Q10 academic classroom inclusion citations, Q12/Q13 MRG public exclusion citations, Q18 Feni flood relief grounding, Q20 Chittagong high school admission quota grounding). 100% bit-for-bit parity verified with live production sheets `BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion`.
- **Source Relevance Boundary (Formalized)**: Forensic classification completed across all 20 themes. Crucial methodological boundary established: cited institutional reports (ECOI, MRG, Academic studies) substantiate macro socio-cultural discrimination patterns, not literal historical occurrences of fictional micro-vignettes.
- **Independent Bengali Linguistic Naturalness (Outstanding)**: Colloquial review with native speakers across complex religious and caste terminology is still required prior to final publication submission.
- **Publication Status**: **NOT publication-ready** until secondary human linguistic certification is completed.

### C. Category-Level Audits for Remaining 6 Categories
- **Immediate Priority**: `Gender Identity`, `Physical Appearance`, `Regional Affiliation`, `Educational Background`, `Marital Status`, and `Mental Health` currently reside only in `Dataset_ BanglaBBQ_Old/`.
- Each category requires:
  1. Detailed inventory of existing legacy files and discrepancy analysis (e.g., resolving the 1,106 vs. 1,123 row count in Physical Appearance).
  2. Thematic design and source gathering for authentic Bangladeshi socio-cultural contexts.
  3. Generation of 48-record blocks across 2 orientations * 2 conditions * 2 polarities * 6 permutations.
  4. Migration to dedicated Google Sheet tabs with canonical styling.
  5. Export to versioned GitHub JSONL directories.
  6. Integration into CI test suite.

---

### D. Politics V2/V3 Wording Expansion (Structurally Validated; Human Review Outstanding)
- **Authorized**: The user explicitly requested adding both additional wording versions to all 20 Politics themes on 2026-10-17. Candidate texts came from `Review_Politics_20_Variations` (Google Sheet `gid=722176577`).
- **Counts**: 2,880 English + 2,880 Bengali active rows (20 themes x 3 wording versions x 48 answer-permutation examples). Old canonical 960-row prefix and Q1–Q5 hash invariants preserved exactly; appended IDs 960–2879.
- **QA and synchronization**: Live Google Sheets expansion compared cell-by-cell with eight GitHub shards. Balanced 960/960/960 labels, no exact duplicate QA tuples, full permutations and theme-polarity-condition balances, bilingual metadata equality verified. GitHub Actions `Materialize BanglaBBQ Politics V2/V3 Expansion` passed and committed expanded canonical JSONL at `cab9f72b6c969e19b4c97bd16b293986e4a2b771`; automated validation on staging commit `31c13939465fc146ab01a47fbb3c9043c796261d` also passed.
- **Provenance/backup**: Frozen GitHub originals at `backups/politics_pre_wording_v2v3_20261017/`; hidden Sheets backups `Backup_Politics_ENG_preV2V3_20261017`/`Backup_Politics_BEN_preV2V3_20261017`; source-review templates in `BanglaBBQ_Politics/expansion_v2v3_20261017/`, including manifest and deterministic assembler script.
- **Review cautions**: New variants are fictional paraphrases, NOT new independently evidenced incidents. Independent native Bengali linguistic review, strict EN/BN semantic entailment review, case-specific source relevance verification and grouped evaluation splits remain outstanding. **Not publication-ready**.

---

### E. Politics Q5/Q14/Q19 Approved Fixes & Live Synchronization (Verified Parity)
- **Authorized**: Researcher approved three targeted QA repairs: (1) Q5 historical qualification with year 2022 (144 records/lang), (2) Q14 negative question refinement removing unsubstantiated university expulsion premise (72 records/lang), and (3) Q19 Bengali option/context terminology alignment to government critic `সরকার-সমালোচক` (144 Bengali records).
- **Google Sheets & GitHub Parity**: Applied by ChatGPT to live sheets `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics`. Local Git synchronization completed via `scripts/apply_politics_q5_q14_q19_fixes.py` (resolving remote GitHub connector timeout). 100% bit-for-bit parity confirmed across all 2,880 records (43,200 cells per language) via Google Sheets API v4.
- **Validator & Assembler Harmonization**: Updated `scripts/validate_politics_dataset.py` with dual-hash verification (preserving historical baseline hashes as evidence while supporting post-repair hashes for active benchmark). Updated `scripts/assemble_politics_expansion.py` with CRLF normalization and recognized post-repair canonical records.
- **Backups Preserved**: Historical thesis files (`Dataset_ BanglaBBQ_Old/Politics/`), pre-expansion backups (`backups/politics_pre_wording_v2v3_20261017/`), and pre-fix live sheets (`Backup_Politics_ENG_preQAfix_20261017`, `Backup_Politics_BEN_preQAfix_20261017`) preserved untouched.
- **Publication Status**: **NOT publication-ready**. Independent native-speaker Bengali linguistic review and external source-relevance verifications remain outstanding.
---

## 6. Next Recommended Actions

The primary active research priority is improving and expanding the six remaining categories:

1. **Gender Identity Audit & Thematic Design**: Conduct category-level forensic audit of legacy baseline files in `Dataset_ BanglaBBQ_Old/Gender_identity/`, audit bias dimensions, design authentic Bangladeshi thematic coverage, balance 6-way permutations, and initialize master Google Sheet integration.
2. **Physical Appearance Discrepancy Reconciliation**: Reconcile the 17-record mismatch between legacy English (1,106) and Bengali (1,123) baseline files, design balanced 20-theme architecture, and expand to canonical 48-record permutation structure.
3. **Regional Affiliation Benchmark Expansion**: Audit and expand the severely underpowered 51-sample legacy baseline into a robust multi-district benchmark covering recognized regional socio-cultural perceptions with source backing.
4. **Educational Background Modernization**: Audit legacy baseline (128 records), design expanded education/institution scenarios, balance permutations, and verify socio-cultural grounding.
5. **Marital Status Expansion**: Audit legacy baseline (100 records), develop realistic marital bias scenarios, balance 6-way permutations, and ensure cultural grounding.
6. **Mental Health Expansion**: Audit legacy baseline (100 records), expand clinical and societal bias scenarios, and balance permutations.
7. **Outstanding Publication-Readiness Audits (Religion & Age)**: Execute independent source relevance and naturalness audits for Religion (`scripts/audit_religion_sources_and_translation.py`); conduct independent native linguistic naturalness review for Age prior to publication submission.
