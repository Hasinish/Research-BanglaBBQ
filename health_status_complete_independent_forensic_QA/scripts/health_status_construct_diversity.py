#!/usr/bin/env python3
"""Manually calibrated theme/variation construct-coverage table based on thirty paired base templates."""
import csv,json
from pathlib import Path
from health_status_create_audit_artifacts import BASE,SOURCE_EVIDENCE
R=Path('/mnt/data'); M=json.loads((R/'health_status_audited_expansion_manifest.json').read_text());v=M['variations']; D={int(s[0][1:]):s for s in SOURCE_EVIDENCE}
fields=['theme_id','variation','records_per_language','start_id','end_id','bias_target','proposed_mechanism','source_tier_for_health_only_construct','scenario_en','scenario_bn','question_neg_en','question_nonneg_en','variation_distinctness','category_boundary_verdict','factual_qualification','AI_cultural_fit_1to5','semantic_note','risk_and_recommendation','human_review']
with (R/'health_status_construct_diversity_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader()
 for idx,x in enumerate(v):
  q=int(x['theme_id'][1:]);vv=int(x['variation'][1:]);scene=x['base_bilingual_template'];src=D[q];n=BASE[q,vv]
  verdict=('CONFOUNDED_SOURCE' if q==4 else 'INTERSECTIONAL_BUT_CONTROLLED_IN_FICTION_BUT_SOURCE_CONFOUNDED' if q==7 else 'IN_SCOPE_FICTIONAL_WITH_SOURCE_LIMITS')
  if q in (2,8,9):verdict='IN_SCOPE_BUT_EXTRAPOLATED_SOCIAL_GATEKEEPING_UNVERIFIED'
  diversity='FAMILY_REPETITION_RISK' if q==2 else 'REPEATED_NEWSLETTER_WORKFLOW_Q08_V3_AND_Q10_V3' if q in (8,10) and vv==3 else 'DISTINCT_SETTING_TASK_AND_EVALUATOR_AFTER_MANUAL_BASE_REVIEW'
  wr.writerow(dict(theme_id=x['theme_id'],variation=x['variation'],records_per_language=48,start_id=x['start_example_id'],end_id=x['end_example_id'],bias_target=D[q][1],proposed_mechanism='Potential illness/disclosure-linked social gatekeeping unrelated to individually observed task performance',source_tier_for_health_only_construct=src[2],scenario_en=scene['scene_en'],scenario_bn=scene['scene_bn'],question_neg_en=scene['questions_en']['neg'],question_nonneg_en=scene['questions_en']['nonneg'],variation_distinctness=diversity,category_boundary_verdict=verdict,factual_qualification='Fictional outcomes, equal relevant qualifications and current access; sources support themes not actual incidents',AI_cultural_fit_1to5=n[2],semantic_note=n[4],risk_and_recommendation=src[7]+' | '+src[8],human_review='NO'))
print('written',len(v),'30 Q-V cases')
