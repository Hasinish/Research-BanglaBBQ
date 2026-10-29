"""
scripts/build_stratified_4000_manifest.py
=========================================
Generates a deterministic, mathematically balanced 4,000-sample benchmark dataset
(2,000 English + 2,000 Bengali paired rows) across all 12 canonical categories.

Allocation:
- BanglaBBQ_Age: 280 pairs (DT + TM weighted)
- BanglaBBQ_Gender: 280 pairs (DT + NA weighted)
- BanglaBBQ_Religion: 240 pairs (Boosted)
- BanglaBBQ_Politics: 240 pairs (Boosted)
- BanglaBBQ_Regional: 120 pairs
- BanglaBBQ_SocialStatus: 120 pairs
- BanglaBBQ_Ethnicity: 120 pairs
- BanglaBBQ_EducationalBackground: 120 pairs
- BanglaBBQ_OccupationalBackground: 120 pairs
- BanglaBBQ_MaritalStatus: 120 pairs
- BanglaBBQ_PhysicalAppearance: 120 pairs
- BanglaBBQ_HealthStatus: 120 pairs
Total: 2,000 English + 2,000 Bengali = 4,000 total evaluations.

Stratification guarantees:
- Exact 50% ambig / 50% disambig
- Exact 50% neg / 50% nonneg
- 100% paired 1-to-1 matching by example_id between English and Bengali
"""

import os
import json
import random
import csv
from pathlib import Path
from collections import defaultdict

SEED = 42
random.seed(SEED)

DATA_DIR = Path("Dataset_BanglaBBQ_New")
OUTPUT_DIR = Path("metadata/eval_4000")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORY_TARGETS = {
    "BanglaBBQ_Age": 280,
    "BanglaBBQ_Gender": 280,
    "BanglaBBQ_Religion": 240,
    "BanglaBBQ_Politics": 240,
    "BanglaBBQ_Regional": 120,
    "BanglaBBQ_SocialStatus": 120,
    "BanglaBBQ_Ethnicity": 120,
    "BanglaBBQ_EducationalBackground": 120,
    "BanglaBBQ_OccupationalBackground": 120,
    "BanglaBBQ_MaritalStatus": 120,
    "BanglaBBQ_PhysicalAppearance": 120,
    "BanglaBBQ_HealthStatus": 120,
}


def sample_category(cat_name, target_pairs):
    cat_dir = DATA_DIR / cat_name
    eng_files = list(cat_dir.glob("*ENG*.jsonl"))
    ben_files = list(cat_dir.glob("*BEN*.jsonl"))

    if not eng_files or not ben_files:
        raise FileNotFoundError(f"Missing ENG or BEN file for {cat_name}")

    eng_path = eng_files[0]
    ben_path = ben_files[0]

    with open(eng_path, "r", encoding="utf-8") as f:
        eng_rows = {json.loads(line)["example_id"]: json.loads(line) for line in f}

    with open(ben_path, "r", encoding="utf-8") as f:
        ben_rows = {json.loads(line)["example_id"]: json.loads(line) for line in f}

    common_ids = sorted(set(eng_rows.keys()) & set(ben_rows.keys()))
    if len(common_ids) < target_pairs:
        raise ValueError(f"Category {cat_name} has only {len(common_ids)} common IDs, need {target_pairs}")

    # Stratify by (context_condition, question_polarity)
    strata = defaultdict(list)
    for eid in common_ids:
        r = eng_rows[eid]
        key = (r["context_condition"], r["question_polarity"])
        strata[key].append(eid)

    per_stratum = target_pairs // 4
    remainder = target_pairs % 4

    selected_ids = []
    # Deterministic shuffle
    rng = random.Random(SEED + hash(cat_name) % 10000)

    for i, (key, ids) in enumerate(sorted(strata.items())):
        rng.shuffle(ids)
        take_count = per_stratum + (1 if i < remainder else 0)
        selected_ids.extend(ids[:take_count])

    selected_ids.sort()

    paired_samples = []
    for eid in selected_ids:
        paired_samples.append({
            "category": cat_name,
            "example_id": eid,
            "eng": eng_rows[eid],
            "ben": ben_rows[eid],
        })

    return paired_samples


def main():
    print("=" * 70)
    print("  BUILDING BALANCED 4,000-SAMPLE BANGLABBQ BENCHMARK MANIFEST")
    print("=" * 70)

    all_pairs = []
    summary_rows = []

    for cat_name, target in CATEGORY_TARGETS.items():
        pairs = sample_category(cat_name, target)
        all_pairs.extend(pairs)

        cond_counts = defaultdict(int)
        pol_counts = defaultdict(int)
        type_counts = defaultdict(int)
        for p in pairs:
            r = p["eng"]
            cond_counts[r["context_condition"]] += 1
            pol_counts[r["question_polarity"]] += 1
            type_counts[r.get("type", "NA")] += 1

        summary_rows.append({
            "Category": cat_name,
            "Pairs": len(pairs),
            "ENG Rows": len(pairs),
            "BEN Rows": len(pairs),
            "Ambig": cond_counts["ambig"],
            "Disambig": cond_counts["disambig"],
            "Neg": pol_counts["neg"],
            "NonNeg": pol_counts["nonneg"],
            "Types": dict(type_counts),
        })

        print(f"[{cat_name:<32}] {len(pairs):>4} pairs | Ambig: {cond_counts['ambig']:>3}, Disambig: {cond_counts['disambig']:>3} | Neg: {pol_counts['neg']:>3}, NonNeg: {pol_counts['nonneg']:>3} | Types: {dict(type_counts)}")

    # Write Manifest CSV
    manifest_csv = OUTPUT_DIR / "manifest_4000_pairs.csv"
    with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "category", "example_id", "context_condition", "question_polarity",
            "type", "eng_label", "ben_label", "stereotyped_groups"
        ])
        for p in all_pairs:
            eng = p["eng"]
            ben = p["ben"]
            groups = ";".join(eng.get("additional_metadata", {}).get("stereotyped_groups", []))
            writer.writerow([
                p["category"], p["example_id"], eng["context_condition"],
                eng["question_polarity"], eng.get("type", "NA"),
                eng["label"], ben["label"], groups
            ])

    # Write Complete Evaluator JSONL (Both English and Bengali records tagged with lang)
    eval_jsonl = OUTPUT_DIR / "eval_4000_all_queries.jsonl"
    with open(eval_jsonl, "w", encoding="utf-8") as f:
        for p in all_pairs:
            # English record
            eng_rec = dict(p["eng"])
            eng_rec["eval_lang"] = "ENG"
            eng_rec["benchmark_category"] = p["category"]
            f.write(json.dumps(eng_rec, ensure_ascii=False) + "\n")

            # Bengali record
            ben_rec = dict(p["ben"])
            ben_rec["eval_lang"] = "BEN"
            ben_rec["benchmark_category"] = p["category"]
            f.write(json.dumps(ben_rec, ensure_ascii=False) + "\n")

    print("=" * 70)
    print(f"[+] Total Paired Scenarios: {len(all_pairs):,}")
    print(f"[+] Total Queries (ENG + BEN): {len(all_pairs) * 2:,}")
    print(f"[+] Manifest CSV written to: {manifest_csv}")
    print(f"[+] Evaluation JSONL written to: {eval_jsonl}")
    print("=" * 70)


if __name__ == "__main__":
    main()

