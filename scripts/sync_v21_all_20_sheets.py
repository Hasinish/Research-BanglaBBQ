#!/usr/bin/env python3
"""
sync_v21_all_20_sheets.py
-------------------------
Dedicated V2.1 Master Google Spreadsheet Synchronizer & Full Cell-Level Verifier.

Synchronizes all 20 promoted JSONL files (10 categories x 2 languages = 46,080 rows = 691,200 data cells)
from Dataset_BanglaBBQ_New/ into existing worksheets in Master Spreadsheet
1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY.

Strictly preserves Age, Gender, sheet IDs, grid dimensions, frozen rows, conditional formatting,
column widths, and all non-target review/backup worksheets. Reads back ALL 691,200 data cells
and headers after upload to verify 100% live parity.
"""

import json
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"
REPORT_OUT = ROOT / "audits" / "v21_production_promotion_20261117" / "sheets_sync_verification_report.json"

SPREADSHEET_ID = "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY"

HEADER = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id"
]

SHEETS_MAP = [
    ("BanglaBBQ_ENG_Education", "BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl", 2880),
    ("BanglaBBQ_BEN_Education", "BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl", 2880),
    ("BanglaBBQ_ENG_Ethnicity", "BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl", 1440),
    ("BanglaBBQ_BEN_Ethnicity", "BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl", 1440),
    ("BanglaBBQ_ENG_HealthStatus", "BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl", 2880),
    ("BanglaBBQ_BEN_HealthStatus", "BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl", 2880),
    ("BanglaBBQ_ENG_MaritalStatus", "BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl", 2880),
    ("BanglaBBQ_BEN_MaritalStatus", "BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl", 2880),
    ("BanglaBBQ_ENG_OccupationalBackground", "BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl", 2880),
    ("BanglaBBQ_BEN_OccupationalBackground", "BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl", 2880),
    ("BanglaBBQ_ENG_PhysicalAppearance", "BanglaBBQ_PhysicalAppearance/BanglaBBQ_ENG_PhysicalAppearance.jsonl", 1440),
    ("BanglaBBQ_BEN_PhysicalAppearance", "BanglaBBQ_PhysicalAppearance/BanglaBBQ_BEN_PhysicalAppearance.jsonl", 1440),
    ("BanglaBBQ_ENG_Politics", "BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl", 2880),
    ("BanglaBBQ_BEN_Politics", "BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl", 2880),
    ("BanglaBBQ_ENG_Regional", "BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl", 1440),
    ("BanglaBBQ_BEN_Regional", "BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl", 1440),
    ("BanglaBBQ_ENG_Religion", "BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl", 2880),
    ("BanglaBBQ_BEN_Religion", "BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl", 2880),
    ("BanglaBBQ_ENG_SocialStatus", "BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl", 1440),
    ("BanglaBBQ_BEN_SocialStatus", "BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl", 1440),
]

UNTOUCHED_SHEETS = [
    "BanglaBBQ_ENG_Age", "BanglaBBQ_BEN_Age",
    "BanglaBBQ_ENG_Gender", "BanglaBBQ_BEN_Gender"
]


def execute_with_retry(func, max_retries=6, initial_backoff=2):
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status in (429, 500, 503) and attempt < max_retries - 1:
                wait = initial_backoff * (2 ** attempt)
                print(f"    [!] HTTP {e.resp.status}; backing off {wait}s...")
                time.sleep(wait)
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                wait = initial_backoff * (2 ** attempt)
                print(f"    [!] Error ({e}); backing off {wait}s...")
                time.sleep(wait)
            else:
                raise


def format_row(r):
    row_vals = []
    for col in HEADER:
        val = r.get(col, "")
        if isinstance(val, (dict, list)):
            row_vals.append(json.dumps(val, ensure_ascii=False))
        else:
            row_vals.append(val)
    return row_vals


def norm_cell(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def get_sheet_metadata_snapshot(service):
    meta = execute_with_retry(lambda: service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        fields="spreadsheetId,sheets(properties,conditionalFormats,data.columnMetadata)"
    ).execute())
    snap = {}
    for s in meta["sheets"]:
        p = s["properties"]
        snap[p["title"]] = {
            "sheetId": p["sheetId"],
            "gridProperties": p.get("gridProperties", {}),
            "conditionalFormats": s.get("conditionalFormats", []),
            "columnMetadata": s.get("data", [{}])[0].get("columnMetadata", []) if s.get("data") else [],
        }
    return snap


def main():
    creds = Credentials.from_authorized_user_file(str(ROOT / "token.json"))
    service = build("sheets", "v4", credentials=creds)

    print("[*] Stage 1: Verifying all 20 target worksheets + pre-sync metadata...")
    pre_snap = get_sheet_metadata_snapshot(service)
    for title, rel_path, exp_rows in SHEETS_MAP:
        assert title in pre_snap, f"FATAL: Target worksheet missing: {title}"
        gp = pre_snap[title]["gridProperties"]
        assert gp.get("rowCount") == exp_rows + 1 and gp.get("columnCount") == 15, (
            f"Grid dimension mismatch on {title}: {gp} (expected {exp_rows + 1}x15)"
        )
    for u in UNTOUCHED_SHEETS:
        assert u in pre_snap, f"Missing untouched sheet {u}"
    print("    -> All 20 target worksheets & grid bounds verified [PASS]")

    print("\n[*] Stage 2: Uploading 20 V2.1 canonical files into Google Sheets (RAW)...")
    print("=" * 90)
    print(f"{'Worksheet Title':<38} {'ID':<12} {'Rows':<6} {'Cells':<8} {'Upload':<8}")
    print("-" * 90)

    local_cache = {}
    total_updated_cells = 0
    for title, rel_path, exp_rows in SHEETS_MAP:
        fpath = DATASET_ROOT / rel_path
        records = [json.loads(l) for l in fpath.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(records) == exp_rows
        data_rows = [format_row(r) for r in records]
        local_cache[title] = data_rows

        # Verify existing header matches
        hdr_res = execute_with_retry(lambda t=title: service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{t}'!A1:O1"
        ).execute())
        actual_hdr = hdr_res.get("values", [[]])[0]
        assert actual_hdr == HEADER, f"Header mismatch on {title}: {actual_hdr}"

        rng = f"'{title}'!A2:O{exp_rows + 1}"
        res = execute_with_retry(lambda r=rng, dr=data_rows: service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=r,
            valueInputOption="RAW",
            body={"values": dr}
        ).execute())

        upd = res.get("updatedCells", 0)
        assert upd == exp_rows * 15, f"Upload cell mismatch on {title}: {upd} vs {exp_rows * 15}"
        total_updated_cells += upd
        sid = pre_snap[title]["sheetId"]
        print(f"{title:<38} {sid:<12} {exp_rows:<6} {upd:<8} PASS")
        time.sleep(1.5)

    print("=" * 90)
    print(f"Total Uploaded Data Cells: {total_updated_cells:,} / 691,200")

    print("\n[*] Stage 3: Exhaustive Full-Cell Live Readback Verification (ALL 691,200 Data Cells + Headers + Metadata)...")
    post_snap = get_sheet_metadata_snapshot(service)
    report = {
        "spreadsheet_id": SPREADSHEET_ID,
        "overall_status": "PASS",
        "total_expected_data_cells": 691200,
        "total_verified_data_cells": 0,
        "total_cell_mismatches": 0,
        "worksheets": {},
        "untouched_age_gender": {}
    }

    for u in UNTOUCHED_SHEETS:
        unchanged = (pre_snap[u] == post_snap[u])
        if not unchanged:
            report["overall_status"] = "FAIL"
        report["untouched_age_gender"][u] = {"sheetId": post_snap[u]["sheetId"], "metadata_unchanged": unchanged}

    for title, rel_path, exp_rows in SHEETS_MAP:
        rng = f"'{title}'!A1:O{exp_rows + 1}"
        res = execute_with_retry(lambda r=rng: service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=r,
            valueRenderOption="UNFORMATTED_VALUE"
        ).execute())
        vals = res.get("values", [])
        expected_rows = local_cache[title]

        hdr_ok = (len(vals) == exp_rows + 1 and vals[0] == HEADER)
        cell_mismatches = []
        if len(vals) == exp_rows + 1:
            for row_idx in range(exp_rows):
                remote_row = vals[row_idx + 1]
                local_row = expected_rows[row_idx]
                if len(remote_row) != 15:
                    cell_mismatches.append({"row": row_idx + 2, "col": "ALL", "error": f"len={len(remote_row)}"})
                    continue
                for col_idx in range(15):
                    if norm_cell(remote_row[col_idx]) != norm_cell(local_row[col_idx]):
                        if len(cell_mismatches) < 20:
                            cell_mismatches.append({
                                "row": row_idx + 2, "col": HEADER[col_idx],
                                "expected": norm_cell(local_row[col_idx])[:80],
                                "actual": norm_cell(remote_row[col_idx])[:80],
                            })

        meta_preserved = (pre_snap[title] == post_snap[title])
        sheet_pass = hdr_ok and (len(vals) == exp_rows + 1) and (len(cell_mismatches) == 0) and meta_preserved
        if not sheet_pass:
            report["overall_status"] = "FAIL"

        verified_cells = exp_rows * 15 if len(cell_mismatches) == 0 else (exp_rows * 15 - len(cell_mismatches))
        report["total_verified_data_cells"] += verified_cells
        report["total_cell_mismatches"] += len(cell_mismatches)

        report["worksheets"][title] = {
            "sheetId": post_snap[title]["sheetId"],
            "status": "PASS" if sheet_pass else "FAIL",
            "expected_data_rows": exp_rows,
            "actual_total_rows_read": len(vals),
            "header_ok": hdr_ok,
            "metadata_formatting_preserved": meta_preserved,
            "cell_mismatches_count": len(cell_mismatches),
            "sample_mismatches": cell_mismatches,
        }
        print(f"    -> {title:<38}: rows={len(vals)-1}/{exp_rows}, mismatches={len(cell_mismatches)}, meta_preserved={meta_preserved} [{'PASS' if sheet_pass else 'FAIL'}]")
        time.sleep(0.5)

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 90)
    print(f"FINAL SHEETS PARITY STATUS: {report['overall_status']} | Verified Cells: {report['total_verified_data_cells']:,} / 691,200 | Mismatches: {report['total_cell_mismatches']}")
    if report["overall_status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
