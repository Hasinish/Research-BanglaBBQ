# Workspace Index

## Directory Structure & Detailed File Context

### Root Directory (`/`)
- `T2510616.pdf`: BRAC University undergraduate CSE thesis book (84 pages, completed June 2025). Titled *"A Bilingual Study of Socio-Cultural Bias in Large Language Models through BanglaBBQ and a Post Processing Mitigation Pipeline"* by Taeeba Tasnia, Ashika Habib Khan, Sumit Anthony Gomes, Tahseen Tanha, and Provat Saha (Supervisors: Dr. Muhammad Iqbal Hossain, Tawhid Anwar, Sifat Tanvir). Contains exhaustive literature review, benchmark definitions, socio-cultural annotation guidelines, Fleiss' Kappa formulas, detailed evaluation benchmarks across models, and ablation studies.
- `T2510616_IEEE_Paper.pdf`: 8-page IEEE conference-formatted paper draft. Formulates the BanglaBBQ benchmark (6,607 bilingual QA pairs across 9 bias categories) and the SafeLLM 3-stage inference-time bias mitigation pipeline (Sensitivity Layer -> Bias Evaluator -> Counterfactual Grounding). Key mathematical formulations include Fleiss' Kappa agreement:
  kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
  Accuracy formulations (Acc_ambig, Acc_disambig, Acc_neg, Acc_nonneg, Acc_DT, Acc_TM, Acc_NA), paired t-tests (t = 6.666 for English, t = 12.005 for Bengali), and Cohen's d effect size (d = 2.22 for English, d = 4.00 for Bengali). Evaluates LLaMA-3.1-8B, LLaMA-3.3-70B, LLaMA-4-Scout-17B, and Gemini 2.0 Flash-Lite.
- `PakBBQ_Age_English.csv`: Flattened, Excel-ready CSV export of the full 2,920 rows from `PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl` with UTF-8 BOM encoding for seamless spreadsheet import. Contains columns: `example_id`, `type`, `context_condition`, `question_polarity`, `context`, `question`, `ans0`, `ans1`, `ans2`, `label`.

---

### Dataset Root Directory (`Dataset_ BanglaBBQ_Old/`)
Legacy, fragmented raw dataset dumps from the original 5-member thesis team. Samples are structured in multiple-choice JSONL format with fields: `example_id`, `question_index`, `question_polarity` (neg / nonneg), `context_condition` (ambig / disambig), `category`, `answer_info` (dictionary mapping ans0/ans1/ans2 to stereotype tags), `additional_metadata`, `context`, `question`, `ans0`, `ans1`, `ans2`, `label`, `type` (DT, TM, NA), and `id`.

- `banbbq_ben_combined.jsonl`: Partially aggregated Bengali JSONL dataset (2,866 lines) compiled during initial thesis experiments.

#### Subdirectory: `Age/`
- `Age_Bengali_800entries.jsonl`: Bengali samples (799 entries) targeting age-related socio-cultural stereotyping (elderly vs youth capability/frailty).
- `Age_Eng.jsonl`: Expanded English age benchmark pool (2,920 entries) derived from BBQ adaptations.

#### Subdirectory: `AGE_ENG/`
- `Age.jsonl`: Curated 799-entry English age evaluation set matching the Bengali 799-entry counterpart.

#### Subdirectory: `Banglabbq/`
- `banglabbq_ben_combined.jsonl`: 850-entry aggregated Bengali multi-category subset used in early thesis smoke runs.
- `banglabbq_eng_combined.jsonl`: 850-entry aggregated English multi-category parallel subset.

#### Subdirectory: `BBQ/BanBBQ_BEN/` (Consolidated Bengali BBQ Categories)
- `Age.jsonl`: 799 entries covering age stereotyping in Bengali context.
- `Gender_identity.jsonl`: 506 entries evaluating gender stereotyping (traditional gender roles, occupations, societal judgment).
- `Physical_appearance.jsonl`: 1,123 entries evaluating appearance discrimination, skin complexion ("shyamla", "fair"), height, and body shaming.
- `Regional.jsonl`: 51 entries probing regional stereotyping across Bangladesh districts (Noakhali, Barisal, Chittagong, Sylhet, Old Dhaka).
- `Religion.jsonl`: 392 entries covering religious harmony, minority stereotyping, and communal perceptions in Bangladesh.

#### Subdirectory: `BBQ/BanBBQ_ENG/` (Consolidated English Parallel Categories)
- `Age.jsonl`: 799 parallel English entries on age bias.
- `Gender_identity.jsonl`: 506 parallel English entries on gender identity.
- `Physical_appearance.jsonl`: 1,106 parallel English entries on physical appearance.
- `Regional.jsonl`: 51 parallel English entries on regional stereotypes translated/adapted.
- `Religion.jsonl`: 392 parallel English entries on religious bias.

#### Subdirectory: `Educational background/`
- `banglabbq_education_bengali.jsonl`: 128 entries probing bias based on university tier (public vs private vs national university) and education medium.
- `banglabbq_education_english.jsonl`: 128 parallel English entries on educational hierarchy stereotypes.

#### Subdirectory: `Gender_identity/` (Raw member working folder)
- `Gender_identity_bng.jsonl`: 506 entries (raw working source matching `BBQ/BanBBQ_BEN/Gender_identity.jsonl`).
- `Gender_identity_eng.jsonl`: 506 entries (raw working source matching `BBQ/BanBBQ_ENG/Gender_identity.jsonl`).

#### Subdirectory: `Marital Status/`
- `Marital_status_Bengali_100entries.jsonl`: 100 entries probing social stigma around unmarried, divorced, or widowed individuals in Bangladesh.
- `Marital_status_Eng.jsonl`: 100 parallel English entries on marital status biases.

#### Subdirectory: `Mental Health/`
- `Mental_health_status_Bengali_100entries.jsonl`: 100 entries evaluating stigma against individuals with depression, therapy seeking, or psychiatric illnesses.
- `Mental_health_status_Eng.jsonl`: 100 parallel English entries on mental health stereotypes.

#### Subdirectory: `Physical_appearance/` (Raw member working folder)
- `Physical_appearance.jsonl`: 1,123 entries (Bengali working file matching `BBQ/BanBBQ_BEN/Physical_appearance.jsonl`).

#### Subdirectory: `Politics/`
- `banglabbq_politics_bengali.jsonl`: 112 entries evaluating partisan political stereotyping in Bangladesh.
- `banglabbq_politics_english.jsonl`: 112 parallel English entries on political affiliation stereotypes.

#### Subdirectory: `P_A_E/` (Physical Appearance English raw folder)
- `Physical_appearance.jsonl`: 1,106 entries (English working file matching `BBQ/BanBBQ_ENG/Physical_appearance.jsonl`).

#### Subdirectory: `Regional/` (Raw member working folder)
- `Regional_ban.jsonl`: 51 entries (working source for Bengali regional biases).
- `Regional_eng.jsonl`: 51 entries (working source for English regional biases).

#### Subdirectory: `Religion/` (Raw member working folder)
- `Religion_bng.jsonl`: 392 entries (working source for Bengali religion biases).
- `Religion_eng.jsonl`: 392 entries (working source for English religion biases).

---

### PakBBQ Cloned Repository (`PakBBQ_Repo/`)
The official PakBBQ benchmark repository (`Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA`, EMNLP 2025 / arXiv:2508.10186).
- `README.md`: Documentation on PakBBQ dataset generation, benchmark evaluation, and findings.
- `requirements.txt`: Python package dependencies.
- `Gemini_eval.py`: Evaluation scripts for Google Gemini API models.
- `GPT_and_DeepSeek_eval.py`: Evaluation scripts for OpenAI GPT and DeepSeek models.
- `Analysis/`: Data analysis notebooks and statistical scripts.
- `PakBBQ/PakBBQ_ENG/`: English benchmark files across 8 categories:
  - `Age.jsonl`: 2,920 entries (1,872 DT + 1,048 TM templates). This is the source pool Provat Saha assigned Hasin to adapt for BanglaBBQ!
  - `Disability_status.jsonl`: 1,380 entries.
  - `ENG-linguistic(language_formality_biases).jsonl`: 88 entries.
  - `Gender_identity.jsonl`: 4,696 entries.
  - `Physical_appearance.jsonl`: 1,368 entries.
  - `Regional.jsonl`: 944 entries.
  - `Religion.jsonl`: 400 entries.
  - `SES.jsonl`: 5,384 entries (Socio-Economic Status).
- `PakBBQ/PakBBQ_UR/`: Urdu benchmark files with parallel 1-to-1 translations across all 8 categories matching `PakBBQ_ENG`.

---

### Scripts Directory (`scripts/`)
Centralized directory containing all 43 automated research, migration, and verification scripts:
- `README.md`: Index and documentation of all scripts grouped by domain (Age migrations, Age audits, Politics expansion, Utilities).
- `apply_p1_p2_corrections.py`: Applies Grandparent/Grandchild (56 rows) and Q7 (48 rows) fixes to Google Sheets and JSONL.
- `audit_live_p1_p2.py`: Automated live Google Sheets audit validating P1 and P2 corrections.
- `apply_family_corrections.py`: Disambiguates Grandma/Grandpa (48 rows) into নানি/নানা.
- `audit_live_sheet_corrections.py`: Validates family term disambiguation on live Google Sheet.
- `expand_politics_to_160.py`: Expands Politics benchmark from 112 to 160 balanced rows.
- `apply_160_expansion.py`: Pushes 160-row Politics benchmark to Google Sheets.
- `fix_politics_color_coding.py`: Applies styling and executive color coding to Politics sheets.
- `refresh_google_token.py`: Handles Google OAuth token refresh and validation.
- Additional 34 forensic scanning, inspection, matrix validation, and simulation scripts.

---

### Memory Directory (`memory/`)
- `personality.md`: AI assistant personality and communication guidelines.
- `personal_info.md`: Detailed developer profile for Hasin Ishrak.
- `purpose.md`: Workspace mission, platform targets, research objectives, and publication roadmap.
- `state.md`: Live tracking of active goals, completed milestones, last session notes, and blockers.
- `history.md`: Chronological log of conversation summaries and session histories.
- `index.md`: Comprehensive map and contextual index of all workspace files, math foundations, and folder structures.
