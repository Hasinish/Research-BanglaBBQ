# purpose.md — Official BanglaBBQ Research Mission

## The One-Line Mission
Repair, improve, validate, and expand the existing bilingual BanglaBBQ benchmark dataset originally created by our seniors' BRAC University thesis group, producing an academically rigorous, culturally authentic, and mathematically balanced foundation for LLM bias evaluation and subsequent SafeLLM mitigation research.

---

## 1. Why BanglaBBQ Exists

Large Language Models (LLMs) deployed across global contexts exhibit pervasive social, cultural, and political biases. However, the overwhelming majority of existing bias benchmarks (e.g., BBQ, CrowS-Pairs, StereoSet) reflect Western, English-centric social dynamics. 

In Bangladesh, socio-cultural biases differ substantially in origin, expression, and demographic nuance — spanning district-level prejudices, religious minority vulnerabilities, partisan political polarization, generational stigmas, educational hierarchy, and physical appearance colorism.

### Foundational Baseline: The Seniors' Thesis (T2510616)
In June 2025, a 5-member BRAC University undergraduate thesis research group completed thesis **T2510616**:
*“A Bilingual Study of Socio-Cultural Bias in Large Language Models through BanglaBBQ and a Post Processing Mitigation Pipeline”*  
**Authors**: Taeeba Tasnia, Ashika Habib Khan, Sumit Anthony Gomes, Tahseen Tanha, and Provat Saha  
**Supervisors**: Dr. Muhammad Iqbal Hossain, Tawhid Anwar, and Sifat Tanvir  
**Artifacts**: Thesis Book (`T2510616.pdf`), IEEE Conference Draft (`T2510616_IEEE_Paper.pdf`), and legacy dataset dumps (`Dataset_ BanglaBBQ_Old/`).

The seniors established the initial conceptual framework of BanglaBBQ across 9 bias categories and drafted the initial SafeLLM post-processing mitigation pipeline. Their groundbreaking effort is our **historical foundation**.

---

## 2. Why the Existing Dataset Needs Urgent Improvement

While the seniors pioneered the benchmark, deep forensic audits of `Dataset_ BanglaBBQ_Old/` revealed critical structural, semantic, and methodological defects that prevent direct academic publication or reliable scientific evaluation:

1. **Truncation & Incomplete Coverage**:
   - `Age`: Legacy Bengali dataset only translated 799 entries (Rows 0–798) out of the full 2,920 PakBBQ template rows.
   - `Regional Affiliation`: Contains only 51 entries — statistically underpowered for reliable LLM bias quantification.
   - `Marital Status` & `Mental Health`: Each limited to 100 entries with minimal scenario diversity.
2. **Structural & Formatting Corruptions**:
   - Syntax errors in combined legacy files (`banbbq_ben_combined.jsonl` has 101 broken JSON lines; `Banglabbq/banglabbq_ben_combined.jsonl` has 29 broken JSON lines).
   - `Physical Appearance`: Discrepancy between English (1,106 entries) and Bengali (1,123 entries) with mismatched identifiers.
3. **Gold Label & Ambiguity Errors**:
   - Legacy Politics contained 40 disambiguated gold label errors where the ground-truth answer was contradicted by the context text.
   - Ambiguous contexts in some categories failed to consistently resolve to "Unknown / Cannot be determined".
4. **Answer Permutation Deficits**:
   - Legacy subsets lacked balanced 6-way answer position permutations ($3! = 6$), inducing severe position bias in LLM evaluations.
5. **Translation & Cultural Localization Flaws**:
   - Literal machine translation artifacts (e.g., "জুমারটি" for boomer, English digits in Bengali text like "58 বছর বয়সী-এর", and unnatural phrasing).
   - Direct imports from PakBBQ containing Pakistani cultural references (Imtiaz supermarket, InDrive, Karachi, Lahore) without Bangladeshi localization.
6. **Lack of Verifiable Source Citations**:
   - Multiple themes lacked documented journalistic, legal, or human rights citations grounding the scenarios in real Bangladeshi societal facts.

---

## 3. Methodological References: BBQ and PakBBQ

We adopt the proven scientific frameworks of two prominent benchmarks, applying their rigorous invariants to Bangladesh:

### BBQ (Bias Benchmark for Question Answering — Parrish et al., ACL Findings 2022)
- **Context Conditions**: Balanced pairs of **Ambiguous** (insufficient information, requiring target answer "Cannot be determined / Unknown / অজানা") and **Disambiguated** (sufficient context explicitly identifying the correct entity).
- **Question Polarities**: Balanced pairs of **Negative** (probing negative stereotypes or harmful actions) and **Non-negative** (probing positive or neutral actions).
- **Counterfactual Symmetry**: Pairwise entity comparisons where demographic attributes are inverted to prove bias without confounding context.
- **Answer Balancing**: Full $3! = 6$ permutations per condition ensuring target demographic entities appear equally in `ans0`, `ans1`, and `ans2`.

### PakBBQ (Pakistan-Adapted BBQ — Hashmat et al., EMNLP 2025 / arXiv:2508.10186)
- **Regional Adaptation Methodology**: Framework for adapting Western BBQ templates into South Asian socio-cultural realities.
- **Combinatorial Generation**: Systematic expansion templates combining demographic groups, settings, and question formulations.
- **Bilingual Translation Standards**: Guidelines for preserving pragmatic meaning and syntactic parity between English and native languages.

> **Critical Distinction**: BBQ and PakBBQ serve as **methodological templates**, **NOT** direct sources of valid Bangladeshi scenarios. Every scenario in BanglaBBQ must be grounded in verified Bangladeshi reality and backed by authoritative sources.

---

## 4. The Nine BanglaBBQ Bias Categories

The improved benchmark covers nine socio-cultural bias dimensions critical to Bangladesh:

| # | Bias Category | Focus in Bangladeshi Context |
| :- | :--- | :--- |
| 1 | **Age** | Workplace competence vs. ageism, technology adoption, physical frailty, generational respect vs. dismissiveness. |
| 2 | **Politics** | Partisan polarization (Awami League, BNP, Jamaat, student activists, interim governance), press freedom, administrative neutrality. |
| 3 | **Religion** | Communal harmony, discrimination against minority groups (Hindus, Buddhists, Christians, Ahmadiyya, Dalit Hindus), festival security. |
| 4 | **Gender Identity** | Traditional domestic roles, professional competence, leadership bias, harassment, socio-economic autonomy. |
| 5 | **Physical Appearance** | Skin complexion ("shyamla" vs. fair skin colorism), body shaming, height discrimination, marital arrangement bias. |
| 6 | **Regional Affiliation** | District stereotyping (Noakhali, Barisal, Chittagong, Sylhet, Old Dhaka, North Bengal), linguistic accents, cultural perceptions. |
| 7 | **Educational Background** | Public universities vs. Private universities vs. National University hierarchy, English-medium vs. Bangla-medium vs. Madrasah. |
| 8 | **Marital Status** | Social stigma against unmarried adults, divorced women, widows, and second marriages. |
| 9 | **Mental Health** | Stigma surrounding therapy, depression, psychiatric medication, clinical consultations vs. perceived weakness. |

---

## 5. English–Bengali Bilingual Objective

BanglaBBQ is strictly a **parallel bilingual benchmark**:
- **Bilingual Structural Parity**: Every English record has an exact 1-to-1 parallel Bengali record sharing identical `example_id`, `question_index`, condition, polarity, and categorical metadata.
- **Authentic Bengali Phrasing**: Translations must reflect natural Bangladeshi colloquial and formal usage, avoiding machine-translation stiffness, incorrect grammatical inflections (e.g., inappropriate case markers like `-এর`), or transliterated loan words.
- **Entity Parity**: Demographic entity labels in `ans0`, `ans1`, and `ans2` must align semantically with `answer_info` definitions in both languages.

---

## 6. Roles of Tools: Working Spreadsheet vs. Versioned GitHub

- **Master Google Spreadsheet**: The primary active working canvas. All dataset repairs, manual reviews, category expansions, and collaborative verifications occur here first.
- **GitHub Repository**: The permanent version-controlled archive. Holds frozen legacy baselines, validated JSONL exports, reproducible test scripts, CI workflows, and authoritative project documentation.
- **Rule of Synchronization**: Changes verified in Google Sheets are exported to GitHub JSONL files via automated scripts with complete invariant checking.

---

## 7. Dataset Quality & Invariant Requirements

Every improved category must satisfy ten strict invariants before being declared complete:
1. **Balanced Record Counts**: Exactly 48 records per theme (2 counterfactual orientations $\times$ 2 context conditions $\times$ 2 question polarities $\times$ 6 answer permutations).
2. **Sequential IDs**: Clean, contiguous zero-indexed numbering (`0` to $N-1$) across `example_id` and `id`.
3. **Canonical 4-Row Block Sequence**: Deterministic ordering (`ambig+neg`, `disambig+neg`, `ambig+nonneg`, `disambig+nonneg`).
4. **Uniform Label Distribution**: Exactly $33.3\%$ distribution across labels `0`, `1`, and `2` ($N/3$ each).
5. **Ambiguous Context Grounding**: All ambiguous QA pairs must resolve strictly to Unknown (`Cannot be determined` / `অজানা`).
6. **Disambiguated Context Grounding**: Disambiguated QA pairs must be logically provable from context without world-knowledge leaps.
7. **Zero Unintended Duplicates**: Complete absence of duplicate $(context, question)$ pairs within any condition.
8. **100% Bilingual Parity**: Identical metadata, conditions, polarities, and label indices across English and Bengali.
9. **Verifiable Sources**: Documented journalistic, legal, or academic URLs for every theme.
10. **Preservation of Baseline**: Legacy files in `Dataset_ BanglaBBQ_Old/` must remain untouched.

---

## 8. Academic Publication & Downstream SafeLLM Roadmap

### Primary Goal: Benchmark Publication
Our immediate and highest-priority objective is publishing the finalized BanglaBBQ benchmark at a top-tier computational linguistics or AI conference (e.g., ACL, EMNLP, EACL, or South Asian NLP workshops):
- Author comprehensive dataset documentation,Datasheet for Datasets, and ethical considerations.
- Run baseline zero-shot evaluations across modern open and proprietary LLMs (e.g., LLaMA-3.1-8B, LLaMA-3.3-70B, LLaMA-4-Scout, Gemini 2.0 Flash, Claude 3.5 Sonnet, DeepSeek-V3).
- Measure Ambiguous Bias Score ($s_{\text{ambig}}$), Disambiguated Accuracy ($acc_{\text{disambig}}$), and Unknown Rate across both languages.

### Downstream Goal: SafeLLM Mitigation Pipeline
Once the benchmark dataset is perfected and validated, we will evaluate the seniors' proposed **SafeLLM** 3-stage inference-time post-processing mitigation pipeline:
1. **Stage 1 (Sensitivity Layer)**: Disambiguation Injection and Chain-of-Thought prompting to alert the model to potential bias traps.
2. **Stage 2 (Bias Evaluator)**: Automated sample-level scoring and flag detection.
3. **Stage 3 (Counterfactual Grounding)**: Identity-sensitive attribute swapping to enforce invariant predictions across demographic groups.

Research must address known limitations from the thesis (e.g., Stage 1 degradation on smaller $<60\text{B}$ parameter models and Stage 3 overcorrection on disambiguated contexts).
