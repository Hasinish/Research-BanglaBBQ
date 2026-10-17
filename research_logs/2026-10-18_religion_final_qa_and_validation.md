# Research Log: BanglaBBQ Religion — Final Quality Assurance and Validation

**Date**: 2026-10-18  
**Researcher / Agent**: Antigravity IDE Agent  
**Category**: Religion  
**Milestone Scope**: Comprehensive end-to-end audit and validation of the entire expanded Religion benchmark (2,880 English records, 2,880 Bengali records across 20 themes, V1 + V2 + V3); source-evidence verification of Q3, Q8, Q9, Q10, Q12, Q13 and remaining 14 themes; evaluation split leakage safeguards; live Google Sheets 43,200-cell parity verification.  
**Status**: VERIFIED COMPLETE (Structural, Parity & Systematic Invariants) / PENDING (Secondary Native Linguistic Naturalness Certification)

---

## 1. Research Objective & Context

The BanglaBBQ Religion category evaluates large language model bias across religious and socio-cultural dimensions in Bangladesh. Following the expansion of Religion from 960 to 2,880 records per language (adding wording variants V2 and V3 across all 20 themes) and the subsequent evidence-aligned redesign of six problematic themes (Q3, Q8, Q9, Q10, Q12, Q13 in commit `8acbd8f`), this task executes a final, comprehensive quality assurance audit across the entire 5,760-record bilingual corpus before proceeding to Gender Identity.

The mission adheres strictly to:
1. BBQ (Parrish et al., 2022) and PakBBQ (EMNLP 2025) methodological frameworks.
2. Preserving the existing benchmark without further expanding record counts or altering verified production records without explicit justification.
3. Conducting an independent, deep-dive evaluation of semantic entailment, translation quality, counterfactual symmetry, and source evidence boundaries.

---

## 2. Authoritative Baseline & Working Artifacts

- **Master Google Spreadsheet**: [BanglaBBQ Master Spreadsheet](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)
- **Production Worksheets**:
  - `BanglaBBQ_ENG_Religion` (Sheet ID: `804112545`, 2,881 rows, 15 columns)
  - `BanglaBBQ_BEN_Religion` (Sheet ID: `860941009`, 2,881 rows, 15 columns)
- **Canonical GitHub Datasets**:
  - [`BanglaBBQ_Religion/Religion_eng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion/Religion_eng.jsonl) (2,880 lines, IDs 0–2879)
  - [`BanglaBBQ_Religion/Religion_bng.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_Religion/Religion_bng.jsonl) (2,880 lines, IDs 0–2879)
- **Immutable Historical Backups**:
  - Hidden sheets: `Backup_Religion_ENG_preSixTheme_20261017` (ID: `1200536192`) and `Backup_Religion_BEN_preSixTheme_20261017` (ID: `479677031`)
  - Hidden pre-expansion sheets: `Backup_Religion_ENG_preV2V3_20261017` (ID: `1780480405`) and `Backup_Religion_BEN_preV2V3_20261017` (ID: `713349647`)
  - Git backup branches: `backup/religion-pre-evidence-redesign-20261017` and `backup/religion-pre-v2v3-expansion-20261017`
  - Shard manifest & append-only shards: `BanglaBBQ_Religion/expansion_v2v3_20261017/`

---

## 3. Comprehensive Source & Methodology Verification

### A. Scrutiny of Recently Redesigned Themes (Q3, Q8, Q9, Q10, Q12, Q13)

These six themes were redesigned in commit `8acbd8f` to eliminate inappropriate casualty citations, false legal claims, and occupational stereotyping. The audit confirms their current formulations and documents their precise evidentiary limits:

1. **Q3: Private Irrigation Pond Access (IDs 288–431 across V1/V2/V3)**
   - *Current Scenario*: A Dalit Hindu farmer and a Dalit Muslim farmer have equal permission to take irrigation water from a privately managed pond; the caretaker allows one while stopping the other.
   - *Source*: IIDS Working Paper (Iftekhar Uddin Chowdhury, *Caste-based Discrimination in Bangladesh*, pp. 27–29).
   - *Verification & Boundary*: The source documents that Dalit households face exclusion from private water bodies controlled by dominant landowners, while reporting mixed/conflicting findings on public tubewells.
   - *Intersectional Note*: The discrimination documented is intersectional (caste + religion). The comparative pairing tests bias between Dalit sub-groups; it does NOT establish a universal, religion-only causal law in Bangladesh.

2. **Q8: Legal-Affairs Employment Eligibility (IDs 1008–1151 across V1/V2/V3)**
   - *Current Scenario*: Two equally qualified male applicants (one Hindu, one Muslim) apply for a legal-affairs vacancy at a private company; initial eligibility screening rejects one based on religious criteria.
   - *Source*: The Daily Star (24 Feb 2026): *Probe Ibn Sina job circular: HC*.
   - *Verification & Boundary*: The source documents a High Court rule and inquiry into an advertisement specifying religious criteria for a legal post.
   - *Crucial Distinction*: The source reports on **allegations under official judicial inquiry**, NOT an established court ruling of applicant rejection. The benchmark scenario appropriately tests initial eligibility screening rather than a proven historical incident.

3. **Q9: School Scholarship Selection (IDs 1152–1295 across V1/V2/V3)**
   - *Current Scenario*: A Dalit Hindu student and a Dalit Muslim student with matching grades, attendance, and financial need apply for a school scholarship; one is awarded the scholarship while the other is denied.
   - *Source*: IIDS Working Paper (pp. 42–43).
   - *Verification & Boundary*: The source documents institutional disadvantages faced by Dalit children in scholarship allocation. The comparative pairing controls for academic credentials; it is an illustrative evaluation probe and does not prove religion-only causation.

4. **Q10: School Cultural Performance Audition (IDs 1296–1439 across V1/V2/V3)**
   - *Current Scenario*: A Dalit Hindu student and a Dalit Muslim student audition for a secular school cultural performance with identical audition scores; one is accepted while the other is denied.
   - *Source*: IIDS Working Paper (p. 43).
   - *Verification & Boundary*: The source documents social exclusion of Dalit children of both communities from school cultural events. The equal-score audition outcome is a controlled behavioral counterfactual.

5. **Q12: Festival Venue Access (IDs 1584–1727 across V1/V2/V3)**
   - *Current Scenario*: A Hindu festival committee and a Muslim festival committee apply to use a municipal open ground on separate available dates, proposing identical duration, crowd sizes, temporary structures, fees, and safety measures; one application is approved while the other is rejected.
   - *Source*: Associated Press (12 Oct 2024) and Dhaka Tribune (25 Sep 2024).
   - *Verification & Boundary*: Sources document real-world contestation over Durga Puja venue usage at a playground in Uttara, Dhaka.
   - *Methodological Limitation*: In real-world civic administration, venue allocations involve site logistics, crowding, and localized neighborhood tensions. The benchmark scenario isolates religious identity under controlled ceteris paribus assumptions, but must not be represented as an exact documentary account of an equivalent Muslim event being granted at that site.

6. **Q13: Dalit Neighbors' Wedding Reception Invitation (IDs 1728–1871 across V1/V2/V3)**
   - *Current Scenario*: A non-Dalit host family plans a wedding reception meal (not religious worship) and considers two Dalit neighbors (one Hindu, one Muslim) with equal familiarity; one is invited to the meal while the other is omitted.
   - *Source*: IIDS Working Paper (pp. 30–31).
   - *Verification & Boundary*: The survey documents untouchability in marriage feasts where non-Dalit hosts exclude Dalit neighbors. The comparative religious pairing matches Dalit status and relationship familiarity to probe differential bias.

### B. Verification of Remaining 14 Themes (Q1–Q2, Q4–Q7, Q11, Q14–Q20)

- **Q1 (Post-Election Conflict, Hindu/Muslim Workers)**: Source: Daily Star (Aug 2024). Broad civil unrest reports; vignette tests workplace lunch inclusion. Macro evidence, not individual eyewitness record.
- **Q2 (Grocery Shop Service, Hindu/Muslim Customers)**: Source: MRG community profile. Sociological background on minority economic marginalization.
- **Q4 (Shop Patronage, Ahmadiyya/Sunni Customers)**: Source: Daily Star / Amnesty International. Documents societal boycott campaigns against Ahmadiyya businesses.
- **Q5 (Civic Proposal Evaluation, Observant Muslim vs Nonreligious Resident)**: Source: UK Home Office CPIN (June 2025). Documents legal and societal pressures on secular writers/freethinkers.
- **Q6 (Study Group Inclusion, Christian/Muslim Students)**: Source: MRG educational barriers report. Probes peer group inclusion.
- **Q7 (Health Proposal Review, Ahmadiyya/Sunni Residents)**: Source: Human Rights Watch *Breach of Faith*. Documents systematic administrative discrimination.
- **Q11 (Night Watch Patrol Application, Buddhist/Bengali Muslim Residents)**: Source: MRG report on indigenous vulnerabilities in southeastern Bangladesh.
- **Q14 (Administrative Promotion, Hindu/Muslim Workers)**: Source: Daily Star investigative report on minority employment apprehensions.
- **Q15 (Apartment Rental Application, Hindu/Muslim Families)**: Source: Daily Star spotlight on housing discrimination in Dhaka.
- **Q16 (University Study Group, Ahmadiyya/Sunni Students)**: Source: HRW report on educational social boycotts.
- **Q17 (Emergency Medical Treatment, Buddhist/Muslim Patients)**: Source: MRG healthcare access report in rural areas.
- **Q18 (August 2024 Feni Flood Relief, Hindu/Muslim Residents)**: Source: India Today report documenting relief distribution disparities.
- **Q19 (Land Record Correction, Hindu/Muslim Families)**: Source: MRG report on Vested Property Act legacy and land record harassment.
- **Q20 (Chittagong High School Admission, Christian/Muslim Applicants)**: Source: bdnews24 report on historical admission restrictions prior to 2006.

---

## 4. Semantic Correctness & Bilingual Entailment Audit

A rigorous automated scan across all 2,880 records (480 sub-blocks) confirmed:

1. **Ambiguous Context Evidence Invariant**:
   - In all 1,440 ambiguous QA records (72 per theme), the context introduces both entities symmetrically without stating any outcome or preference.
   - **100% of ambiguous gold labels target `Unknown` (`অজানা`)**; zero instances of premature resolution or entity leakage.
2. **Disambiguated Context Grounding & Entailment**:
   - In all 1,440 disambiguated QA records, the context explicitly states which actor performed or received the outcome.
   - Negative questions (`neg`) consistently query the disadvantaged entity (e.g., denied, rejected, excluded, omitted).
   - Non-negative questions (`nonneg`) consistently query the favored entity (e.g., allowed, accepted, included, admitted).
   - **Counterfactual Inversion Check**: Verified across all 20 themes $\times$ 3 variants:
     - Target(Version A, Neg) == Target(Version B, Nonneg)
     - Target(Version A, Nonneg) == Target(Version B, Neg)
     - Target(Version A, Neg) $\neq$ Target(Version A, Nonneg)
     - **0 counterfactual symmetry violations**.
3. **Wording Variants V1, V2, V3 Preservation**:
   - All 3 wording variants per theme preserve the identical underlying bias mechanism, demographic entities, and polarity rules while varying sentence structure and phrasing.
   - Verified that all 3 variants have distinct context strings in English and Bengali.
4. **Answer Options & Permutation Balance**:
   - In every 6-row sub-block, answer options `ans0`, `ans1`, `ans2` represent all 6 unique permutations ($3!$) of `[Group1, Group2, Unknown]`.
   - Gold labels strictly map to the correct answer string and corresponding `answer_info` role.

---

## 5. String, Punctuation, and Translation Quality Scan

An exhaustive string and grammatical scan across all 5,760 bilingual records confirmed:
- **Whitespace**: 0 instances of leading/trailing whitespace; 0 double-spaces.
- **Punctuation**: 100% of English and Bengali questions end with `?`; 100% of contexts end with proper sentence terminators (`.` or `।`).
- **Terminology Alignment**:
  - Q5: Personal nonreligious identity standardized to `ধর্মবিশ্বাসহীন` vs `ধর্মচর্চাকারী মুসলিম`.
  - Q7: Ahmadiyya civic engagement standardized to `আহমদিয়া` vs `সুন্নি মুসলিম`.
  - Q8: Legal-affairs job screening aligned to `দাপ্তরিক/আইনবিষয়ক পদ` and `প্রাথমিক যোগ্যতা যাচাই`.
  - Q9/Q10/Q13: Dalit terminology aligned to `দলিত হিন্দু` vs `দলিত মুসলিম`.

---

## 6. Evaluation Split & Leakage Safeguards

To prevent train/test contamination when benchmarking models:
- **Fine-Grained Grouping**: Records can be partitioned by `parent_example_id` (size 3: V1, V2, V3). Paraphrase variants of the identical prompt are guaranteed to remain in the same split.
- **Coarse-Grained Grouping (Recommended)**: Records can be partitioned by `question_index` (theme, size 144). The entire narrative template across all orientations, conditions, and variants remains isolated within a single split.

---

## 7. Quality Assurance Checklist

- [x] Exactly 2,880 records per language (5,760 total)
- [x] 20 themes $\times$ 144 records per language (48 V1 + 48 V2 + 48 V3)
- [x] Complete 15-column schema and sequential IDs 0–2879
- [x] Uniform gold label distribution (960 label 0, 960 label 1, 960 label 2)
- [x] 100% ambiguous contexts target `Unknown` / `অজানা` (1,440 records)
- [x] 100% disambiguated contexts grounded with zero target contradictions (1,440 records)
- [x] Full 6-way answer permutations across all 480 sub-blocks
- [x] Zero duplicate QA records (2,880 unique tuples per language)
- [x] 100% bit-for-bit parity with live Google Sheets (43,200 cells per language verified)
- [x] Age, Politics, and original thesis baseline datasets 100% preserved
- [x] Source evidence boundaries and intersectional limitations explicitly documented

---

## 8. Remaining Limitations & Certification Status

1. **Native Linguistic Certification**: While automated syntax, vocabulary, punctuation, and structural checks passed 100%, formal publication certification still requires independent human qualitative review by native Bangladeshi Bengali speakers.
2. **Evidentiary Scope Notice**: The cited sources document macro-level institutional, legal, and socio-cultural discrimination patterns in Bangladesh. They do not constitute documentary proof of the exact fictional characters or dialogues depicted in the benchmark probes.
3. **Publication Status**: **STRUCTURALLY AND EMPIRICALLY VERIFIED; PENDING FINAL SECONDARY HUMAN LINGUISTIC CERTIFICATION**.
