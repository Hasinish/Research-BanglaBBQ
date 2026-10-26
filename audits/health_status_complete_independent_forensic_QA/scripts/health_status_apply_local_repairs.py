#!/usr/bin/env python3
"""Apply evidence-conservative LOCAL ONLY repairs, preserving source files untouched.
Each mutation is traced by original JSONL line/field/issue and SHA256.
No remote access, Git, or Sheets calls.
"""
import csv,hashlib,json
from pathlib import Path
ROOT=Path('/mnt/data')
OUT=ROOT/'health_status_local_candidate'
OUT.mkdir(exist_ok=True)
FIELDS=['issue_id','severity','language','line','example_id','id','theme','variation','orientation','condition','polarity','field','original_value','revised_value','reason','status']
changes=[]
PATCHES=[
 ('HS-P01','P1',4,2,'english','context','is electing one new member','is selecting one new member','Electing implies voting while the chair makes the selection; align with Bengali.','all'),
 ('HS-P02','P1',9,2,'english','context','to score written descriptions','to review written descriptions','Bengali verifies/reviews written descriptions and not scoring; restore bilingual task parity.','all'),
 ('HS-P03','P1',6,3,'english','context','history study pair','history study group','Study pair with an existing leader cannot be expanded to three without definition.','all'),
 ('HS-P03','P1',6,3,'english','context','to the study pair','to the study group','Harmonize explicit join destination after changing group size.','all'),
 ('HS-P03','P1',6,3,'english','question','study pair','study group','Question must target same study group as context.','all'),
 ('HS-P04','P1',3,3,'english','context','peer mentor','assistant trainer','Peer mentor in office training is closer to assistant trainer than co-teacher.','all'),
 ('HS-P04','P1',3,3,'english','question','peer mentor','assistant trainer','Align role designation in context/question and Bengali.','all'),
 ('HS-P04','P1',3,3,'bengali','context','সহশিক্ষক','সহপ্রশিক্ষক','Use appropriate assistant trainer rather than co-teacher for an office training session.','all'),
 ('HS-P04','P1',3,3,'bengali','question','সহশিক্ষক','সহপ্রশিক্ষক','Maintain one-to-one role correspondence.','all'),
 ('HS-P05','P2',6,1,'english','context','an indoor debate-reading circle','an informal debate-reading circle','Bengali ঘরোয়া implies informal rather than indoor; harmonize.','all'),
 ('HS-P06','P2',5,1,'bengali','context','সাজিদ কোভিড-১৯ রোগের কোনো ইতিহাস নেই','সাজিদ আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning of never having COVID-19.','all'),
 ('HS-P06','P2',5,1,'bengali','context','অনিক কোভিড-১৯ রোগের কোনো ইতিহাস নেই','অনিক আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning.','all'),
 ('HS-P06','P2',5,2,'bengali','context','সাজিদ কোভিড-১৯ রোগের কোনো ইতিহাস নেই','সাজিদ আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning.','all'),
 ('HS-P06','P2',5,2,'bengali','context','অনিক কোভিড-১৯ রোগের কোনো ইতিহাস নেই','অনিক আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning.','all'),
 ('HS-P06','P2',5,3,'bengali','context','সাজিদ কোভিড-১৯ রোগের কোনো ইতিহাস নেই','সাজিদ আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning.','all'),
 ('HS-P06','P2',5,3,'bengali','context','অনিক কোভিড-১৯ রোগের কোনো ইতিহাস নেই','অনিক আগে কখনো কোভিড-১৯-এ আক্রান্ত হননি','Repair ungrammatical Bengali missing genitive; keep meaning.','all'),
 ('HS-P07','P2',8,3,'bengali','context','বার্তাপত্রর','বার্তাপত্রের','Repair erroneous Bengali noun-genitive suffix.','all'),
 ('HS-P07','P2',8,3,'bengali','question','বার্তাপত্রর','বার্তাপত্রের','Repair erroneous Bengali noun-genitive suffix.','all'),
 ('HS-P07','P2',10,3,'bengali','context','বার্তাপত্রর','বার্তাপত্রের','Repair erroneous Bengali noun-genitive suffix.','all'),
 ('HS-P08','P2',9,3,'bengali','context','দুজনই এ বসে করা যায় এমন দায়িত্ব পালনে সক্ষম','কাজটি বসে করা যায় এবং দুজনই দায়িত্বটি পালনে সক্ষম','Correct unidiomatic Bengali phrase while retaining identical ability/fitness.','all'),
 ('HS-P09','P2',8,1,'bengali','context','শিক্ষার্থী পত্রিকার','শিক্ষার্থীদের পত্রিকার','Correct Bengali plural possessive in student newspaper term.','all'),
 ('HS-P09','P2',8,1,'bengali','context','কাজটি ডেস্কে বসে লেখা সম্পাদনা করা','কাজটি ডেস্কে বসে লেখা সম্পাদনার','Improve idiomatic modifier while preserving desk editing.','all'),
]

def variation(i):return i//480+1
def theme(i):return i%480//48+1

def main():
 en=[json.loads(s) for s in (ROOT/'banglabbq_health_status_english.jsonl').read_text().splitlines()]
 bn=[json.loads(s) for s in (ROOT/'banglabbq_health_status_bengali.jsonl').read_text().splitlines()]
 for iid,severity,q,v,lang,field,old,new,reason,condition in PATCHES:
  rows=en if lang=='english' else bn
  start=(v-1)*480+(q-1)*48;end=start+48
  hit=0
  for i in range(start,end):
   r=rows[i];present=r[field]
   if old not in present:continue
   revised=present.replace(old,new)
   assert revised!=present
   r[field]=revised;hit+=1
   changes.append(dict(issue_id=iid,severity=severity,language=lang,line=i+1,example_id=r['example_id'],id=r['id'],theme=f'Q{q:02d}',variation=f'V{v}',orientation=r['additional_metadata']['version'],condition=r['context_condition'],polarity=r['question_polarity'],field=field,original_value=present,revised_value=revised,reason=reason,status='APPLIED_LOCAL_ONLY'))
  assert hit>0,(iid,lang,field,old,q,v)
  print(iid,lang,q,v,field,'hits',hit)
 for lang,rows in [('english',en),('bengali',bn)]:
  path=ROOT/f'health_status_audited_{lang}.jsonl'
  path.write_text(''.join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in rows),encoding='utf-8')
  print('saved',path,'SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
 path=ROOT/'health_status_change_manifest.csv'
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(changes)
 print('applied total field-cell edits',len(changes),'unique affected rows',len(set((x['language'],x['example_id']) for x in changes)))
 stats={'change_count':len(changes),'distinct_changed_language_rows':len(set((x['language'],x['example_id']) for x in changes)),
  'english_changes':sum(x['language']=='english' for x in changes),'bengali_changes':sum(x['language']=='bengali' for x in changes),
  'unique_issue_ids':sorted(set(x['issue_id'] for x in changes)), 'file_sha256':{}}
 for lang in ('english','bengali'):
  stats['file_sha256'][lang]=hashlib.sha256((ROOT/f'health_status_audited_{lang}.jsonl').read_bytes()).hexdigest()
 (ROOT/'health_status_local_repair_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
