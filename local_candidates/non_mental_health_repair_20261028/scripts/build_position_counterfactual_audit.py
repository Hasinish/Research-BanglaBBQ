import os
import sys
import json
import csv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_CSV = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "reports", "position_and_counterfactual_audit.csv")

UNKNOWN_TERMS = {
    "cannot be determined", "unknown", "undetermined", 
    "can't be determined", "not determinable", "not enough information",
    "অজানা", "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না", 
    "বলা সম্ভব নয়", "বলা সম্ভব নয়", "তথ্য অপর্যাপ্ত", "নির্ধারণ করা সম্ভব নয়"
}

def is_unknown(text):
    t = text.strip().lower()
    return any(u in t for u in UNKNOWN_TERMS)

def get_sub(o):
    if "from " in o: return o.split("from ")[-1].strip()
    if "থেকে আসা" in o: return o.split("থেকে আসা")[0].strip()
    if "," in o: return o.split(",")[0].strip()
    return o.split()[0] if o.split() else o

def audit_file(filepath, category, lang, dataset_version):
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    # Aggregate by (theme, variation)
    stats = {}
    for r in records:
        cond = r["context_condition"]
        if cond != "disambig":
            continue
        eid = r["example_id"]
        var = (eid // 480) + 1
        q_idx = ((eid % 480) // 48) + 1
        theme_str = f"Q{q_idx:02d}"
        var_str = f"V{var}"
        pol = r["question_polarity"]

        key = (theme_str, var_str)
        if key not in stats:
            stats[key] = {
                "neg_first": 0, "neg_second": 0,
                "nonneg_first": 0, "nonneg_second": 0,
                "total_neg": 0, "total_nonneg": 0
            }

        answers = [r["ans0"], r["ans1"], r["ans2"]]
        gold = answers[r["label"]]
        ctx = r["context"]

        non_unk = [a for a in answers if not is_unknown(a)]
        if len(non_unk) != 2:
            continue

        o1, o2 = non_unk[0], non_unk[1]
        s1, s2 = get_sub(o1), get_sub(o2)
        pos1, pos2 = ctx.find(s1), ctx.find(s2)
        if pos1 == -1 or pos2 == -1:
            pos1 = ctx.lower().find(s1.lower())
            pos2 = ctx.lower().find(s2.lower())

        first_ent = o1 if pos1 < pos2 else o2
        second_ent = o2 if pos1 < pos2 else o1

        is_first = (gold == first_ent)
        is_sec = (gold == second_ent)

        if pol == "neg":
            stats[key]["total_neg"] += 1
            if is_first: stats[key]["neg_first"] += 1
            elif is_sec: stats[key]["neg_second"] += 1
        else:
            stats[key]["total_nonneg"] += 1
            if is_first: stats[key]["nonneg_first"] += 1
            elif is_sec: stats[key]["nonneg_second"] += 1

    cat_neg_first = sum(v["neg_first"] for v in stats.values())
    cat_neg_second = sum(v["neg_second"] for v in stats.values())
    cat_nonneg_first = sum(v["nonneg_first"] for v in stats.values())
    cat_nonneg_second = sum(v["nonneg_second"] for v in stats.values())

    for (t, v), s in sorted(stats.items()):
        # Determine verdict
        if s["neg_first"] == s["neg_second"]:
            verdict = "BALANCED_50_50"
        elif s["neg_first"] == 0 or s["neg_second"] == 0:
            verdict = "FATAL_POSITIONAL_SHORTCUT_100_PERCENT"
        else:
            verdict = "RESIDUAL_THEME_SKEW_2_TO_1"

        rows.append({
            "dataset_version": dataset_version,
            "category": category,
            "language": lang,
            "theme": t,
            "variation": v,
            "disambig_neg_first": s["neg_first"],
            "disambig_neg_second": s["neg_second"],
            "disambig_nonneg_first": s["nonneg_first"],
            "disambig_nonneg_second": s["nonneg_second"],
            "balance_verdict": verdict,
            "orthogonality_notes": f"V{v} {s['neg_first']}:{s['neg_second']} NEG; {s['nonneg_first']}:{s['nonneg_second']} NONNEG"
        })

    # Add category total
    cat_verdict = "EXACT_50_50_CATEGORY_PARITY" if cat_neg_first == cat_neg_second else "CATEGORY_LEVEL_POSITIONAL_BIAS"
    rows.append({
        "dataset_version": dataset_version,
        "category": category,
        "language": lang,
        "theme": "ALL_THEMES",
        "variation": "CATEGORY_TOTAL",
        "disambig_neg_first": cat_neg_first,
        "disambig_neg_second": cat_neg_second,
        "disambig_nonneg_first": cat_nonneg_first,
        "disambig_nonneg_second": cat_nonneg_second,
        "balance_verdict": cat_verdict,
        "orthogonality_notes": f"Total NEG {cat_neg_first}:{cat_neg_second} ({cat_neg_first/(cat_neg_first+cat_neg_second)*100:.1f}% / {cat_neg_second/(cat_neg_first+cat_neg_second)*100:.1f}%)"
    })
    return rows

def main():
    all_rows = []

    # 1. Audit production baseline files
    prod_targets = [
        ("Health Status", "BanglaBBQ_HealthStatus", "BanglaBBQ_Health_Status_FINAL_english.jsonl", "BanglaBBQ_Health_Status_FINAL_bengali.jsonl"),
        ("Regional Affiliation", "BanglaBBQ_Regional", "BanglaBBQ_Regional_FINAL_english.jsonl", "BanglaBBQ_Regional_FINAL_bengali.jsonl"),
        ("Ethnicity", "BanglaBBQ_Ethnicity", "BanglaBBQ_Ethnicity_FINAL_english.jsonl", "BanglaBBQ_Ethnicity_FINAL_bengali.jsonl"),
        ("Physical Appearance", "BanglaBBQ_PhysicalAppearance", "BanglaBBQ_Physical_Appearance_FINAL_english.jsonl", "BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl"),
    ]
    for cat, folder, en_f, bn_f in prod_targets:
        en_p = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New", folder, en_f)
        bn_p = os.path.join(REPO_ROOT, "Dataset_BanglaBBQ_New", folder, bn_f)
        all_rows.extend(audit_file(en_p, cat, "en", "PRODUCTION_BASELINE"))
        all_rows.extend(audit_file(bn_p, cat, "bn", "PRODUCTION_BASELINE"))

    # 2. Audit new repaired candidate datasets
    cand_targets = [
        ("Health Status", "BanglaBBQ_Health_Status_repaired_english.jsonl", "BanglaBBQ_Health_Status_repaired_bengali.jsonl"),
        ("Regional Affiliation", "BanglaBBQ_Regional_repaired_english.jsonl", "BanglaBBQ_Regional_repaired_bengali.jsonl"),
        ("Ethnicity", "BanglaBBQ_Ethnicity_repaired_english.jsonl", "BanglaBBQ_Ethnicity_repaired_bengali.jsonl"),
        ("Social Status", "BanglaBBQ_SocialStatus_repaired_english.jsonl", "BanglaBBQ_SocialStatus_repaired_bengali.jsonl"),
    ]
    cand_dir = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")
    for cat, en_f, bn_f in cand_targets:
        en_p = os.path.join(cand_dir, en_f)
        bn_p = os.path.join(cand_dir, bn_f)
        all_rows.extend(audit_file(en_p, cat, "en", "REPAIRED_CANDIDATE"))
        all_rows.extend(audit_file(bn_p, cat, "bn", "REPAIRED_CANDIDATE"))


    fieldnames = [
        "dataset_version", "category", "language", "theme", "variation",
        "disambig_neg_first", "disambig_neg_second",
        "disambig_nonneg_first", "disambig_nonneg_second",
        "balance_verdict", "orthogonality_notes"
    ]
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Position and counterfactual audit written to: {OUTPUT_CSV}")
    print(f"Total audit rows: {len(all_rows)}")

if __name__ == "__main__":
    main()
