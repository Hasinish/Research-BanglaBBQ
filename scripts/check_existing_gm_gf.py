import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Check if ANY row with grandmother or grandfather has 'নানি' or 'নানা'
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row_num = idx + 2
    e_full = " ".join(er[5:10]).lower()
    b_full = " ".join(br[5:10])
    
    # Check grandmother
    if re.search(r'\bgrandmother\b', e_full):
        if 'নানি' in b_full or 'নানুর' in b_full:
            print(f"Row {sheet_row_num}: English has grandmother, but Bengali has nani! {b_full}")
            
    # Check grandfather
    if re.search(r'\bgrandfather\b', e_full):
        if 'নানা' in b_full or 'নানুর' in b_full:
            print(f"Row {sheet_row_num}: English has grandfather, but Bengali has nana! {b_full}")

print("Check finished.")
