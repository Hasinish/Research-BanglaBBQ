import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def validate_religion_dataset(eng_path, ben_path):
    print("====================================================================")
    print("COMPREHENSIVE OFFLINE VALIDATION: BANGLABBQ RELIGION BENCHMARK")
    print("====================================================================")
    print(f"Loading datasets:\n  ENG: {eng_path}\n  BEN: {ben_path}")

    failures = []

    with open(eng_path, 'r', encoding='utf-8') as f:
        eng_recs = [json.loads(line) for line in f]
    with open(ben_path, 'r', encoding='utf-8') as f:
        ben_recs = [json.loads(line) for line in f]

    # 1. Total Record Counts: V1 standalone or V1+V2+V3 append-only expansion
    print("\n--- Check 1: Record Counts ---")
    n = len(eng_recs)
    if n not in (960, 2880) or len(ben_recs) != n:
        print(f"  FAIL: ENG={len(eng_recs)} BEN={len(ben_recs)}; expected equal 960 or 2880")
        return False
    print(f"  ENG count: {n} (PASS)")
    print(f"  BEN count: {len(ben_recs)} (PASS)")
    per_theme = n // 20
    per_label = n // 3
    per_condition = per_theme // 2

    # 2. Sequential IDs & 15-Column Schema Integrity
    print("\n--- Check 2: Sequential IDs & 15-Column Schema ---")
    req_fields = [
        'example_id', 'question_index', 'context_condition', 'question_polarity',
        'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
        'answer_info', 'additional_metadata', 'category', 'id'
    ]
    id_errors = 0
    schema_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        if e.get('id') != i or e.get('example_id') != i:
            id_errors += 1
        if b.get('id') != i or b.get('example_id') != i:
            id_errors += 1
        if list(e.keys()) != req_fields or list(b.keys()) != req_fields:
            schema_errors += 1
    if id_errors > 0:
        failures.append(f"Found {id_errors} ID sequencing errors")
    if schema_errors > 0:
        failures.append(f"Found {schema_errors} schema ordering errors")
    print(f"  Sequential IDs (0-{n-1}): {'PASS' if id_errors == 0 else f'FAIL ({id_errors} errors)'}")
    print(f"  15-Column Schema Integrity: {'PASS' if schema_errors == 0 else f'FAIL ({schema_errors} errors)'}")

    # 3. Theme Counts & Condition Balances
    print(f"\n--- Check 3: Theme Counts & Condition Balances ({per_theme} per theme) ---")
    theme_errors = 0
    for q in range(1, 21):
        q_eng = [r for r in eng_recs if r['question_index'] == q]
        q_ben = [r for r in ben_recs if r['question_index'] == q]
        if len(q_eng) != per_theme or len(q_ben) != per_theme:
            theme_errors += 1
        ambig_e = sum(1 for r in q_eng if r['context_condition'] == 'ambig')
        disambig_e = sum(1 for r in q_eng if r['context_condition'] == 'disambig')
        neg_e = sum(1 for r in q_eng if r['question_polarity'] == 'neg')
        nonneg_e = sum(1 for r in q_eng if r['question_polarity'] == 'nonneg')
        if ambig_e != per_condition or disambig_e != per_condition or neg_e != per_condition or nonneg_e != per_condition:
            theme_errors += 1
    if theme_errors > 0:
        failures.append(f"Found {theme_errors} theme balance errors")
    print(f"  All 20 Themes {per_theme} records with {per_condition}/{per_condition} balance: {'PASS' if theme_errors == 0 else 'FAIL'}")

    # 4. Canonical 4-row Block Structure
    print("\n--- Check 4: Canonical 4-row Block Ordering ---")
    order_errors = 0
    expected_order = [
        ('ambig', 'neg'),
        ('disambig', 'neg'),
        ('ambig', 'nonneg'),
        ('disambig', 'nonneg')
    ]
    for i in range(len(eng_recs)):
        exp_cond, exp_pol = expected_order[i % 4]
        e = eng_recs[i]
        b = ben_recs[i]
        if e['context_condition'] != exp_cond or e['question_polarity'] != exp_pol:
            order_errors += 1
        if b['context_condition'] != exp_cond or b['question_polarity'] != exp_pol:
            order_errors += 1
    if order_errors > 0:
        failures.append(f"Found {order_errors} block ordering violations")
    print(f"  Canonical 4-row BBQ Block Sequence throughout all {n} rows: {'PASS' if order_errors == 0 else f'FAIL ({order_errors})'}")

    # 5. Label Distribution
    print("\n--- Check 5: Label Distribution ---")
    e_labels = Counter(r['label'] for r in eng_recs)
    b_labels = Counter(r['label'] for r in ben_recs)
    label_balanced = all(e_labels[k] == per_label and b_labels[k] == per_label for k in (0, 1, 2))
    if not label_balanced:
        failures.append(f"Unbalanced labels: ENG={e_labels}, BEN={b_labels}")
    print(f"  Uniform Label Distribution ({per_label}/{per_label}/{per_label}): {'PASS' if label_balanced else 'FAIL'}")

    # 6. Six Answer Permutations Per Condition x Polarity x Orientation
    print("\n--- Check 6: Six Answer Permutations (3!) per Condition & Orientation ---")
    perm_errors = 0
    for q in range(1, 21):
        q_recs = [r for r in eng_recs if r['question_index'] == q]
        groups = {(r['additional_metadata'].get('wording_variant', 'v1'),
                   r['additional_metadata'].get('version')) for r in q_recs}
        for wording_variant, v in groups:
            v_recs = [r for r in q_recs if
                      r['additional_metadata'].get('wording_variant', 'v1') == wording_variant and
                      r['additional_metadata'].get('version') == v]
            for cond in ['ambig', 'disambig']:
                for pol in ['neg', 'nonneg']:
                    sub = [r for r in v_recs if r['context_condition'] == cond and r['question_polarity'] == pol]
                    if len(sub) != 6:
                        perm_errors += 1
                    # Ensure all 6 permutations of (ans0, ans1, ans2) are distinct
                    ans_perms = set((r['ans0'], r['ans1'], r['ans2']) for r in sub)
                    if len(ans_perms) != 6:
                        perm_errors += 1
    if perm_errors > 0:
        failures.append(f"Found {perm_errors} permutation coverage errors")
    print(f"  Full 6-way Answer Permutations (3!) across all sub-blocks: {'PASS' if perm_errors == 0 else f'FAIL ({perm_errors})'}")

    # 7. Ambiguous Gold-Label Invariant
    print("\n--- Check 7: Ambiguous Context Invariant (Must Target Unknown/অজানা) ---")
    ambig_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        if e['context_condition'] == 'ambig':
            lbl_e = e['label']
            lbl_b = b['label']
            if e[f'ans{lbl_e}'] != 'Unknown' or e['answer_info'][f'ans{lbl_e}'][1] != 'unknown':
                ambig_errors += 1
            if b[f'ans{lbl_b}'] != 'অজানা' or b['answer_info'][f'ans{lbl_b}'][1] != 'unknown':
                ambig_errors += 1
    if ambig_errors > 0:
        failures.append(f"Found {ambig_errors} ambiguous gold-label errors")
    print(f"  All {n//2} Ambiguous QA pairs correctly target Unknown/অজানা: {'PASS' if ambig_errors == 0 else f'FAIL ({ambig_errors})'}")

    # 8. Disambiguated Context Invariant (Must Target Contextually Non-Unknown Entity)
    print("\n--- Check 8: Disambiguated Context Grounding ---")
    disambig_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        if e['context_condition'] == 'disambig':
            lbl_e = e['label']
            lbl_b = b['label']
            if e[f'ans{lbl_e}'] == 'Unknown' or e['answer_info'][f'ans{lbl_e}'][1] == 'unknown':
                disambig_errors += 1
            if b[f'ans{lbl_b}'] == 'অজানা' or b['answer_info'][f'ans{lbl_b}'][1] == 'unknown':
                disambig_errors += 1
    if disambig_errors > 0:
        failures.append(f"Found {disambig_errors} disambiguated context grounding errors")
    print(f"  All {n//2} Disambiguated QA pairs target named entities (semantic entailment needs human review): {'PASS' if disambig_errors == 0 else f'FAIL ({disambig_errors})'}")

    # 9. Bilingual Structural Equality & Metadata Parity
    print("\n--- Check 9: Bilingual Structural Equality & Metadata Parity ---")
    bilingual_errors = 0
    shared_keys = [
        'example_id', 'question_index', 'context_condition', 'question_polarity',
        'type', 'label', 'answer_info', 'additional_metadata', 'category', 'id'
    ]
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        for k in shared_keys:
            if e[k] != b[k]:
                bilingual_errors += 1
                if bilingual_errors <= 3:
                    print(f"    Mismatch at row {i}, key '{k}': ENG={e[k]} vs BEN={b[k]}")
    if bilingual_errors > 0:
        failures.append(f"Found {bilingual_errors} bilingual field mismatches")
    print(f"  100% Bilingual Equality across all 10 structural/metadata fields: {'PASS' if bilingual_errors == 0 else f'FAIL ({bilingual_errors})'}")

    # 10. Duplicate QA Records Check
    print("\n--- Check 10: Duplicate QA Records Check ---")
    eng_tuples = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in eng_recs]
    ben_tuples = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in ben_recs]
    dup_e = len(eng_tuples) - len(set(eng_tuples))
    dup_b = len(ben_tuples) - len(set(ben_tuples))
    if dup_e > 0 or dup_b > 0:
        failures.append(f"Duplicate QA records found: ENG={dup_e}, BEN={dup_b}")
    print(f"  Zero Duplicate QA Records ({n}/{n} unique tuples): {'PASS' if (dup_e == 0 and dup_b == 0) else 'FAIL'}")

    print("\n====================================================================")
    if failures:
        print(f"VALIDATION FAILED with {len(failures)} issues:")
        for f in failures:
            print(f"  - {f}")
        return False
    else:
        print("ALL 10 RELIGION STRUCTURAL INVARIANT CHECKS PASSED (NOT SOURCE/LINGUISTIC CERTIFICATION)")
        print("====================================================================")
        return True

if __name__ == '__main__':
    eng_p = sys.argv[1] if len(sys.argv) > 1 else 'BanglaBBQ_Religion/Religion_eng.jsonl'
    ben_p = sys.argv[2] if len(sys.argv) > 2 else 'BanglaBBQ_Religion/Religion_bng.jsonl'
    success = validate_religion_dataset(eng_p, ben_p)
    sys.exit(0 if success else 1)
