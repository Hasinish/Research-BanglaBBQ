import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

q1 = [r for r in rows if r['question_index'] == '1']
q2 = [r for r in rows if r['question_index'] == '2']

print(f"{'Idx':<4} | {'pol':<6} | {'cond':<8} | {'lbl':<3} | {'C_order':<7} | {'ans_order (0, 1, 2)'}")
print("-" * 65)
for i in range(32):
    r1 = q1[i]
    # Check context order: does Opposition come first or Ruling party?
    c_order = "Opp1st" if r1['context'].startswith("An opposition") else "Rul1st"
    # Identify answers: Target (Opposition) = T, Non-target (Ruling) = N, Unknown = U
    ans_map = {}
    for idx in range(3):
        val = r1[f'ans{idx}'].lower()
        if 'unknown' in val:
            ans_map[idx] = 'U'
        elif 'opposition' in val:
            ans_map[idx] = 'T'
        else:
            ans_map[idx] = 'N'
    perm = f"({ans_map[0]}, {ans_map[1]}, {ans_map[2]})"
    print(f"{i:<4} | {r1['question_polarity']:<6} | {r1['context_condition']:<8} | {r1['label']:<3} | {c_order:<7} | {perm}")
