import json
import sys
from scan_grandparent_grandchild import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

q7_rows = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    if er[1] == '7':
        q7_rows.append((sheet_row, er[14], er, br))

print(f"Total rows in Template Q7: {len(q7_rows)}")

# Check question polarities in Q7
q7_neg = [r for r in q7_rows if r[2][3] == 'neg']
q7_nonneg = [r for r in q7_rows if r[2][3] == 'nonneg']

print(f"Q7 'neg' rows: {len(q7_neg)}")
print(f"Q7 'nonneg' rows: {len(q7_nonneg)}")

# Check English questions in Q7 neg
eng_neg_questions = set(r[2][6] for r in q7_neg)
print(f"English Q7 neg questions: {eng_neg_questions}")

# Check current Bengali questions in Q7 neg
ben_neg_questions = set(r[3][6] for r in q7_neg)
print(f"Bengali Q7 neg questions: {ben_neg_questions}")

# Check English and Bengali questions in Q7 nonneg (should not be touched!)
eng_nonneg_questions = set(r[2][6] for r in q7_nonneg)
ben_nonneg_questions = set(r[3][6] for r in q7_nonneg)
print(f"English Q7 nonneg questions: {eng_nonneg_questions}")
print(f"Bengali Q7 nonneg questions: {ben_nonneg_questions}")
