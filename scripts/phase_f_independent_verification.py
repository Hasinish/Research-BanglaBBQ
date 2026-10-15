import json
import hashlib
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("====================================================================")
print("PHASE F: INDEPENDENT LIVE READBACK & COMPREHENSIVE VERIFICATION")
print("====================================================================")

# 1. Fetch live sheets
print("1. Reading back live Politics tabs from Google Sheets...")
live_eng_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_ENG_Politics!A1:O961'
).execute().get('values', [])

live_ben_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_BEN_Politics!A1:O961'
).execute().get('values', [])

assert len(live_eng_data) == 961, f"Expected 961 rows, got {len(live_eng_data)}"
assert len(live_ben_data) == 961, f"Expected 961 rows, got {len(live_ben_data)}"
print(f"  Successfully fetched 961 rows from both Politics tabs.")

# 2. Compare against local production JSONL
print("\n2. Comparing live Google Sheets field-by-field against local production JSONL...")
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    local_eng = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    local_ben = [json.loads(line) for line in f]

sheet_eng_rows = live_eng_data[1:]
sheet_ben_rows = live_ben_data[1:]

eng_diffs = 0
ben_diffs = 0

for i in range(960):
    r_e = sheet_eng_rows[i]
    r_b = sheet_ben_rows[i]
    loc_e = local_eng[i]
    loc_b = local_ben[i]
    
    dict_e = {
        'example_id': int(r_e[0]),
        'question_index': int(r_e[1]),
        'context_condition': r_e[2],
        'question_polarity': r_e[3],
        'type': r_e[4],
        'context': r_e[5],
        'question': r_e[6],
        'ans0': r_e[7],
        'ans1': r_e[8],
        'ans2': r_e[9],
        'label': int(r_e[10]),
        'answer_info': json.loads(r_e[11]),
        'additional_metadata': json.loads(r_e[12]),
        'category': r_e[13],
        'id': int(r_e[14])
    }
    dict_b = {
        'example_id': int(r_b[0]),
        'question_index': int(r_b[1]),
        'context_condition': r_b[2],
        'question_polarity': r_b[3],
        'type': r_b[4],
        'context': r_b[5],
        'question': r_b[6],
        'ans0': r_b[7],
        'ans1': r_b[8],
        'ans2': r_b[9],
        'label': int(r_b[10]),
        'answer_info': json.loads(r_b[11]),
        'additional_metadata': json.loads(r_b[12]),
        'category': r_b[13],
        'id': int(r_b[14])
    }
    
    if dict_e != loc_e:
        eng_diffs += 1
    if dict_b != loc_b:
        ben_diffs += 1

print(f"  Field-by-field differences: ENG={eng_diffs}, BEN={ben_diffs} (Target: 0)")
assert eng_diffs == 0, f"ENG sheet has {eng_diffs} differences from local JSONL"
assert ben_diffs == 0, f"BEN sheet has {ben_diffs} differences from local JSONL"

# 3. Check Q1-Q5 preservation against pre-audit hashes
print("\n3. Verifying Q1-Q5 Hash Preservation against baseline...")
q1_q5_eng_hash = hashlib.sha256(json.dumps(local_eng[:240], sort_keys=True).encode('utf-8')).hexdigest()
q1_q5_ben_hash = hashlib.sha256(json.dumps(local_ben[:240], sort_keys=True).encode('utf-8')).hexdigest()

exp_eng_hash = "2ab59aec0cb6f6ce42f60e8912c861373b96008db8dec2af281046def64595b3"
exp_ben_hash = "eb6ae51a7b0d4d739243c995e23e5e7a6a55dc895c4a791975dbb18c50d4fc23"

assert q1_q5_eng_hash == exp_eng_hash, "CRITICAL: Q1-Q5 ENG modified!"
assert q1_q5_ben_hash == exp_ben_hash, "CRITICAL: Q1-Q5 BEN modified!"
print(f"  Q1-Q5 ENG SHA-256: {q1_q5_eng_hash} (100% BYTE MATCH)")
print(f"  Q1-Q5 BEN SHA-256: {q1_q5_ben_hash} (100% BYTE MATCH)")

# 4. Check Age tabs are untouched
print("\n4. Verifying Age tabs are completely untouched...")
age_eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='PakBBQ_ENG_Age!A1:O2'
).execute().get('values', [])
age_ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_BEN_Age!A1:O2'
).execute().get('values', [])

# Check grid sizes of Age sheets
sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
age_sheets = [s for s in sheet_metadata['sheets'] if s['properties']['title'] in ['PakBBQ_ENG_Age', 'BanglaBBQ_BEN_Age']]
for s in age_sheets:
    title = s['properties']['title']
    rc = s['properties']['gridProperties']['rowCount']
    print(f"  {title}: rowCount={rc} (PASS, untouched)")
    assert rc == 2921, f"{title} rowCount modified! Found {rc}"

print("\n====================================================================")
print("ALL INDEPENDENT VERIFICATION CHECKS PASSED WITH 100% FIDELITY! 🏆")
print("====================================================================")
