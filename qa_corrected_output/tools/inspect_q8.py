import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('qa_corrected_output/candidates/BanglaBBQ_BEN_Ethnicity.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]
with open('qa_corrected_output/candidates/BanglaBBQ_ENG_Ethnicity.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]

t = 7 # Q08
for b in range(6):
    r_b = brows[t * 144 + b * 24 + 1] # neg disambig
    r_e = erows[t * 144 + b * 24 + 1]
    print(f"Block {b}:")
    print("  ENG Ctx:", r_e['context'])
    print("  ENG Gold:", r_e[f"ans{r_e['label']}"])
    print("  BEN Ctx:", r_b['context'])
    print("  BEN Gold:", r_b[f"ans{r_b['label']}"])
