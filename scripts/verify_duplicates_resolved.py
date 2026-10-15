import json
import sys
from test_replacement_logic import modified_rows
from scan_family_terms_sheets import ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Create a copy of ben_data with the modifications applied
mod_dict = {r['sheet_row'] - 2: r for r in modified_rows}

new_ben_data = []
for idx, br in enumerate(ben_data):
    if idx in mod_dict:
        m = mod_dict[idx]
        new_row = list(br)
        new_row[5] = m['new_context']
        new_row[6] = m['new_q']
        new_row[7] = m['new_ans'][0]
        new_row[8] = m['new_ans'][1]
        new_row[9] = m['new_ans'][2]
        new_ben_data.append(new_row)
    else:
        new_ben_data.append(br)

# Check duplicates across the entire dataset now
seen = {}
new_duplicates = []

for idx, r in enumerate(new_ben_data):
    sheet_row = idx + 2
    sig = (r[1], r[2], r[3], r[5], r[6], r[7], r[8], r[9], r[10])
    if sig in seen:
        new_duplicates.append((seen[sig], sheet_row, r[1], r[14]))
    else:
        seen[sig] = sheet_row

q2_dups_after = [d for d in new_duplicates if d[2] == '2']
print(f"\n================ DUPLICATE AUDIT ================")
print(f"Duplicates in Q2 BEFORE fix: 8")
print(f"Duplicates in Q2 AFTER fix:  {len(q2_dups_after)}")
print(f"Total duplicates across entire dataset BEFORE: 76")
print(f"Total duplicates across entire dataset AFTER:  {len(new_duplicates)}")

# Verify all other remaining duplicates: which question indices do they belong to?
other_dups_by_q = {}
for d in new_duplicates:
    other_dups_by_q[d[2]] = other_dups_by_q.get(d[2], 0) + 1

print("\nRemaining duplicates by question index (completely unrelated templates):")
for q, cnt in sorted(other_dups_by_q.items(), key=lambda x: int(x[0])):
    print(f"  Template Q{q:>2}: {cnt} duplicate pairs")
