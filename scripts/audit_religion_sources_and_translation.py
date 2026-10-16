import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('BanglaBBQ_Religion/Religion_eng.jsonl', 'r', encoding='utf-8') as f:
    eng_recs = [json.loads(line) for line in f]
with open('BanglaBBQ_Religion/Religion_bng.jsonl', 'r', encoding='utf-8') as f:
    ben_recs = [json.loads(line) for line in f]

themes = {}
for e, b in zip(eng_recs, ben_recs):
    qi = e['question_index']
    if qi not in themes:
        meta = e['additional_metadata']
        themes[qi] = {
            'qi': qi,
            'source': meta.get('source'),
            'stereotyped_groups': meta.get('stereotyped_groups'),
            'subcategory': meta.get('subcategory'),
            'eng_context': e['context'],
            'eng_question': e['question'],
            'ben_context': b['context'],
            'ben_question': b['question'],
            'ans0_e': e['ans0'],
            'ans1_e': e['ans1'],
            'ans0_b': b['ans0'],
            'ans1_b': b['ans1'],
            'answer_info': e['answer_info']
        }

print(f"Total Unique Themes: {len(themes)}")
print("=" * 100)
for qi in sorted(themes.keys()):
    t = themes[qi]
    print(f"Q{qi:02d} | Groups: {str(t['stereotyped_groups']):<15} | Question: {t['eng_question']}")
    print(f"     Source: {t['source']}")
print("=" * 100)

