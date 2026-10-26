#!/usr/bin/env python3
"""Produce new LOCAL-only edited templates and regenerate candidate JSONLs.
No remote writes, no modification of immutable ORIGINAL/ snapshots.
"""
import pathlib,json,shutil,subprocess,sys,csv,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parent
ORIG=ROOT/'ORIGINAL'; AUD=ROOT/'audited_generation'
AUD.mkdir(exist_ok=True)
T=json.loads((ORIG/'banglabbq_ethnicity_scenario_templates.json').read_text(encoding='utf-8'))
CHANGE_LOG=[]
def change(q,v,field,new,issue,reason):
    t=T[q-1];target=t if field=='eq' or field=='eqb' else t['variants'][v-1]
    key=field if isinstance(field,str) else field
    old=target[key]
    assert old!=new,(q,v,field)
    target[key]=new
    CHANGE_LOG.append({'theme':f'Q{q:02d}','variation':f'V{v}' if v else 'ALL','template_field':str(field),
                       'old':old,'new':new,'issue_id':issue,'reason':reason})
change(2,1,6,'received a lower mark for the essay','ETH-L002','English assessment phrasing made precise and idiomatic')
change(2,1,7,'প্রবন্ধে কম নম্বর পেয়েছে','ETH-L002','Bengali now refers to marks rather than abstract lower assessment')
change(2,1,8,'received a higher mark for the essay','ETH-L002','Opposed evaluation criterion paired explicitly')
change(2,1,9,'প্রবন্ধে বেশি নম্বর পেয়েছে','ETH-L002','Bengali now refers to higher marks')
change(4,1,6,'was not offered a rental agreement','ETH-L004','English aligned to Bengali absence of agreement rather than unentailed explicit refusal')
change(4,1,7,'ভাড়ার চুক্তির প্রস্তাব পায়নি','ETH-L004','Bengali specifies lack of offer')
change(4,3,2,'Both provide equally detailed rental references and equivalent tenancy documents.','ETH-L005','Unify English criterion and Bengali references')
change(4,3,3,'দুজনেই সমমানের সুপারিশপত্র ও সমতুল্য সম্পূর্ণ ভাড়াসংক্রান্ত কাগজপত্র দেয়।','ETH-L005','Remove unnatural Bengali compound পরিচিতি-সুপারিশ and align document equivalence')
change(5,3,1,'টাঙ্গাইলের একটি প্রসূতি সেবাকেন্দ্রে পরবর্তী সাক্ষাতের দিন নির্ধারণের সময়','ETH-L006','Avoid double সময় in Bengali time-setting clause')
change(10,0,'eq','have equal local residency, relevant experience, and eligibility to advise on the same community service issue.','ETH-P0001','Remove unsupported assertion of already equal speaking time conflicting with denied slot')
change(10,0,'eqb','একই এলাকায় বসবাস করে, একই জনসেবার বিষয়ে প্রাসঙ্গিক অভিজ্ঞতা ও পরামর্শ দেওয়ার যোগ্যতা সমান।','ETH-P0001','Remove contradictory prior speaking-time entitlement in Bengali and improve natural syntax')
(AUD/'banglabbq_ethnicity_scenario_templates.json').write_text(json.dumps(T,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['generate_ethnicity.py','validate_ethnicity_independent.py','banglabbq_ethnicity_pakbbq_theme_crosswalk.csv']:
    shutil.copy2(ORIG/name,AUD/name)
cp=subprocess.run([sys.executable,str(AUD/'generate_ethnicity.py'),'--directory',str(AUD)],capture_output=True,text=True)
(ROOT/'audited_generator_stdout.json').write_text(cp.stdout,encoding='utf-8')
(ROOT/'audited_generator_stderr.log').write_text(cp.stderr,encoding='utf-8')
if cp.returncode!=0:raise RuntimeError(f'Generator failed rc={cp.returncode}: '+cp.stderr[-2000:])
for lang,old_file,new_file in [('en','banglabbq_ethnicity_english.jsonl','banglabbq_ethnicity_audited_english.jsonl'),('bn','banglabbq_ethnicity_bengali.jsonl','banglabbq_ethnicity_audited_bengali.jsonl')]:
    shutil.copy2(AUD/old_file,ROOT/new_file)
shutil.copy2(AUD/'banglabbq_ethnicity_scenario_templates.json',ROOT/'Ethnicity_audited_scenario_templates.json')
shutil.copy2(AUD/'banglabbq_ethnicity_expansion_manifest.json',ROOT/'Ethnicity_audited_expansion_manifest.json')
with (ROOT/'Ethnicity_template_change_log.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=CHANGE_LOG[0].keys());writer.writeheader();writer.writerows(CHANGE_LOG)
rows=[]
for lang in ('en','bn'):
    orig=[json.loads(s) for s in (ORIG/('banglabbq_ethnicity_english.jsonl' if lang=='en' else 'banglabbq_ethnicity_bengali.jsonl')).read_text(encoding='utf-8').splitlines()]
    fixed=[json.loads(s) for s in (ROOT/('banglabbq_ethnicity_audited_english.jsonl' if lang=='en' else 'banglabbq_ethnicity_audited_bengali.jsonl')).read_text(encoding='utf-8').splitlines()]
    assert len(orig)==len(fixed)==1440
    for i,(a,b) in enumerate(zip(orig,fixed)):
        assert tuple(a)==tuple(b)
        for key in a:
            if a[key]!=b[key]:
                assert key in ('context','question'),(lang,i,key)
                q=int(a['question_index']); wave=i//480;v=wave+1
                issue='ETH-P0001' if q==10 else ('ETH-L002' if q==2 else ('ETH-L004' if q==4 and v==1 else ('ETH-L005' if q==4 else 'ETH-L006')))
                rows.append({'issue_id':issue,'language':lang,'file_original':'banglabbq_ethnicity_'+('english' if lang=='en' else 'bengali')+'.jsonl',
                             'line_number':i+1,'example_id':a['example_id'],'id':a['id'],'theme':f'Q{q:02d}','variation':f'V{v}',
                             'orientation':a['additional_metadata']['version'],'context_condition':a['context_condition'],'polarity':a['question_polarity'],
                             'field':key,'before':a[key],'after':b[key],'status':'APPLIED_LOCAL_ONLY'})
with (ROOT/'Ethnicity_change_manifest.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'template_edits':len(CHANGE_LOG),'modified_cells':len(rows),'modified_rows_by_language':{l:len({r['example_id'] for r in rows if r['language']==l}) for l in ('en','bn')},'modified_cells_by_field':{str(k):v for k,v in collections.Counter((r['language'],r['field']) for r in rows).items()},'generator_returncode':cp.returncode}
(ROOT/'local_corrections_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
