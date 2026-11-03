import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

categories = [
    ("HealthStatus", "HealthStatus", 2880),
    ("MaritalStatus", "MaritalStatus", 2880),
    ("OccupationalBackground", "OccupationalBackground", 2880),
    ("Politics", "Politics", 2880),
    ("Regional", "Regional", 1440),
    ("SocialStatus", "SocialStatus", 1440)
]

print(f"{'Category':<25} | {'Lang':<4} | {'Labels (0/1/2)':<15} | {'Neg First/Sec':<15} | {'NonNeg First/Sec':<15}")
print("-" * 80)

for cat_dir, cat_suffix, total_rows in categories:
    for lang in ["ENG", "BEN"]:
        path = f"fixed JsonL/BanglaBBQ_{lang}_{cat_suffix}_QA_fixed.jsonl"
        with open(path, 'r', encoding='utf-8') as f:
            rows = [json.loads(line) for line in f]
            
        labels = {}
        for r in rows:
            labels[r['label']] = labels.get(r['label'], 0) + 1
            
        neg_first, neg_second = 0, 0
        nonneg_first, nonneg_second = 0, 0
        
        for r in rows:
            if r['context_condition'] == 'disambig':
                ctx = r['context']
                ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
                e0, e1 = ans_ents[0], ans_ents[1]
                e0_c = e0.replace('The ', '').replace('the ', '')
                e1_c = e1.replace('The ', '').replace('the ', '')
                p0 = ctx.find(e0_c)
                p1 = ctx.find(e1_c)
                first_ent = e0 if p0 < p1 else e1
                second_ent = e1 if p0 < p1 else e0
                gold = r[f"ans{r['label']}"]
                
                if r['question_polarity'] == 'neg':
                    if gold == first_ent: neg_first += 1
                    else: neg_second += 1
                else:
                    if gold == first_ent: nonneg_first += 1
                    else: nonneg_second += 1
                    
        lbl_str = f"{labels.get(0,0)}/{labels.get(1,0)}/{labels.get(2,0)}"
        neg_str = f"{neg_first}/{neg_second}"
        nonneg_str = f"{nonneg_first}/{nonneg_second}"
        print(f"{cat_dir:<25} | {lang:<4} | {lbl_str:<15} | {neg_str:<15} | {nonneg_str:<15}")
