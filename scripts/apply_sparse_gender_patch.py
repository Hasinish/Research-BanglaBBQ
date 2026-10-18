"""
Genuinely Sparse, Idempotent, Cell-Targeted Production Updater for BanglaBBQ Gender Identity.

Features:
1. Strictly sparse: Updates ONLY specifically authorized cells (no bulk worksheet rewrites).
2. Conflict pre-check: Reads live cell values before writing and verifies they match expected pre-state.
3. Dry-run mode: Calculates and reports exact cell diffs without making any API writes.
4. Immediate readback verification: Fetches all modified ranges to guarantee persistence.
5. Bidirectional synchronization: Updates canonical JSONL files in lockstep.
6. Machine-readable audit report: Outputs changed-cell report with timestamps and cell coordinates.
"""

import argparse
import json
import os
import sys
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
ENG_SHEET_NAME = 'BanglaBBQ_ENG_Gender'
BEN_SHEET_NAME = 'BanglaBBQ_BEN_Gender'

COL_MAP = {
    'example_id': 'A', 'question_index': 'B', 'context_condition': 'C',
    'question_polarity': 'D', 'type': 'E', 'context': 'F', 'question': 'G',
    'ans0': 'H', 'ans1': 'I', 'ans2': 'J', 'label': 'K',
    'answer_info': 'L', 'additional_metadata': 'M', 'category': 'N', 'id': 'O'
}


def build_cell_updates(manifest_path, eng_jsonl_path, ben_jsonl_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    records = manifest.get('records', [])
    eng_updates = [] # list of (row, col_letter, old_val, new_val)
    ben_updates = []
    
    for rec in records:
        eid = rec['example_id']
        row = eid + 2
        after = rec['after']
        before = rec.get('before', {})
        
        # Check context
        if 'context_eng' in after and after['context_eng'] != before.get('context_eng'):
            eng_updates.append((row, COL_MAP['context'], before.get('context_eng', ''), str(after['context_eng'])))
        if 'context_ben' in after and after['context_ben'] != before.get('context_ben'):
            ben_updates.append((row, COL_MAP['context'], before.get('context_ben', ''), str(after['context_ben'])))
            
        # Check question
        if 'question_eng' in after and after['question_eng'] != before.get('question_eng'):
            eng_updates.append((row, COL_MAP['question'], before.get('question_eng', ''), str(after['question_eng'])))
        if 'question_ben' in after and after['question_ben'] != before.get('question_ben'):
            ben_updates.append((row, COL_MAP['question'], before.get('question_ben', ''), str(after['question_ben'])))
            
        # Check choices
        if 'choices_eng' in after:
            c_eng_after = after['choices_eng']
            c_eng_before = before.get('choices_eng', ['', '', ''])
            for idx, col in enumerate(['ans0', 'ans1', 'ans2']):
                if c_eng_after[idx] != c_eng_before[idx]:
                    eng_updates.append((row, COL_MAP[col], c_eng_before[idx], str(c_eng_after[idx])))
                    
        if 'choices_ben' in after:
            c_ben_after = after['choices_ben']
            c_ben_before = before.get('choices_ben', ['', '', ''])
            for idx, col in enumerate(['ans0', 'ans1', 'ans2']):
                if c_ben_after[idx] != c_ben_before[idx]:
                    ben_updates.append((row, COL_MAP[col], c_ben_before[idx], str(c_ben_after[idx])))
                    
        # Check label
        if 'label' in after and after['label'] != before.get('label'):
            eng_updates.append((row, COL_MAP['label'], str(before.get('label', '')), str(after['label'])))
            ben_updates.append((row, COL_MAP['label'], str(before.get('label', '')), str(after['label'])))
            
        # Check answer_info
        if 'answer_info' in after:
            ainfo_after = json.dumps(after['answer_info'], ensure_ascii=False)
            ainfo_before = json.dumps(before.get('answer_info', {}), ensure_ascii=False) if before.get('answer_info') else ''
            if ainfo_after != ainfo_before:
                eng_updates.append((row, COL_MAP['answer_info'], ainfo_before, ainfo_after))
                ben_updates.append((row, COL_MAP['answer_info'], ainfo_before, ainfo_after))
                
        # Check source / additional_metadata
        if 'additional_metadata' in after:
            meta_after = json.dumps(after['additional_metadata'], ensure_ascii=False)
            meta_before = json.dumps(before.get('additional_metadata', {}), ensure_ascii=False) if before.get('additional_metadata') else ''
            if meta_after != meta_before:
                eng_updates.append((row, COL_MAP['additional_metadata'], meta_before, meta_after))
                ben_updates.append((row, COL_MAP['additional_metadata'], meta_before, meta_after))
                
    return eng_updates, ben_updates, records


def main():
    parser = argparse.ArgumentParser(description="Apply genuinely sparse production updates from a patch manifest.")
    parser.add_argument('--manifest', required=True, help="Path to JSON patch manifest.")
    parser.add_argument('--dry-run', action='store_true', help="Inspect and diff without writing.")
    parser.add_argument('--skip-sheets', action='store_true', help="Apply to local JSONL files only.")
    args = parser.parse_args()

    print("====================================================================")
    print("GENUINELY SPARSE PRODUCTION PATCH UPDATER")
    print("====================================================================")
    print(f"Manifest: {args.manifest}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE PRODUCTION WRITE'}")
    
    eng_jsonl = 'BanglaBBQ_Gender/Gender_identity_eng.jsonl'
    ben_jsonl = 'BanglaBBQ_Gender/Gender_identity_bng.jsonl'
    
    eng_updates, ben_updates, records = build_cell_updates(args.manifest, eng_jsonl, ben_jsonl)
    
    print(f"\nIdentified Changed Cells:")
    print(f"  English cells to update: {len(eng_updates)}")
    print(f"  Bengali cells to update: {len(ben_updates)}")
    print(f"  Total sparse cells:      {len(eng_updates) + len(ben_updates)}")
    
    if len(eng_updates) == 0 and len(ben_updates) == 0:
        print("No cells to update. Exiting.")
        return
        
    for sheet_name, updates in [(ENG_SHEET_NAME, eng_updates[:5]), (BEN_SHEET_NAME, ben_updates[:5])]:
        print(f"\nSample cell updates for {sheet_name}:")
        for row, col, old_v, new_v in updates:
            print(f"  Row {row}, Col {col}: '{old_v[:40]}' -> '{new_v[:40]}'")
            
    if args.dry_run:
        print("\nDry run completed successfully. Zero cells written to Google Sheets.")
        return
        
    if not args.skip_sheets:
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('sheets', 'v4', credentials=creds)
        
        # 1. Conflict Pre-check
        print("\n--- Step 1: Pre-checking live cells against manifest baseline ---")
        conflicts = []
        for sheet_name, updates in [(ENG_SHEET_NAME, eng_updates), (BEN_SHEET_NAME, ben_updates)]:
            if not updates:
                continue
            ranges = [f"{sheet_name}!{col}{row}" for row, col, _, _ in updates]
            # Batch get in chunks of 100
            chunk_size = 100
            for i in range(0, len(ranges), chunk_size):
                chunk_ranges = ranges[i:i+chunk_size]
                res = service.spreadsheets().values().batchGet(
                    spreadsheetId=SPREADSHEET_ID,
                    ranges=chunk_ranges
                ).execute()
                value_ranges = res.get('valueRanges', [])
                for idx, vr in enumerate(value_ranges):
                    orig_update = updates[i + idx]
                    live_val = vr.get('values', [['']])[0][0] if vr.get('values') else ''
                    exp_val = orig_update[2]
                    # Strict bidirectional comparison (closing empty-value loophole)
                    exp_clean = '' if exp_val is None else str(exp_val).strip()
                    live_clean = '' if live_val is None else str(live_val).strip()
                    if exp_clean != live_clean:
                        conflicts.append((vr.get('range'), exp_val, live_val))

        if conflicts:
            print(f"\nCRITICAL ABORT: Detected {len(conflicts)} live-cell conflict(s) during pre-check!")
            for rng, exp, act in conflicts[:10]:
                print(f"  Conflict at {rng}: expected '{exp[:40]}', live is '{act[:40]}'")
            if len(conflicts) > 10:
                print(f"  ... and {len(conflicts) - 10} more conflict(s).")
            print("\nAborting update to protect production sheet integrity. ZERO cells were modified.")
            sys.exit(1)

        print(f"Pre-check complete: 0 conflicts detected across all {len(eng_updates) + len(ben_updates)} targeted cells. Safe to proceed.")

        # 2. Execute sparse batchUpdate
        print("\n--- Step 2: Executing sparse batchUpdate ---")
        batch_data = []
        for row, col, _, new_val in eng_updates:
            batch_data.append({
                'range': f"{ENG_SHEET_NAME}!{col}{row}",
                'values': [[new_val]]
            })
        for row, col, _, new_val in ben_updates:
            batch_data.append({
                'range': f"{BEN_SHEET_NAME}!{col}{row}",
                'values': [[new_val]]
            })
            
        body = {
            'valueInputOption': 'RAW',
            'data': batch_data
        }
        res = service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        updated_cells = res.get('totalUpdatedCells', 0)
        print(f"Sparse batchUpdate complete. Total updated cells: {updated_cells}")

        # 3. Readback Verification
        print("\n--- Step 3: Verifying live readback parity ---")
        ranges_to_check = [f"{ENG_SHEET_NAME}!{col}{row}" for row, col, _, _ in eng_updates] + \
                          [f"{BEN_SHEET_NAME}!{col}{row}" for row, col, _, _ in ben_updates]
        all_expected = [new_val for _, _, _, new_val in eng_updates] + \
                       [new_val for _, _, _, new_val in ben_updates]
                       
        mismatches = 0
        chunk_size = 100
        for i in range(0, len(ranges_to_check), chunk_size):
            chunk_r = ranges_to_check[i:i+chunk_size]
            res = service.spreadsheets().values().batchGet(
                spreadsheetId=SPREADSHEET_ID,
                ranges=chunk_r
            ).execute()
            for idx, vr in enumerate(res.get('valueRanges', [])):
                act = vr.get('values', [['']])[0][0] if vr.get('values') else ''
                exp = all_expected[i + idx]
                if act != exp:
                    mismatches += 1
                    print(f"FAIL: Readback mismatch at {vr.get('range')}: exp '{exp}', got '{act}'")
        assert mismatches == 0, f"Readback failed with {mismatches} cell mismatches!"
        print(f"Live readback verification PASSED for all {len(ranges_to_check)} cells!")

    # 4. Synchronize local canonical JSONL files
    print("\n--- Step 4: Synchronizing local canonical JSONL files ---")
    with open(eng_jsonl, 'r', encoding='utf-8') as f:
        eng_recs = [json.loads(line) for line in f]
    with open(ben_jsonl, 'r', encoding='utf-8') as f:
        ben_recs = [json.loads(line) for line in f]
        
    for rec in records:
        eid = rec['example_id']
        after = rec['after']
        if 'context_eng' in after:
            eng_recs[eid]['context'] = after['context_eng']
        if 'question_eng' in after:
            eng_recs[eid]['question'] = after['question_eng']
        if 'choices_eng' in after:
            eng_recs[eid]['ans0'] = after['choices_eng'][0]
            eng_recs[eid]['ans1'] = after['choices_eng'][1]
            eng_recs[eid]['ans2'] = after['choices_eng'][2]
        if 'label' in after:
            eng_recs[eid]['label'] = after['label']
        if 'answer_info' in after:
            eng_recs[eid]['answer_info'] = after['answer_info']
        if 'additional_metadata' in after:
            eng_recs[eid]['additional_metadata'] = after['additional_metadata']
            
        if 'context_ben' in after:
            ben_recs[eid]['context'] = after['context_ben']
        if 'question_ben' in after:
            ben_recs[eid]['question'] = after['question_ben']
        if 'choices_ben' in after:
            ben_recs[eid]['ans0'] = after['choices_ben'][0]
            ben_recs[eid]['ans1'] = after['choices_ben'][1]
            ben_recs[eid]['ans2'] = after['choices_ben'][2]
        if 'label' in after:
            ben_recs[eid]['label'] = after['label']
        if 'answer_info' in after:
            ben_recs[eid]['answer_info'] = after['answer_info']
        if 'additional_metadata' in after:
            ben_recs[eid]['additional_metadata'] = after['additional_metadata']
            
    with open(eng_jsonl, 'w', encoding='utf-8') as f:
        for r in eng_recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    with open(ben_jsonl, 'w', encoding='utf-8') as f:
        for r in ben_recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            
    print(f"Updated {len(records)} records in both {eng_jsonl} and {ben_jsonl}.")
    
    # Generate changed-cell report
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "manifest": args.manifest,
        "eng_cells_count": len(eng_updates),
        "ben_cells_count": len(ben_updates),
        "total_cells_count": len(eng_updates) + len(ben_updates),
        "eng_updates": [{"row": r, "col": c, "new_val": v} for r, c, _, v in eng_updates],
        "ben_updates": [{"row": r, "col": c, "new_val": v} for r, c, _, v in ben_updates]
    }
    with open('scratch/sparse_patch_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Generated changed-cell audit report at scratch/sparse_patch_report.json")
    print("====================================================================")
    print("SPARSE PRODUCTION PATCH COMPLETED SUCCESSFULLY!")
    print("====================================================================")


if __name__ == '__main__':
    main()
