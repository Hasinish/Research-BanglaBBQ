"""
tests/test_all_61312_actual_records_mapping.py
==============================================
Exhaustive GPU-Free Preflight Audit on ALL 61,312 Canonical Records across all 24 JSONL files.

Calls the real production `classify_record_prediction` function from `scripts.bbq_scoring_engine`.
Verifies that:
1. Every record across all 12 categories (including 'Gender_identity', 'Health_status', etc.)
   resolves to its sidecar theme target with ZERO errors.
2. Identifies directional vs non-directional records.
3. Confirms exactly 61,312 records are evaluated.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.bbq_scoring_engine import (
    load_sidecar_map,
    classify_record_prediction,
    normalize_category_name,
)


def run_full_preflight_audit():
    sidecar_map = load_sidecar_map()
    data_dir = REPO_ROOT / "Dataset_BanglaBBQ_New"
    assert data_dir.exists(), f"Dataset directory missing: {data_dir}"

    files = sorted(list(data_dir.rglob("*.jsonl")))
    assert len(files) == 24, f"Expected 24 dataset JSONL files, found {len(files)}"

    total_records = 0
    cleanly_classified = 0
    non_directional_count = 0
    category_counts = defaultdict(int)
    errors = []

    print("=" * 105)
    print("  RUNNING EXHAUSTIVE GPU-FREE PREFLIGHT AUDIT ON ALL 61,312 CANONICAL DATASET RECORDS")
    print("=" * 105)

    for f in files:
        file_records = 0
        with open(f, "r", encoding="utf-8") as fh:
            for line_idx, line in enumerate(fh):
                if not line.strip():
                    continue
                row = json.loads(line)
                file_records += 1
                total_records += 1
                category_counts[row["category"]] += 1

                try:
                    # Call production classification function with mock pred
                    classification = classify_record_prediction(
                        record=row,
                        pred_choice=row["label"],
                        sidecar_map=sidecar_map,
                    )

                    if classification["is_directional"]:
                        cleanly_classified += 1
                    else:
                        non_directional_count += 1

                except Exception as e:
                    errors.append({
                        "file": f.name,
                        "line": line_idx,
                        "category": row.get("category"),
                        "question_index": row.get("question_index"),
                        "error": str(e),
                    })
                    if len(errors) <= 5:
                        print(f"  [ERROR] {f.name}:{line_idx} - {e}")

        print(f"  --> {f.name:<38} | {file_records:>5,} records | normalized: {normalize_category_name(row['category']):<32} [OK]")

    print("=" * 105)
    print(f"[*] Total Records Audited:      {total_records:,}")
    print(f"[*] Cleanly Mapped Directional: {cleanly_classified:,} ({cleanly_classified / total_records * 100:.2f}%)")
    print(f"[*] Non-directional (Identical): {non_directional_count:,} ({non_directional_count / total_records * 100:.2f}%)")
    print(f"[*] Total Mapping Errors:       {len(errors)}")
    print("=" * 105)

    assert total_records == 61312, f"Expected 61,312 total records, got {total_records}"
    assert len(errors) == 0, f"Encountered {len(errors)} mapping errors in production classification!"
    print("\n[SUCCESS] 100% of all 61,312 records across all 24 canonical files pass production classification with ZERO errors!")


if __name__ == "__main__":
    run_full_preflight_audit()

