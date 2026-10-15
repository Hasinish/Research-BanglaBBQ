import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    recs = [json.loads(line) for line in f]

for q in range(1, 21):
    q_recs = [r for r in recs if r['question_index'] == q and r['context_condition'] == 'disambig']
    rec_a_neg = [r for r in q_recs if r['additional_metadata']['version'] == 'a' and r['question_polarity'] == 'neg'][0]
    rec_b_neg = [r for r in q_recs if r['additional_metadata']['version'] == 'b' and r['question_polarity'] == 'neg'][0]
    rec_a_nonneg = [r for r in q_recs if r['additional_metadata']['version'] == 'a' and r['question_polarity'] == 'nonneg'][0]
    rec_b_nonneg = [r for r in q_recs if r['additional_metadata']['version'] == 'b' and r['question_polarity'] == 'nonneg'][0]
    
    lbl_a_neg = rec_a_neg['label']
    cat_a_neg = rec_a_neg['answer_info'][f'ans{lbl_a_neg}'][1]
    
    lbl_b_neg = rec_b_neg['label']
    cat_b_neg = rec_b_neg['answer_info'][f'ans{lbl_b_neg}'][1]

    lbl_a_nonneg = rec_a_nonneg['label']
    cat_a_nonneg = rec_a_nonneg['answer_info'][f'ans{lbl_a_nonneg}'][1]

    lbl_b_nonneg = rec_b_nonneg['label']
    cat_b_nonneg = rec_b_nonneg['answer_info'][f'ans{lbl_b_nonneg}'][1]

    print(f"Theme Q{q:02d}:")
    print(f"  Version a: neg -> {cat_a_neg:15s} | nonneg -> {cat_a_nonneg:15s}")
    print(f"  Version b: neg -> {cat_b_neg:15s} | nonneg -> {cat_b_nonneg:15s}")
    
    # Check that within version a, neg and nonneg are complementary
    assert cat_a_neg != cat_a_nonneg, f"Q{q} ver a: neg and nonneg point to same category!"
    # Check that within version b, neg and nonneg are complementary
    assert cat_b_neg != cat_b_nonneg, f"Q{q} ver b: neg and nonneg point to same category!"
    # Check that version b is the exact counterfactual inversion of version a
    assert cat_a_neg == cat_b_nonneg, f"Q{q}: counterfactual inversion failed between a and b!"
    assert cat_a_nonneg == cat_b_neg, f"Q{q}: counterfactual inversion failed between a and b!"
print("\nAll 20 themes have 100% PERFECT complementary polarity and counterfactual inversion!")
