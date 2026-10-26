# Marital Status - BanglaBBQ local research and QA report

**Run date:** 2026-10-26 (Asia/Dhaka). **Scope:** `Marital_status` only; read-only external research, files generated locally.

**Structural test result:** PASS; 0 failures. **Publication-ready:** NO.

## Live grounding and preservation
- Latest GitHub `main` project memory inspected (`memory/README.md`, `purpose.md`, `state.md`, `index.md`, relevant `history.md`). Last project memory checkpoint was 2026-10-20. Marital Status was still listed PENDING.
- Original legacy Marital_status English/Bengali files each contained 100 parseable JSONL rows, question_index="1" only, 0..99 IDs, no b orientation, 25/50/25 answer-label positions, all pointing to the same irrelevant US PMID 29307947. Legacy originals were left untouched; no legacy QA content was copied.
- Master Google Sheet metadata showed **no current Marital Status tab**. Canonical live Education and Politics exemplars confirmed their 15-column sheet order, metadata shape and string question_index. Local JSONL uses the independent canonical JSONL key order, which differs from the spreadsheet column layout.
- Scanned `id` column in 10 active English/Bengali production tabs (Age, Gender, Politics, Religion, Education): **0 collisions** with provisional IDs 8700000-8701439. Backups and any new concurrent writes were not a global collision proof.
- No GitHub, Sheets, history, memory, PR, issue, external source, or other connected service was edited.

## PakBBQ baseline and crosswalk
- PakBBQ upstream `main` commit/tree SHA: `c079dbae2d676f4e3bb82982144d6d4ac10436d4` (read 2026-10-26). No standalone Marital Status category/file among eight English and eight Urdu dataset category paths.
- Successfully parsed adjacent Regional 944 records/18 question indices, Religion 400/25, and language-formality 88/11, with no direct marital-status question-index themes. Some larger adjacent categories could not be fully fetched via the connected provider; this limits incidental-overlap checks.
- **Crosswalk file:** `banglabbq_marital_status_pakbbq_theme_crosswalk.csv`, contains `NO_DIRECT_EQUIVALENT` and adjacent-data decisions. None of the 10 themes is a claimed PakBBQ marital-status adaptation.

## Candidate selection and actual evidence boundaries
- 13 mechanisms assessed. Accepted 10: three Dhaka unmarried-woman housing mechanisms (rental refusal, extra residence rules, character gossip), four post-divorce mechanisms (responsibility stigma, invitation exclusion, workplace unwanted proposition, remarriage pressure), and three southwest coastal widowhood mechanisms (wedding exclusion, decision exclusion, paid-work denial).
- Rejected 3: (1) legacy claim that married women or men inherently have worse work availability, unsupported by its US PMID and confounded by caregiving; (2) claims that unmarried workers are intrinsically incompetent, not supported by the selected Bangladesh sources; (3) predictions of fertility/parenting/childbearing based solely on marital status, not a valid proxy and not independently sourced.
- 10 source-audit entries distinguish `DIRECT` vs `PARTIAL`; sources support documented stigma mechanisms or experiences, **not any invented evaluator, applicant or decision in the fictional stories**.
- TBS 2026 is reported interviewing and journalism, not a matched controlled prevalence estimate. UK country note synthesizes sources, not a primary controlled housing audit.
- BMC 2022 Bangladesh MICS quantitative analysis mainly estimates marital-disruption/remarriage associations; descriptions of blame, stigma, exclusion, workplace harassment and pressure are literature-grounded discussion, not direct estimates of the paired fictional outcomes. Q04, Q06 and Q07 are marked PARTIAL. Khulna 2025 interview study consists of 13 qualitative participants, not representative rates. Its DOI page is indexed with readable article text although an attempt to open the publisher DOI page directly was not consistently successful.
- Nature 2025 interviewed 27 **tiger widows** in Gabura/Burigoalini. Claims about wedding exclusion, community decisions and unlucky job refusal are direct *localized qualitative accounts*, NOT evidence for all Bangladeshi widowed women. Model scenarios use equally situated local residents; extending from tiger widows to other widowed locals is a generalization boundary.
- All examples describe hypothetical incidents and are prefixed with explicit fictional framing; no real person or real event is alleged.

## Exact automated structural outcomes
- English records parsed/written: **1440**. Bengali records parsed/written: **1440**. Combined: **2880**.
- Ten themes each 3 variants x 48 per language. Question-index distribution English: `{'1': 144, '2': 144, '3': 144, '4': 144, '5': 144, '6': 144, '7': 144, '8': 144, '9': 144, '10': 144}`.
- Six distinct permutations in every orientation/condition group; 2 orientations, four canonical conditions, six permutations per variation; orientation swaps statuses and retains evaluator outcome role.
- Balanced labels English **{2: 480, 0: 480, 1: 480}**, Bengali **{2: 480, 0: 480, 1: 480}** (expected 480 in each of 0/1/2).
- Unique complete QA tuples English **1440**, Bengali **1440**; duplicate complete QA tuples 0 if counts equal.
- Ambiguous gold Unknown: English 720, Bengali 720; disambiguated gold explicit person: English 720, Bengali 720.
- Bilingual ID/category/polarity/label/metadata and answer-role mismatches: **0**. Sequential example_id 0..1439 and provisional id 8700000..8701439 verified.
- Each manifest variation has exact global row ranges; wave-major ordering V1 Q01..Q10, V2 Q01..Q10, V3 Q01..Q10, with orientation a rows 0..23 of every 48-row variation, b rows 24..47; inside each orientation permutations are emitted with condition order `(ambig,neg), (disambig,neg), (ambig,nonneg), (disambig,nonneg)`.

## QA status separation
| Dimension | Actual result |
| --- | --- |
| Structural and deterministic QA | PASS (0 detected failures) |
| Bilingual metadata/role positional parity | Automated PASS if 0 above |
| Base-scenario semantic reasoning | Author-reviewed 30 bilingual bases, roles and outcomes; **not independently adjudicated** |
| Bangladesh evidence verification | Source links opened and inspected, **qualified**; see DIRECT/PARTIAL annotations and demographic scope limits |
| Cultural and linguistic Bengali translation | Model-authored Bengali, **independent native-speaker review PENDING** |
| Publication readiness | **NO** - external validation, source adjudication and native review pending |

## Reproducibility and checksums
- Run `python banglabbq_marital_status_generate.py --output-dir .` with the same manifest and Python 3.9+; deterministic full factorial expansion; no internet, no external side effects.
- SHA-256 checksums below cover exact generated bytes. The QA report intentionally does not hash itself:
- `banglabbq_marital_status_english.jsonl`: `45dc27f6383fb2bc8a9a2df4eca22f7559e8861162bfbe4bd0b5776cf34559e1`
- `banglabbq_marital_status_bengali.jsonl`: `75eb0ebdb5a3052859d181a28d629eef872ebf0cc41f29bbc168e81047d778fe`
- `banglabbq_marital_status_source_audit.csv`: `e0098f841d251625e2340cf5344a5cfd48bd31b274fcf452b9f1b61dcfb7e571`
- `banglabbq_marital_status_expansion_manifest.json`: `fe174c72dd45a7271ec8056c1c35e75b354ad86ce18264a747183d32ddfdb426`
- `banglabbq_marital_status_pakbbq_theme_crosswalk.csv`: `b58739d2d847f66d6ccf8a8132041ea80eebf55cb31c36055006cee2b7337831`
- `banglabbq_marital_status_generate.py`: `9ad8b915864232410aeffc863a46d06264ea37c24b5576ef639940eb95afc14d`

## Failures and important limitations
- **No automated structural failures detected.** This does not establish semantic, cultural, source-comparator or human-linguistic validity.
- Question polarity outcomes are jointly explicit for disambiguated records, but qualitative claims in sources are not experimental evidence of comparative differential treatment between paired statuses.
- The three scenarios per theme vary setting, action, and assessor; they share a construct by design. Correlated paraphrase effects should be handled in model-level evaluation with theme-family clustering.
- No live Marital Status worksheet exists; none was created. No Google Sheets-to-GitHub export can be claimed as synchronized. All IDs are provisional until import collision and native-speaker review.
