# history.md — Historical Research Log

<!-- IMPORTANT FOR AGENTS: Always prepend new conversation log entries to the top of this list (most recent first). Do not append to the bottom. -->

- **[2026-10-17] Convo d939a6e8-f448-4b70-8668-891b85c48e7b**: **Recorded Age Benchmark Phase Acceptance, Preserved Q2, and Prioritized Remaining Six Categories**.
  - **Age Accepted for Current Research Phase**: Formally accepted the Age benchmark (2,920 English records and 2,920 Bengali records across 20 themes) for the current research phase. All previously reported structural repairs and context alignments are complete and verified (Q1, Q3, Q8–Q12, and Q19).
  - **Age Q2 Review & Preservation Decision**: Age Q2 (IDs 32–127, 96 records per language) was reviewed for translation issues involving grandparent terminology, age references, and context phrasing. The researcher explicitly decided to leave Q2 and the entire Age benchmark unchanged for now. No additional Age edits are authorized.
  - **Zero Dataset or Spreadsheet Modifications**: This is a strictly memory-only synchronization. All datasets on disk (`BanglaBBQ_BEN_New/Age.jsonl`, `PakBBQ_Age_English.csv`, etc.), live Google Sheets, validation scripts, and research logs remain completely untouched.
  - **Prioritization of Six Remaining Categories**: Shifted active research focus to improving and expanding the remaining six categories in priority sequence: (1) Gender Identity, (2) Physical Appearance, (3) Regional Affiliation, (4) Educational Background, (5) Marital Status, and (6) Mental Health.
  - **Outstanding Publication-Readiness Considerations**: Transparently documented that independent native Bengali linguistic review and unresolved cross-language cultural alignment (English Pakistani baseline vs Bengali Bangladeshi localizations) remain open requirements before final publication certification.

- **[2026-10-17] Convo d939a6e8-f448-4b70-8668-891b85c48e7b**: **Completed Age Benchmark Translation Repairs (Q19, Q3, Q8, Q10, Q11, Q12), Cultural Localization Audit, and 100% Context Parity**.
  - **Comprehensive Dataset Repairs (332 modified records)**:
    - **Age Q19 (IDs 2360–2639, 118 modified rows)**: Fixed critical semantic mistranslation across 88 disambiguated rows where neighbor was incorrectly substituted for "friend" (48 rows -> `তার এক বন্ধু তার নাম দিয়ে দিয়েছিল`) and "someone else" (40 rows -> `অন্য কেউ তার নাম দিয়ে দিয়েছিল`). Differentiated "The teen" (`কিশোরটি` / `এক কিশোর`) from "The teenager" (`কিশোরবয়সী ছেলেটি` / `এক কিশোরবয়সী ছেলে`) in both context and answer choices across 40 rows. Unique contexts expanded from 120 to 140 (100% parity with English).
    - **Age Q3 (IDs 128–199, 24 modified rows)**: Resolved lexical collapse between "The Zoomer" (`জেন-জি প্রফেসর`) and "The Gen-Z kid" (`জেন-জি তরুণ প্রফেসর`) across context and answer choices. Unique contexts expanded from 24 to 36 (100% parity with English).
    - **Age Q8 (IDs 712–911, 40 modified rows)**: Differentiated "The teen" (`কিশোরটি` / `এক কিশোর`) from "The teenager" (`কিশোরবয়সী ছেলেটি` / `এক কিশোরবয়সী ছেলে`). Unique contexts expanded from 80 to 100 (100% parity with English).
    - **Age Q10 (IDs 1200–1535, 48 modified rows)**: Differentiated "The high schooler" (`স্কুলপড়ুয়া শিক্ষার্থীটি` / `একজন স্কুলপড়ুয়া শিক্ষার্থী`) from "The high school student" (`হাই স্কুলের শিক্ষার্থীটি` / `হাই স্কুলের একজন শিক্ষার্থী`). Unique contexts expanded from 144 to 168 (100% parity with English).
    - **Age Q11 (IDs 1536–1703, 54 modified rows)**: Differentiated high schooler from high school student, and aligned disambiguated actions between fights (`মারামারিতে জড়ায় না`) and confrontations (`কারো সাথে ঝামেলায় জড়ায় না`). Unique contexts expanded from 72 to 84 (100% parity with English).
    - **Age Q12 (IDs 1704–1871, 48 modified rows)**: Differentiated high schooler from high school student, and aligned senior actions between fights (`মারামারিতে জড়ান না`) and confrontations (`কারো সাথে ঝামেলায় জড়ান না`). Unique contexts expanded from 72 to 84 (100% parity with English).
  - **100% Context Uniqueness Across ALL 20 Themes**: Verified that every theme from Q1 to Q20 in Bengali now has 100% context uniqueness matching English (total 2,920 records).
  - **Google Sheets & Local Synchronization**: Pushed batch updates to live Google Sheet `BanglaBBQ_BEN_Age` (1,224 rows / 18,360 cells updated across the 6 theme ranges) and synchronized canonical JSONL [`BanglaBBQ_BEN_New/Age.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New/Age.jsonl) with 0 discrepancies.
  - **Bangladeshi Cultural Localization Audit (TM records Q13–Q20, IDs 1872–2919)**: Conducted deep forensic scan of Pakistani commercial and geographic references in English (Imtiaz, InDrive, Jalal Sons, Lahore, Karachi). Verified that Bengali translation already authentically localized them (Shwapno, Pathao, Tasty Treat, Chittagong, Dhaka). Authored evidence-backed recommendations for future English benchmark alignment.
  - **Research Logs Authored**: Created [`research_logs/2026-10-17_age_q19_semantic_repair.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q19_semantic_repair.md), [`research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q3_q8_q10_q11_q12_lexical_repairs.md), and [`research_logs/2026-10-17_age_cultural_localization_audit.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_cultural_localization_audit.md), updating index in [`research_logs/README.md`](file:///d:/Research-BanglaBBQ/research_logs/README.md).
  - **QA & Invariant Verification**: Updated [`scripts/sync_and_validate_age.py`](file:///d:/Research-BanglaBBQ/scripts/sync_and_validate_age.py) with 10 automated invariant checks, passing all 10 tests with 100% compliance.

- **[2026-10-17] Convo d939a6e8-f448-4b70-8668-891b85c48e7b**: **Synchronized Age Q1/Q9 Context Alignments from Google Sheets and Established Research Logs System**.
  - **Live Dataset Synchronization**: Exported and synchronized verified Age updates from Google Sheet `BanglaBBQ_BEN_Age` to local production dataset [`BanglaBBQ_BEN_New/Age.jsonl`](file:///d:/Research-BanglaBBQ/BanglaBBQ_BEN_New/Age.jsonl):
    - **Age Q1 (IDs 0–31)**: Context diversity alignment expanding unique Bengali contexts from 11 to 16, matching English combinatorial combinations with distinct phrasing for observer perspective and youth descriptors.
    - **Age Q9 (IDs 912–1199)**: Context and answer alignment expanding unique Bengali contexts from 60 to 144 (72 ambiguous, 72 disambiguated, matching English count 144) and aligning 272 answer choices in columns H–J with context demographic descriptors (e.g. ব্যক্তিটি vs লোকটি, প্রবীণ vs পেনশনভোগী).
    - Preserved 100% of all other 2,600 records across Templates 2–8 and 10–20 without unintended mutations.
  - **Comprehensive QA Test Execution**: Developed [`scripts/sync_and_validate_age.py`](file:///d:/Research-BanglaBBQ/scripts/sync_and_validate_age.py) and executed 10-invariant validation suite, confirming: 2,920 total records, sequential IDs (0–2919), 15-column schema, 1,460 ambig / 1,460 disambig, 1,460 neg / 1,460 nonneg, all ambiguous contexts targeting Unknown (`তথ্য অপর্যাপ্ত`), 16 unique contexts in Q1, 144 unique contexts in Q9, and 100% English–Bengali metadata alignment.
  - **Permanent Research Logs Directory Established**:
    - Created [`research_logs/`](file:///d:/Research-BanglaBBQ/research_logs) with [`research_logs/README.md`](file:///d:/Research-BanglaBBQ/research_logs/README.md) (logging rules & index) and [`research_logs/TEMPLATE.md`](file:///d:/Research-BanglaBBQ/research_logs/TEMPLATE.md) (standard template).
    - Authored retrospective research logs [`research_logs/2026-10-17_age_q1_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q1_context_alignment.md) and [`research_logs/2026-10-17_age_q9_context_alignment.md`](file:///d:/Research-BanglaBBQ/research_logs/2026-10-17_age_q9_context_alignment.md) detailing exact row ranges, pre-edit backup references, diffs, and validation outputs.
  - **Memory & Protocol Governance Updated**: Updated [`memory/README.md`](file:///d:/Research-BanglaBBQ/memory/README.md) establishing mandatory research logging rules, updated [`memory/state.md`](file:///d:/Research-BanglaBBQ/memory/state.md) with verified Age progress, and updated [`memory/index.md`](file:///d:/Research-BanglaBBQ/memory/index.md). Flagged older exemplar rows in `Review_Age_20_Templates` (retained untouched).

- **[2026-10-17] Convo d939a6e8-f448-4b70-8668-891b85c48e7b**: **Established BanglaBBQ Official Research Mission & Shared GitHub Memory System**.
  - **Memory Entry Point**: Authored [`memory/README.md`](file:///d:/Research-BanglaBBQ/memory/README.md) as the mandatory first document for all coding agents and researchers, establishing the core mission (repairing/expanding seniors' T2510616 thesis benchmark, using BBQ/PakBBQ as methodological references), hierarchy of tools (Sheets = working canvas, GitHub = versioned repo, memory = single source of truth for project progress), and multi-phase synchronization protocol between ChatGPT and IDE coding agents.
  - **Research Mission Formalized**: Overhauled [`memory/purpose.md`](file:///d:/Research-BanglaBBQ/memory/purpose.md) to define the foundational thesis heritage, specific defects of legacy files in `Dataset_ BanglaBBQ_Old/`, BBQ and PakBBQ invariant frameworks, the 9 bias categories, bilingual standards, and academic publication goals preceding SafeLLM experiments.
  - **Dashboard Restructuring**: Overhauled [`memory/state.md`](file:///d:/Research-BanglaBBQ/memory/state.md) into a concise 9-category dashboard with verified record counts, explicit status markers (`VERIFIED COMPLETE`, `IN PROGRESS`, `PENDING`), live Google Sheet tab IDs, active paths, and transparent research-quality blockers (Religion source/translation review, Age Pakistani entity localization).
  - **Reconciliation & Correction of Historical Record**:
    - Recorded full completion of Religion Phase 2 (commits `6b415c3` and `f49fe17`) which was previously left as "Started".
    - Clarified the multi-stage evolution of Politics (112 legacy -> 160 expansion -> 120 deduplication/correction -> 240 permutation expansion -> 960 20-theme benchmark).
    - Removed stale Age translation blockers (all 2,920 rows are fully translated in `BanglaBBQ_BEN_Age` and `BanglaBBQ_BEN_New/Age.jsonl`; current outstanding work is cultural entity localization in TM rows 1,872–2,919).
    - Clarified that `personal_info.md` is git-ignored via `.gitignore` for developer privacy and is not part of the tracked public GitHub memory.
  - **Repository & Dataset Map Updated**: Overhauled [`memory/index.md`](file:///d:/Research-BanglaBBQ/memory/index.md), verifying every listed file path on disk, separating active production datasets from legacy baselines, and cataloging all 82 automation scripts.

- **[2026-10-16] Convo 88107fa0-e853-403f-8950-4ede808b9fdb**: **Completed Religion Benchmark Backup, Export, Google Sheets Cleanup, and CI Validation**.
  - **Worksheet Backups**: Exported all 4 Religion worksheets (Phase 1 ENG/BEN and Phase 2 ENG/BEN) to versioned GitHub backup `backups/religion_sheets_backup_20261016/` with raw API dumps, metadata, and SHA-256 proofs (`6b415c3`).
  - **Active Dataset Export**: Exported Phase 2 (20 source-backed themes $\times$ 48 records = 960 records per language, 1,920 total) to canonical directory `BanglaBBQ_Religion/` (`Religion_eng.jsonl` and `Religion_bng.jsonl`).
  - **Google Sheets Cleanup**: Safely renamed Phase 2 sheets to `BanglaBBQ_ENG_Religion` (ID: `804112545`) and `BanglaBBQ_BEN_Religion` (ID: `860941009`). Safely deleted legacy Phase 1 worksheets after backup confirmation.
  - **Test Suite & CI Integration**: Built 10-invariant offline test suite `scripts/validate_religion_dataset.py` and live verification script `scripts/verify_religion_live.py`. Integrated Religion validation into `.github/workflows/validate.yml` (`f49fe17`). Confirmed 100% bit-for-bit parity between live sheets and GitHub JSONL.
  - **Remaining Limitations Documented**: Flagged need for independent source relevance checks (e.g. Q20 Christian class enrollment vs ECOI source), naturalness review of Bengali phrasing, and realistic counterfactual auditing.

- **[2026-10-16] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Completed Politics Benchmark Audit, Translation Repair, CI Integration, and Citation Authoring**.
  - **Answer Info Alignment**: Aligned 720 Bengali `answer_info` records to English canonical identities across themes Q6–Q20.
  - **Translation Repair**: Repaired stilted Bengali administrative translations in Q6 (বাতিল -> নামঞ্জুর for nomination rejection), Q10 (ভোটকেন্দ্রে -> ভোটবুথে for polling booth), Q16 (বাতিল -> নাকচ for bill veto), and Q18 (গ্রেপ্তার -> আটক for administrative detention).
  - **Source Validation**: Replaced insufficient source URLs for Q6 (HRW freedom of assembly) and Q13 (CPJ Dainik Dinkal press declaration cancellation).
  - **CI & Repository Governance**: Developed 10-invariant offline test suite (`scripts/validate_politics_dataset.py`) and GitHub Actions workflow (`.github/workflows/validate.yml`). Authored repository `CITATION.cff`, updated `README.md`, and fixed relative links in `scripts/README.md`. Synchronized live Google Sheets tabs with 0 differences and verified untouched baseline Q1–Q5 (`45e0201`, `9f9f91e`, `fce62b3`).

- **[2026-10-16] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Expanded Politics Benchmark to 20 Themes (960 Records per Language)**.
  - **Thematic Expansion**: Preserved baseline Q1–Q5 100% untouched. Added 15 new source-backed themes (Q6–Q20) with 48 records each (720 new records per language) across 2 counterfactual orientations, 2 context conditions, 2 question polarities, and all 6 answer permutations ($3!$).
  - **Dataset Metrics**: Total dataset reached exactly 960 records per language (IDs 0–959) on live Google Sheet tabs `BanglaBBQ_ENG_Politics` and `BanglaBBQ_BEN_Politics` and local JSONL in `BanglaBBQ_Politics/`.
  - **Automated Validation**: Passed 11 automated verification checks (0 duplicate QA records, 0 label errors, perfectly uniform 320/320/320 label distribution, 100% bilingual parity, and full Age styling replication across rows 1–961).

- **[2026-10-16] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Expanded Politics Benchmark to 240 Records (Permutation Expansion)**.
  - Expanded 5 themes to 48 rows each by implementing full 6-way answer permutations across all 8 context-question combinations.
  - Formatted live Google Sheet tabs A1:O241 with Age-replicated conditional formatting and synced local JSONL files.

- **[2026-10-16] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Forensic Audit & Correction of Politics Benchmark (120 Clean Records)**.
  - Corrected 40 disambiguated gold labels strictly grounded in context text.
  - Eliminated speculative probability wording ("more likely to") across Q1–Q5 in English and Bengali with direct factual event questions.
  - Pruned 40 exact duplicate records to yield 120 unique records (24 per template, 50% ambig / 50% disambig, 50% neg / 50% nonneg, uniform 40/40/40 label distribution). Re-indexed IDs 0–119 and synced to live Google Sheets.

- **[2026-10-16] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Corrected Bengali Age Family Terms & Q7 Comparative Formulation**.
  - Corrected 56 rows of Grandparent/Grandchild dual mistranslations (দাদা-দাদি -> দাদু, নাতি-নাতনি -> নাতিটি) directly in live Google Sheet `BanglaBBQ_BEN_Age` and local mirror `BanglaBBQ_BEN_New/Age.jsonl`.
  - Corrected 48 rows of Q7 comparative meaning mismatch ("কার নতুন আইডিয়ার অভাব ছিল?" -> "কে তুলনামূলকভাবে কম সৃজনশীল ছিল?").
  - Verified 100% mathematical parity with 0 label changes and 0 entity leaks.

- **[2026-10-15] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Audited Legacy Politics Benchmark & Initialized Google Sheets Tabs**.
  - Audited legacy Politics benchmark (`Dataset_ BanglaBBQ_Old/Politics/`).
  - Created and styled two new tabs in master Google Spreadsheet: `BanglaBBQ_ENG_Politics` (ID: `1888499205`) and `BanglaBBQ_BEN_Politics` (ID: `2128232344`) with 112 rows each across 15 standard columns.
  - Conducted forensic breakdown of all 5 initial Politics templates, identifying human rights source documentation (HRW, Amnesty, CPJ).

- **[2026-10-14] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Completed Full 2,920-Row Bengali Age Translation & Comparative Review Tab**.
  - Created executive 3-column review tab `Review_Age_20_Templates` (Tab Index 0, ID: `99887766`) in Google Sheet for Provat Saha's review, comparing Original PakBBQ English vs Legacy Thesis BanglaBBQ vs Hasin's authentic Bengali translations.
  - Translated and pushed all remaining rows for Templates 11 to 20 into Google Sheet `BanglaBBQ_BEN_Age` (Rows 1538 to 2921), bringing total translated rows to exactly 2,920.
  - Executed forensic audit across entire dataset (0 leaks, 0 inflections, 100% invariant parity) and exported production-ready dataset to `BanglaBBQ_BEN_New/Age.jsonl`.

- **[2026-10-13] Convo 95d8ba9a-47de-445d-b9f2-8ce163f6afcd**: **Workspace Initialization, Legacy Audit, and Initial Age Translations**.
  - Established workspace memory system and cloned official `PakBBQ_Repo` (EMNLP 2025).
  - Deep forensic analysis of thesis artifacts (`T2510616.pdf` and `T2510616_IEEE_Paper.pdf`).
  - Uncovered critical flaws in legacy `Dataset_ BanglaBBQ_Old/`: truncated to 799 rows in Bengali Age, 101 broken JSON lines in combined file, literal Google Translate errors ("জুমারটি", "অবিশ্বাস্যযোগ্য").
  - Authenticated Google OAuth token with Google Sheets API (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`).
  - Populated `PakBBQ_ENG_Age` (2,920 rows), created `BanglaBBQ_BEN_Age`, and fully translated initial 328 rows (Templates 1–4).
