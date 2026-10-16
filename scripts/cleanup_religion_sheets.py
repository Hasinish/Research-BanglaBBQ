import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

EXPECTED_PRE_SHEETS = {
    'BanglaBBQ_ENG_Religion_Phase1': 957775741,
    'BanglaBBQ_BEN_Religion_Phase1': 912459319,
    'BanglaBBQ_ENG_Religion_Phase2': 804112545,
    'BanglaBBQ_BEN_Religion_Phase2': 860941009,
    'Review_Age_20_Templates': 99887766,
    'PakBBQ_ENG_Age': 0,
    'BanglaBBQ_BEN_Age': 1006819770,
    'BanglaBBQ_ENG_Politics': 1888499205,
    'BanglaBBQ_BEN_Politics': 2128232344,
}

EXPECTED_POST_TITLES = [
    'Review_Age_20_Templates',
    'PakBBQ_ENG_Age',
    'BanglaBBQ_BEN_Age',
    'BanglaBBQ_ENG_Politics',
    'BanglaBBQ_BEN_Politics',
    'BanglaBBQ_ENG_Religion',
    'BanglaBBQ_BEN_Religion',
]

def main():
    print("====================================================================")
    print("STEP 3: GOOGLE SHEETS CLEANUP & PHASE 2 RENAMING")
    print("====================================================================")

    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    # 1. Pre-flight verification
    print("\n[1/4] Running pre-flight check on current Google Sheets...")
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

    for title, expected_id in EXPECTED_PRE_SHEETS.items():
        assert title in sheet_map, f"Missing sheet: {title}"
        assert sheet_map[title] == expected_id, f"ID mismatch for {title}: expected {expected_id}, got {sheet_map[title]}"
    print(f"  ✓ Confirmed all {len(sheet_map)} sheets present with exact matching IDs.")

    # 2. Build batchUpdate requests
    print("\n[2/4] Executing atomic rename and delete batchUpdate...")
    requests = [
        # Rename Phase 2 ENG to BanglaBBQ_ENG_Religion
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 804112545,
                    'title': 'BanglaBBQ_ENG_Religion'
                },
                'fields': 'title'
            }
        },
        # Rename Phase 2 BEN to BanglaBBQ_BEN_Religion
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 860941009,
                    'title': 'BanglaBBQ_BEN_Religion'
                },
                'fields': 'title'
            }
        },
        # Delete Phase 1 ENG
        {
            'deleteSheet': {
                'sheetId': 957775741
            }
        },
        # Delete Phase 1 BEN
        {
            'deleteSheet': {
                'sheetId': 912459319
            }
        }
    ]

    body = {'requests': requests}
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()
    print("  ✓ batchUpdate executed successfully!")

    # 3. Post-flight verification of sheet structure
    print("\n[3/4] Running post-flight check on Google Sheets metadata...")
    meta_post = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    post_sheets = meta_post['sheets']
    post_titles = [s['properties']['title'] for s in post_sheets]
    post_map = {s['properties']['title']: s['properties']['sheetId'] for s in post_sheets}

    print(f"  Total sheets remaining: {len(post_titles)}")
    for s in post_sheets:
        p = s['properties']
        print(f"    - Index {p['index']}: ID {p['sheetId']} | '{p['title']}'")

    assert len(post_titles) == 7, f"Expected exactly 7 sheets, got {len(post_titles)}: {post_titles}"
    assert 'BanglaBBQ_ENG_Religion_Phase1' not in post_titles, "Phase 1 ENG sheet still exists!"
    assert 'BanglaBBQ_BEN_Religion_Phase1' not in post_titles, "Phase 1 BEN sheet still exists!"
    assert 'BanglaBBQ_ENG_Religion' in post_titles, "BanglaBBQ_ENG_Religion not found!"
    assert 'BanglaBBQ_BEN_Religion' in post_titles, "BanglaBBQ_BEN_Religion not found!"
    assert post_map['BanglaBBQ_ENG_Religion'] == 804112545, "ENG Religion sheet ID changed!"
    assert post_map['BanglaBBQ_BEN_Religion'] == 860941009, "BEN Religion sheet ID changed!"
    print("  ✓ Sheet metadata and IDs verified 100%!")

    # 4. Verify data preservation
    print("\n[4/4] Verifying data preservation in renamed Religion sheets...")
    eng_rows = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='BanglaBBQ_ENG_Religion!A1:O1000'
    ).execute().get('values', [])

    ben_rows = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='BanglaBBQ_BEN_Religion!A1:O1000'
    ).execute().get('values', [])

    print(f"  BanglaBBQ_ENG_Religion: {len(eng_rows)} rows (including header)")
    print(f"  BanglaBBQ_BEN_Religion: {len(ben_rows)} rows (including header)")

    assert len(eng_rows) == 961, f"Expected 961 ENG rows, got {len(eng_rows)}"
    assert len(ben_rows) == 961, f"Expected 961 BEN rows, got {len(ben_rows)}"
    print("  ✓ Exactly 960 data records preserved in each Religion worksheet!")

    print("\nSUCCESS: Google Sheets cleanup and renaming completed cleanly.")

if __name__ == '__main__':
    main()
