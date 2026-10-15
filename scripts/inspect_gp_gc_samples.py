import json
import sys
from scan_grandparent_grandchild import gp_matches, gc_matches

sys.stdout.reconfigure(encoding='utf-8')

print("=================== 16 ROWS OF GRANDCHILD IN Q16 ===================")
sample_gc = gc_matches[0]
print(f"Row {sample_gc[0]} (ID: {sample_gc[2]}):")
print("ENG Context:", sample_gc[3][5])
print("ENG Question:", sample_gc[3][6])
print("ENG Ans:", (sample_gc[3][7], sample_gc[3][8], sample_gc[3][9]))
print("ENG Label:", sample_gc[3][10])
print("BEN Context:", sample_gc[4][5])
print("BEN Question:", sample_gc[4][6])
print("BEN Ans:", (sample_gc[4][7], sample_gc[4][8], sample_gc[4][9]))
print("BEN Label:", sample_gc[4][10])

print("\n=================== 16 ROWS OF GRANDPARENT IN Q16 ===================")
sample_gp_q16 = next(r for r in gp_matches if r[1] == '16')
print(f"Row {sample_gp_q16[0]} (ID: {sample_gp_q16[2]}):")
print("ENG Context:", sample_gp_q16[3][5])
print("ENG Question:", sample_gp_q16[3][6])
print("ENG Ans:", (sample_gp_q16[3][7], sample_gp_q16[3][8], sample_gp_q16[3][9]))
print("ENG Label:", sample_gp_q16[3][10])
print("BEN Context:", sample_gp_q16[4][5])
print("BEN Question:", sample_gp_q16[4][6])
print("BEN Ans:", (sample_gp_q16[4][7], sample_gp_q16[4][8], sample_gp_q16[4][9]))
print("BEN Label:", sample_gp_q16[4][10])

print("\n=================== 24 ROWS OF GRANDPARENT IN Q18 ===================")
sample_gp_q18 = next(r for r in gp_matches if r[1] == '18')
print(f"Row {sample_gp_q18[0]} (ID: {sample_gp_q18[2]}):")
print("ENG Context:", sample_gp_q18[3][5])
print("ENG Question:", sample_gp_q18[3][6])
print("ENG Ans:", (sample_gp_q18[3][7], sample_gp_q18[3][8], sample_gp_q18[3][9]))
print("ENG Label:", sample_gp_q18[3][10])
print("BEN Context:", sample_gp_q18[4][5])
print("BEN Question:", sample_gp_q18[4][6])
print("BEN Ans:", (sample_gp_q18[4][7], sample_gp_q18[4][8], sample_gp_q18[4][9]))
print("BEN Label:", sample_gp_q18[4][10])
