import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

def swap_ordinals_eng(text):
    # swap first and second (case-insensitive or preserving case)
    def repl(m):
        w = m.group(0)
        if w == 'first': return 'second'
        if w == 'First': return 'Second'
        if w == 'second': return 'first'
        if w == 'Second': return 'First'
        return w
    return re.sub(r'\b(first|second|First|Second)\b', repl, text)

def swap_ordinals_ben(text):
    # swap প্রথম and দ্বিতীয়
    # use temporary token
    t = text.replace('প্রথম', '@@FIRST@@')
    t = t.replace('দ্বিতীয়', 'প্রথম')
    t = t.replace('@@FIRST@@', 'দ্বিতীয়')
    return t

for t in [0, 1, 2, 3]:
    r_e = erows[t * 144 + 1]
    r_b = brows[t * 144 + 1]
    
    orig_ec = r_e['context']
    orig_bc = r_b['context']
    
    amb_ec = erows[t * 144]['context']
    amb_bc = brows[t * 144]['context']
    
    diff_e = orig_ec.replace(amb_ec, '').strip()
    diff_b = orig_bc.replace(amb_bc, '').strip()
    
    swapped_diff_e = swap_ordinals_eng(diff_e)
    swapped_diff_b = swap_ordinals_ben(diff_b)
    
    print(f"=== Theme Q{t+1:02d} ===")
    print("Orig ENG diff:   ", diff_e)
    print("Swapped ENG diff:", swapped_diff_e)
    print("Orig BEN diff:   ", diff_b)
    print("Swapped BEN diff:", swapped_diff_b)
