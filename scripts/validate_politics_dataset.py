import json
import hashlib
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def validate_dataset(eng_path, ben_path):
    print("====================================================================")
    print("COMPREHENSIVE OFFLINE VALIDATION: BANGLABBQ POLITICS BENCHMARK")
    print("====================================================================")
    print(f"Loading datasets:\n  ENG: {eng_path}\n  BEN: {ben_path}")
    
    with open(eng_path, 'r', encoding='utf-8') as f:
        eng_recs = [json.loads(line) for line in f]
    with open(ben_path, 'r', encoding='utf-8') as f:
        ben_recs = [json.loads(line) for line in f]
        
    failures = []
    expected_count = 2880 if max(len(eng_recs), len(ben_recs)) > 960 else 960
    per_theme = expected_count // 20
    half_theme = per_theme // 2
    
    # 1. Total Record Counts
    print("\n--- Check 1: Record Counts ---")
    if len(eng_recs) != expected_count:
        failures.append(f"ENG records count = {len(eng_recs)}, expected {expected_count}")
    if len(ben_recs) != expected_count:
        failures.append(f"BEN records count = {len(ben_recs)}, expected {expected_count}")
    print(f"  ENG count: {len(eng_recs)} (PASS)" if len(eng_recs) == expected_count else f"  ENG count: FAIL ({len(eng_recs)})")
    print(f"  BEN count: {len(ben_recs)} (PASS)" if len(ben_recs) == expected_count else f"  BEN count: FAIL ({len(ben_recs)})")

    # 2. Sequential IDs & Schema
    print("\n--- Check 2: Sequential IDs & Schema ---")
    req_fields = ['example_id', 'question_index', 'context_condition', 'question_polarity', 
                  'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label', 
                  'answer_info', 'additional_metadata', 'category', 'id']
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
    print(f"  Sequential IDs (0-{expected_count - 1}): {'PASS' if id_errors == 0 else f'FAIL ({id_errors} errors)'}")
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
        if ambig_e != half_theme or disambig_e != half_theme or neg_e != half_theme or nonneg_e != half_theme:
            theme_errors += 1
    if theme_errors > 0:
        failures.append(f"Found {theme_errors} theme balance errors")
    print(f"  All 20 Themes {per_theme} records with {half_theme}/{half_theme} condition & polarity balances: {'PASS' if theme_errors == 0 else 'FAIL'}")

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
    print(f"  Canonical 4-row BBQ Block Sequence throughout all expected rows: {'PASS' if order_errors == 0 else f'FAIL ({order_errors})'}")

    # 5. Label Distribution & Permutations
    print("\n--- Check 5: Label Distribution & Permutations ---")
    e_labels = Counter(r['label'] for r in eng_recs)
    b_labels = Counter(r['label'] for r in ben_recs)
    label_balanced = (e_labels[0] == expected_count // 3 and e_labels[1] == expected_count // 3 and e_labels[2] == expected_count // 3 and
                      b_labels[0] == expected_count // 3 and b_labels[1] == expected_count // 3 and b_labels[2] == expected_count // 3)
    if not label_balanced:
        failures.append(f"Unbalanced labels: ENG={e_labels}, BEN={b_labels}")
    print(f"  Uniform Label Distribution ({expected_count // 3} each): {'PASS' if label_balanced else 'FAIL'}")

    # 6. Ambiguous Gold-Label Invariant
    print("\n--- Check 6: Ambiguous Context Invariant (Must be Unknown) ---")
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
    print(f"  All expected Ambiguous QA pairs correctly target Unknown/অজানা: {'PASS' if ambig_errors == 0 else f'FAIL ({ambig_errors})'}")

    # 7. Disambiguated Semantic Ground Truth & Counterfactual Inversion
    print("\n--- Check 7: Disambiguated Semantic Ground Truth & Counterfactual Inversion ---")
    disambig_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        if e['context_condition'] == 'disambig':
            q_idx = e['question_index']
            offset_in_theme = i % 48
            is_first_orientation = (offset_in_theme < 24)
            pol = e['question_polarity']
            lbl_e = e['label']
            lbl_b = b['label']
            
            # Ground truth determination based on theme-specific counterfactual specification:
            if q_idx <= 5:
                # Q1-Q5: Orientation 1 (rows 0-23) has neg -> nonOpposition, nonneg -> Opposition
                # Orientation 2 (rows 24-47) has neg -> Opposition, nonneg -> nonOpposition
                if is_first_orientation:
                    exp_target = 'nonOpposition' if pol == 'neg' else 'Opposition'
                else:
                    exp_target = 'Opposition' if pol == 'neg' else 'nonOpposition'
            else:
                # Q6-Q20: Orientation 1 (rows 0-23, ver a) has neg -> Opposition, nonneg -> nonOpposition
                # Orientation 2 (rows 24-47, ver b) has neg -> nonOpposition, nonneg -> Opposition
                if is_first_orientation:
                    exp_target = 'Opposition' if pol == 'neg' else 'nonOpposition'
                else:
                    exp_target = 'nonOpposition' if pol == 'neg' else 'Opposition'
                
            e_actual_target = e['answer_info'][f'ans{lbl_e}'][1]
            b_actual_target = b['answer_info'][f'ans{lbl_b}'][1]
            
            if e_actual_target != exp_target:
                disambig_errors += 1
            if b_actual_target != exp_target:
                disambig_errors += 1
    if disambig_errors > 0:
        failures.append(f"Found {disambig_errors} disambiguated semantic ground truth errors")
    print(f"  All expected Disambiguated QA pairs logically proven by contextual ground truth: {'PASS' if disambig_errors == 0 else f'FAIL ({disambig_errors})'}")

    # 8. Bilingual Structural Equality & Metadata Parity
    print("\n--- Check 8: Bilingual Structural Equality & Metadata Parity ---")
    bilingual_errors = 0
    shared_keys = ['example_id', 'question_index', 'context_condition', 'question_polarity', 
                   'type', 'label', 'answer_info', 'additional_metadata', 'category', 'id']
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

    # 9. Duplicate QA Records Check
    print("\n--- Check 9: Duplicate QA Records Check ---")
    eng_tuples = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in eng_recs]
    ben_tuples = [(r['context'], r['question'], r['ans0'], r['ans1'], r['ans2']) for r in ben_recs]
    dup_e = len(eng_tuples) - len(set(eng_tuples))
    dup_b = len(ben_tuples) - len(set(ben_tuples))
    if dup_e > 0 or dup_b > 0:
        failures.append(f"Duplicate QA records found: ENG={dup_e}, BEN={dup_b}")
    print(f"  Zero Duplicate QA Records ({expected_count}/{expected_count} completely unique tuples): {'PASS' if (dup_e == 0 and dup_b == 0) else 'FAIL'}")

    # 10. Q1-Q5 Hash Preservation against Baseline / Approved Repair
    print("\n--- Check 10: Q1-Q5 Hash Preservation ---")
    q1_q5_eng_hash = hashlib.sha256(json.dumps(eng_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()
    q1_q5_ben_hash = hashlib.sha256(json.dumps(ben_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()
    
    # Preserved historical baseline hashes (evidence from pre-repair Phase A audit)
    HISTORICAL_ENG_HASH = "2ab59aec0cb6f6ce42f60e8912c861373b96008db8dec2af281046def64595b3"
    HISTORICAL_BEN_HASH = "eb6ae51a7b0d4d739243c995e23e5e7a6a55dc895c4a791975dbb18c50d4fc23"

    # Approved post-repair hashes (Q5 historical year 2022 qualification applied)
    POST_REPAIR_ENG_HASH = "7390c9ed9d008dc2c0e937ecab545e9d2521fbdb8b44b0adab2b9d218180c51a"
    POST_REPAIR_BEN_HASH = "e30d2b1d8085f6f01ed95e12548ea466aac8cef6317b8c0a678fe4c10c32eda6"

    valid_eng_hashes = {HISTORICAL_ENG_HASH, POST_REPAIR_ENG_HASH}
    valid_ben_hashes = {HISTORICAL_BEN_HASH, POST_REPAIR_BEN_HASH}

    eng_match = q1_q5_eng_hash in valid_eng_hashes
    ben_match = q1_q5_ben_hash in valid_ben_hashes
    if not (eng_match and ben_match):
        failures.append(f"Q1-Q5 hashes do not match historical baseline or approved repair: ENG={q1_q5_eng_hash}, BEN={q1_q5_ben_hash}")
    eng_status = "Historical Baseline" if q1_q5_eng_hash == HISTORICAL_ENG_HASH else ("Approved Post-Q5 Repair" if q1_q5_eng_hash == POST_REPAIR_ENG_HASH else "UNKNOWN")
    ben_status = "Historical Baseline" if q1_q5_ben_hash == HISTORICAL_BEN_HASH else ("Approved Post-Q5 Repair" if q1_q5_ben_hash == POST_REPAIR_BEN_HASH else "UNKNOWN")
    print(f"  Q1-Q5 ENG SHA-256: {q1_q5_eng_hash} ({'PASS - ' + eng_status if eng_match else 'FAIL'})")
    print(f"  Q1-Q5 BEN SHA-256: {q1_q5_ben_hash} ({'PASS - ' + ben_status if ben_match else 'FAIL'})")

    # 11. Wording variant lineage, 48-row blocks, permutations, and identity preservation
    print("\n--- Check 11: V2/V3 Wording Expansion Audit ---")
    expansion_errors = 0
    if expected_count == 2880:
        for lang, records in (("ENG", eng_recs), ("BEN", ben_recs)):
            for q in range(1, 21):
                for variant_offset, variant_name in enumerate(("v2", "v3")):
                    start = 960 + (q - 1) * 96 + variant_offset * 48
                    block = records[start : start + 48]
                    if len(block) != 48 or any(row["question_index"] != q for row in block):
                        expansion_errors += 1
                        continue
                    if len(set(row["context"] for row in block)) != 4:
                        expansion_errors += 1
                    for offset, row in enumerate(block):
                        parent = (q - 1) * 48 + offset
                        source = records[parent]
                        metadata = row["additional_metadata"]
                        if (metadata.get("wording_variant") != variant_name
                                or metadata.get("parent_example_id") != parent):
                            expansion_errors += 1
                        inherited_meta = {k: v for k, v in metadata.items()
                                          if k not in ("wording_variant", "parent_example_id")}
                        if inherited_meta != source["additional_metadata"]:
                            expansion_errors += 1
                        for key in ("question_index", "context_condition", "question_polarity",
                                    "type", "question", "ans0", "ans1", "ans2",
                                    "label", "answer_info", "category"):
                            if row[key] != source[key]:
                                expansion_errors += 1
                    for direction in (0, 1):
                        side = block[direction * 24 : (direction + 1) * 24]
                        ambig = set(r["context"] for r in side
                                    if r["context_condition"] == "ambig")
                        disambig = set(r["context"] for r in side
                                       if r["context_condition"] == "disambig")
                        if len(ambig) != 1 or len(disambig) != 1:
                            expansion_errors += 1
                        elif not next(iter(disambig)).startswith(next(iter(ambig))):
                            expansion_errors += 1
                        for condition in ("ambig", "disambig"):
                            for polarity in ("neg", "nonneg"):
                                six = [r for r in side
                                       if r["context_condition"] == condition
                                       and r["question_polarity"] == polarity]
                                permutations = set((r["ans0"], r["ans1"], r["ans2"])
                                                   for r in six)
                                if len(six) != 6 or len(permutations) != 6:
                                    expansion_errors += 1
        if expansion_errors:
            failures.append(f"V2/V3 expansion has {expansion_errors} provenance or permutation issues")
        print(f"  40 x 48-row bilingual variants, metadata lineage, and 6-way permutations: {'PASS' if expansion_errors == 0 else 'FAIL'}")
    else:
        print("  Legacy 960-row dataset: additional variants not applicable")

    print("\n====================================================================")
    if failures:
        print(f"VALIDATION FAILED with {len(failures)} issues:")
        for f in failures:
            print(f"  - {f}")
        return False
    else:
        print("ALL COMPREHENSIVE BENCHMARK INVARIANT CHECKS PASSED!")
        print("====================================================================")
        return True

if __name__ == '__main__':
    eng_p = sys.argv[1] if len(sys.argv) > 1 else 'Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl'
    ben_p = sys.argv[2] if len(sys.argv) > 2 else 'Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl'
    success = validate_dataset(eng_p, ben_p)
    sys.exit(0 if success else 1)
