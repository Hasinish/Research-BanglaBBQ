import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

def swap_ordinals_eng(text):
    def repl(m):
        w = m.group(0)
        if w == 'first': return 'second'
        if w == 'First': return 'Second'
        if w == 'second': return 'first'
        if w == 'Second': return 'First'
        return w
    return re.sub(r'\b(first|second|First|Second)\b', repl, text)

def swap_ordinals_ben(text):
    t = text.replace('প্রথম', '@@FIRST@@')
    t = t.replace('দ্বিতীয়', 'প্রথম')
    t = t.replace('@@FIRST@@', 'দ্বিতীয়')
    return t

# 10 themes to swap: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19 (indices 0-based)
swap_themes = set([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

for t in swap_themes:
    for idx in range(t * 144, (t + 1) * 144):
        er = erows[idx]
        br = brows[idx]
        
        if er['context_condition'] == 'disambig':
            # Swap sentence 3 in context
            # Find common ambiguous prefix
            amb_idx = idx - 1 if er['question_polarity'] == 'neg' else idx - 1
            # In our blocks, even indices are ambig, odd are disambig (0: ambig neg, 1: dis neg, 2: ambig nonneg, 3: dis nonneg, ...)
            # Let's get the ambig context for this exact question and perm
            # The ambig counterpart is at idx - 1
            amb_e = erows[idx - 1]['context']
            amb_b = brows[idx - 1]['context']
            
            diff_e = er['context'][len(amb_e):]
            diff_b = br['context'][len(amb_b):]
            
            new_diff_e = swap_ordinals_eng(diff_e)
            new_diff_b = swap_ordinals_ben(diff_b)
            
            er['context'] = amb_e + new_diff_e
            br['context'] = amb_b + new_diff_b
            
            # Now update the gold label:
            # Previously:
            # neg question gold was first person
            # nonneg question gold was second person
            # With swapped context:
            # neg question gold is second person
            # nonneg question gold is first person
            # Let's find first and second person from Sentence 1
            s1_e = amb_e.split('.')[0]
            non_unk = [k for k in ['ans0', 'ans1', 'ans2'] if er['answer_info'][k][1] != 'unknown']
            e0_k, e1_k = non_unk[0], non_unk[1]
            
            # Match in s1_e
            # Clean entity name for searching (remove 'The ', 'the ')
            e0_clean = er[e0_k].replace('The ', '').replace('the ', '')
            e1_clean = er[e1_k].replace('The ', '').replace('the ', '')
            p0 = s1_e.find(e0_clean)
            p1 = s1_e.find(e1_clean)
            if p0 == -1 or p1 == -1:
                print(f"Warning: could not find entities in s1 at row {idx}")
            
            first_k = e0_k if p0 < p1 else e1_k
            second_k = e1_k if p0 < p1 else e0_k
            
            if er['question_polarity'] == 'neg':
                new_gold_k = second_k
            else:
                new_gold_k = first_k
                
            # Update label
            er['label'] = int(new_gold_k.replace('ans', ''))
            br['label'] = int(new_gold_k.replace('ans', ''))

# Save candidate files
cand_dir = 'qa_corrected_output/candidates'
with open(f'{cand_dir}/BanglaBBQ_ENG_Education.jsonl', 'w', encoding='utf-8') as f:
    for r in erows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(f'{cand_dir}/BanglaBBQ_BEN_Education.jsonl', 'w', encoding='utf-8') as f:
    for r in brows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print("Successfully written candidate files. Now verifying...")
