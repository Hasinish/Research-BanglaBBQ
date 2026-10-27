import json
import os
import sys
import copy
import hashlib
import csv
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('.')
DATA_ROOT = ROOT / 'Dataset_BanglaBBQ_New'
OUT_ROOT = ROOT / 'local_candidates' / 'final_seven_category_qa'
CAND_DIR = OUT_ROOT / 'candidates'
DIFF_DIR = OUT_ROOT / 'diffs'
REP_DIR = OUT_ROOT / 'reports'

for d in [CAND_DIR, DIFF_DIR, REP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 15 targeted variations used for 50/50 orthogonal balancing
TARGET_15_VARS = [
    (1, 2), # Q01 V2 (EID 48..95)
    (2, 1), # Q02 V1 (EID 144..191)
    (2, 3), # Q02 V3 (EID 240..287)
    (3, 1), # Q03 V1 (EID 288..335)
    (3, 2), # Q03 V2 (EID 336..383)
    (4, 2), # Q04 V2 (EID 480..527)
    (4, 3), # Q04 V3 (EID 528..575)
    (5, 1), # Q05 V1 (EID 576..623)
    (5, 3), # Q05 V3 (EID 672..719)
    (6, 1), # Q06 V1 (EID 720..767)
    (6, 2), # Q06 V2 (EID 768..815)
    (7, 3), # Q07 V3 (EID 960..1007)
    (8, 1), # Q08 V1 (EID 1008..1055)
    (9, 2), # Q09 V2 (EID 1200..1247)
    (10, 3), # Q10 V3 (EID 1392..1439)
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# Change ledger entries list
change_ledger_rows = []

# ==========================================
# 1. REPAIR HEALTH STATUS
# ==========================================
print("\n>>> Processing Health Status...")
hs_dir = DATA_ROOT / 'BanglaBBQ_HealthStatus'
en_hs_prod = [json.loads(line) for line in open(hs_dir / 'BanglaBBQ_Health_Status_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_hs_prod = [json.loads(line) for line in open(hs_dir / 'BanglaBBQ_Health_Status_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_hs_cand = copy.deepcopy(en_hs_prod)
bn_hs_cand = copy.deepcopy(bn_hs_prod)

HEALTH_REPLACEMENTS = [
    (1, 2, 48, 96, 'Tuhin and Rafi each need', 'Rafi and Tuhin each need', 'তুহিন ও রাফি নিয়মিত', 'রাফি ও তুহিন নিয়মিত'),
    (2, 1, 144, 192, 'Kabir and Sagar each ask', 'Sagar and Kabir each ask', 'কবির ও সাগর বিকেলের', 'সাগর ও কবির বিকেলের'),
    (2, 3, 240, 288, 'Nila and Mita volunteer', 'Mita and Nila volunteer', 'নীলা ও মিতা অনানুষ্ঠানিক', 'মিতা ও নীলা অনানুষ্ঠানিক'),
    (3, 1, 288, 336, 'Rina and Rupa both sign up', 'Rupa and Rina both sign up', 'রিনা ও রূপা স্থানীয়', 'রূপা ও রিনা স্থানীয়'),
    (3, 2, 336, 384, 'Nafis and Tamim ask', 'Tamim and Nafis ask', 'নাফিস ও তামিম দুপুরের', 'তামিম ও নাফিস দুপুরের'),
    (4, 2, 480, 528, 'Rifat and Nabil earned', 'Nabil and Rifat earned', 'রিফাত ও নাবিল টাইপিং', 'নাবিল ও রিফাত টাইপিং'),
    (4, 3, 528, 576, 'Tuhin and Rafi each request', 'Rafi and Tuhin each request', 'তুহিন ও রাফি একই ধরনের', 'রাফি ও তুহিন একই ধরনের'),
    (5, 1, 576, 624, 'Mahi and Rumi both satisfy', 'Rumi and Mahi both satisfy', 'মাহি ও রুমি উপস্থিতি', 'রুমি ও মাহি উপস্থিতি'),
    (5, 3, 672, 720, 'Anik and Sajid volunteer', 'Sajid and Anik volunteer', 'অনিক ও সাজিদ স্বেচ্ছায়', 'সাজিদ ও অনিক স্বেচ্ছায়'),
    (6, 1, 720, 768, 'Nila and Mita volunteer', 'Mita and Nila volunteer', 'নীলা ও মিতা ক্যাম্পাসের', 'মিতা ও নীলা ক্যাম্পাসের'),
    (6, 2, 768, 816, 'Rina and Rupa each offer', 'Rupa and Rina each offer', 'রিনা ও রূপা পাঠচক্রে', 'রূপা ও রিনা পাঠচক্রে'),
    (7, 3, 960, 1008, 'Rifat and Nabil are eligible', 'Nabil and Rifat are eligible', 'রিফাত ও নাবিল যোগ্য', 'নাবিল ও রিফাত যোগ্য'),
    (8, 1, 1008, 1056, 'Tuhin and Rafi have identical', 'Rafi and Tuhin have identical', 'তুহিন ও রাফি জরুরি নয়', 'রাফি ও তুহিন জরুরি নয়'),
    (9, 2, 1200, 1248, 'Two students, Nila and Mita, ask', 'Two students, Mita and Nila, ask', 'পড়াশোনায় নীলা ও মিতা যোগ', 'পড়াশোনায় মিতা ও নীলা যোগ'),
    (10, 3, 1392, 1440, 'Raihan and Fahim volunteer', 'Fahim and Raihan volunteer', 'রায়হান ও ফাহিম ডিজিটাল', 'ফাহিম ও রায়হান ডিজিটাল'),
]

for q, v, start, end, en_find, en_replace, bn_find, bn_replace in HEALTH_REPLACEMENTS:
    for i in range(start, end):
        # English
        ctx_en_old = en_hs_cand[i]['context']
        assert ctx_en_old.count(en_find) == 1, f"EN {en_find} in EID {i}"
        en_hs_cand[i]['context'] = ctx_en_old.replace(en_find, en_replace, 1)
        change_ledger_rows.append({
            'Category': 'Health Status',
            'Language': 'English',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_hs_cand[i]['context'],
            'Justification': 'Reverse introductory name order to eliminate 100% first-person negative answer shortcut',
            'Validation outcome': 'PASS'
        })
        
        # Bengali
        ctx_bn_old = bn_hs_cand[i]['context']
        assert ctx_bn_old.count(bn_find) == 1, f"BN {bn_find} in EID {i}"
        bn_hs_cand[i]['context'] = ctx_bn_old.replace(bn_find, bn_replace, 1)
        change_ledger_rows.append({
            'Category': 'Health Status',
            'Language': 'Bengali',
            'Theme': f'Q{q:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_hs_cand[i]['context'],
            'Justification': 'Reverse introductory name order in Bengali to maintain exact semantic alignment with English and balance positions',
            'Validation outcome': 'PASS'
        })

en_hs_cand_path = CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_english.jsonl'
bn_hs_cand_path = CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_bengali.jsonl'

with open(en_hs_cand_path, 'w', encoding='utf-8') as f:
    for r in en_hs_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(bn_hs_cand_path, 'w', encoding='utf-8') as f:
    for r in bn_hs_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

hs_diff_lines = []
hs_diff_lines.append("--- canonical_production/BanglaBBQ_HealthStatus\n")
hs_diff_lines.append("+++ local_candidates/BanglaBBQ_HealthStatus\n")
for i in range(1440):
    if en_hs_prod[i]['context'] != en_hs_cand[i]['context']:
        hs_diff_lines.append(f"@@ -EN EID {i} @@\n")
        hs_diff_lines.append(f"- {en_hs_prod[i]['context']}\n")
        hs_diff_lines.append(f"+ {en_hs_cand[i]['context']}\n")
    if bn_hs_prod[i]['context'] != bn_hs_cand[i]['context']:
        hs_diff_lines.append(f"@@ -BN EID {i} @@\n")
        hs_diff_lines.append(f"- {bn_hs_prod[i]['context']}\n")
        hs_diff_lines.append(f"+ {bn_hs_cand[i]['context']}\n")

with open(DIFF_DIR / 'health_status_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(hs_diff_lines)

print(f"Health Status candidate JSONLs and diff saved. Diff lines: {len(hs_diff_lines)}")


# ==========================================
# 2. REPAIR REGIONAL AFFILIATION
# ==========================================
print("\n>>> Processing Regional Affiliation...")
reg_dir = DATA_ROOT / 'BanglaBBQ_Regional'
en_reg_prod = [json.loads(line) for line in open(reg_dir / 'BanglaBBQ_Regional_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_reg_prod = [json.loads(line) for line in open(reg_dir / 'BanglaBBQ_Regional_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_reg_cand = copy.deepcopy(en_reg_prod)
bn_reg_cand = copy.deepcopy(bn_reg_prod)

for t, v in TARGET_15_VARS:
    eid_start = (t - 1) * 144 + (v - 1) * 48
    
    rec_a = en_reg_prod[eid_start]
    opts_a = [info[0] for opt, info in rec_a['answer_info'].items() if info[1] != 'unknown']
    d1_en = opts_a[0].split('from ')[1].strip()
    d2_en = opts_a[1].split('from ')[1].strip()
    
    rec_bn_a = bn_reg_prod[eid_start]
    opts_bn_a = [info[0] for opt, info in rec_bn_a['answer_info'].items() if info[1] != 'unknown']
    d1_bn = opts_bn_a[0].split('থেকে আসা')[0].strip()
    d2_bn = opts_bn_a[1].split('থেকে আসা')[0].strip()
    
    en_find_a = f"{d1_en} and {d2_en}"
    en_repl_a = f"{d2_en} and {d1_en}"
    bn_find_a = f"{d1_bn} ও {d2_bn}"
    bn_repl_a = f"{d2_bn} ও {d1_bn}"
    
    en_find_b = f"{d2_en} and {d1_en}"
    en_repl_b = f"{d1_en} and {d2_en}"
    bn_find_b = f"{d2_bn} ও {d1_bn}"
    bn_repl_b = f"{d1_bn} ও {d2_bn}"
    
    # Orient a: eid_start .. eid_start+23
    for i in range(eid_start, eid_start + 24):
        ctx_en_old = en_reg_cand[i]['context']
        assert ctx_en_old.count(en_find_a) == 1, f"EN a {en_find_a} in EID {i}"
        en_reg_cand[i]['context'] = ctx_en_old.replace(en_find_a, en_repl_a, 1)
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'English',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in orientation a to balance first/second position',
            'Validation outcome': 'PASS'
        })
        
        ctx_bn_old = bn_reg_cand[i]['context']
        assert ctx_bn_old.count(bn_find_a) == 1, f"BN a {bn_find_a} in EID {i}"
        bn_reg_cand[i]['context'] = ctx_bn_old.replace(bn_find_a, bn_repl_a, 1)
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'Bengali',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in Bengali orientation a to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        
    # Orient b: eid_start+24 .. eid_start+47
    for i in range(eid_start + 24, eid_start + 48):
        ctx_en_old = en_reg_cand[i]['context']
        assert ctx_en_old.count(en_find_b) == 1, f"EN b {en_find_b} in EID {i}"
        en_reg_cand[i]['context'] = ctx_en_old.replace(en_find_b, en_repl_b, 1)
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'English',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in orientation b to balance first/second position',
            'Validation outcome': 'PASS'
        })
        
        ctx_bn_old = bn_reg_cand[i]['context']
        assert ctx_bn_old.count(bn_find_b) == 1, f"BN b {bn_find_b} in EID {i}"
        bn_reg_cand[i]['context'] = ctx_bn_old.replace(bn_find_b, bn_repl_b, 1)
        change_ledger_rows.append({
            'Category': 'Regional Affiliation',
            'Language': 'Bengali',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_reg_cand[i]['context'],
            'Justification': 'Reverse introductory district mention order in Bengali orientation b to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })

en_reg_cand_path = CAND_DIR / 'BanglaBBQ_Regional_FINAL_english.jsonl'
bn_reg_cand_path = CAND_DIR / 'BanglaBBQ_Regional_FINAL_bengali.jsonl'

with open(en_reg_cand_path, 'w', encoding='utf-8') as f:
    for r in en_reg_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(bn_reg_cand_path, 'w', encoding='utf-8') as f:
    for r in bn_reg_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

reg_diff_lines = []
reg_diff_lines.append("--- canonical_production/BanglaBBQ_Regional\n")
reg_diff_lines.append("+++ local_candidates/BanglaBBQ_Regional\n")
for i in range(1440):
    if en_reg_prod[i]['context'] != en_reg_cand[i]['context']:
        reg_diff_lines.append(f"@@ -EN EID {i} @@\n")
        reg_diff_lines.append(f"- {en_reg_prod[i]['context']}\n")
        reg_diff_lines.append(f"+ {en_reg_cand[i]['context']}\n")
    if bn_reg_prod[i]['context'] != bn_reg_cand[i]['context']:
        reg_diff_lines.append(f"@@ -BN EID {i} @@\n")
        reg_diff_lines.append(f"- {bn_reg_prod[i]['context']}\n")
        reg_diff_lines.append(f"+ {bn_reg_cand[i]['context']}\n")

with open(DIFF_DIR / 'regional_affiliation_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(reg_diff_lines)

print(f"Regional Affiliation candidate JSONLs and diff saved. Diff lines: {len(reg_diff_lines)}")


# ==========================================
# 3. REPAIR ETHNICITY
# ==========================================
print("\n>>> Processing Ethnicity...")
eth_dir = DATA_ROOT / 'BanglaBBQ_Ethnicity'
en_eth_prod = [json.loads(line) for line in open(eth_dir / 'BanglaBBQ_Ethnicity_FINAL_english.jsonl', encoding='utf-8') if line.strip()]
bn_eth_prod = [json.loads(line) for line in open(eth_dir / 'BanglaBBQ_Ethnicity_FINAL_bengali.jsonl', encoding='utf-8') if line.strip()]

en_eth_cand = copy.deepcopy(en_eth_prod)
bn_eth_cand = copy.deepcopy(bn_eth_prod)

for t, v in TARGET_15_VARS:
    eid_start = (t - 1) * 144 + (v - 1) * 48
    
    rec_a = en_eth_prod[eid_start]
    opts_a = [info[0] for opt, info in rec_a['answer_info'].items() if info[1] != 'unknown']
    e1_en = opts_a[0]
    e2_en = opts_a[1]
    
    rec_bn_a = bn_eth_prod[eid_start]
    opts_bn_a = [info[0] for opt, info in rec_bn_a['answer_info'].items() if info[1] != 'unknown']
    e1_bn = opts_bn_a[0]
    e2_bn = opts_bn_a[1]
    
    en_find_a = f"{e1_en} and {e2_en}"
    en_repl_a = f"{e2_en} and {e1_en}"
    bn_find_a = f"{e1_bn} এবং {e2_bn}"
    bn_repl_a = f"{e2_bn} এবং {e1_bn}"
    
    rec_b = en_eth_prod[eid_start + 24]
    opts_b = [info[0] for opt, info in rec_b['answer_info'].items() if info[1] != 'unknown']
    eb1_en = opts_b[0]
    eb2_en = opts_b[1]
    
    rec_bn_b = bn_eth_prod[eid_start + 24]
    opts_bn_b = [info[0] for opt, info in rec_bn_b['answer_info'].items() if info[1] != 'unknown']
    eb1_bn = opts_bn_b[0]
    eb2_bn = opts_bn_b[1]
    
    en_find_b = f"{eb1_en} and {eb2_en}"
    en_repl_b = f"{eb2_en} and {eb1_en}"
    bn_find_b = f"{eb1_bn} এবং {eb2_bn}"
    bn_repl_b = f"{eb2_bn} এবং {eb1_bn}"
    
    # Orient a: eid_start .. eid_start+23
    for i in range(eid_start, eid_start + 24):
        ctx_en_old = en_eth_cand[i]['context']
        assert ctx_en_old.count(en_find_a) == 1, f"EN a {en_find_a} in EID {i}"
        en_eth_cand[i]['context'] = ctx_en_old.replace(en_find_a, en_repl_a, 1)
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'English',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic participant order in orientation a to balance first/second position',
            'Validation outcome': 'PASS'
        })
        
        ctx_bn_old = bn_eth_cand[i]['context']
        assert ctx_bn_old.count(bn_find_a) == 1, f"BN a {bn_find_a} in EID {i}"
        bn_eth_cand[i]['context'] = ctx_bn_old.replace(bn_find_a, bn_repl_a, 1)
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'Bengali',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic participant order in Bengali orientation a to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })
        
    # Orient b: eid_start+24 .. eid_start+47
    for i in range(eid_start + 24, eid_start + 48):
        ctx_en_old = en_eth_cand[i]['context']
        assert ctx_en_old.count(en_find_b) == 1, f"EN b {en_find_b} in EID {i}"
        en_eth_cand[i]['context'] = ctx_en_old.replace(en_find_b, en_repl_b, 1)
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'English',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_en_old,
            'After value': en_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic participant order in orientation b to balance first/second position',
            'Validation outcome': 'PASS'
        })
        
        ctx_bn_old = bn_eth_cand[i]['context']
        assert ctx_bn_old.count(bn_find_b) == 1, f"BN b {bn_find_b} in EID {i}"
        bn_eth_cand[i]['context'] = ctx_bn_old.replace(bn_find_b, bn_repl_b, 1)
        change_ledger_rows.append({
            'Category': 'Ethnicity',
            'Language': 'Bengali',
            'Theme': f'Q{t:02d}',
            'Variation': f'V{v}',
            'example_id': i,
            'Changed field': 'context',
            'Before value': ctx_bn_old,
            'After value': bn_eth_cand[i]['context'],
            'Justification': 'Reverse introductory ethnic participant order in Bengali orientation b to maintain bilingual alignment',
            'Validation outcome': 'PASS'
        })

en_eth_cand_path = CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_english.jsonl'
bn_eth_cand_path = CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_bengali.jsonl'

with open(en_eth_cand_path, 'w', encoding='utf-8') as f:
    for r in en_eth_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(bn_eth_cand_path, 'w', encoding='utf-8') as f:
    for r in bn_eth_cand:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

eth_diff_lines = []
eth_diff_lines.append("--- canonical_production/BanglaBBQ_Ethnicity\n")
eth_diff_lines.append("+++ local_candidates/BanglaBBQ_Ethnicity\n")
for i in range(1440):
    if en_eth_prod[i]['context'] != en_eth_cand[i]['context']:
        eth_diff_lines.append(f"@@ -EN EID {i} @@\n")
        eth_diff_lines.append(f"- {en_eth_prod[i]['context']}\n")
        eth_diff_lines.append(f"+ {en_eth_cand[i]['context']}\n")
    if bn_eth_prod[i]['context'] != bn_eth_cand[i]['context']:
        eth_diff_lines.append(f"@@ -BN EID {i} @@\n")
        eth_diff_lines.append(f"- {bn_eth_prod[i]['context']}\n")
        eth_diff_lines.append(f"+ {bn_eth_cand[i]['context']}\n")

with open(DIFF_DIR / 'ethnicity_before_after.diff', 'w', encoding='utf-8') as f:
    f.writelines(eth_diff_lines)

print(f"Ethnicity candidate JSONLs and diff saved. Diff lines: {len(eth_diff_lines)}")


# Save change ledger CSV
ledger_path = DIFF_DIR / 'candidate_change_ledger.csv'
fieldnames = ['Category', 'Language', 'Theme', 'Variation', 'example_id', 'Changed field', 'Before value', 'After value', 'Justification', 'Validation outcome']
with open(ledger_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(change_ledger_rows)

print(f"Saved candidate change ledger to {ledger_path} with {len(change_ledger_rows)} rows.")
