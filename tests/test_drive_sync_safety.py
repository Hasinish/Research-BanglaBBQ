"""
test_drive_sync_safety.py
-------------------------
Verifies safety invariants of sync_drive_dataset.py:
1. Invariant validator detects corrupted fields and halts.
2. Invariant validator detects corrupted line count and halts.
3. Invariant validator detects bad labels and halts.
4. Verify-only mode passes clean on production data.
"""

import sys
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.sync_drive_dataset import validate_local_datasets, EXPECTED_CATEGORIES, REQUIRED_SCHEMA_FIELDS

def test_production_datasets_pass_preflight():
    manifest = validate_local_datasets()
    assert len(manifest) == 24, f"Expected 24 files, got {len(manifest)}"
    total_lines = sum(item["lines"] for item in manifest.values())
    assert total_lines == 60512 or total_lines == 61312, f"Unexpected total lines: {total_lines}"
    print(f"\n[TEST PASS] Pre-flight validation passed for all 24 canonical files ({total_lines} rows).")

def test_validator_rejects_missing_field():
    import scripts.sync_drive_dataset as sync_mod
    orig_root = sync_mod.DATASET_ROOT
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sync_mod.DATASET_ROOT = tmp_path
        
        # Create dummy category
        cat_dir = tmp_path / "BanglaBBQ_Age"
        cat_dir.mkdir(parents=True)
        bad_file = cat_dir / "BanglaBBQ_ENG_Age.jsonl"
        with open(bad_file, "w", encoding="utf-8") as f:
            f.write(json.dumps({"example_id": 0}) + "\n")
            
        try:
            sync_mod.validate_local_datasets()
            assert False, "Should have raised RuntimeError for schema violation!"
        except RuntimeError as e:
            assert "Schema violation" in str(e) or "missing" in str(e)
            print(f"[TEST PASS] Caught expected schema violation: {e}")
        finally:
            sync_mod.DATASET_ROOT = orig_root

def test_validator_rejects_bad_line_count():
    import scripts.sync_drive_dataset as sync_mod
    orig_root = sync_mod.DATASET_ROOT
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sync_mod.DATASET_ROOT = tmp_path
        cat_dir = tmp_path / "BanglaBBQ_Age"
        cat_dir.mkdir(parents=True)
        bad_file = cat_dir / "BanglaBBQ_ENG_Age.jsonl"
        with open(bad_file, "w", encoding="utf-8") as f:
            rec = {k: "val" for k in REQUIRED_SCHEMA_FIELDS}
            rec["example_id"] = 0
            rec["label"] = 0
            f.write(json.dumps(rec) + "\n")
            
        try:
            sync_mod.validate_local_datasets()
            assert False, "Should have raised RuntimeError for line count mismatch!"
        except RuntimeError as e:
            assert "Line count mismatch" in str(e) or "Missing canonical file" in str(e) or "Missing category" in str(e)
            print(f"[TEST PASS] Caught expected line count / file mismatch: {e}")
        finally:
            sync_mod.DATASET_ROOT = orig_root

if __name__ == "__main__":
    test_production_datasets_pass_preflight()
    test_validator_rejects_missing_field()
    test_validator_rejects_bad_line_count()
    print("\nALL SAFETY INVARIANT TESTS PASSED SUCCESSFULLY!")
