#!/usr/bin/env python3
import json,hashlib,sys,importlib.util,tempfile,subprocess,collections
from pathlib import Path
p=Path('/mnt/data/marital_forensic_qa');o=p/'ORIGINAL';m=json.loads((o/'banglabbq_marital_status_expansion_manifest.json').read_text('utf8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('legacy_gen',o/'banglabbq_marital_status_generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=[json.loads(a) for a in (p/'banglabbq_marital_status_audited_english.jsonl').read_text().splitlines()];B=[json.loads(a) for a in (p/'banglabbq_marital_status_audited_bengali.jsonl').read_text().splitlines()]
rawE=[json.loads(a) for a in (o/'banglabbq_marital_status_english.jsonl').read_text().splitlines()];rawB=[json.loads(a) for a in (o/'banglabbq_marital_status_bengali.jsonl').read_text().splitlines()]
orig_check=g.check(m,{'en':rawE,'bn':rawB},o/'banglabbq_marital_status_source_audit.csv',o/'banglabbq_marital_status_pakbbq_theme_crosswalk.csv')
audit_check=g.check(m,{'en':E,'bn':B},o/'banglabbq_marital_status_source_audit.csv',o/'banglabbq_marital_status_pakbbq_theme_crosswalk.csv')
assert len(orig_check['failures'])==0 and len(audit_check['failures'])==0
mapping_misses=[]
for entry in m['row_map']:
 start,end=entry['row_start'],entry['row_end_inclusive']
 for lang,rows in [('en',E),('bn',B)]:
  sel=rows[start:end+1]
  if not(len(sel)==24 and all(x['id']==8700000+x['example_id'] for x in sel) and all(x['additional_metadata']['version']==entry['orientation'] for x in sel) and all(x['example_id']==start+j for j,x in enumerate(sel)) and all(x['question_index']==str(int(entry['theme'][1:])) for x in sel)):
   mapping_misses.append((lang,entry))
assert not mapping_misses
with tempfile.TemporaryDirectory(prefix='marital_reproduce_') as temp:
 temp=Path(temp)
 import shutil
 for f in ['banglabbq_marital_status_expansion_manifest.json','banglabbq_marital_status_pakbbq_theme_crosswalk.csv']:
  shutil.copyfile(o/f,temp/f)
 run=subprocess.run([sys.executable,str(o/'banglabbq_marital_status_generate.py'),'--output-dir',str(temp)],capture_output=True,text=True,timeout=120)
 gen_equal={n:(temp/f'banglabbq_marital_status_{n}.jsonl').read_bytes()==(o/f'banglabbq_marital_status_{n}.jsonl').read_bytes() for n in ('english','bengali')}
 assert all(gen_equal.values())
 patchdir=temp/'candidate';patchrun=subprocess.run([sys.executable,str(p/'marital_status_apply_local_repairs.py'),'--english',str(temp/'banglabbq_marital_status_english.jsonl'),'--bengali',str(temp/'banglabbq_marital_status_bengali.jsonl'),'--outdir',str(patchdir)],capture_output=True,text=True,timeout=120)
 assert patchrun.returncode==0,patchrun.stderr
 edited_equal={n:(patchdir/f'banglabbq_marital_status_audited_{n}.jsonl').read_bytes()==(p/f'banglabbq_marital_status_audited_{n}.jsonl').read_bytes() for n in ('english','bengali')}
 assert all(edited_equal.values())
 manifest_equal=(patchdir/'marital_status_change_manifest.csv').read_bytes()==(p/'marital_status_change_manifest.csv').read_bytes()
 assert manifest_equal
 summary=dict(git_main_commit='e186b283fa5b184058e2cb395273e9968a893b20',local_original_sha256={lang:sha(o/f'banglabbq_marital_status_{lang}.jsonl') for lang in ('english','bengali')},candidate_sha256={lang:sha(p/f'banglabbq_marital_status_audited_{lang}.jsonl') for lang in ('english','bengali')},original_generator_return_code=run.returncode,original_generator_byte_parity=gen_equal,candidate_patch_return_code=patchrun.returncode,candidate_byte_parity=edited_equal,change_manifest_byte_parity=manifest_equal,original_generator_check_failures=len(orig_check['failures']),candidate_original_generator_check_failures=len(audit_check['failures']),manifest_row_map_checked=len(m['row_map']),manifest_map_failures=len(mapping_misses),upstream_generator_does_not_natively_recreate_patches=True,external_writes=0)
 (p/'work/reproducibility_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
