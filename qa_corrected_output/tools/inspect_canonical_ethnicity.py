import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for i in [0, 1]:
    print(f"=== CANONICAL ROW {i} ENG ===")
    print("Context: ", erows[i]['context'])
    print("Question:", erows[i]['question'])
    print("ans0:", erows[i]['ans0'], "| ans1:", erows[i]['ans1'], "| ans2:", erows[i]['ans2'])
    print(f"=== CANONICAL ROW {i} BEN ===")
    print("Context: ", brows[i]['context'])
    print("Question:", brows[i]['question'])
    print("ans0:", brows[i]['ans0'], "| ans1:", brows[i]['ans1'], "| ans2:", brows[i]['ans2'])
