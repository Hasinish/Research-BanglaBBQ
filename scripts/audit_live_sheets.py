import json
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SHEETS_MAP = {
    'BanglaBBQ_ENG_Education': 2880,
    'BanglaBBQ_BEN_Education': 2880,
    'BanglaBBQ_ENG_Ethnicity': 1440,
    'BanglaBBQ_BEN_Ethnicity': 1440,
    'BanglaBBQ_ENG_HealthStatus': 2880,
    'BanglaBBQ_BEN_HealthStatus': 2880,
    'BanglaBBQ_ENG_MaritalStatus': 2880,
    'BanglaBBQ_BEN_MaritalStatus': 2880,
    'BanglaBBQ_ENG_OccupationalBackground': 2880,
    'BanglaBBQ_BEN_OccupationalBackground': 2880,
    'BanglaBBQ_ENG_Politics': 2880,
    'BanglaBBQ_BEN_Politics': 2880,
    'BanglaBBQ_ENG_Regional': 1440,
    'BanglaBBQ_BEN_Regional': 1440,
    'BanglaBBQ_ENG_Religion': 2880,
    'BanglaBBQ_BEN_Religion': 2880,
    'BanglaBBQ_ENG_SocialStatus': 1440,
    'BanglaBBQ_BEN_SocialStatus': 1440
}

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

def audit():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    print("Forensic Audit of all 18 Live Google Sheets Grid Properties & Data Bounds...")
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    
    all_ok = True
    sheet_props = {s['properties']['title']: s['properties']['gridProperties'] for s in meta['sheets']}
    
    for title, expected_rows in SHEETS_MAP.items():
        props = sheet_props.get(title)
        if not props:
            print(f"  [FAIL] Missing sheet {title}")
            all_ok = False
            continue
            
        row_count = props.get('rowCount', 0)
        col_count = props.get('columnCount', 0)
        
        # Verify first row and last row
        res = service.spreadsheets().values().batchGet(
            spreadsheetId=SPREADSHEET_ID,
            ranges=[f"'{title}'!A1:O1", f"'{title}'!A{expected_rows + 1}:O{expected_rows + 1}"]
        ).execute()
        
        hdr = res['valueRanges'][0].get('values', [[]])[0]
        last_row = res['valueRanges'][1].get('values', [[]])[0]
        
        grid_ok = (row_count == expected_rows + 1 and col_count == 15)
        hdr_ok = (len(hdr) == 15 and hdr[0] == 'example_id')
        last_ok = (len(last_row) == 15 and int(last_row[0]) == expected_rows - 1)
        
        if grid_ok and hdr_ok and last_ok:
            print(f"  [PASS] {title:<38}: Grid {row_count}x{col_count}, Header intact, Last Row ID={last_row[0]} (row {expected_rows+1}).")
        else:
            print(f"  [FAIL] {title:<38}: Grid {row_count}x{col_count} (expected {expected_rows+1}x15), hdr={hdr_ok}, last={last_ok}")
            all_ok = False
        time.sleep(0.3)

    if all_ok:
        print("\n[CERTIFIED] ZERO ERRORS ACROSS ALL 18 GOOGLE SHEETS! EXACT GRID DIMENSIONS & BOUNDS VERIFIED.")
    else:
        print("\n[ALERT] DISCREPANCIES DETECTED.")
        raise SystemExit(1)

if __name__ == '__main__':
    audit()
