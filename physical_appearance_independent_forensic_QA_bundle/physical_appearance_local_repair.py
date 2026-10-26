#!/usr/bin/env python3
"""Authorized local-only, conservative bilingual alignment and language repairs.
Only changed fields in Bengali are touched; immutable originals remain untouched.
"""
import csv,json,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
src_en=ROOT/'ORIGINAL/banglabbq_physical_appearance_english.jsonl';src_bn=ROOT/'ORIGINAL/banglabbq_physical_appearance_bengali.jsonl'
dst_en=ROOT/'banglabbq_physical_appearance_audited_english.jsonl';dst_bn=ROOT/'banglabbq_physical_appearance_audited_bengali.jsonl'
E=[json.loads(x) for x in src_en.read_text(encoding='utf8').splitlines()]
B=[json.loads(x) for x in src_bn.read_text(encoding='utf8').splitlines()]
REPAIR={
 2:{'অভিনয় বা উপস্থাপনায় উপযুক্ততার':'পরিবেশনার উপযুক্ততার', 'অভিনয় বা উপস্থাপনায় উপযুক্ততা':'পরিবেশনার উপযুক্ততা'},
 6:{'পরিপাটি উপস্থাপনার যোগ্যতার':'উপস্থাপনার পরিপাট্যের',
    'পরিপাটি উপস্থাপনার যোগ্যতা':'উপস্থাপনার পরিপাট্য'},
 8:{'হাতের নিচের অংশে ছোট একটি দৃশ্যমান ট্যাটু আছে':'কনুই ও কবজির মাঝের অংশে ছোট একটি দৃশ্যমান ট্যাটু আছে',
    'হাতের নিচের অংশে কোনো ট্যাটু নেই':'কনুই ও কবজির মাঝের অংশে কোনো দৃশ্যমান ট্যাটু নেই'},
 9:{'দায়িত্বের প্রতি মনোযোগী থাকার সক্ষমতার':'অর্পিত কাজের প্রতি নিষ্ঠার',
    'দায়িত্বের প্রতি মনোযোগী থাকার সক্ষমতা':'অর্পিত কাজের প্রতি নিষ্ঠা'},
 10:{'সবার সামনে উপস্থাপনায় আত্মবিশ্বাসের':'জনসমক্ষে বক্তব্য দেওয়ার আত্মবিশ্বাসের',
     'সবার সামনে উপস্থাপনায় আত্মবিশ্বাস':'জনসমক্ষে বক্তব্য দেওয়ার আত্মবিশ্বাস'} }
issues={'2':'PA-LINGUISTIC-Q02','6':'PA-BILINGUAL-Q06','8':'PA-LINGUISTIC-Q08','9':'PA-BILINGUAL-Q09','10':'PA-LINGUISTIC-Q10'}
diffs=[]
for eid,row in enumerate(B):
    q=int(row['question_index']);qreps=REPAIR.get(q)
    if not qreps:continue
    for field in ('context','question'):
        old=row[field];new=old
        for a,b in qreps.items():new=new.replace(a,b)
        if new!=old:
            if field=='question' and q==8:raise AssertionError('Q08 change should be in context only')
            row[field]=new
            diffs.append({'issue_id':issues[str(q)],'language':'Bengali','example_id':eid,'jsonl_line':eid+1,'id':row['id'],
                'theme':f'Q{q:02d}','variation':f'V{eid//480+1}','orientation':row['additional_metadata']['version'],
                'condition':row['context_condition'],'polarity':row['question_polarity'],
                'field':field,'before':old,'after':new,'status':'APPLIED_LOCAL_ONLY'})
# English is already semantically faithful for these targeted terms; preserve byte identity.
dst_en.write_bytes(src_en.read_bytes())
with dst_bn.open('w',encoding='utf8',newline='\n') as f:
    for r in B:f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
with (ROOT/'physical_appearance_change_manifest.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(diffs[0]));w.writeheader();w.writerows(diffs)
summary={'field_changes':len(diffs),'records_modified':len(set(x['example_id'] for x in diffs)),
 'affected_themes':sorted(set(x['theme'] for x in diffs)),
 'english_byte_identical':dst_en.read_bytes()==src_en.read_bytes(),
 'bengali_different':dst_bn.read_bytes()!=src_bn.read_bytes(),
 'english_sha256':hashlib.sha256(dst_en.read_bytes()).hexdigest(),
 'bengali_sha256':hashlib.sha256(dst_bn.read_bytes()).hexdigest(),
 'question_index_untouched':all(a['question_index']==b['question_index'] for a,b in zip(E,B))}
(ROOT/'local_repair_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
