import json
import glob
import os

cat_files = glob.glob(r"Dataset_BanglaBBQ_New\*\*_english.jsonl") + glob.glob(r"Dataset_BanglaBBQ_New\*\*eng*.jsonl")
for cf in sorted(cat_files):
    cat_name = os.path.basename(os.path.dirname(cf))
    print(f"\n=================== {cat_name} ===================")
    seen_q = set()
    with open(cf, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            q = rec.get("question_index")
            if q not in seen_q:
                seen_q.add(q)
                src = rec.get("additional_metadata", {}).get("source", "NO_SOURCE_FIELD")
                print(f"Q{q}: {src}")
