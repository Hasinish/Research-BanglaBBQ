import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]

for qi in ['1', '2', '3', '4', '5']:
    q_recs = [r for r in eng_rows if r['question_index'] == qi]
    # Check contexts
    contexts = sorted(list(set(r['context'] for r in q_recs)))
    print(f"\n================ Q{qi} ================")
    print(f"Total rows: {len(q_recs)}, Unique contexts: {len(contexts)}")
    for c_idx, ctx in enumerate(contexts):
        c_recs = [r for r in q_recs if r['context'] == ctx]
        perms = set((r['ans0'], r['ans1'], r['ans2']) for r in c_recs)
        print(f"Context {c_idx+1} ({len(c_recs)} rows): {len(perms)} perms | {ctx[:50]}...")
        for p in perms:
            print(f"    Ans: {[p[0][:15], p[1][:15], p[2][:15]]}")
