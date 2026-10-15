import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

for i in [0, 1, 2, 3]:
    r = rows[i]
    print(f"Row {i} | pol: {r['question_polarity']} | cond: {r['context_condition']} | label: {r['label']}")
    print(f"Context: {r['context']}")
    print(f"Question: {r['question']}")
    print(f"Answers: 0={r['ans0']} | 1={r['ans1']} | 2={r['ans2']}")
    print(f"Answer_info: {r['answer_info']}")
    print("-" * 50)
