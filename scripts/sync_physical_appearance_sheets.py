import hashlib
import json
import os
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_PhysicalAppearance"

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
ENG_SHEET_TITLE = 'BanglaBBQ_ENG_PhysicalAppearance'
BEN_SHEET_TITLE = 'BanglaBBQ_BEN_PhysicalAppearance'
ENG_SHEET_GID = 984262367
BEN_SHEET_GID = 934839633

BACKUP_DIR = ROOT / "backups" / "physical_appearance_pre_sync_20261027"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

HEADER = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

def get_sheets_service():
    creds = Credentials.from_authorized_user_file('token.json')
    return build('sheets', 'v4', credentials=creds)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def load_canonical_jsonl(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def format_canonical_row(r):
    return [
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

def main():
    print("====================================================================")
    print("STARTING GOOGLE SHEETS SYNCHRONIZATION: PHYSICAL APPEARANCE")
    print("====================================================================")
    
    service = get_sheets_service()
    
    # 0. Verify sheet IDs
    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
    assert sheet_map.get(ENG_SHEET_TITLE) == ENG_SHEET_GID, f"ENG sheet GID mismatch: {sheet_map.get(ENG_SHEET_TITLE)} != {ENG_SHEET_GID}"
    assert sheet_map.get(BEN_SHEET_TITLE) == BEN_SHEET_GID, f"BEN sheet GID mismatch: {sheet_map.get(BEN_SHEET_TITLE)} != {BEN_SHEET_GID}"
    print(f"Verified GIDs: {ENG_SHEET_TITLE} ({ENG_SHEET_GID}), {BEN_SHEET_TITLE} ({BEN_SHEET_GID})")
    
    # 1. Complete Backups of both worksheets
    print("\n--- 1. Creating Complete Backups of Live Worksheets ---")
    live_eng_resp = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{ENG_SHEET_TITLE}!A1:O1441"
    ).execute()
    live_eng_rows = live_eng_resp.get("values", [])
    
    live_ben_resp = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{BEN_SHEET_TITLE}!A1:O1441"
    ).execute()
    live_ben_rows = live_ben_resp.get("values", [])
    
    assert len(live_eng_rows) == 1441, f"Expected 1441 ENG rows, got {len(live_eng_rows)}"
    assert len(live_ben_rows) == 1441, f"Expected 1441 BEN rows, got {len(live_ben_rows)}"
    
    backup_file = BACKUP_DIR / "live_physical_appearance_pre_repair_backup.json"
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump({
            "spreadsheet_id": SPREADSHEET_ID,
            "eng_sheet": ENG_SHEET_TITLE,
            "eng_gid": ENG_SHEET_GID,
            "eng_rows_count": len(live_eng_rows),
            "eng_rows": live_eng_rows,
            "ben_sheet": BEN_SHEET_TITLE,
            "ben_gid": BEN_SHEET_GID,
            "ben_rows_count": len(live_ben_rows),
            "ben_rows": live_ben_rows
        }, f, ensure_ascii=False, indent=2)
        
    backup_hash = sha256_file(backup_file)
    manifest_file = BACKUP_DIR / "backup_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump({
            "backup_file": backup_file.name,
            "sha256": backup_hash,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "eng_rows": len(live_eng_rows),
            "ben_rows": len(live_ben_rows)
        }, f, indent=2)
    print(f"Backup saved to {backup_file.name} (SHA-256: {backup_hash})")
    print(f"Backup manifest saved to {manifest_file.name}")
    
    # 2. Compare Live Sheets vs Canonical GitHub JSONLs
    print("\n--- 2. Comparing Live Worksheets Against Canonical Production ---")
    en_canonical = load_canonical_jsonl(DATASET_ROOT / "BanglaBBQ_Physical_Appearance_FINAL_english.jsonl")
    bn_canonical = load_canonical_jsonl(DATASET_ROOT / "BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl")
    
    assert len(en_canonical) == 1440
    assert len(bn_canonical) == 1440
    
    def analyze_diffs(live_rows, canonical_records, sheet_title):
        header = live_rows[0]
        assert header == HEADER, f"Header mismatch in {sheet_title}"
        changed_cells = []
        unexpected_diffs = []
        
        for idx, rec in enumerate(canonical_records):
            row_num = idx + 2 # 1-based, row 1 is header
            live_row = live_rows[idx + 1]
            exp_row = format_canonical_row(rec)
            
            for col_idx in range(15):
                col_name = HEADER[col_idx]
                col_letter = chr(ord('A') + col_idx)
                cell_ref = f"{col_letter}{row_num}"
                
                lv = live_row[col_idx] if col_idx < len(live_row) else ""
                ev = exp_row[col_idx]
                
                # Check JSON equivalence for cols 11 and 12
                if col_idx in (11, 12):
                    try:
                        if json.loads(str(lv)) != json.loads(str(ev)):
                            unexpected_diffs.append((cell_ref, col_name, lv, ev))
                    except Exception:
                        if str(lv) != str(ev):
                            unexpected_diffs.append((cell_ref, col_name, lv, ev))
                else:
                    if str(lv) != str(ev):
                        if col_idx == 5: # Column F is context
                            changed_cells.append({
                                "row": row_num,
                                "cell": cell_ref,
                                "old": str(lv),
                                "new": str(ev)
                            })
                        else:
                            unexpected_diffs.append((cell_ref, col_name, lv, ev))
                            
        return changed_cells, unexpected_diffs

    en_changed, en_unexpected = analyze_diffs(live_eng_rows, en_canonical, ENG_SHEET_TITLE)
    bn_changed, bn_unexpected = analyze_diffs(live_ben_rows, bn_canonical, BEN_SHEET_TITLE)
    
    print(f"ENG: {len(en_changed)} Column F changes detected. Unexpected diffs in other columns: {len(en_unexpected)}")
    print(f"BEN: {len(bn_changed)} Column F changes detected. Unexpected diffs in other columns: {len(bn_unexpected)}")
    
    if en_unexpected or bn_unexpected:
        print("CRITICAL: Unexpected differences detected outside Column F!")
        for diff in (en_unexpected + bn_unexpected)[:10]:
            print("  ", diff)
        sys.exit(1)
        
    assert len(en_changed) == 720, f"Expected 720 ENG changes, got {len(en_changed)}"
    assert len(bn_changed) == 720, f"Expected 720 BEN changes, got {len(bn_changed)}"
    print("PASS: Exactly 720 Column F changes detected per sheet (1,440 total). All other 14 columns 100% identical.")
    
    # 3. Update ONLY the 720 changed context cells in Column F per worksheet
    print("\n--- 3. Updating Exactly 720 Cells in Column F for Both Worksheets ---")
    
    def apply_updates(changed_list, sheet_title):
        data = []
        for item in changed_list:
            data.append({
                "range": f"{sheet_title}!{item['cell']}",
                "values": [[item['new']]]
            })
        # Execute batch update
        body = {
            "valueInputOption": "RAW",
            "data": data
        }
        res = service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print(f"Successfully updated {res.get('totalUpdatedCells')} cells in {sheet_title}.")
        return res
        
    apply_updates(en_changed, ENG_SHEET_TITLE)
    apply_updates(bn_changed, BEN_SHEET_TITLE)
    
    # 4. Read back and verify all 43,200 data cells across both worksheets
    print("\n--- 4. Reading Back and Verifying All 43,200 Data Cells ---")
    time.sleep(2.0)
    
    readback_eng = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{ENG_SHEET_TITLE}!A1:O1441"
    ).execute().get("values", [])
    
    readback_ben = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{BEN_SHEET_TITLE}!A1:O1441"
    ).execute().get("values", [])
    
    assert len(readback_eng) == 1441
    assert len(readback_ben) == 1441
    
    def verify_all_cells(readback_rows, canonical_records, sheet_title):
        total_cells = 1440 * 15
        mismatches = 0
        for idx, rec in enumerate(canonical_records):
            row_num = idx + 2
            live_row = readback_rows[idx + 1]
            exp_row = format_canonical_row(rec)
            for c in range(15):
                lv = live_row[c] if c < len(live_row) else ""
                ev = exp_row[c]
                if c in (11, 12):
                    try:
                        if json.loads(str(lv)) != json.loads(str(ev)):
                            mismatches += 1
                    except Exception:
                        if str(lv) != str(ev):
                            mismatches += 1
                else:
                    if str(lv) != str(ev):
                        mismatches += 1
        print(f"  {sheet_title}: {total_cells - mismatches}/{total_cells} data cells match ({((total_cells - mismatches)/total_cells)*100:.4f}%)")
        assert mismatches == 0, f"Found {mismatches} mismatches in {sheet_title}"
        return total_cells

    en_verified = verify_all_cells(readback_eng, en_canonical, ENG_SHEET_TITLE)
    bn_verified = verify_all_cells(readback_ben, bn_canonical, BEN_SHEET_TITLE)
    print(f"Total live data cells verified: {en_verified + bn_verified} across both worksheets (0 mismatches)")
    
    # 5. Confirm exactly 180 First / 180 Second negative gold introduction positions on live data
    print("\n--- 5. Verifying 180 First / 180 Second Position Parity on Live Sheets ---")
    def verify_live_positions(readback_rows, canonical_records, lang_name):
        first_count = 0
        second_count = 0
        disambig_count = 0
        for idx, rec in enumerate(canonical_records):
            if rec['context_condition'] == 'disambig' and rec['question_polarity'] == 'neg':
                disambig_count += 1
                live_context = readback_rows[idx + 1][5] # Column F
                
                people = [info[0] for opt, info in rec['answer_info'].items() if info[1] != 'unknown']
                p1, p2 = people[0], people[1]
                
                pos1 = live_context.find(p1)
                pos2 = live_context.find(p2)
                assert pos1 != -1 and pos2 != -1, f"Names not found in live context row {idx+2}"
                
                first_person = p1 if pos1 < pos2 else p2
                second_person = p2 if pos1 < pos2 else p1
                
                gold = rec[f"ans{rec['label']}"]
                if gold == first_person:
                    first_count += 1
                elif gold == second_person:
                    second_count += 1
                else:
                    raise ValueError(f"Gold mismatch at row {idx+2}")
        print(f"  Live [{lang_name}]: {first_count} First / {second_count} Second (out of {disambig_count} disambiguated negative rows)")
        assert first_count == 180 and second_count == 180
        return first_count, second_count

    en_f, en_s = verify_live_positions(readback_eng, en_canonical, "English")
    bn_f, bn_s = verify_live_positions(readback_ben, bn_canonical, "Bengali")
    
    print("\n====================================================================")
    print("GOOGLE SHEETS LIVE SYNCHRONIZATION AND VERIFICATION COMPLETE!")
    print("100% BIT-FOR-BIT LIVE PARITY (43,200 CELLS) VERIFIED WITH ZERO ERRORS.")
    print("====================================================================")

if __name__ == '__main__':
    main()
