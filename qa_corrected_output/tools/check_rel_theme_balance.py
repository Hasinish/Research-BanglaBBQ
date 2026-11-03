import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]

for t in range(20):
    t_rows = erows[t*144:(t+1)*144]
    neg_dis = [r for r in t_rows if r['context_condition'] == 'disambig' and r['question_polarity'] == 'neg']
    first, second = 0, 0
    for r in neg_dis:
        ctx = r['context']
        ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
        e0, e1 = ans_ents[0], ans_ents[1]
        e0_term = e0.replace('The ', '').replace('the ', '').split()[0]
        e1_term = e1.replace('The ', '').replace('the ', '').split()[0]
        p0 = ctx.find(e0_term)
        p1 = ctx.find(e1_term)
        first_ent = e0 if p0 < p1 else e1
        gold = r[f"ans{r['label']}"]
        if gold == first_ent: first += 1
        else: second += 1
    print(f"Theme Q{t+1:02d}: First={first:2d}, Second={second:2d}")
