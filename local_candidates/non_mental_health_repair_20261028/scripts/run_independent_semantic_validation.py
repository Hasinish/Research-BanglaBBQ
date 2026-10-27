import os
import sys
import json
import csv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "scripts"))

from independent_semantic_validator import GoldBlindSemanticValidator

CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")
OUTPUT_CSV = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "reports", "semantic_validation_report.csv")

CANDIDATES = [
    ("Ethnicity", "BanglaBBQ_Ethnicity_repaired_english.jsonl", "BanglaBBQ_Ethnicity_repaired_bengali.jsonl"),
    ("Health Status", "BanglaBBQ_Health_Status_repaired_english.jsonl", "BanglaBBQ_Health_Status_repaired_bengali.jsonl"),
    ("Regional Affiliation", "BanglaBBQ_Regional_repaired_english.jsonl", "BanglaBBQ_Regional_repaired_bengali.jsonl"),
    ("Social Status", "BanglaBBQ_SocialStatus_repaired_english.jsonl", "BanglaBBQ_SocialStatus_repaired_bengali.jsonl"),
]

FIELDS = [
    "case_id",
    "category",
    "theme_id",
    "variation",
    "orientation",
    "context_condition",
    "question_polarity",
    "example_id_sample",
    "independent_derived_en_answer",
    "independent_derived_bn_answer",
    "stored_label",
    "gold_blind_verdict",
    "cross_lingual_parity",
    "error_details"
]

def derive_variation_and_qindex(example_id):
    var = (example_id // 480) + 1
    q_idx = ((example_id % 480) // 48) + 1
    return var, q_idx

def main():
    validator = GoldBlindSemanticValidator()
    rows_out = []
    case_idx = 1

    total_cases = 0
    passed_cases = 0

    for cat_name, en_file, bn_file in CANDIDATES:
        p_en = os.path.join(CAND_DIR, en_file)
        p_bn = os.path.join(CAND_DIR, bn_file)

        with open(p_en, "r", encoding="utf-8") as fe, open(p_bn, "r", encoding="utf-8") as fb:
            recs_en = [json.loads(l) for l in fe]
            recs_bn = [json.loads(l) for l in fb]

        # Group by semantic case: (theme, variation, orientation, condition, polarity)
        groups = {}
        for r_en, r_bn in zip(recs_en, recs_bn):
            eid = r_en["example_id"]
            var, q = derive_variation_and_qindex(eid)
            orient = r_en.get("additional_metadata", {}).get("version", "a")
            cond = r_en["context_condition"]
            pol = r_en["question_polarity"]

            key = (cat_name, f"Q{q:02d}", f"V{var}", orient, cond, pol)
            if key not in groups:
                groups[key] = []
            groups[key].append((r_en, r_bn))

        print(f"[{cat_name}] Evaluating {len(groups)} distinct semantic cases...")

        for key, rec_pairs in groups.items():
            cat, theme, var, orient, cond, pol = key
            first_en, first_bn = rec_pairs[0]
            eid_sample = first_en["example_id"]

            res = validator.validate_record_pair(first_en, first_bn)

            total_cases += 1
            is_pass = res["blind_check_passed"]
            if is_pass:
                passed_cases += 1
                verdict = "INDEPENDENTLY_VALIDATED"
            else:
                verdict = "VALIDATION_FLAGGED"

            rows_out.append({
                "case_id": f"SEM-{case_idx:05d}",
                "category": cat,
                "theme_id": theme,
                "variation": var,
                "orientation": orient,
                "context_condition": cond,
                "question_polarity": pol,
                "example_id_sample": eid_sample,
                "independent_derived_en_answer": res["independent_en_gold"],
                "independent_derived_bn_answer": res["independent_bn_gold"],
                "stored_label": first_en["label"],
                "gold_blind_verdict": verdict,
                "cross_lingual_parity": "ALIGNED" if first_en["label"] == first_bn["label"] else "MISMATCH",
                "error_details": "; ".join(res["errors"]) if res["errors"] else "NONE"
            })
            case_idx += 1

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nSemantic Validation Summary: {passed_cases}/{total_cases} cases passed ({passed_cases/total_cases*100:.1f}%).")
    print(f"Full semantic validation report written to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
