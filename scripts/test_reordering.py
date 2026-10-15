import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]

# Canonical 6 permutations definition
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

# Build index of existing templates
reordered_eng = []
reordered_ben = []

# Order of 4 conditions per permutation
FOUR_ROW_CONDITIONS = [
    ('ambig', 'neg'),
    ('disambig', 'neg'),
    ('ambig', 'nonneg'),
    ('disambig', 'nonneg')
]

for qi in ['1', '2', '3', '4', '5']:
    e_q_recs = [r for r in eng_rows if r['question_index'] == qi]
    b_q_recs = [r for r in ben_rows if r['question_index'] == qi]
    
    # Identify the two orientations
    # Orientation 1: opposition first (or version a)
    # Orientation 2: ruling party first (or version b)
    # We can separate by looking at the ambig context text:
    ambig_e_ctxs = sorted(list(set(r['context'] for r in e_q_recs if r['context_condition'] == 'ambig')))
    assert len(ambig_e_ctxs) == 2
    
    # Sort so 'An opposition...' is first, then 'A ruling party...' / 'A pro-government...'
    # Let's inspect them:
    if 'opposition' in ambig_e_ctxs[0].lower():
        orientations_e = [ambig_e_ctxs[0], ambig_e_ctxs[1]]
    else:
        orientations_e = [ambig_e_ctxs[1], ambig_e_ctxs[0]]
        
    canon_eng = CANONICAL_ENG_Q3 if qi == '3' else CANONICAL_ENG_GENERAL
    canon_ben = CANONICAL_BEN_Q3 if qi == '3' else CANONICAL_BEN_GENERAL
    
    theme_eng = []
    theme_ben = []
    
    for orient_ctx_ambig in orientations_e:
        # Find matching disambig context
        disambig_cand = [r['context'] for r in e_q_recs if r['context_condition'] == 'disambig' and r['context'].startswith(orient_ctx_ambig[:40])]
        assert len(disambig_cand) > 0, f"No disambig context matching {orient_ctx_ambig[:40]}"
        orient_ctx_disambig = disambig_cand[0]
        
        # Find matching Bengali contexts
        b_ambig_match = next(r['context'] for r in b_q_recs if r['context_condition'] == 'ambig' and any(er['context'] == orient_ctx_ambig and er['id'] == r['id'] for er in e_q_recs))
        b_disambig_match = next(r['context'] for r in b_q_recs if r['context_condition'] == 'disambig' and any(er['context'] == orient_ctx_disambig and er['id'] == r['id'] for er in e_q_recs))
        
        # Base metadata from this orientation
        sample_er = next(r for r in e_q_recs if r['context'] == orient_ctx_ambig)
        sample_br = next(r for r in b_q_recs if r['context'] == b_ambig_match)
        
        # Questions for this template
        q_neg_e = next(r['question'] for r in e_q_recs if r['question_polarity'] == 'neg')
        q_nonneg_e = next(r['question'] for r in e_q_recs if r['question_polarity'] == 'nonneg')
        q_neg_b = next(r['question'] for r in b_q_recs if r['question_polarity'] == 'neg')
        q_nonneg_b = next(r['question'] for r in b_q_recs if r['question_polarity'] == 'nonneg')
        
        # For each of the 6 answer permutations
        for perm_idx, (e_perm, b_perm) in enumerate(zip(canon_eng, canon_ben)):
            # Generate the 4-row block
            for cond, pol in FOUR_ROW_CONDITIONS:
                e_ctx = orient_ctx_ambig if cond == 'ambig' else orient_ctx_disambig
                b_ctx = b_ambig_match if cond == 'ambig' else b_disambig_match
                e_q = q_neg_e if pol == 'neg' else q_nonneg_e
                b_q = q_neg_b if pol == 'neg' else q_nonneg_b
                
                # Determine gold label
                if cond == 'ambig':
                    target_low = 'unknown'
                else:
                    target_low = solve_target_entity(qi, pol, e_ctx)
                    
                norm_e_perm = [a.lower().strip() for a in e_perm]
                label = norm_e_perm.index(target_low)
                
                # Create English record
                rec_e = {
                    "example_id": 0,
                    "question_index": qi,
                    "context_condition": cond,
                    "question_polarity": pol,
                    "type": sample_er['type'],
                    "context": e_ctx,
                    "question": e_q,
                    "ans0": e_perm[0],
                    "ans1": e_perm[1],
                    "ans2": e_perm[2],
                    "label": label,
                    "answer_info": make_answer_info(qi, e_perm),
                    "additional_metadata": sample_er['additional_metadata'],
                    "category": sample_er['category'],
                    "id": 0
                }
                
                # Create Bengali record
                rec_b = {
                    "example_id": 0,
                    "question_index": qi,
                    "context_condition": cond,
                    "question_polarity": pol,
                    "type": sample_br['type'],
                    "context": b_ctx,
                    "question": b_q,
                    "ans0": b_perm[0],
                    "ans1": b_perm[1],
                    "ans2": b_perm[2],
                    "label": label,
                    "answer_info": make_answer_info(qi, e_perm),
                    "additional_metadata": sample_br['additional_metadata'],
                    "category": sample_br['category'],
                    "id": 0
                }
                
                theme_eng.append(rec_e)
                theme_ben.append(rec_b)
                
    assert len(theme_eng) == 48, f"Q{qi} theme records count: {len(theme_eng)}"
    assert len(theme_ben) == 48, f"Q{qi} theme records count: {len(theme_ben)}"
    
    reordered_eng.extend(theme_eng)
    reordered_ben.extend(theme_ben)

print(f"Total reordered records: ENG={len(reordered_eng)}, BEN={len(reordered_ben)}")
assert len(reordered_eng) == 240
assert len(reordered_ben) == 240

# Verify the 4-row block structure throughout all 240 rows!
for block_idx in range(60): # 240 / 4 = 60 blocks
    start = block_idx * 4
    block = reordered_eng[start:start+4]
    
    # 1. Condition sequence
    conds = [(r['context_condition'], r['question_polarity']) for r in block]
    assert conds == FOUR_ROW_CONDITIONS, f"Block {block_idx} condition mismatch: {conds}"
    
    # 2. Answer permutation invariance within the block
    perm0 = (block[0]['ans0'], block[0]['ans1'], block[0]['ans2'])
    for r in block[1:]:
        perm = (r['ans0'], r['ans1'], r['ans2'])
        assert perm == perm0, f"Block {block_idx} answers not identical: {perm} vs {perm0}"

print("✓ 100% PASS: All 60 blocks strictly follow the exact 4-row structure (ambig+neg, disambig+neg, ambig+nonneg, disambig+nonneg) with identical answer permutations!")
