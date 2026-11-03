import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

categories = [
    ("EducationalBackground", "Education"),
    ("Ethnicity", "Ethnicity"),
    ("HealthStatus", "HealthStatus"),
    ("MaritalStatus", "MaritalStatus"),
    ("OccupationalBackground", "OccupationalBackground"),
    ("Politics", "Politics"),
    ("Regional", "Regional"),
    ("Religion", "Religion"),
    ("SocialStatus", "SocialStatus")
]

print(f"{'Category':<25} | {'Lang':<4} | {'Total':<5} | {'Diff Context':<12} | {'Diff Q':<8} | {'Diff Label':<10}")
print("-" * 75)

for cat_dir, cat_suffix in categories:
    for lang in ["ENG", "BEN"]:
        canon_path = f"Dataset_BanglaBBQ_New/BanglaBBQ_{cat_dir}/BanglaBBQ_{lang}_{cat_suffix}.jsonl"
        fixed_path = f"fixed JsonL/BanglaBBQ_{lang}_{cat_suffix}_QA_fixed.jsonl"
        
        with open(canon_path, 'r', encoding='utf-8') as fc:
            crows = [json.loads(line) for line in fc]
        with open(fixed_path, 'r', encoding='utf-8') as ff:
            frows = [json.loads(line) for line in ff]
            
        diff_ctx = 0
        diff_q = 0
        diff_label = 0
        
        for i in range(len(crows)):
            if crows[i]['context'] != frows[i]['context']: diff_ctx += 1
            if crows[i]['question'] != frows[i]['question']: diff_q += 1
            if crows[i]['label'] != frows[i]['label']: diff_label += 1
            
        print(f"{cat_dir:<25} | {lang:<4} | {len(crows):<5} | {diff_ctx:<12} | {diff_q:<8} | {diff_label:<10}")
