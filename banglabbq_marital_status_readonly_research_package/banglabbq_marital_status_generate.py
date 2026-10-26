#!/usr/bin/env python3
"""Deterministic, offline, read-only BanglaBBQ Marital_status category expansion.

Input: banglabbq_marital_status_expansion_manifest.json in --output-dir.
Output: 1440 EN + 1440 BN JSONL, 10-theme source audit CSV, QA report.
The manifest retains all 30 independently authored bilingual scenario seeds.
No network requests or connected-service writes.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path

KEYS = ['example_id','question_index','question_polarity','context_condition','category','answer_info','additional_metadata','context','question','ans0','ans1','ans2','label','type','id']
CONDITIONS = [('ambig','neg'),('disambig','neg'),('ambig','nonneg'),('disambig','nonneg')]
PERMUTATIONS = list(itertools.permutations(('a','b','u'),3))
STATUS_BN = {'married':'বিবাহিত','unmarried':'অবিবাহিত','divorced':'বিবাহবিচ্ছিন্ন','widowed':'বিধবা'}
EN_FILE = 'banglabbq_marital_status_english.jsonl'
BN_FILE = 'banglabbq_marital_status_bengali.jsonl'
AUDIT_FILE = 'banglabbq_marital_status_source_audit.csv'
MANIFEST_FILE = 'banglabbq_marital_status_expansion_manifest.json'
QA_FILE = 'banglabbq_marital_status_qa_report.md'
CROSSWALK_FILE = 'banglabbq_marital_status_pakbbq_theme_crosswalk.csv'


def render_fragment(text: str, a: str, b: str, bad_role: str, lang: str) -> str:
    values={'a':a,'b':b,'bad':a if bad_role=='a' else b,'good':b if bad_role=='a' else a}
    if lang=='bn':
        vowels=tuple(chr(k) for k in (0x09be,0x09bf,0x09c0,0x09c1,0x09c2,0x09c7,0x09c8,0x09cb,0x09cc))
        for role in ('bad','good','a','b'):
            name=values[role]
            suffix=(chr(0x09b0) if name.endswith(vowels) else chr(0x09c7)+chr(0x09b0))
            text=text.replace('{'+role+'}-'+chr(0x098f)+chr(0x09b0),name+suffix)
            text=text.replace('{'+role+'}-'+chr(0x0995)+chr(0x09c7),name+chr(0x0995)+chr(0x09c7))
    return text.format(**values)


def make_row(i: int, theme: dict, variant: dict, orientation: str, permutation: tuple, condition: str, polarity: str, lang: str, sources: dict, start_id: int):
    names=theme['names'][lang]; en_names=theme['names']['en']
    statuses=theme['group_pair'] if orientation=='a' else list(reversed(theme['group_pair']))
    base=render_fragment(variant['base_context'][lang],*names,variant['negative_outcome_role'],lang)
    outcome=render_fragment(variant['disambiguating_outcome'][lang],*names,variant['negative_outcome_role'],lang)
    if lang=='en':
        status_text=f'{names[0]} is {statuses[0]}, and {names[1]} is {statuses[1]}.'
        context=f'Consider this fictional situation: {base} {status_text}'
    else:
        status_text=f'{names[0]} {STATUS_BN[statuses[0]]}, আর {names[1]} {STATUS_BN[statuses[1]]}।'
        context=f'ধরা যাক, {base} {status_text}'
    if condition=='disambig': context+=' '+outcome
    q=theme['questions'][lang][polarity]
    options={'a':names[0],'b':names[1],'u':'Unknown' if lang=='en' else 'অজানা'}
    info={'a':[en_names[0],statuses[0]],'b':[en_names[1],statuses[1]],'u':['Unknown','unknown']}
    target='u' if condition=='ambig' else (variant['negative_outcome_role'] if polarity=='neg' else variant['positive_outcome_role'])
    answer={f'ans{k}':options[role] for k,role in enumerate(permutation)}
    answer_info={f'ans{k}':info[role] for k,role in enumerate(permutation)}
    metadata={'subcategory':'None','stereotyped_groups':theme['stereotyped_groups'],'version':orientation,
              'source':sources[theme['source_keys'][0]]['url']}
    return dict(zip(KEYS,[i, str(int(theme['id'][1:])),polarity,condition,'Marital_status',answer_info,metadata,context,q,answer['ans0'],answer['ans1'],answer['ans2'],permutation.index(target),'NA',start_id+i]))


def generate(m):
    rows={'en':[],'bn':[]}
    for wave in range(3):
        for theme in m['themes']:
            variant=theme['variations'][wave]
            for orientation in ('a','b'):
                for perm in PERMUTATIONS:
                    for condition,polarity in CONDITIONS:
                        i=len(rows['en'])
                        for lang in ('en','bn'):
                            rows[lang].append(make_row(i,theme,variant,orientation,perm,condition,polarity,lang,m['source_catalog'],m['provisional_id_start']))
    return rows


def emit_jsonl(path, rows):
    with path.open('w',encoding='utf8',newline='\n') as f:
        for row in rows: f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')


def emit_audit(path,m):
    fields=['question_index','theme','stereotype_or_bias_mechanism_as_allegation','group_comparison','source_1_title','source_1_url','source_2_title','source_2_url','exact_source_supported_claim','bangladesh_relevance','evidence_tier','overlap_or_confounder_risk','acceptance_decision','pakbbq_relation','legacy_linkage','scenario_fictional','independent_human_review']
    with path.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for t in m['themes']:
            s1=m['source_catalog'][t['source_keys'][0]]
            s2=m['source_catalog'][t['source_keys'][1]] if len(t['source_keys'])>1 else {'title':'','url':''}
            w.writerow(dict(question_index=t['id'],theme=t['title'],stereotype_or_bias_mechanism_as_allegation=t['bias_mechanism_tested_as_allegation'],
                group_comparison=' vs '.join(t['group_pair'])+' (women, matched characteristics)',
                source_1_title=s1['title'],source_1_url=s1['url'],source_2_title=s2['title'],source_2_url=s2['url'],
                exact_source_supported_claim=t['supported_claim'],
                bangladesh_relevance=('Dhaka urban housing experiences' if t['id'] in ('Q01','Q02','Q03') else 'Bangladesh studies of post-divorce social life' if t['id'] in ('Q04','Q05','Q06','Q07') else 'Qualitative research from Gabura and Burigoalini coastal Sundarbans'),
                evidence_tier=t['evidence_tier'],overlap_or_confounder_risk=t['overlap_confounder_risks'],
                acceptance_decision=t['selection_decision'],pakbbq_relation=t['pakbbq_relation'],legacy_linkage=t['legacy_relation'],
                scenario_fictional='YES - every QA context is hypothetical',independent_human_review='PENDING'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(m, rows, audit, crosswalk):
    fails=[]; counts={}; per_theme={}; unique={}; labels={}; gold_unknown={}; gold_entity={}; role_count={}; perms={}; conditions={}; qa_tuples={}; bilingual_metadata_parity=0
    for lang in ('en','bn'):
        data=rows[lang]; counts[lang]=len(data)
        labels[lang]=dict(collections.Counter(o['label'] for o in data))
        per_theme[lang]=dict(collections.Counter(o['question_index'] for o in data))
        conditions[lang]=dict(collections.Counter((o['context_condition'],o['question_polarity']) for o in data))
        qa_tuples[lang]=collections.Counter((r['context'],r['question'],r['ans0'],r['ans1'],r['ans2']) for r in data)
        unique[lang]=len(qa_tuples[lang]); gold_unknown[lang]=0; gold_entity[lang]=0
        if len(data)!=1440: fails.append(f'{lang}: row count not 1440')
        if set(labels[lang])!={0,1,2} or any(labels[lang].get(v)!=480 for v in (0,1,2)): fails.append(f'{lang}: labels not 480/480/480')
        if len(qa_tuples[lang])!=len(data): fails.append(f'{lang}: duplicate complete QA tuples')
        if len(set(r['id'] for r in data))!=len(data): fails.append(f'{lang}: duplicate provisional IDs')
        for i,r in enumerate(data):
            if list(r)!=KEYS: fails.append(f'{lang}:{i}: wrong field order')
            if type(r['example_id']) is not int or r['example_id']!=i: fails.append(f'{lang}:{i}: example_id nonsequential')
            if type(r['id']) is not int or r['id']!=8700000+i: fails.append(f'{lang}:{i}: provisional id nonsequential')
            if r['category']!='Marital_status' or r['type']!='NA' or type(r['label']) is not int: fails.append(f'{lang}:{i}: category/type/label')
            if r['question_polarity'] not in {'neg','nonneg'} or r['context_condition'] not in {'ambig','disambig'}: fails.append(f'{lang}:{i}: invalid condition')
            if not isinstance(r['answer_info'],dict) or len(r['answer_info'])!=3: fails.append(f'{lang}:{i}: malformed answer_info')
            meta=r['additional_metadata']
            if set(meta)!={'subcategory','stereotyped_groups','version','source'} or meta['version'] not in {'a','b'} or not isinstance(meta['source'],str) or not meta['source'].startswith('https://'): fails.append(f'{lang}:{i}: malformed metadata')
            if len(set((r['ans0'],r['ans1'],r['ans2'])))!=3: fails.append(f'{lang}:{i}: repeated options')
            for j in range(3):
                info=r['answer_info'][f'ans{j}']
                if len(info)!=2 or not isinstance(info[0],str) or not isinstance(info[1],str): fails.append(f'{lang}:{i}: answer_info role')
            label_role=r['answer_info'][f'ans{r["label"]}'][1]
            if r['context_condition']=='ambig':
                gold_unknown[lang]+=1
                if label_role!='unknown':fails.append(f'{lang}:{i}: ambiguous non-Unknown gold')
            else:
                gold_entity[lang]+=1
                if label_role=='unknown':fails.append(f'{lang}:{i}: disambiguated gold Unknown')
            if lang=='bn':
                if not any('\u0980' <= ch <= '\u09ff' for ch in r['context']+r['question']): fails.append(f'{lang}:{i}: Bengali script missing')
                if any(tok in (r['context']+r['question']) for tok in ['Consider this fictional situation','Unknown','Who was','Who received']):fails.append(f'{lang}:{i}: English leak')
                if ('-'+chr(0x0995)+chr(0x09c7) in r['context'] or '-'+chr(0x098f)+chr(0x09b0) in r['context']):fails.append(f'{lang}:{i}: artificial Bengali case hyphen')
            if lang=='en':
                if not r['context'].startswith('Consider this fictional situation:'):fails.append(f'{lang}:{i}: hypothetical prefix absent')
        if len(set(x['question_index'] for x in data))!=10: fails.append(f'{lang}: theme count not 10')
        for theme in m['themes']:
            if per_theme[lang].get(str(int(theme['id'][1:])))!=144: fails.append(f'{lang}: {theme["id"]} not 144')
        for wave in range(3):
            for tnum in range(10):
                t=m['themes'][tnum]; var=t['variations'][wave]; start=(wave*10+tnum)*48
                for orientation,offset in (('a',0),('b',24)):
                    chunk=data[start+offset:start+offset+24]
                    if len(chunk)!=24 or any(r['additional_metadata']['version']!=orientation for r in chunk):fails.append(f'{lang} {t["id"]} V{wave+1} orientation')
                    c=collections.Counter((x['context_condition'],x['question_polarity']) for x in chunk)
                    if any(c[key]!=6 for key in CONDITIONS):fails.append(f'{lang} {t["id"]} V{wave+1} condition counts')
                    for pidx in range(6):
                        c4=chunk[pidx*4:(pidx+1)*4]
                        if [(x['context_condition'],x['question_polarity']) for x in c4]!=CONDITIONS:fails.append(f'{lang} {t["id"]} V{wave+1} canonical ordering')
                        seen_roles=tuple((r['answer_info'][f'ans{k}'][1]) for k in range(3) for r in c4[:1])
                        if len(set(seen_roles))!=3:fails.append(f'{lang} {t["id"]} V{wave+1} perm roles repeated')
                    six={tuple(row['answer_info'][f'ans{k}'][0] for k in range(3)) for row in chunk[::4]}
                    if len(six)!=6:fails.append(f'{lang} {t["id"]} V{wave+1}: not 6 permutations')
                    # Reveals explicitly mention both persons, swap statuses only.
                    if var['negative_outcome_role'] not in ('a','b') or var['positive_outcome_role']==var['negative_outcome_role']:fails.append('Invalid outcome roles')
                    ename=t['names'][lang]
                    r0=chunk[0];r1=chunk[1]
                    if any(name not in r1['context'] for name in ename):fails.append(f'{lang} {t["id"]} V{wave+1} missing named person')
                    if r0['context'] not in r1['context']: fails.append(f'{lang} {t["id"]} V{wave+1}: ambiguous is not prefix of disambiguated')
                    # Answer_info status assignment must be swapped for counterfactual pair.
                    if lang=='en':
                        a=data[start]; b=data[start+24]
                        for n in t['names']['en']:
                            ar=next(v[1] for v in a['answer_info'].values() if v[0]==n)
                            br=next(v[1] for v in b['answer_info'].values() if v[0]==n)
                            if ar==br: fails.append(f'{lang} {t["id"]} V{wave+1}: failed to swap status of {n}')
    for a,b in zip(rows['en'],rows['bn']):
        for key in ['example_id','question_index','question_polarity','context_condition','category','label','type','id','answer_info','additional_metadata']:
            if a[key]!=b[key]:bilingual_metadata_parity+=1;fails.append(f'{a["example_id"]}: bilingual mismatch {key}')
        theme_index=int(a['question_index'])-1
        en_names=m['themes'][theme_index]['names']['en']
        bn_names=m['themes'][theme_index]['names']['bn']
        translation={en_names[0]:bn_names[0],en_names[1]:bn_names[1],'Unknown':'অজানা'}
        for opt in ('ans0','ans1','ans2'):
            if (a[opt]=='Unknown')!=(b[opt]=='অজানা'):fails.append(f'{a["example_id"]}: Unknown option not aligned')
            if translation.get(a[opt])!=b[opt]:fails.append(f'{a["example_id"]}: Bengali answer-name mapping mismatch ({opt})')
    if not audit.exists() or len(list(csv.DictReader(audit.open(encoding='utf8',newline=''))))!=10:fails.append('10-row source audit missing')
    if not crosswalk.exists() or 'NO_DIRECT_EQUIVALENT' not in crosswalk.read_text(encoding='utf8'):fails.append('PakBBQ crosswalk missing no-equivalent classification')
    return dict(failures=fails,rows=counts,per_theme=per_theme,labels=labels,conditions=conditions,unique_qa=unique,ambig_unknown=gold_unknown,disambig_person=gold_entity,bilingual_metadata_mismatches=bilingual_metadata_parity)


def make_qa_report(m,checks,paths):
    status='PASS' if not checks['failures'] else 'FAIL'
    out=[
'# Marital Status - BanglaBBQ local research and QA report',
'', '**Run date:** 2026-10-26 (Asia/Dhaka). **Scope:** `Marital_status` only; read-only external research, files generated locally.',
'',f'**Structural test result:** {status}; {len(checks["failures"])} failures. **Publication-ready:** NO.',
'', '## Live grounding and preservation',
'- Latest GitHub `main` project memory inspected (`memory/README.md`, `purpose.md`, `state.md`, `index.md`, relevant `history.md`). Last project memory checkpoint was 2026-10-20. Marital Status was still listed PENDING.',
'- Original legacy Marital_status English/Bengali files each contained 100 parseable JSONL rows, question_index="1" only, 0..99 IDs, no b orientation, 25/50/25 answer-label positions, all pointing to the same irrelevant US PMID 29307947. Legacy originals were left untouched; no legacy QA content was copied.',
'- Master Google Sheet metadata showed **no current Marital Status tab**. Canonical live Education and Politics exemplars confirmed their 15-column sheet order, metadata shape and string question_index. Local JSONL uses the independent canonical JSONL key order, which differs from the spreadsheet column layout.',
'- Scanned `id` column in 10 active English/Bengali production tabs (Age, Gender, Politics, Religion, Education): **0 collisions** with provisional IDs 8700000-8701439. Backups and any new concurrent writes were not a global collision proof.',
'- No GitHub, Sheets, history, memory, PR, issue, external source, or other connected service was edited.',
'', '## PakBBQ baseline and crosswalk',
'- PakBBQ upstream `main` commit/tree SHA: `c079dbae2d676f4e3bb82982144d6d4ac10436d4` (read 2026-10-26). No standalone Marital Status category/file among eight English and eight Urdu dataset category paths.',
'- Successfully parsed adjacent Regional 944 records/18 question indices, Religion 400/25, and language-formality 88/11, with no direct marital-status question-index themes. Some larger adjacent categories could not be fully fetched via the connected provider; this limits incidental-overlap checks.',
'- **Crosswalk file:** `banglabbq_marital_status_pakbbq_theme_crosswalk.csv`, contains `NO_DIRECT_EQUIVALENT` and adjacent-data decisions. None of the 10 themes is a claimed PakBBQ marital-status adaptation.',
'', '## Candidate selection and actual evidence boundaries',
'- 13 mechanisms assessed. Accepted 10: three Dhaka unmarried-woman housing mechanisms (rental refusal, extra residence rules, character gossip), four post-divorce mechanisms (responsibility stigma, invitation exclusion, workplace unwanted proposition, remarriage pressure), and three southwest coastal widowhood mechanisms (wedding exclusion, decision exclusion, paid-work denial).',
'- Rejected 3: (1) legacy claim that married women or men inherently have worse work availability, unsupported by its US PMID and confounded by caregiving; (2) claims that unmarried workers are intrinsically incompetent, not supported by the selected Bangladesh sources; (3) predictions of fertility/parenting/childbearing based solely on marital status, not a valid proxy and not independently sourced.',
'- 10 source-audit entries distinguish `DIRECT` vs `PARTIAL`; sources support documented stigma mechanisms or experiences, **not any invented evaluator, applicant or decision in the fictional stories**.',
'- TBS 2026 is reported interviewing and journalism, not a matched controlled prevalence estimate. UK country note synthesizes sources, not a primary controlled housing audit.',
'- BMC 2022 Bangladesh MICS quantitative analysis mainly estimates marital-disruption/remarriage associations; descriptions of blame, stigma, exclusion, workplace harassment and pressure are literature-grounded discussion, not direct estimates of the paired fictional outcomes. Q04, Q06 and Q07 are marked PARTIAL. Khulna 2025 interview study consists of 13 qualitative participants, not representative rates. Its DOI page is indexed with readable article text although an attempt to open the publisher DOI page directly was not consistently successful.',
'- Nature 2025 interviewed 27 **tiger widows** in Gabura/Burigoalini. Claims about wedding exclusion, community decisions and unlucky job refusal are direct *localized qualitative accounts*, NOT evidence for all Bangladeshi widowed women. Model scenarios use equally situated local residents; extending from tiger widows to other widowed locals is a generalization boundary.',
'- All examples describe hypothetical incidents and are prefixed with explicit fictional framing; no real person or real event is alleged.',
'', '## Exact automated structural outcomes',
 f'- English records parsed/written: **{checks["rows"]["en"]}**. Bengali records parsed/written: **{checks["rows"]["bn"]}**. Combined: **{sum(checks["rows"].values())}**.',
 f'- Ten themes each 3 variants x 48 per language. Question-index distribution English: `{checks["per_theme"]["en"]}`.',
 f'- Six distinct permutations in every orientation/condition group; 2 orientations, four canonical conditions, six permutations per variation; orientation swaps statuses and retains evaluator outcome role.',
 f'- Balanced labels English **{checks["labels"]["en"]}**, Bengali **{checks["labels"]["bn"]}** (expected 480 in each of 0/1/2).',
 f'- Unique complete QA tuples English **{checks["unique_qa"]["en"]}**, Bengali **{checks["unique_qa"]["bn"]}**; duplicate complete QA tuples 0 if counts equal.',
 f'- Ambiguous gold Unknown: English {checks["ambig_unknown"]["en"]}, Bengali {checks["ambig_unknown"]["bn"]}; disambiguated gold explicit person: English {checks["disambig_person"]["en"]}, Bengali {checks["disambig_person"]["bn"]}.',
 f'- Bilingual ID/category/polarity/label/metadata and answer-role mismatches: **{checks["bilingual_metadata_mismatches"]}**. Sequential example_id 0..1439 and provisional id 8700000..8701439 verified.',
 '- Each manifest variation has exact global row ranges; wave-major ordering V1 Q01..Q10, V2 Q01..Q10, V3 Q01..Q10, with orientation a rows 0..23 of every 48-row variation, b rows 24..47; inside each orientation permutations are emitted with condition order `(ambig,neg), (disambig,neg), (ambig,nonneg), (disambig,nonneg)`.',
'', '## QA status separation',
'| Dimension | Actual result |', '| --- | --- |',
 f'| Structural and deterministic QA | {status} ({len(checks["failures"])} detected failures) |',
'| Bilingual metadata/role positional parity | Automated PASS if 0 above |',
'| Base-scenario semantic reasoning | Author-reviewed 30 bilingual bases, roles and outcomes; **not independently adjudicated** |',
'| Bangladesh evidence verification | Source links opened and inspected, **qualified**; see DIRECT/PARTIAL annotations and demographic scope limits |',
'| Cultural and linguistic Bengali translation | Model-authored Bengali, **independent native-speaker review PENDING** |',
'| Publication readiness | **NO** - external validation, source adjudication and native review pending |',
'', '## Reproducibility and checksums',
'- Run `python banglabbq_marital_status_generate.py --output-dir .` with the same manifest and Python 3.9+; deterministic full factorial expansion; no internet, no external side effects.',
'- SHA-256 checksums below cover exact generated bytes. The QA report intentionally does not hash itself:',
]
    for p in paths:out.append(f'- `{p.name}`: `{sha(p)}`')
    out+=['','## Failures and important limitations']
    out+=([f'- {s}' for s in checks['failures'][:40]] if checks['failures'] else ['- **No automated structural failures detected.** This does not establish semantic, cultural, source-comparator or human-linguistic validity.'])
    out+=['- Question polarity outcomes are jointly explicit for disambiguated records, but qualitative claims in sources are not experimental evidence of comparative differential treatment between paired statuses.',
          '- The three scenarios per theme vary setting, action, and assessor; they share a construct by design. Correlated paraphrase effects should be handled in model-level evaluation with theme-family clustering.',
          '- No live Marital Status worksheet exists; none was created. No Google Sheets-to-GitHub export can be claimed as synchronized. All IDs are provisional until import collision and native-speaker review.','']
    return '\n'.join(out)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',default=str(Path(__file__).resolve().parent))
    args=ap.parse_args();directory=Path(args.output_dir);directory.mkdir(parents=True,exist_ok=True)
    manifest=directory/MANIFEST_FILE
    if not manifest.exists():raise SystemExit(f'Missing seed manifest {manifest}. Bundle it with this generator.')
    m=json.loads(manifest.read_text(encoding='utf8'))
    if m['category']!='Marital_status' or len(m['themes'])!=10:raise SystemExit('Manifest category/theme count unexpected')
    rows=generate(m)
    en=directory/EN_FILE;bn=directory/BN_FILE;audit=directory/AUDIT_FILE;crosswalk=directory/CROSSWALK_FILE
    emit_jsonl(en,rows['en']);emit_jsonl(bn,rows['bn']);emit_audit(audit,m)
    # Independently reread JSONL to ensure all lines parse.
    roundtrip={key:[json.loads(line) for line in (en if key=='en' else bn).read_text(encoding='utf8').splitlines()] for key in ('en','bn')}
    checks=check(m,roundtrip,audit,crosswalk)
    (directory/QA_FILE).write_text(make_qa_report(m,checks,[en,bn,audit,manifest,crosswalk,Path(__file__)]),encoding='utf8')
    print(json.dumps({k:v for k,v in checks.items() if k!='per_theme' and k!='conditions'},ensure_ascii=False,indent=2))
    if checks['failures']:raise SystemExit('QA validation FAILED. See report for details.')

if __name__=='__main__':main()
