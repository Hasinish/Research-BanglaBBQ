import json
import sys
from scan_family_terms_sheets import ben_data

sys.stdout.reconfigure(encoding='utf-8')

# A duplicate record in BBQ is typically defined as having identical:
# (context, question, ans0, ans1, ans2, label)
seen = {}
duplicates = []

for idx, r in enumerate(ben_data):
    sheet_row = idx + 2
    # signature
    sig = (r[1], r[2], r[3], r[5], r[6], r[7], r[8], r[9], r[10]) # q_idx, cond, pol, context, question, ans0, ans1, ans2, label
    if sig in seen:
        duplicates.append((seen[sig], sheet_row, r[1], r[14]))
    else:
        seen[sig] = sheet_row

print(f"Total duplicate records in BanglaBBQ_BEN_Age: {len(duplicates)}")
print("\nSample duplicates found:")
for original_row, dup_row, qi, rid in duplicates[:15]:
    print(f"  Duplicate of Row {original_row} at Row {dup_row} (Q_idx: {qi}, ID: {rid})")
