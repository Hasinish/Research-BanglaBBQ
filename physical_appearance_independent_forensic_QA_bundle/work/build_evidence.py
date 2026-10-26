import csv,json,pathlib,collections
root=pathlib.Path('/mnt/data/physical_appearance_forensic_qa');data=json.loads((root/'work/evidence_observations.json').read_text());old=list(csv.DictReader(open('/mnt/data/banglabbq_physical_appearance_source_audit.csv')))
rows=[]
for row in old:
 q=row['theme_id'];review=data['themes'][q]
 rows.append({'theme':q,'original_theme_title':row['theme'],'group_comparison':row['group_comparison'],'claimed_mechanism':row['mechanism_tested_as_allegation'],
 'primary_url':row['source_1_url'],'primary_cited_title':row['source_1_title'],'primary_access':review['source1'],'primary_date':review['source1_date'],
 'secondary_url':row['source_2_url'],'secondary_cited_title':row['source_2_title'],'secondary_access':review['source2'],'secondary_date':review['source2_date'],
 'primary_source_is_Bangladesh_specific':'YES' if q!='Q05' else 'YES; second source global study is not Bangladesh-specific height evidence',
 'actual_verified_claim':review['supported'],'unverified_extrapolation_and_confounders':review['limitations'],
 'original_evidence_tier':row['evidence_tier'],'independent_evidence_tier':review['tier'],'tier_changed':'YES' if row['evidence_tier']!=review['tier'] else 'NO',
 'decision':review['decision'],'source_verification':'AI_RESEARCH_REVIEW','source_locator':review['citations'],'retrieval_date':data['retrieval_date'],
 'source_verification_note':'fictional incidents are not facts; source supports stereotype/discourse only'})
out=root/'physical_appearance_source_evidence_matrix.csv'
with out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('evidence rows',len(rows),'tiers',dict(collections.Counter(r['independent_evidence_tier'] for r in rows)),'changed',[(x['theme'],x['original_evidence_tier'],x['independent_evidence_tier']) for x in rows if x['tier_changed']=='YES'])
