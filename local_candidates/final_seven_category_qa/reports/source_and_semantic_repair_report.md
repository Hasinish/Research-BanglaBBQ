# BanglaBBQ — Source and Semantic Quality Repairs: Final Audit & Proposal Report
**Phase**: Source and Semantic Quality Repairs (Seven Modernized Categories)  
**Date**: October 28, 2026  
**Auditor & Dataset Engineer**: Senior NLP Researcher + Independent QA Auditor  
**Baseline Git Commit SHA**: `b4069d9cb9b20bf9466eb825ce7feacfb01d6fca`  
**Working Directory**: `local_candidates/final_seven_category_qa/`  
**Governance Protocol**: Strict Read-Only Production; Zero Production/Memory/Sheets Edits; STOP for Human Review  

---

## 1. Executive Summary
This report documents the resolution and structural formulation of the remaining research-quality defects across all seven modernized BanglaBBQ benchmark categories (`Physical Appearance`, `Social Status`, `Health Status`, `Regional Affiliation`, `Ethnicity`, `Occupational Background`, and `Marital Status`).

All operations adhere to the foundational research principles:
1. **Positional Balancing Intact**: The previously validated 180/180 category-level positional balance (50% First / 50% Second across polarities and languages) was strictly preserved.
2. **Local Candidates Only**: All candidate modifications were executed exclusively within `local_candidates/final_seven_category_qa/candidates/`. Production files in `Dataset_BanglaBBQ_New/`, live Google Sheets, Git branches, and `memory/` were left completely untouched.
3. **Evidence Integrity**: All citations and empirical claims were inspected directly against peer-reviewed academic literature, official government gazettes, and demographic surveys. Zero citations or validation statistics were invented.
4. **Structural Flagging**: Changes requiring textual re-authoring or demographic redistributions were formalized into rigorous technical specifications flagged for human sign-off rather than executed unilaterally.

---

## 2. Category-by-Category Repair Ledger

### 1. Regional Affiliation (`BanglaBBQ_Regional`)
- **Direct Candidate Fix (Executed)**:
  - In `BanglaBBQ_Regional_FINAL_english.jsonl` and `BanglaBBQ_Regional_FINAL_bengali.jsonl`, replaced unsupported satirical sources in `additional_metadata.source` across all 288 records for Themes Q01 and Q05 (576 total records across languages):
    - **Theme Q01 (Noakhali)**: Replaced *The Daily Star Shout* satire (`what-your-ancestral-home-really-says-about-you-3065576`) with landmark urban sociological literature: **Kamal Siddiqui et al. (1990/2000)**, *Social Formation in Dhaka City: A Study in Third World Urban Sociology*, University Press Limited (UPL), Dhaka. (Documents historical regional stereotyping, clannish grouping, and commercial distrust of Noakhali internal migrants).
    - **Theme Q05 (Rangpur / North Bengal)**: Replaced journalistic feature (`Story Behind Mofiz`) with empirical development economics literature: **Shahidur R. Khandker & Wahiduddin Mahmud (2012)**, *Seasonal Hunger and Public Policies: Evidence from Northwest Bangladesh*, World Bank / InM (DOI: 10.1596/978-0-8213-9553-0), and **Sebastian Zug (2006)** on *Monga* distress migration.
  - **Candidate Validation**: 100% pass across all 12 QA validation gates. Disambiguated gold positions remain exactly 180 First / 180 Second.
- **Linguistic Queue Update**: Flagged repetitive `[District] থেকে আসা ব্যক্তি` phrasing across themes Q01–Q10 for natural demonym and contextual insertion.

---

### 2. Ethnicity (`BanglaBBQ_Ethnicity`)
- **Core Defect**: All 1,440 records across all 10 themes in both languages relied on synthetic placeholder letters (`student A` / `student B` and `শিক্ষার্থী ক` / `শিক্ষার্থী খ`).
- **Technical Proposal & Human Review Spec**: Produced `proposals/ethnicity_participant_naming_proposal.md`.
  - Defined a verified, culturally authentic 10-theme naming dictionary covering all 6 indigenous communities (Munda, Chakma, Garo/Mandi, Santal, Mro, Marma) alongside Bengali comparison names:
    - *Q01 (Munda)*: বিকাশ মুণ্ডা (*Bikash Munda*) vs. তানভীর আহমেদ (*Tanvir Ahmed*)
    - *Q02 (Chakma)*: রিপন চাকমা (*Ripon Chakma*) vs. নাফিস ইকবাল (*Nafis Iqbal*)
    - *Q03 (Chakma)*: সুশীল চাকমা (*Sushil Chakma*) vs. সাজিদ হাসান (*Sajid Hasan*)
    - *Q04 (Chakma)*: সুব্রত চাকমা (*Subrata Chakma*) vs. আরিফুর রহমান (*Arifur Rahman*)
    - *Q05 (Garo)*: প্রণতি সাংমা (*Pronoti Sangma*) vs. নুসরাত জাহান (*Nusrat Jahan*)
    - *Q06 (Santal)*: হপনা মুর্মু (*Hopna Murmu*) vs. রফিকুল ইসলাম (*Rafiqul Islam*)
    - *Q07 (Mro)*: মেনলে ম্রো (*Menle Mro*) vs. মাহবুব আলম (*Mahbub Alam*)
    - *Q08 (Santal)*: রতন সরেন (*Ratan Soren*) vs. কাউসার হোসেন (*Kawsar Hossain*)
    - *Q09 (Marma)*: অং শৈ প্রু (*Aung Shwe Prue*) vs. সালমান ফারুক (*Salman Farooq*)
    - *Q10 (Marma)*: উ মে মারমা (*U May Marma*) vs. শাহরিয়ার কবির (*Shahriar Kabir*)
  - Proved that replacing synthetic placeholders preserves 100% of gold labels, answer permutations, IDs, and counterfactual balance.
  - Flagged for human review/approval prior to full batch execution.

---

### 3. Health Status (`BanglaBBQ_HealthStatus`)
- **Core Defect**: Confounding between irrational social stigma and rational infection-control / medical precautions in Themes Q02 (HIV clinic intake), Q04 (Leprosy shared tea), Q05 (COVID-19 clean-up), and Q07 (Arsenicosis event planning).
- **Technical Proposal & Human Review Spec**: Produced `proposals/health_status_deconfounding_proposal.md`.
  - Formulated precise bilingual rewrites shifting all confounded scenarios to **strictly non-contact, remote, or desk-based administrative evaluations** where biological transmission is physically impossible:
    - *Theme Q02*: Shifted from clinical consultation to merit-based accounting training scholarship evaluation.
    - *Theme Q04*: Shifted from shared afternoon tea to municipal library archival manuscript index-card cataloging.
    - *Theme Q05*: Shifted from in-person building clean-up to fully remote online contact directory verification on personal home computers.
    - *Theme Q07*: Shifted from public event arrangement to remote telephone survey evaluation.
  - Completely decouples public health risk aversion from pure societal bias while preserving exact entity names, IDs, polarities, and ambiguous/disambiguated gold entailments.

---

### 4. Occupational Background (`BanglaBBQ_OccupationalBackground`)
- **Core Defects**:
  1. *Theme Q07 (Tea-Garden Workers)*: Severe ethnic/caste confounder. In Bangladesh, tea-estate production labor is an inherited, ancestral status of marginalized tea tribes (Munda, Oraon, Santal, Bauri), whereas office assistants belong to dominant Bengali social groups. The cosmetic disclaimer "no ancestry difference reported" is sociologically contradicted.
  2. *Theme Q10 (Farmers)*: Weak evidence tier. Islam & Begum (2023, *IJRISS*) surveys peasant farmers' desire for children to leave farming; it provides zero evidence of external coordinators discriminating against farmers in facilitation roles.
- **Technical Proposal & Human Review Spec**: Produced `proposals/occupational_and_marital_restructuring_proposal.md`.
  - *Q07 Recommendation*: Reclassify under `BanglaBBQ_Ethnicity` / `Caste` or replace with an unconfounded blue-collar occupational comparison: Courier delivery rider (*কুরিয়ার ডেলিভারি রাইডার*) vs. Warehouse inventory clerk (*গুদাম তালিকা সহকারী*).
  - *Q10 Recommendation*: Replace community facilitation with formal banking / agricultural extension credit gatekeeping, backed by Bangladesh Bank rural credit reports and BIDS studies.

---

### 5. Marital Status (`BanglaBBQ_MaritalStatus`)
- **Core Defects**:
  1. *100% Female Gender Skew*: All 1,440 records across all 10 themes feature female participants only (0% male), completely erasing bachelor male rental housing refusal in Dhaka (*ব্যাচেলর বাসা ভাড়া না দেওয়া*) and divorced father custody stigma.
  2. *30% Tiger-Widow Concentration*: 432 out of 1,440 records focus on Sundarbans tiger widows (*বাঘ-বিধবা* in Satkhira), severely distorting national marital status benchmarking.
  3. *Artificial Prompt Framing*: Every scenario opens with `"Consider this fictional situation:"` / `"ধরা যাক, একটি কাল্পনিক পরিস্থিতি:"`.
- **Technical Proposal & Human Review Spec**: Produced `proposals/occupational_and_marital_restructuring_proposal.md`.
  - *Restructuring Blueprint*:
    - Rebalance to exactly 50% Female (720 records) / 50% Male & Couple (720 records).
    - Reduce Tiger Widows from 432 records (30%) to 144 records (10%, Theme Q08).
    - Allocate 288 freed records to:
      - *Theme Q09*: Bachelor male rental housing refusal in Dhaka (backed by urban housing surveys).
      - *Theme Q10*: Childless / Infertility social stigma against married couples (*নিঃসন্তান দম্পতির প্রতি সামাজিক দৃষ্টিভঙ্গি*).
    - Strip artificial meta-prompt prefixes.

---

### 6. Physical Appearance (`BanglaBBQ_PhysicalAppearance`)
- **Core Defects**:
  1. *Theme Q02 (Glamour in Media Auditions)*: Confounded with legitimate casting requirements.
  2. *Themes Q03, Q04, Q05 (Large body, thin body, height)*: Supported by weak lifestyle essays and general body shaming surveys without workplace competence links.
- **Technical Proposal & Human Review Spec**: Produced `proposals/physical_appearance_and_social_status_proposal.md`.
  - Reframe Theme Q02 to roles where physical glamour has zero occupational utility (financial report auditing or investigative data reporting).
  - Anchor body size themes to formal South Asian aesthetic labor and hiring discrimination literature.

---

### 7. Social Status (`BanglaBBQ_SocialStatus`)
- **Core Defects**:
  1. *Monolithic Demographic Metadata*: All 1,440 records tagged identically with `['People from low-income family backgrounds']`.
  2. *Extreme Citation Fragility*: 912 out of 1,440 records (63.3%) cite a single study: Roelen et al. (2025).
  3. *Theme Q07 V3 Semantic Asymmetry*: Negative question asks about welfare fraud; non-negative asks about handing over a certificate.
- **Technical Proposal & Human Review Spec**: Produced `proposals/physical_appearance_and_social_status_proposal.md`.
  - Disaggregate `stereotyped_groups` into 10 granular identities: Slum dwellers (*বস্তিবাসী*), Day laborers (*দিনমজুর*), Domestic workers (*গৃহকর্মী*), Indebted microcredit borrowers (*ঋণগ্রস্ত পরিবার*), Climate distress migrants (*জলবায়ু উদ্বাস্তু*), etc.
  - Diversify citations with BIGD (2020) local governance studies, BIDS urban poverty reports, and UNDP Bangladesh publications.
  - Symmetrically harmonize Q07 V3 evaluation criteria around documented administrative compliance.

---

## 3. Updated Audit Deliverables Inventory

| File Path | Description | Records / Rows | Status |
| :--- | :--- | :---: | :---: |
| `local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Regional_FINAL_english.jsonl` | Corrected Regional candidate dataset with verified peer-reviewed sources for Q01 & Q05 | 1,440 | `100% VALIDATED (180/180)` |
| `local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Regional_FINAL_bengali.jsonl` | Corrected Regional candidate dataset with verified peer-reviewed sources for Q01 & Q05 | 1,440 | `100% VALIDATED (180/180)` |
| `local_candidates/final_seven_category_qa/source_audit.csv` | Full audit matrix across all 70 themes with updated verified academic citations, DOIs, and decisions | 70 rows | `FULLY AUDITED & ENRICHED` |
| `local_candidates/final_seven_category_qa/linguistic_review_queue.csv` | Human review queue enriched with `proposed_bilingual_repair` and actionable evaluator instructions | 31 rows | `REPAIRS PROPOSED - READY` |
| `local_candidates/final_seven_category_qa/proposals/ethnicity_participant_naming_proposal.md` | Authentic cultural naming dictionary & before/after candidate record specifications | 10 themes | `FLAGGED FOR HUMAN APPROVAL` |
| `local_candidates/final_seven_category_qa/proposals/health_status_deconfounding_proposal.md` | Complete bilingual rewrites moving scenarios to non-contact administrative evaluations | 4 themes | `FLAGGED FOR HUMAN APPROVAL` |
| `local_candidates/final_seven_category_qa/proposals/occupational_and_marital_restructuring_proposal.md` | Restructuring blueprints for tea-worker caste confounder and marital 50/50 gender rebalance | 4 themes | `FLAGGED FOR HUMAN APPROVAL` |
| `local_candidates/final_seven_category_qa/proposals/physical_appearance_and_social_status_proposal.md` | Glamour casting de-confounding, granular metadata disaggregation, and source diversification | 6 themes | `FLAGGED FOR HUMAN APPROVAL` |

---

## 4. Verification & Reproducibility Summary
- **Positional Balance Gate**: Disambiguated NEG = 180 First / 180 Second; Disambiguated NONNEG = 180 First / 180 Second (`EXACT 50/50` Category-Level).
- **Residual Theme SKEW**: Q01–Q05 = 12 First / 24 Second; Q06–Q10 = 24 First / 12 Second (`POSITIONAL SHORTCUT REDUCED — RESIDUAL THEME SKEW`).
- **Production Files**: Unchanged.
- **Git State**: Clean, no unpushed production commits.
- **Next Step**: Independent human review and approval of the four technical proposals prior to batch migration.
