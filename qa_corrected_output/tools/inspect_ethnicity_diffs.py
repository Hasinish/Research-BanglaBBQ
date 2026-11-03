import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# Inspect Sentence 3 in all 10 themes for how student A/B or first/second appear
for t in range(10):
    dis_e = erows[t * 144 + 1]['context']
    amb_e = erows[t * 144]['context']
    diff_e = dis_e.replace(amb_e, '').strip()
    
    dis_b = brows[t * 144 + 1]['context']
    amb_b = brows[t * 144]['context']
    diff_b = dis_b.replace(amb_b, '').strip()
    
    print(f"Theme Q{t+1:02d}:")
    print(f"  ENG: {diff_e}")
    print(f"  BEN: {diff_b}")
