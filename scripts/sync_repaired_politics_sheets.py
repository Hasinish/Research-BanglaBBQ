import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("====================================================================")
print("PHASE E: SYNCHRONIZING REPAIRED POLITICS RECORDS TO GOOGLE SHEETS")
print("====================================================================")

# 1. Load validated local JSONL datasets
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_recs = [json.loads(line) for line in f]

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_recs = [json.loads(line) for line in f]

assert len(eng_recs) == 960
assert len(ben_recs) == 960

# We only update Q6-Q20 (rows 240-959, corresponding to sheet rows 242-961)
def rec_to_row(r):
    return [
        str(r['example_id']),
        str(r['question_index']),
        str(r['context_condition']),
        str(r['question_polarity']),
        str(r['type']),
        str(r['context']),
        str(r['question']),
        str(r['ans0']),
        str(r['ans1']),
        str(r['ans2']),
        str(r['label']),
        json.dumps(r['answer_info'], ensure_ascii=False),
        json.dumps(r['additional_metadata'], ensure_ascii=False),
        str(r['category']),
        str(r['id'])
    ]

eng_update_rows = [rec_to_row(r) for r in eng_recs[240:]]
ben_update_rows = [rec_to_row(r) for r in ben_recs[240:]]

print(f"Prepared {len(eng_update_rows)} ENG rows and {len(ben_update_rows)} BEN rows for sync (Rows 242-961).")

# 2. Update BanglaBBQ_ENG_Politics!A242:O961
print("Updating BanglaBBQ_ENG_Politics!A242:O961...")
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A242:O961',
    valueInputOption='RAW',
    body={'values': eng_update_rows}
).execute()
print("  ENG sheet update complete.")

# 3. Update BanglaBBQ_BEN_Politics!A242:O961
print("Updating BanglaBBQ_BEN_Politics!A242:O961...")
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A242:O961',
    valueInputOption='RAW',
    body={'values': ben_update_rows}
).execute()
print("  BEN sheet update complete.")

print("Live Google Sheets successfully synchronized with verified local datasets! 🏆")
