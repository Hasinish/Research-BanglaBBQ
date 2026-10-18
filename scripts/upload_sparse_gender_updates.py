"""
Upload verified Gender Identity repairs to Google Sheets.
1. English worksheet: Sparse update of 12 answer_info cells (EIDs 0-3, 4424-4427, 4496-4499).
2. Bengali worksheet: Chunked update of all canonical records with immediate readback.
3. Readback parity verification across all 140,880 data cells.
"""

import json
import time
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
ENG_SHEET_NAME = 'BanglaBBQ_ENG_Gender'
BEN_SHEET_NAME = 'BanglaBBQ_BEN_Gender'

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
    print("PHASE 9: UPLOADING VERIFIED GENDER REPAIRS TO MASTER GOOGLE SHEETS")
    print("====================================================================")
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    # 1. Update English answer_info cells
    print("\n[Step 1] Updating 12 answer_info cells in BanglaBBQ_ENG_Gender...")
    with open('BanglaBBQ_Gender/Gender_identity_eng.jsonl', 'r', encoding='utf-8') as f:
        eng_recs = [json.loads(l) for l in f]
        
    eng_target_eids = [0, 1, 2, 3, 4424, 4425, 4426, 4427, 4496, 4497, 4498, 4499]
    eng_data = []
    for eid in eng_target_eids:
        row = eid + 2
        val = json.dumps(eng_recs[eid]['answer_info'], ensure_ascii=False)
        eng_data.append({
            'range': f"{ENG_SHEET_NAME}!L{row}",
            'values': [[val]]
        })
        
    eng_body = {
        'valueInputOption': 'RAW',
        'data': eng_data
    }
    eng_res = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=eng_body
    ).execute()
    print(f"  English batchUpdate successful: {eng_res.get('totalUpdatedCells')} cells updated.")
    
    # Verify English updates via readback
    for eid in eng_target_eids:
        row = eid + 2
        exp = json.dumps(eng_recs[eid]['answer_info'], ensure_ascii=False)
        act_res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{ENG_SHEET_NAME}!L{row}"
        ).execute()
        act = act_res.get('values', [['']])[0][0]
        assert act == exp, f"Readback mismatch at Row {row}: exp {exp}, got {act}"
    print("  English readback verification PASSED for all 12 cells.")
    
    # 2. Update Bengali worksheet
    print(f"\n[Step 2] Uploading canonical Bengali records to {BEN_SHEET_NAME}...")
    with open('BanglaBBQ_Gender/Gender_identity_bng.jsonl', 'r', encoding='utf-8') as f:
        ben_recs = [json.loads(l) for l in f]
        
    all_ben_rows = [HEADER] + [format_row(r) for r in ben_recs]
    chunk_size = 1000
    total_chunks = (len(all_ben_rows) + chunk_size - 1) // chunk_size
    
    for i in range(total_chunks):
        start_idx = i * chunk_size
        end_idx = min(start_idx + chunk_size, len(all_ben_rows))
        chunk_rows = all_ben_rows[start_idx:end_idx]
        
        start_row = start_idx + 1
        end_row = end_idx
        cell_range = f"{BEN_SHEET_NAME}!A{start_row}:O{end_row}"
        
        print(f"  [Chunk {i+1}/{total_chunks}] Writing range {cell_range} ({len(chunk_rows)} rows)...")
        body = {'values': chunk_rows}
        res = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=cell_range,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        # Readback verification
        read_res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=cell_range
        ).execute()
        read_rows = read_res.get('values', [])
        assert len(read_rows) == len(chunk_rows), f"Row count mismatch in chunk {i+1}"
        for r_offset, (w_row, r_row) in enumerate(zip(chunk_rows, read_rows)):
            for c_idx in range(15):
                val_w = w_row[c_idx] if c_idx < len(w_row) else ''
                val_r = r_row[c_idx] if c_idx < len(r_row) else ''
                assert val_w == val_r, f"Mismatch at row {start_row + r_offset}, col {c_idx}"
        time.sleep(0.5)
    print("  Bengali upload and chunk readback verification PASSED.")

    print("\n====================================================================")
    print("ALL PRODUCTION UPDATES WRITTEN AND VERIFIED SUCCESSFULLY!")
    print("====================================================================")

if __name__ == '__main__':
    main()
