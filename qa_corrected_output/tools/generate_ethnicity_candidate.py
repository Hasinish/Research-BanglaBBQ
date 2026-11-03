import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# 1. Clean answer choices and questions
for i in range(1440):
    er = erows[i]
    br = brows[i]
    
    for k in ['ans0', 'ans1', 'ans2']:
        if er['answer_info'][k][1] != 'unknown':
            clean_e = re.sub(r'\s+[AB]$', '', er[k]).strip()
            if not clean_e.startswith('The ') and not clean_e.startswith('the '):
                clean_e = 'The ' + clean_e
            er[k] = clean_e
            
        if br['answer_info'][k][1] != 'unknown':
            clean_b = re.sub(r'\s+[কখ]$', '', br[k]).strip()
            br[k] = clean_b

    for target in [' A', ' B']:
        er['question'] = er['question'].replace(target, '')
    for target in [' ক', ' খ']:
        br['question'] = br['question'].replace(target, '')

# 2. Clean contexts cleanly separating ambig and diff
for i in range(0, 1440, 2):
    # even rows are ambig, odd rows are disambig
    er_amb = erows[i]
    er_dis = erows[i + 1]
    br_amb = brows[i]
    br_dis = brows[i + 1]
    
    # Clean ENG ambig
    e_amb = er_amb['context']
    e_amb = re.sub(r'\b(Chakma|Munda|Marma|Mro|Santal|Garo \(Mandi\)|ethnic Bengali)\s+(student|prospective tenant|resident|candidate|applicant|patient|complainant)\s+([AB])\b',
                   r'the \1 \2', e_amb)
    e_amb = e_amb.replace('the the ', 'the ')
    e_amb = re.sub(r',\s+the\b', ', the', e_amb)
    
    # Clean ENG diff
    e_diff = er_dis['context'][len(er_amb['context']):]
    for role in ['student', 'tenant', 'resident', 'candidate', 'applicant', 'patient', 'complainant']:
        e_diff = re.sub(rf'\b{role}\s+A\'s\b', f'the first {role}\'s', e_diff)
        e_diff = re.sub(rf'\b{role}\s+B\'s\b', f'the second {role}\'s', e_diff)
        e_diff = re.sub(rf'\b{role}\s+A\b', f'the first {role}', e_diff)
        e_diff = re.sub(rf'\b{role}\s+B\b', f'the second {role}', e_diff)
        
    er_amb['context'] = e_amb
    er_dis['context'] = e_amb + e_diff
    
    # Clean BEN ambig
    b_amb = br_amb['context']
    b_amb = re.sub(r'\s+[কখ]\b', '', b_amb)
    
    # Clean BEN diff
    b_diff = br_dis['context'][len(br_amb['context']):]
    b_diff = b_diff.replace('ভাড়াটিয়া খ', 'দ্বিতীয় ভাড়াটিয়া').replace('অভিযোগকারী ক', 'প্রথম অভিযোগকারী')
    
    br_amb['context'] = b_amb
    br_dis['context'] = b_amb + b_diff

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

# 3. Rebalance themes: 0, 2, 4, 6, 8 (Q01, Q03, Q05, Q07, Q09)
swap_themes = set([0, 2, 4, 6, 8])

for t in swap_themes:
    for idx in range(t * 144, (t + 1) * 144):
        er = erows[idx]
        br = brows[idx]
        
        if er['context_condition'] == 'disambig':
            amb_e = erows[idx - 1]['context']
            amb_b = brows[idx - 1]['context']
            
            diff_e = er['context'][len(amb_e):]
            diff_b = br['context'][len(amb_b):]
            
            new_diff_e = swap_ordinals_eng(diff_e)
            new_diff_b = swap_ordinals_ben(diff_b)
            
            er['context'] = amb_e + new_diff_e
            br['context'] = amb_b + new_diff_b
            
            ctx_e = amb_e
            non_unk = [k for k in ['ans0', 'ans1', 'ans2'] if er['answer_info'][k][1] != 'unknown']
            e0_k, e1_k = non_unk[0], non_unk[1]
            
            e0_clean = er[e0_k].replace('The ', '').replace('the ', '')
            e1_clean = er[e1_k].replace('The ', '').replace('the ', '')
            p0 = ctx_e.find(e0_clean)
            p1 = ctx_e.find(e1_clean)
            
            first_k = e0_k if p0 < p1 else e1_k
            second_k = e1_k if p0 < p1 else e0_k
            
            if er['question_polarity'] == 'neg':
                new_gold_k = second_k
            else:
                new_gold_k = first_k
                
            er['label'] = int(new_gold_k.replace('ans', ''))
            br['label'] = int(new_gold_k.replace('ans', ''))

# Write candidates
cand_dir = 'qa_corrected_output/candidates'
with open(f'{cand_dir}/BanglaBBQ_ENG_Ethnicity.jsonl', 'w', encoding='utf-8') as f:
    for r in erows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(f'{cand_dir}/BanglaBBQ_BEN_Ethnicity.jsonl', 'w', encoding='utf-8') as f:
    for r in brows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print("Ethnicity candidates generated successfully.")
