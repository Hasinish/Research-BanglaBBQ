import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

# 1. Check existing sheets
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
existing_sheets = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
print("Existing sheets:", existing_sheets)

tabs_to_create = [
    {
        'title': 'BanglaBBQ_ENG_Politics',
        'file': 'Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl',
        'desc': 'English Politics Benchmark'
    },
    {
        'title': 'BanglaBBQ_BEN_Politics',
        'file': 'Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl',
        'desc': 'Bengali Politics Benchmark'
    }
]

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

for tab in tabs_to_create:
    title = tab['title']
    jsonl_path = tab['file']
    
    # If sheet already exists, delete it first to ensure a completely clean slate
    if title in existing_sheets:
        print(f"Sheet '{title}' exists. Deleting...")
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': [{'deleteSheet': {'sheetId': existing_sheets[title]}}]}
        ).execute()

    # Create sheet
    add_res = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': [{'addSheet': {'properties': {'title': title}}}]}
    ).execute()
    sheet_id = add_res['replies'][0]['addSheet']['properties']['sheetId']
    print(f"Created sheet '{title}' with ID {sheet_id}")

    # Read and prepare rows
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f if line.strip()]

    rows = [headers]
    for r in records:
        row = [
            str(r.get('example_id', '')),
            str(r.get('question_index', '')),
            str(r.get('context_condition', '')),
            str(r.get('question_polarity', '')),
            str(r.get('type', '')),
            str(r.get('context', '')),
            str(r.get('question', '')),
            str(r.get('ans0', '')),
            str(r.get('ans1', '')),
            str(r.get('ans2', '')),
            str(r.get('label', '')),
            json.dumps(r.get('answer_info', {}), ensure_ascii=False),
            json.dumps(r.get('additional_metadata', {}), ensure_ascii=False),
            str(r.get('category', '')),
            str(r.get('id', ''))
        ]
        rows.append(row)

    total_rows = len(rows)
    print(f"Writing {total_rows} rows to '{title}'...")
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1",
        valueInputOption='USER_ENTERED',
        body={'values': rows}
    ).execute()

    # Prepare styling requests
    requests = [
        # Header formatting (Row 0)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.09, 'green': 0.13, 'blue': 0.24}, # #17223B
                        'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'bold': True, 'fontSize': 10},
                        'verticalAlignment': 'MIDDLE',
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat.backgroundColor,userEnteredFormat.textFormat,userEnteredFormat.verticalAlignment,userEnteredFormat.horizontalAlignment'
            }
        },
        # Freeze row 1
        {
            'updateSheetProperties': {
                'properties': {'sheetId': sheet_id, 'gridProperties': {'frozenRowCount': 1}},
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Middle vertical alignment across all data cells
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 0, 'endColumnIndex': 15},
                'cell': {'userEnteredFormat': {'verticalAlignment': 'MIDDLE'}},
                'fields': 'userEnteredFormat.verticalAlignment'
            }
        },
        # Center alignment for metadata columns (0 to 5: example_id, question_index, condition, polarity, type)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 0, 'endColumnIndex': 5},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        },
        # Text Wrap and Left Align for context, question, ans0, ans1, ans2 (Cols 5 to 10)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 5, 'endColumnIndex': 10},
                'cell': {'userEnteredFormat': {'wrapStrategy': 'WRAP', 'horizontalAlignment': 'LEFT'}},
                'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.horizontalAlignment'
            }
        },
        # Center align for label (Col 10)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 10, 'endColumnIndex': 11},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        },
        # CLIP and Left Align for JSON columns (Cols 11, 12: answer_info, additional_metadata)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 11, 'endColumnIndex': 13},
                'cell': {'userEnteredFormat': {'wrapStrategy': 'CLIP', 'horizontalAlignment': 'LEFT'}},
                'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.horizontalAlignment'
            }
        },
        # Center align for category, id (Cols 13, 14)
        {
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 13, 'endColumnIndex': 15},
                'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'wrapStrategy': 'CLIP'}},
                'fields': 'userEnteredFormat.horizontalAlignment,userEnteredFormat.wrapStrategy'
            }
        }
    ]

    # Set Column Widths
    for idx, width in col_widths:
        requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': idx, 'endIndex': idx + 1},
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })

    # Add Color Badges
    # Col 2: context_condition (ambig / disambig)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'ambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.95, 'green': 0.91, 'blue': 1.0}, # #F3E8FF
                        'textFormat': {'foregroundColor': {'red': 0.42, 'green': 0.13, 'blue': 0.66}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    })
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'disambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.86, 'green': 0.99, 'blue': 0.91}, # #DCFCE7
                        'textFormat': {'foregroundColor': {'red': 0.09, 'green': 0.40, 'blue': 0.20}, 'bold': True}
                    }
                }
            },
            'index': 1
        }
    })

    # Col 3: question_polarity (neg / nonneg)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'neg'}]},
                    'format': {
                        'backgroundColor': {'red': 1.0, 'green': 0.89, 'blue': 0.90}, # #FFE4E6
                        'textFormat': {'foregroundColor': {'red': 0.62, 'green': 0.07, 'blue': 0.22}, 'bold': True}
                    }
                }
            },
            'index': 2
        }
    })
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'nonneg'}]},
                    'format': {
                        'backgroundColor': {'red': 0.88, 'green': 0.95, 'blue': 1.0}, # #E0F2FE
                        'textFormat': {'foregroundColor': {'red': 0.01, 'green': 0.41, 'blue': 0.63}, 'bold': True}
                    }
                }
            },
            'index': 3
        }
    })

    # Col 4: type (NA)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': total_rows, 'startColumnIndex': 4, 'endColumnIndex': 5}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'NA'}]},
                    'format': {
                        'backgroundColor': {'red': 0.93, 'green': 0.91, 'blue': 1.0}, # #EDE9FE
                        'textFormat': {'foregroundColor': {'red': 0.36, 'green': 0.13, 'blue': 0.71}, 'bold': True}
                    }
                }
            },
            'index': 4
        }
    })

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    print(f"SUCCESS: Sheet '{title}' created, populated, and fully styled!")

print("\nALL POLITICS SHEETS COMPLETED SUCCESSFULLY!")
