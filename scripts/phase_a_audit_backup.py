import os
import json
import hashlib
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

backup_dir = 'backups/audit_20261016'
os.makedirs(backup_dir, exist_ok=True)

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("1. Fetching live Google Sheets data...")
eng_sheet_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_ENG_Politics!A1:O961'
).execute().get('values', [])

ben_sheet_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_BEN_Politics!A1:O961'
).execute().get('values', [])

print(f"Fetched {len(eng_sheet_data)} ENG rows (including header) and {len(ben_sheet_data)} BEN rows.")

# Save backups of live sheets
with open(os.path.join(backup_dir, 'live_sheet_eng_961.json'), 'w', encoding='utf-8') as f:
    json.dump(eng_sheet_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(backup_dir, 'live_sheet_ben_961.json'), 'w', encoding='utf-8') as f:
    json.dump(ben_sheet_data, f, ensure_ascii=False, indent=2)

# Save backups of current local JSONL files
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_jsonl_content = f.read()

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_jsonl_content = f.read()

with open(os.path.join(backup_dir, 'local_eng_backup.jsonl'), 'w', encoding='utf-8') as f:
    f.write(eng_jsonl_content)

with open(os.path.join(backup_dir, 'local_ben_backup.jsonl'), 'w', encoding='utf-8') as f:
    f.write(ben_jsonl_content)

print("Backups successfully created in:", backup_dir)

# Parse JSONL records
eng_records = [json.loads(line) for line in eng_jsonl_content.strip().split('\n')]
ben_records = [json.loads(line) for line in ben_jsonl_content.strip().split('\n')]

# Compute SHA-256 for Q1-Q5
q1_q5_eng_str = json.dumps(eng_records[:240], sort_keys=True)
q1_q5_ben_str = json.dumps(ben_records[:240], sort_keys=True)

eng_q1_q5_hash = hashlib.sha256(q1_q5_eng_str.encode('utf-8')).hexdigest()
ben_q1_q5_hash = hashlib.sha256(q1_q5_ben_str.encode('utf-8')).hexdigest()

print(f"Q1-Q5 ENG SHA-256 (records 0-239): {eng_q1_q5_hash}")
print(f"Q1-Q5 BEN SHA-256 (records 0-239): {ben_q1_q5_hash}")

# Save hashes to a file for continuous verification
hashes = {
    "eng_q1_q5_hash": eng_q1_q5_hash,
    "ben_q1_q5_hash": ben_q1_q5_hash
}
with open(os.path.join(backup_dir, 'q1_q5_hashes.json'), 'w', encoding='utf-8') as f:
    json.dump(hashes, f, indent=2)

# Compare Live Sheet vs Local JSONL
header = eng_sheet_data[0]
sheet_eng_rows = eng_sheet_data[1:]
sheet_ben_rows = ben_sheet_data[1:]

mismatch_eng = 0
mismatch_ben = 0

for i in range(960):
    rec_eng = eng_records[i]
    rec_ben = ben_records[i]
    row_e = sheet_eng_rows[i]
    row_b = sheet_ben_rows[i]
    
    # Check fields against sheet row
    # Header: ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label', 'answer_info', 'additional_metadata', 'category', 'id']
    sheet_e_dict = {
        'example_id': int(row_e[0]),
        'question_index': str(row_e[1]),
        'context_condition': row_e[2],
        'question_polarity': row_e[3],
        'type': row_e[4],
        'context': row_e[5],
        'question': row_e[6],
        'ans0': row_e[7],
        'ans1': row_e[8],
        'ans2': row_e[9],
        'label': int(row_e[10]),
        'answer_info': json.loads(row_e[11]),
        'additional_metadata': json.loads(row_e[12]),
        'category': row_e[13],
        'id': int(row_e[14])
    }
    sheet_b_dict = {
        'example_id': int(row_b[0]),
        'question_index': str(row_b[1]),
        'context_condition': row_b[2],
        'question_polarity': row_b[3],
        'type': row_b[4],
        'context': row_b[5],
        'question': row_b[6],
        'ans0': row_b[7],
        'ans1': row_b[8],
        'ans2': row_b[9],
        'label': int(row_b[10]),
        'answer_info': json.loads(row_b[11]),
        'additional_metadata': json.loads(row_b[12]),
        'category': row_b[13],
        'id': int(row_b[14])
    }
    
    if rec_eng != sheet_e_dict:
        mismatch_eng += 1
    if rec_ben != sheet_b_dict:
        mismatch_ben += 1

print(f"Sheet vs Local JSONL: ENG Mismatches = {mismatch_eng}, BEN Mismatches = {mismatch_ben}")
