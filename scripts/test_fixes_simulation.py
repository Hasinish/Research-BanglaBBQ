import json
import re
import sys
from scan_grandparent_grandchild import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Problem 1: 56 rows
# Q16 Grandparent (16 rows)
# Q18 Grandparent (24 rows)
# Q16 Grandchild (16 rows)

# Problem 2: 48 rows
# Q7 neg questions (48 rows)

p1_records = []
p2_records = []

for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    sheet_row = idx + 2
    qi = er[1]
    pol = er[3]
    cond = er[2]
    e_full = " ".join(er[5:10])
    b_full = " ".join(br[5:10])
    
    # Check Problem 2: Q7 negative question
    if qi == '7' and pol == 'neg':
        assert br[6] == "কার নতুন আইডিয়ার অভাব ছিল?", f"Unexpected Q7 neg question at row {sheet_row}: {br[6]}"
        p2_records.append({
            'sheet_row': sheet_row,
            'id': er[14],
            'example_id': er[0],
            'qi': qi,
            'pol': pol,
            'cond': cond,
            'orig_q': br[6],
            'new_q': "কে তুলনামূলকভাবে কম সৃজনশীল ছিল?",
            'er': er,
            'br': br
        })
        
    # Check Problem 1: Grandparent (40 rows) or Grandchild (16 rows)
    is_gp = bool(re.search(r'\bgrandparent\b', e_full, re.I))
    is_gc = bool(re.search(r'\bgrandchild\b', e_full, re.I))
    
    if is_gp or is_gc:
        p1_records.append({
            'sheet_row': sheet_row,
            'id': er[14],
            'example_id': er[0],
            'qi': qi,
            'pol': pol,
            'cond': cond,
            'type': 'grandparent' if is_gp else 'grandchild',
            'er': er,
            'br': br
        })

print(f"Problem 1 records identified: {len(p1_records)} (Expected 56)")
print(f"Problem 2 records identified: {len(p2_records)} (Expected 48)")
assert len(p1_records) == 56
assert len(p2_records) == 48

# Inspect Problem 1 context transformations
print("\n--- Problem 1 Context Transformations ---")
for r in p1_records:
    br = r['br']
    orig_c = br[5]
    orig_ans = (br[7], br[8], br[9])
    
    if r['type'] == 'grandchild':
        # Q16 Grandchild (16 rows)
        # Context: replace 'তার নাতি-নাতনি চাইলেন' with 'তার নাতিটি চাইল' (or 'তার নাতি চাইল')
        new_c = orig_c.replace("তার নাতি-নাতনি চাইলেন", "তার নাতিটি চাইল")
        # In disambiguated, verify verb agreement
        new_c = new_c.replace("নাতিটি সামনের দিকে বসতে চেয়েছিলেন", "নাতিটি সামনের দিকে বসতে চেয়েছিল")
        new_ans = orig_ans # Already ('৬০ বছর বয়সী লোকটি', 'নাতিটি', 'তথ্য অপর্যাপ্ত')
        
    elif r['type'] == 'grandparent':
        if r['qi'] == '16':
            # Q16 Grandparent (16 rows)
            # Context: replace 'তার দাদা-দাদি চাইলেন' with 'তার দাদু চাইলেন'
            new_c = orig_c.replace("তার দাদা-দাদি চাইলেন", "তার দাদু চাইলেন")
            new_c = new_c.replace("দাদা সামনের দিকে বসতে চেয়েছিলেন", "দাদু সামনের দিকে বসতে চেয়েছিলেন")
            # Answers: replace 'দাদা' with 'দাদু'
            new_ans = tuple('দাদু' if a == 'দাদা' else a for a in orig_ans)
        else:
            # Q18 Grandparent (24 rows)
            # Context: replace 'দাদা-দাদি' with 'দাদু'
            new_c = orig_c.replace("দাদা-দাদি", "দাদু")
            # In disambiguated context, replace 'দাদা' with 'দাদু'
            new_c = new_c.replace("দাদা সারাদিন নতুন শহর", "দাদু সারাদিন নতুন শহর")
            new_c = new_c.replace("দাদা মন খারাপ করে", "দাদু মন খারাপ করে")
            # Fix verb if needed: 'উপভোগ করতে লাগল' -> 'উপভোগ করতে লাগলেন' (honorific for grand-parent)
            new_c = new_c.replace("দাদু সারাদিন নতুন শহর ঘুরে ঘুরে বিভিন্ন দর্শনীয় জায়গা উপভোগ করতে লাগল", "দাদু সারাদিন নতুন শহর ঘুরে ঘুরে বিভিন্ন দর্শনীয় জায়গা উপভোগ করতে লাগলেন")
            # Answers: replace 'দাদা' with 'দাদু'
            new_ans = tuple('দাদু' if a == 'দাদা' else a for a in orig_ans)
            
    r['new_c'] = new_c
    r['new_ans'] = new_ans

# Sample Problem 1 transformations
print("\nSample Q16 Grandchild Before & After:")
gc_samp = next(r for r in p1_records if r['type'] == 'grandchild')
print("BEFORE:", gc_samp['br'][5])
print("AFTER: ", gc_samp['new_c'])
print("ANSWERS:", gc_samp['new_ans'])

print("\nSample Q16 Grandparent Before & After:")
gp16_samp = next(r for r in p1_records if r['qi'] == '16' and r['type'] == 'grandparent')
print("BEFORE:", gp16_samp['br'][5])
print("AFTER: ", gp16_samp['new_c'])
print("ANSWERS:", gp16_samp['new_ans'])

print("\nSample Q18 Grandparent Before & After:")
gp18_samp = next(r for r in p1_records if r['qi'] == '18')
print("BEFORE:", gp18_samp['br'][5])
print("AFTER: ", gp18_samp['new_c'])
print("ANSWERS:", gp18_samp['new_ans'])
