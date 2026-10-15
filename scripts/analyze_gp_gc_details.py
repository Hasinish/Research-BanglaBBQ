import json
import sys
from scan_grandparent_grandchild import gp_matches, gc_matches

sys.stdout.reconfigure(encoding='utf-8')

print("=== Q16 GRANDCHILD (16 rows) ===")
q16_gc = gc_matches
for r in q16_gc:
    print(f"Row {r[0]:4d} | ID: {r[2]:>4s} | ENG Context: {r[3][5][:60]}... | BEN Ans: {r[4][7:10]}")

print("\nUnique Contexts in Q16 Grandchild:")
for c in set(r[4][5] for r in q16_gc):
    print(" ", c)

print("\nUnique Answers in Q16 Grandchild:")
print(set(a for r in q16_gc for a in r[4][7:10]))

print("\n" + "="*80)
print("=== Q16 GRANDPARENT (16 rows) ===")
q16_gp = [r for r in gp_matches if r[1] == '16']
for r in q16_gp:
    print(f"Row {r[0]:4d} | ID: {r[2]:>4s} | ENG Context: {r[3][5][:60]}... | BEN Ans: {r[4][7:10]}")

print("\nUnique Contexts in Q16 Grandparent:")
for c in set(r[4][5] for r in q16_gp):
    print(" ", c)

print("\nUnique Answers in Q16 Grandparent:")
print(set(a for r in q16_gp for a in r[4][7:10]))

print("\n" + "="*80)
print("=== Q18 GRANDPARENT (24 rows) ===")
q18_gp = [r for r in gp_matches if r[1] == '18']
for r in q18_gp:
    print(f"Row {r[0]:4d} | ID: {r[2]:>4s} | ENG Context: {r[3][5][:60]}... | BEN Ans: {r[4][7:10]}")

print("\nUnique Contexts in Q18 Grandparent:")
for c in set(r[4][5] for r in q18_gp):
    print(" ", c)

print("\nUnique Answers in Q18 Grandparent:")
print(set(a for r in q18_gp for a in r[4][7:10]))
