import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

er = erows[1 * 144 + 1]
br = brows[1 * 144 + 1]

print("ENG Context:", er['context'])
print("ENG Ans0:", er['ans0'], "| Ans1:", er['ans1'], "| Ans2:", er['ans2'])
print("ENG Label:", er['label'], er[f"ans{er['label']}"])

print("BEN Context:", br['context'])
print("BEN Ans0:", br['ans0'], "| Ans1:", br['ans1'], "| Ans2:", br['ans2'])
print("BEN Label:", br['label'], br[f"ans{br['label']}"])
