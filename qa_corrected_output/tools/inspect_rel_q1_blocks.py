import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]

# Inspect Theme 0 (Q01) blocks
for b in range(6):
    r = erows[b * 24 + 1] # neg disambig
    ctx = r['context']
    ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
    e0, e1 = ans_ents[0], ans_ents[1]
    e0_term = e0.replace('The ', '').replace('the ', '').split()[0]
    e1_term = e1.replace('The ', '').replace('the ', '').split()[0]
    p0 = ctx.find(e0_term)
    p1 = ctx.find(e1_term)
    first_ent = e0 if p0 < p1 else e1
    second_ent = e1 if p0 < p1 else e0
    gold = r[f"ans{r['label']}"]
    pos = "FIRST" if gold == first_ent else "SECOND"
    print(f"Block {b}: Gold={gold} ({pos}) | p0={p0}({e0_term}), p1={p1}({e1_term})")
    print("  Ctx:", ctx)
