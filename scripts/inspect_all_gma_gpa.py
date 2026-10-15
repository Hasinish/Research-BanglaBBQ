import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

grandma_records = []
grandpa_records = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row_num = idx + 2
    e_full = " ".join(er[5:10])
    
    if re.search(r'\bgrandma\b', e_full, re.I):
        grandma_records.append((sheet_row_num, idx, er, br))
    elif re.search(r'\bgrandpa\b', e_full, re.I):
        grandpa_records.append((sheet_row_num, idx, er, br))

print(f"Grandma count: {len(grandma_records)}")
print("Grandma Sheet Row numbers:", [r[0] for r in grandma_records])
print("Grandma IDs:", [r[2][14] for r in grandma_records])

print(f"\nGrandpa count: {len(grandpa_records)}")
print("Grandpa Sheet Row numbers:", [r[0] for r in grandpa_records])
print("Grandpa IDs:", [r[2][14] for r in grandpa_records])

# Check all unique contexts in Grandma
gma_contexts = set(r[3][5] for r in grandma_records)
print(f"\nGrandma Bengali unique contexts ({len(gma_contexts)}):")
for c in gma_contexts:
    print(" ", c)

# Check all unique contexts in Grandpa
gpa_contexts = set(r[3][5] for r in grandpa_records)
print(f"\nGrandpa Bengali unique contexts ({len(gpa_contexts)}):")
for c in gpa_contexts:
    print(" ", c)

# Check all unique answers in Grandma
gma_answers = set(a for r in grandma_records for a in r[3][7:10])
print(f"\nGrandma Bengali unique answers: {gma_answers}")

# Check all unique answers in Grandpa
gpa_answers = set(a for r in grandpa_records for a in r[3][7:10])
print(f"\nGrandpa Bengali unique answers: {gpa_answers}")

# Check questions
gma_questions = set(r[3][6] for r in grandma_records)
print(f"\nGrandma Bengali unique questions: {gma_questions}")
gpa_questions = set(r[3][6] for r in grandpa_records)
print(f"\nGrandpa Bengali unique questions: {gpa_questions}")
