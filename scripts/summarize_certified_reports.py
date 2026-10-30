import json
import glob

files = sorted(glob.glob('metadata/eval_results/certified_benchmark_report_*.json'))
print(f"Total certified reports found: {len(files)}\n")

rows = []
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    slug = data.get('model_slug')
    model = data.get('model')
    q = data.get('total_queries', 0)
    wall = data.get('wall_time_seconds', 0.0)
    cost = data.get('estimated_gpu_cost_usd', 0.0)
    w = data.get('weighted_averages', {})
    
    rows.append({
        'slug': slug,
        'model': model,
        'queries': q,
        'eng_acc': w.get('eng_accuracy', 0.0),
        'ben_acc': w.get('ben_accuracy', 0.0),
        'acc_gap': w.get('ben_accuracy', 0.0) - w.get('eng_accuracy', 0.0),
        'eng_amb': w.get('eng_acc_ambig', 0.0),
        'ben_amb': w.get('ben_acc_ambig', 0.0),
        'eng_dis': w.get('eng_acc_disambig', 0.0),
        'ben_dis': w.get('ben_acc_disambig', 0.0),
        'eng_samb': w.get('eng_s_amb', 0.0),
        'ben_samb': w.get('ben_s_amb', 0.0),
        'delta_samb': w.get('global_bias_delta', 0.0),
        'eng_sdis': w.get('eng_s_dis', 0.0),
        'ben_sdis': w.get('ben_s_dis', 0.0),
        'delta_sdis': w.get('global_dis_delta', 0.0),
        'unp_cnt': w.get('total_unparseable_count', 0),
        'unp_rate_ben': w.get('ben_unparseable_rate', 0.0),
        'wall_s': wall,
        'cost': cost
    })

header = f"{'Model':<20} | {'Queries':<7} | {'ENG Acc':<7} | {'BEN Acc':<7} | {'Acc Gap':<7} | {'ENG Ambig':<9} | {'BEN Ambig':<9} | {'ENG s_amb':<9} | {'BEN s_amb':<9} | {'Delta Bias':<10} | {'Unp':<4} | {'WallTime':<8} | {'Cost USD':<8}"
print(header)
print("-" * len(header))
for r in rows:
    print(f"{r['slug']:<20} | {r['queries']:<7} | {r['eng_acc']:>6.2f}% | {r['ben_acc']:>6.2f}% | {r['acc_gap']:>+6.2f}% | {r['eng_amb']:>8.2f}% | {r['ben_amb']:>8.2f}% | {r['eng_samb']:>+9.4f} | {r['ben_samb']:>+9.4f} | {r['delta_samb']:>+10.4f} | {r['unp_cnt']:<4} | {r['wall_s']:>6.1f}s | ${r['cost']:>6.4f}")
