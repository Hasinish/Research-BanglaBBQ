import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# Check ans0, ans1 across all 10 themes
eng_entities = set()
ben_entities = set()
for r in erows:
    for k in ['ans0', 'ans1', 'ans2']:
        if r['answer_info'][k][1] != 'unknown':
            eng_entities.add(r[k])
for r in brows:
    for k in ['ans0', 'ans1', 'ans2']:
        if r['answer_info'][k][1] != 'unknown':
            ben_entities.add(r[k])

print("ENG entities found:")
for e in sorted(eng_entities):
    print("  ", repr(e))

print("\nBEN entities found:")
for b in sorted(ben_entities):
    print("  ", repr(b))
