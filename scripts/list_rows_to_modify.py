import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the 48 rows of Q2:
rows_to_modify = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    e_full = " ".join(er[5:10])
    
    is_grandma = bool(re.search(r'\bgrandma\b', e_full, re.I))
    is_grandpa = bool(re.search(r'\bgrandpa\b', e_full, re.I))
    
    if is_grandma or is_grandpa:
        rows_to_modify.append({
            'sheet_row': sheet_row,
            'idx': idx,
            'id': er[14],
            'example_id': er[0],
            'term': 'grandma' if is_grandma else 'grandpa',
            'target_bn': 'নানি' if is_grandma else 'নানা',
            'current_bn': 'দাদি' if is_grandma else 'দাদা',
            'er': er,
            'br': br
        })

print(f"Total rows to modify: {len(rows_to_modify)}")
print("\nList of rows to modify:")
for r in rows_to_modify:
    print(f"Row {r['sheet_row']:4d} | ID: {r['id']:>4s} | Term: {r['term']:<8s} -> {r['target_bn']} | Ans0: {r['br'][7]} | Ans1: {r['br'][8]} | Ans2: {r['br'][9]}")
