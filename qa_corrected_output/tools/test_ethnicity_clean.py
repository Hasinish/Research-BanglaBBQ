import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

for t in [1, 7, 9]: # Themes 2, 8, 10
    amb_b = brows[t * 144]['context']
    dis_b = brows[t * 144 + 1]['context']
    diff_b = dis_b[len(amb_b):]
    
    # clean amb
    clean_amb = re.sub(r'\s+[কখ]\b', '', amb_b)
    # clean diff
    clean_diff = diff_b.replace('ভাড়াটিয়া খ', 'দ্বিতীয় ভাড়াটিয়া').replace('অভিযোগকারী ক', 'প্রথম অভিযোগকারী')
    
    print(f"Theme Q{t+1:02d}:")
    print("  Clean Amb: ", clean_amb[:120])
    print("  Clean Diff:", clean_diff)
