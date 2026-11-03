import json
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

fixed_dir = "fixed JsonL"
cand_dir = "qa_corrected_output/candidates"
os.makedirs(cand_dir, exist_ok=True)

remaining = [
    ("HealthStatus", "HealthStatus"),
    ("MaritalStatus", "MaritalStatus"),
    ("OccupationalBackground", "OccupationalBackground"),
    ("Politics", "Politics"),
    ("Regional", "Regional"),
    ("Religion", "Religion"),
    ("SocialStatus", "SocialStatus")
]

for src_name, dst_name in remaining:
    for lang in ["ENG", "BEN"]:
        src_file = os.path.join(fixed_dir, f"BanglaBBQ_{lang}_{src_name}_QA_fixed.jsonl")
        dst_file = os.path.join(cand_dir, f"BanglaBBQ_{lang}_{dst_name}.jsonl")
        shutil.copy2(src_file, dst_file)
        print(f"Copied {src_file} -> {dst_file}")

print("\nAll 18 candidates now exist in qa_corrected_output/candidates/")
