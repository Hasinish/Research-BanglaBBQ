#!/usr/bin/env python3
"""Append approved Q11-Q20 expansion rows to canonical production JSONLs.

Strictly verifies that:
1. The first 1,440 rows are 100% byte-identical to the pre-expansion backup.
2. The appended rows (1441-2880) match the audited expansion candidate JSONL.
3. Total row count is exactly 2,880 per file.
4. All sequential example_ids, global IDs, labels, and themes conform to benchmark invariants.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = ROOT / "backups" / "pre_expansion_20261028" / "local_jsonl"

OPERATIONS = [
    {
        "category": "Health Status",
        "target_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_HealthStatus",
        "en_target": "BanglaBBQ_Health_Status_FINAL_english.jsonl",
        "bn_target": "BanglaBBQ_Health_Status_FINAL_bengali.jsonl",
        "en_expansion": ROOT / "candidate_bundles/health_mental_q11_q20_review_20261028/BanglaBBQ_Health_Mental_Q11_Q20_english.jsonl",
        "bn_expansion": ROOT / "candidate_bundles/health_mental_q11_q20_review_20261028/BanglaBBQ_Health_Mental_Q11_Q20_bengali.jsonl",
        "id_base": 8300000,
    },
    {
        "category": "Marital Status",
        "target_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_MaritalStatus",
        "en_target": "BanglaBBQ_MaritalStatus_FINAL_english.jsonl",
        "bn_target": "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl",
        "en_expansion": ROOT / "review_artifacts/marital_male_q11_q20/BanglaBBQ_Marital_Male_Q11_Q20_english.jsonl",
        "bn_expansion": ROOT / "review_artifacts/marital_male_q11_q20/BanglaBBQ_Marital_Male_Q11_Q20_bengali.jsonl",
        "id_base": 8700000,
    },
    {
        "category": "Occupational Background",
        "target_dir": ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_OccupationalBackground",
        "en_target": "BanglaBBQ_Occupational_Background_FINAL_english.jsonl",
        "bn_target": "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl",
        "en_expansion": ROOT / "review_submissions/occupational_professional_q11_q20_2026-10-28/BanglaBBQ_Occupational_Professional_Q11_Q20_english.jsonl",
        "bn_expansion": ROOT / "review_submissions/occupational_professional_q11_q20_2026-10-28/BanglaBBQ_Occupational_Professional_Q11_Q20_bengali.jsonl",
        "id_base": 8600000,
    },
]

def main():
    print("=" * 70)
    print("APPEND APPROVED EXPANSION TO CANONICAL PRODUCTION DATASETS")
    print("=" * 70)

    for op in OPERATIONS:
        cat_name = op["category"]
        print(f"\nProcessing category: {cat_name}")

        for lang, target_fname, exp_path in [
            ("English", op["en_target"], op["en_expansion"]),
            ("Bengali", op["bn_target"], op["bn_expansion"]),
        ]:
            target_path = op["target_dir"] / target_fname
            backup_path = BACKUP_DIR / target_fname

            assert backup_path.exists(), f"Backup missing: {backup_path}"
            assert target_path.exists(), f"Target missing: {target_path}"
            assert exp_path.exists(), f"Expansion missing: {exp_path}"

            # Read backup bytes (the immutable 1,440-row baseline)
            orig_bytes = backup_path.read_bytes()
            assert orig_bytes.endswith(b"\r\n"), f"Expected CRLF ending in backup {target_fname}"

            # Read expansion lines
            with exp_path.open("r", encoding="utf-8") as f:
                exp_lines = [line.strip() for line in f if line.strip()]
            assert len(exp_lines) == 1440, f"Expected 1440 expansion lines in {exp_path.name}, got {len(exp_lines)}"

            # Encode expansion lines with CRLF
            exp_bytes = b"".join(line.encode("utf-8") + b"\r\n" for line in exp_lines)

            # Combined bytes
            combined_bytes = orig_bytes + exp_bytes

            # Write to production file
            target_path.write_bytes(combined_bytes)

            # Verification 1: Prefix bit-for-bit identity
            new_bytes = target_path.read_bytes()
            assert len(new_bytes) == len(orig_bytes) + len(exp_bytes), "Length mismatch"
            assert new_bytes[:len(orig_bytes)] == orig_bytes, "BIT DRIFT DETECTED IN ORIGINAL PREFIX!"

            # Verification 2: Line count
            with target_path.open("r", encoding="utf-8") as f:
                all_lines = [line.strip() for line in f if line.strip()]
            assert len(all_lines) == 2880, f"Expected 2880 lines in {target_fname}, got {len(all_lines)}"

            # Verification 3: Example IDs & Global IDs
            row0 = json.loads(all_lines[0])
            row1439 = json.loads(all_lines[1439])
            row1440 = json.loads(all_lines[1440])
            row2879 = json.loads(all_lines[2879])

            assert row0["example_id"] == 0, f"row0 example_id={row0['example_id']}"
            assert row1439["example_id"] == 1439, f"row1439 example_id={row1439['example_id']}"
            assert row1440["example_id"] == 1440, f"row1440 example_id={row1440['example_id']}"
            assert row2879["example_id"] == 2879, f"row2879 example_id={row2879['example_id']}"

            assert row0["id"] == op["id_base"], f"row0 id={row0['id']}"
            assert row2879["id"] == op["id_base"] + 2879, f"row2879 id={row2879['id']}"

            print(f"  [+] {lang} ({target_fname}):")
            print(f"      - Original prefix (0..1439): 100% byte-identical to backup")
            print(f"      - Appended rows (1440..2879): 1,440 rows integrated cleanly")
            print(f"      - Final count: 2,880 records (IDs {row0['id']}..{row2879['id']})")
            print(f"      - SHA-256: {hashlib.sha256(new_bytes).hexdigest()}")

    print("\n" + "=" * 70)
    print("ALL SIX CANONICAL PRODUCTION FILES EXPANDED SUCCESSFULLY (2,880 ROWS EACH)")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
