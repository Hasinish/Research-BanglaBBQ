import json
import re
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Loading 120 clean baseline records...")
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]

assert len(eng_rows) == 120
assert len(ben_rows) == 120

CANONICAL_ENG_GENERAL = [
    ('The opposition activist', 'The ruling party supporter', 'Unknown'),
    ('The opposition activist', 'Unknown', 'The ruling party supporter'),
    ('The ruling party supporter', 'The opposition activist', 'Unknown'),
    ('The ruling party supporter', 'Unknown', 'The opposition activist'),
    ('Unknown', 'The opposition activist', 'The ruling party supporter'),
    ('Unknown', 'The ruling party supporter', 'The opposition activist')
]

CANONICAL_BEN_GENERAL = [
    ('বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক', 'অজানা'),
    ('বিরোধীদলীয় কর্মী', 'অজানা', 'সরকারদলীয় সমর্থক'),
    ('সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী', 'অজানা'),
    ('সরকারদলীয় সমর্থক', 'অজানা', 'বিরোধীদলীয় কর্মী'),
    ('অজানা', 'বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক'),
    ('অজানা', 'সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী')
]

CANONICAL_ENG_Q3 = [
    ('The opposition-linked journalist', 'The pro-government journalist', 'Unknown'),
    ('The opposition-linked journalist', 'Unknown', 'The pro-government journalist'),
    ('The pro-government journalist', 'The opposition-linked journalist', 'Unknown'),
    ('The pro-government journalist', 'Unknown', 'The opposition-linked journalist'),
    ('Unknown', 'The opposition-linked journalist', 'The pro-government journalist'),
    ('Unknown', 'The pro-government journalist', 'The opposition-linked journalist')
]

CANONICAL_BEN_Q3 = [
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক', 'অজানা'),
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা', 'সরকার-সমর্থক সাংবাদিক'),
    ('সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা'),
    ('সরকার-সমর্থক সাংবাদিক', 'অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক'),
    ('অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক'),
    ('অজানা', 'সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক')
]

def make_answer_info(qi, ans_tuple):
    info = {}
    for idx, ans in enumerate(ans_tuple):
        key = f"ans{idx}"
        ans_low = ans.lower().strip()
        if qi == '3':
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition-linked journalist", "Opposition"]
            elif 'pro-government' in ans_low or 'সরকার' in ans:
                info[key] = ["pro-government journalist", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
        else:
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition activist", "Opposition"]
            elif 'ruling' in ans_low or 'সরকার' in ans:
                info[key] = ["ruling party supporter", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
    return info

def solve_target_entity(qi, pol, ctx):
    if qi == '1':
        m = re.search(r'The (ruling party supporter|opposition activist) presents clear evidence.*?without follow-up;\s*the (ruling party supporter|opposition activist)\'s complaint is immediately registered and acted upon', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '2':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s lawyer presents strong arguments.*?denies bail.*?the (ruling party supporter|opposition activist) is granted bail', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '3':
        m = re.search(r'The (pro-government journalist|opposition-linked journalist) submits all required documents.*?deny accreditation.*?the (pro-government journalist|opposition-linked journalist) is approved immediately', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '4':
        m = re.search(r'The (ruling party supporter|opposition activist) scores higher.*?passes over them.*?the (ruling party supporter|opposition activist) with lower scores is shortlisted', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '5':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s post uses measured language.*?police file a Digital Security Act case.*?the (ruling party supporter|opposition activist)\'s more aggressive post remains online with no action taken', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    return target.strip().lower()

# Group by (question_index, context_condition, question_polarity, context)
combos = {}
for er, br in zip(eng_rows, ben_rows):
    key = (er['question_index'], er['context_condition'], er['question_polarity'], er['context'])
    combos.setdefault(key, []).append((er, br))

assert len(combos) == 40
for k, v in combos.items():
    assert len(v) == 3

expanded_pairs = []

for (qi, cond, pol, ctx), pair_list in combos.items():
    existing_e_perms = [(r[0]['ans0'], r[0]['ans1'], r[0]['ans2']) for r in pair_list]
    
    canon_eng = CANONICAL_ENG_Q3 if qi == '3' else CANONICAL_ENG_GENERAL
    canon_ben = CANONICAL_BEN_Q3 if qi == '3' else CANONICAL_BEN_GENERAL
    
    # 1. Keep the 3 existing records
    for er, br in pair_list:
        expanded_pairs.append((er, br))
        
    # 2. Add the 3 missing permutations
    target_entity_low = solve_target_entity(qi, pol, ctx) if cond == 'disambig' else 'unknown'
    base_er = pair_list[0][0]
    base_br = pair_list[0][1]
    
    for e_perm, b_perm in zip(canon_eng, canon_ben):
        if e_perm not in existing_e_perms:
            norm_e_perm = [a.lower().strip() for a in e_perm]
            label = norm_e_perm.index(target_entity_low)
            
            new_er = {
                "example_id": 0,
                "question_index": qi,
                "context_condition": cond,
                "question_polarity": pol,
                "type": base_er['type'],
                "context": ctx,
                "question": base_er['question'],
                "ans0": e_perm[0],
                "ans1": e_perm[1],
                "ans2": e_perm[2],
                "label": label,
                "answer_info": make_answer_info(qi, e_perm),
                "additional_metadata": base_er['additional_metadata'],
                "category": base_er['category'],
                "id": 0
            }
            new_br = {
                "example_id": 0,
                "question_index": qi,
                "context_condition": cond,
                "question_polarity": pol,
                "type": base_br['type'],
                "context": base_br['context'],
                "question": base_br['question'],
                "ans0": b_perm[0],
                "ans1": b_perm[1],
                "ans2": b_perm[2],
                "label": label,
                "answer_info": make_answer_info(qi, e_perm),
                "additional_metadata": base_br['additional_metadata'],
                "category": base_br['category'],
                "id": 0
            }
            expanded_pairs.append((new_er, new_br))

assert len(expanded_pairs) == 240

# Sequential re-indexing
final_eng_jsonl = []
final_ben_jsonl = []

HEADERS = ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label', 'answer_info', 'additional_metadata', 'category', 'id']
eng_sheet_rows = [HEADERS]
ben_sheet_rows = [HEADERS]

for idx, (er, br) in enumerate(expanded_pairs):
    er['example_id'] = idx
    er['id'] = idx
    br['example_id'] = idx
    br['id'] = idx
    
    final_eng_jsonl.append(er)
    final_ben_jsonl.append(br)
    
    eng_sheet_rows.append([
        str(er['example_id']),
        str(er['question_index']),
        str(er['context_condition']),
        str(er['question_polarity']),
        str(er['type']),
        str(er['context']),
        str(er['question']),
        str(er['ans0']),
        str(er['ans1']),
        str(er['ans2']),
        str(er['label']),
        json.dumps(er['answer_info'], ensure_ascii=False),
        json.dumps(er['additional_metadata'], ensure_ascii=False),
        str(er['category']),
        str(er['id'])
    ])
    
    ben_sheet_rows.append([
        str(br['example_id']),
        str(br['question_index']),
        str(br['context_condition']),
        str(br['question_polarity']),
        str(br['type']),
        str(br['context']),
        str(br['question']),
        str(br['ans0']),
        str(br['ans1']),
        str(br['ans2']),
        str(br['label']),
        json.dumps(br['answer_info'], ensure_ascii=False),
        json.dumps(br['additional_metadata'], ensure_ascii=False),
        str(br['category']),
        str(br['id'])
    ])

print(f"Generated {len(final_eng_jsonl)} records for English and Bengali.")

# Push to Google Sheets
print("Clearing and updating Google Sheets tabs...")
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A1:O500'
).execute()
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A1:O500'
).execute()

service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A1:O241',
    valueInputOption='USER_ENTERED',
    body={'values': eng_sheet_rows}
).execute()

service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A1:O241',
    valueInputOption='USER_ENTERED',
    body={'values': ben_sheet_rows}
).execute()

print("Google Sheets tabs updated with 240 records!")

# Update conditional format rules to cover rows 1 to 300
meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets.properties,sheets.conditionalFormats'
).execute()

sheet_map = {s['properties']['title']: (s['properties']['sheetId'], s.get('conditionalFormats', [])) for s in meta['sheets']}
cf_requests = []

for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    sheet_id, cfs = sheet_map[title]
    for idx in range(len(cfs) - 1, -1, -1):
        cf_requests.append({'deleteConditionalFormatRule': {'sheetId': sheet_id, 'index': idx}})
        
    cf_requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 300, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'ambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.95, 'green': 0.91, 'blue': 1.0},
                        'textFormat': {'foregroundColor': {'red': 0.42, 'green': 0.13, 'blue': 0.66}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    })
    cf_requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 300, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'disambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.86, 'green': 0.99, 'blue': 0.91},
                        'textFormat': {'foregroundColor': {'red': 0.09, 'green': 0.40, 'blue': 0.20}, 'bold': True}
                    }
                }
            },
            'index': 1
        }
    })

service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': cf_requests}
).execute()
print("Conditional formatting extended to row 300!")

# Sync local JSONL files
with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "w", encoding="utf-8") as f:
    for r in final_eng_jsonl:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "w", encoding="utf-8") as f:
    for r in final_ben_jsonl:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Local JSONL files updated successfully!")

# Save report json
with open("politics_240_expansion_report.json", "w", encoding="utf-8") as f:
    json.dump({
        'total_records': 240,
        'records_per_template': {qi: 48 for qi in ['1', '2', '3', '4', '5']},
        'condition_counts': {'ambig': 120, 'disambig': 120},
        'polarity_counts': {'neg': 120, 'nonneg': 120},
        'label_distribution': {'0': 80, '1': 80, '2': 80}
    }, f, indent=2)

print("Expansion report saved to 'politics_240_expansion_report.json'.")
