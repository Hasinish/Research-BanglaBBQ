import json
import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect local files first
with open("PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl", "r", encoding="utf-8") as f:
    eng_rows = [json.loads(line) for line in f if line.strip()]

with open("BanglaBBQ_BEN/Age.jsonl", "r", encoding="utf-8") as f:
    ben_rows = [json.loads(line) for line in f if line.strip()]

terms = ["grandma", "grandmother", "grandpa", "grandfather"]

matches = []
for i, (er, br) in enumerate(zip(eng_rows, ben_rows)):
    # Check all relevant fields in English: context, question, ans0, ans1, ans2, answer_info
    eng_text = f"{er['context']} {er['question']} {er['ans0']} {er['ans1']} {er['ans2']} {json.dumps(er.get('answer_info', {}))}".lower()
    
    found_terms = [t for t in terms if re.search(r'\b' + t + r'\b', eng_text)]
    if found_terms:
        matches.append((i, er, br, found_terms))

print(f"Total English rows matching grandma/grandmother/grandpa/grandfather: {len(matches)}")

# Group by question_index and found terms
qi_counts = {}
for i, er, br, found in matches:
    qi = er.get('question_index')
    term_str = ", ".join(found)
    key = f"Q{qi}: {term_str}"
    qi_counts[key] = qi_counts.get(key, 0) + 1

for k, v in sorted(qi_counts.items()):
    print(f"  {k} -> {v} rows")

# Sample a few records
print("\nSample records:")
for i, er, br, found in matches[:5]:
    print(f"--- Row idx {i} (id={er.get('id')}, q_idx={er.get('question_index')}, terms={found}) ---")
    print("ENG Context:", er['context'])
    print("ENG Q:", er['question'])
    print("ENG Ans:", (er['ans0'], er['ans1'], er['ans2']))
    print("BEN Context:", br['context'])
    print("BEN Q:", br['question'])
    print("BEN Ans:", (br['ans0'], br['ans1'], br['ans2']))
    print()
