import hashlib
import io
import json
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

ROOT = Path(__file__).resolve().parents[3]
BACKUP_DIR = ROOT / "backups" / "pre_v21_production_promotion_20261117"
SHEETS_BAK_DIR = BACKUP_DIR / "google_sheets"
DRIVE_BAK_DIR = BACKUP_DIR / "google_drive"

SPREADSHEET_ID = "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY"
DRIVE_ROOT_ID = "1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe"

SHEETS_SPEC = [
    ("BanglaBBQ_ENG_Education", 2880),
    ("BanglaBBQ_BEN_Education", 2880),
    ("BanglaBBQ_ENG_Ethnicity", 1440),
    ("BanglaBBQ_BEN_Ethnicity", 1440),
    ("BanglaBBQ_ENG_HealthStatus", 2880),
    ("BanglaBBQ_BEN_HealthStatus", 2880),
    ("BanglaBBQ_ENG_MaritalStatus", 2880),
    ("BanglaBBQ_BEN_MaritalStatus", 2880),
    ("BanglaBBQ_ENG_OccupationalBackground", 2880),
    ("BanglaBBQ_BEN_OccupationalBackground", 2880),
    ("BanglaBBQ_ENG_PhysicalAppearance", 1440),
    ("BanglaBBQ_BEN_PhysicalAppearance", 1440),
    ("BanglaBBQ_ENG_Politics", 2880),
    ("BanglaBBQ_BEN_Politics", 2880),
    ("BanglaBBQ_ENG_Regional", 1440),
    ("BanglaBBQ_BEN_Regional", 1440),
    ("BanglaBBQ_ENG_Religion", 2880),
    ("BanglaBBQ_BEN_Religion", 2880),
    ("BanglaBBQ_ENG_SocialStatus", 1440),
    ("BanglaBBQ_BEN_SocialStatus", 1440),
]

DRIVE_CATEGORIES = {
    "BanglaBBQ_EducationalBackground": ["BanglaBBQ_ENG_Education.jsonl", "BanglaBBQ_BEN_Education.jsonl"],
    "BanglaBBQ_Ethnicity": ["BanglaBBQ_ENG_Ethnicity.jsonl", "BanglaBBQ_BEN_Ethnicity.jsonl"],
    "BanglaBBQ_HealthStatus": ["BanglaBBQ_ENG_HealthStatus.jsonl", "BanglaBBQ_BEN_HealthStatus.jsonl"],
    "BanglaBBQ_MaritalStatus": ["BanglaBBQ_ENG_MaritalStatus.jsonl", "BanglaBBQ_BEN_MaritalStatus.jsonl"],
    "BanglaBBQ_OccupationalBackground": ["BanglaBBQ_ENG_OccupationalBackground.jsonl", "BanglaBBQ_BEN_OccupationalBackground.jsonl"],
    "BanglaBBQ_PhysicalAppearance": ["BanglaBBQ_ENG_PhysicalAppearance.jsonl", "BanglaBBQ_BEN_PhysicalAppearance.jsonl"],
    "BanglaBBQ_Politics": ["BanglaBBQ_ENG_Politics.jsonl", "BanglaBBQ_BEN_Politics.jsonl"],
    "BanglaBBQ_Regional": ["BanglaBBQ_ENG_Regional.jsonl", "BanglaBBQ_BEN_Regional.jsonl"],
    "BanglaBBQ_Religion": ["BanglaBBQ_ENG_Religion.jsonl", "BanglaBBQ_BEN_Religion.jsonl"],
    "BanglaBBQ_SocialStatus": ["BanglaBBQ_ENG_SocialStatus.jsonl", "BanglaBBQ_BEN_SocialStatus.jsonl"],
}


def retry(func):
    for attempt in range(5):
        try:
            return func()
        except HttpError as e:
            if e.resp.status in (429, 500, 503) and attempt < 4:
                time.sleep(2 ** attempt)
            else:
                raise


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def backup_sheets(sheets_svc):
    print("[*] Phase 3B: Backing up all 20 Google Sheets worksheets + properties...")
    SHEETS_BAK_DIR.mkdir(parents=True, exist_ok=True)
    meta = retry(lambda: sheets_svc.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        fields="spreadsheetId,properties,sheets(properties,conditionalFormats,data.columnMetadata)"
    ).execute())

    sheets_by_title = {s["properties"]["title"]: s for s in meta["sheets"]}
    backup_manifest = {"spreadsheet_id": SPREADSHEET_ID, "worksheets": {}}

    target_meta_dump = {}
    for title, exp_rows in SHEETS_SPEC:
        assert title in sheets_by_title, f"Missing target sheet in Google Sheets: {title}"
        s_info = sheets_by_title[title]
        props = s_info["properties"]
        target_meta_dump[title] = {
            "sheetId": props["sheetId"],
            "gridProperties": props.get("gridProperties"),
            "conditionalFormats": s_info.get("conditionalFormats", []),
            "columnMetadata": s_info.get("data", [{}])[0].get("columnMetadata", []) if s_info.get("data") else [],
        }

        rng = f"'{title}'!A1:O{exp_rows + 1}"
        res = retry(lambda r=rng: sheets_svc.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=r,
            valueRenderOption="UNFORMATTED_VALUE"
        ).execute())
        vals = res.get("values", [])
        out_p = SHEETS_BAK_DIR / f"{title}.json"
        raw = json.dumps(vals, ensure_ascii=False, indent=1).encode("utf-8")
        out_p.write_bytes(raw)

        backup_manifest["worksheets"][title] = {
            "sheetId": props["sheetId"],
            "range_exported": rng,
            "rows_exported": len(vals),
            "backup_file": str(out_p.relative_to(ROOT)),
            "sha256": sha256_bytes(raw),
            "bytes": len(raw),
        }
        print(f"    -> Backed up sheet {title:<38} (ID: {props['sheetId']}) rows={len(vals)}")
        time.sleep(0.4)

    meta_raw = json.dumps(target_meta_dump, ensure_ascii=False, indent=2).encode("utf-8")
    (SHEETS_BAK_DIR / "sheets_metadata_backup.json").write_bytes(meta_raw)
    backup_manifest["metadata_sha256"] = sha256_bytes(meta_raw)
    (SHEETS_BAK_DIR / "sheets_backup_manifest.json").write_text(json.dumps(backup_manifest, indent=2), encoding="utf-8")
    print("    -> Phase 3B Google Sheets backup COMPLETE [PASS]")


def backup_drive(drive_svc):
    print("[*] Phase 3C: Backing up all 20 remote Google Drive dataset files...")
    DRIVE_BAK_DIR.mkdir(parents=True, exist_ok=True)
    folders_res = retry(lambda: drive_svc.files().list(
        q=f"'{DRIVE_ROOT_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute())
    folder_map = {f["name"]: f["id"] for f in folders_res.get("files", [])}

    manifest = {"drive_root_id": DRIVE_ROOT_ID, "files": {}, "untouched_remote_age_gender": {}}

    # Also record untouched Age & Gender remote IDs & hashes
    for untouched_cat in ("BanglaBBQ_Age", "BanglaBBQ_Gender"):
        fid = folder_map[untouched_cat]
        res = retry(lambda folder_id=fid: drive_svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, size, md5Checksum, properties)"
        ).execute())
        for rf in res.get("files", []):
            manifest["untouched_remote_age_gender"][f"{untouched_cat}/{rf['name']}"] = {
                "file_id": rf["id"],
                "md5": rf.get("md5Checksum"),
                "sha256_prop": (rf.get("properties") or {}).get("sha256"),
                "size": rf.get("size"),
            }

    for cat_folder, fnames in DRIVE_CATEGORIES.items():
        assert cat_folder in folder_map, f"Missing Drive category folder: {cat_folder}"
        fid = folder_map[cat_folder]
        res = retry(lambda folder_id=fid: drive_svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, parents, size, md5Checksum, properties)"
        ).execute())
        fmap = {rf["name"]: rf for rf in res.get("files", [])}

        for fn in fnames:
            assert fn in fmap, f"Missing remote Drive file: {cat_folder}/{fn}"
            rf = fmap[fn]
            bak_p = DRIVE_BAK_DIR / cat_folder / fn
            bak_p.parent.mkdir(parents=True, exist_ok=True)

            req = drive_svc.files().get_media(fileId=rf["id"])
            buf = io.BytesIO()
            downloader = MediaIoBaseDownload(buf, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            data = buf.getvalue()
            bak_p.write_bytes(data)

            manifest["files"][f"{cat_folder}/{fn}"] = {
                "file_id": rf["id"],
                "parent_folder_id": fid,
                "remote_size": int(rf.get("size", 0)),
                "remote_md5": rf.get("md5Checksum"),
                "remote_sha256_prop": (rf.get("properties") or {}).get("sha256"),
                "backup_path": str(bak_p.relative_to(ROOT)),
                "backup_sha256": sha256_bytes(data),
            }
            print(f"    -> Downloaded Drive backup {cat_folder}/{fn} (ID: {rf['id']}, bytes={len(data)})")

    (DRIVE_BAK_DIR / "drive_backup_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("    -> Phase 3C Google Drive backup COMPLETE [PASS]")


def main():
    creds = Credentials.from_authorized_user_file(str(ROOT / "token.json"))
    sheets_svc = build("sheets", "v4", credentials=creds)
    drive_svc = build("drive", "v3", credentials=creds)
    backup_sheets(sheets_svc)
    backup_drive(drive_svc)


if __name__ == "__main__":
    main()
