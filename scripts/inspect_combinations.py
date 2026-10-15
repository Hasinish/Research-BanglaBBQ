import json
import sys
from itertools import permutations

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]

print(f"Current rows: ENG={len(eng_rows)}, BEN={len(ben_rows)}")

# Group by (question_index, context, question)
combos = {}
for er, br in zip(eng_rows, ben_rows):
    key = (er['question_index'], er['context_condition'], er['question_polarity'], er['context'])
    combos.setdefault(key, []).append((er, br))

print(f"Total unique (qi, cond, pol, context) combinations: {len(combos)}")

by_qi = {}
for (qi, cond, pol, ctx), items in combos.items():
    by_qi.setdefault(qi, []).append(((cond, pol, ctx), len(items)))

for qi, clist in sorted(by_qi.items()):
    print(f"\nTemplate Q{qi}: {len(clist)} combinations (should be 8)")
    for (cond, pol, ctx), count in clist:
        print(f"  [{cond:8s} | {pol:6s}] count={count} | Context snippet: {ctx[:60]}...")
