import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

print('Total rows:', len(erows), len(brows))

print("Row 24 Ctx:", erows[24]['context'])
print("Row 25 Ctx:", erows[25]['context'])
print("Row 25 Question:", erows[25]['question'])
print("Row 25 Label:", erows[25]['label'], erows[25][f"ans{erows[25]['label']}"])
print("Row 25 BEN Ctx:", brows[25]['context'])


