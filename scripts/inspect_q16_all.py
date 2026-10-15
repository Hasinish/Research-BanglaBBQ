import json
import sys
from scan_grandparent_grandchild import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

q16_rows = [(idx+2, er, br) for idx, (er, br) in enumerate(zip(eng_data, ben_data)) if er[1] == '16']
print(f"Total rows in Q16: {len(q16_rows)}")

# Let's inspect unique English contexts and their corresponding Bengali contexts in Q16
pairs = {}
for r_num, er, br in q16_rows:
    e_c = er[5]
    b_c = br[5]
    if e_c not in pairs:
        pairs[e_c] = (b_c, er[7:10], br[7:10])

for ec, (bc, ea, ba) in pairs.items():
    print("ENG Context:", ec[:80])
    print("BEN Context:", bc[:80])
    print("ENG Ans:", ea)
    print("BEN Ans:", ba)
    print("-" * 60)
