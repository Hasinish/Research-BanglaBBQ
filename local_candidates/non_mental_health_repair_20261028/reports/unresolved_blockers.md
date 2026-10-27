# BanglaBBQ Unresolved Blockers & Scientific Limitations Report

## 1. Overview
In rigorous benchmark engineering, identifying what **cannot** be safely repaired without external human review or additional empirical evidence is as critical as executing candidate fixes. This document details all open blockers, paywalled/inaccessible sources, cultural review requirements, and parallel development boundaries as of **October 28, 2026**.

---

## 2. Blocked Sources Requiring Academic Replacement
The following themes have been marked `BLOCKED_SOURCE` in `source_evidence_matrix.csv` and are prohibited from production deployment until rigorous academic citations are provided:

### A. Regional Affiliation
1. **Theme Q01 (Noakhali / Bogura): Schuman (1966)**
   - *Status*: `HISTORICAL_ONLY` / Paywall Limitation.
   - *Reason*: Schuman (1966) documented stereotypes in the pre-independence East Pakistan era. While historically foundational, it does not provide empirical evidence of contemporary (2020s) economic or workplace discrimination in Bangladesh. Furthermore, precise page-level quotations could not be independently verified without commercial database authentication.
   - *Action Required*: Identify contemporary sociological fieldwork or experimental audit studies on regional discrimination in Dhaka's labor market.

2. **Theme Q03 (Tangail / Barishal): Satirical Lifestyle Article**
   - *Status*: `UNSUPPORTED` for institutional discrimination.
   - *Reason*: The existing citation relies on a lighthearted, satirical lifestyle column discussing cultural tropes and sweetmeats. Satire does not establish an institutional exclusion mechanism.
   - *Action Required*: Propose a replacement scenario grounded in verified labor market or housing audit data.

3. **Theme Q10 (Old Dhaka / Modern Dhaka): Heritage Feature Article**
   - *Status*: `UNSUPPORTED`.
   - *Reason*: The cited source celebrates the culinary and architectural heritage of Old Dhaka (Dhakaiya culture). It contains zero empirical evidence demonstrating anti-Dhakaiya institutional prejudice in modern professional settings.
   - *Action Required*: Locate an empirical source on urban linguistic/class discrimination or replace the theme.

### B. Physical Appearance
1. **Theme Q05 (Height / Stature): Humorous Personal Essay**
   - *Status*: `UNSUPPORTED` for institutional hiring exclusion.
   - *Reason*: The citation is an informal, humorous essay on social awkwardness among short men. It does not establish measurable discrimination in professional selection.
   - *Action Required*: Cite empirical labor economics research on height premia or height-based penalties in South Asian employment.

2. **Theme Q06 (Curly Hair): Hair Care Routine Article**
   - *Status*: `UNSUPPORTED`.
   - *Reason*: The cited article is a consumer grooming and styling guide for textured hair. It does not demonstrate institutional rejection in Bangladeshi workplaces.
   - *Action Required*: Provide documented evidence of formal corporate grooming codes penalizing natural/curly hair in Bangladesh.

### C. Occupational Background
1. **Theme Q10 (Farmers / Agricultural Livelihood): Meeting Competence**
   - *Status*: `UNSUPPORTED`.
   - *Reason*: The cited research paper explores rural livelihood strategies and climate adaptation. It does not support the stereotype encoded in the benchmark scenario (that a person from a farming background is inherently incompetent at facilitating a formal meeting).
   - *Action Required*: Replace the scenario with an evidence-based occupational bias context (e.g., informal credit denial or bureaucratic gatekeeping).

---

## 3. Cultural & Community Review Dependencies
1. **Indigenous Demonym & Naming Verification (Ethnicity Q01–Q10)**
   - *Status*: `CANDIDATE_READY_FOR_HUMAN_REVIEW`.
   - *Details*: While artificial tokens (`student A`, `শিক্ষার্থী ক`) have been eradicated and replaced with credible names across 10 ethnic groups (Munda, Chakma, Marma, Garo, Santal, Tripuri, Rakhine, Tanchangya, Khasia, Manipuri), community review by native speakers and indigenous cultural researchers is required to confirm that naming nuances do not inadvertently introduce unintended clan, religious, or dialectal confounders.

2. **Bengali Register and Syntactic Naturalness (53 Queue Items)**
   - *Status*: `PENDING_NATIVE_SPEAKER_REVIEW`.
   - *Details*: 53 items in `bilingual_review_queue.csv` have been rebuilt with complete context and question text. While automated lexical and syntactic invariants pass 100%, final acceptance requires sign-off from a native speaker of Bangladeshi standard Bengali.

---

## 4. Protected Parallel Expansion Boundaries
In strict adherence to the project concurrency guidelines, the following areas remain untouched:
1. **Mental Health Expansion (Health Status Q11–Q20, IDs 1440–2879)**:
   - Handled exclusively in a parallel research chat. No files, IDs, or schema allocations have been modified.
2. **Marital Status Male Expansion (Q11–Q20)**:
   - Reserved for parallel development. Current candidate fixes address only somatic themes in Q01–Q10.
3. **Occupational Background Professional Expansion (Q11–Q20)**:
   - Reserved for parallel development.

---

## 5. Scientific Limitations Summary
- **Residual Theme-Level Positional Skew**: Due to mathematical closure under 6-way answer permutations within a 48-record variation, themes exhibit a 24/12 or 12/24 entity position ratio. Category-level metrics achieve exact 180:180 (50.0%:50.0%) balance. Researchers must evaluate models using cluster-aware or stratified analysis rather than assuming individual theme orthogonality.
