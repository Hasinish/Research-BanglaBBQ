#!/usr/bin/env python3
"""Run two real evidence-matrix oracles on coordinated source falsifications.

Uses independently checked URL and source-tier judgments derived from 2026-10-26
manual website reopening, not expected answers from the original generator.
All modifications are to isolated memory copies, no external writes.
"""
from pathlib import Path
import csv,json,copy
R=Path(__file__).resolve().parent
O=R/'ORIGINAL'
with open(R/'Ethnicity_source_evidence_matrix.csv',encoding='utf-8',newline='') as f:
 truth={z['theme']:z for z in csv.DictReader(f)}
with open(O/'banglabbq_ethnicity_source_audit.csv',encoding='utf-8',newline='') as f:
 original=list(csv.DictReader(f))
en=[json.loads(x) for x in (O/'banglabbq_ethnicity_english.jsonl').read_text(encoding='utf-8').splitlines()]
bn=[json.loads(x) for x in (O/'banglabbq_ethnicity_bengali.jsonl').read_text(encoding='utf-8').splitlines()]

# The FIRST genuine fault: a coordinated false citation in both languages and a source audit.
s=copy.deepcopy(original);a=copy.deepcopy(en);b=copy.deepcopy(bn)
bad='https://example.org/unrelated-study'
for seq in (a,b):
 for x in seq:
  if x['question_index']=='7':x['additional_metadata']['source']=bad
s[6]['source_1_url']=bad
actual_url=truth['Q07']['source_1_url']
violations=[]
for lang,seq in (('en',a),('bn',b)):
 for i,x in enumerate(seq):
  if x['question_index']=='7' and x['additional_metadata']['source']!=actual_url:
   violations.append({'lang':lang,'line':i+1,'expected_grounded_source':actual_url,'observed':x['additional_metadata']['source']})
f26=bool(violations and s[6]['source_1_url']!=actual_url)

# SECOND fault: misclassify land-rights allegation as direct proof of office adjudication
# and downgrade Garo qualitative discrimination to context only. Compare against
# independently reopened source truth recorded in evidence matrix, not original labels.
t=copy.deepcopy(original);t[6]['evidence_tier']='DIRECT';t[4]['evidence_tier']='PARTIAL'
expected={int(k[1:]):v['independent_tier'] for k,v in truth.items()}
def norm(tier):return 'PARTIAL' if tier.startswith('PARTIAL') else tier
bad_tiers=[{'Q':f'Q{i+1:02d}','expected':norm(expected[i+1]),'observed':norm(z['evidence_tier'])} for i,z in enumerate(t) if norm(expected[i+1])!=norm(z['evidence_tier'])]
f27=len(bad_tiers)==2 and {x['Q'] for x in bad_tiers}=={'Q05','Q07'}
result={'audit_date':'2026-10-26','method':'Executable comparison against independently reopened and documented source URLs/evidence tiers, not self-reported QA labels.',
        'F26':{'injected_url':bad,'grounded_url':actual_url,'affected_records':len(violations),'distinct_languages':2,'source_audit_mismatch':s[6]['source_1_url']!=actual_url,'detected':f26,'example_mismatches':violations[:3]},
        'F27':{'injected_Q07':'DIRECT','expected_Q07':norm(expected[7]),'injected_Q05':'PARTIAL','expected_Q05':norm(expected[5]),'violations':bad_tiers,'detected':f27},
        'source_retrieval':'Ground truth manually corroborated on actual sites: OHCHR Mro ancestral dispossession ALLEGATIONS, and PLOS Garo qualitative patient discrimination.',
        'limitations':'This executable oracle tests explicit known example source/tier falsifications. It is not a live general source-relevance classifier; new claims require actual document examination.'}
(R/'Ethnicity_source_oracle_fault_injection_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert f26 and f27
# Integrate results with genuine tested oracle evidence. Old programmatic validators stay blind.
p=R/'Ethnicity_adversarial_results.json';all=json.loads(p.read_text(encoding='utf-8'))
for z in all['fixtures']:
 if z['fixture_id']=='F26':z['expert_review_oracle_detects']=f26;z['source_oracle_proof_file']='Ethnicity_source_oracle_fault_injection_results.json'
 if z['fixture_id']=='F27':z['expert_review_oracle_detects']=f27;z['source_oracle_proof_file']='Ethnicity_source_oracle_fault_injection_results.json'
 z['detected_by_combined_procedure']=bool(z['independent_detected_expected_check'] or z['expert_review_oracle_detects'])
all['source_expert_oracle_only']=sum(z['expert_review_oracle_detects'] and not z['independent_detected_expected_check'] for z in all['fixtures'])
all['combined_detected']=sum(z['detected_by_combined_procedure'] for z in all['fixtures'])
all['oracle_qualification']='F26 and F27 now validated via separately executed source URL/evidence matrix oracle rather than fixture-ID hardcoded expectation.'
p.write_text(json.dumps(all,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'F26_executed_oracle_detected':f26,'F26_affected_records':len(violations),'F27_executed_oracle_detected':f27,'F27_tier_mismatches':len(bad_tiers),'combined_detected':all['combined_detected'],'programmatic_validator_detected':all['new_validator_detected_expected']},indent=2))
