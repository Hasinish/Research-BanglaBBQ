import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Fetching PakBBQ_ENG_Age...")
eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='PakBBQ_ENG_Age!A1:O2922'
).execute()
eng_rows = eng_res.get('values', [])
eng_headers = eng_rows[0]
eng_data = eng_rows[1:]

print("Fetching BanglaBBQ_BEN_Age...")
ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2922'
).execute()
ben_rows = ben_res.get('values', [])
ben_headers = ben_rows[0]
ben_data = ben_rows[1:]

print(f"English rows: {len(eng_data)}, Bengali rows: {len(ben_data)}")

# Expected column indices:
# 0: example_id, 1: question_index, 2: context_condition, 3: question_polarity, 4: type,
# 5: context, 6: question, 7: ans0, 8: ans1, 9: ans2, 10: label,
# 11: answer_info, 12: additional_metadata, 13: category, 14: id

terms = ["grandma", "grandmother", "grandpa", "grandfather"]

matches = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row_num = idx + 2 # Excel 1-indexed row number (Header is row 1)
    
    # Extract fields from English
    e_context = er[5] if len(er) > 5 else ""
    e_question = er[6] if len(er) > 6 else ""
    e_ans0 = er[7] if len(er) > 7 else ""
    e_ans1 = er[8] if len(er) > 8 else ""
    e_ans2 = er[9] if len(er) > 9 else ""
    e_ans_info = er[11] if len(er) > 11 else ""
    
    e_full = f"{e_context} {e_question} {e_ans0} {e_ans1} {e_ans2} {e_ans_info}".lower()
    
    found = []
    for t in terms:
        # Match whole word, including possessives like grandma's
        if re.search(r'\b' + t + r"('s)?\b", e_full):
            found.append(t)
            
    if found:
        matches.append({
            'sheet_row': sheet_row_num,
            'idx': idx,
            'id': er[14] if len(er) > 14 else er[0],
            'q_idx': er[1] if len(er) > 1 else "",
            'terms': found,
            'er': er,
            'br': br
        })

print(f"\nTotal records with target family terms: {len(matches)}")

# Breakdown by terms and question_index
breakdown = {}
for m in matches:
    t_key = "+".join(sorted(m['terms']))
    k = (m['q_idx'], t_key)
    breakdown[k] = breakdown.get(k, 0) + 1

print("\nBreakdown by (Question Index, Term):")
for k, v in sorted(breakdown.items(), key=lambda x: (int(x[0][0]) if x[0][0].isdigit() else 999, x[0][1])):
    print(f"  Question Index {k[0]:>2} | Terms: {k[1]:<25} -> {v} rows")

