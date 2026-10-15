import os
import json
import csv
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

backup_dir = os.path.join('backups', 'politics_before_corrections')
os.makedirs(backup_dir, exist_ok=True)

print("Fetching BanglaBBQ_ENG_Politics and BanglaBBQ_BEN_Politics...")
eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A1:Z500'
).execute().get('values', [])

ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A1:Z500'
).execute().get('values', [])

print(f"Fetched ENG rows: {len(eng_res)}, BEN rows: {len(ben_res)}")

# Save raw JSON dumps
with open(os.path.join(backup_dir, 'BanglaBBQ_ENG_Politics_raw.json'), 'w', encoding='utf-8') as f:
    json.dump(eng_res, f, ensure_ascii=False, indent=2)

with open(os.path.join(backup_dir, 'BanglaBBQ_BEN_Politics_raw.json'), 'w', encoding='utf-8') as f:
    json.dump(ben_res, f, ensure_ascii=False, indent=2)

# Save CSV backups
with open(os.path.join(backup_dir, 'BanglaBBQ_ENG_Politics_backup.csv'), 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(eng_res)

with open(os.path.join(backup_dir, 'BanglaBBQ_BEN_Politics_backup.csv'), 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(ben_res)

print("Backups saved successfully to", backup_dir)
