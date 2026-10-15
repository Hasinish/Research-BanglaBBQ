import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Re-fetching live data from Google Sheets for audit...")
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

assert len(eng_data) == 2920, f"Expected 2920 English rows, got {len(eng_data)}"
assert len(ben_data) == 2920, f"Expected 2920 Bengali rows, got {len(ben_data)}"

# Check 1: Mapping consistency across all 2,920 rows
# Grandma -> নানি
# Grandmother -> দাদি
# Grandpa -> নানা
# Grandfather -> দাদা

mapping_errors = []
target_counts = {'Grandma': 0, 'Grandmother': 0, 'Grandpa': 0, 'Grandfather': 0}

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    e_full = " ".join(er[5:10])
    b_full = " ".join(br[5:10])
    
    # Check Grandma
    if re.search(r'\bgrandma\b', e_full, re.I):
        target_counts['Grandma'] += 1
        if 'নানি' not in b_full or 'দাদি' in b_full:
            mapping_errors.append((sheet_row, er[14], 'Grandma', 'Expected নানি, found inconsistent text', b_full))
            
    # Check Grandmother
    if re.search(r'\bgrandmother\b', e_full, re.I):
        target_counts['Grandmother'] += 1
        if 'দাদি' not in b_full or 'নানি' in b_full:
            mapping_errors.append((sheet_row, er[14], 'Grandmother', 'Expected দাদি, found inconsistent text', b_full))
            
    # Check Grandpa
    if re.search(r'\bgrandpa\b', e_full, re.I):
        target_counts['Grandpa'] += 1
        if 'নানা' not in b_full or 'দাদা' in b_full:
            mapping_errors.append((sheet_row, er[14], 'Grandpa', 'Expected নানা, found inconsistent text', b_full))
            
    # Check Grandfather
    if re.search(r'\bgrandfather\b', e_full, re.I):
        target_counts['Grandfather'] += 1
        if 'দাদা' not in b_full or 'নানা' in b_full:
            mapping_errors.append((sheet_row, er[14], 'Grandfather', 'Expected দাদা, found inconsistent text', b_full))

print("\n--- CHECK 1 & 2: MAPPING CONSISTENCY ---")
print("Target counts verified across all 2,920 rows:")
for term, count in target_counts.items():
    print(f"  {term:<12}: {count} occurrences")
print(f"Mapping consistency errors found: {len(mapping_errors)}")

# Check 3: Logic consistency between context and answer choices
logic_errors = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    # If context mentions নানি, does answer mention নানি (and not দাদি/দাদা/নানা)?
    b_context = br[5]
    b_answers = br[7:10]
    
    if 'নানি' in b_context:
        has_nani_ans = any('নানি' in a for a in b_answers)
        has_other_ans = any(('দাদি' in a or 'দাদা' in a or 'নানা' in a) for a in b_answers)
        if not has_nani_ans or has_other_ans:
            logic_errors.append((sheet_row, 'Context has নানি but answers mismatch', b_answers))
            
    if 'নানা' in b_context:
        has_nana_ans = any('নানা' in a for a in b_answers)
        has_other_ans = any(('দাদি' in a or 'দাদা' in a or 'নানি' in a) for a in b_answers)
        if not has_nana_ans or has_other_ans:
            logic_errors.append((sheet_row, 'Context has নানা but answers mismatch', b_answers))

print("\n--- CHECK 3: CONTEXT & ANSWER LOGIC CONSISTENCY ---")
print(f"Context and answer mismatch errors: {len(logic_errors)}")

# Check 4: Metadata and labels completely untouched
metadata_diffs = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    # Verify cols 0 to 4 (example_id, question_index, context_condition, question_polarity, type)
    if er[0:5] != br[0:5]:
        metadata_diffs.append((sheet_row, 'Cols 0-4 mismatch', er[0:5], br[0:5]))
    # Verify col 10 (label)
    if er[10] != br[10]:
        metadata_diffs.append((sheet_row, 'Label mismatch', er[10], br[10]))
    # Verify col 13, 14 (category, id)
    if er[13:15] != br[13:15]:
        metadata_diffs.append((sheet_row, 'Category/ID mismatch', er[13:15], br[13:15]))

print("\n--- CHECK 4: METADATA & LABEL IMMUTABILITY ---")
print(f"Metadata or label discrepancies: {len(metadata_diffs)}")

# Check 5: Duplicate records audit
seen = {}
duplicates = []
for idx, r in enumerate(ben_data):
    sheet_row = idx + 2
    sig = (r[1], r[2], r[3], r[5], r[6], r[7], r[8], r[9], r[10])
    if sig in seen:
        duplicates.append((seen[sig], sheet_row, r[1], r[14]))
    else:
        seen[sig] = sheet_row

q2_dups = [d for d in duplicates if d[2] == '2']
print("\n--- CHECK 5: DUPLICATE RESOLUTION AUDIT ---")
print(f"Duplicates in Question Index 2 (target family template): {len(q2_dups)}")
print(f"Total remaining duplicates in entire dataset: {len(duplicates)}")
by_q = {}
for d in duplicates:
    by_q[d[2]] = by_q.get(d[2], 0) + 1
for q, cnt in sorted(by_q.items(), key=lambda x: int(x[0])):
    print(f"  Template Q{q:>2}: {cnt} duplicate pairs (unrelated)")
