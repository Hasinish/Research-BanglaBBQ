import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

grandma_rows = []
grandpa_rows = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row_num = idx + 2
    e_full = " ".join(er[5:10])
    
    if re.search(r'\bgrandma\b', e_full, re.I):
        grandma_rows.append((sheet_row_num, idx, er, br))
    elif re.search(r'\bgrandpa\b', e_full, re.I):
        grandpa_rows.append((sheet_row_num, idx, er, br))

print(f"Grandma rows: {len(grandma_rows)}, Grandpa rows: {len(grandpa_rows)}")

print("\n=== SAMPLE GRANDMA ROW ===")
r_num, idx, er, br = grandma_rows[0]
print(f"Sheet Row: {r_num} (ID: {er[14]}, example_id: {er[0]})")
print("ENG Context:", er[5])
print("ENG Question:", er[6])
print("ENG Ans0:", er[7], "| Ans1:", er[8], "| Ans2:", er[9])
print("BEN Context:", br[5])
print("BEN Question:", br[6])
print("BEN Ans0:", br[7], "| Ans1:", br[8], "| Ans2:", br[9])

print("\n=== SAMPLE GRANDPA ROW ===")
r_num, idx, er, br = grandpa_rows[0]
print(f"Sheet Row: {r_num} (ID: {er[14]}, example_id: {er[0]})")
print("ENG Context:", er[5])
print("ENG Question:", er[6])
print("ENG Ans0:", er[7], "| Ans1:", er[8], "| Ans2:", er[9])
print("BEN Context:", br[5])
print("BEN Question:", br[6])
print("BEN Ans0:", br[7], "| Ans1:", br[8], "| Ans2:", br[9])
