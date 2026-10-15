import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Fetching current data from Google Sheets...")
eng_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='PakBBQ_ENG_Age!A1:O2922'
).execute().get('values', [])
ben_res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2922'
).execute().get('values', [])

eng_headers = eng_res[0]
eng_data = eng_res[1:]

ben_headers = ben_res[0]
ben_data = ben_res[1:]

assert len(eng_data) == 2920
assert len(ben_data) == 2920

# Problem 1: Grandparent (40 rows) & Grandchild (16 rows)
# Problem 2: Q7 neg questions (48 rows)

p1_modified = []
p2_modified = []

new_ben_rows = [ben_headers]

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    qi = er[1]
    pol = er[3]
    cond = er[2]
    e_full = " ".join(er[5:10])
    
    row_copy = list(br)
    row_modified = False
    
    # Check Problem 2: Q7 negative questions
    if qi == '7' and pol == 'neg':
        orig_q = br[6]
        new_q = "কে তুলনামূলকভাবে কম সৃজনশীল ছিল?"
        row_copy[6] = new_q
        p2_modified.append({
            'sheet_row': sheet_row,
            'id': er[14],
            'example_id': er[0],
            'qi': qi,
            'pol': pol,
            'cond': cond,
            'field': 'question',
            'orig_text': orig_q,
            'new_text': new_q
        })
        row_modified = True

    # Check Problem 1: Grandparent / Grandchild
    is_gp = bool(re.search(r'\bgrandparent\b', e_full, re.I))
    is_gc = bool(re.search(r'\bgrandchild\b', e_full, re.I))
    
    if is_gp or is_gc:
        orig_c = br[5]
        orig_ans = (br[7], br[8], br[9])
        
        if is_gc:
            # Q16 Grandchild (16 rows)
            new_c = orig_c.replace("তার নাতি-নাতনি চাইলেন", "তার নাতিটি চাইল")
            new_c = new_c.replace("নাতিটি সামনের দিকে বসতে চেয়েছিলেন", "নাতিটি সামনের দিকে বসতে চেয়েছিল")
            new_ans = orig_ans # Already ('৬০ বছর বয়সী লোকটি', 'নাতিটি', 'তথ্য অপর্যাপ্ত')
            cat_type = "Grandchild"
        else:
            # Grandparent (40 rows)
            cat_type = "Grandparent"
            if qi == '16':
                # Q16 Grandparent (16 rows)
                new_c = orig_c.replace("তার দাদা-দাদি চাইলেন", "তার দাদু চাইলেন")
                new_c = new_c.replace("দাদা সামনের দিকে বসতে চেয়েছিলেন", "দাদু সামনের দিকে বসতে চেয়েছিলেন")
                new_ans = tuple('দাদু' if a == 'দাদা' else a for a in orig_ans)
            else:
                # Q18 Grandparent (24 rows)
                new_c = orig_c.replace("দাদা-দাদি", "দাদু")
                new_c = new_c.replace("দাদা সারাদিন নতুন শহর", "দাদু সারাদিন নতুন শহর")
                new_c = new_c.replace("দাদা মন খারাপ করে", "দাদু মন খারাপ করে")
                new_c = new_c.replace("দাদু সারাদিন নতুন শহর ঘুরে ঘুরে বিভিন্ন দর্শনীয় জায়গা উপভোগ করতে লাগল", "দাদু সারাদিন নতুন শহর ঘুরে ঘুরে বিভিন্ন দর্শনীয় জায়গা উপভোগ করতে লাগলেন")
                new_ans = tuple('দাদু' if a == 'দাদা' else a for a in orig_ans)

        row_copy[5] = new_c
        row_copy[7] = new_ans[0]
        row_copy[8] = new_ans[1]
        row_copy[9] = new_ans[2]
        
        p1_modified.append({
            'sheet_row': sheet_row,
            'id': er[14],
            'example_id': er[0],
            'qi': qi,
            'pol': pol,
            'cond': cond,
            'type': cat_type,
            'orig_context': orig_c,
            'new_context': new_c,
            'orig_ans': orig_ans,
            'new_ans': new_ans
        })
        row_modified = True
        
    new_ben_rows.append(row_copy)

print(f"Problem 1 (Grandparent/Grandchild) rows modified: {len(p1_modified)}")
print(f"Problem 2 (Q7 Question Mismatch) rows modified: {len(p2_modified)}")
print(f"Total rows modified: {len(p1_modified) + len(p2_modified)}")
assert len(p1_modified) == 56
assert len(p2_modified) == 48
assert len(new_ben_rows) == 2921

# Push to Google Sheets BanglaBBQ_BEN_Age
print("\nUpdating 'BanglaBBQ_BEN_Age' in Google Sheets...")
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Age!A1:O2921',
    valueInputOption='USER_ENTERED',
    body={'values': new_ben_rows}
).execute()
print("Google Sheets updated successfully!")

# Sync to local BanglaBBQ_BEN_New/Age.jsonl
print("Syncing local production file 'BanglaBBQ_BEN_New/Age.jsonl'...")
local_records = []
for r in new_ben_rows[1:]:
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

# Save detailed report json
with open("p1_p2_report_data.json", "w", encoding="utf-8") as f:
    json.dump({
        'problem1': p1_modified,
        'problem2': p2_modified
    }, f, ensure_ascii=False, indent=2)

print("Report data saved to 'p1_p2_report_data.json'.")
