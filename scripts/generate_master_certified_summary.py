import json
import glob
import os
import csv

files = sorted(glob.glob('metadata/eval_results/certified_benchmark_report_*.json'))
print(f"Aggregating {len(files)} certified evaluation reports...")

master_data = {
    "benchmark_title": "BanglaBBQ Canonical 61,312-Query Certified Benchmark Summary",
    "scoring_methodology": "Alicia Parrish et al. (2022) BBQ Formulation via scripts/bbq_scoring_engine.py",
    "eval_date": "2026-10-30",
    "total_models": len(files),
    "total_queries_evaluated_across_all_models": sum([json.load(open(f, 'r', encoding='utf-8'))['total_queries'] for f in files]),
    "models": []
}

csv_rows = []
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    slug = d.get('model_slug')
    model = d.get('model')
    q = d.get('total_queries', 0)
    gpu = d.get('gpu', 'NVIDIA L40S')
    wall_s = d.get('wall_time_seconds', 0.0)
    cost = d.get('estimated_gpu_cost_usd', 0.0)
    w = d.get('weighted_averages', {})
    
    model_entry = {
        "model_slug": slug,
        "model_name": model,
        "gpu": gpu,
        "total_queries": q,
        "wall_time_seconds": wall_s,
        "estimated_gpu_cost_usd": cost,
        "eng_accuracy": w.get('eng_accuracy', 0.0),
        "ben_accuracy": w.get('ben_accuracy', 0.0),
        "accuracy_gap": round(w.get('ben_accuracy', 0.0) - w.get('eng_accuracy', 0.0), 2),
        "eng_acc_ambig": w.get('eng_acc_ambig', 0.0),
        "ben_acc_ambig": w.get('ben_acc_ambig', 0.0),
        "eng_acc_disambig": w.get('eng_acc_disambig', 0.0),
        "ben_acc_disambig": w.get('ben_acc_disambig', 0.0),
        "eng_s_amb": w.get('eng_s_amb', 0.0),
        "ben_s_amb": w.get('ben_s_amb', 0.0),
        "global_bias_delta": w.get('global_bias_delta', 0.0),
        "eng_s_dis": w.get('eng_s_dis', 0.0),
        "ben_s_dis": w.get('ben_s_dis', 0.0),
        "global_dis_delta": w.get('global_dis_delta', 0.0),
        "eng_unparseable_rate": w.get('eng_unparseable_rate', 0.0),
        "ben_unparseable_rate": w.get('ben_unparseable_rate', 0.0),
        "total_unparseable_count": w.get('total_unparseable_count', 0)
    }
    master_data["models"].append(model_entry)
    csv_rows.append(model_entry)

# Write master JSON
json_out = "metadata/eval_results/certified_benchmark_master_summary.json"
with open(json_out, 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)
print(f"Wrote {json_out}")

# Write master CSV
csv_out = "metadata/eval_results/certified_benchmark_master_summary.csv"
fieldnames = [
    "model_slug", "model_name", "total_queries", "eng_accuracy", "ben_accuracy", "accuracy_gap",
    "eng_acc_ambig", "ben_acc_ambig", "eng_acc_disambig", "ben_acc_disambig",
    "eng_s_amb", "ben_s_amb", "global_bias_delta",
    "eng_s_dis", "ben_s_dis", "global_dis_delta",
    "total_unparseable_count", "eng_unparseable_rate", "ben_unparseable_rate",
    "wall_time_seconds", "estimated_gpu_cost_usd"
]
with open(csv_out, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(csv_rows)
print(f"Wrote {csv_out}")
