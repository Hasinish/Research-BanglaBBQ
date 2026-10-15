from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("token.json")
service = build("sheets", "v4", credentials=creds)
meta = service.spreadsheets().get(spreadsheetId="1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY").execute()
for s in meta["sheets"]:
    p = s["properties"]
    print(f"Sheet ID: {p['sheetId']} | Title: {p['title']} | Index: {p['index']}")
