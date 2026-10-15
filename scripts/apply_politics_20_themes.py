import json
import sys
import time
import socket
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
socket.setdefaulttimeout(60)

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

POL_ENG_ID = 1888499205
POL_BEN_ID = 2128232344
AGE_ENG_ID = 0
AGE_BEN_ID = 1006819770

def execute_with_retry(request, retries=5, delay=3):
    for attempt in range(retries):
        try:
            return request.execute()
        except Exception as e:
            if attempt < retries - 1:
                print(f"Network error: {e}. Retrying in {delay}s (attempt {attempt+1}/{retries})...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e

print("Loading generated Q6-Q20 records...")
with open('Dataset_ BanglaBBQ_Old/Politics/q6_q20_generated_eng.json', 'r', encoding='utf-8') as f:
    new_eng_records = json.load(f)
with open('Dataset_ BanglaBBQ_Old/Politics/q6_q20_generated_ben.json', 'r', encoding='utf-8') as f:
    new_ben_records = json.load(f)

print(f"Loaded {len(new_eng_records)} new ENG records, {len(new_ben_records)} new BEN records.")

# --- STEP 1: WRITE VALUES TO GOOGLE SHEETS (ROWS 242 TO 961) ---
print("Writing values to BanglaBBQ_ENG_Politics!A242:O961...")
val_eng_req = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_ENG_Politics!A242:O961',
    valueInputOption='RAW',
    body={'values': new_eng_records}
)
execute_with_retry(val_eng_req)

print("Writing values to BanglaBBQ_BEN_Politics!A242:O961...")
val_ben_req = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='BanglaBBQ_BEN_Politics!A242:O961',
    valueInputOption='RAW',
    body={'values': new_ben_records}
)
execute_with_retry(val_ben_req)

print("Data rows written successfully!")

# --- STEP 2: PREPARE FORMATTING REQUESTS FOR NEW ROWS (241 to 961, 0-indexed) ---
requests = []

pairs = [
    (AGE_ENG_ID, POL_ENG_ID, "ENG"),
    (AGE_BEN_ID, POL_BEN_ID, "BEN")
]

for src_id, dst_id, lang in pairs:
    # A. Copy 4-row format pattern A2:O5 to each of the 180 new blocks (block 60 to 239)
    for block_idx in range(60, 240):
        start_row = 1 + block_idx * 4
        end_row = start_row + 4
        requests.append({
            'copyPaste': {
                'source': {
                    'sheetId': src_id,
                    'startRowIndex': 1,
                    'endRowIndex': 5,
                    'startColumnIndex': 0,
                    'endColumnIndex': 15
                },
                'destination': {
                    'sheetId': dst_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': 0,
                    'endColumnIndex': 15
                },
                'pasteType': 'PASTE_FORMAT',
                'pasteOrientation': 'NORMAL'
            }
        })
        
        # B. Set Row Heights: 42px for ambig (rows 0, 2 of block), 88px for disambig (rows 1, 3 of block)
        # ambig neg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': start_row, 'endIndex': start_row + 1},
                'properties': {'pixelSize': 42},
                'fields': 'pixelSize'
            }
        })
        # disambig neg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': start_row + 1, 'endIndex': start_row + 2},
                'properties': {'pixelSize': 88},
                'fields': 'pixelSize'
            }
        })
        # ambig nonneg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': start_row + 2, 'endIndex': start_row + 3},
                'properties': {'pixelSize': 42},
                'fields': 'pixelSize'
            }
        })
        # disambig nonneg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': start_row + 3, 'endIndex': start_row + 4},
                'properties': {'pixelSize': 88},
                'fields': 'pixelSize'
            }
        })

# --- STEP 3: EXPAND CONDITIONAL FORMATTING TO ROWS 1 TO 961 ---
# Fetch current rules
sheet_meta = execute_with_retry(service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets(properties(sheetId,title),conditionalFormats)'
))

for s in sheet_meta['sheets']:
    sid = s['properties']['sheetId']
    if sid in (POL_ENG_ID, POL_BEN_ID):
        cfs = s.get('conditionalFormats', [])
        for idx in range(len(cfs)-1, -1, -1):
            requests.append({'deleteConditionalFormatRule': {'sheetId': sid, 'index': idx}})

for sid in (POL_ENG_ID, POL_BEN_ID):
    # Rule 0: Col C ambig -> Purple
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 961, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'ambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.9490196, 'green': 0.9098039, 'blue': 1},
                        'textFormat': {'foregroundColor': {'red': 0.41960785, 'green': 0.12941177, 'blue': 0.65882355}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    })
    # Rule 1: Col C disambig -> Green
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 961, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'disambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.9882353, 'blue': 0.9098039},
                        'textFormat': {'foregroundColor': {'red': 0.08627451, 'green': 0.4, 'blue': 0.2}, 'bold': True}
                    }
                }
            },
            'index': 1
        }
    })
    # Rule 2: Col D neg -> Pink
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 961, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'neg'}]},
                    'format': {
                        'backgroundColor': {'red': 1.0, 'green': 0.8862745, 'blue': 0.8980392},
                        'textFormat': {'foregroundColor': {'red': 0.61960787, 'green': 0.06666667, 'blue': 0.21960784}, 'bold': True}
                    }
                }
            },
            'index': 2
        }
    })
    # Rule 3: Col D nonneg -> Light Blue
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 961, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'nonneg'}]},
                    'format': {
                        'backgroundColor': {'red': 0.8784314, 'green': 0.9490196, 'blue': 1.0},
                        'textFormat': {'foregroundColor': {'red': 0.007843138, 'green': 0.40784314, 'blue': 0.627451}, 'bold': True}
                    }
                }
            },
            'index': 3
        }
    })
    # Rule 4: Col E NA -> Light Blue
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 961, 'startColumnIndex': 4, 'endColumnIndex': 5}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'NA'}]},
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.91764706, 'blue': 1.0},
                        'textFormat': {'foregroundColor': {'red': 0.11764706, 'green': 0.24705882, 'blue': 0.6862745}, 'bold': True}
                    }
                }
            },
            'index': 4
        }
    })

print(f"Total formatting requests prepared: {len(requests)}")

# Execute in chunks of 150
CHUNK_SIZE = 150
for chunk_start in range(0, len(requests), CHUNK_SIZE):
    chunk = requests[chunk_start:chunk_start + CHUNK_SIZE]
    print(f"Executing batch chunk {chunk_start // CHUNK_SIZE + 1} ({len(chunk)} requests)...")
    batch_req = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': chunk}
    )
    execute_with_retry(batch_req)

print("SUCCESS: Google Sheets expanded and formatted for all 960 records!")

# --- STEP 4: SYNC LOCAL JSONL PRODUCTION DATASETS ---
print("Syncing local production JSONL datasets (all 960 records)...")

# Load Q1-Q5 rows (from backup)
with open('Dataset_ BanglaBBQ_Old/Politics/backup_q1_q5_eng_240.json', 'r', encoding='utf-8') as f:
    headers_eng = f.readline() # or json
    f.seek(0)
    q1_q5_eng_list = json.load(f)[1:] # drop header row

with open('Dataset_ BanglaBBQ_Old/Politics/backup_q1_q5_ben_240.json', 'r', encoding='utf-8') as f:
    q1_q5_ben_list = json.load(f)[1:]

full_eng_960 = q1_q5_eng_list + new_eng_records
full_ben_960 = q1_q5_ben_list + new_ben_records

assert len(full_eng_960) == 960
assert len(full_ben_960) == 960

def row_to_dict(r):
    return {
        "example_id": int(r[0]),
        "question_index": int(r[1]),
        "context_condition": r[2],
        "question_polarity": r[3],
        "type": r[4],
        "context": r[5],
        "question": r[6],
        "ans0": r[7],
        "ans1": r[8],
        "ans2": r[9],
        "label": int(r[10]),
        "answer_info": json.loads(r[11]),
        "additional_metadata": json.loads(r[12]),
        "category": r[13],
        "id": int(r[14])
    }

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "w", encoding="utf-8") as f:
    for r in full_eng_960:
        f.write(json.dumps(row_to_dict(r), ensure_ascii=False) + "\n")

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "w", encoding="utf-8") as f:
    for r in full_ben_960:
        f.write(json.dumps(row_to_dict(r), ensure_ascii=False) + "\n")

print("Local JSONL files successfully updated with all 960 records!")
