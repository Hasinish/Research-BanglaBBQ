"""
generate_answer_change_manifest.py
Author: Antigravity AI & BanglaBBQ Research Team
Date: November 6, 2026

Generates machine-readable field-level change manifests for:
1. Ethnicity answer options (ans0..2) and answer_info
2. Politics answer options (ans0..2) in Bengali
Confirms demographic/political code invariance and answer assignment identity.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

FIXED_DIR = 'fixed JsonL'
CANON_DIR = 'Dataset_BanglaBBQ_New'
OUT_DIR = 'audits/final_18_jsonl_preflight/manifests'

# -------------------------------------------------------------
# 1. ETHNICITY ANSWER & METADATA MANIFEST
# -------------------------------------------------------------
eng_fix_eth = [json.loads(l) for l in open(os.path.join(FIXED_DIR, 'BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl'), encoding='utf-8')]
eng_can_eth = [json.loads(l) for l in open(os.path.join(CANON_DIR, 'BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl'), encoding='utf-8')]
ben_fix_eth = [json.loads(l) for l in open(os.path.join(FIXED_DIR, 'BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl'), encoding='utf-8')]
ben_can_eth = [json.loads(l) for l in open(os.path.join(CANON_DIR, 'BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl'), encoding='utf-8')]

ethnicity_manifest = {
    "category": "Ethnicity",
    "total_records_per_language": 1440,
    "demographic_code_invariance_verified": True,
    "unknown_mapping_invariance_verified": True,
    "english_answer_string_transformations": {},
    "bengali_answer_string_transformations": {},
    "representative_examples": []
}

for i in range(1440):
    fe, ce = eng_fix_eth[i], eng_can_eth[i]
    fb, cb = ben_fix_eth[i], ben_can_eth[i]
    
    # Verify codes
    for k in ['ans0', 'ans1', 'ans2']:
        assert fe['answer_info'][k][1] == ce['answer_info'][k][1], f"ENG code mismatch at {i} {k}"
        assert fb['answer_info'][k][1] == cb['answer_info'][k][1], f"BEN code mismatch at {i} {k}"
        assert fe['label'] == ce['label'], f"ENG label mismatch at {i}"
        assert fb['label'] == cb['label'], f"BEN label mismatch at {i}"
        
        # Track unique string mappings
        if ce[k] != fe[k]:
            ethnicity_manifest["english_answer_string_transformations"][ce[k]] = fe[k]
        if cb[k] != fb[k]:
            ethnicity_manifest["bengali_answer_string_transformations"][cb[k]] = fb[k]

# Add representative examples (first 5 distinct themes)
for t in range(5):
    idx = t * 144
    ethnicity_manifest["representative_examples"].append({
        "theme_index": t + 1,
        "row_index": idx,
        "canonical_eng_ans": [eng_can_eth[idx]['ans0'], eng_can_eth[idx]['ans1'], eng_can_eth[idx]['ans2']],
        "fixed_eng_ans":     [eng_fix_eth[idx]['ans0'], eng_fix_eth[idx]['ans1'], eng_fix_eth[idx]['ans2']],
        "canonical_eng_info": eng_can_eth[idx]['answer_info'],
        "fixed_eng_info":     eng_fix_eth[idx]['answer_info'],
        "canonical_ben_ans": [ben_can_eth[idx]['ans0'], ben_can_eth[idx]['ans1'], ben_can_eth[idx]['ans2']],
        "fixed_ben_ans":     [ben_fix_eth[idx]['ans0'], ben_fix_eth[idx]['ans1'], ben_fix_eth[idx]['ans2']],
        "canonical_ben_info": ben_can_eth[idx]['answer_info'],
        "fixed_ben_info":     ben_fix_eth[idx]['answer_info']
    })

with open(os.path.join(OUT_DIR, 'ethnicity_answer_change_manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(ethnicity_manifest, f, indent=2, ensure_ascii=False)

print(f"Generated ethnicity_answer_change_manifest.json with {len(ethnicity_manifest['english_answer_string_transformations'])} ENG and {len(ethnicity_manifest['bengali_answer_string_transformations'])} BEN transformations.")

# -------------------------------------------------------------
# 2. POLITICS ANSWER MANIFEST (BENGALI)
# -------------------------------------------------------------
ben_fix_pol = [json.loads(l) for l in open(os.path.join(FIXED_DIR, 'BanglaBBQ_BEN_Politics_QA_fixed.jsonl'), encoding='utf-8')]
ben_can_pol = [json.loads(l) for l in open(os.path.join(CANON_DIR, 'BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl'), encoding='utf-8')]

politics_manifest = {
    "category": "Politics",
    "total_records": 2880,
    "political_code_invariance_verified": True,
    "unknown_mapping_invariance_verified": True,
    "bengali_answer_string_transformations": {},
    "representative_examples": []
}

for i in range(2880):
    fb, cb = ben_fix_pol[i], ben_can_pol[i]
    for k in ['ans0', 'ans1', 'ans2']:
        assert fb['answer_info'][k][1] == cb['answer_info'][k][1], f"POL code mismatch at {i} {k}"
        assert fb['label'] == cb['label'], f"POL label mismatch at {i}"
        if cb[k] != fb[k]:
            politics_manifest["bengali_answer_string_transformations"][cb[k]] = fb[k]

# Find rows where ans changed
seen_themes = set()
for i in range(2880):
    fb, cb = ben_fix_pol[i], ben_can_pol[i]
    if fb['ans0'] != cb['ans0'] or fb['ans1'] != cb['ans1']:
        theme_id = i // 144 + 1
        if theme_id not in seen_themes:
            seen_themes.add(theme_id)
            politics_manifest["representative_examples"].append({
                "theme_index": theme_id,
                "row_index": i,
                "canonical_ben_ans": [cb['ans0'], cb['ans1'], cb['ans2']],
                "fixed_ben_ans":     [fb['ans0'], fb['ans1'], fb['ans2']],
                "canonical_ben_info": cb['answer_info'],
                "fixed_ben_info":     fb['answer_info']
            })

with open(os.path.join(OUT_DIR, 'politics_answer_change_manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(politics_manifest, f, indent=2, ensure_ascii=False)

print(f"Generated politics_answer_change_manifest.json with {len(politics_manifest['bengali_answer_string_transformations'])} BEN transformations.")

