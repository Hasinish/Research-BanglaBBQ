import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

for qi in ['3', '4', '5']:
    q = [r for r in rows if r['question_index'] == qi]
    print(f"=== Q{qi} ===")
    print("Ambig context:", q[0]['context'])
    print("Disambig context:", q[1]['context'])
    print("Answers set (Row 0):", (q[0]['ans0'], q[0]['ans1'], q[0]['ans2']))
    print("Answer info:", q[0]['answer_info'])
    print("Labels across rows 0-15:", [r['label'] for r in q])
    print()
