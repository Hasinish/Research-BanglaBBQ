import json
import glob
import os

cats = [
    "BanglaBBQ_PhysicalAppearance",
    "BanglaBBQ_SocialStatus",
    "BanglaBBQ_HealthStatus",
    "BanglaBBQ_Regional",
    "BanglaBBQ_Ethnicity",
    "BanglaBBQ_OccupationalBackground",
    "BanglaBBQ_MaritalStatus"
]

for cat in cats:
    matches = glob.glob(f"Dataset_BanglaBBQ_New/{cat}/*english.jsonl")
    if not matches:
        continue
    fpath = matches[0]
    print(f"\n=================== {cat} ({os.path.basename(fpath)}) ===================")
    seen = set()
    with open(fpath, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            q = r.get("question_index")
            if q not in seen:
                seen.add(q)
                src = r.get("additional_metadata", {}).get("source")
                print(f"Q{q}: {src}")
