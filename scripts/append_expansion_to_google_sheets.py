#!/usr/bin/env python3
"""Append approved Q11-Q20 expansion rows to live Google Sheets worksheets.

Appends rows 1442..2881 to the 6 target worksheets in the Master Spreadsheet
(1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY).
Sets rowCount to 2881, applies 96px row height, updates values, and performs
100% cell readback verification.
"""
import json
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"
SPREADSHEET_ID = "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY"

TARGET_SHEETS = [
    {
        "category": "Health Status",
        "en_jsonl": DATASET_ROOT / "BanglaBBQ_HealthStatus" / "BanglaBBQ_Health_Status_FINAL_english.jsonl",
        "bn_jsonl": DATASET_ROOT / "BanglaBBQ_HealthStatus" / "BanglaBBQ_Health_Status_FINAL_bengali.jsonl",
        "en_title": "BanglaBBQ_ENG_HealthStatus",
        "bn_title": "BanglaBBQ_BEN_HealthStatus",
        "en_gid": 577820949,
        "bn_gid": 1261981579,
    },
    {
        "category": "Marital Status",
        "en_jsonl": DATASET_ROOT / "BanglaBBQ_MaritalStatus" / "BanglaBBQ_MaritalStatus_FINAL_english.jsonl",
        "bn_jsonl": DATASET_ROOT / "BanglaBBQ_MaritalStatus" / "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl",
        "en_title": "BanglaBBQ_ENG_MaritalStatus",
        "bn_title": "BanglaBBQ_BEN_MaritalStatus",
        "en_gid": 2049623557,
        "bn_gid": 1929463163,
    },
    {
        "category": "Occupational Background",
        "en_jsonl": DATASET_ROOT / "BanglaBBQ_OccupationalBackground" / "BanglaBBQ_Occupational_Background_FINAL_english.jsonl",
        "bn_jsonl": DATASET_ROOT / "BanglaBBQ_OccupationalBackground" / "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl",
        "en_title": "BanglaBBQ_ENG_OccupationalBackground",
        "bn_title": "BanglaBBQ_BEN_OccupationalBackground",
        "en_gid": 1499154542,
        "bn_gid": 934780717,
    },
]

HEADER = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id"
]

def format_row(r):
    return [
        int(r["example_id"]),
        int(r["question_index"]),
        str(r["context_condition"]),
        str(r["question_polarity"]),
        str(r["type"]),
        str(r["context"]),
        str(r["question"]),
        str(r["ans0"]),
        str(r["ans1"]),
        str(r["ans2"]),
        int(r["label"]),
        json.dumps(r["answer_info"], ensure_ascii=False, separators=(",", ":")),
        json.dumps(r["additional_metadata"], ensure_ascii=False, separators=(",", ":")),
        str(r["category"]),
        int(r["id"])
    ]

def load_expansion_rows(jsonl_path: Path):
    with jsonl_path.open("r", encoding="utf-8") as f:
        all_rows = [json.loads(line.strip()) for line in f if line.strip()]
    assert len(all_rows) == 2880, f"Expected 2880 rows in {jsonl_path.name}, got {len(all_rows)}"
    # Rows 1440..2879 (example_id 1440..2879)
    exp_rows = [format_row(r) for r in all_rows[1440:]]
    assert len(exp_rows) == 1440, f"Expected 1440 expansion rows, got {len(exp_rows)}"
    assert exp_rows[0][0] == 1440
    assert exp_rows[-1][0] == 2879
    return exp_rows, all_rows

def main():
    print("=" * 70)
    print("GOOGLE SHEETS EXPANSION: APPEND ROWS 1442..2881 (Q11-Q20)")
    print("=" * 70)

    creds = Credentials.from_authorized_user_file(ROOT / "token.json")
    service = build("sheets", "v4", credentials=creds)

    meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_map = {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}

    for item in TARGET_SHEETS:
        cat_name = item["category"]
        print(f"\n====================================================================")
        print(f"PROCESSING CATEGORY: {cat_name}")
        print(f"====================================================================")

        for lang, jsonl_path, title, expected_gid in [
            ("English", item["en_jsonl"], item["en_title"], item["en_gid"]),
            ("Bengali", item["bn_jsonl"], item["bn_title"], item["bn_gid"]),
        ]:
            print(f"\n[+] Synchronizing '{title}' (GID: {expected_gid})...")
            actual_gid = sheet_map.get(title)
            assert actual_gid == expected_gid, f"GID mismatch for {title}: {actual_gid} != {expected_gid}"

            exp_formatted, all_canonical = load_expansion_rows(jsonl_path)

            # Step 1: Expand Grid to 2881 rows and format row height
            print("    1. Updating grid properties to 2,881 rows & setting 96px row height...")
            requests = [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": expected_gid,
                            "gridProperties": {
                                "rowCount": 2881,
                                "columnCount": 15,
                                "frozenRowCount": 1,
                            },
                        },
                        "fields": "gridProperties(rowCount,columnCount,frozenRowCount)",
                    }
                },
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": expected_gid,
                            "dimension": "ROWS",
                            "startIndex": 1441,
                            "endIndex": 2881,
                        },
                        "properties": {
                            "pixelSize": 96,
                        },
                        "fields": "pixelSize",
                    }
                },
            ]
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={"requests": requests}
            ).execute()
            print("       Grid expanded to 2,881 rows; row height 96px applied.")

            # Step 2: Write rows in batches to range A1442:O2881
            print("    2. Writing rows 1442..2881 in batches...")
            batch_size = 500
            for start_idx in range(0, len(exp_formatted), batch_size):
                end_idx = min(start_idx + batch_size, len(exp_formatted))
                batch_data = exp_formatted[start_idx:end_idx]
                sheet_start_row = 1442 + start_idx
                sheet_end_row = 1442 + end_idx - 1
                target_range = f"'{title}'!A{sheet_start_row}:O{sheet_end_row}"

                service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=target_range,
                    valueInputOption="RAW",
                    body={"values": batch_data}
                ).execute()
                print(f"       Written range {target_range} ({len(batch_data)} rows)")
                time.sleep(0.5)

            # Step 3: Full Readback & Parity Verification across all 2,880 data rows
            print("    3. Performing 100% full live readback verification (A1:O2881)...")
            res = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"'{title}'!A1:O2881",
                valueRenderOption="UNFORMATTED_VALUE"
            ).execute()
            live_rows = res.get("values", [])
            assert len(live_rows) == 2881, f"Expected 2881 rows, got {len(live_rows)}"
            assert live_rows[0] == HEADER, f"Header row mismatch: {live_rows[0]}"

            mismatches = 0
            total_cells = 2880 * 15
            for r_idx in range(1, 2881):
                live_r = live_rows[r_idx]
                canon_r = format_row(all_canonical[r_idx - 1])
                for c_idx in range(15):
                    lv = live_r[c_idx] if c_idx < len(live_r) else ""
                    cv = canon_r[c_idx]

                    if c_idx in (0, 1, 10, 14):
                        try:
                            if int(lv) != int(cv):
                                mismatches += 1
                        except Exception:
                            mismatches += 1
                    elif c_idx in (11, 12):
                        try:
                            if json.loads(lv) != json.loads(cv):
                                mismatches += 1
                        except Exception:
                            if str(lv) != str(cv):
                                mismatches += 1
                    else:
                        if str(lv) != str(cv):
                            mismatches += 1

            parity_pct = ((total_cells - mismatches) / total_cells) * 100.0
            print(f"       Data Cell Parity: {total_cells - mismatches}/{total_cells} cells ({parity_pct:.4f}%)")
            assert mismatches == 0, f"Found {mismatches} mismatches in '{title}'!"
            print(f"       PASS: 100% BIT-FOR-BIT LIVE PARITY VERIFIED FOR '{title}'")
            time.sleep(1.0)

    print("\n" + "=" * 70)
    print("ALL SIX WORKSHEETS SUCCESSFULLY EXPANDED AND VERIFIED AT 100% LIVE PARITY!")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
