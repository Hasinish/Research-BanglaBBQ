import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# The mapping:
# Grandma -> নানি
# Grandmother -> দাদি
# Grandpa -> নানা
# Grandfather -> দাদা

# Let's inspect each template: Q2, Q13, Q14, Q16, Q18
# For each template, what English terms appear, and where do they appear (context, question, answers)?

regex_terms = re.compile(r'\b(grandma|grandmother|grandpa|grandfather)\b', re.IGNORECASE)

records_to_check = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row_num = idx + 2
    
    # Check context, question, ans0, ans1, ans2
    e_context, e_question, e_ans0, e_ans1, e_ans2 = er[5], er[6], er[7], er[8], er[9]
    b_context, b_question, b_ans0, b_ans1, b_ans2 = br[5], br[6], br[7], br[8], br[9]
    
    # Check which term is present in this row
    e_full = f"{e_context} {e_question} {e_ans0} {e_ans1} {e_ans2}"
    matches = regex_terms.findall(e_full)
    if matches:
        # Normalize term to lowercase
        unique_matches = set(m.lower() for m in matches)
        records_to_check.append({
            'row_num': sheet_row_num,
            'id': er[14],
            'q_idx': er[1],
            'cond': er[2],
            'pol': er[3],
            'terms': unique_matches,
            'er': er,
            'br': br
        })

print(f"Total matching records: {len(records_to_check)}")

# Check if any row has multiple different terms (e.g. grandma AND grandfather)
mixed = [r for r in records_to_check if len(r['terms']) > 1]
print(f"Rows with multiple terms: {len(mixed)}")
if mixed:
    for m in mixed[:5]:
        print(f"  Row {m['row_num']}: terms={m['terms']}")

# Now let's see for each term (grandma, grandmother, grandpa, grandfather), what Bengali words are currently used!
term_stats = {'grandma': [], 'grandmother': [], 'grandpa': [], 'grandfather': []}
for r in records_to_check:
    for t in r['terms']:
        term_stats[t].append(r)

for t, rows in term_stats.items():
    print(f"\nTerm: '{t}' (appears in {len(rows)} rows)")
    # Check what words appear in Bengali context and answers for these rows
    b_words_context = set()
    b_words_answers = set()
    for item in rows:
        br = item['br']
        for w in ['দাদা', 'দাদি', 'নানা', 'নানি', 'দাদাকে', 'দাদিকে', 'নানাকে', 'নানিকে', 'দাদার', 'দাদির', 'নানুর', 'দাদুর']:
            if w in br[5]: b_words_context.add(w)
            for a in br[7:10]:
                if w in a: b_words_answers.add(w)
    print(f"  Bengali context words found: {b_words_context}")
    print(f"  Bengali answer words found: {b_words_answers}")
