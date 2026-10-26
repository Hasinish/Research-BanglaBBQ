"""
Upload canonical Bengali Gender Identity dataset to Google Sheets BanglaBBQ_BEN_Gender.
Performs chunked, idempotent writes with immediate readback verification.
Target sheet: BanglaBBQ_BEN_Gender (Sheet ID: 1990010102)
Total rows: 1 header row + 4,696 data rows = 4,697 rows (A1:O4697).
"""

import json
import time
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
BEN_JSONL_PATH = 'Dataset_BanglaBBQ_New/BanglaBBQ_Gender/Gender_identity_bng.jsonl' if os.path.exists('Dataset_BanglaBBQ_New/BanglaBBQ_Gender/Gender_identity_bng.jsonl') else 'BanglaBBQ_Gender/Gender_identity_bng.jsonl'
SHEET_NAME = 'BanglaBBQ_BEN_Gender'

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity', 'type',
    'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

def format_row(r):
    return [
        str(r['example_id']),
        str(r['question_index']),
        str(r['context_condition']),
        str(r['question_polarity']),
        str(r['type']),
        str(r['context']),
        str(r['question']),
        str(r['ans0']),
        str(r['ans1']),
        str(r['ans2']),
        str(r['label']),
        json.dumps(r['answer_info'], ensure_ascii=False),
        json.dumps(r['additional_metadata'], ensure_ascii=False),
        str(r['category']),
        str(r['id'])
    ]

def main():
    print("====================================================================")
    print("STEP 1: UPLOADING BANGLABBO_BEN_GENDER TO MASTER GOOGLE SPREADSHEET")
    print("====================================================================")
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    # Load canonical records
    with open(BEN_JSONL_PATH, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f]
    print(f"Loaded {len(records)} Bengali records from {BEN_JSONL_PATH}")
    
    all_rows = [HEADER] + [format_row(r) for r in records]
    print(f"Total rows to upload (including header): {len(all_rows)}")
    
    # Chunked upload: 1000 rows per chunk
    chunk_size = 1000
    total_chunks = (len(all_rows) + chunk_size - 1) // chunk_size
    
    for i in range(total_chunks):
        start_idx = i * chunk_size
        end_idx = min(start_idx + chunk_size, len(all_rows))
        chunk_rows = all_rows[start_idx:end_idx]
        
        start_row = start_idx + 1
        end_row = end_idx
        cell_range = f"{SHEET_NAME}!A{start_row}:O{end_row}"
        
        print(f"\n[Chunk {i+1}/{total_chunks}] Writing range {cell_range} ({len(chunk_rows)} rows)...")
        body = {'values': chunk_rows}
        
        # Write
        res = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=cell_range,
            valueInputOption='RAW',
            body=body
        ).execute()
        updated_cells = res.get('updatedCells', 0)
        print(f"  API update response: {updated_cells} cells updated.")
        
        # Immediate readback verification
        read_res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=cell_range
        ).execute()
        read_rows = read_res.get('values', [])
        assert len(read_rows) == len(chunk_rows), f"Readback row count mismatch: wrote {len(chunk_rows)}, read {len(read_rows)}"
        for r_idx, (w_row, r_row) in enumerate(zip(chunk_rows, read_rows)):
            for c_idx in range(15):
                val_w = w_row[c_idx] if c_idx < len(w_row) else ''
                val_r = r_row[c_idx] if c_idx < len(r_row) else ''
                assert val_w == val_r, f"Mismatch at row {start_row + r_idx}, col {c_idx}: wrote '{val_w[:30]}...', read '{val_r[:30]}...'"
        print(f"  Chunk {i+1} readback verification PASSED (100% match across {len(chunk_rows)*15} cells).")
        time.sleep(1)
        
    print("\n====================================================================")
    print("ALL 4,697 ROWS SUCCESSFULLY UPLOADED & VERIFIED IN BanglaBBQ_BEN_Gender!")
    print("====================================================================")

if __name__ == '__main__':
    main()
