import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Fetching PakBBQ_ENG_Age and BanglaBBQ_BEN_Age...")
eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='PakBBQ_ENG_Age!A1:O2922'
).execute().get('values', [])
ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2922'
).execute().get('values', [])

eng_data = eng_res[1:]
ben_data = ben_res[1:]

print(f"Total rows: ENG={len(eng_data)}, BEN={len(ben_data)}")

# Search for grandparent / grandchild in English
gp_matches = []
gc_matches = []

# Also search for দাদা-দাদি / নাতি-নাতনি in Bengali
dada_dadi_rows = []
nati_natni_rows = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    e_full = " ".join(er[5:10])
    b_full = " ".join(br[5:10])
    
    if re.search(r'\bgrandparent\b', e_full, re.I):
        gp_matches.append((sheet_row, er[1], er[14], er, br))
    if re.search(r'\bgrandchild\b', e_full, re.I):
        gc_matches.append((sheet_row, er[1], er[14], er, br))
        
    if 'দাদা-দাদি' in b_full or 'দাদি-দাদা' in b_full:
        dada_dadi_rows.append((sheet_row, er[1], er[14], er, br))
    if 'নাতি-নাতনি' in b_full or 'নাতনি-নাতি' in b_full:
        nati_natni_rows.append((sheet_row, er[1], er[14], er, br))

print(f"English 'grandparent' matches: {len(gp_matches)} rows")
print(f"English 'grandchild' matches: {len(gc_matches)} rows")
print(f"Total English GP/GC matches: {len(gp_matches) + len(gc_matches)} rows")

print(f"\nBengali 'দাদা-দাদি' occurrences: {len(dada_dadi_rows)} rows")
print(f"Bengali 'নাতি-নাতনি' occurrences: {len(nati_natni_rows)} rows")

# Breakdown by question_index
print("\nBreakdown of English grandparent rows by Question Index:")
q_gp = {}
for r in gp_matches:
    q_gp[r[1]] = q_gp.get(r[1], 0) + 1
for k, v in sorted(q_gp.items(), key=lambda x: int(x[0])):
    print(f"  Q{k}: {v} rows")

print("\nBreakdown of English grandchild rows by Question Index:")
q_gc = {}
for r in gc_matches:
    q_gc[r[1]] = q_gc.get(r[1], 0) + 1
for k, v in sorted(q_gc.items(), key=lambda x: int(x[0])):
    print(f"  Q{k}: {v} rows")
