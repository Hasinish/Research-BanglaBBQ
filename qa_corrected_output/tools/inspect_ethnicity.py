import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

print("Total Ethnicity rows:", len(erows), len(brows))

# Inspect row 0 (ambig) and row 1 (disambig)
for i in [0, 1]:
    print(f"=== ROW {i} ENG ===")
    print("Context: ", erows[i]['context'])
    print("Question:", erows[i]['question'])
    print("ans0:", erows[i]['ans0'], "| ans1:", erows[i]['ans1'], "| ans2:", erows[i]['ans2'])
    print(f"=== ROW {i} BEN ===")
    print("Context: ", brows[i]['context'])
    print("Question:", brows[i]['question'])
    print("ans0:", brows[i]['ans0'], "| ans1:", brows[i]['ans1'], "| ans2:", brows[i]['ans2'])
