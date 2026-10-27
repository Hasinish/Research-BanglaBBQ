# Independent Forensic Quality Audit Verdict: Seven BanglaBBQ Benchmark Categories

**Audit Title**: Zero-Assumption Independent Source & Semantic Forensic Audit  
**Auditor Collective**: Senior NLP Benchmark Researcher, Bilingual Bangladeshi QA Engineer, Scientific Source-Verification Auditor  
**Date**: 2026-10-28  
**Repository**: [Hasinish/Research-BanglaBBQ](https://github.com/Hasinish/Research-BanglaBBQ)  
**Baseline Git Commit HEAD SHA**: `b4069d9cb9b20bf9466eb825ce7feacfb01d6fca`  
**Execution Mode**: Strictly Read-Only Dataset Forensic Audit (0 production mutations, 0 candidate mutations, 0 Google Sheets writes, 0 GitHub pushes)  

---

## 1. Executive Summary & Approval Recommendations

| Benchmark Artifact / Target Group | Volume (Rows per Lang) | Unique Semantic Cases | Structural Invariants | Semantic Grounding | Source Evidence Status | Official Approval Recommendation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Positional Candidates: Health Status** | 1,440 EN / 1,440 BN | 80 | **PASS (100%)** | Local PASS / Macro Skew | Partially Grounded | **STRUCTURALLY VALIDATED — SEMANTIC REVIEW PENDING** |
| **Positional Candidates: Regional Affiliation** | 1,440 EN / 1,440 BN | 80 | **PASS (100%)** | Synthetic Tokens | 2 Satire / 1 Historical | **BLOCKED — SOURCE OR SEMANTIC DEFECT** |
| **Positional Candidates: Ethnicity** | 1,440 EN / 1,440 BN | 80 | **PASS (100%)** | Synthetic Placeholders | General Reports | **BLOCKED — SOURCE OR SEMANTIC DEFECT** |
| **Content Prototype: Health Status (Q02, Q04, Q05, Q07)** | 576 EN / 576 BN | 96 | **PASS (100%)** | Confounder Neutralized | Verified PLOS/BMC | **SEMANTICALLY REVIEWED — NEEDS HUMAN VALIDATION** |
| **Content Prototype: Physical Appearance (Q02)** | 144 EN / 144 BN | 24 | **PASS (100%)** | Confounder Neutralized | Verified Heliyon | **SEMANTICALLY REVIEWED — NEEDS HUMAN VALIDATION** |
| **Content Prototype: Social Status (Q07 V3)** | 48 EN / 48 BN | 8 | **PASS (100%)** | Symmetrized Entailment | Verified Roelen et al. | **SEMANTICALLY REVIEWED — NEEDS HUMAN VALIDATION** |

> **Scientific Honesty Rule**: **NO DATASET IS DECLARED PUBLICATION-READY**. While automated structural checks and permutation closures pass 100%, severe content flaws (synthetic tokens in Ethnicity, satire citations in Regional, and complete omission of Mental Health) require mandatory human panel validation and lead researcher authorization before deployment.

---

## 2. Input Integrity & Cryptographic Hash Manifest

All 12 input JSONLs and documentation files were locked before the audit and verified unchanged upon completion:

| File Name | Record Count | File Size (Bytes) | SHA-256 Hash | Integrity Status |
| :--- | :---: | :---: | :--- | :---: |
| `candidates/BanglaBBQ_Health_Status_FINAL_english.jsonl` | 1,440 | 1,433,202 | `eacb118018cebf02492955b2e0b6ada05e96fa1e72bc23291c8f55156e377f11` | **UNCHANGED** |
| `candidates/BanglaBBQ_Health_Status_FINAL_bengali.jsonl` | 1,440 | 2,404,218 | `16996de2013f4a45bae46b99c3b6e8b4f5e99bfd2955247c079b507871350f60` | **UNCHANGED** |
| `candidates/BanglaBBQ_Regional_FINAL_english.jsonl` | 1,440 | 1,431,378 | `fcf4414af7ba9c88bbdf3112302e6976b7de8ba6e1e370f52ecab312677bbb49` | **UNCHANGED** |
| `candidates/BanglaBBQ_Regional_FINAL_bengali.jsonl` | 1,440 | 2,467,146 | `5846999cf4b4aab40fb3b8ab45d8a83cc81a2f82bc42413174a9c2acfe99a6bf` | **UNCHANGED** |
| `candidates/BanglaBBQ_Ethnicity_FINAL_english.jsonl` | 1,440 | 1,639,674 | `29a0849436ce630a035a60bb75d2bccba3acfcbf2bce747bd8cfcdb57a3ef86a` | **UNCHANGED** |
| `candidates/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl` | 1,440 | 3,041,106 | `1635587e621c5af4e008c40b0753a7e9f2d922d72703d6b4242b37676319d089` | **UNCHANGED** |
| `prototypes/Health_Status_Q02_Q04_Q05_Q07_prototype_english.jsonl` | 576 | 591,768 | `e23ecdc8de415cac046072b12b4727e363d5ce9fc65713ca6ed095504f9313fe` | **UNCHANGED** |
| `prototypes/Health_Status_Q02_Q04_Q05_Q07_prototype_bengali.jsonl` | 576 | 985,176 | `93275d67e38b4808c8ad382d2febc9f3865cfa2c77fc53013a39cbc1973d3b29` | **UNCHANGED** |
| `prototypes/Physical_Appearance_Q02_prototype_english.jsonl` | 144 | 166,800 | `57bf71414512fbf3fd68dee955b3d07bab57f051891226e98ca7f589185039d5` | **UNCHANGED** |
| `prototypes/Physical_Appearance_Q02_prototype_bengali.jsonl` | 144 | 274,896 | `fe93e23ef8e477a4909177f47abf5b84fc16d3cb4227c90c72aa7120dd7f3e5c` | **UNCHANGED** |
| `prototypes/Social_Status_Q07_V3_prototype_english.jsonl` | 48 | 59,112 | `e5e0f670538bde78d3d6dae66f83f942eb10eaceb30f2c0147f85ae4fe614b27` | **UNCHANGED** |
| `prototypes/Social_Status_Q07_V3_prototype_bengali.jsonl` | 48 | 102,624 | `6a9cb5c6de20aff8bb22a79991280f29192f1e97078e2a9035c34c61f199e41c` | **UNCHANGED** |

- **Confirmed Production Mutations**: Exactly 0 tracked files modified in `Dataset_BanglaBBQ_New/`.
- **Confirmed Candidate / Prototype Mutations**: Exactly 0 bytes altered across all 12 files.

---

## 3. Scientific Source & Citation Forensic Audit Findings

Exhaustive audit of all 70 themes across the 7 modernized categories generated `reports/source_claim_verification.csv` (21 columns):
- **Total Source Claims Inspected**: 70
- **Directly Supported**: 32 (45.7%)
- **Contextually Supported**: 31 (44.3%)
- **Historically Supported Only**: 2 (2.9%)
- **Unsupported (Satire / Lifestyle / False Leap)**: 5 (7.1%)
- **Full Text Inaccessible for Verbatim Verification**: 2 (2.9%)
- **Bibliographic Errors Identified**: 1 (Regional Q05 publication date corrected from 2024 to June 14, 2025)
- **Unverified Exact Quotation Claims Flagged**: 1 (Regional Q01 Schuman 1966)

### Explicit Deep-Dive Findings

1. **Regional Q01 (Howard Schuman 1966, DOI: 10.2307/2786297)**:
   - *Full Text Access*: Inaccessible in execution environment due to JSTOR Cloudflare/bot challenge (`Client Challenge` page returned).
   - *Alleged Page Quotations*: Unsupported. The previous agent claims citing exact quotes from "pages 431–435" could not be verified from primary source text. In accordance with Section 4.1, exact quote is marked empty (`""`), quote match marked `NOT_CHECKABLE`, and classification assigned as `HISTORICAL_ONLY`.
   - *Substantive Evidence*: Schuman (1966) conducted an attitude survey of 1,001 East Pakistani factory workers in 1963–1964 regarding perceived character traits. It did **NOT** conduct an experimental audit of commercial discrimination, and historical perceptions in 1966 East Pakistan do not establish contemporary 2026 economic discrimination without modern evidence.

2. **Regional Q05 (*The Daily Star* "Mofiz" Article)**:
   - *Inspected URL*: `https://www.thedailystar.net/slow-reads/big-picture/news/stereotypes-struggle-and-survival-reclaiming-the-story-behind-mofiz-3916331`
   - *Primary Text Verification*: Inspected directly (29 paragraphs, 49 occurrences of "Mofiz").
   - *Author & Date*: Authored by Saad Quasem, published **Saturday, June 14, 2025** (corrected from previous incorrect 2024 citation).
   - *Literal Supporting Text*:
     > "For a long time, people have made the derogatory word mofiz synonymous with the residents of the Rangpur region. ... Today, the mention of mofiz commonly implies a simpleton."
   - *Evidence Scope*: Directly supports the cultural existence, meaning ("simpleton"), and 1970s bus chit historical etymology of the "Mofiz" slur. It does **NOT** provide econometric audit data measuring hiring discrimination callback rates.

---

## 4. Prototype Semantic QA & Entailment Evaluation

Review of all 1,536 bilingual prototype records (768 EN, 768 BN) across 16 distinct 48-record blocks (128 unique semantic cases):

### 4.1 Health Status Prototypes (576 EN / 576 BN; 96 Semantic Cases)
- **Q02 (HIV Disclosure)**: Shifted from dental/clinic consultation to university research fellowship ranking. Eliminates doctor procedural infection-control confounder. Evaluator discrimination isolated. Flagged `NEEDS_CLINICAL_REVIEW` to ensure scholarship health declarations align with real institutional practices.
- **Q04 (Leprosy Treatment History)**: Shifted from afternoon tea dining to municipal archival manuscript cataloging. Eliminates salivary/food transmission misconceptions while preserving social stigma.
- **Q05 (COVID-19 Recovery)**: Shifted from physical cleanup to remote directory collation from home. Physically eliminates viral aerosol transmission fear.
- **Q07 (Arsenicosis Stigma)**: Shifted from public community meeting to phone-based agricultural survey verification. Eliminates visible skin lesion revulsion / leprosy confusion.
- *Structural Invariants*: 100% PASS (576 rows, labels 192/192/192, 48 rows/variation, 0 ambig leaks).

### 4.2 Physical Appearance Q02 Prototype (144 EN / 144 BN; 24 Semantic Cases)
- *Scenario*: Shifted from commercial television acting audition to commercial bank annual financial auditing.
- *Construct Validity*: Completely isolates aesthetic appearance from bona fide occupational qualifications (BFOQ).
- *Structural Invariants*: 100% PASS (144 rows, labels 48/48/48, 0 ambig leaks).

### 4.3 Social Status Q07 V3 Prototype (48 EN / 48 BN; 8 Semantic Cases)
- *Scenario*: Harmonized negative question (procedural relief resale/misuse) and non-negative question (verified eligibility compliance) around official distribution audit findings.
- *Construct Validity*: Replaces administrative certificate handover with symmetric compliance evaluation.
- *Structural Invariants*: 100% PASS (48 rows, labels 16/16/16, 0 ambig leaks).

---

## 5. Positional Balance & Simulation Findings

### 5.1 Candidate Positional Balances (Confirmed)
- **Health Status, Regional Affiliation, Ethnicity** (both EN and BN):
  - **Category Disambiguated NEG**: **180 First / 180 Second (50.0% / 50.0%)**
  - **Category Disambiguated NONNEG**: **180 First / 180 Second (50.0% / 50.0%)**
  - **Theme Residual Skew**: Exactly 12/24 or 24/12 across all 10 themes. Terminology strictly designated: `POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW (2:1)`.

### 5.2 Prototype Replacement Simulation (In-Memory Read-Only)
- **Physical Appearance Q02**: Baseline 180/180 -> Post-replacement **180/180** (0 regression).
- **Social Status Q07 V3**: Baseline 180/180 -> Post-replacement **180/180** (0 regression).
- **Health Status (Q02, Q04, Q05, Q07)**: When simulated against the 180/180 candidate, retains exact **180/180** category balance with 12/24, 12/24, 12/24, 24/12 across repaired themes.

---

## 6. High-Priority Failure Register

| Priority | Category / Theme | Affected IDs | Confirmed Problem | Severity | Recommended Repair | Approval Required |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| **P0** | **Ethnicity (All Themes)** | 0–1439 | Synthetic dehumanizing placeholders (`Student A`/`B`, `শিক্ষার্থী ক`/`খ`) used instead of authentic names. | **CRITICAL** | Replace with authentic ethnic names (`Ripon Chakma`, `Hopna Murmu`, `Bikash Munda`). | **YES** |
| **P0** | **Health Status (Category-wide)** | All | Complete omission of Mental Health (0 records in modernized benchmark). | **CRITICAL** | Restore 100-row thesis baseline or expand to dedicated 1,440-row Mental Health benchmark. | **YES** |
| **P1** | **Regional Affiliation (Q03, Q10)** | 96–143, 432–479 | Citing *Daily Star Shout* satirical humor columns as scientific proof of regional discrimination. | **HIGH** | Replace with verified anthropological/sociolinguistic studies. | **YES** |
| **P1** | **Occupational Background (Q10)** | 432–479 | Citing Islam & Begum (2023) on farmers' children leaving agriculture as proof of meeting facilitation bias. | **HIGH** | Replace Theme Q10 with documented agricultural discrimination or reframe theme. | **YES** |
| **P1** | **Occupational Background (Q07)** | 288–335 | Tea garden worker discrimination is ancestral/caste-bound, confounding occupation with ethnicity. | **HIGH** | Restructure theme or move under Ethnicity/Caste. | **YES** |
| **P1** | **Marital Status (Category-wide)** | 0–1439 | 100% female gender skew; 30% concentration on localized Sundarbans Tiger Widows. | **HIGH** | Introduce male bachelor rental housing refusal; reduce Tiger Widows to 10%. | **YES** |
| **P2** | **Physical Appearance (Q05, Q06)** | 192–239, 240–287 | Citing teen humor columns (Height) and lifestyle hair care blogs (Curly Girl method). | **MEDIUM** | Replace with documented colorism, acid attack survivorship, or burn scar discrimination. | **YES** |
| **P2** | **Social Status (All Themes)** | 0–1439 | Monolithic demographic label `People from low-income family backgrounds` across all 1,440 records. | **MEDIUM** | Disaggregate into slum dwellers, day laborers, and indebted families. | **YES** |

---

## 7. Final Scientific Auditor Sign-Off

All independent verification scripts, cryptographic hashes, and report artifacts are permanently preserved under:
`local_candidates/final_seven_category_qa/independent_source_semantic_audit/`
- Manifest: `input_manifest.json`
- Source audit: `reports/source_claim_verification.csv` & `reports/source_claim_discrepancies.md`
- Semantic audit: `reports/prototype_semantic_cases.csv` & `reports/prototype_failure_examples.md`
- Invariants: `reports/structural_invariants.json` & `reports/counterfactual_position_checks.csv`
- Review queue: `reports/bilingual_alignment_queue.csv`
- Final verdict: `reports/independent_final_verdict.md`

**FINAL DIRECTIVE**: AUDIT COMPLETE. 0 REPOSITORIES MUTATED. 0 DATASETS OVERWRITTEN. AWAITING RESEARCHER HUMAN PANEL REVIEW.
