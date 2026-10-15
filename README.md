# Research-BanglaBBQ

A bilingual (English–Bengali) socio-cultural and political bias evaluation benchmark for Large Language Models (LLMs), culturally adapted and mathematically grounded following the BBQ (Bias Benchmark for QA) framework.

---

## 📌 Project Overview

This repository hosts the research assets, dataset manifests, validation tooling, and production datasets for **BanglaBBQ**:
1. **Age Bias Benchmark (`Age`)**:
   - **2,920 records** per language (Directly Translated and Target Modified).
   - 100% mathematical invariant parity with BBQ / PakBBQ standards.
   - Natural, conversational Bengali phrasing resolving kinship disambiguation (Grandma -> নানি, Grandpa -> নানা, Grandparent -> দাদু, Grandchild -> নাতিটি).
2. **Political Bias Benchmark (`Politics`)**:
   - **20 source-backed themes** covering real-world institutional decisions and civil liberties documentation in Bangladesh (Human Rights Watch, Amnesty International, CPJ, UN Human Rights, Transparency International Bangladesh, Prothom Alo).
   - **960 records** each in English and Bengali (1,920 total records).
   - Full 6-way answer permutations ($3!$) across 2 counterfactual orientations.
   - Canonical 4-row block sequence throughout (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`).
   - Perfectly balanced labels (320 / 320 / 320), 0 label errors, 0 duplicate QA pairs.

---

## 📂 Repository Structure

```
├── BanglaBBQ_BEN_New/                # Verified Bengali production dataset exports
│   └── Age.jsonl                    # Full 2,920-record Age benchmark in conversational Bengali
├── Dataset_ BanglaBBQ_Old/           # Legacy thesis corpora & active domain working directories
│   ├── Politics/                    # Production Politics datasets & verified backups
│   │   ├── banglabbq_politics_english.jsonl   # Full 960-record English Politics benchmark
│   │   ├── banglabbq_politics_bengali.jsonl   # Full 960-record Bengali Politics benchmark
│   │   ├── backup_q1_q5_eng_240.json          # Untouched baseline backup of Q1-Q5
│   │   └── backup_q1_q5_ben_240.json
│   ├── Age/
│   ├── Educational background/
│   ├── Gender_identity/
│   ├── Marital Status/
│   ├── Mental Health/
│   ├── Physical_appearance/
│   ├── Regional/
│   └── Religion/
├── scripts/                         # 45+ automated research, migration, and live audit scripts
│   ├── README.md                    # Detailed documentation and categorisation of all scripts
│   ├── generate_all_politics_themes.py # Generator for Q6-Q20 source-backed themes
│   ├── apply_politics_20_themes.py     # Batch pusher and Google Sheets styler
│   ├── verify_politics_960_live.py     # 11-check live Google Sheets verification suite
│   ├── apply_exact_age_style_to_politics.py # Visual formatting replication
│   └── verify_exact_age_style.py
├── memory/                          # Workspace state, project purpose, and contextual indices
├── PakBBQ_Age_English.csv           # 2,920-record English Age source dataset
├── T2510616.pdf                     # BRAC University undergraduate thesis monograph
└── T2510616_IEEE_Paper.pdf          # 8-page IEEE conference paper draft
```

---

## ⚖️ Political Bias Benchmark: 20 Research Themes

| ID | Theme | Source Document | Records |
|:---|:---|:---|:---:|
| **Q1** | Police complaint registration | [HRW (2022)](https://www.hrw.org/news/2022/10/10/bangladesh-crackdown-political-opposition) | 48 |
| **Q2** | Business permit renewals | [HRW (2023)](https://www.hrw.org/world-report/2023/country-chapters/bangladesh) | 48 |
| **Q3** | Journalist press access | [CPJ (2024)](https://cpj.org/2024/01/bangladesh-election-crackdown-press-freedom/) | 48 |
| **Q4** | Public hospital admission | [Amnesty International (2023)](https://www.amnesty.org/en/latest/news/2023/08/bangladesh-unlawful-use-of-force-against-protesters-must-end-immediately/) | 48 |
| **Q5** | Bank loan approvals | [Transparency International Bangladesh (2023)](https://www.ti-bangladesh.org/en/articles/research/7211) | 48 |
| **Q6** | Political rally permission | [HRW (2023)](https://www.hrw.org/news/2023/08/02/bangladesh-excessive-force-against-political-protesters) | 48 |
| **Q7** | Unequal policing of demonstrations | [Amnesty International (2023)](https://www.amnesty.org/en/latest/news/2023/08/bangladesh-unlawful-use-of-force-against-protesters-must-end-immediately/) | 48 |
| **Q8** | Political travel checkpoints | [HRW (2023)](https://www.hrw.org/news/2023/11/01/bangladesh-violence-erupts-amid-demands-fair-election) | 48 |
| **Q9** | Election campaign obstruction | [HRW (2018)](https://www.hrw.org/news/2018/12/22/bangladesh-violent-campaign-targets-opposition) | 48 |
| **Q10** | Voter intimidation and access | [HRW (2019)](https://www.hrw.org/news/2019/01/02/bangladesh-election-abuses-need-independent-probe) | 48 |
| **Q11** | NGO registration restrictions | [HRW (2022)](https://www.hrw.org/news/2022/06/09/bangladesh-stop-punishing-human-rights-work) | 48 |
| **Q12** | Removal of critical online news articles | [HRW (2023)](https://www.hrw.org/news/2023/05/03/bangladesh-end-crackdown-against-journalists-and-critics) | 48 |
| **Q13** | Newspaper publication restrictions | [HRW (2023)](https://www.hrw.org/news/2023/05/03/bangladesh-end-crackdown-against-journalists-and-critics) | 48 |
| **Q14** | Politicized university dormitory allocation | [Prothom Alo (2023)](https://en.prothomalo.com/bangladesh/politics/chhatra-league-decides-who-stays-where-in-the-halls) | 48 |
| **Q15** | Forced student participation in political rallies | [Prothom Alo (2023)](https://en.prothomalo.com/bangladesh/hdr5whpl87) | 48 |
| **Q16** | Political favoritism in social welfare | [Sage Publications (2020)](https://journals.sagepub.com/doi/10.1177/0021909620970581) | 48 |
| **Q17** | Political influence over government procurement | [Transparency International Bangladesh (2023)](https://www.ti-bangladesh.org/en/articles/research/7211) | 48 |
| **Q18** | Obstructed medical care for protesters | [United Nations Human Rights (2024)](https://bangladesh.un.org/en/289108-bangladesh-un-report-finds-brutal-systematic-repression-protests-calls-justice-serious) | 48 |
| **Q19** | Harassment of relatives of expatriate dissidents | [HRW World Report (2023)](https://www.hrw.org/world-report/2023/country-chapters/bangladesh) | 48 |
| **Q20** | Politically motivated home raids | [HRW (2022)](https://www.hrw.org/news/2022/10/10/bangladesh-crackdown-political-opposition) | 48 |

---

## 🔬 Benchmark Verification & Invariant Audits

Run the live audit suites directly:
```bash
# Verify 20 Politics Themes on Google Sheets & JSONL (11 comprehensive mathematical checks)
python scripts/verify_politics_960_live.py

# Verify Visual Formatting & Text Wrapping Parity with Age
python scripts/verify_exact_age_style.py

# Verify Age Benchmark Parity & Invariance
python scripts/audit_live_p1_p2.py
```

---

## 👥 Authors & Acknowledgments

- **Hasin Ishrak** — Researcher & Lead Implementation (BRAC University)
- **Taeeba Tasnia**, **Ashika Habib Khan**, **Sumit Anthony Gomes**, **Tahseen Tanha**, **Provat Saha** — Original Thesis Authors (`T2510616`)
- Supervised under the Department of Computer Science & Engineering, **BRAC University, Dhaka, Bangladesh**.
