import json

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    eng_sample = json.loads(f.readline())

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "r", encoding="utf-8") as f:
    ben_sample = json.loads(f.readline())

print("ENG keys:", list(eng_sample.keys()))
print("BEN keys:", list(ben_sample.keys()))

# Check Tab 1 / Tab 2 column order from Age
# In Age:
# 0: example_id
# 1: question_index
# 2: context_condition
# 3: question_polarity
# 4: type
# 5: context
# 6: question
# 7: ans0
# 8: ans1
# 9: ans2
# 10: label
# 11: answer_info
# 12: additional_metadata
# 13: category
# 14: id

expected_cols = [
    'example_id', 'question_index', 'context_condition', 'question_polarity', 'type',
    'context', 'question', 'ans0', 'ans1', 'ans2',
    'label', 'answer_info', 'additional_metadata', 'category', 'id'
]

print("\nMissing in ENG:", [c for c in expected_cols if c not in eng_sample])
print("Missing in BEN:", [c for c in expected_cols if c not in ben_sample])
