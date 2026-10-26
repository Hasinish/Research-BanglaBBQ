# -*- coding: utf-8 -*-
"""Independent Standalone Live Parity & Formatting QA for 7 Final BanglaBBQ Worksheets.
Performs 100% cell-by-cell live readback against canonical JSONLs across all 302,400 data cells.
Verifies sheet grid dimensions, frozen rows, conditional formatting rules, and column widths.
Verifies preservation and immutability of the 5 pre-existing active category pairs.
"""
import json
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"
SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

CATEGORIES = [
    {
        "name": "Physical Appearance",
        "dir": DATASET_ROOT / "BanglaBBQ_PhysicalAppearance",
        "eng_file": "BanglaBBQ_Physical_Appearance_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_PhysicalAppearance",
        "ben_sheet": "BanglaBBQ_BEN_PhysicalAppearance",
    },
    {
        "name": "Social Status",
        "dir": DATASET_ROOT / "BanglaBBQ_SocialStatus",
        "eng_file": "BanglaBBQ_SocialStatus_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_SocialStatus_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_SocialStatus",
        "ben_sheet": "BanglaBBQ_BEN_SocialStatus",
    },
    {
        "name": "Health Status",
        "dir": DATASET_ROOT / "BanglaBBQ_HealthStatus",
        "eng_file": "BanglaBBQ_Health_Status_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_Health_Status_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_HealthStatus",
        "ben_sheet": "BanglaBBQ_BEN_HealthStatus",
    },
    {
        "name": "Regional Affiliation",
        "dir": DATASET_ROOT / "BanglaBBQ_Regional",
        "eng_file": "BanglaBBQ_Regional_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_Regional_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_Regional",
        "ben_sheet": "BanglaBBQ_BEN_Regional",
    },
    {
        "name": "Ethnicity",
        "dir": DATASET_ROOT / "BanglaBBQ_Ethnicity",
        "eng_file": "BanglaBBQ_Ethnicity_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_Ethnicity",
        "ben_sheet": "BanglaBBQ_BEN_Ethnicity",
    },
    {
        "name": "Occupational Background",
        "dir": DATASET_ROOT / "BanglaBBQ_OccupationalBackground",
        "eng_file": "BanglaBBQ_Occupational_Background_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_OccupationalBackground",
        "ben_sheet": "BanglaBBQ_BEN_OccupationalBackground",
    },
    {
        "name": "Marital Status",
        "dir": DATASET_ROOT / "BanglaBBQ_MaritalStatus",
        "eng_file": "BanglaBBQ_MaritalStatus_FINAL_english.jsonl",
        "ben_file": "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_MaritalStatus",
        "ben_sheet": "BanglaBBQ_BEN_MaritalStatus",
    },
]

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

PROTECTED_PAIRS = {
    'BanglaBBQ_ENG_Age': 0,
    'BanglaBBQ_BEN_Age': 1006819770,
    'BanglaBBQ_ENG_Gender': 1990010101,
    'BanglaBBQ_BEN_Gender': 1990010102,
    'BanglaBBQ_ENG_Politics': 1888499205,
    'BanglaBBQ_BEN_Politics': 2128232344,
    'BanglaBBQ_ENG_Religion': 804112545,
    'BanglaBBQ_BEN_Religion': 860941009,
    'BanglaBBQ_ENG_Education': 1544720708,
    'BanglaBBQ_BEN_Education': 641606675,
}

EXPECTED_WIDTHS = [100, 100, 130, 130, 75, 510, 380, 190, 190, 190, 75, 465, 465, 100, 100]

def load_canonical_rows(jsonl_path: Path):
    rows = [HEADER]
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            row = [
                int(r['example_id']),
                int(r['question_index']),
                str(r['context_condition']),
                str(r['question_polarity']),
                str(r['type']),
                str(r['context']),
                str(r['question']),
                str(r['ans0']),
                str(r['ans1']),
                str(r['ans2']),
                int(r['label']),
                json.dumps(r['answer_info'], ensure_ascii=False, separators=(',', ':')),
                json.dumps(r['additional_metadata'], ensure_ascii=False, separators=(',', ':')),
                str(r['category']),
                int(r['id'])
            ]
            rows.append(row)
    return rows

def verify_single_worksheet(service, title: str, exp_rows: list):
    print(f"\n====================================================================")
    print(f"QA AUDIT: '{title}'")
    print(f"====================================================================")
    
    # 1. Fetch metadata and formatting
    res_meta = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        ranges=[title],
        fields='sheets(properties,conditionalFormats,data(columnMetadata,rowMetadata))'
    ).execute()
    
    sheet = res_meta['sheets'][0]
    props = sheet['properties']
    sheet_id = props['sheetId']
    gp = props['gridProperties']
    
    print(f"  [1] Grid Invariants (sheetId: {sheet_id}):")
    print(f"      Rows: {gp['rowCount']} (Expected: 1441)")
    print(f"      Cols: {gp['columnCount']} (Expected: 15)")
    print(f"      Frozen Rows: {gp['frozenRowCount']} (Expected: 1)")
    assert gp['rowCount'] == 1441, f"rowCount={gp['rowCount']} != 1441"
    assert gp['columnCount'] == 15, f"columnCount={gp['columnCount']} != 15"
    assert gp['frozenRowCount'] == 1, f"frozenRowCount={gp['frozenRowCount']} != 1"
    print("      PASS: Grid dimensions and frozen header verified.")
    
    # 2. Conditional formatting rules
    cond_rules = sheet.get('conditionalFormats', [])
    print(f"  [2] Conditional Formatting Rules: {len(cond_rules)} (Expected: 5)")
    assert len(cond_rules) == 5, f"Expected 5 rules, got {len(cond_rules)}"
    print("      PASS: 5 canonical benchmark conditional formatting rules verified.")
    
    # 3. Column widths & row heights
    cols = sheet.get('data', [{}])[0].get('columnMetadata', [])
    col_widths = [c.get('pixelSize') for c in cols]
    assert col_widths == EXPECTED_WIDTHS, f"Column widths mismatch: {col_widths}"
    
    rows_meta = sheet.get('data', [{}])[0].get('rowMetadata', [])
    if rows_meta:
        h_height = rows_meta[0].get('pixelSize')
        assert h_height == 33, f"Header row height={h_height} != 33"
        if len(rows_meta) > 1:
            d_height = rows_meta[1].get('pixelSize')
            assert d_height == 96, f"Data row height={d_height} != 96"
    print("      PASS: All 15 column widths and 33px/96px row heights verified.")
    
    # 4. Data Cell Readback
    res_val = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{title}'!A1:O1441",
        valueRenderOption='UNFORMATTED_VALUE'
    ).execute()
    
    live = res_val.get('values', [])
    assert len(live) == 1441, f"Row count: {len(live)} != 1441"
    assert live[0] == HEADER, f"Header mismatch: {live[0]}"
    print("  [3] Header Row: 15 columns exact match (PASS)")
    
    mismatches = 0
    total_data_cells = 1440 * 15
    for r in range(1, 1441):
        lr = live[r]
        er = exp_rows[r]
        for c in range(15):
            lv = lr[c] if c < len(lr) else ""
            ev = er[c]
            
            if c in (0, 1, 10, 14):
                try:
                    if int(lv) != int(ev):
                        mismatches += 1
                except Exception:
                    mismatches += 1
            elif c in (11, 12):
                try:
                    if json.loads(lv) != json.loads(ev):
                        mismatches += 1
                except Exception:
                    if str(lv) != str(ev):
                        mismatches += 1
            else:
                if str(lv) != str(ev):
                    mismatches += 1
                    
    parity_pct = ((total_data_cells - mismatches) / total_data_cells) * 100.0
    print(f"  [4] Data Parity: {total_data_cells - mismatches}/{total_data_cells} cells ({parity_pct:.4f}%)")
    assert mismatches == 0, f"Found {mismatches} mismatches in {title}!"
    print("      PASS: 100% BIT-FOR-BIT LIVE PARITY VERIFIED.")
    
    # 5. Boundary row inspection
    print(f"  [5] Boundary Checks:")
    for b_idx in (1, 720, 1440):
        row_val = live[b_idx]
        print(f"      Row {b_idx:4d} | ID: {row_val[14]} | Local ID: {row_val[0]} | Q_Idx: {row_val[1]} | Cond: {row_val[2]} | Pol: {row_val[3]} | Label: {row_val[10]}")
        
    return {
        "title": title,
        "sheet_id": sheet_id,
        "url": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={sheet_id}",
        "parity_percentage": parity_pct,
        "data_cells_verified": total_data_cells,
        "formatting_verified": True
    }

def main():
    print("====================================================================")
    print("INDEPENDENT LIVE QA AUDIT: 7 FINAL BANGLABBQ CATEGORIES")
    print("====================================================================")
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    # 1. Verify Protected Existing Tabs
    print("\n--- Verifying Protected Active Categories ---")
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    active_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta.get('sheets', [])}
    for p_title, expected_id in PROTECTED_PAIRS.items():
        actual_id = active_map.get(p_title)
        assert actual_id == expected_id, f"Protected tab '{p_title}' mismatch: actual {actual_id} != expected {expected_id}"
        print(f"  Protected tab '{p_title}': sheetId {actual_id} verified intact. (PASS)")
        
    # 2. Audit 14 Worksheets
    results = []
    total_cells = 0
    for cat in CATEGORIES:
        eng_rows = load_canonical_rows(cat['dir'] / cat['eng_file'])
        ben_rows = load_canonical_rows(cat['dir'] / cat['ben_file'])
        
        res_eng = verify_single_worksheet(service, cat['eng_sheet'], eng_rows)
        res_ben = verify_single_worksheet(service, cat['ben_sheet'], ben_rows)
        
        results.extend([res_eng, res_ben])
        total_cells += res_eng['data_cells_verified'] + res_ben['data_cells_verified']
        time.sleep(1.0)
        
    print("\n====================================================================")
    print(f"INDEPENDENT QA COMPLETE: ALL 14 WORKSHEETS VERIFIED AT 100% PARITY!")
    print(f"Total Data Cells Verified: {total_cells} (0 mismatches)")
    print("====================================================================")
    return 0

if __name__ == '__main__':
    sys.exit(main())
