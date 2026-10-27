# BanglaBBQ — Mental Health Coverage Restoration Plan

## 1. Executive Summary & Historical Context
In the original benchmark developed by the senior research team (`Dataset_ BanglaBBQ_Old/Mental Health/`), **Mental Health** existed as an explicit evaluation axis containing 100 entries (`Mental_health_status_Bengali_100entries.jsonl` and `Mental_health_status_Eng.jsonl`). These probed stigma regarding conditions such as generalized anxiety, depression, and psychological distress.

During the modernization phase (which expanded categories to 1,440 records each with 10 themes, 3 scenario variations, and complete 6-way permutations), the newly generated category was named **Health Status** (`BanglaBBQ_HealthStatus`). However, the 10 selected themes in Health Status focused almost exclusively on somatic, physical, or infectious conditions:
- Q01: Tuberculosis (টিবি)
- Q02: Hepatitis B (হেপাটাইটিস বি)
- Q03: Leprosy (কুষ্ঠরোগ)
- Q04: HIV/AIDS (এইচআইভি/এইডস)
- Q05: Burn Scars (পোড়া দাগ)
- Q06: Thalassemia (থ্যালাসেমিয়া)
- Q07: COVID-19 history
- Q08: Chronic Kidney Disease / Dialysis
- Q09: Stroke / Hemiplegia
- Q10: Polio / Physical disability

Consequently, **psychiatric and mental health stigmas were entirely displaced from the modernized benchmark**, leaving a severe blind spot in evaluating LLM bias in the Bangladeshi sociocultural context.

---

## 2. Sociocultural Necessity in Bangladesh
Mental illness in Bangladesh carries extreme social stigma that fundamentally differs from physical health prejudice:
1. **Derogatory Psychiatric Labeling ("পাগল" / "মস্তিষ্কবিকৃত")**: People experiencing clinical psychiatric disorders are frequently stereotyped as violent, unpredictable, or morally deficient.
2. **Arranged Marriage Disqualification (বিয়ে ভাঙা)**: A history of counseling or antidepressant therapy is widely hidden in matrimonial matchmaking due to severe marital disqualification.
3. **Workplace Exclusion & Incompetence Assumptions**: Employees seeking psychiatric leave are often branded as permanently incapable of professional responsibility.
4. **Supernatural & Moral Attribution**: Mental health episodes are sometimes misattributed to weakness of faith, possession, or family curses, exacerbating discrimination.

---

## 3. Structural Architectural Options

### Option A: Internal Re-partition of Existing Health Status (Not Recommended)
- **Mechanism**: Replace 3–4 somatic themes (e.g., COVID-19 history, Burn Scars) with mental health themes inside `BanglaBBQ_HealthStatus`.
- **Drawbacks**: 
  - Destroys existing 1,440-record somatic baseline comparability.
  - Dilutes both somatic disease stigma and mental health stigma into an inconsistent hybrid.
  - Overwrites peer-reviewed historical datasets.

### Option B: Dedicated Modernized Category — `BanglaBBQ_MentalHealth` (Recommended)
- **Mechanism**: Implement a standalone 8th modernized category containing 1,440 bilingual records (1,440 EN, 1,440 BN).
- **Structure**:
  - 10 distinct psychiatric themes (Q01–Q10).
  - 3 scenario variations per theme (30 unique contexts).
  - 48 records per variation (complete 6-way answer permutations across 2 counterfactual orientations and 2 question polarities).
  - Positional introduction balance built in from day one (180 First / 180 Second across negative and non-negative disambiguated contexts).
- **Advantages**:
  - Preserves 100% of the somatic Health Status benchmark intact.
  - Honors the seniors' original research scope while scaling it to the modern 1,440-row rigors.
  - Allows targeted clinical review by Bangladeshi mental health professionals.

---

## 4. Proposed 10 Mental Health Themes (DSM-5 & NIMH Bangladesh Aligned)

| Theme ID | Clinical Focus | Bengali Term | Stigmatized Dimension / Scenario Context | Empirical Literature Reference |
|---|---|---|---|---|
| **Q01** | Major Depressive Disorder | বিষণ্ণতা | Workplace incompetence; stereotyped as "lazy" or "unmotivated" during team appraisals. | National Institute of Mental Health (NIMH) Bangladesh Survey (2019) |
| **Q02** | Generalized Anxiety Disorder | অতিরিক্ত উদ্বেগজনিত ব্যাধি | Inability to lead or make crisis decisions in professional management. | Hossain et al., *Lancet Psychiatry* (2020) |
| **Q03** | Bipolar Disorder | বাইপোলার ডিসঅর্ডার | Emotional instability, unfitness for parenting or family stewardship. | Islam et al., *Asian J. Psychiatr.* (2021) |
| **Q04** | Schizophrenia | সিজোফ্রেনিয়া | Stereotyped as inherently dangerous or unpredictable in neighborhood tenancy. | ICDDR,B Mental Health Stigma Report (2022) |
| **Q05** | Obsessive-Compulsive Disorder | শুচিবায়ু / ওসিডি | Social ostracization, mocked as eccentric or ritualistic in communal events. | Bangladesh Association of Psychiatrists (BAP) (2021) |
| **Q06** | Post-Traumatic Stress Disorder | ট্রমা-পরবর্তী মানসিক চাপ (পিটিএসডি) | Perceived as emotionally damaged or volatile following climate/industrial disasters. | WHO Bangladesh Mental Health Atlas |
| **Q07** | Psychotherapy & Counseling Seeking | কাউন্সেলিং বা সাইকিয়াট্রিস্ট দেখানো | Matrimonial rejection; viewed as "damaged" or having a hidden moral flaw. | Kabir et al., *BMC Public Health* (2023) |
| **Q08** | Postpartum Depression | প্রসবোত্তর বিষণ্ণতা (পিপিডি) | Accused of maternal failure, lack of maternal affection, or family ingratitude. | Gausia et al., *BJOG* (2009) |
| **Q09** | Substance Addiction Recovery | মাদকাসক্তি পুনর্বাসন | Incurable moral corruption; denied financial loans or business partnerships. | Department of Narcotics Control (DNC) / NIMH (2020) |
| **Q10** | Panic Disorder | প্যানিক ডিজঅর্ডার | Stereotyped as physically weak or unreliable under routine corporate stress. | Hasan et al., *BMJ Open* (2021) |

---

## 5. Scientific Guardrails & Confounder Prevention
To avoid replicating the methodological flaws identified in somatic Health Status:
1. **No Medical Precautions as Stigma**: Scenarios must never present legitimate medical/safety contraindications (e.g., driving heavy machinery while heavily sedated) as social bias. Scenarios must test irrational social, professional, and personal prejudice.
2. **Bilingual Semantic Equivalence**: Diagnostic terms must use accepted Bengali clinical terms (e.g., 'বিষণ্ণতা' rather than literal transliterations) with natural colloquial register.
3. **No Synthetic Placeholders**: Must use authentic Bangladeshi names rather than synthetic labels ('ব্যক্তি ক / খ').
4. **Strict Positional Orthogonality**: Exactly 5 V1, 5 V2, and 5 V3 variations reversed across Q01–Q10 to guarantee 180/180 introduction-order balance in both English and Bengali.

---

## 6. Implementation Protocol
- **Step 1**: Formulate formal scenario templates with clinical psychologist/psychiatrist consultation (NIMH/BSMMU).
- **Step 2**: Generate candidate JSONL files using deterministic permutation generator (`generate_permutations_6way()`).
- **Step 3**: Execute full structural validation (15-field schema, sequential EIDs 0–1439, 180/180 balance).
- **Step 4**: Blinded human annotation audit (Phase 5 protocol) before promotion to production.
