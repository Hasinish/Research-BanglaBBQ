# Research Log: 2026-10-29 — Full 4,000-Sample Evaluation of Gemma 2 9B on NVIDIA L40S

## 1. Overview & Setup
- **Model**: `google/gemma-2-9b-it` (Google DeepMind)
- **Framework**: `vLLM` 0.6.x with PagedAttention (`bfloat16`, 90% GPU memory allocation)
- **Hardware**: NVIDIA L40S GPU (48 GB GDDR6 ECC VRAM, 864 GB/s bandwidth) hosted on Modal AI
- **Dataset**: Stratified 4,000 queries (2,000 English + 2,000 Bengali paired scenarios) across all 12 categories in `Dataset_BanglaBBQ_New/`
- **Total Execution Latency**: **165.52 seconds (2 minutes, 45 seconds)** across all 4,000 prompts (~24.2 queries/sec).

---

## 2. Benchmark Results Table

| Category | ENG Acc | BEN Acc | ENG Bias | BEN Bias | Bias Delta (BEN - ENG) | ENG Ambig Acc | BEN Ambig Acc |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BanglaBBQ_HealthStatus** | 95.83% | 80.00% | +0.0833 | **+0.4000** | **+0.3167 🚨** | 91.67% | 60.00% |
| **BanglaBBQ_SocialStatus** | 83.33% | 75.00% | +0.3333 | **+0.5000** | **+0.1667 🚨** | 66.67% | 50.00% |
| **BanglaBBQ_PhysicalAppearance** | 84.17% | 75.83% | +0.3167 | **+0.4833** | **+0.1666 🚨** | 68.33% | 51.67% |
| **BanglaBBQ_Gender** | 92.14% | 79.29% | +0.0286 | +0.0214 | -0.0072 | 97.14% | 97.86% |
| **BanglaBBQ_Age** | 78.93% | 82.50% | +0.2857 | +0.1000 | -0.1857 | 71.43% | 90.00% |
| **BanglaBBQ_EducationalBackground** | 70.83% | 78.33% | +0.5833 | +0.4333 | -0.1500 | 41.67% | 56.67% |
| **BanglaBBQ_Ethnicity** | 91.67% | 97.50% | +0.1667 | +0.0500 | -0.1167 | 83.33% | 95.00% |
| **BanglaBBQ_OccupationalBackground** | 95.00% | 98.33% | +0.1000 | +0.0333 | -0.0667 | 90.00% | 96.67% |
| **BanglaBBQ_Religion** | 97.08% | 98.33% | +0.0583 | +0.0167 | -0.0416 | 94.17% | 96.67% |
| **BanglaBBQ_MaritalStatus** | 90.83% | 91.67% | +0.1667 | +0.1333 | -0.0334 | 83.33% | 86.67% |
| **BanglaBBQ_Politics** | 90.42% | 89.17% | +0.1917 | +0.1750 | -0.0167 | 80.83% | 82.50% |
| **BanglaBBQ_Regional** | 100.00% | 100.00% | +0.0000 | +0.0000 | +0.0000 | 100.00% | 100.00% |
| **OVERALL AVERAGE** | **89.19%** | **87.16%** | **+0.1929** | **+0.1955** | **+0.0027** | **80.73%** | **80.25%** |

---

## 3. Scientific Discoveries & Analysis

### A. Severe Cross-Lingual Safety Degradation in Somatic & Societal Bias
1. **Health Status (Delta: +0.3167)**:
   - In English, Gemma 2 exhibits high safety compliance (bias = +0.0833, ambiguous accuracy = 91.67%), properly choosing "Unknown / Cannot be determined".
   - In Bengali, ambiguous accuracy drops drastically to 60.00%, and the model picks the health-stigmatized group (e.g. leprosy, tuberculosis, mental health conditions) with a bias score of **+0.4000 (a 380% surge!)**.
2. **Social Status (Delta: +0.1667)**:
   - Ambiguous context accuracy collapses from 66.67% in English to 50.00% in Bengali.
   - Bengali bias score hits **+0.5000**, meaning when context is ambiguous, the model defaults to assigning negative attributes to slum dwellers and low-income demographics 50% of the time.
3. **Physical Appearance (Delta: +0.1666)**:
   - Bengali bias increases to **+0.4833** with ambiguous accuracy dropping to 51.67%. Colorism and appearance stereotyping become pronounced in native Bengali prompts.

### B. Language Comprehension vs. Guardrail Drift
- In categories like **Gender**, overall accuracy drops from **92.14% in English to 79.29% in Bengali** (a 12.85% drop), indicating substantial lexical and syntax comprehension degradation in Bengali, despite conservative bias scores.
- In categories like **Educational Background**, high baseline bias exists across both languages (+0.5833 ENG vs +0.4333 BEN), demonstrating deep model priors regarding academic pedigree and institutional hierarchy.

---

## 4. Next Experimental Steps
1. Execute the identical 4,000-sample benchmark on **`meta-llama/Llama-3.1-8B-Instruct`** on L40S to compare Google's Constitutional AI against Meta's RLHF guardrails.
2. Evaluate **`Qwen/Qwen2.5-14B-Instruct`** to test high-fluency multilingual architectures against low-resource alignment drift.

