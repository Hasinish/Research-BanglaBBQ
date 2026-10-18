"""
Format BanglaBBQ_ENG_Gender and BanglaBBQ_BEN_Gender to exactly match production specifications.
Replicates:
- Frozen header row (row 1)
- Header row height: 33px
- Data rows height (rows 2-4697): 96px
- Exact column widths (A-O): [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]
- Header formatting: Navy fill #16213D, bold white text size 10, center/middle alignment, overflow wrapping
- Data row formatting: size 10 Arial, middle vertical alignment:
    - Columns A-E: CENTER, CLIP
    - Columns F-J (context, question, ans0, ans1, ans2): LEFT, WRAP
    - Column K (label): CENTER, CLIP
    - Columns L-M (answer_info, additional_metadata): LEFT, CLIP
    - Columns N-O (category, id): CENTER, CLIP
- Conditional formatting rules: exactly 6 rules (ambig, disambig, neg, nonneg, DT, NA)
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
    
    # 1. Freeze header row 1 & grid properties
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
    
    # 2. Row height for header row (Row 0 -> 33 px)
    requests.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': 0,
                'endIndex': 1
            },
            'properties': {
                'pixelSize': 33
            },
            'fields': 'pixelSize'
        }
    })
    
    # 3. Row height for all data rows (Rows 1-4697 -> 96 px)
    requests.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': 1,
                'endIndex': 4697
            },
            'properties': {
                'pixelSize': 96
            },
            'fields': 'pixelSize'
        }
    })
    
    # 4. Set column widths (A-O)
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
        
    # 5. Format header row (Row 0, Cols 0-15)
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
    
    # 6. Center alignment and CLIP for columns: A (0), B (1), C (2), D (3), E (4), K (10), N (13), O (14)
    center_clip_cols = [0, 1, 2, 3, 4, 10, 13, 14]
    for c in center_clip_cols:
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
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'CLIP',
                        'textFormat': {
                            'fontFamily': 'Arial',
                            'fontSize': 10,
                            'bold': False
                        }
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    # 7. Left alignment and WRAP for text/content columns: F (5), G (6), H (7), I (8), J (9)
    wrap_text_cols = [5, 6, 7, 8, 9]
    for c in wrap_text_cols:
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
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {
                            'fontFamily': 'Arial',
                            'fontSize': 10,
                            'bold': False
                        }
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    # 8. Left alignment and CLIP for metadata columns: L (11), M (12)
    meta_clip_cols = [11, 12]
    for c in meta_clip_cols:
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
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'CLIP',
                        'textFormat': {
                            'fontFamily': 'Arial',
                            'fontSize': 10,
                            'bold': False
                        }
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)'
            }
        })
        
    return requests

def verify_live_formatting(service):
    print("\n--- Verifying Live Formatting Properties ---")
    res = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        ranges=['BanglaBBQ_ENG_Gender!A1:O2', 'BanglaBBQ_BEN_Gender!A1:O2'],
        fields='sheets(properties.title,conditionalFormats,data.rowMetadata,data.columnMetadata,data.rowData.values.userEnteredFormat)'
    ).execute()
    
    all_ok = True
    for s in res['sheets']:
        title = s['properties']['title']
        cfs = s.get('conditionalFormats', [])
        data = s['data'][0]
        row_meta = data.get('rowMetadata', [])
        col_meta = data.get('columnMetadata', [])
        row2_values = data.get('rowData', [{}, {}])[1].get('values', [])
        wraps = [v.get('userEnteredFormat', {}).get('wrapStrategy') for v in row2_values]
        
        h_h = row_meta[0].get('pixelSize') if len(row_meta) > 0 else None
        d_h = row_meta[1].get('pixelSize') if len(row_meta) > 1 else None
        widths = [c.get('pixelSize') for c in col_meta[:15]]
        
        print(f"\nWorksheet: {title}")
        print(f"  Header row height: {h_h} px (Expected: 33)")
        print(f"  Data row height: {d_h} px (Expected: 96)")
        print(f"  Column widths: {widths}")
        print(f"  Row 2 wrapStrategies: {wraps}")
        print(f"  Conditional format rules: {len(cfs)}")
        
        if h_h != 33 or d_h != 96:
            print(f"  FAIL: Row heights incorrect on {title}")
            all_ok = False
        if widths != COL_WIDTHS:
            print(f"  FAIL: Column widths incorrect on {title}")
            all_ok = False
        expected_wraps = ['CLIP', 'CLIP', 'CLIP', 'CLIP', 'CLIP', 'WRAP', 'WRAP', 'WRAP', 'WRAP', 'WRAP', 'CLIP', 'CLIP', 'CLIP', 'CLIP', 'CLIP']
        if wraps != expected_wraps:
            print(f"  FAIL: Wrap strategies incorrect on {title}")
            all_ok = False
        if len(cfs) != 6:
            print(f"  FAIL: Expected 6 conditional formatting rules on {title}, found {len(cfs)}")
            all_ok = False
            
    if all_ok:
        print("\nALL FORMATTING PROPERTIES VERIFIED AND EXACTLY MATCH PRODUCTION STANDARD!")
    return all_ok

def main():
    print("====================================================================")
    print("PHASE 7: APPLYING PRODUCTION FORMATTING TO GENDER WORKSHEETS")
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
        
    ok = verify_live_formatting(service)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()

