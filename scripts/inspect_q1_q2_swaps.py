import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    e_rows = [json.loads(line) for line in f if line.strip()]

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "r", encoding="utf-8") as f:
    b_rows = [json.loads(line) for line in f if line.strip()]

for qi in ['1', '2']:
    eq = [r for r in e_rows if r['question_index'] == qi]
    bq = [r for r in b_rows if r['question_index'] == qi]
    print(f"=== Q{qi} ===")
    print("ENG Order 1 Ambig (Row 0):", eq[0]['context'])
    print("ENG Order 2 Ambig (Row 4):", eq[4]['context'])
    print("ENG Order 1 Disambig (Row 1):", eq[1]['context'])
    print("ENG Order 2 Disambig (Row 5):", eq[5]['context'])
    print()
    print("BEN Order 1 Ambig (Row 0):", bq[0]['context'])
    print("BEN Order 2 Ambig (Row 4):", bq[4]['context'])
    print("BEN Order 1 Disambig (Row 1):", bq[1]['context'])
    print("BEN Order 2 Disambig (Row 5):", bq[5]['context'])
    print("=" * 70)
