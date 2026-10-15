from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=['BanglaBBQ_ENG_Politics!A1:O2'],
    fields='sheets.data'
).execute()

data = meta['sheets'][0]['data'][0]
col_meta = data.get('columnMetadata', [])
print("Column widths:")
for idx, cm in enumerate(col_meta[:15]):
    print(f"  Col {idx} ({chr(65+idx)}): {cm.get('pixelSize')}px")

row_data = data.get('rowData', [])
if row_data:
    row1 = row_data[0].get('values', [])
    row2 = row_data[1].get('values', [])
    print("\nRow 1 (Header) cell 0 borders:", row1[0].get('userEnteredFormat', {}).get('borders'))
    print("Row 2 (Data) cell 0 borders:", row2[0].get('userEnteredFormat', {}).get('borders'))
