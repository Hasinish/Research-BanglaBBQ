import hashlib
import json
import shutil
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_sheets_service():
    creds = Credentials.from_authorized_user_file('token.json')
    return build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
SHEET_ENG_TITLE = 'BanglaBBQ_ENG_Education'
SHEET_BEN_TITLE = 'BanglaBBQ_BEN_Education'

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "backups" / "education_pre_final_qa_repair_20261019"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# 1. Backup local canonical files
files_to_copy = [
    "BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl",
    "BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl",
    "BanglaBBQ_EducationalBackground/scenario_templates.json",
    "BanglaBBQ_EducationalBackground/source_audit_matrix.json",
    "BanglaBBQ_EducationalBackground/source_audit_matrix.md",
    "BanglaBBQ_EducationalBackground/legacy_to_improved_mapping.json"
]

manifest = {"local_files": {}, "sheets": {}}

for rel in files_to_copy:
    src = ROOT / rel
    dst = BACKUP_DIR / src.name
    shutil.copy2(src, dst)
    h = sha256_file(dst)
    manifest["local_files"][src.name] = {
        "source": str(rel),
        "sha256": h,
        "size": dst.stat().st_size
    }
    print(f"Backed up {src.name} -> SHA256: {h}")

# 2. Backup live Google Sheets tabs
print("\nFetching live Google Sheets tabs...")
service = get_sheets_service()

eng_resp = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"{SHEET_ENG_TITLE}!A1:O2881"
).execute()
eng_rows = eng_resp.get("values", [])

ben_resp = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"{SHEET_BEN_TITLE}!A1:O2881"
).execute()
ben_rows = ben_resp.get("values", [])

print(f"Fetched ENG rows: {len(eng_rows)}, BEN rows: {len(ben_rows)}")

sheets_dump_path = BACKUP_DIR / "live_sheets_backup.json"
with open(sheets_dump_path, "w", encoding="utf-8") as f:
    json.dump({
        "spreadsheet_id": SPREADSHEET_ID,
        "eng_sheet": SHEET_ENG_TITLE,
        "eng_rows_count": len(eng_rows),
        "eng_rows": eng_rows,
        "ben_sheet": SHEET_BEN_TITLE,
        "ben_rows_count": len(ben_rows),
        "ben_rows": ben_rows
    }, f, ensure_ascii=False, indent=2)

h_sheets = sha256_file(sheets_dump_path)
manifest["sheets"] = {
    "file": "live_sheets_backup.json",
    "sha256": h_sheets,
    "eng_rows": len(eng_rows),
    "ben_rows": len(ben_rows)
}

manifest_path = BACKUP_DIR / "backup_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"\nLive sheets dump saved to {sheets_dump_path.name} (SHA256: {h_sheets})")
print(f"Backup manifest saved to {manifest_path.name}")
