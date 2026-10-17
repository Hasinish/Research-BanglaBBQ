"""
Format BanglaBBQ_ENG_Gender and BanglaBBQ_BEN_Gender to exactly match production specifications.
Replicates:
- Frozen header row (row 1)
- Exact column widths (A-O): [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]
- Header formatting: Navy fill #16213D, bold white text size 10, center/middle alignment, overflow wrapping
- Data row formatting: size 10 Arial, middle vertical alignment, clip wrapping, center alignment for codes/numbers, left alignment for text
- Conditional formatting rules: ambig, disambig, neg, nonneg, DT, NA across rows 2-4697
"""

import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
ENG_SHEET_ID = 1990010101
BEN_SHEET_ID = 1990010102

COL_WIDTHS = [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]

def build_formatting_requests(sheet_id):
    requests = []
    
    # 1. Freeze header row 1
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'gridProperties': {
                    'rowCount': 4697,
                    'columnCount': 15,
                    'frozenRowCount': 1
                }
            },
            'fields': 'gridProperties(rowCount,columnCount,frozenRowCount)'
        }
    })
    
    # 2. Set column widths (A-O)
    for col_idx, width in enumerate(COL_WIDTHS):
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': col_idx,
                    'endIndex': col_idx + 1
                },
                'properties': {
                    'pixelSize': width
                },
                'fields': 'pixelSize'
            }
        })
        
    # 3. Format header row (Row 0, Cols 0-15)
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 15
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {
                        'red': 0.08627451,
                        'green': 0.12941177,
                        'blue': 0.23921569
                    },
                    'horizontalAlignment': 'CENTER',
                    'verticalAlignment': 'MIDDLE',
                    'wrapStrategy': 'OVERFLOW_CELL',
                    'textFormat': {
                        'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                        'fontFamily': 'Arial',
                        'fontSize': 10,
                        'bold': True
                    }
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
        }
    })
    
    # 4. Format all data rows (Rows 1-4697): general font, vertical alignment, and wrapStrategy = CLIP
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 1,
                'endRowIndex': 4697,
                'startColumnIndex': 0,
                'endColumnIndex': 15
            },
            'cell': {
                'userEnteredFormat': {
                    'verticalAlignment': 'MIDDLE',
                    'wrapStrategy': 'CLIP',
                    'textFormat': {
                        'fontFamily': 'Arial',
                        'fontSize': 10,
                        'bold': False
                    }
                }
            },
            'fields': 'userEnteredFormat(verticalAlignment,wrapStrategy,textFormat)'
        }
    })
    
    # 5. Center alignment for numeric/code columns: A (0), B (1), C (2), D (3), E (4), K (10), N (13), O (14)
    center_cols = [0, 1, 2, 3, 4, 10, 13, 14]
    for c in center_cols:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': c,
                    'endColumnIndex': c + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment)'
            }
        })
        
    # 6. Left alignment for text/content columns: F (5), G (6), H (7), I (8), J (9), L (11), M (12)
    left_cols = [5, 6, 7, 8, 9, 11, 12]
    for c in left_cols:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': c,
                    'endColumnIndex': c + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT'
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment)'
            }
        })
        
    # 7. Conditional formatting rules (Rows 1-4697)
    # Rule 1: Col C == 'ambig' -> Lavender (#F2E8FF, text #6B21A8)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 2,
                    'endColumnIndex': 3
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'ambig'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.9490196, 'green': 0.9098039, 'blue': 1},
                        'textFormat': {
                            'foregroundColor': {'red': 0.41960785, 'green': 0.12941177, 'blue': 0.65882355},
                            'bold': True
                        }
                    }
                }
            },
            'index': 0
        }
    })
    
    # Rule 2: Col C == 'disambig' -> Mint (#DBFCE8, text #166633)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 2,
                    'endColumnIndex': 3
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'disambig'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.9882353, 'blue': 0.9098039},
                        'textFormat': {
                            'foregroundColor': {'red': 0.08627451, 'green': 0.4, 'blue': 0.2},
                            'bold': True
                        }
                    }
                }
            },
            'index': 1
        }
    })
    
    # Rule 3: Col D == 'neg' -> Light Red (#FFE2E5, text #9E1138)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 3,
                    'endColumnIndex': 4
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'neg'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 1, 'green': 0.8862745, 'blue': 0.8980392},
                        'textFormat': {
                            'foregroundColor': {'red': 0.61960787, 'green': 0.06666667, 'blue': 0.21960784},
                            'bold': True
                        }
                    }
                }
            },
            'index': 2
        }
    })
    
    # Rule 4: Col D == 'nonneg' -> Light Blue (#E0F2FF, text #0268A0)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 3,
                    'endColumnIndex': 4
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'nonneg'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.8784314, 'green': 0.9490196, 'blue': 1},
                        'textFormat': {
                            'foregroundColor': {'red': 0.007843138, 'green': 0.40784314, 'blue': 0.627451},
                            'bold': True
                        }
                    }
                }
            },
            'index': 3
        }
    })
    
    # Rule 5: Col E == 'DT' -> Periwinkle (#DBEAFE, text #1E3FAF)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 4,
                    'endColumnIndex': 5
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'DT'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.91764706, 'blue': 1},
                        'textFormat': {
                            'foregroundColor': {'red': 0.11764706, 'green': 0.24705882, 'blue': 0.6862745},
                            'bold': True
                        }
                    }
                }
            },
            'index': 4
        }
    })
    
    # Rule 6: Col E == 'NA' -> Periwinkle (#DBEAFE, text #1E3FAF)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 4697,
                    'startColumnIndex': 4,
                    'endColumnIndex': 5
                }],
                'booleanRule': {
                    'condition': {
                        'type': 'TEXT_EQ',
                        'values': [{'userEnteredValue': 'NA'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.85882354, 'green': 0.91764706, 'blue': 1},
                        'textFormat': {
                            'foregroundColor': {'red': 0.11764706, 'green': 0.24705882, 'blue': 0.6862745},
                            'bold': True
                        }
                    }
                }
            },
            'index': 5
        }
    })
    
    return requests

def main():
    print("====================================================================")
    print("STEP 2: APPLYING PRODUCTION FORMATTING TO GENDER WORKSHEETS")
    print("====================================================================")
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    for title, s_id in [('BanglaBBQ_ENG_Gender', ENG_SHEET_ID), ('BanglaBBQ_BEN_Gender', BEN_SHEET_ID)]:
        print(f"\nProcessing '{title}' (Sheet ID: {s_id})...")
        reqs = build_formatting_requests(s_id)
        print(f"  Sending {len(reqs)} formatting requests in batchUpdate...")
        body = {'requests': reqs}
        res = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print(f"  BatchUpdate completed successfully! Total replies: {len(res.get('replies', []))}")
        
    print("\n====================================================================")
    print("PRODUCTION FORMATTING SUCCESSFULLY APPLIED TO BOTH GENDER WORKSHEETS!")
    print("====================================================================")

if __name__ == '__main__':
    main()
