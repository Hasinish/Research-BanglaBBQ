import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# Check label agreement
label_diff = 0
for i in range(2880):
    if erows[i]['label'] != brows[i]['label']:
        label_diff += 1
print(f"Religion label differences between ENG and BEN: {label_diff}")

# Check theme by theme
for t in range(20):
    t_erows = erows[t*144:(t+1)*144]
    t_brows = brows[t*144:(t+1)*144]
    
    # neg disambig rows
    e_neg = [r for r in t_erows if r['context_condition'] == 'disambig' and r['question_polarity'] == 'neg']
    b_neg = [r for r in t_brows if r['context_condition'] == 'disambig' and r['question_polarity'] == 'neg']
    
    # check first/second in ENG and BEN
    def get_fs(rows, lang):
        f, s = 0, 0
        for r in rows:
            ctx = r['context']
            ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
            e0, e1 = ans_ents[0], ans_ents[1]
            p0 = ctx.find(e0.split()[0])
            p1 = ctx.find(e1.split()[0])
            first_ent = e0 if p0 < p1 else e1
            second_ent = e1 if p0 < p1 else e0
            gold = r[f"ans{r['label']}"]
            if gold == first_ent: f += 1
            else: s += 1
        return f, s

    ef, es = get_fs(e_neg, 'ENG')
    bf, bs = get_fs(b_neg, 'BEN')
    print(f"Theme Q{t+1:02d}: ENG F={ef:2d}/S={es:2d} | BEN F={bf:2d}/S={bs:2d}")
