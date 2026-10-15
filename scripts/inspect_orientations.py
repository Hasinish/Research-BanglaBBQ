import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]

for qi in ['1', '2', '3', '4', '5']:
    q_recs = [r for r in eng_rows if r['question_index'] == qi]
    # Unique contexts for ambig
    ambig_ctxs = sorted(list(set(r['context'] for r in q_recs if r['context_condition'] == 'ambig')))
    # Unique contexts for disambig
    disambig_ctxs = sorted(list(set(r['context'] for r in q_recs if r['context_condition'] == 'disambig')))
    
    print(f"\n================ Q{qi} ================")
    print("Ambig contexts count:", len(ambig_ctxs))
    for c in ambig_ctxs:
        print("  AMBIG:   ", c[:65])
    print("Disambig contexts count:", len(disambig_ctxs))
    for c in disambig_ctxs:
        print("  DISAMBIG:", c[:65])
