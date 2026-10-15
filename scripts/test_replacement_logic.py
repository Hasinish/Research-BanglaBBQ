import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Let's write the exact replacement logic and inspect before/after for all 48 rows

def replace_family_term(b_text, from_term, to_term):
    # from_term is 'দাদি' or 'দাদা'
    # to_term is 'নানি' or 'নানা'
    # We want to replace whole words or words with inflection like 'দাদিকে' -> 'নানিকে', 'দাদির' -> 'নানির', etc.
    # But let's check what actual forms appear!
    res = b_text
    res = res.replace(f"আমার {from_term}", f"আমার {to_term}")
    res = res.replace(f"আর {from_term}", f"আর {to_term}")
    res = res.replace(f"{from_term} আর", f"{to_term} আর")
    res = res.replace(f"অন্যদিকে {from_term}", f"অন্যদিকে {to_term}")
    res = res.replace(f"{from_term} অসময়ে", f"{to_term} অসময়ে")
    # Exact match for answer choices
    if res == from_term:
        res = to_term
    return res

modified_rows = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    e_full = " ".join(er[5:10])
    
    is_grandma = bool(re.search(r'\bgrandma\b', e_full, re.I))
    is_grandpa = bool(re.search(r'\bgrandpa\b', e_full, re.I))
    
    if not (is_grandma or is_grandpa):
        continue
        
    from_term = 'দাদি' if is_grandma else 'দাদা'
    to_term = 'নানি' if is_grandma else 'নানা'
    
    # Original Bengali
    orig_context = br[5]
    orig_q = br[6]
    orig_ans0 = br[7]
    orig_ans1 = br[8]
    orig_ans2 = br[9]
    
    new_context = replace_family_term(orig_context, from_term, to_term)
    new_q = replace_family_term(orig_q, from_term, to_term)
    new_ans0 = replace_family_term(orig_ans0, from_term, to_term)
    new_ans1 = replace_family_term(orig_ans1, from_term, to_term)
    new_ans2 = replace_family_term(orig_ans2, from_term, to_term)
    
    # Check if there are any un-replaced from_term left in the row
    rem_check = f"{new_context} {new_q} {new_ans0} {new_ans1} {new_ans2}"
    has_leak = from_term in rem_check
    
    modified_rows.append({
        'sheet_row': sheet_row,
        'id': er[14],
        'term': 'grandma' if is_grandma else 'grandpa',
        'from_term': from_term,
        'to_term': to_term,
        'orig_context': orig_context,
        'new_context': new_context,
        'orig_q': orig_q,
        'new_q': new_q,
        'orig_ans': (orig_ans0, orig_ans1, orig_ans2),
        'new_ans': (new_ans0, new_ans1, new_ans2),
        'has_leak': has_leak
    })

print(f"Total modified rows: {len(modified_rows)}")
leaks = [r for r in modified_rows if r['has_leak']]
print(f"Rows with un-replaced terms remaining: {len(leaks)}")
if leaks:
    for l in leaks:
        print(f"Leak in Row {l['sheet_row']}: {l['new_context']}")

# Print before and after for the first 5 and last 5
print("\n--- SAMPLE BEFORE AND AFTER ---")
for r in modified_rows[:3] + modified_rows[-3:]:
    print(f"Row {r['sheet_row']} (ID: {r['id']}, {r['term']} -> {r['to_term']}):")
    print(f"  Orig Context: {r['orig_context']}")
    print(f"  New Context:  {r['new_context']}")
    print(f"  Orig Answers: {r['orig_ans']}")
    print(f"  New Answers:  {r['new_ans']}")
    print()
