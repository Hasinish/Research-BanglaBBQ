#!/usr/bin/env python3
"""Apply only reviewed local Social_status fixes to immutable exact-hash originals.

Never touches GitHub or Sheets. Raises on SHA-256 mismatch or stale original field;
preserves 15-key JSONL schema, EIDs, roles, labels, IDs and order.
"""
import argparse,csv,hashlib,json,pathlib,collections,sys
PREF='banglabbq_social_status_'
EXPECTED={'english':'40d7a9aae0a51285ceaa6cad83a317fdd70e0fcb4b8c47cbdadf3e3432ed3705','bengali':'ebbf776c88d35593610241eda7913d0ec7fe8522d68c5eec236f080a8a783589'}

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--original-dir',type=pathlib.Path,required=True);p.add_argument('--changes',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--expected-out-sha-json',type=pathlib.Path,required=False);args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    change=list(csv.DictReader(args.changes.open('r',encoding='utf-8-sig',newline='')))
    out={};n=collections.Counter()
    for lang in ('english','bengali'):
        f=args.original_dir/(PREF+lang+'.jsonl');raw=f.read_bytes();assert sha(raw)==EXPECTED[lang],f'original SHA mismatch: {f}: {sha(raw)}'
        rs=[json.loads(x) for x in raw.decode('utf-8').splitlines()]
        assert len(rs)==1440
        old_ident=[(r['example_id'],r['id'],r['label'],r['category'],r['question_index']) for r in rs]
        key='en' if lang=='english' else 'bn'
        for rec in change:
            if rec['language']!=key:continue
            eid=int(rec['example_id']);field=rec['field'];r=rs[eid]
            assert r['example_id']==eid and r['id']==int(rec['id'])
            assert field in ('context','question'),f'not approved edit field {field}'
            assert r[field]==rec['original'],f'changed base at {lang} EID {eid} {field}'
            r[field]=rec['revised'];n[lang]+=1
        assert [(r['example_id'],r['id'],r['label'],r['category'],r['question_index']) for r in rs]==old_ident
        dest=args.out/(PREF+'audited_'+lang+'.jsonl')
        with open(dest,'w',encoding='utf-8',newline='\n') as h:
            for rec in rs:h.write(json.dumps(rec,ensure_ascii=False,separators=(',',':'))+'\n')
        out[lang]={'path':str(dest),'sha256':sha(dest.read_bytes()),'rows':len(rs),'edits':n[lang]}
    if args.expected_out_sha_json:
        expected=json.loads(args.expected_out_sha_json.read_text(encoding='utf-8'))['candidate_sha256']
        for lang,x in out.items():assert x['sha256']==expected[lang],f'candidate reconstruction SHA mismatch {lang}'
    print(json.dumps({'status':'REPRODUCED_LOCAL_CANDIDATES','outputs':out},indent=2))
if __name__=='__main__':sys.exit(main())
