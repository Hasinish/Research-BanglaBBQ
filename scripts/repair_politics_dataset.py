import json
import hashlib
import sys
import copy

sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print("PHASE B: TARGETED AUDIT & REPAIR OF BANGLABBQ POLITICS DATASET")
print("====================================================================")

# 1. Load current JSONL files
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    eng_recs = [json.loads(line) for line in f]

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'r', encoding='utf-8') as f:
    ben_recs = [json.loads(line) for line in f]

assert len(eng_recs) == 960
assert len(ben_recs) == 960

# 2. Check Q1-Q5 hashes before modifications
q1_q5_eng_pre = hashlib.sha256(json.dumps(eng_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()
q1_q5_ben_pre = hashlib.sha256(json.dumps(ben_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()

print(f"Pre-repair Q1-Q5 ENG SHA-256: {q1_q5_eng_pre}")
print(f"Pre-repair Q1-Q5 BEN SHA-256: {q1_q5_ben_pre}")

# Tracking changes for report
report = {
    'answer_info_corrections': 0,
    'source_corrections': {'Q6': 0, 'Q13': 0},
    'translation_corrections': {'Q6': 0, 'Q10': 0, 'Q16': 0, 'Q18': 0},
    'detailed_logs': []
}

# 3. Apply repairs to Q6-Q20 (IDs 240-959)
for i in range(240, 960):
    e = eng_recs[i]
    b = ben_recs[i]
    q_idx = e['question_index']
    rec_id = e['id']
    
    # 3.1 Repair answer_info: align Bengali with English canonical identifiers
    if b['answer_info'] != e['answer_info']:
        old_b_ans_info = copy.deepcopy(b['answer_info'])
        b['answer_info'] = copy.deepcopy(e['answer_info'])
        report['answer_info_corrections'] += 1
        if report['answer_info_corrections'] <= 3:
            report['detailed_logs'].append({
                'type': 'answer_info',
                'id': rec_id,
                'q_index': q_idx,
                'before': old_b_ans_info,
                'after': b['answer_info']
            })
            
    # 3.2 Source repairs
    # Q6: Political rally permission -> HRW World Report 2023 (Freedom of Peaceful Assembly)
    if q_idx == 6:
        new_src = 'https://www.hrw.org/world-report/2023/country-chapters/bangladesh'
        if e['additional_metadata']['source'] != new_src:
            e['additional_metadata']['source'] = new_src
            b['additional_metadata']['source'] = new_src
            report['source_corrections']['Q6'] += 1
            
    # Q13: Newspaper printing press declaration revocation -> CPJ investigation on Dainik Dinkal
    if q_idx == 13:
        new_src = 'https://cpj.org/2023/02/bangladesh-shuts-down-main-opposition-newspaper-dainik-dinkal/'
        if e['additional_metadata']['source'] != new_src:
            e['additional_metadata']['source'] = new_src
            b['additional_metadata']['source'] = new_src
            report['source_corrections']['Q13'] += 1

    # 3.3 Bengali Translation corrections
    # Q6: 'বাতিল' (cancelled) -> 'নামঞ্জুর' (denied) in negative questions & disambiguated contexts
    if q_idx == 6:
        if b['question_polarity'] == 'neg':
            if 'বাতিল করা হয়েছিল' in b['question']:
                old_q = b['question']
                b['question'] = b['question'].replace('বাতিল করা হয়েছিল', 'নামঞ্জুর করা হয়েছিল')
                report['translation_corrections']['Q6'] += 1
                if report['translation_corrections']['Q6'] == 1:
                    report['detailed_logs'].append({
                        'type': 'translation_question',
                        'id': rec_id,
                        'q_index': 6,
                        'before': old_q,
                        'after': b['question'],
                        'reason': 'English "denied permission" describes an application rejection (নামঞ্জুর), not revocation/cancellation (বাতিল) of existing approval.'
                    })
        if b['context_condition'] == 'disambig':
            if 'ছাড়পত্র বাতিল করে দেয়' in b['context']:
                old_c = b['context']
                b['context'] = b['context'].replace('ছাড়পত্র বাতিল করে দেয়', 'ছাড়পত্র নামঞ্জুর করে দেয়')
                report['translation_corrections']['Q6'] += 1

    # Q10: 'ভোটকেন্দ্রে' (polling station/center) -> 'ভোটবুথে' (voting booth) in negative question
    if q_idx == 10:
        if b['question_polarity'] == 'neg':
            if 'ভোটকেন্দ্রে প্রবেশ করতে বাধা' in b['question']:
                old_q = b['question']
                b['question'] = b['question'].replace('ভোটকেন্দ্রে প্রবেশ করতে বাধা', 'ভোটবুথে প্রবেশ করতে বাধা')
                report['translation_corrections']['Q10'] += 1
                if report['translation_corrections']['Q10'] == 1:
                    report['detailed_logs'].append({
                        'type': 'translation_question',
                        'id': rec_id,
                        'q_index': 10,
                        'before': old_q,
                        'after': b['question'],
                        'reason': 'English "voting booth" specifically refers to the booth (ভোটবুথ/ভোটকক্ষ) where ballots are cast, distinguishing it from the entire polling center (ভোটকেন্দ্র).'
                    })

    # Q16: 'বাতিল' (cancelled) -> 'নাকচ' (rejected) for welfare/relief application
    if q_idx == 16:
        if b['question_polarity'] == 'neg':
            if 'আবেদন বাতিল করা হয়েছিল' in b['question']:
                old_q = b['question']
                b['question'] = b['question'].replace('আবেদন বাতিল করা হয়েছিল', 'আবেদন নাকচ করা হয়েছিল')
                report['translation_corrections']['Q16'] += 1
                if report['translation_corrections']['Q16'] == 1:
                    report['detailed_logs'].append({
                        'type': 'translation_question',
                        'id': rec_id,
                        'q_index': 16,
                        'before': old_q,
                        'after': b['question'],
                        'reason': 'English "application was rejected" in administrative Bengali is "নাকচ করা" (application rejected), whereas "বাতিল করা" implies cancellation of an already issued card.'
                    })

    # Q18: 'গ্রেপ্তার করে' (arrested) -> 'আটক করে' (detained) in disambiguated context
    if q_idx == 18:
        if b['context_condition'] == 'disambig':
            if 'ওয়ার্ড থেকে গ্রেপ্তার করে' in b['context']:
                old_c = b['context']
                b['context'] = b['context'].replace('ওয়ার্ড থেকে গ্রেপ্তার করে', 'ওয়ার্ড থেকে আটক করে')
                report['translation_corrections']['Q18'] += 1
                if report['translation_corrections']['Q18'] == 1:
                    report['detailed_logs'].append({
                        'type': 'translation_context',
                        'id': rec_id,
                        'q_index': 18,
                        'before': old_c,
                        'after': b['context'],
                        'reason': 'English "detain them from the ward" refers to police custody/detention (আটক), distinct from formal judicial arrest under warrant (গ্রেপ্তার). Matches Bengali question "আটক করেছিল".'
                    })

print(f"\n--- Repairs Summary ---")
print(f"Total answer_info corrections (aligned with English canonical identities): {report['answer_info_corrections']} (Target: 720)")
print(f"Source corrections: Q6={report['source_corrections']['Q6']} (48 rows), Q13={report['source_corrections']['Q13']} (48 rows)")
print(f"Translation corrections: Q6={report['translation_corrections']['Q6']}, Q10={report['translation_corrections']['Q10']}, Q16={report['translation_corrections']['Q16']}, Q18={report['translation_corrections']['Q18']}")

# 4. Critical Invariant Checks
q1_q5_eng_post = hashlib.sha256(json.dumps(eng_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()
q1_q5_ben_post = hashlib.sha256(json.dumps(ben_recs[:240], sort_keys=True).encode('utf-8')).hexdigest()

print("\n--- Integrity Invariant Checks ---")
print(f"Q1-Q5 ENG SHA-256 match pre-repair: {q1_q5_eng_post == q1_q5_eng_pre}")
print(f"Q1-Q5 BEN SHA-256 match pre-repair: {q1_q5_ben_post == q1_q5_ben_pre}")
assert q1_q5_eng_post == q1_q5_eng_pre, "CRITICAL ERROR: Q1-Q5 ENG modified!"
assert q1_q5_ben_post == q1_q5_ben_pre, "CRITICAL ERROR: Q1-Q5 BEN modified!"

# 5. Save updated JSONL files
with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'w', encoding='utf-8') as f:
    for r in eng_recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl', 'w', encoding='utf-8') as f:
    for r in ben_recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

# Also write to a new clean canonical directory `Dataset_BanglaBBQ_New/BanglaBBQ_Politics/`
import os
pol_out_dir = 'Dataset_BanglaBBQ_New/BanglaBBQ_Politics' if os.path.exists('Dataset_BanglaBBQ_New/BanglaBBQ_Politics') else 'BanglaBBQ_Politics'
os.makedirs(pol_out_dir, exist_ok=True)
with open(f'{pol_out_dir}/banglabbq_politics_english.jsonl', 'w', encoding='utf-8') as f:
    for r in eng_recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(f'{pol_out_dir}/banglabbq_politics_bengali.jsonl', 'w', encoding='utf-8') as f:
    for r in ben_recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

# Save translation audit report
with open('backups/audit_20261016/translation_repair_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Updated datasets successfully written to:")
print("  - Dataset_ BanglaBBQ_Old/Politics/ (production)")
print("  - BanglaBBQ_Politics/ (canonical mirror)")
print("  - backups/audit_20261016/translation_repair_report.json")
