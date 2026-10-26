# Research-BanglaBBQ

A bilingual (English–Bengali) socio-cultural and political bias evaluation benchmark for Large Language Models (LLMs), culturally adapted and mathematically grounded following the BBQ (Bias Benchmark for QA) framework.

---

## 📌 Project Overview

This repository hosts the research assets, dataset manifests, validation tooling, and production datasets for **BanglaBBQ**:
1. **Age Bias Benchmark (`Age`)**:
   - **2,920 records** per language (Directly Translated and Target Modified).
   - 100% mathematical invariant parity with BBQ and PakBBQ standards.
   - Authentic, conversational Bangladeshi Bengali phrasing resolving kinship terms (`Grandma` -> `নানি`, `Grandpa` -> `নানা`, `Grandparent` -> `দাদু`, `Grandchild` -> `নাতিটি`).
2. **Political Bias Benchmark (`Politics`)**:
   - **20 source-backed themes** covering real-world institutional decisions and civil liberties documentation in Bangladesh (Human Rights Watch, Amnesty International, CPJ, UN Human Rights, Transparency International Bangladesh, Prothom Alo, SagePub).
   - **960 records** each in English and Bengali (1,920 total records).
   - Full 6-way answer permutations (3!) across 2 counterfactual orientations.
   - Canonical 4-row block sequence throughout (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`).
   - Perfectly balanced labels (320 / 320 / 320), 0 label errors, 0 duplicate QA pairs.
   - Complete bilingual alignment across all 10 structural/metadata fields.
3. **Religious Bias Benchmark (`Religion`)**:
   - **20 socio-cultural themes** representing documented religious minority contexts in Bangladesh (Hindus, Dalit Hindus, Ahmadiyya Muslims, Buddhists, Christians, Secular/Atheists).
   - **960 records** each in English and Bengali (1,920 total records) exported directly from Phase 2 worksheets.
   - 100% mathematical invariant parity: full 6-way answer permutations (3!), canonical 4-row block sequence (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`), uniform 320/320/320 label balance, and 0 duplicate records.
   - Synchronized live with Master Google Sheet tabs `BanglaBBQ_ENG_Religion` and `BanglaBBQ_BEN_Religion`.

---

## 📂 Repository Organization & Directory Guide

To ensure clean distinction between active production benchmarks, independent audits, candidate bundles, and historical archives:

```
├── BanglaBBQ_Age/                    # Canonical 2,920-record Age Bias Benchmark (English & Bengali)
├── BanglaBBQ_Politics/               # Canonical 2,880-record Political Bias Benchmark (20 themes, V1/V2/V3)
├── BanglaBBQ_Religion/               # Canonical 2,880-record Religious Bias Benchmark (20 themes, V1/V2/V3)
├── BanglaBBQ_Gender/                 # Canonical 4,696-record Gender Identity Benchmark (34 themes)
├── BanglaBBQ_EducationalBackground/  # Canonical 2,880-record Educational Background Benchmark (20 themes, V1/V2/V3)
├── BanglaBBQ_Ethnicity/              # Canonical 1,440-record Ethnicity Bias Benchmark (FINAL)
├── BanglaBBQ_HealthStatus/           # Canonical 1,440-record Health Status Bias Benchmark (FINAL)
├── BanglaBBQ_MaritalStatus/          # Canonical 1,440-record Marital Status Bias Benchmark (FINAL)
├── BanglaBBQ_OccupationalBackground/ # Canonical 1,440-record Occupational Background Bias Benchmark (FINAL)
├── BanglaBBQ_PhysicalAppearance/     # Canonical 1,440-record Physical Appearance Bias Benchmark (FINAL)
├── BanglaBBQ_Regional/               # Canonical 1,440-record Regional Affiliation Bias Benchmark (FINAL)
├── BanglaBBQ_SocialStatus/           # Canonical 1,440-record Social Status Bias Benchmark (FINAL)
├── audits/                           # Independent Forensic QA Complete Packages (7 categories)
│   ├── Ethnicity_forensic_QA_complete/
│   ├── health_status_complete_independent_forensic_QA/
│   ├── marital_status_independent_forensic_QA_bundle/
│   ├── occupational_background_forensic_QA_complete/
│   ├── physical_appearance_independent_forensic_QA_bundle/
│   ├── Regional_independent_forensic_QA_bundle/
│   └── banglabbq_social_status_forensic_QA_complete/
├── candidate_bundles/                # Pre-Audit Candidate Benchmark Bundles & Generators (7 categories)
│   ├── banglabbq_ethnicity_bundle/
│   ├── banglabbq_health_status_complete/
│   ├── banglabbq_marital_status_readonly_research_package/
│   ├── banglabbq_occupational_background_readonly_bundle/
│   ├── banglabbq_physical_appearance_readonly_research_bundle/
│   ├── banglabbq_regional_research_bundle/
│   └── banglabbq_social_status_complete/
├── docs/                             # Academic Papers & Historical Audit Reports
│   ├── papers/                       # Monograph (T2510616.pdf) & IEEE Draft (T2510616_IEEE_Paper.pdf)
│   └── reports/                      # Historical expansion and correction JSON reports
├── research_logs/                    # 30+ empirical investigation, audit, and semantic repair logs
├── Dataset_ BanglaBBQ_Old/           # Historical thesis working tree (preserved byte-for-byte)
├── PakBBQ_Repo/                      # Upstream PakBBQ baseline repository (EMNLP 2025)
├── scripts/                          # Automated validation, repair, and live sync engines
├── backups/                          # Versioned immutable pre-repair snapshots
├── memory/                           # Agent state dashboard, index, and audit trail
├── requirements.txt                  # Portable Python dependencies
└── CITATION.cff                      # Academic citation metadata
```

---

## ⚖️ Political Bias Benchmark: 20 Research Themes

Every theme is grounded in documented human rights investigations, investigative journalism, or academic literature. 

> **Important Distinction**: Real-world source documentation establishes the **sociological reality of differential institutional treatment** in Bangladesh. The benchmark scenarios themselves are **fictional, counterbalanced evaluation probes** that systematically pair a ruling-party-aligned entity and an opposition-aligned entity under identical circumstances to test whether LLMs exhibit stereotypical bias in ambiguous and disambiguated contexts.

| ID | Theme | Documented Institutional Practice | Source Document | Records |
|:---|:---|:---|:---|:---:|
| **Q1** | Police complaint follow-up | Differential police responsiveness to complaints filed by opposition vs ruling party activists | [HRW (2022)](https://www.hrw.org/news/2022/10/10/bangladesh-crackdown-political-opposition) | 48 |
| **Q2** | Bail decisions | Asymmetric denial of judicial bail for charged opposition members compared to ruling party affiliates | [HRW (2023)](https://www.hrw.org/news/2023/08/02/bangladesh-excessive-force-against-political-protesters) | 48 |
| **Q3** | Journalist press accreditation | Withholding or denial of official press cards for opposition-linked reporters | [CPJ (2023)](https://cpj.org/2023/11/journalist-shahed-alam-jailed-in-bangladesh/) | 48 |
| **Q4** | Ministry recruitment / shortlisting | Political vetting and exclusion of opposition-affiliated applicants in public recruitment | [Amnesty (2023)](https://www.amnesty.org/en/latest/news/2023/01/bangladesh-government-critics-face-arbitrary-detention/) | 48 |
| **Q5** | Social media criticism cases | Selective prosecution under digital security laws for critical posts against the government | [HRW (2023)](https://www.hrw.org/news/2023/02/09/bangladesh-digital-security-act-silences-dissent) | 48 |
| **Q6** | Political rally permission | Administrative refusal and venue denial for opposition rallies vs prompt approval for ruling party | [HRW (2023)](https://www.hrw.org/world-report/2023/country-chapters/bangladesh) | 48 |
| **Q7** | Unequal policing of demonstrations | Facilitation of ruling party marches vs baton charges and tear gas against opposition protests | [Amnesty (2023)](https://www.amnesty.org/en/latest/news/2023/08/bangladesh-unlawful-use-of-force-against-protesters-must-end-immediately/) | 48 |
| **Q8** | Travel security checkpoints | Police roadblocks at city entrances stopping, searching, and turning back opposition supporters | [HRW (2023)](https://www.hrw.org/news/2023/11/01/bangladesh-violence-erupts-amid-demands-fair-election) | 48 |
| **Q9** | Campaign equipment & posters | Confiscation of sound systems and tearing down of opposition campaign posters by law enforcement | [HRW (2018)](https://www.hrw.org/news/2018/12/22/bangladesh-violent-campaign-targets-opposition) | 48 |
| **Q10** | Polling booth obstruction | Physical obstruction of opposition voters at voting booths with claims votes were already cast | [HRW (2019)](https://www.hrw.org/news/2019/01/02/bangladesh-election-abuses-need-independent-probe) | 48 |
| **Q11** | NGO foreign grant clearance | Bureaucratic deregistration and bank account freezes targeting rights NGOs vs routine approvals | [HRW (2022)](https://www.hrw.org/news/2022/06/09/bangladesh-stop-punishing-human-rights-work) | 48 |
| **Q12** | Online news article removal | Administrative orders forcing removal of critical investigative reports under domain blocking threats | [HRW (2023)](https://www.hrw.org/news/2023/05/03/bangladesh-end-crackdown-against-journalists-and-critics) | 48 |
| **Q13** | Printing press declaration revocation | Revocation of newspaper printing declarations (e.g. *Dainik Dinkal*) under publications law | [CPJ (2023)](https://cpj.org/2023/02/bangladesh-shuts-down-main-opposition-newspaper-dainik-dinkal/) | 48 |
| **Q14** | University hall seat allocation | Allocation of dormitory seats by ruling student wing and forcible expulsion of dissidents | [Prothom Alo (2023)](https://en.prothomalo.com/bangladesh/politics/chhatra-league-decides-who-stays-where-in-the-halls) | 48 |
| **Q15** | Forced political rally mobilization | Guestroom intimidation and eviction threats against students resisting compulsory rally attendance | [Prothom Alo (2023)](https://en.prothomalo.com/bangladesh/hdr5whpl87) | 48 |
| **Q16** | Food ration & welfare cards | Partisan gatekeeping and tearing up of welfare applications of opposition-affiliated families | [SagePub (2020)](https://journals.sagepub.com/doi/10.1177/0021909620970581) | 48 |
| **Q17** | Municipal tender submission | Armed blocking of tender boxes preventing opposition contractors from bidding | [TIB (2023)](https://www.ti-bangladesh.org/en/articles/research/7211) | 48 |
| **Q18** | Hospital emergency care access | Plainclothes police intercepting and detaining injured opposition protesters in hospital wards | [UN OHCHR (2024)](https://bangladesh.un.org/en/289108-bangladesh-un-report-finds-brutal-systematic-repression-protests-calls-justice-serious) | 48 |
| **Q19** | Harassment of dissident families | Police interrogation and passport threats against relatives of expatriate critics | [HRW (2023)](https://www.hrw.org/world-report/2023/country-chapters/bangladesh) | 48 |
| **Q20** | Midnight residential raids | Midnight home searches and computer confiscations targeting opposition politicians without warrants | [HRW (2022)](https://www.hrw.org/news/2022/10/10/bangladesh-crackdown-political-opposition) | 48 |

---

## 🔬 Benchmark Verification & Reproducibility

### 1. Offline Automated Invariant Testing (No Credentials Needed)
To run the automated validation suite on clean environments:
```bash
# Clone the repository
git clone https://github.com/Hasinish/Research-BanglaBBQ.git
cd Research-BanglaBBQ

# Install dependencies
pip install -r requirements.txt

# Execute comprehensive offline test suites
python scripts/validate_politics_dataset.py
python scripts/validate_religion_dataset.py
```
This tests all 10 mathematical and semantic invariants:
1. Exact 960 records per language.
2. Sequential IDs 0–959 and 15-column schema integrity.
3. 20 themes with 48 records each, balanced across condition (24/24) and polarity (24/24).
4. Canonical 4-row BBQ block sequence throughout (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`).
5. Uniform label distribution: exactly 320 for label 0, 320 for 1, and 320 for 2.
6. Ambiguous QA pairs strictly resolve to "Unknown" (`অজানা`).
7. Disambiguated QA pairs logically proven by contextual evidence and counterfactual inversion.
8. 100% bilingual structural and metadata equality.
9. Zero duplicate QA records (960 completely unique tuples).
10. Byte-for-byte SHA-256 hash preservation of baselines.

### 2. Live Google Sheets Audit (Requires `token.json`)
```bash
python scripts/verify_politics_960_live.py
python scripts/verify_religion_live.py
python scripts/verify_exact_age_style.py
python scripts/audit_live_p1_p2.py
```

---

## 📜 Dataset Licensing Recommendation

- **Dataset**: Recommended under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Source Code & Tooling**: Recommended under the [MIT License](https://opensource.org/licenses/MIT).
- **Third-Party Attribution**: The Age benchmark is culturally adapted from [PakBBQ](https://github.com/Hashmat02/PakBBQ-A-Culturally-Adapted-Bias-Benchmark-for-QA) (Hashmat et al., EMNLP 2025), which is licensed under MIT. The overarching framework adheres to [BBQ](https://github.com/nyu-mll/bias-benchmark-for-qa) (Parrish et al., Findings of ACL 2022).

---

## 👥 Authors & Academic Attribution

- **Hasin Ishrak** — Researcher & Dataset Engineer, BRAC University
- **Provat Saha** — Co-Author & Thesis Researcher, BRAC University
- **Taeeba Tasnia**, **Ashika Habib Khan**, **Sumit Anthony Gomes**, **Tahseen Tanha** — Co-Authors (`T2510616`)
- **Dr. Md. Khalilur Rahman** — Thesis Supervisor & Professor, Department of Computer Science & Engineering, BRAC University

To cite this repository in academic work, refer to [`CITATION.cff`](CITATION.cff).
