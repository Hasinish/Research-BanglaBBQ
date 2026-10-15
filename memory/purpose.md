# purpose.md — The Bot Journey

## The One Line Version
Publish a high-impact research paper and release the curated BanglaBBQ benchmark dataset on socio-cultural bias evaluation and post-processing mitigation (SafeLLM) for Large Language Models in the Bangladeshi context.

## Mission & Platform Goals
- **Core Mission**: Revitalize and finalize the 5-member BRAC University undergraduate thesis (T2510616: *"A Bilingual Study of Socio-Cultural Bias in Large Language Models through BanglaBBQ and a Post Processing Mitigation Pipeline"*) across the finish line for conference/journal publication (e.g., IEEE, ACL, EMNLP, or South Asian NLP workshops).
- **Dataset Perfection & Publishing**: Consolidate, audit, and clean the 6,607-sample bilingual (Bengali + English) BanglaBBQ dataset across 9 bias categories (Age, Gender Identity, Physical Appearance, Religion, Regional Affiliation, Educational Background, Marital Status, Mental Health, Politics) and 4 template types (DT: Directly Translated, TM: Target Modified, NA: Newly Added, SR: Sample Removed).
- **Codebase & Pipeline Construction**: Build or reconstruct clean, robust, and reproducible scripts for:
  - Zero-shot LLM evaluation across target models (LLaMA-3.1-8B, LLaMA-3.3-70B, LLaMA-4-Scout-17B, Gemini 2.0 Flash-Lite).
  - Cyclic prompt permutation (ABC -> BCA -> CAB) and majority voting.
  - SafeLLM 3-stage inference-time post-processing mitigation pipeline:
    - Stage 1: Sensitivity Layer (Disambiguation Injection + Chain-of-Thought Prompting).
    - Stage 2: Bias Evaluator (Sample-level flagging using Bias Score, Accuracy, and Unknown Rate).
    - Stage 3: Counterfactual Grounding (Systematic demographic attribute swap and identity-sensitive overriding).
- **Tackle Key Methodological Limitations**:
  - Solve the Stage 1 scaling threshold issue (where <60B models degrade in accuracy and increase in bias).
  - Eliminate the severe Stage 3 overcorrection problem using adaptive confidence thresholds.
  - Bridge the cross-lingual performance and identity sensitivity gap between English and Bengali.
- **Paper Writing & Submission**: Polish the 8-page IEEE conference draft, upgrade figures/tables, tighten mathematical formalism, and ensure publication readiness.
