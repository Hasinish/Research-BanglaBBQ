import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]

# Check theme 0 (first 144 rows)
for block_idx in range(6):
    start = block_idx * 24
    r_ambig_neg = erows[start]
    r_dis_neg = erows[start + 1]
    r_dis_nonneg = erows[start + 3]
    
    # entity order in s1
    ctx = r_ambig_neg['context']
    s1 = ctx.split('.')[0]
    
    ans_ents = [r_dis_neg[f'ans{i}'] for i in range(3) if r_dis_neg['answer_info'][f'ans{i}'][1] != 'unknown']
    
    gold_neg = r_dis_neg[f"ans{r_dis_neg['label']}"]
    gold_nonneg = r_dis_nonneg[f"ans{r_dis_nonneg['label']}"]
    
    # check positions of ans_ents in s1
    p0 = s1.find(ans_ents[0].replace('The ', '').replace('the ', ''))
    p1 = s1.find(ans_ents[1].replace('The ', '').replace('the ', ''))
    first_ent = ans_ents[0] if p0 < p1 else ans_ents[1]
    second_ent = ans_ents[1] if p0 < p1 else ans_ents[0]
    
    neg_pos = "FIRST" if gold_neg == first_ent else ("SECOND" if gold_neg == second_ent else "UNKNOWN")
    nonneg_pos = "FIRST" if gold_nonneg == first_ent else ("SECOND" if gold_nonneg == second_ent else "UNKNOWN")
    
    print(f"Block {block_idx} (rows {start:3d}-{start+23:3d}):")
    print(f"  First: {first_ent} | Second: {second_ent}")
    print(f"  Neg Gold: {gold_neg} ({neg_pos}) | NonNeg Gold: {gold_nonneg} ({nonneg_pos})")
    print(f"  Target in answer_info: {r_dis_neg['answer_info']['ans0'][1]}, {r_dis_neg['answer_info']['ans1'][1]}")
