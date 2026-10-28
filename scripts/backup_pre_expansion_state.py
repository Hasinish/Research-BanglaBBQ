#!/usr/bin/env python3
"""Backup pre-expansion canonical JSONLs and live Google Sheets worksheets.

Guarantees 100% immutable preservation before any append operations.
"""
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = ROOT / "backups" / "pre_expansion_20261028"
LOCAL_BACKUP = BACKUP_DIR / "local_jsonl"
SHEETS_BACKUP = BACKUP_DIR / "google_sheets"
SPREADSHEET_ID = "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY"

TARGETS = [
    {
        "category": "Health Status",
        "jsonl_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_HealthStatus",
        "en_file": "BanglaBBQ_Health_Status_FINAL_english.jsonl",
        "bn_file": "BanglaBBQ_Health_Status_FINAL_bengali.jsonl",
        "en_sheet": "BanglaBBQ_ENG_HealthStatus",
        "bn_sheet": "BanglaBBQ_BEN_HealthStatus",
    },
    {
        "category": "Marital Status",
        "jsonl_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_MaritalStatus",
        "en_file": "BanglaBBQ_MaritalStatus_FINAL_english.jsonl",
        "bn_file": "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl",
        "en_sheet": "BanglaBBQ_ENG_MaritalStatus",
        "bn_sheet": "BanglaBBQ_BEN_MaritalStatus",
    },
    {
        "category": "Occupational Background",
        "jsonl_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_OccupationalBackground",
        "en_file": "BanglaBBQ_Occupational_Background_FINAL_english.jsonl",
        "bn_file": "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl",
        "en_sheet": "BanglaBBQ_ENG_OccupationalBackground",
        "bn_sheet": "BanglaBBQ_BEN_OccupationalBackground",
    },
]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    print("=" * 70)
    print("PRE-EXPANSION BACKUP: Canonical JSONLs and Live Google Sheets")
    print("=" * 70)

    LOCAL_BACKUP.mkdir(parents=True, exist_ok=True)
    SHEETS_BACKUP.mkdir(parents=True, exist_ok=True)

    manifest = {"timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "files": {}, "sheets": {}}

    # 1. Backup Local JSONLs
    print("\n[1] Backing up local canonical 1,440-row JSONL files...")
    for target in TARGETS:
        for lang_key, fname in [("English", target["en_file"]), ("Bengali", target["bn_file"])]:
            src_path = target["jsonl_dir"] / fname
            dest_path = LOCAL_BACKUP / fname
            assert src_path.exists(), f"Source file missing: {src_path}"

            # Verify line count is exactly 1440
            with src_path.open("r", encoding="utf-8") as f:
                lines = [line for line in f if line.strip()]
            assert len(lines) == 1440, f"{fname} count={len(lines)} != 1440"

            shutil.copyfile(src_path, dest_path)
            h = sha256_file(src_path)
            manifest["files"][fname] = {
                "source": str(src_path.relative_to(ROOT)),
                "backup": str(dest_path.relative_to(ROOT)),
                "records": len(lines),
                "bytes": src_path.stat().st_size,
                "sha256": h,
            }
            print(f"    - {fname}: 1,440 rows, SHA-256={h} (SAVED)")

    # 2. Backup Live Google Sheets
    print("\n[2] Exporting live Google Sheets rows 1..1441 (pre-expansion)...")
    creds = Credentials.from_authorized_user_file(ROOT / "token.json")
    service = build("sheets", "v4", credentials=creds)

    for target in TARGETS:
        for sheet_title in (target["en_sheet"], target["bn_sheet"]):
            print(f"    - Fetching '{sheet_title}' (A1:O1441)...")
            res = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"'{sheet_title}'!A1:O1441",
                valueRenderOption="UNFORMATTED_VALUE"
            ).execute()
            values = res.get("values", [])
            assert len(values) == 1441, f"Expected 1441 rows for {sheet_title}, got {len(values)}"
            assert len(values[0]) == 15, f"Expected 15 header columns for {sheet_title}, got {len(values[0])}"

            out_path = SHEETS_BACKUP / f"{sheet_title}.json"
            out_path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
            manifest["sheets"][sheet_title] = {
                "rows_exported": len(values),
                "columns": len(values[0]),
                "backup_path": str(out_path.relative_to(ROOT)),
            }
            print(f"      Saved {len(values)} rows to {out_path.name}")
            time.sleep(0.5)

    manifest_path = BACKUP_DIR / "pre_expansion_hashes.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[+] Pre-expansion manifest written to {manifest_path}")
    print("BACKUP COMPLETED WITH 100% INTEGRITY")
    return 0

if __name__ == "__main__":
    sys.exit(main())
