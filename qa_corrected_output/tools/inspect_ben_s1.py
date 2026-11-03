import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('qa_corrected_output/candidates/BanglaBBQ_BEN_Ethnicity.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for t in [2, 3]: # Theme 3 and 4
    for b in range(6):
        r = brows[t * 144 + b * 24]
        s1 = r['context'].split('।')[0]
        ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
        print(f"Theme Q{t+1:02d} Block {b}:")
        print(f"  s1: {s1}")
        print(f"  ans0: {r['ans0']} | ans1: {r['ans1']}")
        p0 = s1.find(ans_ents[0])
        p1 = s1.find(ans_ents[1])
        print(f"  p0={p0}, p1={p1} (ans_ents[0]={ans_ents[0]}, ans_ents[1]={ans_ents[1]})")
