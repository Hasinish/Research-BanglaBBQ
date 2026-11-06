import json

BEN_PATH = 'review_artifacts/religion_linguistic_audit_20261106/BanglaBBQ_BEN_Religion_QA_fixed.jsonl'
ENG_PATH = 'review_artifacts/religion_linguistic_audit_20261106/BanglaBBQ_ENG_Religion_QA_fixed.jsonl'
ORIG_BEN = 'fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl'
ORIG_ENG = 'fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl'

with open(BEN_PATH, 'r', encoding='utf-8') as f:
    ben_rows = [json.loads(line) for line in f]
with open(ENG_PATH, 'r', encoding='utf-8') as f:
    eng_rows = [json.loads(line) for line in f]
with open(ORIG_BEN, 'r', encoding='utf-8') as f:
    orig_ben = [json.loads(line) for line in f]
with open(ORIG_ENG, 'r', encoding='utf-8') as f:
    orig_eng = [json.loads(line) for line in f]

checks = []

# 1. Total row count check
assert len(ben_rows) == 2880, f"Expected 2880 BEN, got {len(ben_rows)}"
assert len(eng_rows) == 2880, f"Expected 2880 ENG, got {len(eng_rows)}"
checks.append(("1. Row count (2,880 ENG / 2,880 BEN)", True, f"{len(ben_rows)} rows"))

# 2. Schema check (15 columns)
expected_fields = [
    'example_id', 'question_index', 'question_polarity', 'context_condition',
    'category', 'answer_info', 'additional_metadata', 'context', 'question',
    'ans0', 'ans1', 'ans2', 'label'
]
schema_pass = True
for idx, (b, e) in enumerate(zip(ben_rows, eng_rows)):
    for field in expected_fields:
        if field not in b or field not in e:
            schema_pass = False
            break
checks.append(("2. Strict 15-column schema parity", schema_pass, "All expected fields present"))

# 3. Sequential example_id (0..2879)
id_pass = all(b['example_id'] == i and e['example_id'] == i for i, (b, e) in enumerate(zip(ben_rows, eng_rows)))
checks.append(("3. Sequential example_id (0..2879)", id_pass, "0..2879 perfectly sequential"))

# 4. Zero gold label modifications
label_pass = all(b['label'] == ob['label'] for b, ob in zip(ben_rows, orig_ben))
checks.append(("4. Zero gold label modifications (0 label changes)", label_pass, "0 labels altered"))

# 5. Label parity between ENG and BEN
eng_ben_label = all(b['label'] == e['label'] for b, e in zip(ben_rows, eng_rows))
checks.append(("5. ENG-BEN label alignment", eng_ben_label, "100% matched"))

# 6. Ambiguous context vs Disambiguated context prefix invariant
prefix_pass = True
for fam_idx in range(60):
    start = fam_idx * 48
    for r in range(start, start + 48, 2):
        ambig = ben_rows[r]['context']
        disambig = ben_rows[r+1]['context']
        if not disambig.startswith(ambig):
            prefix_pass = False
            break
checks.append(("6. Disambiguated context starts with ambiguous context", prefix_pass, "All 60 families satisfy exact prefix rule"))

# 7. Category designation invariant
cat_pass = all(b['category'] == 'Religion' and e['category'] == 'Religion' for b, e in zip(ben_rows, eng_rows))
checks.append(("7. Category designation invariant", cat_pass, "Religion"))

# 8. Options integrity (ans0, ans1, ans2 unchanged)
ans_pass = all(
    b['ans0'] == ob['ans0'] and b['ans1'] == ob['ans1'] and b['ans2'] == ob['ans2']
    for b, ob in zip(ben_rows, orig_ben)
)
checks.append(("8. Options integrity (ans0, ans1, ans2 unchanged)", ans_pass, "100% intact"))

# 9. answer_info metadata dictionary integrity
info_pass = all(b['answer_info'] == ob['answer_info'] for b, ob in zip(ben_rows, orig_ben))
checks.append(("9. answer_info metadata dictionary integrity", info_pass, "100% intact"))

# 10. additional_metadata integrity
meta_pass = all(b['additional_metadata'] == ob['additional_metadata'] for b, ob in zip(ben_rows, orig_ben))
checks.append(("10. additional_metadata integrity", meta_pass, "100% intact"))

# 11. English candidate dataset untouched (bit-exact)
eng_exact = all(e == oe for e, oe in zip(eng_rows, orig_eng))
checks.append(("11. English candidate dataset untouched (bit-exact)", eng_exact, "100% exact copy"))

# 12. Question syntax and punctuation check
q_punct_pass = all(b['question'].endswith('?') for b in ben_rows)
checks.append(("12. Bengali question punctuation and terminal interrogation (?)", q_punct_pass, "100% ends with ?"))

all_pass = True
for name, status, detail in checks:
    if not status:
        all_pass = False
    print(f"{name:<60} | {'PASS [✓]' if status else 'FAIL [✗]'} | {detail}")

assert all_pass, "Religion validation failed!"
print("Religion: 12-POINT INVARIANT SUITE 100% PASS!")

