import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]

# Inspect Theme 1 Block 0 and Block 1
for b in [0, 1]:
    r_b = brows[b * 24 + 1]
    r_e = erows[b * 24 + 1]
    print(f"=== Block {b} ===")
    print("ENG ctx:", r_e['context'])
    print("ENG ans:", [r_e[f'ans{i}'] for i in range(3)], "Gold:", r_e[f"ans{r_e['label']}"])
    print("BEN ctx:", r_b['context'])
    print("BEN ans:", [r_b[f'ans{i}'] for i in range(3)], "Gold:", r_b[f"ans{r_b['label']}"])
