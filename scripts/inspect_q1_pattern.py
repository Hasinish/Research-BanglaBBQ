import json

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

q1 = [r for r in rows if r["question_index"] == "1"]
print(f"Total Q1 rows: {len(q1)}")
for i, r in enumerate(q1):
    c_start = r["context"][:45]
    print(f"Row {i:2d} | pol: {r['question_polarity']:6s} | cond: {r['context_condition']:7s} | lbl: {r['label']} | c_start: {c_start} | ans0: {r['ans0'][:18]} | ans1: {r['ans1'][:18]} | ans2: {r['ans2'][:18]}")
