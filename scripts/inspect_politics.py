import json

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

q1 = [r for r in rows if r["question_index"] == "1"]
print(f"Q1 total rows: {len(q1)}")
for i in [0, 1, 2, 3, 4, 5, 6, 7]:
    r = q1[i]
    print(f"Row {i:2d} | pol: {r['question_polarity']:6s} | cond: {r['context_condition']:7s} | label: {r['label']} | q: {r['question'][:30]} | context: {r['context'][:40]} | ans: ({r['ans0'][:15]}, {r['ans1'][:15]}, {r['ans2'][:15]})")

q3 = [r for r in rows if r["question_index"] == "3"]
print(f"\nQ3 total rows: {len(q3)}")
for i in range(len(q3)):
    r = q3[i]
    print(f"Row {i:2d} | pol: {r['question_polarity']:6s} | cond: {r['context_condition']:7s} | label: {r['label']} | q: {r['question'][:30]} | context: {r['context'][:40]} | ans: ({r['ans0'][:15]}, {r['ans1'][:15]}, {r['ans2'][:15]})")
