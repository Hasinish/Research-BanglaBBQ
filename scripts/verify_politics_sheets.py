from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    res = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1:K3"
    ).execute()
    print(f"=== {title} ===")
    for row in res.get('values', []):
        print(" | ".join(row[:7]))
    print()
