import json

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

q1 = [r for r in rows if r['question_index'] == '1']
q2 = [r for r in rows if r['question_index'] == '2']

match = True
for i in range(32):
    r1, r2 = q1[i], q2[i]
    if r1['question_polarity'] != r2['question_polarity']: match = False
    if r1['context_condition'] != r2['context_condition']: match = False
    if r1['label'] != r2['label']: match = False
    
    # Check context ordering
    c1_opp = r1['context'].startswith("An opposition")
    c2_opp = r2['context'].startswith("An opposition")
    if c1_opp != c2_opp: match = False

print("Q1 and Q2 match 100% on every single property:", match)
