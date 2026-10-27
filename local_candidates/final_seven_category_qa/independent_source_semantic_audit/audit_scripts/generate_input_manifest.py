import os
import json
import hashlib
import subprocess

BASE_DIR = r"d:\Research-BanglaBBQ"
QA_DIR = os.path.join(BASE_DIR, "local_candidates", "final_seven_category_qa")
AUDIT_DIR = os.path.join(QA_DIR, "independent_source_semantic_audit")

def get_git_head():
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=BASE_DIR, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        return f"UNKNOWN: {e}"

def compute_file_stats(filepath):
    if not os.path.exists(filepath):
        return {
            "exists": False,
            "error": "File not found"
        }
    hasher = hashlib.sha256()
    size = os.path.getsize(filepath)
    line_count = 0
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    # count lines if text/jsonl
    if filepath.endswith(".jsonl") or filepath.endswith(".csv") or filepath.endswith(".md"):
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for _ in f:
                line_count += 1
    return {
        "exists": True,
        "path": os.path.relpath(filepath, BASE_DIR).replace("\\", "/"),
        "size_bytes": size,
        "line_count": line_count,
        "sha256": hasher.hexdigest()
    }

def main():
    head_sha = get_git_head()
    
    files_to_track = {
        "positional_candidates": [
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Health_Status_FINAL_english.jsonl"),
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl"),
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Regional_FINAL_english.jsonl"),
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Regional_FINAL_bengali.jsonl"),
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Ethnicity_FINAL_english.jsonl"),
            os.path.join(QA_DIR, "candidates", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl"),
        ],
        "content_prototypes": [
            os.path.join(QA_DIR, "prototypes", "Health_Status_Q02_Q04_Q05_Q07_prototype_english.jsonl"),
            os.path.join(QA_DIR, "prototypes", "Health_Status_Q02_Q04_Q05_Q07_prototype_bengali.jsonl"),
            os.path.join(QA_DIR, "prototypes", "Physical_Appearance_Q02_prototype_english.jsonl"),
            os.path.join(QA_DIR, "prototypes", "Physical_Appearance_Q02_prototype_bengali.jsonl"),
            os.path.join(QA_DIR, "prototypes", "Social_Status_Q07_V3_prototype_english.jsonl"),
            os.path.join(QA_DIR, "prototypes", "Social_Status_Q07_V3_prototype_bengali.jsonl"),
        ],
        "research_documentation": [
            os.path.join(QA_DIR, "source_audit.csv"),
            os.path.join(QA_DIR, "linguistic_review_queue.csv"),
            os.path.join(QA_DIR, "master_qa_summary.md"),
            os.path.join(QA_DIR, "human_validation_protocol.md"),
            os.path.join(QA_DIR, "mental_health_coverage_plan.md"),
            os.path.join(QA_DIR, "reports", "independent_review_remediation_report.md"),
            os.path.join(QA_DIR, "reports", "source_and_semantic_repair_report.md"),
        ]
    }
    
    manifest = {
        "timestamp": "2026-10-28T01:53:00+06:00",
        "baseline_commit_sha": head_sha,
        "files": {}
    }
    
    for category, paths in files_to_track.items():
        manifest["files"][category] = []
        for p in paths:
            stats = compute_file_stats(p)
            manifest["files"][category].append(stats)
            print(f"[{category}] {os.path.basename(p)}: size={stats.get('size_bytes')}, lines={stats.get('line_count')}, sha256={stats.get('sha256')}")

    out_path = os.path.join(AUDIT_DIR, "input_manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest successfully written to: {out_path}")

if __name__ == "__main__":
    main()
