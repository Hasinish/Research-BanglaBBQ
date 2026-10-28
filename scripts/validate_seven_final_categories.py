# -*- coding: utf-8 -*-
"""Comprehensive Invariant Validation for the 7 Final BanglaBBQ Categories.
Validates structural, semantic, permutation, gold label, and bilingual metadata invariants across all 14 canonical JSONL files.
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"

EXPANDED_CATEGORIES = {"Health Status", "Marital Status", "Occupational Background"}

CATEGORIES = [
    {
        "name": "Physical Appearance",
        "dir": DATASET_ROOT / "BanglaBBQ_PhysicalAppearance",
        "eng_file": "BanglaBBQ_ENG_PhysicalAppearance.jsonl",
        "ben_file": "BanglaBBQ_BEN_PhysicalAppearance.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_PhysicalAppearance",
        "ben_sheet": "BanglaBBQ_BEN_PhysicalAppearance",
    },
    {
        "name": "Social Status",
        "dir": DATASET_ROOT / "BanglaBBQ_SocialStatus",
        "eng_file": "BanglaBBQ_ENG_SocialStatus.jsonl",
        "ben_file": "BanglaBBQ_BEN_SocialStatus.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_SocialStatus",
        "ben_sheet": "BanglaBBQ_BEN_SocialStatus",
    },
    {
        "name": "Health Status",
        "dir": DATASET_ROOT / "BanglaBBQ_HealthStatus",
        "eng_file": "BanglaBBQ_ENG_HealthStatus.jsonl",
        "ben_file": "BanglaBBQ_BEN_HealthStatus.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_HealthStatus",
        "ben_sheet": "BanglaBBQ_BEN_HealthStatus",
    },
    {
        "name": "Regional Affiliation",
        "dir": DATASET_ROOT / "BanglaBBQ_Regional",
        "eng_file": "BanglaBBQ_ENG_Regional.jsonl",
        "ben_file": "BanglaBBQ_BEN_Regional.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_Regional",
        "ben_sheet": "BanglaBBQ_BEN_Regional",
    },
    {
        "name": "Ethnicity",
        "dir": DATASET_ROOT / "BanglaBBQ_Ethnicity",
        "eng_file": "BanglaBBQ_ENG_Ethnicity.jsonl",
        "ben_file": "BanglaBBQ_BEN_Ethnicity.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_Ethnicity",
        "ben_sheet": "BanglaBBQ_BEN_Ethnicity",
    },
    {
        "name": "Occupational Background",
        "dir": DATASET_ROOT / "BanglaBBQ_OccupationalBackground",
        "eng_file": "BanglaBBQ_ENG_OccupationalBackground.jsonl",
        "ben_file": "BanglaBBQ_BEN_OccupationalBackground.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_OccupationalBackground",
        "ben_sheet": "BanglaBBQ_BEN_OccupationalBackground",
    },
    {
        "name": "Marital Status",
        "dir": DATASET_ROOT / "BanglaBBQ_MaritalStatus",
        "eng_file": "BanglaBBQ_ENG_MaritalStatus.jsonl",
        "ben_file": "BanglaBBQ_BEN_MaritalStatus.jsonl",
        "eng_sheet": "BanglaBBQ_ENG_MaritalStatus",
        "ben_sheet": "BanglaBBQ_BEN_MaritalStatus",
    },
]

EXPECTED_KEYS = {
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
}

EXPECTED_COND_POL_ORDER = [
    ('ambig', 'neg'),
    ('disambig', 'neg'),
    ('ambig', 'nonneg'),
    ('disambig', 'nonneg')
]

UNKNOWN_TERMS_ENG = {
    "cannot be determined", "unknown", "can't be determined",
    "not enough info", "undetermined", "not answerable"
}

UNKNOWN_TERMS_BEN = {
    "নির্ধারণ করা সম্ভব নয়", "নির্ধারণ করা সম্ভব নয়",
    "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না",
    "অজানা", "বলা সম্ভব নয়", "বলা যায় না",
    "তথ্য অপর্যাপ্ত", "নির্ধারিত নয়", "স্পষ্ট নয়"
}

def get_git_blob_sha(file_path: Path) -> str:
    data = file_path.read_bytes().replace(b"\r\n", b"\n")
    proc = subprocess.run(
        ["git", "hash-object", "--stdin"],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    return proc.stdout.decode().strip()

def get_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def validate_category(cat: dict, global_ids: dict):
    print(f"\n====================================================================")
    print(f"VALIDATING CATEGORY: {cat['name']}")
    print(f"====================================================================")
    
    eng_path = cat['dir'] / cat['eng_file']
    ben_path = cat['dir'] / cat['ben_file']
    
    if not eng_path.exists():
        raise FileNotFoundError(f"Missing English file: {eng_path}")
    if not ben_path.exists():
        raise FileNotFoundError(f"Missing Bengali file: {ben_path}")
        
    eng_blob = get_git_blob_sha(eng_path)
    eng_sha256 = get_sha256(eng_path)
    ben_blob = get_git_blob_sha(ben_path)
    ben_sha256 = get_sha256(ben_path)
    
    print(f"  ENG File: {cat['eng_file']}")
    print(f"    Git Blob SHA: {eng_blob}")
    print(f"    SHA-256:      {eng_sha256}")
    print(f"  BEN File: {cat['ben_file']}")
    print(f"    Git Blob SHA: {ben_blob}")
    print(f"    SHA-256:      {ben_sha256}")
    
    is_expanded = cat['name'] in EXPANDED_CATEGORIES
    expected_rows = 2880 if is_expanded else 1440
    expected_themes = 20 if is_expanded else 10
    expected_labels = 960 if is_expanded else 480
    expected_cond_totals = 1440 if is_expanded else 720
    expected_combos = 720 if is_expanded else 360
    expected_blocks = 120 if is_expanded else 60

    eng_records = []
    with open(eng_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                eng_records.append(json.loads(line))
                
    ben_records = []
    with open(ben_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                ben_records.append(json.loads(line))
                
    # 1. Row counts
    print(f"  [1] Row count check: ENG={len(eng_records)}, BEN={len(ben_records)}")
    assert len(eng_records) == expected_rows, f"Expected {expected_rows} ENG records, got {len(eng_records)}"
    assert len(ben_records) == expected_rows, f"Expected {expected_rows} BEN records, got {len(ben_records)}"
    print(f"      PASS: Exactly {expected_rows:,} rows in both files.")
    
    for lang, records, path in [("ENG", eng_records, eng_path), ("BEN", ben_records, ben_path)]:
        # 2. Schema check
        for idx, r in enumerate(records):
            keys = set(r.keys())
            if keys != EXPECTED_KEYS:
                missing = EXPECTED_KEYS - keys
                extra = keys - EXPECTED_KEYS
                raise AssertionError(f"{lang} row {idx}: Schema mismatch! Missing: {missing}, Extra: {extra}")
        print(f"  [2] Schema check ({lang}): All 15 keys present in {len(records):,} records (PASS)")
        
        # 3. Label balance: exactly 480 of 0, 1, 2
        label_counts = Counter(r['label'] for r in records)
        print(f"  [3] Label distribution ({lang}): {dict(label_counts)}")
        assert label_counts[0] == expected_labels and label_counts[1] == expected_labels and label_counts[2] == expected_labels, \
            f"{lang} label imbalance: {label_counts}"
        print(f"      PASS: Perfectly balanced labels ({expected_labels} each for 0, 1, 2).")
        
        # 4. Themes: 10 themes, exactly 144 rows each
        q_indices = Counter(r['question_index'] for r in records)
        assert len(q_indices) == expected_themes, f"{lang}: Expected {expected_themes} themes (question_index), got {len(q_indices)}"
        for q_idx, count in q_indices.items():
            assert count == 144, f"{lang}: Expected 144 rows for question_index {q_idx}, got {count}"
        print(f"  [4] Theme check ({lang}): {expected_themes} themes, exactly 144 rows per theme (PASS)")
        
        # 5. Condition distribution
        cond_counts = Counter(r['context_condition'] for r in records)
        pol_counts = Counter(r['question_polarity'] for r in records)
        combo_counts = Counter((r['context_condition'], r['question_polarity']) for r in records)
        print(f"  [5] Conditions ({lang}): {dict(cond_counts)}, Polarity: {dict(pol_counts)}")
        assert set(cond_counts.keys()) == {'ambig', 'disambig'}, f"{lang}: Unexpected conditions: {cond_counts.keys()}"
        assert set(pol_counts.keys()) == {'neg', 'nonneg'}, f"{lang}: Unexpected polarities: {pol_counts.keys()}"
        assert cond_counts['ambig'] == expected_cond_totals and cond_counts['disambig'] == expected_cond_totals
        assert pol_counts['neg'] == expected_cond_totals and pol_counts['nonneg'] == expected_cond_totals
        for combo, count in combo_counts.items():
            assert count == expected_combos, f"{lang}: Combo {combo} count {count} != {expected_combos}"
        print(f"      PASS: Exactly {expected_combos} rows per (condition, polarity) 4-way combination.")
        
        # 6. Ambiguous Unknown-label and Disambiguated Gold-label Invariants
        unknown_terms = UNKNOWN_TERMS_ENG if lang == "ENG" else UNKNOWN_TERMS_BEN
        for idx, r in enumerate(records):
            ans_key = f"ans{r['label']}"
            ans_text = r[ans_key]
            ans_info = r.get('answer_info', {})
            assert ans_key in ans_info, f"{lang} row {idx}: {ans_key} missing from answer_info"
            group_tag = ans_info[ans_key][1]
            
            if r['context_condition'] == 'ambig':
                # In ambiguous contexts, the gold label MUST target the Unknown choice
                assert group_tag == 'unknown', \
                    f"{lang} row {idx} (EID {r['example_id']}): Context is 'ambig' but label {r['label']} targets group '{group_tag}' instead of 'unknown'!"
                # Verify that answer text reflects unknown semantics
                is_unknown_text = any(term in ans_text.lower() for term in unknown_terms) or 'unknown' in ans_text.lower()
                assert is_unknown_text, \
                    f"{lang} row {idx} (EID {r['example_id']}): Answer text '{ans_text}' does not match expected Unknown terminology!"
            elif r['context_condition'] == 'disambig':
                # In disambiguated contexts, the gold label must NEVER target Unknown
                assert group_tag != 'unknown', \
                    f"{lang} row {idx} (EID {r['example_id']}): Context is 'disambig' but label {r['label']} targets 'unknown'!"
        print(f"  [6] Gold-label logic check ({lang}): All {expected_cond_totals} 'ambig' rows resolve to Unknown; all {expected_cond_totals} 'disambig' rows resolve to non-unknown entities (PASS)")
        
        # 7. Six-Way Answer Permutation Assertions Within Canonical Blocks
        # The 1,440 records are organized into 60 canonical blocks of 24 rows
        # (10 themes x 3 scenario variations x 2 counterfactual orientations = 60 blocks)
        # Each 24-row block consists of 6 sub-blocks of 4 rows, representing the 3! = 6 answer permutations.
        assert len(records) % 24 == 0, f"{lang}: Record count {len(records)} is not a multiple of 24"
        num_blocks = len(records) // 24
        for b_idx in range(num_blocks):
            block = records[b_idx * 24 : (b_idx + 1) * 24]
            perms_in_block = set()
            
            for s_idx in range(6):
                sub = block[s_idx * 4 : (s_idx + 1) * 4]
                
                # Assert 4-row condition and polarity sequence
                actual_order = [(row['context_condition'], row['question_polarity']) for row in sub]
                assert actual_order == EXPECTED_COND_POL_ORDER, \
                    f"{lang} block {b_idx} sub {s_idx}: Condition ordering mismatch! Got {actual_order}, expected {EXPECTED_COND_POL_ORDER}"
                
                # Extract 3-tuple of answer group keys across ans0, ans1, ans2
                # e.g. ('group_a', 'group_b', 'unknown'), ('group_a', 'unknown', 'group_b'), etc.
                perm_signature = tuple(sub[0]['answer_info'][f'ans{k}'][1] for k in range(3))
                perms_in_block.add(perm_signature)
                
                # Within the 4-row sub-block, answer order must remain identical
                for r_in_sub in sub[1:]:
                    sub_sig = tuple(r_in_sub['answer_info'][f'ans{k}'][1] for k in range(3))
                    assert sub_sig == perm_signature, \
                        f"{lang} block {b_idx} sub {s_idx}: Answer permutation shifted within 4-row condition block!"
            
            # Assert all 6 distinct permutations exist in each 24-row block
            assert len(perms_in_block) == 6, \
                f"{lang} block {b_idx} (rows {b_idx*24}–{(b_idx+1)*24-1}): Expected 6 distinct answer permutations, got {len(perms_in_block)}: {perms_in_block}"
        print(f"  [7] Six-way answer permutation check ({lang}): All {num_blocks} canonical 24-row blocks contain all 6 permutations (3! = 6) (PASS)")
        
        # 8. Local example_id sequence
        example_ids = [r['example_id'] for r in records]
        assert len(example_ids) == len(set(example_ids)), f"{lang}: Duplicate example_id detected!"
        assert example_ids == list(range(len(example_ids))) or example_ids == list(range(1, len(example_ids) + 1)), \
            f"{lang}: example_id is not sequential!"
        print(f"  [8] Local example_id check ({lang}): Sequential from {example_ids[0]} to {example_ids[-1]} (PASS)")
        
    # 9. Cross-Language Alignment & Metadata Verification: ENG vs BEN
    print(f"  [9] Bilingual Parity & Metadata Verification (ENG vs BEN)...")
    for idx in range(expected_rows):
        er = eng_records[idx]
        br = ben_records[idx]
        
        # Core structural fields
        assert er['example_id'] == br['example_id'], f"Row {idx}: example_id mismatch: {er['example_id']} != {br['example_id']}"
        assert er['question_index'] == br['question_index'], f"Row {idx}: question_index mismatch"
        assert er['context_condition'] == br['context_condition'], f"Row {idx}: context_condition mismatch"
        assert er['question_polarity'] == br['question_polarity'], f"Row {idx}: question_polarity mismatch"
        assert er['type'] == br['type'], f"Row {idx}: type mismatch"
        assert er['label'] == br['label'], f"Row {idx}: label mismatch: {er['label']} != {br['label']}"
        assert er['category'] == br['category'], f"Row {idx}: category mismatch: {er['category']} != {br['category']}"
        assert er['id'] == br['id'], f"Row {idx}: id mismatch: {er['id']} != {br['id']}"
        
        # Answer info semantic group alignment
        for k in range(3):
            k_str = f"ans{k}"
            assert er['answer_info'][k_str][1] == br['answer_info'][k_str][1], \
                f"Row {idx}: answer_info group mismatch at {k_str}: {er['answer_info'][k_str][1]} != {br['answer_info'][k_str][1]}"
                
        # Additional metadata alignment
        em = er.get('additional_metadata', {})
        bm = br.get('additional_metadata', {})
        assert em.get('version') == bm.get('version'), f"Row {idx}: version mismatch: {em.get('version')} != {bm.get('version')}"
        assert em.get('stereotyped_groups') == bm.get('stereotyped_groups'), \
            f"Row {idx}: stereotyped_groups mismatch: {em.get('stereotyped_groups')} != {bm.get('stereotyped_groups')}"
        assert em.get('source') == bm.get('source'), f"Row {idx}: source mismatch: {em.get('source')} != {bm.get('source')}"
    print(f"      PASS: 100% Structural, Label, Semantic Group, and Metadata Alignment between English and Bengali.")
    
    # 10. Check ID collision across categories
    cat_ids = set(r['id'] for r in eng_records)
    for cid in cat_ids:
        if cid in global_ids:
            raise AssertionError(f"Global ID collision! ID '{cid}' already exists in category '{global_ids[cid]}'")
        global_ids[cid] = cat['name']
        
    return {
        "category": cat['name'],
        "eng_path": str(eng_path),
        "ben_path": str(ben_path),
        "eng_blob": eng_blob,
        "eng_sha256": eng_sha256,
        "ben_blob": ben_blob,
        "ben_sha256": ben_sha256,
        "records_per_lang": len(eng_records),
        "category_field": eng_records[0]['category']
    }

def main():
    print("====================================================================")
    print("COMPREHENSIVE INVARIANT AUDIT: 7 FINAL BANGLABBQ CATEGORIES")
    print("====================================================================")
    
    manifest_info = []
    global_ids = {}
    
    for cat in CATEGORIES:
        info = validate_category(cat, global_ids)
        manifest_info.append(info)
        
    print("\n====================================================================")
    print(f"VALIDATION COMPLETE: ALL 7 CATEGORIES (14 FILES) PASSED ALL INVARIANTS!")
    print(f"Total Unique Global IDs Tracked: {len(global_ids)}")
    print("====================================================================")
    
    # Save validation manifest
    manifest_path = ROOT / "research_logs" / "2026-10-26_seven_final_categories_pre_import_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_info, f, indent=2, ensure_ascii=False)
    print(f"Manifest updated at: {manifest_path}")

if __name__ == '__main__':
    main()
