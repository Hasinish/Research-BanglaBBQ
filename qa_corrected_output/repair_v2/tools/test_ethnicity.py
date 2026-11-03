import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

roles_e = ['student', 'prospective tenant', 'tenant', 'resident', 'candidate', 'applicant', 'patient', 'complainant']
roles_b = ['শিক্ষার্থী', 'সম্ভাব্য ভাড়াটিয়া', 'ভাড়াটিয়া', 'বাসিন্দা', 'প্রার্থী', 'আবেদনকারী', 'রোগী', 'অভিযোগকারী']

def clean_eng_row(r):
    ctx = r['context']
    def repl_s1(m):
        g1, r1, g2, r2 = m.group(1), m.group(2), m.group(3), m.group(4)
        art1 = 'an' if g1.startswith('ethnic') else 'a'
        art2 = 'an' if g2.startswith('ethnic') else 'a'
        return f'{art1} {g1} {r1} and {art2} {g2} {r2}'
    
    ctx = re.sub(r'\b(Chakma|Munda|Marma|Mro|Santal|Garo \(Mandi\)|ethnic Bengali)\s+(' + '|'.join(roles_e) + r')\s+A\s+and\s+(Chakma|Munda|Marma|Mro|Santal|Garo \(Mandi\)|ethnic Bengali)\s+(' + '|'.join(roles_e) + r')\s+B\b', repl_s1, ctx)
    
    for role in sorted(roles_e, key=len, reverse=True):
        ctx = re.sub(rf'\b{role}\s+A\'s\b', f'the first {role}\'s', ctx)
        ctx = re.sub(rf'\b{role}\s+B\'s\b', f'the second {role}\'s', ctx)
        ctx = re.sub(rf'\b{role}\s+A\b', f'the first {role}', ctx)
        ctx = re.sub(rf'\b{role}\s+B\b', f'the second {role}', ctx)
        
        cap_role = role.capitalize()
        ctx = re.sub(rf'\b{cap_role}\s+A\'s\b', f'The first {role}\'s', ctx)
        ctx = re.sub(rf'\b{cap_role}\s+B\'s\b', f'The second {role}\'s', ctx)
        ctx = re.sub(rf'\b{cap_role}\s+A\b', f'The first {role}', ctx)
        ctx = re.sub(rf'\b{cap_role}\s+B\b', f'The second {role}', ctx)
        
    r['context'] = ctx
    
    for k in ['ans0', 'ans1', 'ans2']:
        if r['answer_info'][k][1] != 'unknown':
            clean_ans = re.sub(r'\s+[AB]$', '', r[k]).strip()
            if not clean_ans.startswith('The ') and not clean_ans.startswith('the '):
                clean_ans = 'The ' + clean_ans
            r[k] = clean_ans
            r['answer_info'][k][0] = clean_ans
        else:
            r['answer_info'][k][0] = 'Unknown'
            r[k] = 'Unknown'
    return r

def clean_ben_row(r):
    ctx = r['context']
    for role in sorted(roles_b, key=len, reverse=True):
        ctx = ctx.replace(f'{role} ক আর ', f'{role} এবং ')
        ctx = re.sub(rf'({role})\s+খ(\s+|$|[।,?!])', r'\1\2', ctx)
        ctx = ctx.replace(f'{role} ক', f'প্রথম {role}')
        ctx = ctx.replace(f'{role} খ', f'দ্বিতীয় {role}')
    r['context'] = ctx
    for k in ['ans0', 'ans1', 'ans2']:
        if r['answer_info'][k][1] != 'unknown':
            clean_ans = re.sub(r'\s+[কখ]$', '', r[k]).strip()
            r[k] = clean_ans
            r['answer_info'][k][0] = clean_ans
        else:
            r['answer_info'][k][0] = 'অজানা'
            r[k] = 'অজানা'
    return r

cleaned_e = [clean_eng_row(r) for r in erows]
cleaned_b = [clean_ben_row(r) for r in brows]

residuals_e = []
for i, r in enumerate(cleaned_e):
    for f in ['context', 'question', 'ans0', 'ans1', 'ans2']:
        m = re.findall(r"\bB\b|\b[AB]'s\b|\b[AB]’s\b", r[f])
        if m:
            residuals_e.append((i, f, m, r[f]))

residuals_b = []
for i, r in enumerate(cleaned_b):
    for f in ['context', 'question', 'ans0', 'ans1', 'ans2']:
        m = re.findall(r'(?:^|\s)[কখ](?:[\s।,?!]|$)', r[f])
        if m:
            residuals_b.append((i, f, m, r[f]))

print(f'English residual placeholders: {len(residuals_e)}')
print(f'Bengali residual placeholders: {len(residuals_b)}')
