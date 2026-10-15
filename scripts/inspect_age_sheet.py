from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("token.json")
service = build("sheets", "v4", credentials=creds)
res = service.spreadsheets().values().get(
    spreadsheetId="1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY",
    range="PakBBQ_ENG_Age!A1:O3"
).execute()

for r in res.get('values', []):
    print("Row length:", len(r))
    print("Cols 0-4:", r[0:5])
    print("Cols 10-14:", r[10:15])
