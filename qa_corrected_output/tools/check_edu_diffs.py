import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for t in range(20):
    amb_e = erows[t * 144]['context']
    dis_e = erows[t * 144 + 1]['context']
    diff_e = dis_e.replace(amb_e, '').strip()
    
    amb_b = brows[t * 144]['context']
    dis_b = brows[t * 144 + 1]['context']
    diff_b = dis_b.replace(amb_b, '').strip()
    
    print(f"Theme Q{t+1:02d}:")
    print(f"  ENG diff: {diff_e}")
    print(f"  BEN diff: {diff_b}")
