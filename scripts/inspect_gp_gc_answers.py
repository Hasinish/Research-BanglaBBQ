import json
import sys
from scan_grandparent_grandchild import gp_matches, gc_matches

sys.stdout.reconfigure(encoding='utf-8')

print("=== Q16 GRANDCHILD ANSWERS ===")
for r in gc_matches:
    print(f"Row {r[0]}: {r[4][7:10]} | Gold label: {r[4][10]}")

print("\n=== Q16 GRANDPARENT ANSWERS ===")
for r in gp_matches:
    if r[1] == '16':
        print(f"Row {r[0]}: {r[4][7:10]} | Gold label: {r[4][10]}")

print("\n=== Q18 GRANDPARENT ANSWERS ===")
for r in gp_matches:
    if r[1] == '18':
        print(f"Row {r[0]}: {r[4][7:10]} | Gold label: {r[4][10]}")
