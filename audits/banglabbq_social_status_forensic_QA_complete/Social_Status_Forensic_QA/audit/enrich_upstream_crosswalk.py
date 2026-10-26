#!/usr/bin/env python3
"""Enrich 35-index crosswalk with exact source-presence aggregates from connected GitHub Git blob.
Counts/URLs independently computed with a read-only GitHub fetch_blob parser on 2026-10-26.
No outside source verification claimed for upstream citation relevance.
"""
import csv,pathlib,collections,json
P=pathlib.Path(__file__).resolve().parent
inp=P/'social_status_pakbbq_35_theme_crosswalk.csv'
rows=list(csv.DictReader(inp.open(encoding='utf-8-sig',newline='')))
U={
'NCBI':'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6020691/',
'WP':'https://www.washingtonpost.com/news/answer-sheet/wp/2013/10/28/five-stereotypes-about-poor-families-and-education/',
'JH':'https://www.justharvest.org/wp-content/uploads/2015/07/Just-Harvest-Poverty-Myths-Stereotypes-fact-sheet.pdf',
'SAGE':'https://journals.sagepub.com/doi/10.1177/1948550613504968',
'SD':'https://www.sciencedirect.com/science/article/pii/S1658077X20300965.com',
'UNKNOWN':'https://www.socioeconomicbias.com/job-interview-biases',
'DAWN':'https://www.dawn.com/news/1851507',
'PT':'https://profit.pakistantoday.com.pk/2022/12/04/income-culture-and-inequality-who-are-pakistans-middle-classes/'
}
codes={i:('NCBI',) for i in [1,2,3,8,15,23,24]}
codes.update({i:('WP',) for i in [4,5,6,7,9,10,12,13,14,16,18,22]})
codes.update({i:('SAGE',) for i in [17,19,25]})
codes.update({11:('JH',),20:('JH','SD'),21:('NCBI','SD'),33:('UNKNOWN',),34:('DAWN',),35:('PT',)})
for i in range(26,33):codes[i]=()
assert set(codes)==set(range(1,36)),set(range(1,36))-set(codes)
for r in rows:
 i=int(r['question_index']);count=int(r['total_records']);src=[U[x] for x in codes[i]]
 r['source_url_count']=len(src);r['source_urls']=' | '.join(src);r['cited_records']=count if src else 0;r['missing_source_records']=0 if src else count
 r['upstream_stereotyped_groups']='Rural' if i==26 else 'Rural communities' if i==35 else 'lowSES' if i in (27,28,29,30,31,32,33,34) else 'low SES'
 r['upstream_source_present']='YES' if src else 'NO'
 r['upstream_source_evidence_verified']='NO: presence/path only; URL relevance not independently reopened' if src else 'NO: no URL in original rows'
 r['source_quality_note']='Missing source for all rows' if not src else ('Contains malformed .com extension in apparent article identifier' if i in (20,21) else 'Source presence does not establish Bangladesh-specific validity; Pakistani or US sources in upstream')
 r['citation_availability']=str(r['cited_records'])+' / '+str(count)+' rows with source field' 
with inp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='raise');w.writeheader();w.writerows(rows)
summary={'source':'actual connected GitHub SES blob c079dbae2 / 93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe','total_records':sum(int(r['total_records']) for r in rows),'indices':len(rows),'no_source_theme_indices':[int(r['question_index']) for r in rows if int(r['missing_source_records'])>0],'uncited_records':sum(int(r['missing_source_records']) for r in rows),'cited_records':sum(int(r['cited_records']) for r in rows),'note':'This is exact URL presence, not evidence relevance or source accessibility; some nonempty URLs are from US and Pakistan.'}
(P/'social_status_pakbbq_upstream_source_presence_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(summary)
