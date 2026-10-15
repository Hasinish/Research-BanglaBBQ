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

AGE_ENG_ID = 0
AGE_BEN_ID = 1006819770
POL_ENG_ID = 1888499205
POL_BEN_ID = 2128232344

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

# 1. Fetch exact conditional formatting rules from PakBBQ_ENG_Age
get_req = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=['PakBBQ_ENG_Age!A1:O5', 'BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics'],
    fields='sheets(properties(sheetId,title),conditionalFormats)'
)
sheet_meta = execute_with_retry(get_req)

pol_eng_cfs = []
pol_ben_cfs = []
for s in sheet_meta['sheets']:
    sid = s['properties']['sheetId']
    if sid == POL_ENG_ID:
        pol_eng_cfs = s.get('conditionalFormats', [])
    elif sid == POL_BEN_ID:
        pol_ben_cfs = s.get('conditionalFormats', [])

print(f"Current conditional format rules in Politics ENG: {len(pol_eng_cfs)}, BEN: {len(pol_ben_cfs)}")

requests = []

# --- CLEAR EXISTING CONDITIONAL FORMAT RULES IN POLITICS SHEETS ---
for idx in range(len(pol_eng_cfs) - 1, -1, -1):
    requests.append({'deleteConditionalFormatRule': {'sheetId': POL_ENG_ID, 'index': idx}})
for idx in range(len(pol_ben_cfs) - 1, -1, -1):
    requests.append({'deleteConditionalFormatRule': {'sheetId': POL_BEN_ID, 'index': idx}})

# --- APPLY COPY_PASTE WITH PASTE_FORMAT ---
pairs = [
    (AGE_ENG_ID, POL_ENG_ID, "ENG"),
    (AGE_BEN_ID, POL_BEN_ID, "BEN")
]

for src_id, dst_id, lang in pairs:
    # A. Copy Header format A1:O1
    requests.append({
        'copyPaste': {
            'source': {
                'sheetId': src_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 15
            },
            'destination': {
                'sheetId': dst_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 15
            },
            'pasteType': 'PASTE_FORMAT',
            'pasteOrientation': 'NORMAL'
        }
    })
    
    # B. Apply Age 4-row pattern A2:O5 across all 60 blocks (rows 1 to 241)
    for block_idx in range(60):
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

    # C. Freeze Row 1
    requests.append({
        'updateSheetProperties': {
            'properties': {'sheetId': dst_id, 'gridProperties': {'frozenRowCount': 1}},
            'fields': 'gridProperties.frozenRowCount'
        }
    })

    # D. Match Exact Column Widths from Age
    COLUMN_WIDTHS = [
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
        (14, 75),  # id
    ]
    for col_idx, width in COLUMN_WIDTHS:
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': dst_id,
                    'dimension': 'COLUMNS',
                    'startIndex': col_idx,
                    'endIndex': col_idx + 1
                },
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })

    # E. Header row height: 28px
    requests.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': dst_id,
                'dimension': 'ROWS',
                'startIndex': 0,
                'endIndex': 1
            },
            'properties': {'pixelSize': 28},
            'fields': 'pixelSize'
        }
    })

    # F. Adjust Row Heights for All 60 4-Row Blocks
    # Row 0 of block (ambig, 2 lines context): 42px
    # Row 1 of block (disambig, 5 lines context): 88px
    # Row 2 of block (ambig, 2 lines context): 42px
    # Row 3 of block (disambig, 5 lines context): 88px
    for block_idx in range(60):
        b_start = 1 + block_idx * 4
        # ambig neg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': b_start, 'endIndex': b_start + 1},
                'properties': {'pixelSize': 42},
                'fields': 'pixelSize'
            }
        })
        # disambig neg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': b_start + 1, 'endIndex': b_start + 2},
                'properties': {'pixelSize': 88},
                'fields': 'pixelSize'
            }
        })
        # ambig nonneg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': b_start + 2, 'endIndex': b_start + 3},
                'properties': {'pixelSize': 42},
                'fields': 'pixelSize'
            }
        })
        # disambig nonneg
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': dst_id, 'dimension': 'ROWS', 'startIndex': b_start + 3, 'endIndex': b_start + 4},
                'properties': {'pixelSize': 88},
                'fields': 'pixelSize'
            }
        })

    # G. Conditional Formatting Rules (Matching Age Exactly)
    # Rule 0: Col C ambig -> Purple
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': dst_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 2, 'endColumnIndex': 3}],
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
                'ranges': [{'sheetId': dst_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 2, 'endColumnIndex': 3}],
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
                'ranges': [{'sheetId': dst_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 3, 'endColumnIndex': 4}],
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
                'ranges': [{'sheetId': dst_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 3, 'endColumnIndex': 4}],
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
    # Rule 4: Col E NA -> Light Blue (Matching DT in Age)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': dst_id, 'startRowIndex': 1, 'endRowIndex': 241, 'startColumnIndex': 4, 'endColumnIndex': 5}],
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

print(f"Total batch requests prepared: {len(requests)}")

# Execute in chunks of 150 requests to avoid network payload timeouts
CHUNK_SIZE = 150
for chunk_start in range(0, len(requests), CHUNK_SIZE):
    chunk = requests[chunk_start:chunk_start + CHUNK_SIZE]
    print(f"Executing batch chunk {chunk_start // CHUNK_SIZE + 1} ({len(chunk)} requests)...")
    batch_req = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': chunk}
    )
    execute_with_retry(batch_req)

print("SUCCESS: Full Age-matching format applied to BanglaBBQ_ENG_Politics and BanglaBBQ_BEN_Politics!")
