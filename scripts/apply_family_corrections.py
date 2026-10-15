import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

# 1. Fetch current data from both sheets
print("Fetching current PakBBQ_ENG_Age from Google Sheets...")
eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='PakBBQ_ENG_Age!A1:O2922'
).execute()
eng_rows = eng_res.get('values', [])
eng_headers = eng_rows[0]
eng_data = eng_rows[1:]

print("Fetching current BanglaBBQ_BEN_Age from Google Sheets...")
ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2922'
).execute()
ben_rows = ben_res.get('values', [])
ben_headers = ben_rows[0]
ben_data = ben_rows[1:]

print(f"English rows: {len(eng_data)}, Bengali rows: {len(ben_data)}")
assert len(eng_data) == 2920
assert len(ben_data) == 2920

def replace_family_term(b_text, from_term, to_term):
    res = b_text
    res = res.replace(f"আমার {from_term}", f"আমার {to_term}")
    res = res.replace(f"আর {from_term}", f"আর {to_term}")
    res = res.replace(f"{from_term} আর", f"{to_term} আর")
    res = res.replace(f"অন্যদিকে {from_term}", f"অন্যদিকে {to_term}")
    res = res.replace(f"{from_term} অসময়ে", f"{to_term} অসময়ে")
    if res == from_term:
        res = to_term
    return res

modified_records = []
new_ben_rows = [ben_headers]

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    e_full = " ".join(er[5:10])
    
    is_grandma = bool(re.search(r'\bgrandma\b', e_full, re.I))
    is_grandpa = bool(re.search(r'\bgrandpa\b', e_full, re.I))
    is_grandmother = bool(re.search(r'\bgrandmother\b', e_full, re.I))
    is_grandfather = bool(re.search(r'\bgrandfather\b', e_full, re.I))
    
    row_copy = list(br)
    
    if is_grandma or is_grandpa:
        from_term = 'দাদি' if is_grandma else 'দাদা'
        to_term = 'নানি' if is_grandma else 'নানা'
        eng_term = 'Grandma' if is_grandma else 'Grandpa'
        
        orig_context = br[5]
        orig_q = br[6]
        orig_ans0 = br[7]
        orig_ans1 = br[8]
        orig_ans2 = br[9]
        
        new_context = replace_family_term(orig_context, from_term, to_term)
        new_q = replace_family_term(orig_q, from_term, to_term)
        new_ans0 = replace_family_term(orig_ans0, from_term, to_term)
        new_ans1 = replace_family_term(orig_ans1, from_term, to_term)
        new_ans2 = replace_family_term(orig_ans2, from_term, to_term)
        
        row_copy[5] = new_context
        row_copy[6] = new_q
        row_copy[7] = new_ans0
        row_copy[8] = new_ans1
        row_copy[9] = new_ans2
        
        modified_records.append({
            'sheet_row': sheet_row,
            'id': er[14],
            'example_id': er[0],
            'eng_term': eng_term,
            'from_term': from_term,
            'to_term': to_term,
            'orig_context': orig_context,
            'new_context': new_context,
            'orig_ans': (orig_ans0, orig_ans1, orig_ans2),
            'new_ans': (new_ans0, new_ans1, new_ans2),
            'er': er,
            'br_before': br,
            'br_after': row_copy
        })
        
    new_ben_rows.append(row_copy)

print(f"\nTotal records modified: {len(modified_records)}")
assert len(modified_records) == 48
assert len(new_ben_rows) == 2921 # 1 header + 2920 rows

# Push updated data to BanglaBBQ_BEN_Age in Google Sheets
print("Pushing updated records to Google Sheets tab 'BanglaBBQ_BEN_Age'...")
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2921',
    valueInputOption='USER_ENTERED',
    body={'values': new_ben_rows}
).execute()

print("Google Sheets updated successfully!")

# Also sync local production file BanglaBBQ_BEN_New/Age.jsonl
print("Syncing local production file 'BanglaBBQ_BEN_New/Age.jsonl'...")
local_records = []
for r in new_ben_rows[1:]:
    # Reconstruct json object
    obj = {
        "example_id": int(r[0]) if r[0].isdigit() else r[0],
        "question_index": r[1],
        "context_condition": r[2],
        "question_polarity": r[3],
        "type": r[4],
        "context": r[5],
        "question": r[6],
        "ans0": r[7],
        "ans1": r[8],
        "ans2": r[9],
        "label": int(r[10]) if r[10].isdigit() else r[10],
        "answer_info": json.loads(r[11]) if r[11].startswith('{') else r[11],
        "additional_metadata": json.loads(r[12]) if r[12].startswith('{') else r[12],
        "category": r[13],
        "id": int(r[14]) if r[14].isdigit() else r[14]
    }
    local_records.append(obj)

with open("BanglaBBQ_BEN_New/Age.jsonl", "w", encoding="utf-8") as f:
    for obj in local_records:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"Synced {len(local_records)} records to 'BanglaBBQ_BEN_New/Age.jsonl'.")

# Save detailed report log for final response
with open("modified_records_report.json", "w", encoding="utf-8") as f:
    json.dump([
        {
            'sheet_row': m['sheet_row'],
            'id': m['id'],
            'example_id': m['example_id'],
            'eng_term': m['eng_term'],
            'from_term': m['from_term'],
            'to_term': m['to_term'],
            'orig_context': m['orig_context'],
            'new_context': m['new_context'],
            'orig_ans': m['orig_ans'],
            'new_ans': m['new_ans']
        } for m in modified_records
    ], f, ensure_ascii=False, indent=2)

print("Report data saved to 'modified_records_report.json'.")
