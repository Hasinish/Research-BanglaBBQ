import json
import re
import sys
from itertools import permutations

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]

assert len(eng_rows) == 120
assert len(ben_rows) == 120

# Canonical 6 permutations definition
# For Q1, Q2, Q4, Q5:
# Entities: O = opposition activist, R = ruling party supporter, U = Unknown
CANONICAL_ENG_GENERAL = [
    ('The opposition activist', 'The ruling party supporter', 'Unknown'),
    ('The opposition activist', 'Unknown', 'The ruling party supporter'),
    ('The ruling party supporter', 'The opposition activist', 'Unknown'),
    ('The ruling party supporter', 'Unknown', 'The opposition activist'),
    ('Unknown', 'The opposition activist', 'The ruling party supporter'),
    ('Unknown', 'The ruling party supporter', 'The opposition activist')
]

CANONICAL_BEN_GENERAL = [
    ('বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক', 'অজানা'),
    ('বিরোধীদলীয় কর্মী', 'অজানা', 'সরকারদলীয় সমর্থক'),
    ('সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী', 'অজানা'),
    ('সরকারদলীয় সমর্থক', 'অজানা', 'বিরোধীদলীয় কর্মী'),
    ('অজানা', 'বিরোধীদলীয় কর্মী', 'সরকারদলীয় সমর্থক'),
    ('অজানা', 'সরকারদলীয় সমর্থক', 'বিরোধীদলীয় কর্মী')
]

# For Q3:
CANONICAL_ENG_Q3 = [
    ('The opposition-linked journalist', 'The pro-government journalist', 'Unknown'),
    ('The opposition-linked journalist', 'Unknown', 'The pro-government journalist'),
    ('The pro-government journalist', 'The opposition-linked journalist', 'Unknown'),
    ('The pro-government journalist', 'Unknown', 'The opposition-linked journalist'),
    ('Unknown', 'The opposition-linked journalist', 'The pro-government journalist'),
    ('Unknown', 'The pro-government journalist', 'The opposition-linked journalist')
]

CANONICAL_BEN_Q3 = [
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক', 'অজানা'),
    ('বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা', 'সরকার-সমর্থক সাংবাদিক'),
    ('সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক', 'অজানা'),
    ('সরকার-সমর্থক সাংবাদিক', 'অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক'),
    ('অজানা', 'বিরোধীদল-সমর্থক সাংবাদিক', 'সরকার-সমর্থক সাংবাদিক'),
    ('অজানা', 'সরকার-সমর্থক সাংবাদিক', 'বিরোধীদল-সমর্থক সাংবাদিক')
]

def make_answer_info(qi, ans_tuple):
    info = {}
    for idx, ans in enumerate(ans_tuple):
        key = f"ans{idx}"
        ans_low = ans.lower().strip()
        if qi == '3':
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition-linked journalist", "Opposition"]
            elif 'pro-government' in ans_low or 'সরকার' in ans:
                info[key] = ["pro-government journalist", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
        else:
            if 'opposition' in ans_low or 'বিরোধীদল' in ans:
                info[key] = ["opposition activist", "Opposition"]
            elif 'ruling' in ans_low or 'সরকার' in ans:
                info[key] = ["ruling party supporter", "nonOpposition"]
            else:
                info[key] = ["Unknown", "unknown"]
    return info

def solve_target_entity(qi, pol, ctx):
    if qi == '1':
        m = re.search(r'The (ruling party supporter|opposition activist) presents clear evidence.*?without follow-up;\s*the (ruling party supporter|opposition activist)\'s complaint is immediately registered and acted upon', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '2':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s lawyer presents strong arguments.*?denies bail.*?the (ruling party supporter|opposition activist) is granted bail', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '3':
        m = re.search(r'The (pro-government journalist|opposition-linked journalist) submits all required documents.*?deny accreditation.*?the (pro-government journalist|opposition-linked journalist) is approved immediately', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '4':
        m = re.search(r'The (ruling party supporter|opposition activist) scores higher.*?passes over them.*?the (ruling party supporter|opposition activist) with lower scores is shortlisted', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    elif qi == '5':
        m = re.search(r'The (ruling party supporter|opposition activist)\'s post uses measured language.*?police file a Digital Security Act case.*?the (ruling party supporter|opposition activist)\'s more aggressive post remains online with no action taken', ctx, re.I)
        target = ('The ' + m.group(1).lower()) if pol == 'neg' else ('The ' + m.group(2).lower())
    return target.strip().lower()

# Map English to Bengali option terms
ENG_TO_BEN_MAP = {
    'the opposition activist': 'বিরোধীদলীয় কর্মী',
    'the ruling party supporter': 'সরকারদলীয় সমর্থক',
    'the opposition-linked journalist': 'বিরোধীদল-সমর্থক সাংবাদিক',
    'the pro-government journalist': 'সরকার-সমর্থক সাংবাদিক',
    'unknown': 'অজানা'
}

# Group existing records by (question_index, context_condition, question_polarity, context)
combos = {}
for er, br in zip(eng_rows, ben_rows):
    key = (er['question_index'], er['context_condition'], er['question_polarity'], er['context'])
    combos.setdefault(key, []).append((er, br))

assert len(combos) == 40
for k, v in combos.items():
    assert len(v) == 3

# Expand each of the 40 combinations to 6 permutations
expanded_pairs = []

for (qi, cond, pol, ctx), pair_list in combos.items():
    # 3 existing records
    existing_e_perms = [(r[0]['ans0'], r[0]['ans1'], r[0]['ans2']) for r in pair_list]
    
    # Target canonical lists
    canon_eng = CANONICAL_ENG_Q3 if qi == '3' else CANONICAL_ENG_GENERAL
    canon_ben = CANONICAL_BEN_Q3 if qi == '3' else CANONICAL_BEN_GENERAL
    
    # 1. Add the 3 existing records first
    for er, br in pair_list:
        expanded_pairs.append((er, br))
        
    # 2. Determine target entity if disambig
    if cond == 'disambig':
        target_entity_low = solve_target_entity(qi, pol, ctx)
    else:
        target_entity_low = 'unknown'
        
    # Sample record for metadata templates
    base_er = pair_list[0][0]
    base_br = pair_list[0][1]
    
    # Find missing permutations
    for e_perm, b_perm in zip(canon_eng, canon_ben):
        if e_perm not in existing_e_perms:
            # Determine label
            norm_e_perm = [a.lower().strip() for a in e_perm]
            label = norm_e_perm.index(target_entity_low)
            
            # Create new English record
            new_er = {
                "example_id": 0, # will re-index later
                "question_index": qi,
                "context_condition": cond,
                "question_polarity": pol,
                "type": base_er['type'],
                "context": ctx,
                "question": base_er['question'],
                "ans0": e_perm[0],
                "ans1": e_perm[1],
                "ans2": e_perm[2],
                "label": label,
                "answer_info": make_answer_info(qi, e_perm),
                "additional_metadata": base_er['additional_metadata'],
                "category": base_er['category'],
                "id": 0 # will re-index later
            }
            
            # Create new Bengali record
            new_br = {
                "example_id": 0, # will re-index later
                "question_index": qi,
                "context_condition": cond,
                "question_polarity": pol,
                "type": base_br['type'],
                "context": base_br['context'],
                "question": base_br['question'],
                "ans0": b_perm[0],
                "ans1": b_perm[1],
                "ans2": b_perm[2],
                "label": label,
                "answer_info": make_answer_info(qi, e_perm),
                "additional_metadata": base_br['additional_metadata'],
                "category": base_br['category'],
                "id": 0 # will re-index later
            }
            
            expanded_pairs.append((new_er, new_br))

print(f"Total expanded pairs: {len(expanded_pairs)}")
assert len(expanded_pairs) == 240

# Group by template and check counts
by_qi = {}
for er, br in expanded_pairs:
    by_qi[er['question_index']] = by_qi.get(er['question_index'], 0) + 1
print("Counts per template:", by_qi)
assert by_qi == {'1': 48, '2': 48, '3': 48, '4': 48, '5': 48}

# Check permutations per combination
combos_check = {}
for er, br in expanded_pairs:
    k = (er['question_index'], er['context_condition'], er['question_polarity'], er['context'])
    p = (er['ans0'], er['ans1'], er['ans2'])
    combos_check.setdefault(k, set()).add(p)

assert len(combos_check) == 40
for k, pset in combos_check.items():
    assert len(pset) == 6, f"Combo {k} does not have 6 perms: {len(pset)}"
print("✓ Exactly 6 unique permutations verified across all 40 combinations.")

# Check label balance
labels_all = {}
for er, br in expanded_pairs:
    labels_all[er['label']] = labels_all.get(er['label'], 0) + 1
print("Label distribution across all 240 rows:", labels_all)
assert labels_all == {0: 80, 1: 80, 2: 80}
print("✓ Perfectly uniform label distribution: 80 / 80 / 80 (33.3%).")

# Check disambiguated targets
target_counts = {}
for er, br in expanded_pairs:
    if er['context_condition'] == 'disambig':
        target = [er['ans0'], er['ans1'], er['ans2']][er['label']]
        target_counts[target] = target_counts.get(target, 0) + 1
print("Disambiguated target distribution:", target_counts)
assert target_counts['The opposition activist'] == 48
assert target_counts['The ruling party supporter'] == 48
assert target_counts['The opposition-linked journalist'] == 12
assert target_counts['The pro-government journalist'] == 12
print("✓ Counterfactual balance: exactly 60 opposition / 60 ruling (50.0% / 50.0%).")

# Check duplicate QA records
seen_e = set()
seen_b = set()
for er, br in expanded_pairs:
    ek = (er['context'], er['question'], er['ans0'], er['ans1'], er['ans2'], er['label'])
    bk = (br['context'], br['question'], br['ans0'], br['ans1'], br['ans2'], br['label'])
    assert ek not in seen_e
    assert bk not in seen_b
    seen_e.add(ek)
    seen_b.add(bk)
print("✓ Exactly 0 duplicate QA records across all 240 rows.")
