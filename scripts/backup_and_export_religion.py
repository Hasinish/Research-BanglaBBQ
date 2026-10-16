import os
import sys
import json
import hashlib
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
BACKUP_DIR = 'backups/religion_sheets_backup_20261016'
ACTIVE_DIR = 'BanglaBBQ_Religion'
OLD_RELIGION_DIR = 'Dataset_ BanglaBBQ_Old/Religion'

TABS_TO_BACKUP = [
    ('BanglaBBQ_ENG_Religion_Phase1', 'BanglaBBQ_ENG_Religion_Phase1.jsonl'),
    ('BanglaBBQ_BEN_Religion_Phase1', 'BanglaBBQ_BEN_Religion_Phase1.jsonl'),
    ('BanglaBBQ_ENG_Religion_Phase2', 'BanglaBBQ_ENG_Religion_Phase2.jsonl'),
    ('BanglaBBQ_BEN_Religion_Phase2', 'BanglaBBQ_BEN_Religion_Phase2.jsonl'),
]

EXPECTED_OLD_HASHES = {
    os.path.join(OLD_RELIGION_DIR, 'Religion_eng.jsonl'): '930b9e01fadfc018a3c8cf56988a827037aec27d09a4dab95c781a9900f08660',
    os.path.join(OLD_RELIGION_DIR, 'Religion_bng.jsonl'): '6f33f99da941ed2a740b72adc14bdcd7ebbbedfbae4e68578ce29aa016e7ca2a',
}

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def row_to_record(row):
    # Standard 15-column schema:
    # ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type',
    #  'context', 'question', 'ans0', 'ans1', 'ans2', 'label', 'answer_info',
    #  'additional_metadata', 'category', 'id']
    return {
        'example_id': int(row[0]),
        'question_index': int(row[1]),
        'context_condition': str(row[2]),
        'question_polarity': str(row[3]),
        'type': str(row[4]),
        'context': str(row[5]),
        'question': str(row[6]),
        'ans0': str(row[7]),
        'ans1': str(row[8]),
        'ans2': str(row[9]),
        'label': int(row[10]),
        'answer_info': json.loads(row[11]),
        'additional_metadata': json.loads(row[12]),
        'category': str(row[13]),
        'id': int(row[14])
    }

def main():
    print("====================================================================")
    print("STEP 1 & 2: BACKUP ALL RELIGION WORKSHEETS & EXPORT ACTIVE DATASET")
    print("====================================================================")

    # 1. Verify legacy files are pristine
    print("\n[1/5] Verifying legacy Religion files integrity...")
    for path, expected_hash in EXPECTED_OLD_HASHES.items():
        assert os.path.exists(path), f"Missing legacy file: {path}"
        cur_hash = compute_sha256(path)
        assert cur_hash == expected_hash, f"Hash mismatch for {path}! Expected {expected_hash}, got {cur_hash}"
        print(f"  ✓ Preserved legacy file: {path} (SHA-256: {cur_hash[:16]}...)")

    # 2. Connect to Google Sheets
    print("\n[2/5] Authenticating with Google Sheets API...")
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(ACTIVE_DIR, exist_ok=True)

    raw_sheets_export = {}
    backup_metadata = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'spreadsheet_id': SPREADSHEET_ID,
        'tabs': {}
    }

    # 3. Export all 4 tabs to backup directory
    print("\n[3/5] Exporting 4 Religion worksheets to backup directory...")
    for tab_title, filename in TABS_TO_BACKUP:
        print(f"  Fetching '{tab_title}'...")
        res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{tab_title}!A1:O1000"
        ).execute()
        values = res.get('values', [])
        assert len(values) > 1, f"No data found in {tab_title}"
        
        header = values[0]
        data_rows = values[1:]
        print(f"    Fetched {len(data_rows)} data rows.")

        raw_sheets_export[tab_title] = {
            'header': header,
            'rows': data_rows
        }

        # Convert to JSONL
        records = [row_to_record(r) for r in data_rows]
        out_path = os.path.join(BACKUP_DIR, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        
        file_hash = compute_sha256(out_path)
        backup_metadata['tabs'][tab_title] = {
            'records_count': len(records),
            'filename': filename,
            'sha256': file_hash
        }
        print(f"    Saved {out_path} ({len(records)} records, SHA-256: {file_hash[:16]}...)")

    # Save raw sheets export
    raw_path = os.path.join(BACKUP_DIR, 'raw_sheets_data.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(raw_sheets_export, f, ensure_ascii=False, indent=2)
    backup_metadata['raw_sheets_data_sha256'] = compute_sha256(raw_path)

    # Save metadata
    meta_path = os.path.join(BACKUP_DIR, 'metadata.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(backup_metadata, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Saved backup metadata to {meta_path}")

    # 4. Export Phase 2 to active Religion directory
    print("\n[4/5] Exporting Phase 2 to active dataset directory:", ACTIVE_DIR)
    phase2_eng_records = [row_to_record(r) for r in raw_sheets_export['BanglaBBQ_ENG_Religion_Phase2']['rows']]
    phase2_ben_records = [row_to_record(r) for r in raw_sheets_export['BanglaBBQ_BEN_Religion_Phase2']['rows']]

    assert len(phase2_eng_records) == 960, f"Expected 960 ENG records, got {len(phase2_eng_records)}"
    assert len(phase2_ben_records) == 960, f"Expected 960 BEN records, got {len(phase2_ben_records)}"

    active_eng_path = os.path.join(ACTIVE_DIR, 'Religion_eng.jsonl')
    active_ben_path = os.path.join(ACTIVE_DIR, 'Religion_bng.jsonl')

    with open(active_eng_path, 'w', encoding='utf-8') as f:
        for rec in phase2_eng_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    with open(active_ben_path, 'w', encoding='utf-8') as f:
        for rec in phase2_ben_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    eng_hash = compute_sha256(active_eng_path)
    ben_hash = compute_sha256(active_ben_path)
    print(f"  ✓ Exported {active_eng_path} (960 records, SHA-256: {eng_hash})")
    print(f"  ✓ Exported {active_ben_path} (960 records, SHA-256: {ben_hash})")

    # 5. Integrity Verification
    print("\n[5/5] Checking hash alignment between Phase 2 backup and active exports...")
    assert eng_hash == backup_metadata['tabs']['BanglaBBQ_ENG_Religion_Phase2']['sha256']
    assert ben_hash == backup_metadata['tabs']['BanglaBBQ_BEN_Religion_Phase2']['sha256']
    print("  ✓ Active Religion files match Phase 2 backups bit-for-bit!")

    # Verify legacy files untouched again
    for path, expected_hash in EXPECTED_OLD_HASHES.items():
        assert compute_sha256(path) == expected_hash, f"Legacy file modified: {path}"
    print("  ✓ Legacy files remain 100% untouched.")

    print("\nSUCCESS: All backups and active dataset files created and verified.")

if __name__ == '__main__':
    main()
