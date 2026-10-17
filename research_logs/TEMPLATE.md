# Research Log Template

```markdown
# Research Log: [Topic / Milestone Name]

**Date**: YYYY-MM-DD  
**Researcher / Agent**: [Name / Agent Identifier]  
**Category**: [Age | Politics | Religion | Gender Identity | Physical Appearance | Regional Affiliation | Educational Background | Marital Status | Mental Health]  
**Milestone Scope**: [Specific templates, row ranges, or pipeline component]  
**Status**: [VERIFIED COMPLETE | IN PROGRESS | PENDING | UNVERIFIED | BLOCKED]  

---

## 1. Research Objective & Context
- Summary of the research goal and purpose of this task.
- Traceability to seniors' thesis (T2510616), BBQ, or PakBBQ methodological references.

---

## 2. Source Files & Live Google Sheet References
- **Master Google Sheet**: [BanglaBBQ Master Spreadsheet](https://docs.google.com/spreadsheets/d/1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY/edit)
- **Worksheet Title & ID**: e.g., `BanglaBBQ_BEN_Age` (ID: `1006819770`)
- **Sheet Range & Row Count**: e.g., Rows `A2:O33` (32 data rows)
- **Record ID Range**: e.g., `id: 0` to `31`
- **Canonical GitHub Paths**: e.g., `BanglaBBQ_BEN_New/Age.jsonl`

---

## 3. Original Issue & Forensic Evidence
- Detailed description of the defect, gap, or inconsistency identified in the baseline.
- Why the change was required (e.g., collapsed contexts, duplicate records, mistranslations, label errors).
- Pre-edit backup URL or file path: [Link to backup]

---

## 4. Methodology & Decisions Made
- Methodological rationale (BBQ counterfactual alignment, PakBBQ adaptation, linguistic nuances).
- Design decisions regarding vocabulary, cultural grounding, or permutations.
- Preserved invariants (e.g., gold label indices, metadata schema, condition balances).

---

## 5. Exact Changes & Before/After Comparisons
- Summary of modified fields (contexts, answer choices, metadata).
- Concrete before/after examples demonstrating the transformation:
  - **Before**: `[Original text]`
  - **After**: `[Updated text]`

---

## 6. Pre-Edit and Post-Edit Backups
- **Pre-Edit Backup Reference**: [URL / Local path]
- **Post-Edit Backup Reference**: [URL / Local path]

---

## 7. Quality Assurance & Validation Results
- Description of automated and manual tests executed (e.g., test scripts in `scripts/`).
- Invariant verification checklist:
  - [ ] Record count matches expected target
  - [ ] Contiguous 0-indexed sequential IDs
  - [ ] 15-column schema integrity and valid JSON types
  - [ ] Condition and polarity balances (50% ambig, 50% disambig; 50% neg, 50% nonneg)
  - [ ] Ambiguous context gold label targets Unknown
  - [ ] Bilingual metadata alignment
  - [ ] Context uniqueness counts
  - [ ] Zero unintended duplicate QA pairs
  - [ ] Non-target themes preserved 100% byte-for-byte

---

## 8. Remaining Limitations & Open Issues
- Independent linguistic or cultural reviews required.
- Known limitations or blockers preventing full publication readiness.
- Potential impact on review worksheets or downstream SafeLLM evaluation.

---

## 9. Git & Commit Tracking
- **Git Commit SHA**: `[Commit SHA]`
- **Committed Files**: List of modified and created files.
- **Remote Synchronization**: Push status to `origin/main`.
```
