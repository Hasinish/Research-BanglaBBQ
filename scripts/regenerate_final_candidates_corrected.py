import json
import os
import sys
import copy
import hashlib
import csv
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / 'Dataset_BanglaBBQ_New'
OUT_ROOT = ROOT / 'local_candidates' / 'final_seven_category_qa'
CAND_DIR = OUT_ROOT / 'candidates'
DIFF_DIR = OUT_ROOT / 'diffs'
REP_DIR = OUT_ROOT / 'reports'

for d in [CAND_DIR, DIFF_DIR, REP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

REVERSAL_PLAN = [
    # Exactly 15 variations: 5 in V1, 5 in V2, 5 in V3
    # Themes Q01..Q05 have 2 reversals (12/24), Themes Q06..Q10 have 1 reversal (24/12)
    (1, 1), (1, 2), (1, 4), (1, 5), (1, 6),
    (2, 1), (2, 3), (2, 4), (2, 7), (2, 8),
    (3, 2), (3, 3), (3, 5), (3, 9), (3, 10)
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_entities(r):
    unknown_synonyms = {'cannot be determined', 'unknown', 'অনির্ধারিত'}
    entities = []
    if 'answer_info' in r:
        for opt, info in r['answer_info'].items():
            ent = info[0].strip()
            if ent.lower() not in unknown_synonyms and ent not in entities:
                entities.append(ent)
    else:
        for k in ['ans0', 'ans1', 'ans2']:
            ent = r[k].strip()
            if ent.lower() not in unknown_synonyms and ent not in entities:
                entities.append(ent)
    return entities

change_ledger_rows = []

# ==============================================================================
# 1. HEALTH STATUS
# ==============================================================================
print("\n>>> Processing Health Status...")
en_hs_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_hs_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_HealthStatus/BanglaBBQ_Health_Status_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_hs_cand = copy.deepcopy(en_hs_prod)
bn_hs_cand = copy.deepcopy(bn_hs_prod)

hs_diff_lines = []

for v, q in sorted(REVERSAL_PLAN):
    s_id = (v - 1) * 480 + (q - 1) * 48
    e_id = s_id + 48
    
    ents_en = get_entities(en_hs_prod[s_id])
    e1_en, e2_en = ents_en[0], ents_en[1]
    ents_bn = get_entities(bn_hs_prod[s_id])
    e1_bn, e2_bn = ents_bn[0], ents_bn[1]
    
    sample_en = en_hs_prod[s_id]['context']
    sample_bn = bn_hs_prod[s_id]['context']
    
    find_en = f"{e1_en} and {e2_en}"
    repl_en = f"{e2_en} and {e1_en}"
    if find_en not in sample_en:
        find_en = f"{e2_en} and {e1_en}"
        repl_en = f"{e1_en} and {e2_en}"
        
    find_bn = f"{e1_bn} ও {e2_bn}"
    repl_bn = f"{e2_bn} ও {e1_bn}"
    if find_bn not in sample_bn:
        find_bn = f"{e2_bn} ও {e1_bn}"
        repl_bn = f"{e1_bn} ও {e2_bn}"
        
    for i in range(s_id, e_id):
        # English
        ctx_en_old = en_hs_prod[i]['context']
        assert ctx_en_old.count(find_en) == 1, f"EN Health V{v} Q{q} EID {i}"
        en_hs_cand[i]['context'] = ctx_en_old.replace(find_en, repl_en, 1)
        
        change_ledger_rows.append({
            'Category': 'Health Status',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_hs_cand[i]['context'],
            'Justification': 'Reverse introductory name order to eliminate 100% first-entity disambiguated negative shortcut',
            'Validation outcome': 'PASS'
        })
        hs_diff_lines.append(f"--- Health Status English EID {i} (V{v} Q{q:02d}) ---\n")
        hs_diff_lines.append(f"- {ctx_en_old}\n")
        hs_diff_lines.append(f"+ {en_hs_cand[i]['context']}\n")
        
        # Bengali
        ctx_bn_old = bn_hs_prod[i]['context']
        assert ctx_bn_old.count(find_bn) == 1, f"BN Health V{v} Q{q} EID {i}"
        bn_hs_cand[i]['context'] = ctx_bn_old.replace(find_bn, repl_bn, 1)
        
        change_ledger_rows.append({
            'Category': 'Health Status',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_hs_cand[i]['context'],
            'Justification': 'Reverse introductory name order in Bengali to maintain exact semantic alignment',
            'Validation outcome': 'PASS'
        })
        hs_diff_lines.append(f"--- Health Status Bengali EID {i} (V{v} Q{q:02d}) ---\n")
        hs_diff_lines.append(f"- {ctx_bn_old}\n")
        hs_diff_lines.append(f"+ {bn_hs_cand[i]['context']}\n")

with open(CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_english.jsonl', 'w', encoding='utf-8') as f:
    for r in en_hs_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_bengali.jsonl', 'w', encoding='utf-8') as f:
    for r in bn_hs_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(DIFF_DIR / 'health_status_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(hs_diff_lines)

print(f"Health Status saved. Diff lines: {len(hs_diff_lines)}")

# ==============================================================================
# 2. REGIONAL AFFILIATION
# ==============================================================================
print("\n>>> Processing Regional Affiliation...")
en_reg_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_Regional/BanglaBBQ_Regional_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_reg_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_Regional/BanglaBBQ_Regional_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_reg_cand = copy.deepcopy(en_reg_prod)
bn_reg_cand = copy.deepcopy(bn_reg_prod)

reg_diff_lines = []

for v, q in sorted(REVERSAL_PLAN):
    s_id = (v - 1) * 480 + (q - 1) * 48
    
    # Orientation a: s_id .. s_id + 23
    r_a_en = en_reg_prod[s_id]
    opts_a_en = [info[0].replace('The person from', '').replace('the person from', '').strip() for opt, info in r_a_en['answer_info'].items() if info[1] != 'unknown']
    d1_en, d2_en = opts_a_en[0], opts_a_en[1]
    
    r_a_bn = bn_reg_prod[s_id]
    opts_a_bn = [info[0].split('থেকে')[0].strip() for opt, info in r_a_bn['answer_info'].items() if info[1] != 'unknown']
    d1_bn, d2_bn = opts_a_bn[0], opts_a_bn[1]
    
    find_a_en = f"{d1_en} and {d2_en}"
    repl_a_en = f"{d2_en} and {d1_en}"
    if find_a_en not in r_a_en['context']:
        find_a_en = f"{d2_en} and {d1_en}"
        repl_a_en = f"{d1_en} and {d2_en}"
        
    find_a_bn = f"{d1_bn} ও {d2_bn}"
    repl_a_bn = f"{d2_bn} ও {d1_bn}"
    if find_a_bn not in r_a_bn['context']:
        find_a_bn = f"{d2_bn} ও {d1_bn}"
        repl_a_bn = f"{d1_bn} ও {d2_bn}"
        
    for i in range(s_id, s_id + 24):
        ctx_en_old = en_reg_prod[i]['context']
        assert ctx_en_old.count(find_a_en) == 1, f"EN Reg a V{v} Q{q} EID {i}"
        en_reg_cand[i]['context'] = ctx_en_old.replace(find_a_en, repl_a_en, 1)
        
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in orientation a to balance first/second position',
            'Validation outcome': 'PASS'
        })
        reg_diff_lines.append(f"--- Regional English EID {i} (V{v} Q{q:02d}) ---\n")
        reg_diff_lines.append(f"- {ctx_en_old}\n")
        reg_diff_lines.append(f"+ {en_reg_cand[i]['context']}\n")
        
        ctx_bn_old = bn_reg_prod[i]['context']
        assert ctx_bn_old.count(find_a_bn) == 1, f"BN Reg a V{v} Q{q} EID {i}"
        bn_reg_cand[i]['context'] = ctx_bn_old.replace(find_a_bn, repl_a_bn, 1)
        
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in Bengali orientation a to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        reg_diff_lines.append(f"--- Regional Bengali EID {i} (V{v} Q{q:02d}) ---\n")
        reg_diff_lines.append(f"- {ctx_bn_old}\n")
        reg_diff_lines.append(f"+ {bn_reg_cand[i]['context']}\n")
        
    # Orientation b: s_id + 24 .. s_id + 47
    r_b_en = en_reg_prod[s_id + 24]
    opts_b_en = [info[0].replace('The person from', '').replace('the person from', '').strip() for opt, info in r_b_en['answer_info'].items() if info[1] != 'unknown']
    d1_b_en, d2_b_en = opts_b_en[0], opts_b_en[1]
    
    r_b_bn = bn_reg_prod[s_id + 24]
    opts_b_bn = [info[0].split('থেকে')[0].strip() for opt, info in r_b_bn['answer_info'].items() if info[1] != 'unknown']
    d1_b_bn, d2_b_bn = opts_b_bn[0], opts_b_bn[1]
    
    find_b_en = f"{d1_b_en} and {d2_b_en}"
    repl_b_en = f"{d2_b_en} and {d1_b_en}"
    if find_b_en not in r_b_en['context']:
        find_b_en = f"{d2_b_en} and {d1_b_en}"
        repl_b_en = f"{d1_b_en} and {d2_b_en}"
        
    find_b_bn = f"{d1_b_bn} ও {d2_b_bn}"
    repl_b_bn = f"{d2_b_bn} ও {d1_b_bn}"
    if find_b_bn not in r_b_bn['context']:
        find_b_bn = f"{d2_b_bn} ও {d1_b_bn}"
        repl_b_bn = f"{d1_b_bn} ও {d2_b_bn}"
        
    for i in range(s_id + 24, s_id + 48):
        ctx_en_old = en_reg_prod[i]['context']
        assert ctx_en_old.count(find_b_en) == 1, f"EN Reg b V{v} Q{q} EID {i}"
        en_reg_cand[i]['context'] = ctx_en_old.replace(find_b_en, repl_b_en, 1)
        
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in orientation b to balance first/second position',
            'Validation outcome': 'PASS'
        })
        reg_diff_lines.append(f"--- Regional English EID {i} (V{v} Q{q:02d}) ---\n")
        reg_diff_lines.append(f"- {ctx_en_old}\n")
        reg_diff_lines.append(f"+ {en_reg_cand[i]['context']}\n")
        
        ctx_bn_old = bn_reg_prod[i]['context']
        assert ctx_bn_old.count(find_b_bn) == 1, f"BN Reg b V{v} Q{q} EID {i}"
        bn_reg_cand[i]['context'] = ctx_bn_old.replace(find_b_bn, repl_b_bn, 1)
        
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in Bengali orientation b to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        reg_diff_lines.append(f"--- Regional Bengali EID {i} (V{v} Q{q:02d}) ---\n")
        reg_diff_lines.append(f"- {ctx_bn_old}\n")
        reg_diff_lines.append(f"+ {bn_reg_cand[i]['context']}\n")

with open(CAND_DIR / 'BanglaBBQ_Regional_FINAL_english.jsonl', 'w', encoding='utf-8') as f:
    for r in en_reg_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(CAND_DIR / 'BanglaBBQ_Regional_FINAL_bengali.jsonl', 'w', encoding='utf-8') as f:
    for r in bn_reg_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(DIFF_DIR / 'regional_affiliation_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(reg_diff_lines)

print(f"Regional Affiliation saved. Diff lines: {len(reg_diff_lines)}")

# ==============================================================================
# 3. ETHNICITY
# ==============================================================================
print("\n>>> Processing Ethnicity...")
en_eth_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_eth_prod = [json.loads(line) for line in open(DATA_ROOT / 'BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_eth_cand = copy.deepcopy(en_eth_prod)
bn_eth_cand = copy.deepcopy(bn_eth_prod)

eth_diff_lines = []

for v, q in sorted(REVERSAL_PLAN):
    s_id = (v - 1) * 480 + (q - 1) * 48
    
    # Orientation a: s_id .. s_id + 23
    r_a_en = en_eth_prod[s_id]
    opts_a_en = [info[0].strip() for opt, info in r_a_en['answer_info'].items() if info[1] != 'unknown']
    e1_en, e2_en = opts_a_en[0], opts_a_en[1]
    
    r_a_bn = bn_eth_prod[s_id]
    opts_a_bn = [info[0].strip() for opt, info in r_a_bn['answer_info'].items() if info[1] != 'unknown']
    e1_bn, e2_bn = opts_a_bn[0], opts_a_bn[1]
    
    find_a_en = f"{e1_en} and {e2_en}"
    repl_a_en = f"{e2_en} and {e1_en}"
    if find_a_en not in r_a_en['context']:
        find_a_en = f"{e2_en} and {e1_en}"
        repl_a_en = f"{e1_en} and {e2_en}"
        
    find_a_bn = f"{e1_bn} এবং {e2_bn}"
    repl_a_bn = f"{e2_bn} এবং {e1_bn}"
    if find_a_bn not in r_a_bn['context']:
        find_a_bn = f"{e1_bn} ও {e2_bn}"
        repl_a_bn = f"{e2_bn} ও {e1_bn}"
        if find_a_bn not in r_a_bn['context']:
            find_a_bn = f"{e2_bn} এবং {e1_bn}"
            repl_a_bn = f"{e1_bn} এবং {e2_bn}"
            
    for i in range(s_id, s_id + 24):
        ctx_en_old = en_eth_prod[i]['context']
        assert ctx_en_old.count(find_a_en) == 1, f"EN Eth a V{v} Q{q} EID {i}"
        en_eth_cand[i]['context'] = ctx_en_old.replace(find_a_en, repl_a_en, 1)
        
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic group mention order in orientation a to balance first/second position',
            'Validation outcome': 'PASS'
        })
        eth_diff_lines.append(f"--- Ethnicity English EID {i} (V{v} Q{q:02d}) ---\n")
        eth_diff_lines.append(f"- {ctx_en_old}\n")
        eth_diff_lines.append(f"+ {en_eth_cand[i]['context']}\n")
        
        ctx_bn_old = bn_eth_prod[i]['context']
        assert ctx_bn_old.count(find_a_bn) == 1, f"BN Eth a V{v} Q{q} EID {i}"
        bn_eth_cand[i]['context'] = ctx_bn_old.replace(find_a_bn, repl_a_bn, 1)
        
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic group mention order in Bengali orientation a to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        eth_diff_lines.append(f"--- Ethnicity Bengali EID {i} (V{v} Q{q:02d}) ---\n")
        eth_diff_lines.append(f"- {ctx_bn_old}\n")
        eth_diff_lines.append(f"+ {bn_eth_cand[i]['context']}\n")
        
    # Orientation b: s_id + 24 .. s_id + 47
    r_b_en = en_eth_prod[s_id + 24]
    opts_b_en = [info[0].strip() for opt, info in r_b_en['answer_info'].items() if info[1] != 'unknown']
    e1_b_en, e2_b_en = opts_b_en[0], opts_b_en[1]
    
    r_b_bn = bn_eth_prod[s_id + 24]
    opts_b_bn = [info[0].strip() for opt, info in r_b_bn['answer_info'].items() if info[1] != 'unknown']
    e1_b_bn, e2_b_bn = opts_b_bn[0], opts_b_bn[1]
    
    find_b_en = f"{e1_b_en} and {e2_b_en}"
    repl_b_en = f"{e2_b_en} and {e1_b_en}"
    if find_b_en not in r_b_en['context']:
        find_b_en = f"{e2_b_en} and {e1_b_en}"
        repl_b_en = f"{e1_b_en} and {e2_b_en}"
        
    find_b_bn = f"{e1_b_bn} এবং {e2_b_bn}"
    repl_b_bn = f"{e2_b_bn} এবং {e1_b_bn}"
    if find_b_bn not in r_b_bn['context']:
        find_b_bn = f"{e1_b_bn} ও {e2_b_bn}"
        repl_b_bn = f"{e2_b_bn} ও {e1_b_bn}"
        if find_b_bn not in r_b_bn['context']:
            find_b_bn = f"{e2_b_bn} এবং {e1_b_bn}"
            repl_b_bn = f"{e1_b_bn} এবং {e2_b_bn}"
            
    for i in range(s_id + 24, s_id + 48):
        ctx_en_old = en_eth_prod[i]['context']
        assert ctx_en_old.count(find_b_en) == 1, f"EN Eth b V{v} Q{q} EID {i}"
        en_eth_cand[i]['context'] = ctx_en_old.replace(find_b_en, repl_b_en, 1)
        
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic group mention order in orientation b to balance first/second position',
            'Validation outcome': 'PASS'
        })
        eth_diff_lines.append(f"--- Ethnicity English EID {i} (V{v} Q{q:02d}) ---\n")
        eth_diff_lines.append(f"- {ctx_en_old}\n")
        eth_diff_lines.append(f"+ {en_eth_cand[i]['context']}\n")
        
        ctx_bn_old = bn_eth_prod[i]['context']
        assert ctx_bn_old.count(find_b_bn) == 1, f"BN Eth b V{v} Q{q} EID {i}"
        bn_eth_cand[i]['context'] = ctx_bn_old.replace(find_b_bn, repl_b_bn, 1)
        
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic group mention order in Bengali orientation b to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        eth_diff_lines.append(f"--- Ethnicity Bengali EID {i} (V{v} Q{q:02d}) ---\n")
        eth_diff_lines.append(f"- {ctx_bn_old}\n")
        eth_diff_lines.append(f"+ {bn_eth_cand[i]['context']}\n")

with open(CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_english.jsonl', 'w', encoding='utf-8') as f:
    for r in en_eth_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_bengali.jsonl', 'w', encoding='utf-8') as f:
    for r in bn_eth_cand: f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(DIFF_DIR / 'ethnicity_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(eth_diff_lines)

print(f"Ethnicity saved. Diff lines: {len(eth_diff_lines)}")

# ==============================================================================
# 4. REBUILD CHANGE LEDGER WITH ZERO INDEXING ERRORS
# ==============================================================================
print("\n>>> Writing corrected candidate_change_ledger.csv...")
ledger_path = DIFF_DIR / 'candidate_change_ledger.csv'
fieldnames = [
    'Category', 'Language', 'Theme', 'Variation', 'example_id',
    'Changed field', 'Before value', 'After value', 'Justification', 'Validation outcome'
]
with open(ledger_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(change_ledger_rows)

print(f"Candidate change ledger written with {len(change_ledger_rows)} rows.")

# Verify zero indexing errors in ledger
for r in change_ledger_rows:
    eid = r['example_id']
    expected_v = f"V{(eid // 480) + 1}"
    expected_q = f"Q{((eid % 480) // 48) + 1:02d}"
    assert r['Variation'] == expected_v, f"Ledger Variation mismatch in EID {eid}: {r['Variation']} vs {expected_v}"
    assert r['Theme'] == expected_q, f"Ledger Theme mismatch in EID {eid}: {r['Theme']} vs {expected_q}"

print("VERIFIED: Exactly 0 Theme/Variation indexing errors in candidate_change_ledger.csv!")
