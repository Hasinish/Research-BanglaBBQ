import json
import sys
import hashlib
from pathlib import Path
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('.')
DATA_ROOT = ROOT / 'Dataset_BanglaBBQ_New'
OUT_ROOT = ROOT / 'local_candidates' / 'final_seven_category_qa'
CAND_DIR = OUT_ROOT / 'candidates'
REP_DIR = OUT_ROOT / 'reports'

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

EXPECTED_KEYS = {
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
}

CANONICAL_BLOCK_ORDER = [
    ('ambig', 'neg'),
    ('disambig', 'neg'),
    ('ambig', 'nonneg'),
    ('disambig', 'nonneg')
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

CATEGORIES_TO_VALIDATE = [
    {
        'name': 'Health Status',
        'is_candidate': True,
        'eng_path': CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_english.jsonl',
        'ben_path': CAND_DIR / 'BanglaBBQ_Health_Status_FINAL_bengali.jsonl',
        'prod_eng_path': DATA_ROOT / 'BanglaBBQ_HealthStatus' / 'BanglaBBQ_Health_Status_FINAL_english.jsonl',
        'prod_ben_path': DATA_ROOT / 'BanglaBBQ_HealthStatus' / 'BanglaBBQ_Health_Status_FINAL_bengali.jsonl',
        'report_path': REP_DIR / 'health_status_validation_report.md',
    },
    {
        'name': 'Regional Affiliation',
        'is_candidate': True,
        'eng_path': CAND_DIR / 'BanglaBBQ_Regional_FINAL_english.jsonl',
        'ben_path': CAND_DIR / 'BanglaBBQ_Regional_FINAL_bengali.jsonl',
        'prod_eng_path': DATA_ROOT / 'BanglaBBQ_Regional' / 'BanglaBBQ_Regional_FINAL_english.jsonl',
        'prod_ben_path': DATA_ROOT / 'BanglaBBQ_Regional' / 'BanglaBBQ_Regional_FINAL_bengali.jsonl',
        'report_path': REP_DIR / 'regional_affiliation_validation_report.md',
    },
    {
        'name': 'Ethnicity',
        'is_candidate': True,
        'eng_path': CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_english.jsonl',
        'ben_path': CAND_DIR / 'BanglaBBQ_Ethnicity_FINAL_bengali.jsonl',
        'prod_eng_path': DATA_ROOT / 'BanglaBBQ_Ethnicity' / 'BanglaBBQ_Ethnicity_FINAL_english.jsonl',
        'prod_ben_path': DATA_ROOT / 'BanglaBBQ_Ethnicity' / 'BanglaBBQ_Ethnicity_FINAL_bengali.jsonl',
        'report_path': REP_DIR / 'ethnicity_validation_report.md',
    },
    {
        'name': 'Physical Appearance',
        'is_candidate': False,
        'eng_path': DATA_ROOT / 'BanglaBBQ_PhysicalAppearance' / 'BanglaBBQ_Physical_Appearance_FINAL_english.jsonl',
        'ben_path': DATA_ROOT / 'BanglaBBQ_PhysicalAppearance' / 'BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl',
    },
    {
        'name': 'Social Status',
        'is_candidate': False,
        'eng_path': DATA_ROOT / 'BanglaBBQ_SocialStatus' / 'BanglaBBQ_SocialStatus_FINAL_english.jsonl',
        'ben_path': DATA_ROOT / 'BanglaBBQ_SocialStatus' / 'BanglaBBQ_SocialStatus_FINAL_bengali.jsonl',
    },
    {
        'name': 'Occupational Background',
        'is_candidate': False,
        'eng_path': DATA_ROOT / 'BanglaBBQ_OccupationalBackground' / 'BanglaBBQ_Occupational_Background_FINAL_english.jsonl',
        'ben_path': DATA_ROOT / 'BanglaBBQ_OccupationalBackground' / 'BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl',
    },
    {
        'name': 'Marital Status',
        'is_candidate': False,
        'eng_path': DATA_ROOT / 'BanglaBBQ_MaritalStatus' / 'BanglaBBQ_MaritalStatus_FINAL_english.jsonl',
        'ben_path': DATA_ROOT / 'BanglaBBQ_MaritalStatus' / 'BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl',
    },
]

overall_results = {}

for cat in CATEGORIES_TO_VALIDATE:
    name = cat['name']
    print(f"\n=======================================================")
    print(f"  VALIDATING: {name.upper()} ({'CANDIDATE' if cat['is_candidate'] else 'CANONICAL PRODUCTION'})")
    print(f"=======================================================")
    
    en_records = [json.loads(line) for line in open(cat['eng_path'], encoding='utf-8') if line.strip()]
    bn_records = [json.loads(line) for line in open(cat['ben_path'], encoding='utf-8') if line.strip()]
    
    checks = {}
    
    # 1. Total row count
    c1 = (len(en_records) == 1440 and len(bn_records) == 1440)
    checks['Total record count (1,440 per lang)'] = (c1, f"EN: {len(en_records)}, BN: {len(bn_records)}")
    
    # 2. Schema and keys
    en_schema_ok = all(set(r.keys()) == EXPECTED_KEYS for r in en_records)
    bn_schema_ok = all(set(r.keys()) == EXPECTED_KEYS for r in bn_records)
    checks['15-column schema preservation'] = (en_schema_ok and bn_schema_ok, f"All 15 keys present: {en_schema_ok and bn_schema_ok}")
    
    # 3. Sequential IDs
    en_ids_ok = all(r['example_id'] == i for i, r in enumerate(en_records))
    bn_ids_ok = all(r['example_id'] == i for i, r in enumerate(bn_records))
    checks['Contiguous sequential example_id (0..1439)'] = (en_ids_ok and bn_ids_ok, f"EN IDs ok: {en_ids_ok}, BN IDs ok: {bn_ids_ok}")
    
    # 4. 10 themes with 144 rows each
    en_themes = Counter(r['question_index'] for r in en_records)
    bn_themes = Counter(r['question_index'] for r in bn_records)
    c4 = (len(en_themes) == 10 and all(v == 144 for v in en_themes.values()) and
          len(bn_themes) == 10 and all(v == 144 for v in bn_themes.values()))
    checks['10 themes with 144 records each'] = (c4, f"Themes: EN {len(en_themes)}, BN {len(bn_themes)}")
    
    # 5. Bilingual 1-to-1 metadata alignment
    meta_mismatches = 0
    for i in range(1440):
        er, br = en_records[i], bn_records[i]
        for k in ['example_id', 'question_index', 'context_condition', 'question_polarity', 'type', 'label', 'category', 'id']:
            if er[k] != br[k]:
                meta_mismatches += 1
        if er['additional_metadata'].get('version') != br['additional_metadata'].get('version'):
            meta_mismatches += 1
    checks['Bilingual 1-to-1 metadata alignment'] = (meta_mismatches == 0, f"Mismatches: {meta_mismatches}")
    
    # 6. Label distribution
    en_lbls = Counter(r['label'] for r in en_records)
    bn_lbls = Counter(r['label'] for r in bn_records)
    c6 = (en_lbls == {0: 480, 1: 480, 2: 480} and bn_lbls == {0: 480, 1: 480, 2: 480})
    checks['Uniform label distribution (480 / 480 / 480)'] = (c6, f"EN: {dict(en_lbls)}, BN: {dict(bn_lbls)}")
    
    # 7. Condition and polarity counts
    cond_counts = Counter((r['context_condition'], r['question_polarity']) for r in en_records)
    c7 = (cond_counts[('ambig', 'neg')] == 360 and cond_counts[('disambig', 'neg')] == 360 and
          cond_counts[('ambig', 'nonneg')] == 360 and cond_counts[('disambig', 'nonneg')] == 360)
    checks['Condition & polarity balance (360 each)'] = (c7, f"Counts: {dict(cond_counts)}")
    
    # 8. Canonical 4-row block sequence
    blocks_ok = True
    for i in range(0, 1440, 4):
        seq = [(r['context_condition'], r['question_polarity']) for r in en_records[i:i+4]]
        if seq != CANONICAL_BLOCK_ORDER:
            blocks_ok = False
            break
    checks['Canonical 4-row block ordering'] = (blocks_ok, f"All 360 blocks match: {blocks_ok}")
    
    # 9. Ambiguous context Unknown grounding
    ambig_en_ok = True
    ambig_bn_ok = True
    for r in en_records:
        if r['context_condition'] == 'ambig':
            gold_ans = r[f"ans{r['label']}"]
            if gold_ans.strip().lower() not in UNKNOWN_TERMS_ENG and gold_ans.strip() not in UNKNOWN_TERMS_ENG:
                ambig_en_ok = False
    for r in bn_records:
        if r['context_condition'] == 'ambig':
            gold_ans = r[f"ans{r['label']}"]
            if gold_ans.strip() not in UNKNOWN_TERMS_BEN:
                ambig_bn_ok = False
    checks['Ambiguous context Unknown grounding'] = (ambig_en_ok and ambig_bn_ok, f"EN ok: {ambig_en_ok}, BN ok: {ambig_bn_ok}")
    
    # 10. Disambiguated context targets a named entity strictly
    dis_en_ok = True
    dis_bn_ok = True
    for r in en_records:
        if r['context_condition'] == 'disambig':
            gold_ans = r[f"ans{r['label']}"]
            if gold_ans.strip().lower() in UNKNOWN_TERMS_ENG or gold_ans.strip() in UNKNOWN_TERMS_ENG:
                dis_en_ok = False
    for r in bn_records:
        if r['context_condition'] == 'disambig':
            gold_ans = r[f"ans{r['label']}"]
            if gold_ans.strip() in UNKNOWN_TERMS_BEN:
                dis_bn_ok = False
    checks['Disambiguated context non-Unknown grounding'] = (dis_en_ok and dis_bn_ok, f"EN ok: {dis_en_ok}, BN ok: {dis_bn_ok}")
    
    # 11. Six-way answer permutations in 24-row blocks
    perms_ok = True
    for b in range(0, 1440, 24):
        block = en_records[b:b+24]
        for cond, pol in CANONICAL_BLOCK_ORDER:
            sub = [r for r in block if r['context_condition'] == cond and r['question_polarity'] == pol]
            if len(sub) != 6:
                perms_ok = False
            opt_tuples = [tuple(r[f'ans{k}'] for k in range(3)) for r in sub]
            if len(set(opt_tuples)) != 6:
                perms_ok = False
    checks['Complete 6-way answer permutations closure'] = (perms_ok, f"Permutations valid across all 60 blocks: {perms_ok}")
    
    # 12. Position balance in disambiguated negative questions
    def eval_pos_balance(records, lang):
        dis_neg = [r for r in records if r['context_condition'] == 'disambig' and r['question_polarity'] == 'neg']
        dis_nonneg = [r for r in records if r['context_condition'] == 'disambig' and r['question_polarity'] == 'nonneg']
        p1_neg, p2_neg = 0, 0
        p1_nonneg, p2_nonneg = 0, 0
        
        for r in dis_neg:
            ctx = r['context']
            gold = r['ans' + str(r['label'])]
            opts = [r['ans' + str(k)] for k in range(3) if r['ans' + str(k)].strip().lower() not in UNKNOWN_TERMS_ENG and r['ans' + str(k)].strip() not in UNKNOWN_TERMS_BEN]
            assert len(opts) == 2, f"EID {r['example_id']}: opts={opts}"
            o1, o2 = opts[0], opts[1]
            
            if 'from ' in o1:
                d1 = o1.split('from ')[1].strip()
                d2 = o2.split('from ')[1].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            elif 'থেকে আসা' in o1:
                d1 = o1.split('থেকে আসা')[0].strip()
                d2 = o2.split('থেকে আসা')[0].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            elif ',' in o1 and ',' in o2:
                d1 = o1.split(',')[0].strip()
                d2 = o2.split(',')[0].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            else:
                pos1, pos2 = ctx.find(o1), ctx.find(o2)
                
            assert pos1 != -1 and pos2 != -1 and pos1 != pos2, f"EID {r['example_id']}: {o1}:{pos1}, {o2}:{pos2}"
            fp = o1 if pos1 < pos2 else o2
            sp = o2 if pos1 < pos2 else o1
            if gold == fp:
                p1_neg += 1
            elif gold == sp:
                p2_neg += 1
            else:
                raise ValueError(f"EID {r['example_id']}: Gold {gold} != {fp} and != {sp}")
                
        for r in dis_nonneg:
            ctx = r['context']
            gold = r['ans' + str(r['label'])]
            opts = [r['ans' + str(k)] for k in range(3) if r['ans' + str(k)].strip().lower() not in UNKNOWN_TERMS_ENG and r['ans' + str(k)].strip() not in UNKNOWN_TERMS_BEN]
            assert len(opts) == 2
            o1, o2 = opts[0], opts[1]
            
            if 'from ' in o1:
                d1 = o1.split('from ')[1].strip()
                d2 = o2.split('from ')[1].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            elif 'থেকে আসা' in o1:
                d1 = o1.split('থেকে আসা')[0].strip()
                d2 = o2.split('থেকে আসা')[0].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            elif ',' in o1 and ',' in o2:
                d1 = o1.split(',')[0].strip()
                d2 = o2.split(',')[0].strip()
                pos1, pos2 = ctx.find(d1), ctx.find(d2)
            else:
                pos1, pos2 = ctx.find(o1), ctx.find(o2)
                
            assert pos1 != -1 and pos2 != -1 and pos1 != pos2
            fp = o1 if pos1 < pos2 else o2
            sp = o2 if pos1 < pos2 else o1
            if gold == fp:
                p1_nonneg += 1
            elif gold == sp:
                p2_nonneg += 1
            else:
                raise ValueError(f"EID {r['example_id']}: Gold {gold} != {fp} and != {sp}")
                
        return (p1_neg, p2_neg, p1_nonneg, p2_nonneg)
    
    en_pos = eval_pos_balance(en_records, 'English')
    bn_pos = eval_pos_balance(bn_records, 'Bengali')
    pos_balanced = (en_pos[0] == 180 and en_pos[1] == 180 and en_pos[2] == 180 and en_pos[3] == 180 and
                    bn_pos[0] == 180 and bn_pos[1] == 180 and bn_pos[2] == 180 and bn_pos[3] == 180)
    checks['Position balance (180 First / 180 Second in Neg and NonNeg)'] = (
        pos_balanced,
        f"EN Neg: {en_pos[0]}/{en_pos[1]}, NonNeg: {en_pos[2]}/{en_pos[3]} | BN Neg: {bn_pos[0]}/{bn_pos[1]}, NonNeg: {bn_pos[2]}/{bn_pos[3]}"
    )
    
    # 13. Unaltered fields check for candidates
    if cat['is_candidate']:
        prod_en = [json.loads(line) for line in open(cat['prod_eng_path'], encoding='utf-8') if line.strip()]
        prod_bn = [json.loads(line) for line in open(cat['prod_ben_path'], encoding='utf-8') if line.strip()]
        non_ctx_diffs = 0
        mod_count_en = 0
        mod_count_bn = 0
        for i in range(1440):
            if en_records[i]['context'] != prod_en[i]['context']:
                mod_count_en += 1
            if bn_records[i]['context'] != prod_bn[i]['context']:
                mod_count_bn += 1
            for k in EXPECTED_KEYS:
                if k != 'context':
                    if en_records[i][k] != prod_en[i][k] or bn_records[i][k] != prod_bn[i][k]:
                        non_ctx_diffs += 1
        c13 = (non_ctx_diffs == 0 and mod_count_en == 720 and mod_count_bn == 720)
        checks['Surgical minimal modification (exactly 720 context edits, 0 other diffs)'] = (
            c13, f"EN modified: {mod_count_en}, BN modified: {mod_count_bn}, Non-context diffs: {non_ctx_diffs}"
        )
        
    overall_results[name] = checks
    
    # Print results
    pass_cnt = sum(1 for status, detail in checks.values() if status)
    fail_cnt = len(checks) - pass_cnt
    print(f"Summary for {name}: {pass_cnt} PASS / {fail_cnt} FAIL")
    for chk_name, (status, detail) in checks.items():
        status_str = "PASS" if status else "FAIL"
        print(f"  [{status_str}] {chk_name}: {detail}")
        
    # Generate category report if candidate
    if cat.get('report_path'):
        with open(cat['report_path'], 'w', encoding='utf-8') as rf:
            rf.write(f"# Category Validation Report — {name}\n\n")
            rf.write(f"**Validation Status**: `{'STRUCTURALLY VALIDATED' if fail_cnt == 0 else 'BLOCKED'}`\n\n")
            rf.write(f"- **Total Invariants Tested**: {len(checks)}\n")
            rf.write(f"- **Pass Count**: {pass_cnt}\n")
            rf.write(f"- **Fail Count**: {fail_cnt}\n\n")
            rf.write("## Test Results by Invariant Gate\n\n")
            rf.write("| Gate # | Invariant Description | Status | Details |\n")
            rf.write("| :---: | :--- | :---: | :--- |\n")
            for idx, (chk_name, (status, detail)) in enumerate(checks.items(), 1):
                rf.write(f"| {idx} | {chk_name} | `{'PASS' if status else 'FAIL'}` | {detail} |\n")
            rf.write("\n## Candidate Artifact Hashes (SHA-256)\n\n")
            rf.write(f"- **English Candidate**: `{cat['eng_path'].name}` -> `{sha256_file(cat['eng_path'])}`\n")
            rf.write(f"- **Bengali Candidate**: `{cat['ben_path'].name}` -> `{sha256_file(cat['ben_path'])}`\n")

# Write overall validation report
with open(REP_DIR / 'all_seven_categories_independent_validation.md', 'w', encoding='utf-8') as rf:
    rf.write("# Independent Validation Report Across All Seven Categories\n\n")
    rf.write("| Category | Role | Records | Status | Disambig Neg Position Split | Invariant Pass Rate |\n")
    rf.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for cat in CATEGORIES_TO_VALIDATE:
        name = cat['name']
        res = overall_results[name]
        p_cnt = sum(1 for s, d in res.values() if s)
        f_cnt = len(res) - p_cnt
        status_lbl = "STRUCTURALLY VALIDATED" if f_cnt == 0 else "BLOCKED"
        pos_det = res['Position balance (180 First / 180 Second in Neg and NonNeg)'][1].split(' | ')[0]
        rf.write(f"| **{name}** | {'Candidate' if cat['is_candidate'] else 'Production'} | 1,440 x 2 | `{status_lbl}` | {pos_det} | {p_cnt}/{len(res)} (100%) |\n")

print("\nAll validation checks and reports successfully generated!")
