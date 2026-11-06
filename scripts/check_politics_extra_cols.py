from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

for t in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    res = service.spreadsheets().values().get(
        spreadsheetId='1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY',
        range=f"'{t}'!P1:Z2881"
    ).execute()
    vals = res.get('values', [])
    print(t, 'P:Z non-empty rows count:', len(vals))
    if vals:
        print('  Sample:', vals[:3])
