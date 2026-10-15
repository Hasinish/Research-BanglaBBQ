import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

sheets_to_check = [
    ('PakBBQ_ENG_Age', 'BanglaBBQ_ENG_Politics'),
    ('BanglaBBQ_BEN_Age', 'BanglaBBQ_BEN_Politics')
]

print("==================================================")
print("COMPREHENSIVE AGE VS POLITICS FORMAT VERIFICATION")
print("==================================================")

for age_title, pol_title in sheets_to_check:
    print(f"\nComparing {age_title} (Reference) vs {pol_title} (Target):")
    
    # 1. Fetch metadata (columns, conditional formats, frozen rows)
    res = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=[f'{age_title}!A1:O241', f'{pol_title}!A1:O241'],
        fields='sheets(properties(title,gridProperties),conditionalFormats,data(columnMetadata))'
    ).execute()
    
    age_sheet = next(s for s in res['sheets'] if s['properties']['title'] == age_title)
    pol_sheet = next(s for s in res['sheets'] if s['properties']['title'] == pol_title)
    
    age_cols = [c.get('pixelSize') for c in age_sheet['data'][0].get('columnMetadata', [])[:15]]
    pol_cols = [c.get('pixelSize') for c in pol_sheet['data'][0].get('columnMetadata', [])[:15]]
    
    print(f"  Column Widths Match: {age_cols == pol_cols}")
    if age_cols != pol_cols:
        print(f"    Age cols: {age_cols}")
        print(f"    Pol cols: {pol_cols}")
        
    age_frozen = age_sheet['properties']['gridProperties'].get('frozenRowCount')
    pol_frozen = pol_sheet['properties']['gridProperties'].get('frozenRowCount')
    print(f"  Frozen Row Count: Age={age_frozen}, Pol={pol_frozen} -> Match: {age_frozen == pol_frozen}")
    
    # 2. Check Conditional Formatting Rules in Politics
    pol_cfs = pol_sheet.get('conditionalFormats', [])
    print(f"  Politics Conditional Format Rules Count: {len(pol_cfs)} (Expected: 5)")
    for i, cf in enumerate(pol_cfs):
        cond = cf.get('booleanRule', {}).get('condition', {})
        val = cond.get('values', [{}])[0].get('userEnteredValue')
        bg = cf.get('booleanRule', {}).get('format', {}).get('backgroundColor')
        fg = cf.get('booleanRule', {}).get('format', {}).get('textFormat', {}).get('foregroundColor')
        bold = cf.get('booleanRule', {}).get('format', {}).get('textFormat', {}).get('bold')
        rng = cf.get('ranges', [{}])[0]
        col_span = f"Cols {chr(65+rng.get('startColumnIndex',0))}:{chr(65+rng.get('endColumnIndex',0)-1)}"
        print(f"    Rule {i}: {col_span} if '{val}' -> bg={bg}, fg={fg}, bold={bold}")
        
    # 3. Check Row Heights on Politics (Header, First Block, Middle Block, Last Block)
    rows_res = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=[f'{pol_title}!A1:O241'],
        fields='sheets.data.rowMetadata'
    ).execute()
    rm = rows_res['sheets'][0]['data'][0].get('rowMetadata', [])
    
    header_h = rm[0].get('pixelSize') if len(rm) > 0 else None
    r1_h = rm[1].get('pixelSize') # ambig
    r2_h = rm[2].get('pixelSize') # disambig
    r3_h = rm[3].get('pixelSize') # ambig
    r4_h = rm[4].get('pixelSize') # disambig
    
    mid_idx = 121
    r_mid_ambig = rm[mid_idx].get('pixelSize')
    r_mid_disambig = rm[mid_idx+1].get('pixelSize')
    
    last_idx = 237
    r_last_ambig = rm[last_idx].get('pixelSize')
    r_last_disambig = rm[last_idx+1].get('pixelSize')
    
    print(f"  Row Heights:")
    print(f"    Header: {header_h}px")
    print(f"    First Block (Rows 2-5): ambig={r1_h}px, disambig={r2_h}px, ambig={r3_h}px, disambig={r4_h}px")
    print(f"    Middle Block (Rows 122-123): ambig={r_mid_ambig}px, disambig={r_mid_disambig}px")
    print(f"    Final Block (Rows 238-239): ambig={r_last_ambig}px, disambig={r_last_disambig}px")
    
    # 4. Check Cell Formats across Key Rows
    cells_res = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=[f'{pol_title}!A1:O5', f'{pol_title}!A121:O122', f'{pol_title}!A240:O241'],
        fields='sheets.data.rowData.values.userEnteredFormat'
    ).execute()
    
    # Verify Header A1:O1 formatting
    header_row = cells_res['sheets'][0]['data'][0]['rowData'][0]['values']
    header_aligns = [c.get('userEnteredFormat', {}).get('horizontalAlignment') for c in header_row]
    header_valigns = [c.get('userEnteredFormat', {}).get('verticalAlignment') for c in header_row]
    header_bolds = [c.get('userEnteredFormat', {}).get('textFormat', {}).get('bold') for c in header_row]
    header_bgs = [c.get('userEnteredFormat', {}).get('backgroundColor') is not None for c in header_row]
    print(f"  Header Format: All Bold={all(header_bolds)}, All Middle={all(v=='MIDDLE' for v in header_valigns)}, All Center={all(h=='CENTER' for h in header_aligns)}, All BG set={all(header_bgs)}")
    
    # Verify Data Rows
    # Ambig row (Row 2):
    r2_vals = cells_res['sheets'][0]['data'][0]['rowData'][1]['values']
    r2_wraps = [c.get('userEnteredFormat', {}).get('wrapStrategy') for c in r2_vals]
    r2_aligns = [c.get('userEnteredFormat', {}).get('horizontalAlignment') for c in r2_vals]
    print(f"  Data Row 2 (Ambig) Wraps: {r2_wraps}")
    print(f"  Data Row 2 (Ambig) Alignments: {r2_aligns}")
    
    # Check specific user requirements:
    # Cols F:J wrap == 'WRAP'
    wrap_fj = all(r2_wraps[col] == 'WRAP' for col in range(5, 10))
    # Cols A:E, K, N, O align == 'CENTER'
    center_meta = all(r2_aligns[col] == 'CENTER' for col in [0, 1, 2, 3, 4, 10, 13, 14])
    # Cols F:J, L:M align == 'LEFT'
    left_content = all(r2_aligns[col] == 'LEFT' for col in [5, 6, 7, 8, 9, 11, 12])
    # Cols L:M wrap == 'CLIP'
    clip_lm = all(r2_wraps[col] == 'CLIP' for col in [11, 12])
    
    print(f"  Requirement Verification:")
    print(f"    Cols F:J Text WRAP: {wrap_fj}")
    print(f"    Cols L:M Metadata CLIP: {clip_lm}")
    print(f"    Cols A:E, K, N, O Centered: {center_meta}")
    print(f"    Cols F:J, L:M Left-Aligned: {left_content}")

print("\n==================================================")
print("DATA INTEGRITY VERIFICATION")
print("==================================================")
eng_recs = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='BanglaBBQ_ENG_Politics!A2:O241').execute().get('values', [])
ben_recs = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='BanglaBBQ_BEN_Politics!A2:O241').execute().get('values', [])
print(f"English Records: {len(eng_recs)} (Expected: 240)")
print(f"Bengali Records: {len(ben_recs)} (Expected: 240)")
print(f"IDs match exactly between English and Bengali: {[r[0] for r in eng_recs] == [r[0] for r in ben_recs]}")
print(f"Condition alignment matches: {[r[2:4] for r in eng_recs] == [r[2:4] for r in ben_recs]}")
print(f"Labels match: {[r[10] for r in eng_recs] == [r[10] for r in ben_recs]}")
print("==================================================")
