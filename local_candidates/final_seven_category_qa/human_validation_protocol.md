# BanglaBBQ — Independent Human Validation Protocol

## 1. Protocol Scope & Objectives
This document establishes the official independent human validation protocol for the **BanglaBBQ (Bangla Bias Benchmark for Question-Answering)** benchmark across all seven modernized categories:
- Physical Appearance
- Social Status
- Health Status
- Regional Affiliation
- Ethnicity
- Occupational Background
- Marital Status

The objective is to establish gold-standard human verification across linguistic naturalness, cultural ecological validity, unambiguous semantic entailment, counterfactual symmetry, and empirical source credibility before any candidate dataset is promoted to canonical production.

---

## 2. Annotator Cohort Requirements & Qualifications
To ensure cultural competence and statistical independence, human evaluation must be conducted by qualified native Bengali speakers meeting the following criteria:
1. **Linguistic Competence**: Native Bengali speakers born and educated in Bangladesh, possessing fluent bilingual proficiency in English and Standard Colloquial Bengali (*Cholitobhasha*).
2. **Demographic & Regional Diversity**:
   - Equal gender balance across the annotator pool.
   - Broad regional representation, specifically including native speakers from historically stereotyped districts (Noakhali, Barisal, Sylhet, Chittagong, Rangpur/North Bengal).
   - Inclusion of ethnic minority representatives (Chakma, Marma, or Garo) for the Ethnicity category.
3. **Academic Background**: Advanced undergraduate or graduate degrees in Linguistics, Bengali Literature, NLP/Computer Science, Anthropology, or Sociology.
4. **Conflict of Interest**: Annotators must be independent third parties who were not involved in the original automated scenario generation or heuristic repair workflows.

---

## 3. Core Evaluation Dimensions & Scoring Rubrics

### Dimension 1: Bengali Linguistic Fluency & Naturalness
- **Question**: Does the Bengali text read like authentic, natural Bengali written by a native speaker, or does it sound like an unnatural translation / synthetic template?
- **Scale (1–5 Likert)**:
  - **1 (Unacceptable)**: Severe grammatical errors, broken inflectional morphology, or machine-translation gibberish.
  - **2 (Poor)**: Unnatural syntax, synthetic placeholder names (e.g., "শিক্ষার্থী ক"), awkward clitics (e.g., "ব্যক্তি-এর"), or heavy English calques.
  - **3 (Acceptable)**: Grammatically correct but visibly stiff or bureaucratic; unlikely to be spoken or written organically.
  - **4 (Good)**: Natural Bengali phrasing with minor stylistic stiffness in technical vocabulary.
  - **5 (Excellent)**: Completely natural, idiomatic Bangladeshi phrasing indistinguishable from native human authoring.

### Dimension 2: Stereotype Relevance & Cultural Ecological Validity
- **Question**: Does the scenario reflect a genuine, culturally recognizable social bias or discriminatory mechanism within Bangladeshi society?
- **Scale (Binary + Qualitative)**:
  - **Valid (1)**: The biased presupposition represents a documented, recognizable prejudice in Bangladesh (e.g., negative bias against sweepers, regional bias regarding financial shrewdness, marital stigma against widows).
  - **Invalid (0)**: The stereotype is an artificial Western artifact, an unfounded internet trope, or a satirical parody (e.g., Noakhali passport memes presented as sociological discrimination).

### Dimension 3: Unambiguous Semantic Entailment
- **Question**: Is the gold answer strictly entailed by the context and question logic alone?
- **Requirements**:
  - **Disambiguated Contexts**: The text MUST provide explicit, unambiguous evidence pointing to exactly one entity. If an annotator can reasonably argue that the other entity or 'Unknown' is defensible, the example FAILS.
  - **Ambiguous Contexts**: The text MUST contain zero information revealing the target attribute or outcome. 'অনির্ধারিত / Unknown' MUST be the only logically correct response. Any accidental leakage FAILS.

### Dimension 4: Counterfactual Symmetry & Semantic Invariance
- **Question**: Between counterfactual pairs (Orientation 'a' vs 'b'), are the two versions perfectly symmetric except for the demographic interchange?
- **Requirements**:
  - No confounding lexical variations introduced between target and comparison conditions.
  - Introduction order, sentence length, and grammatical complexity must be identical across counterfactual pairs.

### Dimension 5: Empirical Source Credibility
- **Question**: Does the cited source document substantiate the existence of the specific social prejudice tested in the scenario?
- **Tiers**:
  - **Tier 1 (Direct Empirical)**: Peer-reviewed journal article, government census, UN/ILO/WHO report, or formal sociological fieldwork documenting discrimination.
  - **Tier 2 (Investigative Journalism)**: Established national broadsheet investigative report (e.g., *Prothom Alo*, *The Daily Star*) documenting verified cases.
  - **Tier 3 (Confounded / General Context)**: Source provides general demographic data but does not prove discrimination, or conflates occupation with ethnicity/caste.
  - **Tier 4 (Unacceptable / Flawed)**: Satirical articles, entertainment blogs, social media memes, or unverified opinion essays.

---

## 4. Annotation Procedure & Blinding Protocol
1. **Blinded Presentation**:
   - Annotators are presented with context, question, and answer choices in randomized order without visibility into `question_polarity`, `context_condition`, `counterfactual_orientation`, or `label`.
2. **Batching Structure**:
   - Each annotator evaluates complete themes (all 3 scenario variations) to assess coverage consistency.
   - Redundant triple-annotation: Each item is independently rated by at least three annotators.
3. **Audit Question Injections**:
   - 5% synthetic "gold sanity check" questions with obvious factual errors or clear entailment traps are randomly inserted to monitor annotator attentiveness. Annotators failing >10% of sanity checks are disqualified.

---

## 5. Inter-Annotator Agreement (IAA) & Adjudication Rules
1. **Agreement Metrics**:
   - **Categorical Decisions (Entailment, Stereotype Validity)**: Fleiss' Kappa (κ) or Krippendorff's Alpha (α) with nominal metric. Target threshold: **κ >= 0.75**.
   - **Ordinal Ratings (Fluency Likert)**: Krippendorff's Alpha (α) with ordinal metric. Target threshold: **α >= 0.70**.
2. **Disagreement Adjudication**:
   - When 2 out of 3 annotators agree, a senior linguistics arbitrator reviews the rationale.
   - When all 3 annotators disagree (1 vs 1 vs 1), the item is flagged as **BLOCKED** and scheduled for scenario redesign.
3. **Automatic Disqualification Threshold**:
   - Any scenario where >=2 annotators rate Linguistic Naturalness <= 2 or Entailment = False is disqualified from the production benchmark.

---

## 6. Official Status Disclaimer
> [!IMPORTANT]
> **Status Disclosure**: This document defines the protocol and operational specification for independent human validation. As of this candidate repair package, **formal human annotation under this protocol has NOT yet been completed**. In accordance with scientific integrity guidelines, no dataset or category in this repository may be labeled `PUBLICATION READY` until this protocol is executed with independent human annotators and certified IAA reports are published.
