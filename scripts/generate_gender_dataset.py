#!/usr/bin/env python3
"""
scripts/generate_gender_dataset.py

Deterministic generator and translation pipeline for BanglaBBQ Gender Identity benchmark.
Processes all 4,696 English records from PakBBQ source, translates content into natural
Bangladeshi Bengali, and exports canonical English and Bengali JSONL datasets with the
exact 15-column schema.

Author: Hasin Ishrak / BanglaBBQ Research Project
"""

import os
import json
import sys
import copy
import argparse

# Ensure UTF-8 output in Windows shells
sys.stdout.reconfigure(encoding='utf-8')

# Ensure script directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from gender_translation.base_mappings import ANS_MAP, QUESTION_MAP
from gender_translation.group1_translator import (
    translate_context_theme7,
    translate_context_theme10,
    translate_context_theme11,
    translate_context_theme12,
    translate_context_theme19,
)
from gender_translation.group2_translator import translate_context_group2
from gender_translation.group3_translator import (
    translate_context_theme51,
    translate_context_theme52,
    translate_context_theme53,
    translate_context_theme54,
    translate_context_theme55,
    translate_context_theme56,
    translate_context_theme57,
    translate_context_theme58,
)

SCHEMA_COLUMNS = [
    'example_id', 'question_index', 'context_condition', 'question_polarity', 'type',
    'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

SRC_PATH = os.path.join('PakBBQ_Repo', 'PakBBQ', 'PakBBQ_ENG', 'Gender_identity.jsonl')

def fix_metadata_inconsistencies(r):
    """
    Correct verified inherited metadata mismatches where female answers were tagged as male.
    Affected IDs:
    Q7: IDs 0, 1, 2, 3 -> ans2 'The female teacher' tagged as ['male', 'M'] -> ['female', 'F']
    Q51: IDs 4424, 4425, 4426, 4427 -> ans1 'The female' tagged as ['male', 'M'] -> ['female', 'F']
    Q53: IDs 4496, 4497, 4498, 4499 -> ans1 'The female' tagged as ['male', 'M'] -> ['female', 'F']
    """
    eid = r['example_id']
    r_copy = copy.deepcopy(r)
    if eid in [0, 1, 2, 3]:
        if 'answer_info' in r_copy and 'ans2' in r_copy['answer_info']:
            info = r_copy['answer_info']['ans2']
            if isinstance(info, list) and len(info) >= 2 and info[0] == 'male' and info[1] == 'M':
                r_copy['answer_info']['ans2'] = ['female', 'F']
    elif eid in [4424, 4425, 4426, 4427, 4496, 4497, 4498, 4499]:
        if 'answer_info' in r_copy and 'ans1' in r_copy['answer_info']:
            info = r_copy['answer_info']['ans1']
            if isinstance(info, list) and len(info) >= 2 and info[0] == 'male' and info[1] == 'M':
                r_copy['answer_info']['ans1'] = ['female', 'F']
    return r_copy

def reorder_record(r, c_bng=None, q_bng=None, ans0_bng=None, ans1_bng=None, ans2_bng=None):
    """Reorder keys to strictly match the canonical 15-column schema order."""
    r_fixed = fix_metadata_inconsistencies(r)
    return {
        'example_id': r_fixed['example_id'],
        'question_index': r_fixed['question_index'],
        'context_condition': r_fixed['context_condition'],
        'question_polarity': r_fixed['question_polarity'],
        'type': r_fixed['type'],
        'context': c_bng if c_bng is not None else r_fixed['context'],
        'question': q_bng if q_bng is not None else r_fixed['question'],
        'ans0': ans0_bng if ans0_bng is not None else r_fixed['ans0'],
        'ans1': ans1_bng if ans1_bng is not None else r_fixed['ans1'],
        'ans2': ans2_bng if ans2_bng is not None else r_fixed['ans2'],
        'label': r_fixed['label'],
        'answer_info': r_fixed['answer_info'],
        'additional_metadata': r_fixed['additional_metadata'],
        'category': r_fixed['category'],
        'id': r_fixed['id']
    }

def translate_record(r):
    """Translate context, question, and answer choices for a single record."""
    q_idx = str(r['question_index'])
    pol = r['question_polarity']
    q_eng = r['question']
    cond = r['context_condition']
    is_dis = (cond == 'disambig')
    c_eng = r['context']
    
    q_key = (q_idx, pol, q_eng)
    if q_key not in QUESTION_MAP:
        raise KeyError(f"Missing question translation for key: {q_key}")
    q_bng = QUESTION_MAP[q_key]
    
    if r['ans0'] not in ANS_MAP or r['ans1'] not in ANS_MAP or r['ans2'] not in ANS_MAP:
        raise KeyError(f"Missing answer translation in record {r['example_id']}: {r['ans0']}, {r['ans1']}, {r['ans2']}")
    ans0_bng = ANS_MAP[r['ans0']]
    ans1_bng = ANS_MAP[r['ans1']]
    ans2_bng = ANS_MAP[r['ans2']]
    
    if q_idx == '7': c_bng = translate_context_theme7(c_eng, is_dis)
    elif q_idx == '10': c_bng = translate_context_theme10(c_eng, is_dis)
    elif q_idx == '11': c_bng = translate_context_theme11(c_eng, is_dis)
    elif q_idx == '12': c_bng = translate_context_theme12(c_eng, is_dis)
    elif q_idx == '19': c_bng = translate_context_theme19(c_eng, is_dis)
    elif q_idx in ['51', '52', '53', '54', '55', '56', '57', '58']:
        if q_idx == '51': c_bng = translate_context_theme51(c_eng, is_dis)
        elif q_idx == '52': c_bng = translate_context_theme52(c_eng, is_dis)
        elif q_idx == '53': c_bng = translate_context_theme53(c_eng, is_dis)
        elif q_idx == '54': c_bng = translate_context_theme54(c_eng, is_dis)
        elif q_idx == '55': c_bng = translate_context_theme55(c_eng, is_dis)
        elif q_idx == '56': c_bng = translate_context_theme56(c_eng, is_dis)
        elif q_idx == '57': c_bng = translate_context_theme57(c_eng, is_dis)
        elif q_idx == '58': c_bng = translate_context_theme58(c_eng, is_dis)
    else:
        c_bng = translate_context_group2(r)
        
    return reorder_record(r, c_bng, q_bng, ans0_bng, ans1_bng, ans2_bng)

def main():
    parser = argparse.ArgumentParser(description="Generate BanglaBBQ Gender Identity datasets.")
    parser.add_argument('--out-dir', default='BanglaBBQ_Gender', help="Output directory for generated JSONL files")
    args = parser.parse_args()

    if not os.path.exists(SRC_PATH):
        raise FileNotFoundError(f"Source file not found at: {SRC_PATH}")
        
    os.makedirs(args.out_dir, exist_ok=True)
    eng_out_path = os.path.join(args.out_dir, 'Gender_identity_eng.jsonl')
    bng_out_path = os.path.join(args.out_dir, 'Gender_identity_bng.jsonl')

    with open(SRC_PATH, 'r', encoding='utf-8') as f:
        raw_eng_recs = [json.loads(line) for line in f]
    
    print(f"Loaded {len(raw_eng_recs)} raw records from {SRC_PATH}")
    
    # 1. Export canonical English
    eng_recs = [reorder_record(r) for r in raw_eng_recs]
    with open(eng_out_path, 'w', encoding='utf-8') as f:
        for r in eng_recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f"Exported {len(eng_recs)} English records to {eng_out_path}")
    
    # 2. Export canonical Bengali
    bng_recs = [translate_record(r) for r in raw_eng_recs]
    with open(bng_out_path, 'w', encoding='utf-8') as f:
        for r in bng_recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f"Exported {len(bng_recs)} Bengali records to {bng_out_path}")
    print("Generation complete.")

if __name__ == '__main__':
    main()
