import sys
import json
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl', 'r', encoding='utf-8') as f:
    eng = [json.loads(line) for line in f]
with open('BanglaBBQ_BEN_New/Age.jsonl', 'r', encoding='utf-8') as f:
    ben = [json.loads(line) for line in f]

assert len(eng) == 2920
assert len(ben) == 2920

repaired_ben = []
modified_row_indices = []
modified_by_theme = Counter()

for idx, (e, b_orig) in enumerate(zip(eng, ben)):
    b = json.loads(json.dumps(b_orig))
    qi = b['question_index']
    
    # ----------------------------------------------------
    # Theme Q3 (IDs 128-199): Zoomer vs Gen-Z kid
    # ----------------------------------------------------
    if qi == '3':
        if 'The Gen-Z kid' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'জেন-জি প্রফেসর':
                    b[k] = 'জেন-জি তরুণ প্রফেসর'
            b['context'] = b['context'].replace('একজন জেন-জি প্রফেসর', 'একজন জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('আসলে জেন-জি প্রফেসর', 'আসলে জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('আরেকজন জেন-জি প্রফেসর', 'আরেকজন জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('জেন-জি প্রফেসর', 'জেন-জি তরুণ প্রফেসর')

    # ----------------------------------------------------
    # Theme Q8 (IDs 712-911): Teen vs Teenager
    # ----------------------------------------------------
    elif qi == '8':
        if 'The teenager' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'কিশোরটি':
                    b[k] = 'কিশোরবয়সী ছেলেটি'
            b['context'] = b['context'].replace('এক কিশোর এবং', 'এক কিশোরবয়সী ছেলে এবং')
            b['context'] = b['context'].replace('এবং এক কিশোর', 'এবং এক কিশোরবয়সী ছেলে')
            b['context'] = b['context'].replace('—কিশোরটি কোনো চাকরি', '—কিশোরবয়সী ছেলেটি কোনো চাকরি')
            b['context'] = b['context'].replace('কিশোরটি কোনো চাকরি', 'কিশোরবয়সী ছেলেটি কোনো চাকরি')
            b['context'] = b['context'].replace('কিশোরটি', 'কিশোরবয়সী ছেলেটি')

    # ----------------------------------------------------
    # Theme Q10 (IDs 1200-1535): High schooler vs High school student
    # ----------------------------------------------------
    elif qi == '10':
        if 'The high school student' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'স্কুলপড়ুয়া শিক্ষার্থীটি':
                    b[k] = 'হাই স্কুলের শিক্ষার্থীটি'
            b['context'] = b['context'].replace('একজন স্কুলপড়ুয়া শিক্ষার্থী এবং', 'হাই স্কুলের একজন শিক্ষার্থী এবং')
            b['context'] = b['context'].replace('এবং একজন স্কুলপড়ুয়া শিক্ষার্থী', 'এবং হাই স্কুলের একজন শিক্ষার্থী')
            b['context'] = b['context'].replace('যে স্কুলপড়ুয়া শিক্ষার্থীটি নিয়মিত', 'যে হাই স্কুলের শিক্ষার্থীটি নিয়মিত')
            b['context'] = b['context'].replace('কিন্তু স্কুলপড়ুয়া শিক্ষার্থীটি প্রায়ই', 'কিন্তু হাই স্কুলের শিক্ষার্থীটি প্রায়ই')
            b['context'] = b['context'].replace('স্কুলপড়ুয়া শিক্ষার্থীটি', 'হাই স্কুলের শিক্ষার্থীটি')

    # ----------------------------------------------------
    # Theme Q11 (IDs 1536-1703): High school student & confrontations
    # ----------------------------------------------------
    elif qi == '11':
        if 'The high school student' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'স্কুলপড়ুয়া শিক্ষার্থীটি':
                    b[k] = 'হাই স্কুলের শিক্ষার্থীটি'
            b['context'] = b['context'].replace('একজন স্কুলপড়ুয়া শিক্ষার্থী আর', 'হাই স্কুলের একজন শিক্ষার্থী আর')
            b['context'] = b['context'].replace('আর একজন স্কুলপড়ুয়া শিক্ষার্থী', 'আর হাই স্কুলের একজন শিক্ষার্থী')
            b['context'] = b['context'].replace('স্কুলপড়ুয়া শিক্ষার্থীটি কখনোই', 'হাই স্কুলের শিক্ষার্থীটি কখনোই')
            b['context'] = b['context'].replace('অথচ স্কুলপড়ুয়া শিক্ষার্থীটি প্রায়ই', 'অথচ হাই স্কুলের শিক্ষার্থীটি প্রায়ই')
            b['context'] = b['context'].replace('স্কুলপড়ুয়া শিক্ষার্থীটি', 'হাই স্কুলের শিক্ষার্থীটি')
            
        if e['context_condition'] == 'disambig':
            if 'never gets into confrontations' in e['context']:
                b['context'] = b['context'].replace('কখনোই মারামারিতে জড়ায় না', 'কখনোই কারো সাথে ঝামেলায় জড়ায় না')
                b['context'] = b['context'].replace('কখনোই মারামারিতে জড়ান না', 'কখনোই কারো সাথে ঝামেলায় জড়ান না')
            elif 'never gets into fights' in e['context']:
                b['context'] = b['context'].replace('কখনোই কারো সাথে ঝামেলায় জড়ায় না', 'কখনোই মারামারিতে জড়ায় না')
                b['context'] = b['context'].replace('কখনোই কারো সাথে ঝামেলায় জড়ান না', 'কখনোই মারামারিতে জড়ান না')

    # ----------------------------------------------------
    # Theme Q12 (IDs 1704-1871): High school student & fights/confrontations
    # ----------------------------------------------------
    elif qi == '12':
        if 'The high school student' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'স্কুলপড়ুয়া শিক্ষার্থীটি':
                    b[k] = 'হাই স্কুলের শিক্ষার্থীটি'
            b['context'] = b['context'].replace('আর একজন স্কুলপড়ুয়া শিক্ষার্থী', 'আর হাই স্কুলের একজন শিক্ষার্থী')
            b['context'] = b['context'].replace('একজন স্কুলপড়ুয়া শিক্ষার্থী আর', 'হাই স্কুলের একজন শিক্ষার্থী আর')
            b['context'] = b['context'].replace('স্কুলপড়ুয়া শিক্ষার্থীটি', 'হাই স্কুলের শিক্ষার্থীটি')
            
        if e['context_condition'] == 'disambig':
            if 'never gets into fights' in e['context']:
                b['context'] = b['context'].replace('কখনোই কারো সাথে ঝামেলায় জড়ান না', 'কখনোই মারামারিতে জড়ান না')
                b['context'] = b['context'].replace('কখনোই কারো সাথে ঝামেলায় জড়ায় না', 'কখনোই মারামারিতে জড়ায় না')
            elif 'never gets into confrontations' in e['context']:
                b['context'] = b['context'].replace('কখনোই মারামারিতে জড়ান না', 'কখনোই কারো সাথে ঝামেলায় জড়ান না')
                b['context'] = b['context'].replace('কখনোই মারামারিতে জড়ায় না', 'কখনোই কারো সাথে ঝামেলায় জড়ায় না')

    # ----------------------------------------------------
    # Theme Q19 (IDs 2360-2639): Teenager & Neighbor/Friend/Someone else
    # ----------------------------------------------------
    elif qi == '19':
        if 'The teenager' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'কিশোরটি':
                    b[k] = 'কিশোরবয়সী ছেলেটি'
            b['context'] = b['context'].replace('এক কিশোর আর', 'এক কিশোরবয়সী ছেলে আর')
            b['context'] = b['context'].replace('আর এক কিশোর।', 'আর এক কিশোরবয়সী ছেলে।')
            b['context'] = b['context'].replace('আর এক কিশোর ', 'আর এক কিশোরবয়সী ছেলে ')
            b['context'] = b['context'].replace('কিশোরটি', 'কিশোরবয়সী ছেলেটি')
            
        if e['context_condition'] == 'disambig':
            if 'a friend signed them up' in e['context']:
                b['context'] = b['context'].replace('পাশের বাসার একজন তার নাম দিয়ে দিয়েছিল', 'তার এক বন্ধু তার নাম দিয়ে দিয়েছিল')
            elif 'someone else signed them up' in e['context']:
                b['context'] = b['context'].replace('পাশের বাসার একজন তার নাম দিয়ে দিয়েছিল', 'অন্য কেউ তার নাম দিয়ে দিয়েছিল')

    if b != b_orig:
        modified_row_indices.append(idx)
        modified_by_theme[qi] += 1
        
    repaired_ben.append(b)

print("=" * 80)
print("REPAIR SIMULATION SUMMARY")
print("=" * 80)
print(f"Total modified records: {len(modified_row_indices)}")
for q in sorted([int(k) for k in modified_by_theme.keys()]):
    print(f"  Theme Q{q}: {modified_by_theme[str(q)]} modified records")

print("\n" + "=" * 80)
print("10-INVARIANT QA VERIFICATION CHECK")
print("=" * 80)

# Check 1: Record count
assert len(repaired_ben) == 2920
print("[Check 1: Total Record Count] -> 2,920 (PASS)")

# Check 2: Sequential IDs
for idx, r in enumerate(repaired_ben):
    assert r['example_id'] == idx and r['id'] == idx
print("[Check 2: Sequential IDs] -> 0 to 2919 contiguous (PASS)")

# Check 3: Schema fields
expected_headers = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]
for idx, r in enumerate(repaired_ben):
    assert list(r.keys()) == expected_headers
    assert isinstance(r['answer_info'], dict)
    assert isinstance(r['additional_metadata'], dict)
    assert r['label'] in (0, 1, 2)
print("[Check 3: 15-Column Schema & Types] -> 100% valid (PASS)")

# Check 4: Condition and Polarity Balances
conds = Counter(r['context_condition'] for r in repaired_ben)
pols = Counter(r['question_polarity'] for r in repaired_ben)
assert conds == {'ambig': 1460, 'disambig': 1460}
assert pols == {'neg': 1460, 'nonneg': 1460}
print(f"[Check 4: Condition & Polarity] -> {conds['ambig']} ambig / {conds['disambig']} disambig, {pols['neg']} neg / {pols['nonneg']} nonneg (PASS)")

# Check 5: Ambiguous contexts target unknown
for idx, r in enumerate(repaired_ben):
    if r['context_condition'] == 'ambig':
        target_ans = r[f"ans{r['label']}"]
        assert target_ans in ['তথ্য অপর্যাপ্ত', 'অজানা', 'বলা সম্ভব নয়', 'Unknown']
print("[Check 5: Ambiguous Context Invariant] -> All 1,460 ambiguous QA pairs target Unknown (PASS)")

# Check 6: English-Bengali Metadata Alignment
for idx, (er, br) in enumerate(zip(eng, repaired_ben)):
    assert er['example_id'] == br['example_id'] == idx
    assert er['question_index'] == br['question_index']
    assert er['context_condition'] == br['context_condition']
    assert er['question_polarity'] == br['question_polarity']
    assert er['type'] == br['type']
    assert er['label'] == br['label']
    assert er['category'] == br['category'] == 'Age'
print("[Check 6: Metadata & Label Alignment] -> 100% alignment across all records (PASS)")

# Check 7: Context uniqueness across all 20 themes
all_themes_match = True
for q in range(1, 21):
    q_str = str(q)
    e_rows = [r for r in eng if r['question_index'] == q_str]
    b_rows = [r for r in repaired_ben if r['question_index'] == q_str]
    e_ctx = set(r['context'] for r in e_rows)
    b_ctx = set(r['context'] for r in b_rows)
    if len(e_ctx) != len(b_ctx):
        all_themes_match = False
        print(f"Mismatch in Q{q}: ENG={len(e_ctx)}, BEN={len(b_ctx)}")
    else:
        print(f"[Check 7.{q:02d}: Theme Q{q:<2} Unique Contexts] -> {len(b_ctx)} / {len(e_ctx)} (100% MATCH)")
assert all_themes_match, "Not all themes match unique context counts!"
print("✓ All 20 themes have 100% context uniqueness parity with English!")

# Check 8: Preserved themes (Q1, Q2, Q4-Q7, Q9, Q13-Q18, Q20)
untouched_themes = [str(q) for q in [1, 2, 4, 5, 6, 7, 9, 13, 14, 15, 16, 17, 18, 20]]
for idx, (b_orig, b_rep) in enumerate(zip(ben, repaired_ben)):
    if b_orig['question_index'] in untouched_themes:
        assert b_orig == b_rep, f"Row {idx} in theme Q{b_orig['question_index']} was unexpectedly modified!"
print(f"[Check 8: Untouched Themes Preservation] -> All 14 non-target themes (including previously repaired Q1 & Q9) are 100% byte-for-byte identical (PASS)")

print("\n" + "=" * 80)
print("ALL VERIFICATIONS COMPLETED WITH ZERO ERRORS! 🏆")
print("=" * 80)
