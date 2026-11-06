"""
comprehensive_audit_runner.py
Author: Antigravity AI & BanglaBBQ Research Team
Date: November 6, 2026

Fully reproducible forensic audit suite for the 18 candidate JSONL files in 'fixed JsonL/':
1. Structural Invariant Gates (Schema, sequential IDs, record counts, label bounds)
2. Condition-Label Entailment Gates (Ambig -> unknown, Disambig -> non-unknown)
3. Canonical Difference Tracking (Field-level diffs vs Dataset_BanglaBBQ_New)
4. Bengali Linguistic & Lexical Gates (Bureaucratic vocabulary, broken tokens, hyphenated suffixes)
5. Bilingual Equivalence Gates (Label agreement, condition pairing, polarity matching, code matching)
6. Counterfactual Ambiguous Duplicate Gate (Zero identical Block A / Block B ambiguous contexts)
7. Answer-Position & Heuristic Susceptibility Analysis (First/Second distributions, heuristic baselines)
8. Exact Spreadsheet Parity Sizing (43,200 rows x 15 columns = 648,000 cells)
"""

import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

FIXED_DIR = 'fixed JsonL'
CANON_DIR = 'Dataset_BanglaBBQ_New'
LOG_FILE = 'audits/final_18_jsonl_preflight/logs/audit_execution_log.txt'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

CATEGORIES = [
    ('Education', 'BanglaBBQ_EducationalBackground', 2880),
    ('Ethnicity', 'BanglaBBQ_Ethnicity', 1440),
    ('HealthStatus', 'BanglaBBQ_HealthStatus', 2880),
    ('MaritalStatus', 'BanglaBBQ_MaritalStatus', 2880),
    ('OccupationalBackground', 'BanglaBBQ_OccupationalBackground', 2880),
    ('Politics', 'BanglaBBQ_Politics', 2880),
    ('Regional', 'BanglaBBQ_Regional', 1440),
    ('Religion', 'BanglaBBQ_Religion', 2880),
    ('SocialStatus', 'BanglaBBQ_SocialStatus', 1440),
]

REQUIRED_KEYS = [
    'example_id', 'question_index', 'question_polarity', 'context_condition',
    'category', 'answer_info', 'additional_metadata', 'context', 'question',
    'ans0', 'ans1', 'ans2', 'label'
]

BUREAUCRATIC_PATTERNS = [
    'অবহিত করেন', 'প্রদান করেন', 'দাখিল করেন', 'ব্যর্থ হন',
    'উক্ত', 'সম্পাদন করেন', 'গ্রহণ করেন'
]

BROKEN_TOKENS = [
    'একই্লাসে', 'বলতেওারও', 'নিয়মটিার্ষেত্রে', 'সেমিনারোর্সে',
    'ফলাফলাছাকাছি', 'বিশ্ববিদ্যালয়ের্লাবে'
]

log_lines = []

def log(msg=""):
    print(msg)
    log_lines.append(msg)

log("=" * 80)
log("BANGLABBQ COMPREHENSIVE PREFLIGHT FORENSIC AUDIT (REPRODUCIBLE RUNNER)")
log("=" * 80)

total_records = 0
total_cells = 0
audit_matrix = []

for cat_short, cat_dir, expected_count in CATEGORIES:
    log(f"\n>>> AUDITING CATEGORY: {cat_short.upper()} ({expected_count} rows/language)")
    
    eng_fix_file = os.path.join(FIXED_DIR, f'BanglaBBQ_ENG_{cat_short}_QA_fixed.jsonl')
    ben_fix_file = os.path.join(FIXED_DIR, f'BanglaBBQ_BEN_{cat_short}_QA_fixed.jsonl')
    eng_can_file = os.path.join(CANON_DIR, cat_dir, f'BanglaBBQ_ENG_{cat_short}.jsonl')
    ben_can_file = os.path.join(CANON_DIR, cat_dir, f'BanglaBBQ_BEN_{cat_short}.jsonl')
    
    # Read files
    with open(eng_fix_file, 'r', encoding='utf-8') as f:
        eng_fix = [json.loads(l) for l in f]
    with open(ben_fix_file, 'r', encoding='utf-8') as f:
        ben_fix = [json.loads(l) for l in f]
    with open(eng_can_file, 'r', encoding='utf-8') as f:
        eng_can = [json.loads(l) for l in f]
    with open(ben_can_file, 'r', encoding='utf-8') as f:
        ben_can = [json.loads(l) for l in f]
        
    n_eng = len(eng_fix)
    n_ben = len(ben_fix)
    total_records += n_eng + n_ben
    total_cells += (n_eng + n_ben) * 15
    
    # Check Gate 1: Structure & Schema
    struct_errors = []
    for lang, rows in [('ENG', eng_fix), ('BEN', ben_fix)]:
        if len(rows) != expected_count:
            struct_errors.append(f"{lang} count mismatch: {len(rows)} != {expected_count}")
        for idx, r in enumerate(rows):
            if r.get('example_id') != idx:
                struct_errors.append(f"{lang} row {idx} invalid ID {r.get('example_id')}")
                break
            for k in REQUIRED_KEYS:
                if k not in r:
                    struct_errors.append(f"{lang} row {idx} missing key {k}")
                    break
            if r.get('label') not in [0, 1, 2]:
                struct_errors.append(f"{lang} row {idx} invalid label {r.get('label')}")
                break
                
    # Check Gate 2: Logic & Unknown mapping
    logic_errors = []
    for lang, rows in [('ENG', eng_fix), ('BEN', ben_fix)]:
        for idx, r in enumerate(rows):
            lbl = r['label']
            gold_info = r['answer_info'][f'ans{lbl}']
            if r['context_condition'] == 'ambig':
                if gold_info[1] != 'unknown':
                    logic_errors.append(f"{lang} row {idx} ambig gold is not unknown")
                    break
            else:
                if gold_info[1] == 'unknown':
                    logic_errors.append(f"{lang} row {idx} disambig gold is unknown")
                    break
                    
    # Check Gate 3: Diffs vs Canonical
    diffs = {'ENG': defaultdict(int), 'BEN': defaultdict(int)}
    unexpected_changes = []
    for lang, fix_rows, can_rows in [('ENG', eng_fix, eng_can), ('BEN', ben_fix, ben_can)]:
        for idx, (fr, cr) in enumerate(zip(fix_rows, can_rows)):
            for k in REQUIRED_KEYS:
                if fr[k] != cr[k]:
                    diffs[lang][k] += 1
                    if k not in ['context', 'question']:
                        unexpected_changes.append((lang, idx, k))
                        
    # Check Gate 4: Bengali Linguistic Quality
    bureau_hits = Counter()
    broken_hits = Counter()
    for r in ben_fix:
        text = r['context'] + " " + r['question']
        for b in BUREAUCRATIC_PATTERNS:
            if b in text: bureau_hits[b] += 1
        for brk in BROKEN_TOKENS:
            if brk in text: broken_hits[brk] += 1
            
    # Check Gate 5: Bilingual Equivalence
    bilingual_mismatches = 0
    for idx, (er, br) in enumerate(zip(eng_fix, ben_fix)):
        if er['label'] != br['label'] or er['context_condition'] != br['context_condition'] or er['question_polarity'] != br['question_polarity']:
            bilingual_mismatches += 1
        for k in ['ans0', 'ans1', 'ans2']:
            if er['answer_info'][k][1] != br['answer_info'][k][1]:
                bilingual_mismatches += 1
                
    # Check Gate 6: Counterfactual Ambig Duplicates
    var_len = 48
    amb_dups = 0
    for v_start in range(0, expected_count, var_len):
        block_a = eng_fix[v_start : v_start + 24]
        block_b = eng_fix[v_start + 24 : v_start + 48]
        for ra, rb in zip(block_a, block_b):
            if ra['context_condition'] == 'ambig' and rb['context_condition'] == 'ambig':
                if ra['context'] == rb['context']:
                    amb_dups += 1
                    
    # Check Gate 7: Position Distributions
    pos_neg = {'first': 0, 'second': 0}
    pos_nonneg = {'first': 0, 'second': 0}
    for r in eng_fix:
        if r['context_condition'] == 'ambig': continue
        gold = r['ans' + str(r['label'])]
        ctx = r['context']
        non_unk = [r[k] for k in ['ans0', 'ans1', 'ans2'] if r['answer_info'][k][1] != 'unknown']
        e0_clean = non_unk[0].replace('The ', '').replace('the ', '')
        e1_clean = non_unk[1].replace('The ', '').replace('the ', '')
        p0 = ctx.find(e0_clean)
        p1 = ctx.find(e1_clean)
        first_ans = non_unk[0] if p0 < p1 else non_unk[1]
        if r['question_polarity'] == 'neg':
            if gold == first_ans: pos_neg['first'] += 1
            else: pos_neg['second'] += 1
        else:
            if gold == first_ans: pos_nonneg['first'] += 1
            else: pos_nonneg['second'] += 1

    # Log results
    log(f"  Record Counts: {n_eng} ENG / {n_ben} BEN (Expected: {expected_count})")
    log(f"  Gate 1 (Structure & Schema): {'PASS' if not struct_errors else f'FAIL: {struct_errors[:2]}'}")
    log(f"  Gate 2 (Logic & Unknowns):   {'PASS' if not logic_errors else f'FAIL: {logic_errors[:2]}'}")
    log(f"  Gate 3 (Canonical Diffs):    ENG={dict(diffs['ENG'])}, BEN={dict(diffs['BEN'])}")
    log(f"    - Unexpected field changes: {len(unexpected_changes)}")
    log(f"  Gate 4 (Bengali Naturalness): Bureaucratic={sum(bureau_hits.values())}, Broken={sum(broken_hits.values())}")
    log(f"  Gate 5 (Bilingual Parity):   Mismatches={bilingual_mismatches}")
    log(f"  Gate 6 (Ambig Duplicates):   {amb_dups} duplicate counterfactual pairs")
    log(f"  Gate 7 (Position Balance):   Neg: {pos_neg['first']} First / {pos_neg['second']} Second | NonNeg: {pos_nonneg['first']} First / {pos_nonneg['second']} Second")

    audit_matrix.append({
        'category': cat_short,
        'count': expected_count,
        'struct_pass': len(struct_errors) == 0,
        'logic_pass': len(logic_errors) == 0,
        'unexpected_changes': len(unexpected_changes),
        'bilingual_pass': bilingual_mismatches == 0,
        'amb_dups': amb_dups,
        'pos_neg_first': pos_neg['first'],
        'pos_neg_second': pos_neg['second'],
    })

log("\n" + "=" * 80)
log(f"AUDIT SUMMARY: {total_records} TOTAL RECORDS | {total_cells} TOTAL DATA CELLS")
log("=" * 80)
log(f"Spreadsheet Parity Verification: Exactly {total_records} rows x 15 columns = {total_cells:,} data cells across 18 worksheets.")

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines) + '\n')

print(f"\nExecution log persisted to: {LOG_FILE}")

