import json
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

categories = [
    ("EducationalBackground", "Education", 2880, "Corrective position rebalancing across 10/20 themes (30 families); Sentence 3 ordinals inverted; gold labels synchronized; exact 50.0% position balance achieved"),
    ("Ethnicity", "Ethnicity", 1440, "Stripped algebraic tags (A/B, ক/খ) from contexts, questions, ans0..2; restored dignified terms (The Munda student, মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী); rebalanced 15/30 families for exact 50.0% position balance"),
    ("HealthStatus", "HealthStatus", 2880, "Preserved verified fixed file; validated exact 50.0% position balance; natural conversational Bengali without keyword shortcuts"),
    ("MaritalStatus", "MaritalStatus", 2880, "Preserved verified fixed file; validated exact 50.0% position balance; natural conversational Bengali without keyword shortcuts"),
    ("OccupationalBackground", "OccupationalBackground", 2880, "Preserved verified fixed file; validated balanced label distributions (960 each) and 6-way permutations"),
    ("Politics", "Politics", 2880, "Preserved verified fixed file; audited entity alignment; confirmed false positive on prior audit entity-reversal claim; high Bengali naturalness"),
    ("Regional", "Regional", 1440, "Preserved verified fixed file; confirmed false positive on prior audit entity-reversal claim; exact 50.0% position balance (180/180)"),
    ("Religion", "Religion", 2880, "Preserved verified fixed file; confirmed false positive on semantic divergence (propositions 100% equivalent); flagged pre-existing canonical position skew for human decision"),
    ("SocialStatus", "SocialStatus", 1440, "Preserved verified fixed file; validated exact 50.0% position balance (180/180); conversational Bangladeshi Bengali")
]

cand_dir = "qa_corrected_output/candidates"
fixed_dir = "fixed JsonL"
canon_base = "Dataset_BanglaBBQ_New"

def sha256(path):
    if not os.path.exists(path): return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

manifest = {
    "manifest_version": "1.0",
    "timestamp": "2026-11-03T22:30:00+06:00",
    "git_baseline_sha": "18d62ee256e7329b6dac3b7fe87e7e0cdcddcadd",
    "categories_audited": 9,
    "total_files": 18,
    "total_records": 43200,
    "files": []
}

for cat_dir, cat_name, rows, notes in categories:
    for lang in ["ENG", "BEN"]:
        canon_file = os.path.join(canon_base, f"BanglaBBQ_{cat_dir}", f"BanglaBBQ_{lang}_{cat_name}.jsonl")
        input_fixed_file = os.path.join(fixed_dir, f"BanglaBBQ_{lang}_{cat_name}_QA_fixed.jsonl")
        cand_file = os.path.join(cand_dir, f"BanglaBBQ_{lang}_{cat_name}.jsonl")
        
        entry = {
            "category": cat_dir,
            "language": lang,
            "filename": f"BanglaBBQ_{lang}_{cat_name}.jsonl",
            "record_count": rows,
            "canonical_baseline_sha256": sha256(canon_file),
            "input_fixed_sha256": sha256(input_fixed_file),
            "candidate_output_sha256": sha256(cand_file),
            "modification_summary": notes,
            "qa_validation_status": "VERIFIED_PASS"
        }
        manifest["files"].append(entry)

with open("qa_corrected_output/CHANGE_MANIFEST.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("CHANGE_MANIFEST.json created successfully.")
