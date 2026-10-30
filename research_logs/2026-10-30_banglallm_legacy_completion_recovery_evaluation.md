# Research Log: BanglaLLM Prompt Compatibility Recovery Evaluation (Legacy Completion Mode)

**Date**: 2026-10-30  
**Researcher / Agent**: Hasin Ishrak / Antigravity Agent  
**Category**: Experimental Prompt Compatibility Diagnosis & Bias Evaluation  
**Milestone Scope**: Full 61,312-query evaluation of `BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct` using historical plain completion prompting (`legacy_completion_v2`) with the certified Alicia Parrish et al. (2022) BBQ scoring engine on NVIDIA L40S GPU  
**Status**: EXPERIMENTAL VERIFICATION COMPLETE / SEPARATE FROM CANONICAL 8-MODEL SUITE  

---

## 1. Executive Summary & Diagnostic Motivation

In the canonical eight-model benchmark evaluation (`certified_benchmark_report_banglallm_qwen_3b.json`), `BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct` collapsed to **0.00% Bengali accuracy** and produced **36,170 unparseable outputs** (58.99% overall, >98% in Bengali).

This investigation tested the **prompting format incompatibility hypothesis**: that the community fine-tune `BanglaLLM` was trained strictly as a text completion model rather than complying with the ChatML `<|im_start|>` chat template inherited from its base model (`Qwen/Qwen2.5-3B-Instruct`).

### Key Findings
1. **Bengali Performance Fully Recovered**: Under plain completion prompting, BanglaLLM achieved **80.77% English accuracy** and **59.13% Bengali accuracy**, almost exactly replicating the original baseline (80.79% ENG / 59.15% BEN, a variance of only 0.02%).
2. **Zero Parsing Failures**: Unparseable outputs dropped from **36,170 down to exactly 0 (0.00%)** across all 61,312 queries.
3. **Hypothesis Confirmed**: The 0.00% collapse in the canonical benchmark was entirely an artifact of prompt-template mismatch, not a total loss of Bengali language comprehension.
4. **Research Integrity Separation**: Because the seven other models were evaluated using their native instruction chat templates, this completion-mode run is classified as an **experimental diagnostic evaluation** (`experimental_benchmark_report_banglallm_qwen_3b_legacy_completion_v2.{json,csv}`) and kept separate from the certified canonical master benchmark table.

---

## 2. Comparative Analysis: Three BanglaLLM Evaluations

| Metric | 1. Original Baseline (Legacy Run, 2026-10-29) | 2. Canonical Benchmark (Chat Template, 2026-10-30) | 3. Recovery Evaluation (Legacy Completion, 2026-10-30) |
| :--- | :--- | :--- | :--- |
| **Prompt Format** | Plain completion (`Context... Answer:`) | Native ChatML (`<|im_start|>user...`) | Plain completion (`Context... Answer:`) |
| **Scoring Engine** | Legacy `compute_metrics()` (flawed fallthrough) | Parrish et al. (2022) BBQ engine | Parrish et al. (2022) BBQ engine |
| **Total Queries** | 61,312 | 61,312 | 61,312 |
| **ENG Overall Acc** | 80.79% | 48.04% | **80.77%** |
| **BEN Overall Acc** | 59.15% | 0.00% | **59.13%** |
| **Accuracy Gap** | -21.64% | -48.04% | **-21.64%** |
| **ENG Ambig Acc** | 67.80% | 19.53% | **67.77%** |
| **BEN Ambig Acc** | 43.72% | 0.00% | **43.70%** |
| **ENG Disambig Acc**| 93.78% | 76.55% | **93.77%** |
| **BEN Disambig Acc**| 74.58% | 0.00% | **74.56%** |
| **ENG Amb Bias ($s_{\text{amb}}$)** | +0.2189 (flawed engine) | +0.0863 | **+0.0911** |
| **BEN Amb Bias ($s_{\text{amb}}$)** | +0.2203 (flawed engine) | +0.0000 | **-0.0035** |
| **Bias Delta ($s_{\text{amb}}$)** | +0.0014 (flawed engine) | -0.0863 | **-0.0946** |
| **ENG Dis Bias ($s_{\text{dis}}$)** | N/A (not implemented) | 0.0000 | **+0.0039** |
| **BEN Dis Bias ($s_{\text{dis}}$)** | N/A (not implemented) | 0.0000 | **-0.0093** |
| **Unparseable Count**| 0 | 36,170 (58.99%) | **0 (0.00%)** |
| **Wall-Clock Time** | 485s | 515.8s | **415.34s (6.92 min)** |
| **GPU Cost (USD)** | ~$0.24 | $0.2579 | **$0.2077 (~$0.21)** |

---

## 3. Category-by-Category Results (Legacy Completion Mode)

```
========================================================================================================================
         BANGLALLM EXPERIMENTAL RECOVERY EVALUATION REPORT (LEGACY COMPLETION V2): 61,312 QUERIES
========================================================================================================================
Category                         | Queries | ENG Acc | BEN Acc | ENG s_amb | BEN s_amb | Delta Bias | Unparseable
------------------------------------------------------------------------------------------------------------------------
BanglaBBQ_Age                    |   5,840 |  74.21% |  50.45% |   +0.1623 |   +0.0774 |    -0.0849 |           0
BanglaBBQ_EducationalBackground  |   5,760 |  72.81% |  56.53% |   +0.1382 |   +0.0014 |    -0.1368 |           0
BanglaBBQ_Ethnicity              |   2,880 |  89.93% |  74.65% |   +0.0764 |   +0.0042 |    -0.0722 |           0
BanglaBBQ_Gender                 |   9,392 |  85.14% |  59.88% |   +0.0254 |   +0.0064 |    -0.0190 |           0
BanglaBBQ_HealthStatus           |   5,760 |  59.69% |  49.93% |   +0.1604 |   -0.2243 |    -0.3847 |           0
BanglaBBQ_MaritalStatus          |   5,760 |  74.20% |  61.08% |   +0.0174 |   -0.0382 |    -0.0556 |           0
BanglaBBQ_OccupationalBackground |   5,760 |  95.24% |  65.21% |   +0.0028 |   -0.0042 |    -0.0070 |           0
BanglaBBQ_PhysicalAppearance     |   2,880 |  65.69% |  48.68% |   +0.3819 |   +0.1167 |    -0.2652 |           0
BanglaBBQ_Politics               |   5,760 |  86.32% |  53.51% |   +0.1306 |   +0.0986 |    -0.0320 |           0
BanglaBBQ_Regional               |   2,880 |  99.24% |  85.14% |   +0.0000 |   -0.0111 |    -0.0111 |           0
BanglaBBQ_Religion               |   5,760 |  95.90% |  62.57% |   +0.0104 |   -0.0111 |    -0.0215 |           0
BanglaBBQ_SocialStatus           |   2,880 |  68.19% |  55.21% |   +0.1486 |   -0.0069 |    -0.1555 |           0
------------------------------------------------------------------------------------------------------------------------
WEIGHTED GRAND TOTAL             |  61,312 |  80.77% |  59.13% |   +0.0911 |   -0.0035 |    -0.0946 |           0
========================================================================================================================
```

---

## 4. Deep Scientific Implications for the BanglaBBQ Paper

### 1. Fine-Tuning Fragility vs Prompt Invariance
The base model (`Qwen/Qwen2.5-3B-Instruct`) achieves 80.68% ENG / 51.38% BEN under its canonical chat template with 0 unparseable outputs. When BanglaLLM was trained on top of Qwen 2.5 3B with conversational Bengali instruction pairs, the fine-tuning process altered the conditioning expectations:
- In completion mode, BanglaLLM outperforms base Qwen 3B in Bengali accuracy (**59.13% vs 51.38%**, a +7.75% improvement) and ambiguous epistemic accuracy (**43.70% vs 18.26%**, a +25.44% improvement).
- In standard ChatML chat mode, BanglaLLM completely breaks down (0.00% accuracy, 58.99% unparseable).
- This provides a crucial methodological finding for the benchmark paper: **Community-released language-specific LLM fine-tunes often break standard API chat wrappers, necessitating both chat-template and completion-mode evaluation audits to distinguish prompt fragility from semantic incompetence.**

### 2. Disambiguated vs Ambiguous Bias Dynamics
- **Disambiguated Contexts**: BanglaLLM demonstrates high fidelity to facts across both languages (93.77% ENG / 74.56% BEN disambiguated accuracy) with near-zero disambiguated bias ($s_{\text{dis}} = +0.0039$ ENG, $-0.0093$ BEN).
- **Ambiguous Contexts**: BanglaLLM maintains a moderate English bias ($s_{\text{amb}} = +0.0911$) but effectively neutralizes ambiguous bias in Bengali ($s_{\text{amb}} = -0.0035$), resulting in a negative global delta ($-0.0946$). However, this is partially mediated by lower ambiguous accuracy in Bengali (43.70% vs 67.77% in English), where the model defaults to specific non-stereotypical options or 'তথ্য অপর্যাপ্ত' inconsistently across categories.

---

## 5. Artifact Verification & Deliverables

- **Experimental Report JSON**: `metadata/eval_results/experimental_benchmark_report_banglallm_qwen_3b_legacy_completion_v2.json`
- **Experimental Report CSV**: `metadata/eval_results/experimental_benchmark_report_banglallm_qwen_3b_legacy_completion_v2.csv`
- **Durable Modal Volume Predictions**: Committed under `banglabbq-eval-volume:predictions/banglallm_qwen_3b_legacy_completion_v2/` (24 chunk JSONL files).
- **Execution Script**: `scripts/modal_eval_banglallm_legacy_completion_l40s.py`
