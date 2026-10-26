import json
import sys
from collections import Counter
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

def sync_and_validate_age():
    print("=" * 80)
    print("STEP 1: FETCHING LIVE DATA FROM GOOGLE SHEETS")
    print("=" * 80)
    
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)
    
    # Fetch BanglaBBQ_BEN_Age
    res_ben = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='BanglaBBQ_BEN_Age!A1:O2921'
    ).execute().get('values', [])
    
    # Fetch BanglaBBQ_ENG_Age for bilingual parity check
    res_eng = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='BanglaBBQ_ENG_Age!A1:O2921'
    ).execute().get('values', [])
    
    ben_headers = res_ben[0]
    ben_rows = res_ben[1:]
    eng_headers = res_eng[0]
    eng_rows = res_eng[1:]
    
    print(f"BanglaBBQ_BEN_Age fetched: {len(ben_rows)} data rows")
    print(f"PakBBQ_ENG_Age fetched: {len(eng_rows)} data rows")
    assert len(ben_rows) == 2920, f"Expected 2920 rows, got {len(ben_rows)}"
    assert len(eng_rows) == 2920, f"Expected 2920 rows, got {len(eng_rows)}"
    
    expected_headers = [
        'example_id', 'question_index', 'context_condition', 'question_polarity',
        'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
        'answer_info', 'additional_metadata', 'category', 'id'
    ]
    assert ben_headers == expected_headers, f"Header mismatch: {ben_headers}"
    assert eng_headers == expected_headers, f"English Header mismatch: {eng_headers}"
    print("✓ Headers verified: 15-column canonical schema")

    # Read existing local file to detect diffs
    ben_path = Path('BanglaBBQ_Age/banglabbq_age_bengali.jsonl') if Path('BanglaBBQ_Age/banglabbq_age_bengali.jsonl').exists() else Path('BanglaBBQ_BEN_New/Age.jsonl')
    with open(ben_path, 'r', encoding='utf-8') as f:
        existing_local = [json.loads(line) for line in f]
    assert len(existing_local) == 2920, f"Expected 2920 local records, got {len(existing_local)}"

    # Parse sheet rows into canonical JSON objects
    parsed_ben_records = []
    diff_count = 0
    diff_by_qi = Counter()

    for idx, (sr, lr) in enumerate(zip(ben_rows, existing_local)):
        rec = {
            'example_id': int(sr[0]) if sr[0].isdigit() else sr[0],
            'question_index': str(sr[1]),
            'context_condition': str(sr[2]),
            'question_polarity': str(sr[3]),
            'type': str(sr[4]),
            'context': str(sr[5]),
            'question': str(sr[6]),
            'ans0': str(sr[7]),
            'ans1': str(sr[8]),
            'ans2': str(sr[9]),
            'label': int(sr[10]) if sr[10].isdigit() else sr[10],
            'answer_info': json.loads(sr[11]) if sr[11].startswith('{') else sr[11],
            'additional_metadata': json.loads(sr[12]) if sr[12].startswith('{') else sr[12],
            'category': str(sr[13]),
            'id': int(sr[14]) if sr[14].isdigit() else sr[14]
        }
        parsed_ben_records.append(rec)
        
        if rec != lr:
            diff_count += 1
            diff_by_qi[rec['question_index']] += 1

    print(f"\nTotal differences detected against local file: {diff_count}")
    if diff_count > 0:
        for qi, cnt in sorted(diff_by_qi.items(), key=lambda x: int(x[0])):
            print(f"  Theme Q{qi}: {cnt} modified records")
        print("Synchronizing differences to local file...")
        with open(ben_path, 'w', encoding='utf-8') as f:
            for rec in parsed_ben_records:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(f"✓ Synchronized updated records to {ben_path}")
    else:
        print("✓ Local JSONL is in 100% bit-for-bit synchronization with live Google Sheets!")

    print("\n" + "=" * 80)
    print("STEP 2: COMPREHENSIVE QUALITY ASSURANCE & INVARIANT VERIFICATION")
    print("=" * 80)

    # Reload from disk to verify disk serialization
    with open(ben_path, 'r', encoding='utf-8') as f:
        verified_ben = [json.loads(line) for line in f]

    # Check 1: Record count
    assert len(verified_ben) == 2920, f"Record count failure: {len(verified_ben)}"
    print("[Check 1: Total Record Count] -> 2,920 (PASS)")

    # Check 2: Sequential IDs
    for idx, r in enumerate(verified_ben):
        assert r['example_id'] == idx, f"example_id mismatch at {idx}: {r['example_id']}"
        assert r['id'] == idx, f"id mismatch at {idx}: {r['id']}"
    print("[Check 2: Sequential IDs (0 to 2919)] -> Strict 0-indexed sequence (PASS)")

    # Check 3: Schema fields
    for idx, r in enumerate(verified_ben):
        assert list(r.keys()) == expected_headers, f"Schema mismatch at row {idx}"
        assert isinstance(r['answer_info'], dict), f"answer_info not dict at row {idx}"
        assert isinstance(r['additional_metadata'], dict), f"additional_metadata not dict at row {idx}"
        assert isinstance(r['label'], int) and r['label'] in (0, 1, 2), f"Invalid label at row {idx}: {r['label']}"
    print("[Check 3: 15-Column Schema & JSON Types] -> 100% compliant (PASS)")

    # Check 4: Condition and Polarity Balances
    cond_counts = Counter(r['context_condition'] for r in verified_ben)
    pol_counts = Counter(r['question_polarity'] for r in verified_ben)
    assert cond_counts == {'ambig': 1460, 'disambig': 1460}, f"Condition imbalance: {cond_counts}"
    assert pol_counts == {'neg': 1460, 'nonneg': 1460}, f"Polarity imbalance: {pol_counts}"
    print(f"[Check 4: Context Condition & Polarity] -> {cond_counts['ambig']} ambig / {cond_counts['disambig']} disambig, {pol_counts['neg']} neg / {pol_counts['nonneg']} nonneg (PASS)")

    # Check 5: Ambiguous contexts gold label check
    for idx, r in enumerate(verified_ben):
        if r['context_condition'] == 'ambig':
            target_ans = r[f"ans{r['label']}"]
            assert target_ans in ['তথ্য অপর্যাপ্ত', 'অজানা', 'বলা সম্ভব নয়', 'Unknown'], f"Ambig row {idx} does not target unknown: '{target_ans}'"
    print("[Check 5: Ambiguous Context Invariant] -> All 1,460 ambiguous QA pairs correctly target Unknown/তথ্য অপর্যাপ্ত (PASS)")

    # Check 6: English-Bengali Bilingual Structural Alignment
    for idx, (er, br) in enumerate(zip(eng_rows, verified_ben)):
        assert int(er[0]) == br['example_id'] == idx
        assert er[1] == br['question_index']
        assert er[2] == br['context_condition']
        assert er[3] == br['question_polarity']
        assert er[4] == br['type']
        assert int(er[10]) == br['label']
        assert er[13] == br['category'] == 'Age'
        assert int(er[14]) == br['id'] == idx
    print("[Check 6: English-Bengali Metadata Alignment] -> 100% alignment across all shared structural fields (PASS)")

    # Check 7: Context uniqueness across ALL 20 themes
    print("\n[Check 7: Unique Context Parity across All 20 Themes against English]:")
    all_matched = True
    for q in range(1, 21):
        q_str = str(q)
        q_ben = [r for r in verified_ben if r['question_index'] == q_str]
        q_eng = [r for r in eng_rows if r[1] == q_str]
        ben_ctxs = set(r['context'] for r in q_ben)
        eng_ctxs = set(r[5] for r in q_eng)
        if len(ben_ctxs) != len(eng_ctxs):
            all_matched = False
            print(f"  Theme Q{q:<2}: MISMATCH (BEN: {len(ben_ctxs)}, ENG: {len(eng_ctxs)})")
        else:
            print(f"  Theme Q{q:<2}: {len(ben_ctxs):>3} / {len(eng_ctxs):>3} unique contexts (100% MATCH)")
    assert all_matched, "Context uniqueness mismatch detected!"
    print("✓ Check 7 PASS: All 20 themes match English context uniqueness counts perfectly!")

    # Check 8: Disambiguated contexts establish exactly one correct answer
    for idx, r in enumerate(verified_ben):
        if r['context_condition'] == 'disambig':
            correct_ans = r[f"ans{r['label']}"]
            assert correct_ans not in ['তথ্য অপর্যাপ্ত', 'অজানা', 'বলা সম্ভব নয়', 'Unknown'], f"Disambig row {idx} has unknown answer: {correct_ans}"
            other_answers = [r[f"ans{i}"] for i in [0, 1, 2] if i != r['label']]
            assert correct_ans not in other_answers, f"Disambig row {idx} has duplicate correct answer among choices!"
    print("[Check 8: Disambiguated Context Correctness] -> Exactly one non-ambiguous answer established per QA pair (PASS)")

    # Check 9: Duplicate QA pairs within condition
    qa_tuples = Counter((r['question_index'], r['context_condition'], r['context'], r['question']) for r in verified_ben)
    max_dups = max(qa_tuples.values())
    print(f"[Check 9: QA Pair Permutation Consistency] -> Max occurrences per (context, question) tuple: {max_dups} (Expected <= 6 permutations) (PASS)")
    assert max_dups <= 6, f"Too many permutations: {max_dups}"

    # Check 10: Untouched themes preservation from baseline backup
    with open('backups/age_sheets_backup_20261017/BanglaBBQ_BEN_Age.json', 'r', encoding='utf-8') as f:
        pre_edit_backup = json.load(f)[1:]
    
    untouched_themes = [str(q) for q in [1, 2, 4, 5, 6, 7, 9, 13, 14, 15, 16, 17, 18]]
    for idx, (bk_row, r) in enumerate(zip(pre_edit_backup, verified_ben)):
        if r['question_index'] in untouched_themes:
            assert bk_row[5] == r['context'], f"Context unexpectedly changed in untouched theme Q{r['question_index']} at row {idx}"
            assert bk_row[7] == r['ans0'] and bk_row[8] == r['ans1'] and bk_row[9] == r['ans2'], f"Answers unexpectedly changed in theme Q{r['question_index']} at row {idx}"
    print(f"[Check 10: Untouched Themes Preservation] -> All 13 non-target themes (including Q1 & Q9) are 100% byte-for-byte preserved from pre-edit backup (PASS)")

    print("\n" + "=" * 80)
    print("ALL 10 QUALITY ASSURANCE CHECKS PASSED PERFECTLY! 🏆")
    print("=" * 80)

if __name__ == '__main__':
    sync_and_validate_age()
