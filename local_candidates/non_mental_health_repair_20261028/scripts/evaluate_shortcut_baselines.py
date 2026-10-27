import os
import sys
import json
import csv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

CATEGORIES = [
    ("Health Status", "BanglaBBQ_HealthStatus", "BanglaBBQ_Health_Status_FINAL_english.jsonl", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl"),
    ("Regional Affiliation", "BanglaBBQ_Regional", "BanglaBBQ_Regional_FINAL_english.jsonl", "BanglaBBQ_Regional_FINAL_bengali.jsonl"),
    ("Ethnicity", "BanglaBBQ_Ethnicity", "BanglaBBQ_Ethnicity_FINAL_english.jsonl", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl"),
    ("Physical Appearance", "BanglaBBQ_PhysicalAppearance", "BanglaBBQ_Physical_Appearance_FINAL_english.jsonl", "BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl"),
    ("Social Status", "BanglaBBQ_SocialStatus", "BanglaBBQ_SocialStatus_FINAL_english.jsonl", "BanglaBBQ_SocialStatus_FINAL_bengali.jsonl"),
    ("Occupational Background", "BanglaBBQ_OccupationalBackground", "BanglaBBQ_Occupational_Background_FINAL_english.jsonl", "BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl"),
    ("Marital Status", "BanglaBBQ_MaritalStatus", "BanglaBBQ_MaritalStatus_FINAL_english.jsonl", "BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl")
]

UNKNOWN_TERMS = {
    "cannot be determined", "unknown", "undetermined", 
    "can't be determined", "not determinable", "not enough information",
    "অজানা", "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না", 
    "বলা সম্ভব নয়", "বলা সম্ভব নয়", "তথ্য অপর্যাপ্ত", "নির্ধারণ করা সম্ভব নয়"
}

def is_unknown(text):
    t = text.strip().lower()
    return any(u in t for u in UNKNOWN_TERMS)

def evaluate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    total_disambig = 0
    total_disambig_neg = 0
    total_ambig = 0

    acc = {
        "always_first": 0,
        "always_second": 0,
        "always_ans0": 0,
        "always_ans1": 0,
        "always_ans2": 0,
        "target_demographic": 0
    }

    acc_neg = {
        "always_first": 0,
        "always_second": 0,
        "always_ans0": 0,
        "always_ans1": 0,
        "always_ans2": 0,
        "target_demographic": 0
    }

    for r in records:
        cond = r["context_condition"]
        pol = r["question_polarity"]
        lbl = r["label"]
        answers = [r["ans0"], r["ans1"], r["ans2"]]
        gold = answers[lbl]
        ctx = r["context"]

        if cond == "ambig":
            total_ambig += 1
            continue

        if cond == "disambig":
            total_disambig += 1
            if pol == "neg":
                total_disambig_neg += 1

            # Extract entities
            non_unk = [a for a in answers if not is_unknown(a)]
            if len(non_unk) != 2:
                continue

            o1, o2 = non_unk[0], non_unk[1]

            # Find position in context
            def get_sub(o):
                if "from " in o: return o.split("from ")[-1].strip()
                if "থেকে আসা" in o: return o.split("থেকে আসা")[0].strip()
                if "," in o: return o.split(",")[0].strip()
                return o.split()[0] if o.split() else o

            s1 = get_sub(o1)
            s2 = get_sub(o2)

            pos1 = ctx.find(s1)
            pos2 = ctx.find(s2)
            if pos1 == -1 or pos2 == -1:
                pos1 = ctx.lower().find(s1.lower())
                pos2 = ctx.lower().find(s2.lower())

            first_ent = o1 if pos1 < pos2 else o2
            second_ent = o2 if pos1 < pos2 else o1

            is_first = (gold == first_ent)
            is_sec = (gold == second_ent)

            if is_first:
                acc["always_first"] += 1
                if pol == "neg": acc_neg["always_first"] += 1
            if is_sec:
                acc["always_second"] += 1
                if pol == "neg": acc_neg["always_second"] += 1

            if lbl == 0:
                acc["always_ans0"] += 1
                if pol == "neg": acc_neg["always_ans0"] += 1
            elif lbl == 1:
                acc["always_ans1"] += 1
                if pol == "neg": acc_neg["always_ans1"] += 1
            elif lbl == 2:
                acc["always_ans2"] += 1
                if pol == "neg": acc_neg["always_ans2"] += 1

            ans_info = r.get("answer_info", {})
            gold_key = f"ans{lbl}"
            role = ans_info.get(gold_key, [])
            if "target" in role:
                acc["target_demographic"] += 1
                if pol == "neg": acc_neg["target_demographic"] += 1

    results = {
        "total_disambig": total_disambig,
        "total_disambig_neg": total_disambig_neg,
        "overall": {k: v / total_disambig if total_disambig else 0 for k, v in acc.items()},
        "negative_only": {k: v / total_disambig_neg if total_disambig_neg else 0 for k, v in acc_neg.items()}
    }
    return results

def main():
    print("=== SHORTCUT BASELINE EVALUATION ACROSS CANONICAL PRODUCTION DATASETS ===")
    prod_dir = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New")
    for cat_name, folder, en_f, bn_f in CATEGORIES:
        en_res = evaluate_file(os.path.join(prod_dir, folder, en_f))
        print(f"\n[{cat_name} - English Production]")
        print(f"  Disambig Negative (N={en_res['total_disambig_neg']}):")
        print(f"    Always First-Mentioned : {en_res['negative_only']['always_first']*100:.1f}%")
        print(f"    Always Second-Mentioned: {en_res['negative_only']['always_second']*100:.1f}%")
        print(f"    Always ans0            : {en_res['negative_only']['always_ans0']*100:.1f}%")
        print(f"    Always ans1            : {en_res['negative_only']['always_ans1']*100:.1f}%")
        print(f"    Always ans2            : {en_res['negative_only']['always_ans2']*100:.1f}%")
        print(f"    Target Demographic     : {en_res['negative_only']['target_demographic']*100:.1f}%")

    print("\n=== SHORTCUT BASELINE EVALUATION ACROSS CANDIDATE DATASETS ===")
    cand_dir = os.path.join(REPO_ROOT, "local_candidates", "final_seven_category_qa", "candidates")
    cand_files = [
        ("Health Status", "BanglaBBQ_Health_Status_FINAL_english.jsonl"),
        ("Regional Affiliation", "BanglaBBQ_Regional_FINAL_english.jsonl"),
        ("Ethnicity", "BanglaBBQ_Ethnicity_FINAL_english.jsonl")
    ]
    for cat_name, f_name in cand_files:
        p = os.path.join(cand_dir, f_name)
        if os.path.exists(p):
            res = evaluate_file(p)
            print(f"\n[{cat_name} - Candidate English]")
            print(f"  Disambig Negative (N={res['total_disambig_neg']}):")
            print(f"    Always First-Mentioned : {res['negative_only']['always_first']*100:.1f}%")
            print(f"    Always Second-Mentioned: {res['negative_only']['always_second']*100:.1f}%")
            print(f"    Always ans0            : {res['negative_only']['always_ans0']*100:.1f}%")
            print(f"    Always ans1            : {res['negative_only']['always_ans1']*100:.1f}%")
            print(f"    Always ans2            : {res['negative_only']['always_ans2']*100:.1f}%")
            print(f"    Target Demographic     : {res['negative_only']['target_demographic']*100:.1f}%")

if __name__ == "__main__":
    main()
