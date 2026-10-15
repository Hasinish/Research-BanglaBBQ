import json
import shutil
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from expand_politics_to_160 import generate_dataset

eng_160 = generate_dataset("ENG")
ben_160 = generate_dataset("BEN")

dir_path = "Dataset_ BanglaBBQ_Old/Politics"

# 1. Create backups of old 112-row files
eng_old = os.path.join(dir_path, "banglabbq_politics_english.jsonl")
ben_old = os.path.join(dir_path, "banglabbq_politics_bengali.jsonl")

eng_bak = os.path.join(dir_path, "banglabbq_politics_english_112old.jsonl")
ben_bak = os.path.join(dir_path, "banglabbq_politics_bengali_112old.jsonl")

if not os.path.exists(eng_bak):
    shutil.copyfile(eng_old, eng_bak)
    print("Created backup:", eng_bak)

if not os.path.exists(ben_bak):
    shutil.copyfile(ben_old, ben_bak)
    print("Created backup:", ben_bak)

# 2. Write new 160-row files
with open(eng_old, "w", encoding="utf-8") as f:
    for row in eng_160:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(f"Updated {eng_old} with 160 rows.")

with open(ben_old, "w", encoding="utf-8") as f:
    for row in ben_160:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(f"Updated {ben_old} with 160 rows.")

# 3. Push to Google Spreadsheet
spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

headers = [
    'example_id', 'question_index', 'context_condition', 'question_polarity', 'type',
    'context', 'question', 'ans0', 'ans1', 'ans2',
    'label', 'answer_info', 'additional_metadata', 'category', 'id'
]

col_widths = [
    (0, 75),   # example_id
    (1, 85),   # question_index
    (2, 125),  # context_condition
    (3, 125),  # question_polarity
    (4, 75),   # type
    (5, 480),  # context
    (6, 270),  # question
    (7, 160),  # ans0
    (8, 160),  # ans1
    (9, 160),  # ans2
    (10, 65),  # label
    (11, 180), # answer_info
    (12, 180), # additional_metadata
    (13, 70),  # category
    (14, 75)   # id
]

for title, dataset in [('BanglaBBQ_ENG_Politics', eng_160), ('BanglaBBQ_BEN_Politics', ben_160)]:
    sheet_id = sheet_map[title]
    rows = [headers]
    for r in dataset:
        row = [
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
        rows.append(row)
        
    total_rows = len(rows) # 161
    print(f"Uploading {total_rows} rows to '{title}'...")
    
    # Clear old data first
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1:O300"
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1",
        valueInputOption='USER_ENTERED',
        body={'values': rows}
    ).execute()

    # Re-apply styling for 161 rows
    requests = [
        # Middle vertical alignment across all data cells
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {'userEnteredFormat': {'verticalAlignment': 'MIDDLE'}},
                'fields': 'userEnteredFormat.verticalAlignment'
            }
        },
        # Center alignment for metadata columns
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 0, 'endColumnIndex': 5},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        },
        # Text Wrap and Left Align for context, question, ans0, ans1, ans2
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 5, 'endColumnIndex': 10},
                'cell': {'userEnteredFormat': {'wrapStrategy': 'WRAP', 'horizontalAlignment': 'LEFT'}},
                'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.horizontalAlignment'
            }
        },
        # Center align for label
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 10, 'endColumnIndex': 11},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        },
        # CLIP and Left Align for JSON columns
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 11, 'endColumnIndex': 13},
                'cell': {'userEnteredFormat': {'wrapStrategy': 'CLIP', 'horizontalAlignment': 'LEFT'}},
                'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.horizontalAlignment'
            }
        },
        # Center align for category, id
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 13, 'endColumnIndex': 15},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()
    print(f"Updated and restyled '{title}'!")

print("\nALL POLITICS DATASETS AND SHEETS EXPANDED TO 160 ROWS!")
