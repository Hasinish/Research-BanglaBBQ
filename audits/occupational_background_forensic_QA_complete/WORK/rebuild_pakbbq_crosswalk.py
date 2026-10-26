import csv,collections
from pathlib import Path
D=Path('/mnt/data/occupational_forensic_audit');p=Path('/mnt/data/banglabbq_occupational_background_pakbbq_theme_crosswalk.csv')
data=list(csv.DictReader(p.open(encoding='utf-8-sig')))
field=list(data[0]);print(field)
SES_COUNTS=[48,48,48,288,320,72,272,240,272,272,288,48,48,272,272,272,48,48,272,48,48,72,48,256,288,24,288,8,272,8,8,256,272,8,32]
SES_DESCRIPTIONS={
1:'Rich vs poor neighborhoods: drug-use suspicion',2:'Rich vs poor park visitors: alleged drug use',3:'Rich vs poor: competence in complex task',
4:'Factory worker vs dentist: retrospective school performance',5:'Landlord vs farmworker: inattentive parenting; socioeconomic family labels crossed',
6:'Low-income vs wealthy parents: engagement in children education',7:'Line cook vs dentist: failing high-school classes',
8:'Farmworker vs dentist: presumed drug use',9:'Professor vs maid: parent engagement at school career day',
10:'Dentist vs maid: English-language proficiency in a telephone survey',11:'Professor vs maid as election volunteers: presumed laziness',
12:'Rich vs poor nervous callers: English ability',13:'Welfare-supported vs wealthy family: child school engagement',
14:'Line cook vs dentist: daycare parental attention',15:'Line cook vs dentist: airport drugs suspicion',
16:'Lawyer vs maid: high-school learning ability',17:'Welfare-supported vs wealthy: complex form/test ability',
18:'Rich vs poor university students: performance',19:'Janitor vs dentist on Jeeto Pakistan quiz show: who loses',
20:'Pension vs well-off: laziness',21:'Pension-supported vs wealthy: value of school education',
22:'Wealthy vs low-income students: school drug sales',23:'Rich vs poor mosque food-stall helpers: competence',
24:'Engineer vs maid mosque fundraising: competence',25:'Real-estate agent vs maid general-knowledge quiz: intelligence',
26:'Rural vs urban applicant: corporate skill evaluation',27:'Professor vs maid: assumed out of place in high-status housing',
28:'Madrasa vs elite school child: presumed economy flight',29:'Real-estate agent vs maid: bank loan default risk',
30:'Government school vs elite-school student: restaurant menu familiarity',31:'House help vs rich parent: engagement in child schooling',
32:'Line cook vs dentist: private hospital bill-paying assumption',33:'Engineer vs maid: assumed tech-job suitability',
34:'Poor laborer vs middle-class employer: wage negotiation fairness',35:'Village vs urban candidate: urban-insight stereotype'}
OCC={4,5,7,8,9,10,11,14,15,16,19,24,25,27,29,31,32,33,34}
assert len(SES_COUNTS)==35 and sum(SES_COUNTS)==5384 and len(SES_DESCRIPTIONS)==35
result=[]
for x in data:
 if x['question_index']=='INACCESSIBLE' and 'SES' in x['scenario_summary']:
  x['question_index']='SES_VERIFIED_SUMMARY';x['record_count']='5384 across 35 themes';x['scenario_summary']='Git blob SHA 93b7ecc9dd0bfaed0d44c41e45d9c27d585fefbe retrieved in full: 5384 UTF-8 JSONL records; 35 question_index values; no standalone protected occupation category.';x['source_availability']='Content and per-theme source strings accessible; Pakistan/US sources not proof of Bangladesh occupational bias';x['audit_status']='SES_FULL_BLOB_READ_2026-10-26';x['rationale']='Original inaccessible assumption REVOKED; exact 35-theme index crosswalk below. Many examples use job titles as socioeconomic proxies (SES label), not occupational bias targets.'
 result.append(x)
for i,(n) in enumerate(SES_COUNTS,1):
 row=dict.fromkeys(field,'');row.update(dataset='PakBBQ_ENG SES',path='PakBBQ/PakBBQ_ENG/SES.jsonl',question_index=str(i),record_count=str(n),scenario_summary=SES_DESCRIPTIONS[i],comparison_variable=('SES (highSES vs lowSES), occupation labels as class proxy' if i in OCC else 'Socioeconomic class/wealth, not controlled occupation'),source_availability='Git blob fully parsed; sources in original record; not independently relevant to Bangladesh',decision='REJECT' if i in OCC else 'NOT_RELEVANT',mapped_q='',audit_status='SES_QUESTION_INDEX_VERIFIED_2026-10-26',rationale='Do NOT import job labels as evidence of an occupational stereotype; job training and SES differ. At most generic BBQ design lead.' if i in OCC else 'Source target is SES/wealth/region/education, not protected occupation.')
 result.append(row)
out=D/'occupational_background_revised_pakbbq_crosswalk.csv'
with out.open('w',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=field);writer.writeheader();writer.writerows(result)
print('crosswalk rows',len(result),'SES rows',sum(x['dataset']=='PakBBQ_ENG SES' for x in result),'SES reject',len(OCC),'no direct',sum(x['question_index']=='NO_DIRECT_EQUIVALENT' for x in result))
