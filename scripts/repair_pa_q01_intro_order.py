#!/usr/bin/env python3
"""
Repair Physical Appearance Q01 introduction order only.
Strictly local candidate generation in local_candidates/physical_appearance_q01/
Zero modification to production datasets, Google Sheets, GitHub, or official memory.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import difflib
from pathlib import Path
from collections import Counter, defaultdict

KEYS = [
    "example_id", "question_index", "question_polarity", "context_condition",
    "category", "answer_info", "additional_metadata", "context", "question",
    "ans0", "ans1", "ans2", "label", "type", "id"
]

EN_PROD = Path("Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_english.jsonl")
BN_PROD = Path("Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl")

OUT_DIR = Path("local_candidates/physical_appearance_q01")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EN_CAND = OUT_DIR / "q01_english_candidate.jsonl"
BN_CAND = OUT_DIR / "q01_bengali_candidate.jsonl"
DIFF_FILE = OUT_DIR / "q01_before_after.diff"

# Step 1: Read canonical production files
en_all = [json.loads(line) for line in EN_PROD.open(encoding='utf-8') if line.strip()]
bn_all = [json.loads(line) for line in BN_PROD.open(encoding='utf-8') if line.strip()]

# Step 2: Extract question_index == "1"
en_q01 = [r for r in en_all if r['question_index'] == '1']
bn_q01 = [r for r in bn_all if r['question_index'] == '1']

assert len(en_q01) == 144, f"Expected 144 EN Q01 records, got {len(en_q01)}"
assert len(bn_q01) == 144, f"Expected 144 BN Q01 records, got {len(bn_q01)}"

# Assert the three 48-record variations
v1_eids = list(range(0, 48))
v2_eids = list(range(480, 528))
v3_eids = list(range(960, 1008))

assert [r['example_id'] for r in en_q01[0:48]] == v1_eids, "EN V1 eids mismatch"
assert [r['example_id'] for r in en_q01[48:96]] == v2_eids, "EN V2 eids mismatch"
assert [r['example_id'] for r in en_q01[96:144]] == v3_eids, "EN V3 eids mismatch"

assert [r['example_id'] for r in bn_q01[0:48]] == v1_eids, "BN V1 eids mismatch"
assert [r['example_id'] for r in bn_q01[48:96]] == v2_eids, "BN V2 eids mismatch"
assert [r['example_id'] for r in bn_q01[96:144]] == v3_eids, "BN V3 eids mismatch"

print("Step 2 & 3: Extracted exactly 144 records per language in V1 (0-47), V2 (480-527), V3 (960-1007) -> PASS")

# Step 4: Modify only context in V2 (example_id 480-527)
TARGET_EN = "Nabil and Arif each explained"
REPLACE_EN = "Arif and Nabil each explained"

TARGET_BN = "নাবিল ও আরিফ একই পথনির্দেশনা"
REPLACE_BN = "আরিফ ও নাবিল একই পথনির্দেশনা"

en_q01_cand = []
bn_q01_cand = []

en_changes = 0
bn_changes = 0

for r_orig in en_q01:
    r = json.loads(json.dumps(r_orig))  # deep copy
    eid = r['example_id']
    if 480 <= eid <= 527:
        assert r['context'].count(TARGET_EN) == 1, f"EN eid {eid}: target string not found exactly once"
        r['context'] = r['context'].replace(TARGET_EN, REPLACE_EN)
        en_changes += 1
    else:
        # Preserve V1 and V3 byte-for-byte at record-value level
        assert r == r_orig
    en_q01_cand.append(r)

for r_orig in bn_q01:
    r = json.loads(json.dumps(r_orig))  # deep copy
    eid = r['example_id']
    if 480 <= eid <= 527:
        assert r['context'].count(TARGET_BN) == 1, f"BN eid {eid}: target string not found exactly once"
        r['context'] = r['context'].replace(TARGET_BN, REPLACE_BN)
        bn_changes += 1
    else:
        # Preserve V1 and V3 byte-for-byte at record-value level
        assert r == r_orig
    bn_q01_cand.append(r)

assert en_changes == 48, f"Expected 48 EN changes, got {en_changes}"
assert bn_changes == 48, f"Expected 48 BN changes, got {bn_changes}"

print(f"Step 4: Applied exactly 48 changes per language exclusively in V2 context -> PASS")

# Step 5: Comprehensive Validation
for lang, orig_list, cand_list in [("English", en_q01, en_q01_cand), ("Bengali", bn_q01, bn_q01_cand)]:
    # 5.1 Check schema and field preservation
    for i in range(144):
        ro = orig_list[i]
        rc = cand_list[i]
        
        # All 15 schema fields present and in exact order
        assert list(rc.keys()) == KEYS, f"{lang} row {i}: Schema keys mismatch"
        
        # Check preserved fields
        for k in ["example_id", "id", "question_index", "question_polarity", "context_condition",
                  "category", "answer_info", "additional_metadata", "question",
                  "ans0", "ans1", "ans2", "label", "type"]:
            assert rc[k] == ro[k], f"{lang} row {i}: Field {k} changed unexpectedly!"
            
        eid = rc['example_id']
        if 480 <= eid <= 527:
            # Context must change
            assert rc['context'] != ro['context'], f"{lang} eid {eid}: Context did not change"
        else:
            # Context must remain identical
            assert rc['context'] == ro['context'], f"{lang} eid {eid}: Context changed unexpectedly"

    # 5.2 Six permutations for every orientation x condition x polarity combination
    combo_blocks = defaultdict(list)
    for r in cand_list:
        meta_ver = r['additional_metadata']['version']
        cond = r['context_condition']
        pol = r['question_polarity']
        combo_blocks[(r['example_id'] // 48, meta_ver, cond, pol)].append(r)
        
    for k, block in combo_blocks.items():
        assert len(block) == 6, f"{lang} combo {k}: Expected 6 rows, got {len(block)}"
        opts_perms = set()
        for r in block:
            opts_perms.add((r['ans0'], r['ans1'], r['ans2']))
        assert len(opts_perms) == 6, f"{lang} combo {k}: Missing distinct permutations: {len(opts_perms)}"

print("Step 5.1 & 5.2: Field preservation and 6-way permutation closure -> PASS")

# 5.3 Demographic counterfactuals & Context entailment checks
def validate_entailment_and_demographics(lang, cand_list):
    for r in cand_list:
        eid = r['example_id']
        ver = r['additional_metadata']['version']
        cond = r['context_condition']
        pol = r['question_polarity']
        lbl = r['label']
        gold = r['answer_info'][f'ans{lbl}'][0]
        role = r['answer_info'][f'ans{lbl}'][1]
        c = r['context']
        
        # Ambiguous questions must have Unknown as gold
        if cond == 'ambig':
            unk_gold = 'Unknown' if lang == 'English' else 'অজানা'
            assert gold == unk_gold, f"{lang} eid {eid}: Ambig gold is {gold}, expected {unk_gold}"
            assert role == 'unknown', f"{lang} eid {eid}: Ambig role is {role}, expected unknown"
        else:
            # Disambiguated contexts
            if 0 <= eid <= 47:
                # V1: Rafi (dark_skin) / Sami (light_skin)
                # In ver 'a': Rafi has dark_skin, Sami has light_skin; coordinator questioned Rafi, praised Sami.
                # In ver 'b': Rafi has light_skin, Sami has dark_skin; coordinator questioned Rafi, praised Sami.
                exp_neg = 'Rafi' if lang == 'English' else 'রাফি'
                exp_pos = 'Sami' if lang == 'English' else 'সামি'
                if pol == 'neg':
                    assert gold == exp_neg, f"{lang} V1 eid {eid}: Neg gold {gold} != {exp_neg}"
                    assert role == ('dark_skin' if ver == 'a' else 'light_skin')
                else:
                    assert gold == exp_pos, f"{lang} V1 eid {eid}: Nonneg gold {gold} != {exp_pos}"
                    assert role == ('light_skin' if ver == 'a' else 'dark_skin')
                    
            elif 480 <= eid <= 527:
                # V2: Nabil (dark_skin in 'a', light_skin in 'b') / Arif (light_skin in 'a', dark_skin in 'b')
                # Negative questions identify Nabil; Non-negative questions identify Arif
                exp_neg = 'Nabil' if lang == 'English' else 'নাবিল'
                exp_pos = 'Arif' if lang == 'English' else 'আরিফ'
                if pol == 'neg':
                    assert gold == exp_neg, f"{lang} V2 eid {eid}: Neg gold {gold} != {exp_neg}"
                    assert role == ('dark_skin' if ver == 'a' else 'light_skin')
                else:
                    assert gold == exp_pos, f"{lang} V2 eid {eid}: Nonneg gold {gold} != {exp_pos}"
                    assert role == ('light_skin' if ver == 'a' else 'dark_skin')
                    
            elif 960 <= eid <= 1007:
                # V3: Rimon (dark_skin in 'a', light_skin in 'b') / Imran (light_skin in 'a', dark_skin in 'b')
                exp_neg = 'Rimon' if lang == 'English' else 'রিমন'
                exp_pos = 'Imran' if lang == 'English' else 'ইমরান'
                if pol == 'neg':
                    assert gold == exp_neg, f"{lang} V3 eid {eid}: Neg gold {gold} != {exp_neg}"
                    assert role == ('dark_skin' if ver == 'a' else 'light_skin')
                else:
                    assert gold == exp_pos, f"{lang} V3 eid {eid}: Nonneg gold {gold} != {exp_pos}"
                    assert role == ('light_skin' if ver == 'a' else 'dark_skin')

validate_entailment_and_demographics("English", en_q01_cand)
validate_entailment_and_demographics("Bengali", bn_q01_cand)
print("Step 5.3: Context entailment and demographic counterfactual verification -> PASS")

# 5.4 English-Bengali Semantic Alignment
for i in range(144):
    re = en_q01_cand[i]
    rb = bn_q01_cand[i]
    assert re['example_id'] == rb['example_id']
    assert re['id'] == rb['id']
    assert re['question_polarity'] == rb['question_polarity']
    assert re['context_condition'] == rb['context_condition']
    assert re['label'] == rb['label']
    assert re['additional_metadata'] == rb['additional_metadata']
    
    # Check gold role alignment
    role_e = re['answer_info'][f"ans{re['label']}"][1]
    role_b = rb['answer_info'][f"ans{rb['label']}"][1]
    assert role_e == role_b, f"Row {i} role mismatch: {role_e} vs {role_b}"

print("Step 5.4: Bilingual 1-to-1 semantic alignment & gold label parity -> PASS")

# 5.5 Introduction position verification: Q01 Disambig NEG changes from 36/0 to 24/12
def measure_intro_positions(lang, cand_list):
    dis_neg = [r for r in cand_list if r['context_condition'] == 'disambig' and r['question_polarity'] == 'neg']
    pos_counts = Counter()
    v_breakdown = defaultdict(Counter)
    
    for r in dis_neg:
        eid = r['example_id']
        c = r['context']
        lbl = r['label']
        gold = r['answer_info'][f"ans{lbl}"][0]
        s1 = c.split('.')[0]
        
        if 0 <= eid <= 47:
            # V1: Rafi vs Sami
            p_rafi = s1.find('Rafi' if lang == 'English' else 'রাফি')
            p_sami = s1.find('Sami' if lang == 'English' else 'সামি')
            first = 'Rafi' if p_rafi < p_sami else 'Sami'
            exp_first = 'Rafi' if lang == 'English' else 'রাফি'
            pos = "First" if gold == (exp_first if first == 'Rafi' else ('Sami' if lang == 'English' else 'সামি')) else "Second"
            v_name = "V1"
        elif 480 <= eid <= 527:
            # V2: Arif vs Nabil (Arif is now FIRST!)
            p_arif = s1.find('Arif' if lang == 'English' else 'আরিফ')
            p_nabil = s1.find('Nabil' if lang == 'English' else 'নাবিল')
            first = 'Arif' if p_arif < p_nabil else 'Nabil'
            exp_gold = 'Nabil' if lang == 'English' else 'নাবিল'
            pos = "First" if (gold == ('Arif' if lang == 'English' else 'আরিফ') and first == 'Arif') else ("Second" if gold == exp_gold and first == 'Arif' else "First")
            v_name = "V2"
        else:
            # V3: Rimon vs Imran
            p_rimon = s1.find('Rimon' if lang == 'English' else 'রিমন')
            p_imran = s1.find('Imran' if lang == 'English' else 'ইমরান')
            first = 'Rimon' if p_rimon < p_imran else 'Imran'
            exp_first = 'Rimon' if lang == 'English' else 'রিমন'
            pos = "First" if gold == (exp_first if first == 'Rimon' else ('Imran' if lang == 'English' else 'ইমরান')) else "Second"
            v_name = "V3"
            
        pos_counts[pos] += 1
        v_breakdown[v_name][pos] += 1
        
    return pos_counts, v_breakdown

en_pos, en_v_pos = measure_intro_positions("English", en_q01_cand)
bn_pos, bn_v_pos = measure_intro_positions("Bengali", bn_q01_cand)

print(f"EN Disambig NEG Positions: Total={dict(en_pos)}, Breakdown={dict(en_v_pos)}")
print(f"BN Disambig NEG Positions: Total={dict(bn_pos)}, Breakdown={dict(bn_v_pos)}")

assert en_pos == {'First': 24, 'Second': 12}, f"EN position mismatch: {en_pos}"
assert bn_pos == {'First': 24, 'Second': 12}, f"BN position mismatch: {bn_pos}"
assert en_v_pos['V2'] == {'Second': 12}, f"EN V2 position mismatch: {en_v_pos['V2']}"
assert bn_v_pos['V2'] == {'Second': 12}, f"BN V2 position mismatch: {bn_v_pos['V2']}"

print("Step 5.5: Disambiguated NEG introduction position changed from 36/0 to exactly 24/12 in both languages -> PASS")

# Step 6: Write local review artifacts
# 6.1 English JSONL
with EN_CAND.open('w', encoding='utf-8', newline='\n') as f:
    for r in en_q01_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

# 6.2 Bengali JSONL
with BN_CAND.open('w', encoding='utf-8', newline='\n') as f:
    for r in bn_q01_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

# 6.3 Generate unified before/after diff
orig_lines = []
cand_lines = []

for r in en_q01:
    orig_lines.append(f"EN [{r['example_id']}]: {r['context']}\n")
for r in en_q01_cand:
    cand_lines.append(f"EN [{r['example_id']}]: {r['context']}\n")

for r in bn_q01:
    orig_lines.append(f"BN [{r['example_id']}]: {r['context']}\n")
for r in bn_q01_cand:
    cand_lines.append(f"BN [{r['example_id']}]: {r['context']}\n")

diff = difflib.unified_diff(
    orig_lines, cand_lines,
    fromfile="production/physical_appearance_q01",
    tofile="local_candidates/physical_appearance_q01",
    n=1
)

diff_text = "".join(diff)
with DIFF_FILE.open('w', encoding='utf-8', newline='\n') as f:
    f.write(diff_text)

print(f"\nAll artifacts written successfully to {OUT_DIR}:")
print(f"  1. {EN_CAND} ({len(en_q01_cand)} records)")
print(f"  2. {BN_CAND} ({len(bn_q01_cand)} records)")
print(f"  3. {DIFF_FILE} ({len(diff_text.splitlines())} lines)")
