import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl', 'r', encoding='utf-8') as f:
    eng = [json.loads(line) for line in f]
from pathlib import Path
ben_path = Path('BanglaBBQ_Age/banglabbq_age_bengali.jsonl') if Path('BanglaBBQ_Age/banglabbq_age_bengali.jsonl').exists() else Path('BanglaBBQ_BEN_New/Age.jsonl')
with open(ben_path, 'r', encoding='utf-8') as f:
    ben = [json.loads(line) for line in f]

print("=" * 80)
print("AUDITING CULTURAL LOCALIZATION IN THEMES Q13-Q20 (IDs 1872-2919)")
print("=" * 80)

# Check themes Q13 to Q20
for q in range(13, 21):
    q_str = str(q)
    e_rows = [r for r in eng if r['question_index'] == q_str]
    b_rows = [r for r in ben if r['question_index'] == q_str]
    
    start_id = e_rows[0]['example_id']
    end_id = e_rows[-1]['example_id']
    
    print(f"\n--- THEME Q{q} (IDs {start_id}-{end_id}) ---")
    sample_e = e_rows[0]
    sample_b = b_rows[0]
    print(f"Sample ENG context: {sample_e['context'][:150]}...")
    print(f"Sample BEN context: {sample_b['context'][:150]}...")
    
    # Check for specific Pakistani or regional entities
    pk_terms = ['Imtiaz', 'Indrive', 'Jalal Sons', 'Lahore', 'Karachi', 'Chai Dhaba', 'qawwali', 'mehfil', 'chowk']
    found_terms = []
    for t in pk_terms:
        if any(t.lower() in r['context'].lower() for r in e_rows):
            found_terms.append(t)
    print(f"Identified Pakistani entities/cultural terms in Q{q}: {found_terms}")
