# BanglaBBQ Mental Health Q11-Q20: Corrected Submission Bundle

**Candidate status: STRUCTURALLY VERIFIED, AWAITING CLINICAL AND INDEPENDENT NATIVE-BENGALI REVIEW.**
This package is not represented as 100% scientifically proven or publication-ready.

## The two JSONL files
- `BanglaBBQ_Health_Mental_Q11_Q20_english.jsonl`: 1,440 UTF-8 JSON objects.
- `BanglaBBQ_Health_Mental_Q11_Q20_bengali.jsonl`: 1,440 structurally and semantically aligned UTF-8 JSON objects.

**Append only:** use the existing `Health_status` category; add `example_id` 1440–2879 and `id` 8301440–8302879. Q01–Q10 (0–1439) must stay unchanged. The expected size after an authorized append is 2,880 rows **per language**.

**Live spreadsheet read-only verified:** `BanglaBBQ_ENG_HealthStatus` and `BanglaBBQ_BEN_HealthStatus` have 1,440 populated rows plus header. Import starts at sheet row **1442**, after backing up and expanding the grid. Do not write until authorized.

**CRITICAL:** Google Sheets A:O column order differs from JSONL object order. See the import manifest. Serialize `answer_info` and `additional_metadata` JSON to cells using UTF-8.

## Quality
- Deterministic structural validator PASS (including 6/6 tampered fixtures rejected).
- A **separately implemented text-based gold inferencer** parsed all 720 disambiguated cases *per language* from actual rendered outcome clauses and found zero gold conflicts.
- 30 distinct bilingual authored scenario families, 240 paired semantic cases, 6-way options, exact 6/6 protected/comparator and first/second introduction balance within every variation.
- NFC-normalized Bengali text and corrected English/Bengali editorial mismatches.
- Sources: five real Bangladesh mental-health research publications. **Nine themes have only CONTEXTUAL evidence; Q19 has DIRECT evidence of general professional help-seeking stigma, not of a specific fictional decision.**

## Important limits
1. No independent psychiatrist/clinical psychologist certification.
2. No independent native Bengali human review.
3. Original Q01–Q10 Health Status remains first-name-position biased (360/360 negative disambiguated cases); append alone leaves combined category 540/720 (75%) negative gold answers selecting the first-mentioned person.
4. All examples are fictional and test possible prejudice; they do not report real discrimination incidents.
5. This package makes NO Google Sheets writes and NO GitHub pushes.

## How to verify
```
python health_mental_validation.py --negative-tests
python health_mental_independent_audit.py
python health_mental_generate.py
python health_mental_validation.py
```
Read `health_mental_QA_report.md` and `health_mental_import_manifest.json` before import.
