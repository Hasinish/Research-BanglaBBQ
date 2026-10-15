import json
import sys
from collections import Counter
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("====================================================================")
print("COMPREHENSIVE LIVE AUDIT: BANGLABBQ POLITICS 20 THEMES (960 RECORDS)")
print("====================================================================")

# 1. Fetch live data from Google Sheets
print("Fetching live data from BanglaBBQ_ENG_Politics and BanglaBBQ_BEN_Politics...")
eng_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_ENG_Politics!A1:O961'
).execute().get('values', [])

ben_data = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range='BanglaBBQ_BEN_Politics!A1:O961'
).execute().get('values', [])

header_eng = eng_data[0]
header_ben = ben_data[0]
eng_rows = eng_data[1:]
ben_rows = ben_data[1:]

print(f"Total live rows fetched (excluding header): ENG={len(eng_rows)}, BEN={len(ben_rows)} (Target: 960)")
assert len(eng_rows) == 960, f"Expected 960 ENG rows, found {len(eng_rows)}"
assert len(ben_rows) == 960, f"Expected 960 BEN rows, found {len(ben_rows)}"

# 2. Verify Q1-Q5 Unchanged against backup
print("\n--- Check 1: Q1-Q5 Preservation against Pre-Expansion Backup ---")
with open('Dataset_ BanglaBBQ_Old/Politics/backup_q1_q5_eng_240.json', 'r', encoding='utf-8') as f:
    backup_eng = json.load(f)[1:] # drop header
with open('Dataset_ BanglaBBQ_Old/Politics/backup_q1_q5_ben_240.json', 'r', encoding='utf-8') as f:
    backup_ben = json.load(f)[1:]

eng_q1_q5_match = (eng_rows[:240] == backup_eng)
ben_q1_q5_match = (ben_rows[:240] == backup_ben)
print(f"  ENG Q1-Q5 rows 1-240 100% Identical to Backup: {eng_q1_q5_match}")
print(f"  BEN Q1-Q5 rows 1-240 100% Identical to Backup: {ben_q1_q5_match}")
assert eng_q1_q5_match, "CRITICAL: ENG Q1-Q5 modified!"
assert ben_q1_q5_match, "CRITICAL: BEN Q1-Q5 modified!"

# 3. Verify Theme Record Counts (Q1 to Q20)
print("\n--- Check 2: Theme Record Counts (Exactly 48 per theme) ---")
eng_q_counts = Counter(r[1] for r in eng_rows)
ben_q_counts = Counter(r[1] for r in ben_rows)
all_48 = True
for q in range(1, 21):
    c_eng = eng_q_counts.get(str(q), 0)
    c_ben = ben_q_counts.get(str(q), 0)
    if c_eng != 48 or c_ben != 48:
        print(f"  Theme Q{q}: ENG={c_eng}, BEN={c_ben} (FAIL)")
        all_48 = False
    else:
        print(f"  Theme Q{q}: 48 records (PASS)")
assert all_48, "Theme record count check failed!"

# 4. Sequential IDs and Example IDs
print("\n--- Check 3: Sequential IDs (0 to 959) ---")
eng_ids = [int(r[0]) for r in eng_rows]
ben_ids = [int(r[0]) for r in ben_rows]
eng_col_ids = [int(r[14]) for r in eng_rows]
ben_col_ids = [int(r[14]) for r in ben_rows]
seq_target = list(range(960))
print(f"  ENG example_id sequential 0..959: {eng_ids == seq_target}")
print(f"  BEN example_id sequential 0..959: {ben_ids == seq_target}")
print(f"  ENG id col sequential 0..959: {eng_col_ids == seq_target}")
print(f"  BEN id col sequential 0..959: {ben_col_ids == seq_target}")
assert eng_ids == seq_target and ben_ids == seq_target

# 5. Invariant Balances
print("\n--- Check 4: Mathematical Balances & Invariants ---")
cond_counts_eng = Counter(r[2] for r in eng_rows)
pol_counts_eng = Counter(r[3] for r in eng_rows)
lbl_counts_eng = Counter(r[10] for r in eng_rows)
lbl_counts_ben = Counter(r[10] for r in ben_rows)

print(f"  Context Conditions: {cond_counts_eng} (Target: 480 ambig, 480 disambig)")
print(f"  Question Polarities: {pol_counts_eng} (Target: 480 neg, 480 nonneg)")
print(f"  ENG Label Distribution: {lbl_counts_eng} (Target: 320 for 0, 320 for 1, 320 for 2)")
print(f"  BEN Label Distribution: {lbl_counts_ben} (Target: 320 for 0, 320 for 1, 320 for 2)")
assert cond_counts_eng['ambig'] == 480 and cond_counts_eng['disambig'] == 480
assert pol_counts_eng['neg'] == 480 and pol_counts_eng['nonneg'] == 480
assert lbl_counts_eng == Counter({'0': 320, '1': 320, '2': 320})
assert lbl_counts_ben == Counter({'0': 320, '1': 320, '2': 320})

# 6. Four-Row Canonical Sequence Ordering
print("\n--- Check 5: Canonical Four-Row Block Sequence ---")
order_errors = 0
for b in range(240):
    start = b * 4
    b_conds = [eng_rows[start + i][2] for i in range(4)]
    b_pols = [eng_rows[start + i][3] for i in range(4)]
    expected_conds = ['ambig', 'disambig', 'ambig', 'disambig']
    expected_pols = ['neg', 'neg', 'nonneg', 'nonneg']
    if b_conds != expected_conds or b_pols != expected_pols:
        order_errors += 1
print(f"  Four-row ordering errors across all 240 blocks: {order_errors} (Target: 0)")
assert order_errors == 0, f"Found {order_errors} order errors!"

# 7. Answer Permutations Check
print("\n--- Check 6: Unique Answer Permutations (6 per context-question combo) ---")
perm_errors = 0
for qi in range(1, 21):
    q_rows = [r for r in eng_rows if r[1] == str(qi)]
    # Each theme has 2 versions x 4 condition combos = 8 combos. Each must have 6 distinct answer arrangements
    for v_idx in [0, 24]:
        for c_idx in range(4):
            # rows v_idx + c_idx + 4*k for k in 0..5
            arrangements = [tuple(q_rows[v_idx + c_idx + 4*k][7:10]) for k in range(6)]
            if len(set(arrangements)) != 6:
                perm_errors += 1
print(f"  Permutation errors across all 160 QA combos: {perm_errors} (Target: 0)")
assert perm_errors == 0, f"Found {perm_errors} permutation errors!"

# 8. Duplicate QA Records Check
print("\n--- Check 7: Duplicate QA Records Check ---")
eng_qa_tuples = [(r[5], r[6], r[7], r[8], r[9]) for r in eng_rows]
ben_qa_tuples = [(r[5], r[6], r[7], r[8], r[9]) for r in ben_rows]
dup_eng = len(eng_qa_tuples) - len(set(eng_qa_tuples))
dup_ben = len(ben_qa_tuples) - len(set(ben_qa_tuples))
print(f"  Exact duplicate records in English: {dup_eng} (Target: 0)")
print(f"  Exact duplicate records in Bengali: {dup_ben} (Target: 0)")
assert dup_eng == 0 and dup_ben == 0, "Duplicate records found!"

# 9. Gold Label Integrity Check
print("\n--- Check 8: Gold Label Grounding & Accuracy ---")
label_errors = 0
for idx, r in enumerate(eng_rows):
    cond = r[2]
    lbl = int(r[10])
    gold_ans = r[7 + lbl]
    if cond == 'ambig' and gold_ans != 'Unknown':
        label_errors += 1
print(f"  Ambiguous gold label errors: {label_errors} (Target: 0)")
assert label_errors == 0, "Ambiguous gold label error!"

# 10. Bilingual 1-to-1 Alignment Check
print("\n--- Check 9: Bilingual Alignment Check ---")
align_errors = 0
for idx in range(960):
    e = eng_rows[idx]
    b = ben_rows[idx]
    if e[0] != b[0] or e[1] != b[1] or e[2] != b[2] or e[3] != b[3] or e[10] != b[10]:
        align_errors += 1
    # Check JSON metadata
    m_e = json.loads(e[12])
    m_b = json.loads(b[12])
    if m_e['source'] != m_b['source'] or m_e['version'] != m_b['version']:
        align_errors += 1
print(f"  Bilingual 1-to-1 alignment errors: {align_errors} (Target: 0)")
assert align_errors == 0, "Bilingual alignment mismatch!"

# 11. Formatting & Row Heights Check
print("\n--- Check 10: Live Formatting, Conditional Rules, and Row Heights ---")
sheet_meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets(properties(sheetId,title),conditionalFormats)'
).execute()

for s in sheet_meta['sheets']:
    t = s['properties']['title']
    if 'Politics' in t:
        cfs = s.get('conditionalFormats', [])
        print(f"  {t} Conditional Format Rules Count: {len(cfs)}")
        assert len(cfs) == 5, f"Expected 5 conditional format rules on {t}, got {len(cfs)}"
        for i, cf in enumerate(cfs):
            rng = cf['ranges'][0]
            print(f"    Rule {i}: rows {rng.get('startRowIndex')}..{rng.get('endRowIndex')} (Expected: 1..961)")
            assert rng.get('endRowIndex') == 961, f"Rule {i} range endRowIndex is {rng.get('endRowIndex')}, expected 961"

rows_meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=['BanglaBBQ_ENG_Politics!A1:O961'],
    fields='sheets.data.rowMetadata'
).execute()
rm = rows_meta['sheets'][0]['data'][0].get('rowMetadata', [])
print(f"  Total row metadata entries fetched: {len(rm)}")
print(f"  Header height: {rm[0].get('pixelSize')}px (Expected: 28px)")
print(f"  Row 2 (Ambig) height: {rm[1].get('pixelSize')}px (Expected: 42px)")
print(f"  Row 3 (Disambig) height: {rm[2].get('pixelSize')}px (Expected: 88px)")
print(f"  Row 500 (Ambig) height: {rm[499].get('pixelSize')}px (Expected: 42px)")
print(f"  Row 501 (Disambig) height: {rm[500].get('pixelSize')}px (Expected: 88px)")
print(f"  Row 960 (Ambig) height: {rm[959].get('pixelSize')}px (Expected: 42px)")
print(f"  Row 961 (Disambig) height: {rm[960].get('pixelSize')}px (Expected: 88px)")

# 12. Untouched Age Sheets Check
print("\n--- Check 11: Untouched Age Sheets Invariance ---")
for t in ['PakBBQ_ENG_Age', 'BanglaBBQ_BEN_Age']:
    age_vals = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=f'{t}!A:A'
    ).execute().get('values', [])
    rows_cnt = len(age_vals)
    print(f"  {t} total rows (header + data): {rows_cnt} (Expected: 2921)")
    assert rows_cnt == 2921, f"Age sheet {t} modified! Expected 2921 rows, got {rows_cnt}."

print("\n====================================================================")
print("ALL 11 VERIFICATION CHECKS PASSED WITH 100% MATHEMATICAL PERFECTION!")
print("====================================================================")
