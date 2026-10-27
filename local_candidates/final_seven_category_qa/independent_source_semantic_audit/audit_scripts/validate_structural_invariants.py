import json
import os
import sys
import glob

# Ensure utf-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

QA_DIR = r"d:\Research-BanglaBBQ\local_candidates\final_seven_category_qa"
AUDIT_DIR = os.path.join(QA_DIR, "independent_source_semantic_audit")
REPORTS_DIR = os.path.join(AUDIT_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

EXPECTED_FIELDS = [
    "example_id",
    "question_index",
    "question_polarity",
    "context_condition",
    "category",
    "context",
    "question",
    "ans0",
    "ans1",
    "ans2",
    "label",
    "answer_info",
    "additional_metadata"
]

def derive_variation_and_qindex(example_id):
    var = (example_id // 480) + 1
    q_idx = ((example_id % 480) // 48) + 1
    return var, q_idx

def validate_file_structure(filepath, expected_count, is_prototype=False):
    errors = []
    line_count = 0
    label_dist = {0: 0, 1: 0, 2: 0}
    cond_pol_dist = {
        ("ambig", "neg"): 0,
        ("disambig", "neg"): 0,
        ("ambig", "nonneg"): 0,
        ("disambig", "nonneg"): 0,
    }
    
    seen_ids = set()
    prev_id = None
    
    with open(filepath, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line_str = line.strip()
            if not line_str:
                errors.append(f"Line {idx+1}: Empty line")
                continue
            line_count += 1
            try:
                rec = json.loads(line_str)
            except Exception as e:
                errors.append(f"Line {idx+1}: JSON parse error: {e}")
                continue
                
            eid = rec.get("example_id")
            if eid is None:
                errors.append(f"Line {idx+1}: Missing example_id")
            else:
                seen_ids.add(eid)
                if not is_prototype:
                    if prev_id is not None and eid != prev_id + 1:
                        errors.append(f"Line {idx+1}: Non-sequential example_id (prev={prev_id}, curr={eid})")
                    prev_id = eid
                    
            # check question_index & variation derivation
            q_idx_field = rec.get("question_index")
            try:
                q_idx_int = int(q_idx_field)
            except Exception:
                q_idx_int = -1
                
            calc_var, calc_q = derive_variation_and_qindex(eid)
            if q_idx_int != calc_q:
                errors.append(f"Line {idx+1} (EID {eid}): question_index mismatch (field={q_idx_field}, calc={calc_q})")
                
            # check fields
            for ef in EXPECTED_FIELDS:
                if ef not in rec:
                    errors.append(f"Line {idx+1} (EID {eid}): Missing expected field '{ef}'")
                    
            # check label
            lbl = rec.get("label")
            if lbl not in [0, 1, 2]:
                errors.append(f"Line {idx+1} (EID {eid}): Invalid label {lbl}")
            else:
                label_dist[lbl] += 1
                
            # check answers
            ans0 = rec.get("ans0")
            ans1 = rec.get("ans1")
            ans2 = rec.get("ans2")
            if not (ans0 and ans1 and ans2):
                errors.append(f"Line {idx+1} (EID {eid}): Empty answer option")
                
            # check condition and polarity
            cond = rec.get("context_condition")
            pol = rec.get("question_polarity")
            if (cond, pol) in cond_pol_dist:
                cond_pol_dist[(cond, pol)] += 1
            else:
                errors.append(f"Line {idx+1} (EID {eid}): Invalid cond/pol ({cond}, {pol})")
                
            # check ambiguous gold answer is Unknown
            answers = [ans0, ans1, ans2]
            gold_ans = answers[lbl] if lbl in [0, 1, 2] else ""
            
            # Check Unknown presence
            unknown_candidates = [
                "cannot be determined", "undetermined", "not known", "unknown", 
                "তথ্য অপর্যাপ্ত", "অজানা", "নির্ধারণ করা সম্ভব নয়", "নির্ধারণ করা যায় না", 
                "নির্ধারণ করা যায় না", "বলা সম্ভব নয়", "বলা সম্ভব নয়"
            ]
            is_gold_unknown = any(u in gold_ans.lower() for u in unknown_candidates)
            
            if cond == "ambig":
                if not is_gold_unknown:
                    errors.append(f"Line {idx+1} (EID {eid}): Ambiguous gold answer is not Unknown ('{gold_ans}')")
            elif cond == "disambig":
                if is_gold_unknown:
                    errors.append(f"Line {idx+1} (EID {eid}): Disambiguated gold answer is Unknown ('{gold_ans}')")
                    
    if line_count != expected_count:
        errors.append(f"Record count mismatch: expected {expected_count}, got {line_count}")
        
    return {
        "file": os.path.basename(filepath),
        "path": os.path.relpath(filepath, QA_DIR).replace("\\", "/"),
        "line_count": line_count,
        "expected_count": expected_count,
        "unique_example_ids": len(seen_ids),
        "label_distribution": label_dist,
        "condition_polarity_distribution": {f"{k[0]}_{k[1]}": v for k, v in cond_pol_dist.items()},
        "errors_count": len(errors),
        "errors_sample": errors[:10]
    }

def main():
    files_to_validate = [
        # Candidates (1,440 each)
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Health_Status_FINAL_english.jsonl"), 1440, False),
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl"), 1440, False),
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Regional_FINAL_english.jsonl"), 1440, False),
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Regional_FINAL_bengali.jsonl"), 1440, False),
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Ethnicity_FINAL_english.jsonl"), 1440, False),
        (os.path.join(QA_DIR, "candidates", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl"), 1440, False),
        # Prototypes
        (os.path.join(QA_DIR, "prototypes", "Health_Status_Q02_Q04_Q05_Q07_prototype_english.jsonl"), 576, True),
        (os.path.join(QA_DIR, "prototypes", "Health_Status_Q02_Q04_Q05_Q07_prototype_bengali.jsonl"), 576, True),
        (os.path.join(QA_DIR, "prototypes", "Physical_Appearance_Q02_prototype_english.jsonl"), 144, True),
        (os.path.join(QA_DIR, "prototypes", "Physical_Appearance_Q02_prototype_bengali.jsonl"), 144, True),
        (os.path.join(QA_DIR, "prototypes", "Social_Status_Q07_V3_prototype_english.jsonl"), 48, True),
        (os.path.join(QA_DIR, "prototypes", "Social_Status_Q07_V3_prototype_bengali.jsonl"), 48, True),
    ]
    
    results = {}
    all_passed = True
    
    for fpath, exp_cnt, is_proto in files_to_validate:
        fname = os.path.basename(fpath)
        print(f"Validating {fname}...")
        res = validate_file_structure(fpath, exp_cnt, is_proto)
        results[fname] = res
        if res["errors_count"] > 0:
            all_passed = False
            print(f"  FAILED: {res['errors_count']} errors found. First error: {res['errors_sample'][0] if res['errors_sample'] else ''}")
        else:
            print(f"  PASS: {res['line_count']} records, label_dist={res['label_distribution']}")
            
    out_json = os.path.join(REPORTS_DIR, "structural_invariants.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "overall_status": "PASS" if all_passed else "FAIL",
            "files": results
        }, f, indent=2)
    print(f"\nStructural invariant report written to: {out_json}")

if __name__ == "__main__":
    main()
