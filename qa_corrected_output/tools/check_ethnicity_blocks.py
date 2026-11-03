import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

print("Scanning Ethnicity themes and variations...")
for t in range(10):
    t_rows = erows[t * 144 : (t + 1) * 144]
    # check variations
    print(f"Theme Q{t+1:02d}:")
    for b in range(6):
        r = t_rows[b * 24]
        ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
        print(f"  Block {b} (row {t*144 + b*24}): {ans_ents}")
