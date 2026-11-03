import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# 1. Clean entities in ans0, ans1, ans2, and answer_info
for i in range(1440):
    er = erows[i]
    br = brows[i]
    
    # English answers
    for k in ['ans0', 'ans1', 'ans2']:
        if er['answer_info'][k][1] != 'unknown':
            # Remove ' A' or ' B' suffix
            clean_e = re.sub(r'\s+[AB]$', '', er[k]).strip()
            if not clean_e.startswith('The ') and not clean_e.startswith('the '):
                clean_e = 'The ' + clean_e
            er[k] = clean_e
            
        if br['answer_info'][k][1] != 'unknown':
            # Remove ' ক' or ' খ' suffix
            clean_b = re.sub(r'\s+[কখ]$', '', br[k]).strip()
            br[k] = clean_b

    # Clean question text if it has A or B / ক or খ
    for target in [' A', ' B']:
        er['question'] = er['question'].replace(target, '')
    for target in [' ক', ' খ']:
        br['question'] = br['question'].replace(target, '')

# 2. Clean contexts across all 1440 rows
# In Sentence 1:
# ENG: replace 'student A and ethnic Bengali student B' with 'the student and the ethnic Bengali student'
# More systematically: in ENG Sentence 1:
# replace ' A and ' with ' and the ' (or ' and ')
# Let's inspect context patterns
for i in range(1440):
    er = erows[i]
    br = brows[i]
    
    # In Bengali:
    # replace ' ক আর ' with ' আর '
    # replace ' খ ' with ' ' (in sentence 1)
    # replace 'ভাড়াটিয়া খ' with 'দ্বিতীয় ভাড়াটিয়া'
    # replace 'অভিযোগকারী ক' with 'প্রথম অভিযোগকারী'
    b_ctx = br['context']
    b_ctx = b_ctx.replace(' ক আর ', ' আর ')
    b_ctx = b_ctx.replace(' খ একই ', ' একই ')
    b_ctx = b_ctx.replace('ভাড়াটিয়া খ', 'দ্বিতীয় ভাড়াটিয়া')
    b_ctx = b_ctx.replace('অভিযোগকারী ক', 'প্রথম অভিযোগকারী')
    # clean any stray ক/খ after demographic terms
    b_ctx = re.sub(r'(জনগোষ্ঠীর\s+[^\s]+)\s+[কখ]\b', r'\1', b_ctx)
    br['context'] = b_ctx
    
    # In English:
    # replace ' A and ' with ' and the '
    # replace ' B are ' with ' are '
    # replace ' B live ' with ' live '
    # replace ' B apply ' with ' apply '
    # replace ' B have ' with ' have '
    # replace ' B pursue ' with ' pursue '
    # replace ' B were ' with ' were '
    # replace ' B is ' with ' is '
    e_ctx = er['context']
    # Let's replace ' [role] A' and ' [role] B' in Sentence 1:
    # We can match: '(Chakma|Munda|Marma|Mro|Santal|Garo \(Mandi\)|ethnic Bengali) (student|prospective tenant|resident|candidate|applicant|patient|complainant) [AB]'
    def clean_s1_eng(match):
        group = match.group(1)
        role = match.group(2)
        tag = match.group(3)
        return f"{group} {role}"
    
    e_ctx = re.sub(r'\b(Chakma|Munda|Marma|Mro|Santal|Garo \(Mandi\)|ethnic Bengali)\s+(student|prospective tenant|resident|candidate|applicant|patient|complainant)\s+([AB])\b',
                   r'the \1 \2', e_ctx)
    # Fix 'At a ... , the ...' capitalization or double 'the'
    e_ctx = e_ctx.replace('the the ', 'the ')
    e_ctx = re.sub(r',\s+the\b', ', the', e_ctx)
    
    # Now in Sentence 3 (diff):
    # replace 'student A' with 'the first student', 'student B' with 'the second student'
    # 'tenant A' -> 'the first tenant', 'tenant B' -> 'the second tenant'
    # 'resident A' -> 'the first resident', 'resident B' -> 'the second resident'
    # 'candidate A' -> 'the first candidate', 'candidate B' -> 'the second candidate'
    # 'applicant A' -> 'the first applicant', 'applicant B' -> 'the second applicant'
    # 'patient A' -> 'the first patient', 'patient B' -> 'the second patient'
    # 'complainant A' -> 'the first complainant', 'complainant B' -> 'the second complainant'
    for role in ['student', 'tenant', 'resident', 'candidate', 'applicant', 'patient', 'complainant']:
        # Possessive
        e_ctx = re.sub(rf'\b{role}\s+A\'s\b', f'the first {role}\'s', e_ctx)
        e_ctx = re.sub(rf'\b{role}\s+B\'s\b', f'the second {role}\'s', e_ctx)
        e_ctx = re.sub(rf'\b{role}\s+A\b', f'the first {role}', e_ctx)
        e_ctx = re.sub(rf'\b{role}\s+B\b', f'the second {role}', e_ctx)
        
    er['context'] = e_ctx

print("Context cleaning pass done. Checking samples...")
for t in [0, 1]:
    print(f"Theme Q{t+1:02d} ENG Ctx:", erows[t*144 + 1]['context'])
    print(f"Theme Q{t+1:02d} BEN Ctx:", brows[t*144 + 1]['context'])
