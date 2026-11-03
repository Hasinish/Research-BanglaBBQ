import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

print("Scanning all 20 themes in Education for 'first'/'second' and 'প্রথম'/'দ্বিতীয়'...")
for t in range(20):
    # take disambig row
    er = erows[t * 144 + 1]
    br = brows[t * 144 + 1]
    
    # check sentence 3
    ectx = er['context']
    bctx = br['context']
    
    has_eng = ('second' in ectx.lower() and 'first' in ectx.lower())
    has_ben = ('দ্বিতীয়' in bctx and 'প্রথম' in bctx)
    
    print(f"Theme Q{t+1:02d}: ENG match={has_eng}, BEN match={has_ben}")
    if not has_eng or not has_ben:
        print(f"  ENG ctx: {ectx}")
        print(f"  BEN ctx: {bctx}")
