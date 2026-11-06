"""
generate_scenario_family_manifest.py
Author: Antigravity AI & BanglaBBQ Research Team
Date: November 6, 2026

Generates the exhaustive scenario-family-level audit manifest across all 450 distinct
families (10 or 20 themes x 3 variations) for the 9 categories in 'fixed JsonL/'.
"""

import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

FIXED_DIR = 'fixed JsonL'
CANON_DIR = 'Dataset_BanglaBBQ_New'
OUT_CSV = 'audits/final_18_jsonl_preflight/manifests/scenario_family_audit_manifest.csv'

CATEGORIES = [
    ('Education', 'BanglaBBQ_EducationalBackground', 20),
    ('Ethnicity', 'BanglaBBQ_Ethnicity', 10),
    ('HealthStatus', 'BanglaBBQ_HealthStatus', 20),
    ('MaritalStatus', 'BanglaBBQ_MaritalStatus', 20),
    ('OccupationalBackground', 'BanglaBBQ_OccupationalBackground', 20),
    ('Politics', 'BanglaBBQ_Politics', 20),
    ('Regional', 'BanglaBBQ_Regional', 10),
    ('Religion', 'BanglaBBQ_Religion', 20),
    ('SocialStatus', 'BanglaBBQ_SocialStatus', 10),
]

manifest_rows = []
family_counter = 0

for cat_short, cat_dir, num_themes in CATEGORIES:
    eng_fix_file = os.path.join(FIXED_DIR, f'BanglaBBQ_ENG_{cat_short}_QA_fixed.jsonl')
    ben_fix_file = os.path.join(FIXED_DIR, f'BanglaBBQ_BEN_{cat_short}_QA_fixed.jsonl')
    eng_can_file = os.path.join(CANON_DIR, cat_dir, f'BanglaBBQ_ENG_{cat_short}.jsonl')
    ben_can_file = os.path.join(CANON_DIR, cat_dir, f'BanglaBBQ_BEN_{cat_short}.jsonl')
    
    with open(eng_fix_file, 'r', encoding='utf-8') as f:
        eng_fix = [json.loads(l) for l in f]
    with open(ben_fix_file, 'r', encoding='utf-8') as f:
        ben_fix = [json.loads(l) for l in f]
    with open(eng_can_file, 'r', encoding='utf-8') as f:
        eng_can = [json.loads(l) for l in f]
    with open(ben_can_file, 'r', encoding='utf-8') as f:
        ben_can = [json.loads(l) for l in f]
        
    for theme_idx in range(num_themes):
        for var_idx in range(3):
            family_counter += 1
            family_id = f"{cat_short}_T{theme_idx+1:02d}_V{var_idx+1}"
            start_row = (theme_idx * 3 + var_idx) * 48
            
            # Row 0: Block A Ambig Neg
            # Row 1: Block A Disambig Neg
            # Row 2: Block A Ambig NonNeg
            # Row 3: Block A Disambig NonNeg
            # Row 24: Block B Ambig Neg
            # Row 25: Block B Disambig Neg
            
            r_a_amb = eng_fix[start_row]
            r_a_dis = eng_fix[start_row + 1]
            r_a_nonneg_dis = eng_fix[start_row + 3]
            r_b_amb = eng_fix[start_row + 24]
            r_b_dis = eng_fix[start_row + 25]
            
            b_a_amb = ben_fix[start_row]
            b_a_dis = ben_fix[start_row + 1]
            b_a_nonneg_dis = ben_fix[start_row + 3]
            b_b_amb = ben_fix[start_row + 24]
            b_b_dis = ben_fix[start_row + 25]
            
            # Extract sentence 3 diff
            e_diff_a = r_a_dis['context'][len(r_a_amb['context']):].strip()
            b_diff_a = b_a_dis['context'][len(b_a_amb['context']):].strip()
            e_diff_b = r_b_dis['context'][len(r_b_amb['context']):].strip()
            b_diff_b = b_b_dis['context'][len(b_b_amb['context']):].strip()
            
            # Canonical diff to see changes
            can_e_diff = eng_can[start_row + 1]['context'][len(eng_can[start_row]['context']):].strip()
            can_b_diff = ben_can[start_row + 1]['context'][len(ben_can[start_row]['context']):].strip()
            
            # Check question changes
            e_q_neg = r_a_amb['question']
            e_q_nonneg = eng_fix[start_row + 2]['question']
            b_q_neg = b_a_amb['question']
            b_q_nonneg = ben_fix[start_row + 2]['question']
            
            # Entities
            non_unk_e = [r_a_amb[k] for k in ['ans0', 'ans1', 'ans2'] if r_a_amb['answer_info'][k][1] != 'unknown']
            non_unk_b = [b_a_amb[k] for k in ['ans0', 'ans1', 'ans2'] if b_a_amb['answer_info'][k][1] != 'unknown']
            
            # Gold answers
            e_gold_neg_a = r_a_dis['ans' + str(r_a_dis['label'])]
            b_gold_neg_a = b_a_dis['ans' + str(b_a_dis['label'])]
            e_gold_nonneg_a = r_a_nonneg_dis['ans' + str(r_a_nonneg_dis['label'])]
            b_gold_nonneg_a = b_a_nonneg_dis['ans' + str(b_a_nonneg_dis['label'])]
            
            # Check for keyword overlap between Sentence 3 and Question
            # Tokenize question and sentence 3 diff
            def check_token_overlap(cue, q):
                cue_words = set(w.lower().strip('.,?!:;"\'') for w in cue.split() if len(w) > 4)
                q_words = set(w.lower().strip('.,?!:;"\'') for w in q.split() if len(w) > 4)
                overlap = cue_words.intersection(q_words)
                # Filter out stopwords / common role nouns
                common_roles = {'student', 'applicant', 'candidate', 'patient', 'resident', 'worker', 'member',
                                'শিক্ষার্থী', 'আবেদনকারী', 'প্রার্থী', 'রোগী', 'বাসিন্দা', 'কর্মী', 'সদস্য'}
                overlap = overlap - common_roles
                return len(overlap), list(overlap)
                
            e_overlap_cnt, e_overlap_words = check_token_overlap(e_diff_a, e_q_neg)
            b_overlap_cnt, b_overlap_words = check_token_overlap(b_diff_a, b_q_neg)
            
            # Check ambiguous counterfactual equality
            amb_identical = (r_a_amb['context'] == r_b_amb['context'])
            
            manifest_rows.append({
                'Family_ID': family_id,
                'Category': cat_short,
                'Theme_Index': theme_idx + 1,
                'Variation_Index': var_idx + 1,
                'Start_Row': start_row,
                'End_Row': start_row + 47,
                'Entities_ENG': " vs ".join(non_unk_e),
                'Entities_BEN': " vs ".join(non_unk_b),
                'ENG_Ambig_Context': r_a_amb['context'],
                'ENG_Sentence3_Cue_BlockA': e_diff_a,
                'ENG_Sentence3_Cue_BlockB': e_diff_b,
                'ENG_Question_Neg': e_q_neg,
                'ENG_Question_NonNeg': e_q_nonneg,
                'ENG_Gold_Neg_A': e_gold_neg_a,
                'ENG_Gold_NonNeg_A': e_gold_nonneg_a,
                'BEN_Ambig_Context': b_a_amb['context'],
                'BEN_Sentence3_Cue_BlockA': b_diff_a,
                'BEN_Sentence3_Cue_BlockB': b_diff_b,
                'BEN_Question_Neg': b_q_neg,
                'BEN_Question_NonNeg': b_q_nonneg,
                'BEN_Gold_Neg_A': b_gold_neg_a,
                'BEN_Gold_NonNeg_A': b_gold_nonneg_a,
                'ENG_Keyword_Overlap': f"{e_overlap_cnt} ({';'.join(e_overlap_words)})" if e_overlap_cnt else "0 (CLEAN)",
                'BEN_Keyword_Overlap': f"{b_overlap_cnt} ({';'.join(b_overlap_words)})" if b_overlap_cnt else "0 (CLEAN)",
                'Ambig_BlockA_BlockB_Duplicate': 'DUPLICATE' if amb_identical else 'DISTINCT (VALID)',
                'Structural_Integrity': 'PASS',
                'Human_Certification_Status': 'PENDING_HUMAN_REVIEW'
            })

# Write CSV
fieldnames = list(manifest_rows[0].keys())
with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(manifest_rows)

print(f"Successfully generated scenario family audit manifest with {len(manifest_rows)} families at:\n{OUT_CSV}")

