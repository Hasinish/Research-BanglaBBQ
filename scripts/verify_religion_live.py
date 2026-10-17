import os
import sys
import json
import hashlib
from collections import Counter
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
ACTIVE_ENG_JSONL = 'BanglaBBQ_Religion/Religion_eng.jsonl'
ACTIVE_BEN_JSONL = 'BanglaBBQ_Religion/Religion_bng.jsonl'

def row_to_rec(row):
    return {
        'example_id': int(row[0]),
        'question_index': int(row[1]),
        'context_condition': str(row[2]),
        'question_polarity': str(row[3]),
        'type': str(row[4]),
        'context': str(row[5]),
        'question': str(row[6]),
        'ans0': str(row[7]),
        'ans1': str(row[8]),
        'ans2': str(row[9]),
        'label': int(row[10]),
        'answer_info': json.loads(row[11]),
        'additional_metadata': json.loads(row[12]),
        'category': str(row[13]),
        'id': int(row[14])
    }

def main():
    print("====================================================================")
    print("STEP 4: INDEPENDENT VERIFICATION OF LIVE SHEETS & GITHUB ARTIFACTS")
    print("====================================================================")

    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    # 1. Check all live sheet titles and IDs
    print("\n[Check 1: Sheet Titles & IDs]")
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = meta['sheets']
    sheet_titles = [s['properties']['title'] for s in sheets]
    sheet_ids = {s['properties']['title']: s['properties']['sheetId'] for s in sheets}
    print(f"Total live sheets: {len(sheets)}")
    for s in sheets:
        p = s['properties']
        print(f"  - Sheet ID: {p['sheetId']} | '{p['title']}' | Index: {p['index']}")

    expected_sheets = {
        'Review_Age_20_Templates': 99887766,
        'PakBBQ_ENG_Age': 0,
        'BanglaBBQ_BEN_Age': 1006819770,
        'BanglaBBQ_ENG_Politics': 1888499205,
        'BanglaBBQ_BEN_Politics': 2128232344,
        'BanglaBBQ_ENG_Religion': 804112545,
        'BanglaBBQ_BEN_Religion': 860941009,
    }
    for t, sid in expected_sheets.items():
        assert t in sheet_ids, f"Missing sheet: {t}"
        assert sheet_ids[t] == sid, f"Mismatch ID for {t}: expected {sid}, got {sheet_ids[t]}"
    assert 'BanglaBBQ_ENG_Religion_Phase1' not in sheet_ids
    assert 'BanglaBBQ_BEN_Religion_Phase1' not in sheet_ids
    print("  ✓ All required core benchmark sheets match expected titles and IDs perfectly.")

    # 2. Check Non-Religion Sheets (Age and Politics) are unchanged
    print("\n[Check 2: Non-Religion Worksheets Data Preservation]")
    age_eng = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='PakBBQ_ENG_Age!A1:A3000').execute().get('values', [])
    age_ben = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='BanglaBBQ_BEN_Age!A1:A3000').execute().get('values', [])
    pol_eng = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='BanglaBBQ_ENG_Politics!A1:A3000').execute().get('values', [])
    pol_ben = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='BanglaBBQ_BEN_Politics!A1:A3000').execute().get('values', [])

    print(f"  PakBBQ_ENG_Age rows: {len(age_eng)} (Expected 2921)")
    print(f"  BanglaBBQ_BEN_Age rows: {len(age_ben)} (Expected 2921)")
    print(f"  BanglaBBQ_ENG_Politics rows: {len(pol_eng)} (Expected 2881)")
    print(f"  BanglaBBQ_BEN_Politics rows: {len(pol_ben)} (Expected 2881)")

    assert len(age_eng) == 2921, f"PakBBQ_ENG_Age row count changed: {len(age_eng)}"
    assert len(age_ben) == 2921, f"BanglaBBQ_BEN_Age row count changed: {len(age_ben)}"
    assert len(pol_eng) == 2881, f"BanglaBBQ_ENG_Politics row count changed: {len(pol_eng)}"
    assert len(pol_ben) == 2881, f"BanglaBBQ_BEN_Politics row count changed: {len(pol_ben)}"
    print("  ✓ Age and Politics worksheet row counts unchanged (content not audited here).")

    # 3. Fetch Live Religion sheets data
    print("\n[Check 3: Fetch Live Religion Sheets Data]")
    rel_eng_data = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='BanglaBBQ_ENG_Religion!A1:O3000').execute().get('values', [])
    rel_ben_data = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='BanglaBBQ_BEN_Religion!A1:O3000').execute().get('values', [])

    n = len(rel_eng_data) - 1
    assert n in (960, 2880), f"Unexpected English Religion count: {n}"
    assert len(rel_ben_data) == n + 1, f"Unequal Bengali Religion count: {len(rel_ben_data)-1}"
    print(f"  BanglaBBQ_ENG_Religion: {n} data records")
    print(f"  BanglaBBQ_BEN_Religion: {n} data records")

    sheet_recs_eng = [row_to_rec(r) for r in rel_eng_data[1:]]
    sheet_recs_ben = [row_to_rec(r) for r in rel_ben_data[1:]]

    # 4. Compare Live Sheets vs GitHub Religion JSONL files
    print("\n[Check 4: Exact Agreement between GitHub JSONL and Live Sheets]")
    with open(ACTIVE_ENG_JSONL, 'r', encoding='utf-8') as f:
        file_recs_eng = [json.loads(line) for line in f]
    with open(ACTIVE_BEN_JSONL, 'r', encoding='utf-8') as f:
        file_recs_ben = [json.loads(line) for line in f]

    assert len(file_recs_eng) == n
    assert len(file_recs_ben) == n

    eng_diffs = []
    ben_diffs = []
    for i in range(n):
        if sheet_recs_eng[i] != file_recs_eng[i]:
            eng_diffs.append((i, sheet_recs_eng[i], file_recs_eng[i]))
        if sheet_recs_ben[i] != file_recs_ben[i]:
            ben_diffs.append((i, sheet_recs_ben[i], file_recs_ben[i]))

    assert len(eng_diffs) == 0, f"Found {len(eng_diffs)} differences in ENG JSONL vs Sheets"
    assert len(ben_diffs) == 0, f"Found {len(ben_diffs)} differences in BEN JSONL vs Sheets"
    print(f"  ✓ Full semantic cell equality across {n * 15} fields/language (not a byte-for-byte encoding check).")

    # 5. Check 20 themes x 48 records
    print(f"\n[Check 5: Theme Distribution (20 Themes x {n//20} Records)]")
    eng_themes = Counter(r['question_index'] for r in sheet_recs_eng)
    ben_themes = Counter(r['question_index'] for r in sheet_recs_ben)
    for q in range(1, 21):
        assert eng_themes[q] == n//20, f"ENG theme {q} has {eng_themes[q]} records"
        assert ben_themes[q] == n//20, f"BEN theme {q} has {ben_themes[q]} records"
    print(f"  ✓ Exactly 20 themes with {n//20} records each in both languages.")

    # 6. Check IDs 0-959, unique and sequential
    print(f"\n[Check 6: Unique & Sequential IDs 0-{n-1}]")
    for i in range(n):
        assert sheet_recs_eng[i]['example_id'] == i
        assert sheet_recs_eng[i]['id'] == i
        assert sheet_recs_ben[i]['example_id'] == i
        assert sheet_recs_ben[i]['id'] == i
    print(f"  ✓ IDs 0-{n-1} are sequential and unique across both sheets.")

    # 7. Check valid gold labels & JSON metadata
    print("\n[Check 7: Valid Gold Labels & JSON Metadata]")
    eng_labels = Counter(r['label'] for r in sheet_recs_eng)
    ben_labels = Counter(r['label'] for r in sheet_recs_ben)
    assert eng_labels == Counter({0: n//3, 1: n//3, 2: n//3})
    assert ben_labels == Counter({0: n//3, 1: n//3, 2: n//3})
    print(f"  ✓ Label distribution: {eng_labels} (uniform {n//3} per gold label)")

    # 8. Six answer permutations per counterfactual orientation
    print("\n[Check 8: Six Answer Permutations Per Counterfactual Orientation]")
    for q in range(1, 21):
        q_recs = [r for r in sheet_recs_eng if r['question_index'] == q]
        versions = {(r['additional_metadata'].get('wording_variant', 'v1'),
                     r['additional_metadata'].get('version')) for r in q_recs}
        for word_variant, v in versions:
            v_recs = [r for r in q_recs if
                      r['additional_metadata'].get('wording_variant', 'v1') == word_variant and
                      r['additional_metadata'].get('version') == v]
            for cond in ['ambig', 'disambig']:
                for pol in ['neg', 'nonneg']:
                    sub = [r for r in v_recs if r['context_condition'] == cond and r['question_polarity'] == pol]
                    assert len(sub) == 6
                    perms = set((r['ans0'], r['ans1'], r['ans2']) for r in sub)
                    assert len(perms) == 6
    print("  ✓ Full 6-way answer permutations (3!) verified across all counterfactual blocks.")

    # 9. English-Bengali structural alignment
    print("\n[Check 9: English-Bengali Structural Alignment]")
    shared_keys = ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type', 'label', 'answer_info', 'additional_metadata', 'category', 'id']
    for i in range(n):
        e = sheet_recs_eng[i]
        b = sheet_recs_ben[i]
        for k in shared_keys:
            assert e[k] == b[k], f"Row {i} mismatch on {k}: {e[k]} != {b[k]}"
    print("  ✓ 100% bilingual structural alignment verified across all shared fields.")

    # 10. Check unintended duplicate records
    print("\n[Check 10: Duplicate QA Records Check]")
    eng_qa = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in sheet_recs_eng]
    ben_qa = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in sheet_recs_ben]
    assert len(eng_qa) == len(set(eng_qa)), "ENG contains duplicate QA records!"
    assert len(ben_qa) == len(set(ben_qa)), "BEN contains duplicate QA records!"
    print(f"  ✓ Exactly 0 unintended duplicate QA records ({n} distinct per language).")

    print("\n====================================================================")
    print("ALL LIVE/JSONL STRUCTURAL PARITY CHECKS PASSED (SEMANTIC/SOURCE REVIEW REMAINS OPEN)")
    print("====================================================================")

if __name__ == '__main__':
    main()
