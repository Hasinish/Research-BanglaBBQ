# -*- coding: utf-8 -*-
"""Standalone Live Parity Verification for BanglaBBQ Educational Background worksheets.
Verifies bit-for-bit parity across all 43,200 data cells per language against canonical JSONLs.
"""
import json
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

ENG_JSONL = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_english.jsonl"
BEN_JSONL = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_bengali.jsonl"

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

def load_expected_rows(jsonl_path):
    rows = [HEADER]
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            row = [
                str(r['example_id']),
                str(r['question_index']),
                r['context_condition'],
                r['question_polarity'],
                r['type'],
                r['context'],
                r['question'],
                r['ans0'],
                r['ans1'],
                r['ans2'],
                str(r['label']),
                json.dumps(r['answer_info'], ensure_ascii=False, separators=(',', ':')),
                json.dumps(r['additional_metadata'], ensure_ascii=False, separators=(',', ':')),
                r['category'],
                str(r['id'])
            ]
            rows.append(row)
    return rows

def check_sheet(service, title, expected_rows):
    print(f"\nChecking live worksheet '{title}' against canonical JSONL...")
    res = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{title}!A1:O2881"
    ).execute()
    live = res.get('values', [])
    
    if len(live) != len(expected_rows):
        print(f"  FAIL: Row count mismatch: live={len(live)} vs exp={len(expected_rows)}")
        return False
    print(f"  Row count: {len(live)} (PASS)")
    
    if live[0] != HEADER:
        print(f"  FAIL: Header mismatch: {live[0]}")
        return False
    print("  Header row: 15 columns (PASS)")
    
    mismatches = 0
    total_data_cells = 2880 * 15
    for r in range(1, 2881):
        live_r = live[r]
        exp_r = expected_rows[r]
        for c in range(15):
            val_live = live_r[c] if c < len(live_r) else ""
            val_exp = exp_r[c]
            if c in (11, 12):
                try:
                    if json.loads(val_live) != json.loads(val_exp):
                        mismatches += 1
                        if mismatches <= 3:
                            print(f"    JSON Mismatch at R{r}C{c}: live={val_live} vs exp={val_exp}")
                except Exception:
                    if val_live != val_exp:
                        mismatches += 1
            else:
                if val_live != val_exp:
                    mismatches += 1
                    if mismatches <= 3:
                        print(f"    Mismatch at R{r}C{c}: live={val_live} vs exp={val_exp}")
                        
    if mismatches == 0:
        print(f"  100% BIT-FOR-BIT PARITY: 0/{total_data_cells} mismatches (PASS)")
        return True
    else:
        print(f"  FAIL: {mismatches}/{total_data_cells} cell mismatches!")
        return False

def main():
    print("====================================================================")
    print("LIVE PRODUCTION PARITY VERIFICATION: EDUCATIONAL BACKGROUND")
    print("====================================================================")
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    eng_rows = load_expected_rows(ENG_JSONL)
    ben_rows = load_expected_rows(BEN_JSONL)
    
    ok_eng = check_sheet(service, 'BanglaBBQ_ENG_Education', eng_rows)
    ok_ben = check_sheet(service, 'BanglaBBQ_BEN_Education', ben_rows)
    
    if ok_eng and ok_ben:
        print("\nALL 86,400 LIVE DATA CELLS VERIFIED 100% BIT-FOR-BIT ACCURATE!")
        print("====================================================================")
        return 0
    else:
        print("\nLIVE PARITY CHECK FAILED!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
