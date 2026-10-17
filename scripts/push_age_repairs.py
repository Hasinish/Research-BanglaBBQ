import sys
import json
from collections import Counter
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'

# 1. Load English source and current Bengali benchmark
with open('PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl', 'r', encoding='utf-8') as f:
    eng = [json.loads(line) for line in f]
with open('BanglaBBQ_BEN_New/Age.jsonl', 'r', encoding='utf-8') as f:
    ben = [json.loads(line) for line in f]

assert len(eng) == 2920
assert len(ben) == 2920

# 2. Generate repaired Bengali records
repaired_ben = []
theme_ranges = {
    '3': (128, 199, 130, 201),
    '8': (712, 911, 714, 913),
    '10': (1200, 1535, 1202, 1537),
    '11': (1536, 1703, 1538, 1705),
    '12': (1704, 1871, 1706, 1873),
    '19': (2360, 2639, 2362, 2641),
}

modified_counts = Counter()

for idx, (e, b_orig) in enumerate(zip(eng, ben)):
    b = json.loads(json.dumps(b_orig))
    qi = b['question_index']
    
    # Theme Q3: Zoomer vs Gen-Z kid
    if qi == '3':
        if 'The Gen-Z kid' in [e['ans0'], e['ans1'], e['ans2']]:
            for k in ['ans0', 'ans1', 'ans2']:
                if b[k] == 'জেন-জি প্রফেসর':
                    b[k] = 'জেন-জি তরুণ প্রফেসর'
            b['context'] = b['context'].replace('একজন জেন-জি প্রফেসর', 'একজন জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('আসলে জেন-জি প্রফেসর', 'আসলে জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('আরেকজন জেন-জি প্রফেসর', 'আরেকজন জেন-জি তরুণ প্রফেসর')
            b['context'] = b['context'].replace('জেন-জি প্রফেসর', 'জেন-জি তরুণ প্রফেসর')

    # Theme Q8: Teen vs Teenager
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

    # Theme Q10: High schooler vs High school student
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

    # Theme Q11: High school student & confrontations
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

    # Theme Q12: High school student & fights/confrontations
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

    # Theme Q19: Teenager & Neighbor/Friend/Someone else
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
        modified_counts[qi] += 1
        
    repaired_ben.append(b)

print("Modified counts across themes:")
for q, cnt in sorted(modified_counts.items(), key=lambda x: int(x[0])):
    print(f"  Theme Q{q}: {cnt} rows")

# Convert records to sheet row list
def rec_to_row(r):
    return [
        str(r['example_id']),
        str(r['question_index']),
        str(r['context_condition']),
        str(r['question_polarity']),
        str(r['type']),
        str(r['context']),
        str(r['question']),
        str(r['ans0']),
        str(r['ans1']),
        str(r['ans2']),
        str(r['label']),
        json.dumps(r['answer_info'], ensure_ascii=False) if isinstance(r['answer_info'], dict) else str(r['answer_info']),
        json.dumps(r['additional_metadata'], ensure_ascii=False) if isinstance(r['additional_metadata'], dict) else str(r['additional_metadata']),
        str(r['category']),
        str(r['id'])
    ]

# Build batch update data
data = []
for t, (start_id, end_id, start_row, end_row) in theme_ranges.items():
    theme_rows = [rec_to_row(repaired_ben[i]) for i in range(start_id, end_id + 1)]
    assert len(theme_rows) == (end_id - start_id + 1)
    data.append({
        'range': f'BanglaBBQ_BEN_Age!A{start_row}:O{end_row}',
        'values': theme_rows
    })

print(f"\nPrepared batch update with {len(data)} theme ranges.")

# Push to Google Sheets API
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

print("Pushing updates to Google Sheets tab BanglaBBQ_BEN_Age...")
body = {
    'valueInputOption': 'RAW',
    'data': data
}
res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body=body
).execute()

print(f"✓ Google Sheets API response: {res.get('totalUpdatedRows')} total rows updated across {res.get('totalUpdatedCells')} cells!")

# Synchronize local file BanglaBBQ_BEN_New/Age.jsonl
with open('BanglaBBQ_BEN_New/Age.jsonl', 'w', encoding='utf-8') as f:
    for r in repaired_ben:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print("✓ Synchronized 2,920 records to BanglaBBQ_BEN_New/Age.jsonl")
