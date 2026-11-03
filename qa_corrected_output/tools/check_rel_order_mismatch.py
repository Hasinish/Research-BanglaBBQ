import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for t in range(20):
    er = erows[t * 144 + 1]
    br = brows[t * 144 + 1]
    
    e_ans = [er[f'ans{i}'] for i in range(3) if er['answer_info'][f'ans{i}'][1] != 'unknown']
    b_ans = [br[f'ans{i}'] for i in range(3) if br['answer_info'][f'ans{i}'][1] != 'unknown']
    
    e0_c = e_ans[0].replace('The ', '').replace('the ', '')
    e1_c = e_ans[1].replace('The ', '').replace('the ', '')
    e_p0 = er['context'].find(e0_c)
    e_p1 = er['context'].find(e1_c)
    e_first = 0 if e_p0 < e_p1 else 1
    
    b_p0 = br['context'].find(b_ans[0])
    b_p1 = br['context'].find(b_ans[1])
    b_first = 0 if b_p0 < b_p1 else 1
    
    match = (e_first == b_first)
    print(f"Theme Q{t+1:02d}: Match={match} (ENG first={e_ans[e_first]}, BEN first={b_ans[b_first]})")
    if not match:
        print("  ENG ctx:", er['context'][:100])
        print("  BEN ctx:", br['context'][:100])
