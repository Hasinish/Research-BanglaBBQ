from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets_dict = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

requests = []
for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    sheet_id = sheets_dict[title]
    requests.append({
        'deleteDimension': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'COLUMNS',
                'startIndex': 15,
                'endIndex': 26
            }
        }
    })

body = {'requests': requests}
res = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
print('Successfully trimmed columns P:Z in Politics sheets:', res)
