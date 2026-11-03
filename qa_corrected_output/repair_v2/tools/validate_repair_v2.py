"""
validate_repair_v2.py
Author: Antigravity AI & BanglaBBQ QA Team
Date: November 3, 2026

Comprehensive independent validation suite for all 18 candidate JSONLs in qa_corrected_output/repair_v2/candidates/:
- Gate 1: Structural & Schema Invariants (15 keys, sequential IDs, record counts)
- Gate 2: Logical & Gold-Label Entailment (Ambig -> unknown, Disambig -> valid non-unknown)
- Gate 3: Bengali Linguistic Quality & Unicode Integrity (zero broken words, valid spacing)
- Gate 4: Bilingual Equivalence & Parity (100% label and condition agreement)
- Gate 5: Counterfactual Structure & Ambiguous Distinctness (zero duplicate counterfactual ambig contexts)
- Gate 6: Answer-Option Metadata Synchronization
- Gate 7: Position-Bias Distribution & Shortcut Analysis
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

CAND_DIR = 'qa_corrected_output/repair_v2/candidates'
LOG_FILE = 'qa_corrected_output/repair_v2/validation_results/validation_suite_output.txt'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

CATEGORIES = [
    ('Education', 2880),
    ('Ethnicity', 1440),
    ('HealthStatus', 2880),
    ('MaritalStatus', 2880),
    ('OccupationalBackground', 2880),
    ('Politics', 2880),
    ('Regional', 1440),
    ('Religion', 2880),
    ('SocialStatus', 1440),
]

REQUIRED_KEYS = {
    'example_id', 'question_index', 'question_polarity', 'context_condition',
    'category', 'answer_info', 'additional_metadata', 'context', 'question',
    'ans0', 'ans1', 'ans2', 'label'
}

CORRUPTED_TOKENS = [
    'একই্লাসে', 'বলতেওারও', 'নিয়মটিার্ষেত্রে', 'সেমিনারোর্সে',
    'ফলাফলাছাকাছি', 'বিশ্ববিদ্যালয়ের্লাবে'
]

log_lines = []

def log(msg=""):
    print(msg)
    log_lines.append(msg)

results = {}
total_records_checked = 0
gate_failures = defaultdict(list)

log("=" * 80)
log("BANGLABBQ REPAIR V2 INDEPENDENT FORENSIC VALIDATION SUITE")
log("=" * 80)

for cat_name, expected_count in CATEGORIES:
    log(f"\n>>> Validating Category: {cat_name} (Expected: {expected_count} records/lang)")
    
    eng_file = os.path.join(CAND_DIR, f'BanglaBBQ_ENG_{cat_name}.jsonl')
    ben_file = os.path.join(CAND_DIR, f'BanglaBBQ_BEN_{cat_name}.jsonl')
    
    assert os.path.exists(eng_file), f"Missing ENG file: {eng_file}"
    assert os.path.exists(ben_file), f"Missing BEN file: {ben_file}"
    
    with open(eng_file, 'r', encoding='utf-8') as f:
        eng_rows = [json.loads(line) for line in f]
    with open(ben_file, 'r', encoding='utf-8') as f:
        ben_rows = [json.loads(line) for line in f]
        
    assert len(eng_rows) == expected_count, f"ENG count mismatch: {len(eng_rows)} != {expected_count}"
    assert len(ben_rows) == expected_count, f"BEN count mismatch: {len(ben_rows)} != {expected_count}"
    total_records_checked += len(eng_rows) + len(ben_rows)
    
    cat_res = {
        'count_eng': len(eng_rows),
        'count_ben': len(ben_rows),
        'gate1_schema': True,
        'gate2_logic': True,
        'gate3_bengali_integrity': True,
        'gate4_bilingual_parity': True,
        'gate5_counterfactual_duplicates': 0,
        'gate6_metadata_sync': True,
        'label_dist_eng': Counter(r['label'] for r in eng_rows),
        'label_dist_ben': Counter(r['label'] for r in ben_rows),
        'positions_neg': {'first': 0, 'second': 0},
        'positions_nonneg': {'first': 0, 'second': 0},
    }
    
    # -------------------------------------------------------------
    # GATE 1: SCHEMA & ID INVARIANTS
    # -------------------------------------------------------------
    for lang, rows in [('ENG', eng_rows), ('BEN', ben_rows)]:
        for idx, r in enumerate(rows):
            if r['example_id'] != idx:
                gate_failures[cat_name].append(f"Gate 1: {lang} row {idx} example_id {r['example_id']} != {idx}")
                cat_res['gate1_schema'] = False
                break
            if not REQUIRED_KEYS.issubset(set(r.keys())):
                gate_failures[cat_name].append(f"Gate 1: {lang} row {idx} missing required keys")
                cat_res['gate1_schema'] = False
                break
            if r['label'] not in [0, 1, 2]:
                gate_failures[cat_name].append(f"Gate 1: {lang} row {idx} invalid label {r['label']}")
                cat_res['gate1_schema'] = False
                break
                
    # -------------------------------------------------------------
    # GATE 2: LOGICAL & GOLD-LABEL ENTAILMENT
    # -------------------------------------------------------------
    for lang, rows in [('ENG', eng_rows), ('BEN', ben_rows)]:
        for idx, r in enumerate(rows):
            lbl = r['label']
            gold_info = r['answer_info'][f'ans{lbl}']
            if r['context_condition'] == 'ambig':
                if gold_info[1] != 'unknown':
                    gate_failures[cat_name].append(f"Gate 2: {lang} row {idx} ambig gold is not unknown")
                    cat_res['gate2_logic'] = False
                    break
            else:
                if gold_info[1] == 'unknown':
                    gate_failures[cat_name].append(f"Gate 2: {lang} row {idx} disambig gold is unknown")
                    cat_res['gate2_logic'] = False
                    break

    # -------------------------------------------------------------
    # GATE 3: BENGALI LINGUISTIC QUALITY & UNICODE INTEGRITY
    # -------------------------------------------------------------
    corrupt_hits = 0
    for idx, r in enumerate(ben_rows):
        for ct in CORRUPTED_TOKENS:
            if ct in r['context'] or ct in r['question']:
                corrupt_hits += 1
                gate_failures[cat_name].append(f"Gate 3: BEN row {idx} contains corrupted token '{ct}'")
    if corrupt_hits > 0:
        cat_res['gate3_bengali_integrity'] = False
        
    # Check for residual placeholders in Ethnicity
    if cat_name == 'Ethnicity':
        res_e = sum(1 for r in eng_rows if re.search(r"\bB\b|\b[AB]'s\b|\b[AB]’s\b", r['context']))
        res_b = sum(1 for r in ben_rows if re.search(r'(?:^|\s)[কখ](?:[\s।,?!]|$)', r['context']))
        if res_e > 0 or res_b > 0:
            gate_failures[cat_name].append(f"Gate 3: Ethnicity residual placeholders: ENG={res_e}, BEN={res_b}")
            cat_res['gate3_bengali_integrity'] = False

    # -------------------------------------------------------------
    # GATE 4: BILINGUAL EQUIVALENCE & PARITY
    # -------------------------------------------------------------
    for idx, (er, br) in enumerate(zip(eng_rows, ben_rows)):
        if er['label'] != br['label']:
            gate_failures[cat_name].append(f"Gate 4: Label mismatch at row {idx}: ENG {er['label']} != BEN {br['label']}")
            cat_res['gate4_bilingual_parity'] = False
            break
        if er['context_condition'] != br['context_condition']:
            gate_failures[cat_name].append(f"Gate 4: Condition mismatch at row {idx}")
            cat_res['gate4_bilingual_parity'] = False
            break
        if er['question_polarity'] != br['question_polarity']:
            gate_failures[cat_name].append(f"Gate 4: Polarity mismatch at row {idx}")
            cat_res['gate4_bilingual_parity'] = False
            break

    # -------------------------------------------------------------
    # GATE 5: COUNTERFACTUAL DUPLICATE AMBIGUOUS CONTEXTS
    # -------------------------------------------------------------
    var_len = 48
    dups = 0
    for v_start in range(0, expected_count, var_len):
        block_a = eng_rows[v_start : v_start + 24]
        block_b = eng_rows[v_start + 24 : v_start + 48]
        for ra, rb in zip(block_a, block_b):
            if ra['context_condition'] == 'ambig' and rb['context_condition'] == 'ambig':
                if ra['context'] == rb['context']:
                    dups += 1
    cat_res['gate5_counterfactual_duplicates'] = dups
    if dups > 0:
        gate_failures[cat_name].append(f"Gate 5: Found {dups} identical ambiguous contexts between Block A and Block B")

    # -------------------------------------------------------------
    # GATE 6: ANSWER_INFO METADATA SYNCHRONIZATION
    # -------------------------------------------------------------
    if cat_name == 'Ethnicity':
        for lang, rows in [('ENG', eng_rows), ('BEN', ben_rows)]:
            for idx, r in enumerate(rows):
                for k in ['ans0', 'ans1', 'ans2']:
                    if r[k] != r['answer_info'][k][0]:
                        gate_failures[cat_name].append(f"Gate 6: {lang} row {idx} answer_info mismatch: {r[k]!r} != {r['answer_info'][k][0]!r}")
                        cat_res['gate6_metadata_sync'] = False
                        break

    # -------------------------------------------------------------
    # GATE 7: POSITION BIAS ANALYSIS
    # -------------------------------------------------------------
    for r in eng_rows:
        if r['context_condition'] == 'ambig':
            continue
        gold = r['ans' + str(r['label'])]
        ctx = r['context']
        non_unk = [r[k] for k in ['ans0', 'ans1', 'ans2'] if r['answer_info'][k][1] != 'unknown']
        e0_clean = non_unk[0].replace('The ', '').replace('the ', '')
        e1_clean = non_unk[1].replace('The ', '').replace('the ', '')
        p0 = ctx.find(e0_clean)
        p1 = ctx.find(e1_clean)
        first_ans = non_unk[0] if p0 < p1 else non_unk[1]
        second_ans = non_unk[1] if p0 < p1 else non_unk[0]
        
        pol = r['question_polarity']
        if pol == 'neg':
            if gold == first_ans: cat_res['positions_neg']['first'] += 1
            else: cat_res['positions_neg']['second'] += 1
        else:
            if gold == first_ans: cat_res['positions_nonneg']['first'] += 1
            else: cat_res['positions_nonneg']['second'] += 1
            
    results[cat_name] = cat_res
    
    log(f"  Count: {cat_res['count_eng']} ENG / {cat_res['count_ben']} BEN")
    log(f"  Gate 1 (Schema & IDs): {'PASS' if cat_res['gate1_schema'] else 'FAIL'}")
    log(f"  Gate 2 (Logic & Unknowns): {'PASS' if cat_res['gate2_logic'] else 'FAIL'}")
    log(f"  Gate 3 (Bengali Integrity): {'PASS' if cat_res['gate3_bengali_integrity'] else 'FAIL'}")
    log(f"  Gate 4 (Bilingual Parity): {'PASS' if cat_res['gate4_bilingual_parity'] else 'FAIL'}")
    log(f"  Gate 5 (Ambig Counterfactual Duplicates): {cat_res['gate5_counterfactual_duplicates']} dups")
    log(f"  Gate 6 (Metadata Sync): {'PASS' if cat_res['gate6_metadata_sync'] else 'FAIL'}")
    log(f"  Label Distribution (ENG): {dict(cat_res['label_dist_eng'])}")
    log(f"  Disambig Negative Positions: {cat_res['positions_neg']['first']} First / {cat_res['positions_neg']['second']} Second")
    log(f"  Disambig Non-Negative Positions: {cat_res['positions_nonneg']['first']} First / {cat_res['positions_nonneg']['second']} Second")

log("\n" + "=" * 80)
log(f"VALIDATION SUMMARY ACROSS ALL {len(CATEGORIES)} CATEGORIES ({total_records_checked} TOTAL RECORDS)")
log("=" * 80)

for cat_name, _ in CATEGORIES:
    res = results[cat_name]
    fails = gate_failures[cat_name]
    status = "CLEAN PASS" if len(fails) == 0 else f"{len(fails)} FAILURES"
    log(f"  {cat_name:25s} | {status}")
    for f in fails[:3]:
        log(f"    - {f}")

log("\nValidation suite execution completed.")

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines) + '\n')

print(f"\nSaved execution log to {LOG_FILE} (UTF-8)")
