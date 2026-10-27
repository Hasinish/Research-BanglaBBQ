import os
import sys
import json
import csv
import hashlib

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROD_DIR = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New")
CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")
OUTPUT_CSV = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "reports", "change_ledger.csv")

PAIRS = [
    ("Health Status", "BanglaBBQ_HealthStatus", "BanglaBBQ_Health_Status_FINAL_english.jsonl", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl",
     "BanglaBBQ_Health_Status_repaired_english.jsonl", "BanglaBBQ_Health_Status_repaired_bengali.jsonl",
     "Position shortcut repair (180:180 balance) + contagion confounder prototype replacement in Q02, Q04, Q05, Q07"),
    ("Regional Affiliation", "BanglaBBQ_Regional", "BanglaBBQ_Regional_FINAL_english.jsonl", "BanglaBBQ_Regional_FINAL_bengali.jsonl",
     "BanglaBBQ_Regional_repaired_english.jsonl", "BanglaBBQ_Regional_repaired_bengali.jsonl",
     "Position shortcut repair (180:180 balance)"),
    ("Ethnicity", "BanglaBBQ_Ethnicity", "BanglaBBQ_Ethnicity_FINAL_english.jsonl", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl",
     "BanglaBBQ_Ethnicity_repaired_english.jsonl", "BanglaBBQ_Ethnicity_repaired_bengali.jsonl",
     "Position shortcut repair (180:180 balance) + complete eradication of synthetic placeholder tokens ('A'/'B', 'ক'/'খ') with authentic names"),
    ("Social Status", "BanglaBBQ_SocialStatus", "BanglaBBQ_SocialStatus_FINAL_english.jsonl", "BanglaBBQ_SocialStatus_FINAL_bengali.jsonl",
     "BanglaBBQ_SocialStatus_repaired_english.jsonl", "BanglaBBQ_SocialStatus_repaired_bengali.jsonl",
     "Integration of Q07 V3 procedural compliance symmetrization prototype"),
]

FIELDS = [
    "change_id",
    "category",
    "language",
    "example_id",
    "theme_id",
    "variation",
    "field_modified",
    "value_before",
    "value_after",
    "baseline_sha256",
    "candidate_sha256",
    "rationale"
]

def hash_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    rows_out = []
    change_idx = 1

    for cat_name, prod_folder, en_prod_f, bn_prod_f, en_cand_f, bn_cand_f, reason in PAIRS:
        for lang, prod_f, cand_f in [("en", en_prod_f, en_cand_f), ("bn", bn_prod_f, bn_cand_f)]:
            p_prod = os.path.join(PROD_DIR, prod_folder, prod_f)
            p_cand = os.path.join(CAND_DIR, cand_f)

            base_h = hash_file(p_prod)
            cand_h = hash_file(p_cand)

            with open(p_prod, "r", encoding="utf-8") as fp, open(p_cand, "r", encoding="utf-8") as fc:
                recs_p = [json.loads(l) for l in fp]
                recs_c = [json.loads(l) for l in fc]

            for r_p, r_c in zip(recs_p, recs_c):
                eid = r_p["example_id"]
                var = (eid // 480) + 1
                q_idx = ((eid % 480) // 48) + 1
                theme_str = f"Q{q_idx:02d}"

                # Compare fields
                for k in ["context", "question", "ans0", "ans1", "ans2", "label", "answer_info"]:
                    v_p = r_p.get(k)
                    v_c = r_c.get(k)
                    if v_p != v_c:
                        rows_out.append({
                            "change_id": f"CHG-{change_idx:06d}",
                            "category": cat_name,
                            "language": lang,
                            "example_id": eid,
                            "theme_id": theme_str,
                            "variation": f"V{var}",
                            "field_modified": k,
                            "value_before": json.dumps(v_p, ensure_ascii=False) if isinstance(v_p, (dict, list)) else str(v_p),
                            "value_after": json.dumps(v_c, ensure_ascii=False) if isinstance(v_c, (dict, list)) else str(v_c),
                            "baseline_sha256": base_h,
                            "candidate_sha256": cand_h,
                            "rationale": reason
                        })
                        change_idx += 1

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Generated change ledger: {len(rows_out)} field-level modifications documented in {OUTPUT_CSV}.")

if __name__ == "__main__":
    main()
