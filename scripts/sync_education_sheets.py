# -*- coding: utf-8 -*-
"""Synchronize BanglaBBQ Educational Background datasets to Google Sheets.
Creates/updates:
  - BanglaBBQ_ENG_Education (sheetId: auto-created or reused)
  - BanglaBBQ_BEN_Education (sheetId: auto-created or reused)
Applies production formatting (33px/96px row heights, exact widths, wrap/clip rules, frozen header).
Performs 100% cell-by-cell live readback verification across all 43,200 data cells per language.
"""
import json
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

BASE = ROOT / "Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground"
if not BASE.exists():
    BASE = ROOT / "BanglaBBQ_EducationalBackground"
ENG_JSONL = BASE / "banglabbq_education_english.jsonl"
BEN_JSONL = BASE / "banglabbq_education_bengali.jsonl"

COL_WIDTHS = [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]
HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

def load_records_as_rows(jsonl_path):
    rows = [HEADER]
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            row = [
                str(r['example_id']),
                str(r['question_index']),
                r['context_condition'],
                r['question_polarity'],
                r['type'],
                r['context'],
                r['question'],
                r['ans0'],
                r['ans1'],
                r['ans2'],
                str(r['label']),
                json.dumps(r['answer_info'], ensure_ascii=False, separators=(',', ':')),
                json.dumps(r['additional_metadata'], ensure_ascii=False, separators=(',', ':')),
                r['category'],
                str(r['id'])
            ]
            rows.append(row)
    return rows

def ensure_worksheets(service):
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
    
    eng_title = 'BanglaBBQ_ENG_Education'
    ben_title = 'BanglaBBQ_BEN_Education'
    
    add_reqs = []
    if eng_title not in existing:
        add_reqs.append({
            'addSheet': {
                'properties': {
                    'title': eng_title,
                    'gridProperties': {
                        'rowCount': 2881,
                        'columnCount': 15,
                        'frozenRowCount': 1
                    }
                }
            }
        })
    if ben_title not in existing:
        add_reqs.append({
            'addSheet': {
                'properties': {
                    'title': ben_title,
                    'gridProperties': {
                        'rowCount': 2881,
                        'columnCount': 15,
                        'frozenRowCount': 1
                    }
                }
            }
        })
        
    if add_reqs:
        print(f"Creating missing worksheets ({len(add_reqs)})...")
        res = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': add_reqs}
        ).execute()
        for r in res.get('replies', []):
            p = r['addSheet']['properties']
            existing[p['title']] = p['sheetId']
            print(f"  Created '{p['title']}' with Sheet ID: {p['sheetId']}")
            
    return existing[eng_title], existing[ben_title]

def apply_formatting(service, sheet_id, src_religion_id=804112545):
    print(f"Applying canonical production formatting to sheetId {sheet_id}...")
    reqs = []
    
    # 1. Grid Properties: 2881 rows, 15 columns, frozen row 1
    reqs.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'gridProperties': {
                    'rowCount': 2881,
                    'columnCount': 15,
                    'frozenRowCount': 1
                }
            },
            'fields': 'gridProperties(rowCount,columnCount,frozenRowCount)'
        }
    })
    
    # 2. Row height: Header row 0 -> 33px
    reqs.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': 0,
                'endIndex': 1
            },
            'properties': {'pixelSize': 33},
            'fields': 'pixelSize'
        }
    })
    
    # 3. Row height: Data rows 1-2881 -> 96px
    reqs.append({
        'updateDimensionProperties': {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'startIndex': 1,
                'endIndex': 2881
            },
            'properties': {'pixelSize': 96},
            'fields': 'pixelSize'
        }
    })
    
    # 4. Column widths (A-O)
    for col_idx, width in enumerate(COL_WIDTHS):
        reqs.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': col_idx,
                    'endIndex': col_idx + 1
                },
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })
        
    # 5. Header row format: Navy fill #16213D, bold white text size 10, center/middle
    reqs.append({
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
    
    # 6. Data rows: Center/Clip for A-E (0-4), K (10), N-O (13-14)
    center_clip_cols = [0, 1, 2, 3, 4, 10, 13, 14]
    for c in center_clip_cols:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2881,
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
        
    # 7. Data rows: Left/Wrap for F-J (5-9)
    wrap_cols = [5, 6, 7, 8, 9]
    for c in wrap_cols:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2881,
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
        
    # 8. Data rows: Left/Clip for L-M (11-12)
    meta_cols = [11, 12]
    for c in meta_cols:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2881,
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
        
    # 9. Copy conditional formatting and block styles from Religion (804112545)
    # Religion has 5 canonical conditional formatting rules and 4-row alternating styling
    if src_religion_id:
        reqs.append({
            'copyPaste': {
                'source': {
                    'sheetId': src_religion_id,
                    'startRowIndex': 1,
                    'endRowIndex': 5,
                    'startColumnIndex': 0,
                    'endColumnIndex': 15
                },
                'destination': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2881,
                    'startColumnIndex': 0,
                    'endColumnIndex': 15
                },
                'pasteType': 'PASTE_FORMAT',
                'pasteOrientation': 'NORMAL'
            }
        })
        
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': reqs}
    ).execute()
    print(f"Formatting applied successfully to sheetId {sheet_id}!")

def upload_data(service, title, rows):
    print(f"Uploading {len(rows)} rows to {title}...")
    chunk_size = 500
    for start in range(0, len(rows), chunk_size):
        end = min(start + chunk_size, len(rows))
        chunk = rows[start:end]
        cell_range = f"{title}!A{start + 1}:O{end}"
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=cell_range,
            valueInputOption='USER_ENTERED',
            body={'values': chunk}
        ).execute()
        print(f"  Uploaded rows {start + 1} to {end}...")
        time.sleep(0.5)
    print(f"Upload to {title} complete!")

def verify_live_parity(service, title, expected_rows):
    print(f"\n--- Verifying Live Parity for {title} ---")
    res = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{title}!A1:O2881"
    ).execute()
    live_rows = res.get('values', [])
    
    assert len(live_rows) == len(expected_rows), f"Row count mismatch: live={len(live_rows)} vs exp={len(expected_rows)}"
    print(f"  Row count verified: {len(live_rows)} rows (PASS)")
    
    # Verify header
    assert live_rows[0] == HEADER, f"Header mismatch: {live_rows[0]}"
    print("  Header row verified: 15 columns (PASS)")
    
    # Cell-by-cell verification across all 43,200 data cells
    mismatches = 0
    total_data_cells = 2880 * 15
    for r_idx in range(1, 2881):
        live_r = live_rows[r_idx]
        exp_r = expected_rows[r_idx]
        for c_idx in range(15):
            val_live = live_r[c_idx] if c_idx < len(live_r) else ""
            val_exp = exp_r[c_idx]
            
            # For JSON columns L and M, compare normalized JSON
            if c_idx in (11, 12):
                try:
                    j_live = json.loads(val_live)
                    j_exp = json.loads(val_exp)
                    if j_live != j_exp:
                        mismatches += 1
                        if mismatches <= 3:
                            print(f"    Mismatch at row {r_idx}, col {c_idx}: live={val_live} vs exp={val_exp}")
                except Exception:
                    if val_live != val_exp:
                        mismatches += 1
            else:
                if val_live != val_exp:
                    mismatches += 1
                    if mismatches <= 3:
                        print(f"    Mismatch at row {r_idx}, col {c_idx}: live={val_live} vs exp={val_exp}")
                        
    if mismatches == 0:
        print(f"  100% BIT-FOR-BIT LIVE PARITY VERIFIED across all {total_data_cells} data cells! (0 mismatches) (PASS)")
        return True
    else:
        print(f"  FAIL: Found {mismatches} cell mismatches!")
        return False

def main():
    print("====================================================================")
    print("GOOGLE SHEETS SYNCHRONIZATION: BANGLABBQ EDUCATIONAL BACKGROUND")
    print("====================================================================")
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    eng_rows = load_records_as_rows(ENG_JSONL)
    ben_rows = load_records_as_rows(BEN_JSONL)
    
    eng_sheet_id, ben_sheet_id = ensure_worksheets(service)
    
    # Upload English
    upload_data(service, 'BanglaBBQ_ENG_Education', eng_rows)
    apply_formatting(service, eng_sheet_id)
    
    # Upload Bengali
    upload_data(service, 'BanglaBBQ_BEN_Education', ben_rows)
    apply_formatting(service, ben_sheet_id)
    
    # Readback verification
    eng_ok = verify_live_parity(service, 'BanglaBBQ_ENG_Education', eng_rows)
    ben_ok = verify_live_parity(service, 'BanglaBBQ_BEN_Education', ben_rows)
    
    if eng_ok and ben_ok:
        print("\n====================================================================")
        print("GOOGLE SHEETS INTEGRATION & 100% LIVE PARITY VERIFICATION COMPLETE")
        print(f"  BanglaBBQ_ENG_Education (sheetId: {eng_sheet_id}): 2,881 rows, 43,200 data cells verified")
        print(f"  BanglaBBQ_BEN_Education (sheetId: {ben_sheet_id}): 2,881 rows, 43,200 data cells verified")
        print("====================================================================")
        return 0
    else:
        print("\nFAIL: Parity verification failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
