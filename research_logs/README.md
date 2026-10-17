# BanglaBBQ Research Logs

Welcome to the **BanglaBBQ Research Logs** directory (`research_logs/`). This directory houses detailed, evidence-backed, reproducible records of every substantial milestone, audit, dataset repair, benchmark expansion, linguistic review, and experimental validation in the BanglaBBQ project.

---

## 1. Role & Relationship to `memory/`

To maintain clarity and separation of concerns across human researchers, AI coding agents (Antigravity, Cursor, Claude Code), and conversational assistants (ChatGPT):

- **`memory/` (High-Level State & Dashboard)**:
  - Houses the authoritative, concise project dashboard (`state.md`), chronological overview (`history.md`), official mission (`purpose.md`), directory map (`index.md`), and synchronization protocol (`README.md`).
  - Intended to be read at the start of every session for immediate orientation.
- **`research_logs/` (Detailed Technical Evidence & Audit Reports)**:
  - Houses deep-dive investigative logs, before/after diffs, exact row ranges, backup links, statistical distributions, linguistic rationales, and test suite execution logs.
  - Every major dataset change or architectural decision must produce a dedicated research log.

---

## 2. Mandatory Research Logging Rules

1. **Standardized Naming Convention**:
   - Every research log file must follow the pattern:  
     `research_logs/YYYY-MM-DD_<topic_in_snake_case>.md`  
     *(Example: `research_logs/2026-10-17_age_q1_context_alignment.md`)*
2. **Template Adherence**:
   - All logs must follow the standard structure defined in [`research_logs/TEMPLATE.md`](TEMPLATE.md).
3. **Empirical Evidence & Zero Fabrication**:
   - Never invent statistics, test results, citations, or commit SHAs.
   - Record exact pre-edit backup URLs or paths, sheet row ranges, and record ID ranges.
4. **Index Maintenance**:
   - Whenever a new research log is created, add an entry to the index table below.
5. **Quality over Quantity**:
   - Clearly document remaining limitations, linguistic nuances, and pending reviews. Never claim a dataset is publication-ready based purely on automated structural validation.

---

## 3. Chronological Index of Research Logs

| Date | Log File | Category | Focus / Scope | Status |
| :--- | :--- | :---: | :--- | :---: |
| **2026-10-17** | [`2026-10-17_age_q1_context_alignment.md`](2026-10-17_age_q1_context_alignment.md) | Age (Q1) | Retrospective audit and context alignment expanding unique contexts from 11 to 16 | `VERIFIED COMPLETE` |
| **2026-10-17** | [`2026-10-17_age_q9_context_alignment.md`](2026-10-17_age_q9_context_alignment.md) | Age (Q9) | Retrospective audit and alignment of technology stereotypes expanding unique contexts from 60 to 144 | `VERIFIED COMPLETE` |
