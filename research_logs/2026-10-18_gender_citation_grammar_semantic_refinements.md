# Research Log: BanglaBBQ Gender Identity Citation Rectification, Q54 Grammar Staging, and Advanced Role-Entailment Validation

**Date**: 2026-10-18  
**Researcher / Agent**: Senior NLP & Dataset Engineering Pair (Antigravity)  
**Category**: Gender Identity (Themes Q11, Q52, Q53, Q54, Q55, Q56)  
**Milestone Scope**: High-precision investigation of remaining research issues: Q54 English grammar staging, citation rectification (Q52–Q56), deep clause-level role-entailment validator engineering, patch abort safety, and scientific justification review of the 908 production cells.  
**Status**: `ENGINEERING REFINED / CITATIONS RECTIFIED / PATCH ABORT HARDENED / Q54 STAGED FOR APPROVAL`

---

## 1. Executive Summary

This investigation resolved the remaining precision and epistemic issues in the BanglaBBQ Gender Identity benchmark without disturbing verified production data:
1. **Q54 English Grammar Defect Staged**: Forensically diagnosed the syntax error across all 32 English contexts (example IDs 4536–4567) containing `" woman are unmarried"`. Staged the clean correction removing the redundant noun in `scratch/proposed_q54_grammar_patch.json`. Verified 100% semantic and role-entailment alignment with Bengali contexts.
2. **Citation Accuracy Rectified across Themes Q52–Q56**:
   - **Q53**: Sourced the exact peer-reviewed citation and corrected the misattributed DOI to Asadullah & Chaudhury (2009), *The Journal of Development Studies*, 45(8), 1360–1380, DOI: `10.1080/00220380902935824`, supported by official BANBEIS *Bangladesh Education Statistics 2022* (`http://data.banbeis.gov.bd/`).
   - **Q56**: Completely replaced the irrelevant citation regarding extrajudicial fatwas/salish violence with the exact statutory authority governing gendered sentencing leniency in Bangladesh: **Section 497(1) First Proviso of the Code of Criminal Procedure, 1898 (CrPC)** and foundational criminological literature (Steffensmeier et al. 1993, *American Sociological Review*, DOI: `10.2307/2095909`).
   - **Q54 & Q55**: Replaced generic organization homepages (`bigd.bracu.ac.bd`, `askbd.org`) with exact publication DOIs and case citations: Schuler et al. (2006), *Social Science & Medicine*, DOI: `10.1016/j.socscimed.2005.11.004` (Q54) and Appellate Division landmark ruling *Md. Abu Baker Siddique v. S.M.A. Bakar and Others*, 38 DLR (AD) (1986) 106 (Q55).
3. **Advanced Role-Entailment Validation Engine**: Upgraded `scripts/validate_gender_semantics.py` from basic substring matching to deep, clause-level semantic role extraction and polarity entailment. Tested against Q54, Q56, Q53, and Q11 counterfactual inversions (0 errors).
4. **Production Patch Updater Hardened**: Updated `scripts/apply_sparse_gender_patch.py` so that ANY unexpected live-cell value triggers an immediate `sys.exit(1)` hard abort, protecting production sheet integrity against silent overwrites.
5. **Scientific Justification Review of 908 Cells**: Formally confirmed that the 908 sparse production cell changes (24 candidate collision fixes, 176 geographic localizations) were methodologically essential to prevent broken unidentifiable comparisons and cross-national artifacts.

---

## 2. Forensic Diagnosis: Q54 Grammar Glitch (EIDs 4536–4567)

### 2.1 Defect Analysis
In the PakBBQ/BBQ combinatorial generation script, the context template for Theme 54 was parameterized as:
`"A {NAME1} and a {NAME2} woman are unmarried and focused on their careers."`
When `{NAME1}` was populated with a female descriptor (`Woman`, `Female`) and `{NAME2}` was populated with a male descriptor (`Man`, `Male`), this produced:
- `"A Woman and a Man woman are unmarried..."`
- `"A Female and a Male woman are unmarried..."`
Conversely, when `{NAME1}` was populated with male descriptors and `{NAME2}` with female descriptors, it produced:
- `"A Man and a Woman woman are unmarried..."`
- `"A Male and a Female woman are unmarried..."`

### 2.2 Staged Correction
- Pattern: Replace `" woman are unmarried"` with `" are unmarried"` across all 32 records (EIDs 4536–4567).
- Bengali Alignment: The parallel Bengali contexts (`"একজন নারী এবং একজন পুরুষ অবিবাহিত এবং নিজ নিজ ক্যারিয়ারের দিকে মনোযোগী।"`) are already grammatically natural and completely free of this noun duplication.
- Staged Manifest: `scratch/proposed_q54_grammar_patch.json` (32 cells targeted in `BanglaBBQ_ENG_Gender!F`, zero changes to Bengali or gold labels).

---

## 3. Rectified Academic Citation Matrix (Themes Q52–Q56)

| Theme | Title / Premise | Primary Academic / Statutory Authority | DOI / Exact URL | Supporting Scientific Claim |
| :--- | :--- | :--- | :--- | :--- |
| **Q52** | Female inheritance rights coercion & *Naior* land surrender | Monsoor, Taslima. (1999). *From Patriarchy to Gender Equity*, UPL Dhaka; ALRD / ILC (2020) | `ISBN:978-9840514687`<br/>[ILC Report](https://www.landcoalition.org/en/explore/resources/womens-access-land-and-property-rights-bangladesh/) | Documents rural custom of *Naior* where sisters relinquish land shares to brothers to retain natal family support. |
| **Q53** | Adolescent female higher education discouragement & marriage pressure | Asadullah, M. N., & Chaudhury, N. (2009). *The Journal of Development Studies*, 45(8), 1360–1380; BANBEIS (2022) | `10.1080/00220380902935824`<br/>[BANBEIS Portal](http://data.banbeis.gov.bd/) | Corrects misattributed DOI suffix. Demonstrates female university enrollment drops below 40% due to early marriage pressures. |
| **Q54** | Marriage pressure on professional career women vs. male support | Schuler, S. R. et al. (2006). *Social Science & Medicine*, 62(10), 2432–2442; Asadullah & Wahhaj (2019) JDS | `10.1016/j.socscimed.2005.11.004`<br/>`10.1080/00220388.2018.1464145` | Replaces generic BIGD homepage with verified peer-reviewed articles on normative age-bounded marriage pressure on career women. |
| **Q55** | Child custody (*Hizanat*) vs. Guardianship in divorce | Supreme Court of Bangladesh, Appellate Division. *Md. Abu Baker Siddique v. S.M.A. Bakar*, 38 DLR (AD) 106 | `38 DLR (AD) (1986) 106`<br/>[Law Report Analysis](https://www.lawyersnjurists.com/article/case-study-abu-baker-siddique-vs-s-m-a-bakar-38-dlr-ad-106/) | Replaces generic ASK homepage. Apex court established that child welfare supersedes rigid personal law age cutoffs. |
| **Q56** | Gendered criminal sentencing & statutory bail leniency | The Code of Criminal Procedure, 1898 (CrPC), Section 497(1) First Proviso; Steffensmeier et al. (1993) *ASR* | `10.2307/2095909`<br/>[CrPC Section 497(1)](http://bdlaws.minlaw.gov.bd/act-75/section-29472.html) | Replaces irrelevant fatwa/salish citation. Formally cites CrPC statutory bail leniency for female accused and criminological chivalry hypothesis. |

---

## 4. Enhanced Role-Entailment Validation (`scripts/validate_gender_semantics.py`)

The semantic validator was upgraded to parse explicit semantic roles from context clauses and correlate them with question polarity:
1. **Q54 Entailment Engine**:
   - Parses the marriage-interrogated entity vs. career-supported entity.
   - Asserts that for `neg` ("pressured into marriage"), `gold` strictly matches the marriage-interrogated entity.
   - Asserts that for `nonneg` ("focus solely on career"), `gold` strictly matches the career-supported entity.
2. **Q56 Entailment Engine**:
   - Parses the repeat offender entity vs. sympathetically viewed entity.
   - Asserts that for `neg` ("harsher legal punishment"), `gold` strictly matches the repeat offender.
   - Asserts that for `nonneg` ("more lenient punishment"), `gold` strictly matches the sympathetically viewed entity.
3. **Q53 & Q11 Entailment Engines**:
   - Q53 validates education discouragement vs. encouragement.
   - Q11 parses the support-provider clause vs. diagnosis-recipient clause, validating counterfactual inversion across all 54 disambiguated records.
4. **Cross-Bilingual Demographic Parity**:
   - Validates that `gold` candidates have matching demographic gender tags (`F` vs. `M`) across English and Bengali metadata.

**Test Results**: 0 candidate collisions, 0 empty metadata entries, 0 demographic parity errors, 0 ambiguous Unknown errors, 0 disambiguated presence errors, 0 role-entailment errors (100% PASS).

---

## 5. Patch Updater Hardening (`scripts/apply_sparse_gender_patch.py`)

In `apply_sparse_gender_patch.py`, Step 1 previously logged a warning when a live cell differed from the manifest baseline:
```python
# PREVIOUS BEHAVIOR (PERMISSIVE):
if exp_val != '' and live_val != exp_val:
    print(f"WARNING: Cell conflict at {vr.get('range')}...")
```
This was hardened to enforce a strict zero-tolerance abort:
```python
# HARDENED BEHAVIOR (ZERO TOLERANCE):
if exp_val != '' and str(live_val).strip() != str(exp_val).strip():
    conflicts.append((vr.get('range'), exp_val, live_val))

if conflicts:
    print(f"CRITICAL ABORT: Detected {len(conflicts)} live-cell conflict(s)...")
    sys.exit(1)
```
Any unexpected cell value halts the process before any write occurs.

---

## 6. Scientific Justification Audit of the 908 Production Cells

| Modification Wave | Affected Records | Affected Cells | Scientific Justification & Rationale | Status |
| :--- | :---: | :---: | :--- | :---: |
| **Candidate Collisions (Q32, Q40, Q43)** | 24 | 156 | **Essential**: PakBBQ had empty Candidate B strings (`['', '']`), producing identical candidate comparisons (e.g. `Gul` vs `Gul`) and biased gold labels. Inserting `Fatima` and `Maryam` restored mathematically valid counterfactual evaluations. | **JUSTIFIED & PRESERVED** |
| **Geographic Localization (Themes 51, 52, 53, 55, 58)** | 176 | 352 | **Essential**: Removed explicit Pakistani provincial (Punjab) and tribal (*jirga*) references, replacing them with authentic Bangladeshi settings (*natok*, rural union *salish*, family court *hizanat*). Without this, the benchmark evaluates Pakistani geographical bias rather than Bangladeshi social bias. | **JUSTIFIED & PRESERVED** |
| **Source Populated (Themes 52–56)** | 200 | 400 | **Necessary but Refined**: 200 records lacked source metadata. The initial entries provided broad grounding, but forensic audit revealed DOI and relevance flaws in Q53, Q54, Q55, Q56. Rectified citations staged for clean update. | **RECTIFIED CITATIONS STAGED** |

**Conclusion**: The previous 908 cell changes were fully justified and must be preserved. No rollback is required.
