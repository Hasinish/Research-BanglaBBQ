import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for lang, rows in [("ENG", erows), ("BEN", brows)]:
    neg_first, neg_second = 0, 0
    nonneg_first, nonneg_second = 0, 0
    
    for r in rows:
        if r['context_condition'] == 'disambig':
            ctx = r['context']
            ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
            e0, e1 = ans_ents[0], ans_ents[1]
            
            # Use clean full string
            e0_clean = e0.replace('The ', '').replace('the ', '')
            e1_clean = e1.replace('The ', '').replace('the ', '')
            
            p0 = ctx.find(e0_clean)
            p1 = ctx.find(e1_clean)
            
            first_ent = e0 if p0 < p1 else e1
            second_ent = e1 if p0 < p1 else e0
            gold = r[f"ans{r['label']}"]
            
            if r['question_polarity'] == 'neg':
                if gold == first_ent: neg_first += 1
                else: neg_second += 1
            else:
                if gold == first_ent: nonneg_first += 1
                else: nonneg_second += 1
                
    print(f"Full-string {lang} Disambig Position Balance:")
    print(f"  Neg:    First={neg_first}, Second={neg_second}")
    print(f"  NonNeg: First={nonneg_first}, Second={nonneg_second}")
