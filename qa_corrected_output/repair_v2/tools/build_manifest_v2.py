"""
build_manifest_v2.py
Author: Antigravity AI & BanglaBBQ QA Team
Date: November 3, 2026

Generates qa_corrected_output/repair_v2/CHANGE_MANIFEST.json with complete cryptographic SHA-256 hashes,
field modification metrics, file mappings, and category validation verdicts.
"""

import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

FIXED_DIR = 'fixed JsonL'
CAND_DIR = 'qa_corrected_output/repair_v2/candidates'
CANON_DIR = 'Dataset_BanglaBBQ_New'
OUT_MANIFEST = 'qa_corrected_output/repair_v2/CHANGE_MANIFEST.json'

CATEGORY_MAP = [
    ('Education', 'BanglaBBQ_EducationalBackground', 2880, 'BLOCKED / PENDING METHODOLOGICAL APPROVAL'),
    ('Ethnicity', 'BanglaBBQ_Ethnicity', 1440, 'APPROVED (CANDIDATE REPAIRED)'),
    ('HealthStatus', 'BanglaBBQ_HealthStatus', 2880, 'APPROVED'),
    ('MaritalStatus', 'BanglaBBQ_MaritalStatus', 2880, 'APPROVED'),
    ('OccupationalBackground', 'BanglaBBQ_OccupationalBackground', 2880, 'APPROVED'),
    ('Politics', 'BanglaBBQ_Politics', 2880, 'APPROVED'),
    ('Regional', 'BanglaBBQ_Regional', 1440, 'APPROVED'),
    ('Religion', 'BanglaBBQ_Religion', 2880, 'BLOCKED PENDING THESIS REVIEW'),
    ('SocialStatus', 'BanglaBBQ_SocialStatus', 1440, 'APPROVED'),
]

def sha256(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

manifest = {
    "title": "BanglaBBQ Corrective Repair v2 Change Manifest",
    "author": "Antigravity AI & BanglaBBQ QA Team",
    "timestamp": "2026-11-03T23:54:00+06:00",
    "git_context": {
        "repository": "https://github.com/Hasinish/Research-BanglaBBQ",
        "branch": "main",
        "earlier_canonical_baseline_sha": "18d62ee256e7329b6dac3b7fe87e7e0cdcddcadd",
        "previous_candidate_publication_sha": "b8b619f0b79deae88a2b0679eca173716cd3df45",
    },
    "scope": {
        "total_categories": 9,
        "total_files": 18,
        "total_records": 43200,
        "excluded_categories": ["Age", "Gender", "Physical Appearance"]
    },
    "categories": {}
}

for cat_short, cat_dir, count, status in CATEGORY_MAP:
    cat_entry = {
        "category_name": cat_short,
        "canonical_directory": cat_dir,
        "record_count_per_language": count,
        "readiness_verdict": status,
        "files": {}
    }
    
    for lang in ['ENG', 'BEN']:
        fixed_file = os.path.join(FIXED_DIR, f'BanglaBBQ_{lang}_{cat_short}_QA_fixed.jsonl')
        cand_file = os.path.join(CAND_DIR, f'BanglaBBQ_{lang}_{cat_short}.jsonl')
        canon_file = os.path.join(CANON_DIR, cat_dir, f'BanglaBBQ_{lang}_{cat_short}.jsonl')
        
        # Count field modifications between fixed input and candidate
        diff_context = 0
        diff_question = 0
        diff_label = 0
        diff_ans = 0
        diff_metadata = 0
        
        with open(fixed_file, 'r', encoding='utf-8') as f:
            fix_rows = [json.loads(line) for line in f]
        with open(cand_file, 'r', encoding='utf-8') as f:
            cand_rows = [json.loads(line) for line in f]
            
        for fr, cr in zip(fix_rows, cand_rows):
            if fr['context'] != cr['context']: diff_context += 1
            if fr['question'] != cr['question']: diff_question += 1
            if fr['label'] != cr['label']: diff_label += 1
            if (fr['ans0'], fr['ans1'], fr['ans2']) != (cr['ans0'], cr['ans1'], cr['ans2']): diff_ans += 1
            if fr['answer_info'] != cr['answer_info']: diff_metadata += 1
            
        cat_entry["files"][lang] = {
            "candidate_filename": os.path.basename(cand_file),
            "candidate_sha256": sha256(cand_file),
            "fixed_input_sha256": sha256(fixed_file),
            "canonical_baseline_sha256": sha256(canon_file),
            "field_modifications_from_fixed_input": {
                "context": diff_context,
                "question": diff_question,
                "label": diff_label,
                "ans_options": diff_ans,
                "answer_info": diff_metadata
            }
        }
    manifest["categories"][cat_short] = cat_entry

with open(OUT_MANIFEST, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {OUT_MANIFEST}")
