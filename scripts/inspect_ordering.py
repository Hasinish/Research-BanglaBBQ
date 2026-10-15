import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]

for i, r in enumerate(eng_rows[:24]):
    ans = [r['ans0'][:10], r['ans1'][:10], r['ans2'][:10]]
    print(f"{i:2d}: Q{r['question_index']} {r['context_condition']:8s} {r['question_polarity']:6s} | Ans: {ans} | Ctx: {r['context'][:35]}...")
