# -*- coding: utf-8 -*-
"""Sparse Production Patch and Diff Manifest Generator for BanglaBBQ Educational Background.

This script:
  1. Reads live data from Google Sheets (BanglaBBQ_ENG_Education and BanglaBBQ_BEN_Education).
  2. Compares every live cell against the canonical repaired JSONL files.
  3. Records an exact before/after diff manifest (qa_repair_diff_manifest.json).
  4. Applies sparse batch updates ONLY to modified cells (predominantly Col F, G, M).
  5. Performs 100% full-sheet readback verification across all 86,400 data cells.
"""
import json
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

ENG_JSONL = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_english.jsonl"
BEN_JSONL = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_bengali.jsonl"
MANIFEST_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "qa_repair_diff_manifest.json"

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]
COL_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

def get_service():
    creds = Credentials.from_authorized_user_file('token.json')
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open('token.json', 'w', encoding='utf-8') as f:
            f.write(creds.to_json())
    return build('sheets', 'v4', credentials=creds)

def load_canonical_rows(jsonl_path):
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

def sync_sheet_sparse(service, sheet_title, canonical_rows):
    print(f"\n====================================================================")
    print(f"ANALYZING AND PATCHING: {sheet_title}")
    print(f"====================================================================")
    res = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_title}!A1:O2881"
    ).execute()
    live_rows = res.get('values', [])
    
    assert len(live_rows) == 2881, f"Expected 2881 rows, got {len(live_rows)}"
    
    diff_entries = []
    update_data = []
    
    for r_idx in range(1, 2881):
        live_r = live_rows[r_idx]
        exp_r = canonical_rows[r_idx]
        
        for c_idx in range(15):
            val_live = live_r[c_idx] if c_idx < len(live_r) else ""
            val_exp = exp_r[c_idx]
            
            is_diff = False
            if c_idx in (11, 12):
                try:
                    if json.loads(val_live) != json.loads(val_exp):
                        is_diff = True
                except Exception:
                    if val_live != val_exp:
                        is_diff = True
            else:
                if val_live != val_exp:
                    is_diff = True
                    
            if is_diff:
                cell_a1 = f"{sheet_title}!{COL_LETTERS[c_idx]}{r_idx + 1}"
                diff_entries.append({
                    "sheet": sheet_title,
                    "example_id": r_idx - 1,
                    "row": r_idx + 1,
                    "col": COL_LETTERS[c_idx],
                    "column_name": HEADER[c_idx],
                    "old_value": val_live,
                    "new_value": val_exp
                })
                update_data.append({
                    "range": cell_a1,
                    "values": [[val_exp]]
                })
                
    print(f"  Identified {len(diff_entries)} cells requiring repair in {sheet_title}.")
    
    if update_data:
        print(f"  Executing sparse batch update in chunks of 500 cells...")
        chunk_size = 500
        for i in range(0, len(update_data), chunk_size):
            chunk = update_data[i:i + chunk_size]
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": chunk
            }
            service.spreadsheets().values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            print(f"    Written cells {i + 1} to {min(i + chunk_size, len(update_data))}...")
            time.sleep(0.5)
        print(f"  Successfully applied {len(update_data)} sparse cell updates to {sheet_title}!")
    else:
        print(f"  {sheet_title} is already in 100% parity with canonical JSONL. No writes needed.")
        
    return diff_entries

def main():
    service = get_service()
    
    eng_canonical = load_canonical_rows(ENG_JSONL)
    ben_canonical = load_canonical_rows(BEN_JSONL)
    
    eng_diffs = sync_sheet_sparse(service, "BanglaBBQ_ENG_Education", eng_canonical)
    ben_diffs = sync_sheet_sparse(service, "BanglaBBQ_BEN_Education", ben_canonical)
    
    full_manifest = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_english_cells_changed": len(eng_diffs),
        "total_bengali_cells_changed": len(ben_diffs),
        "total_cells_changed": len(eng_diffs) + len(ben_diffs),
        "diff_records": eng_diffs + ben_diffs
    }
    
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(full_manifest, f, indent=2, ensure_ascii=False)
    print(f"\nWrote full sparse diff manifest to: {MANIFEST_PATH}")
    
    # Verify Live Parity bit-for-bit
    print("\n====================================================================")
    print("EXECUTING MANDATORY 100% CELL-BY-CELL LIVE READBACK VERIFICATION")
    print("====================================================================")
    from verify_education_live_parity import check_sheet
    ok_eng = check_sheet(service, "BanglaBBQ_ENG_Education", eng_canonical)
    ok_ben = check_sheet(service, "BanglaBBQ_BEN_Education", ben_canonical)
    
    if ok_eng and ok_ben:
        print("\nSUCCESS: 100% LIVE PARITY VERIFIED ACROSS ALL 86,400 DATA CELLS (0 MISMATCHES).")
        return 0
    else:
        print("\nERROR: Parity check failed after sparse write!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
