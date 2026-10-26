#!/usr/bin/env python3
import collections,csv,hashlib,json,pathlib,itertools
R=pathlib.Path(__file__).resolve().parents[1]
res={}
for stage in ['ORIGINAL','AUDITED']:
    D={}
    for lang in ['english','bengali']:
        p=(R/'ORIGINAL'/f'banglabbq_physical_appearance_{lang}.jsonl') if stage=='ORIGINAL' else R/f'banglabbq_physical_appearance_audited_{lang}.jsonl'
        data=[json.loads(z) for z in p.read_text(encoding='utf-8').splitlines()]
        group=collections.Counter(str(x['question_index']) for x in data)
        condition=collections.Counter(f"{x['context_condition']}+{x['question_polarity']}" for x in data)
        answer_positions=collections.Counter(x['label'] for x in data)
        orient=collections.Counter(x['additional_metadata']['version'] for x in data)
        tupes=[(x['context'],x['question'],x['ans0'],x['ans1'],x['ans2']) for x in data]
        D[lang]={'rows':len(data),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':len(p.read_bytes()),'unique_full_tuples':len(set(tupes)),'unique_context_strings':len(set(x['context'] for x in data)),'unique_question_strings':len(set(x['question'] for x in data)),'unique_themes':len(group),'theme_row_counts':dict(group),'condition_polarity':dict(condition),'answer_position_counts':dict(answer_positions),'orientations':dict(orient),'id_min':min(x['id'] for x in data),'id_max':max(x['id'] for x in data),'all_15_fields':all(len(x)==15 for x in data),'all_nonblank':all(all(str(x[k]) for k in ('context','question','ans0','ans1','ans2')) for x in data)}
    res[stage]=D
res['source_assessment']={}
for row in csv.DictReader((R/'physical_appearance_source_evidence_matrix.csv').open()):res['source_assessment'][row['theme']]={'tier':row['independent_evidence_tier'],'decision':row['decision'],'original_tier':row['original_evidence_tier']}
(R/'physical_appearance_structural_metrics.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:{lang:{k:d[k] for k in ('rows','unique_themes','unique_full_tuples','unique_context_strings','unique_question_strings','answer_position_counts','condition_polarity','orientations')} for lang,d in val.items()} for key,val in res.items() if key in ('ORIGINAL','AUDITED')},indent=2))
