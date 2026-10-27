import os
import sys
import json
import hashlib
from datetime import datetime, timezone

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PRODUCTION_DIR = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New")
OUTPUT_MANIFEST = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "baseline_manifest.json")

CATEGORIES = [
    ("Physical Appearance", "BanglaBBQ_PhysicalAppearance", "BanglaBBQ_Physical_Appearance_FINAL_english.jsonl", "BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl", "984262367", "934839633"),
    ("Social Status", "BanglaBBQ_SocialStatus", "BanglaBBQ_SocialStatus_FINAL_english.jsonl", "BanglaBBQ_SocialStatus_FINAL_bengali.jsonl", "1061280109", "1761692098"),
    ("Health Status", "BanglaBBQ_HealthStatus", "BanglaBBQ_Health_Status_FINAL_english.jsonl", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl", "577820949", "1261981579"),
    ("Regional Affiliation", "BanglaBBQ_Regional", "BanglaBBQ_Regional_FINAL_english.jsonl", "BanglaBBQ_Regional_FINAL_bengali.jsonl", "1321419120", "786932138"),
    ("Ethnicity", "BanglaBBQ_Ethnicity", "BanglaBBQ_Ethnicity_FINAL_english.jsonl", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl", "210887456", "1845601757"),
    ("Occupational Background", "BanglaBBQ_OccupationalBackground", "BanglaBBQ_Occupational_Background_FINAL_english.jsonl", "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl", "1499154542", "934780717"),
    ("Marital Status", "BanglaBBQ_MaritalStatus", "BanglaBBQ_MaritalStatus_FINAL_english.jsonl", "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl", "2049623557", "1929463163"),
]

EXPECTED_SCHEMA_KEYS = set([
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id"
])

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def validate_schema_and_count(filepath):
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            keys = set(rec.keys())
            if keys != EXPECTED_SCHEMA_KEYS or len(rec.keys()) != 15:
                raise ValueError(f"Schema mismatch at row {idx} in {filepath}: missing {EXPECTED_SCHEMA_KEYS - keys}, extra {keys - EXPECTED_SCHEMA_KEYS}")
            count += 1
    return count

def main():
    manifest = {
        "metadata": {
            "title": "BanglaBBQ Non-Mental-Health Baseline Manifest",
            "generation_timestamp": datetime.now(timezone.utc).isoformat(),

            "source_git_commit": "6967700fcb34dd83a0ba2af78bad2d4fcfd0ed65",
            "active_review_branch": "review/non-mental-health-repair-20261028",
            "google_spreadsheet_id": "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY",
            "google_spreadsheet_import_date": "2026-10-26",
            "total_categories": len(CATEGORIES),
            "expected_records_per_language": 10080,
            "expected_total_records": 20160,
            "policy": "NON-DESTRUCTIVE - ZERO MUTATIONS TO Dataset_BanglaBBQ_New OR LIVE SPREADSHEETS"
        },
        "protected_boundaries": {
            "historical_thesis_dataset": {
                "path": "Dataset_ BanglaBBQ_Old/",
                "protection": "READ-ONLY IMMUTABLE (Preserve byte-for-byte lineage)"
            },
            "canonical_production_dataset": {
                "path": "Dataset_BanglaBBQ_New/",
                "protection": "PROTECTED - No direct writes authorized in this task"
            },
            "master_google_spreadsheet": {
                "spreadsheet_id": "1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY",
                "protection": "PROTECTED - No live cell edits authorized in this task"
            },
            "mental_health_expansion": {
                "reserved_category": "Health Status Themes Q11-Q20 (IDs 1440-2879)",
                "protection": "STRICT EXCLUSION - Managed in separate designated research chat"
            },
            "marital_status_male_expansion": {
                "reserved_category": "Marital Status Themes Q11-Q20",
                "protection": "STRICT EXCLUSION - Managed in separate designated research chat"
            },
            "occupational_background_expansion": {
                "reserved_category": "Occupational Background Themes Q11-Q20",
                "protection": "STRICT EXCLUSION - Managed in separate designated research chat"
            },
            "completed_categories_regression_only": {
                "categories": ["Age", "Gender Identity", "Educational Background", "Religion", "Politics"],
                "protection": "READ-ONLY REGRESSION MONITORING - No unnecessary rewrites"
            }
        },
        "baseline_files": {}
    }

    for cat_name, folder_name, en_file, bn_file, sheet_id_en, sheet_id_bn in CATEGORIES:
        en_path = os.path.join(PRODUCTION_DIR, folder_name, en_file)
        bn_path = os.path.join(PRODUCTION_DIR, folder_name, bn_file)

        en_hash = hash_file(en_path)
        bn_hash = hash_file(bn_path)

        en_count = validate_schema_and_count(en_path)
        bn_count = validate_schema_and_count(bn_path)

        manifest["baseline_files"][cat_name] = {
            "folder": folder_name,
            "english": {
                "filename": en_file,
                "relative_path": os.path.relpath(en_path, REPO_ROOT).replace("\\", "/"),
                "sha256": en_hash,
                "row_count": en_count,
                "google_sheet_tab_id": sheet_id_en,
                "schema_valid": True
            },
            "bengali": {
                "filename": bn_file,
                "relative_path": os.path.relpath(bn_path, REPO_ROOT).replace("\\", "/"),
                "sha256": bn_hash,
                "row_count": bn_count,
                "google_sheet_tab_id": sheet_id_bn,
                "schema_valid": True
            }
        }
        print(f"Verified {cat_name}: EN={en_count} rows, BN={bn_count} rows, 15-key schema OK.")

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nBaseline manifest written to: {OUTPUT_MANIFEST}")

if __name__ == "__main__":
    main()
