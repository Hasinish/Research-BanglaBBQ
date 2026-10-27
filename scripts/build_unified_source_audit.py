import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path('.')
OUT_FILE = ROOT / 'local_candidates' / 'final_seven_category_qa' / 'source_audit.csv'

# Standard output fields
FIELDNAMES = [
    'category',
    'theme_id',
    'theme_title',
    'groups_compared',
    'claimed_mechanism',
    'primary_source_title',
    'primary_source_url',
    'is_bangladesh_specific',
    'evidence_tier',
    'evidence_assessment',
    'confounders_and_limitations',
    'audit_decision',
    'status_label'
]

unified_rows = []

# 1. Physical Appearance
pa_path = ROOT / 'audits/physical_appearance_independent_forensic_QA_bundle/physical_appearance_source_evidence_matrix.csv'
with open(pa_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        unified_rows.append({
            'category': 'Physical Appearance',
            'theme_id': row.get('theme', ''),
            'theme_title': row.get('original_theme_title', ''),
            'groups_compared': row.get('group_comparison', ''),
            'claimed_mechanism': row.get('claimed_mechanism', ''),
            'primary_source_title': row.get('primary_cited_title', ''),
            'primary_source_url': row.get('primary_url', ''),
            'is_bangladesh_specific': row.get('primary_source_is_Bangladesh_specific', ''),
            'evidence_tier': row.get('independent_evidence_tier', row.get('original_evidence_tier', '')),
            'evidence_assessment': row.get('actual_verified_claim', ''),
            'confounders_and_limitations': row.get('unverified_extrapolation_and_confounders', ''),
            'audit_decision': row.get('decision', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in row.get('independent_evidence_tier', '') else 'NEEDS HUMAN REVIEW'
        })

# 2. Social Status
ss_path = ROOT / 'audits/banglabbq_social_status_forensic_QA_complete/Social_Status_Forensic_QA/audit/social_status_source_evidence_matrix.csv'
with open(ss_path, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        unified_rows.append({
            'category': 'Social Status',
            'theme_id': row.get('theme', row.get('\ufefftheme', '')),
            'theme_title': row.get('title', ''),
            'groups_compared': row.get('target_comparison', ''),
            'claimed_mechanism': row.get('alleged_mechanism', ''),
            'primary_source_title': row.get('primary_title', ''),
            'primary_source_url': row.get('primary_url', ''),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': row.get('independent_tier', ''),
            'evidence_assessment': row.get('verified_empirical_finding', ''),
            'confounders_and_limitations': row.get('unsupported_extrapolations_and_confounders', ''),
            'audit_decision': row.get('action', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in row.get('independent_tier', '') else 'NEEDS HUMAN REVIEW'
        })

# 3. Health Status
hs_path = ROOT / 'audits/health_status_complete_independent_forensic_QA/evidence/health_status_source_evidence_matrix.csv'
with open(hs_path, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        unified_rows.append({
            'category': 'Health Status',
            'theme_id': row.get('theme_id', row.get('\ufefftheme_id', '')),
            'theme_title': row.get('theme', ''),
            'groups_compared': row.get('condition_focus', row.get('theme', '')),
            'claimed_mechanism': row.get('stereotype_mechanism', ''),
            'primary_source_title': row.get('primary_source_title', ''),
            'primary_source_url': row.get('primary_source_url', ''),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': row.get('forensic_tier', ''),
            'evidence_assessment': row.get('forensic_evidence_summary', ''),
            'confounders_and_limitations': row.get('infection_or_confounder_notes', ''),
            'audit_decision': row.get('forensic_decision', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in row.get('forensic_tier', '') else 'NEEDS HUMAN REVIEW'
        })

# 4. Regional Affiliation
reg_path = ROOT / 'audits/Regional_independent_forensic_QA_bundle/output/Regional_source_evidence_matrix.csv'
with open(reg_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        tier = row.get('forensic_tier_final', row.get('forensic_tier', ''))
        unified_rows.append({
            'category': 'Regional Affiliation',
            'theme_id': row.get('theme', ''),
            'theme_title': row.get('claimed_bias_proposition', ''),
            'groups_compared': row.get('group_comparison', ''),
            'claimed_mechanism': row.get('claimed_bias_proposition', ''),
            'primary_source_title': row.get('source_titles', '').split(';')[0].strip(),
            'primary_source_url': row.get('source_urls', '').split(';')[0].strip(),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': tier,
            'evidence_assessment': row.get('verified_empirical_claims', ''),
            'confounders_and_limitations': row.get('unsupported_extrapolations', ''),
            'audit_decision': row.get('final_decision', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in tier else ('BLOCKED' if 'FLAWED' in tier or 'SATIRE' in tier else 'NEEDS HUMAN REVIEW')
        })

# 5. Ethnicity
eth_path = ROOT / 'audits/Ethnicity_forensic_QA_complete/Ethnicity_source_evidence_matrix.csv'
with open(eth_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        tier = row.get('independent_tier', row.get('original_csv_tier', ''))
        unified_rows.append({
            'category': 'Ethnicity',
            'theme_id': row.get('theme', ''),
            'theme_title': row.get('bias_proposition', ''),
            'groups_compared': row.get('groups', ''),
            'claimed_mechanism': row.get('bias_proposition', ''),
            'primary_source_title': row.get('primary_source_title', ''),
            'primary_source_url': row.get('primary_url', ''),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': tier,
            'evidence_assessment': row.get('verified_claim_in_source', ''),
            'confounders_and_limitations': row.get('confounders_and_extrapolations', ''),
            'audit_decision': row.get('audit_recommendation', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in tier else 'NEEDS HUMAN REVIEW'
        })

def format_qid(val):
    if not val:
        return ''
    s = str(val).strip()
    if s.startswith('Q'):
        return s
    try:
        return f"Q{int(s):02d}"
    except Exception:
        return s

# 6. Occupational Background
occ_path = ROOT / 'audits/occupational_background_forensic_QA_complete/occupational_background_source_evidence_matrix.csv'
with open(occ_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        tier = row.get('independent_audit_tier', row.get('committed_source_tier', ''))
        unified_rows.append({
            'category': 'Occupational Background',
            'theme_id': format_qid(row.get('question_index', '')),
            'theme_title': row.get('theme', ''),
            'groups_compared': row.get('compared_occupations', ''),
            'claimed_mechanism': row.get('alleged_stereotype', ''),
            'primary_source_title': row.get('primary_source_title', ''),
            'primary_source_url': row.get('primary_source_url', ''),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': tier,
            'evidence_assessment': row.get('verified_empirical_finding', ''),
            'confounders_and_limitations': row.get('unsupported_extrapolations_and_confounders', ''),
            'audit_decision': row.get('recommended_action', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in tier else ('BLOCKED' if 'UNSUPPORTED' in tier or 'CONFOUNDED' in tier else 'NEEDS HUMAN REVIEW')
        })

# 7. Marital Status
mar_path = ROOT / 'audits/marital_status_independent_forensic_QA_bundle/marital_status_forensic_QA/marital_status_source_evidence_matrix.csv'
with open(mar_path, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        tier = row.get('forensic_evidence_tier', '')
        unified_rows.append({
            'category': 'Marital Status',
            'theme_id': format_qid(row.get('question_index', '')),
            'theme_title': row.get('theme', ''),
            'groups_compared': row.get('comparison', ''),
            'claimed_mechanism': row.get('stereotype_mechanism_as_allegation', ''),
            'primary_source_title': row.get('source_title_primary', ''),
            'primary_source_url': row.get('source_url_primary', ''),
            'is_bangladesh_specific': 'YES',
            'evidence_tier': tier,
            'evidence_assessment': row.get('verified_evidence_summary', ''),
            'confounders_and_limitations': row.get('confounders_and_scope_limits', ''),
            'audit_decision': row.get('forensic_decision', ''),
            'status_label': 'SOURCE VERIFIED' if 'DIRECT' in tier else 'NEEDS HUMAN REVIEW'
        })

# Write unified source audit CSV
with open(OUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(unified_rows)

print(f"Unified source audit written to {OUT_FILE} with {len(unified_rows)} themes across 7 categories.")
