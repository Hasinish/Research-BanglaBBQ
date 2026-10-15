from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

# Get sheet metadata with gridProperties, conditionalFormats
meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets(properties,conditionalFormats,data.rowMetadata,data.columnMetadata)'
).execute()

sheet_map = {s['properties']['title']: s for s in meta['sheets']}

for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    s = sheet_map[title]
    props = s['properties']
    print(f"=== {title} ===")
    print("Sheet ID:", props['sheetId'])
    print("Grid Properties:", props.get('gridProperties', {}))
    print("Conditional formats count:", len(s.get('conditionalFormats', [])))
    for idx, cf in enumerate(s.get('conditionalFormats', [])):
        print(f"  CF {idx}:", cf)

# Now let's fetch cell formatting for Row 1 (header), Row 2 (sample early data row), and Row 170 (sample later data row)
fmt_res = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=['BanglaBBQ_ENG_Politics!A1:O3', 'BanglaBBQ_ENG_Politics!A170:O171'],
    fields='sheets.data.rowData.values.userEnteredFormat,sheets.data.rowData.values.effectiveFormat'
).execute()

print("\n--- CELL FORMATTING SAMPLES (ENG) ---")
sheet_data = fmt_res['sheets'][0]['data']

# Header format
header_cell = sheet_data[0]['rowData'][0]['values'][0]
print("Header cell userEnteredFormat:", json.dumps(header_cell.get('userEnteredFormat', {}), indent=2))

# Row 2 (early row)
row2_cell = sheet_data[0]['rowData'][1]['values'][0]
print("Row 2 cell userEnteredFormat:", json.dumps(row2_cell.get('userEnteredFormat', {}), indent=2))

# Row 170 (later row)
row170_cell = sheet_data[1]['rowData'][0]['values'][0]
print("Row 170 cell userEnteredFormat:", json.dumps(row170_cell.get('userEnteredFormat', {}), indent=2))
