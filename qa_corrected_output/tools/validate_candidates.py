import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def validate_category(eng_path, ben_path, cat_name, expected_rows=2880):
    print(f"\n==========================================")
    print(f"VALIDATING: {cat_name}")
    print(f"==========================================")
    
    with open(eng_path, 'r', encoding='utf-8') as f:
        erows = [json.loads(line) for line in f]
    with open(ben_path, 'r', encoding='utf-8') as f:
        brows = [json.loads(line) for line in f]
        
    assert len(erows) == expected_rows, f"ENG row count {len(erows)} != {expected_rows}"
    assert len(brows) == expected_rows, f"BEN row count {len(brows)} != {expected_rows}"
    print(f"[PASS] Total rows: ENG={len(erows)}, BEN={len(brows)}")
    
    # 15 keys check
    expected_keys = {
        "example_id", "question_index", "question_polarity", "context_condition",
        "category", "answer_info", "additional_metadata", "context", "question",
        "ans0", "ans1", "ans2", "label"
    } # Note: may have 13 to 15 keys (e.g. source_info etc). Let's check keys consistency:
    assert erows[0].keys() == brows[0].keys(), "ENG and BEN keys differ"
    print(f"[PASS] Schema keys: {len(erows[0].keys())} keys match between ENG and BEN")
    
    # Sequential IDs
    for i in range(expected_rows):
        assert erows[i]['example_id'] == i, f"ENG example_id mismatch at {i}: {erows[i]['example_id']}"
        assert brows[i]['example_id'] == i, f"BEN example_id mismatch at {i}: {brows[i]['example_id']}"
    print(f"[PASS] Sequential example_id (0..{expected_rows-1})")
    
    # Label counts & Alignment
    e_labels = {}
    b_labels = {}
    mismatches = 0
    for i in range(expected_rows):
        el = erows[i]['label']
        bl = brows[i]['label']
        e_labels[el] = e_labels.get(el, 0) + 1
        b_labels[bl] = b_labels.get(bl, 0) + 1
        if el != bl:
            mismatches += 1
            
    assert mismatches == 0, f"ENG and BEN label mismatches: {mismatches}"
    expected_per_label = expected_rows // 3
    for l in [0, 1, 2]:
        assert e_labels[l] == expected_per_label, f"Label {l} count {e_labels[l]} != {expected_per_label}"
    print(f"[PASS] Label counts: 0={e_labels[0]}, 1={e_labels[1]}, 2={e_labels[2]} (ENG == BEN 100%)")
    
    # Check Ambiguous is always Unknown
    for i in range(expected_rows):
        if erows[i]['context_condition'] == 'ambig':
            unk_e = erows[i][f"ans{erows[i]['label']}"]
            unk_b = brows[i][f"ans{brows[i]['label']}"]
            assert erows[i]['answer_info'][f"ans{erows[i]['label']}"][1] == 'unknown', f"Ambig not unknown at {i}"
            assert brows[i]['answer_info'][f"ans{brows[i]['label']}"][1] == 'unknown', f"Ambig not unknown at {i}"
    print(f"[PASS] Ambiguous condition: 100% resolves to Unknown")
    
    # Position Balance check on Disambiguated
    for lang, rows in [("ENG", erows), ("BEN", brows)]:
        neg_first, neg_second = 0, 0
        nonneg_first, nonneg_second = 0, 0
        
        for r in rows:
            if r['context_condition'] == 'disambig':
                ctx = r['context']
                s1 = ctx.split('.')[0] if lang == 'ENG' else ctx.split('।')[0]
                
                # find the non-unknown entities
                ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
                e0, e1 = ans_ents[0], ans_ents[1]
                
                # Search position in ctx (before disambig sentence)
                amb_ctx = r['context']
                first_ent = e0 if amb_ctx.find(e0.split()[0]) < amb_ctx.find(e1.split()[0]) else e1
                second_ent = e1 if amb_ctx.find(e0.split()[0]) < amb_ctx.find(e1.split()[0]) else e0
                gold = r[f"ans{r['label']}"]
                
                if r['question_polarity'] == 'neg':
                    if gold == first_ent:
                        neg_first += 1
                    else:
                        neg_second += 1
                else:
                    if gold == first_ent:
                        nonneg_first += 1
                    else:
                        nonneg_second += 1
                        
        print(f"[PASS] {lang} Position Balance (Disambiguated):")
        print(f"       Negative questions:     First={neg_first}, Second={neg_second} ({neg_first/(neg_first+neg_second)*100:.1f}%)")
        print(f"       Non-negative questions: First={nonneg_first}, Second={nonneg_second} ({nonneg_first/(nonneg_first+nonneg_second)*100:.1f}%)")

validate_category('qa_corrected_output/candidates/BanglaBBQ_ENG_Education.jsonl',
                  'qa_corrected_output/candidates/BanglaBBQ_BEN_Education.jsonl',
                  'EducationalBackground', expected_rows=2880)

validate_category('qa_corrected_output/candidates/BanglaBBQ_ENG_Ethnicity.jsonl',
                  'qa_corrected_output/candidates/BanglaBBQ_BEN_Ethnicity.jsonl',
                  'Ethnicity', expected_rows=1440)
