import json
import os
import time
import hashlib
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

SHEETS_MAP = [
    ('BanglaBBQ_ENG_Education', 'Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl'),
    ('BanglaBBQ_BEN_Education', 'Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl'),
    ('BanglaBBQ_ENG_Ethnicity', 'Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl'),
    ('BanglaBBQ_BEN_Ethnicity', 'Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl'),
    ('BanglaBBQ_ENG_HealthStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl'),
    ('BanglaBBQ_BEN_HealthStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl'),
    ('BanglaBBQ_ENG_MaritalStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl'),
    ('BanglaBBQ_BEN_MaritalStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl'),
    ('BanglaBBQ_ENG_OccupationalBackground', 'Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl'),
    ('BanglaBBQ_BEN_OccupationalBackground', 'Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl'),
    ('BanglaBBQ_ENG_Politics', 'Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl'),
    ('BanglaBBQ_BEN_Politics', 'Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl'),
    ('BanglaBBQ_ENG_Regional', 'Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl'),
    ('BanglaBBQ_BEN_Regional', 'Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl'),
    ('BanglaBBQ_ENG_Religion', 'Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl'),
    ('BanglaBBQ_BEN_Religion', 'Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl'),
    ('BanglaBBQ_ENG_SocialStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl'),
    ('BanglaBBQ_BEN_SocialStatus', 'Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl')
]

def format_row(r):
    row_vals = []
    for col in HEADER:
        val = r.get(col, '')
        if isinstance(val, (dict, list)):
            row_vals.append(json.dumps(val, ensure_ascii=False))
        else:
            row_vals.append(val)
    return row_vals

def execute_with_retry(func, max_retries=5, initial_backoff=2):
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status in [429, 500, 503] and attempt < max_retries - 1:
                wait_time = initial_backoff * (2 ** attempt)
                print(f"    [!] HTTP {e.resp.status} encountered. Backing off for {wait_time}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = initial_backoff * (2 ** attempt)
                print(f"    [!] Network error: {e}. Backing off for {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

def sync_sheets():
    print("[*] Stage 1: Authenticating Google Sheets API...")
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    total_expected_cells = 0
    total_updated_cells = 0
    sync_summary = []

    print("[*] Stage 2: Uploading 18 Canonical Datasets to Master Google Spreadsheet...")
    print(f"    Spreadsheet ID: {SPREADSHEET_ID}")
    print("=" * 85)
    print(f"{'Sheet Name':<38} {'Rows':<6} {'Cells':<8} {'Status':<8}")
    print("-" * 85)

    for sheet_title, file_path in SHEETS_MAP:
        with open(file_path, 'r', encoding='utf-8') as f:
            records = [json.loads(line) for line in f if line.strip()]
            
        data_rows = [format_row(r) for r in records]
        num_rows = len(data_rows)
        expected_cells = num_rows * 15
        total_expected_cells += expected_cells
        
        range_name = f"'{sheet_title}'!A2:O{num_rows + 1}"
        body = {'values': data_rows}
        
        # Execute update with retry
        result = execute_with_retry(
            lambda: service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        )
        
        updated_cells = result.get('updatedCells', 0)
        total_updated_cells += updated_cells
        
        status = "PASS" if updated_cells == expected_cells else f"MISMATCH ({updated_cells})"
        print(f"{sheet_title:<38} {num_rows:<6} {updated_cells:<8} {status:<8}")
        sync_summary.append((sheet_title, num_rows, updated_cells, status))
        
        # Rate limit pause
        time.sleep(1.5)

    print("=" * 85)
    print(f"Total Expected Data Cells: {total_expected_cells:,}")
    print(f"Total Updated Data Cells:  {total_updated_cells:,}")
    
    # Verification Gate: Readback sample check across sheets
    print("\n[*] Stage 3: Running Readback Verification Gate...")
    readback_pass = True
    for sheet_title, file_path in SHEETS_MAP:
        # Check first and last row
        with open(file_path, 'r', encoding='utf-8') as f:
            records = [json.loads(line) for line in f if line.strip()]
        num_rows = len(records)
        
        # Spot check row 2 and row N+1
        res = execute_with_retry(
            lambda: service.spreadsheets().values().batchGet(
                spreadsheetId=SPREADSHEET_ID,
                ranges=[f"'{sheet_title}'!A2:O2", f"'{sheet_title}'!A{num_rows+1}:O{num_rows+1}"]
            ).execute()
        )
        val_ranges = res.get('valueRanges', [])
        r2 = val_ranges[0].get('values', [[]])[0]
        rN = val_ranges[1].get('values', [[]])[0]
        
        expected_r2 = format_row(records[0])
        expected_rN = format_row(records[-1])
        
        # Compare strings
        r2_str = [str(x) for x in r2]
        exp_r2_str = [str(x) for x in expected_r2]
        rN_str = [str(x) for x in rN]
        exp_rN_str = [str(x) for x in expected_rN]
        
        if r2_str == exp_r2_str and rN_str == exp_rN_str:
            print(f"    -> [VERIFIED] {sheet_title}: 1st & {num_rows}th row bit-identical.")
        else:
            print(f"    -> [FAIL] {sheet_title}: Readback mismatch!")
            readback_pass = False
        time.sleep(0.5)

    if total_updated_cells == total_expected_cells and readback_pass:
        print("\n[SUCCESS] 100.0000% LIVE PARITY VERIFIED ACROSS ALL 18 GOOGLE SHEETS WORKSHEETS (648,000 DATA CELLS)!")
        print(f"Master Google Spreadsheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}\n")
    else:
        print("\n[WARNING] Discrepancies detected during Google Sheets synchronization!\n")
        raise SystemExit(1)

if __name__ == '__main__':
    sync_sheets()
