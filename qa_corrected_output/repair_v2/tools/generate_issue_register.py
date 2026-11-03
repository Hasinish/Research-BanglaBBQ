"""
generate_issue_register.py
Author: Antigravity AI & BanglaBBQ QA Team
Date: November 3, 2026

Generates qa_corrected_output/repair_v2/ISSUE_REGISTER.csv documenting all confirmed defects,
methodological conflicts, linguistic repairs, and resolution statuses across the 9 categories.
"""

import csv
import os

OUT_FILE = 'qa_corrected_output/repair_v2/ISSUE_REGISTER.csv'

issues = [
    {
        'Issue ID': 'ISSUE-ETH-001',
        'Category': 'Ethnicity',
        'Language': 'Bengali',
        'Scenario family': 'All 30 families (Q01-Q10, V1-V3)',
        'Exact affected record IDs': '984 records across rows 0..1439',
        'Severity': 'CRITICAL',
        'Original problem': "Automated regex re.sub(r'\\s+[কখ]\\b', '', b_amb) stripped Bengali letters from ordinary words starting with or containing ক/খ ('একই ক্লাসে' -> 'একই্লাসে', 'কারও' -> 'ারও', 'কার ক্ষেত্রে' -> 'ার্ষেত্রে', 'কাছাকাছি' -> 'াফাছাকাছি', 'কোর্সে' -> 'োর্সে', 'ক্লাবে' -> '্লাবে').",
        'Corrected text or recommended change': "Restored uncorrupted text from fixed JsonL; used exact role noun replacements ('শিক্ষার্থী ক' -> 'শিক্ষার্থী এবং', 'শিক্ষার্থী খ' -> 'শিক্ষার্থী'); zero blind regex word stripping.",
        'Resolution status': 'RESOLVED',
        'Verification evidence': 'Clean vocabulary audit: 0 broken glued tokens, 0 corrupted words across all 1,440 Bengali records; certified in Gate 3.'
    },
    {
        'Issue ID': 'ISSUE-ETH-002',
        'Category': 'Ethnicity',
        'Language': 'English / Bengali',
        'Scenario family': 'All 30 families (Q01-Q10, V1-V3)',
        'Exact affected record IDs': 'All 1,440 rows (2,880 answer instances per lang)',
        'Severity': 'HIGH',
        'Original problem': "answer_info display metadata remained desynchronized from ans0..2 text (e.g., ans0='The Munda student' but answer_info['ans0'][0]='Munda student A'; in Bengali ans0='মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী' but answer_info='মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী ক').",
        'Corrected text or recommended change': "Synchronized answer_info[k][0] = r[k] across all answer choices while strictly preserving demographic codes ('munda', 'ethnic_bengali', etc.) in answer_info[k][1].",
        'Resolution status': 'RESOLVED',
        'Verification evidence': '100% parity across all 4,320 answer_info instances; Gate 6 PASS.'
    },
    {
        'Issue ID': 'ISSUE-ETH-003',
        'Category': 'Ethnicity',
        'Language': 'English / Bengali',
        'Scenario family': 'All 30 families (Q01-Q10, V1-V3)',
        'Exact affected record IDs': 'Rows 0..1439',
        'Severity': 'HIGH',
        'Original problem': "Residual entity placeholders ('Student A/B', 'Candidate A/B', 'Patient A/B', 'শিক্ষার্থী ক/খ') present in baseline benchmark.",
        'Corrected text or recommended change': "Sentence 1 rewritten to natural introducing clauses ('a Munda student and an ethnic Bengali student' / 'মুণ্ডা জনগোষ্ঠীর শিক্ষার্থী এবং বাঙালি জনগোষ্ঠীর শিক্ষার্থী'); Sentence 3 disambiguated via ordinal role references ('the first student' / 'the second student'; 'প্রথম শিক্ষার্থী' / 'দ্বিতীয় শিক্ষার্থী').",
        'Resolution status': 'RESOLVED',
        'Verification evidence': 'Exhaustive regex scan for standalone [AB] and [কখ]: exactly 0 residual placeholder tags across all 1,440 records in both languages; Gate 3 PASS.'
    },
    {
        'Issue ID': 'ISSUE-ETH-004',
        'Category': 'Ethnicity',
        'Language': 'English / Bengali',
        'Scenario family': 'Themes Q01, Q03, Q05, Q07, Q09',
        'Exact affected record IDs': '360 disambiguated rows in even-indexed themes',
        'Severity': 'METHODOLOGICAL',
        'Original problem': "Previous agent swapped ordinals in 5 themes to artificially force a 180:180 position balance, altering canonical gold labels (360 label diffs) and creating a theme-index position confound.",
        'Corrected text or recommended change': "Reverted unapproved label modifications to canonical gold baseline; documented inherited 360 First / 0 Second position skew on negative questions as an open benchmark characteristic awaiting thesis-team introduction-order rebalancing.",
        'Resolution status': 'PENDING THESIS APPROVAL',
        'Verification evidence': 'Canonical label invariance restored; Gate 1 PASS; 480/480/480 balanced labels.'
    },
    {
        'Issue ID': 'ISSUE-REL-001',
        'Category': 'Religion',
        'Language': 'English / Bengali',
        'Scenario family': 'All 60 scenario families (Q01-Q20, V1-V3)',
        'Exact affected record IDs': '720 Version-B ambiguous records per language',
        'Severity': 'CRITICAL',
        'Original problem': "Previous agent overwrote Sentence 1 in Block B with Sentence 1 from Block A, making 720 Version-B ambiguous records 100% identical duplicates of Version-A ambiguous records, destroying ambiguous counterfactual distinctness.",
        'Corrected text or recommended change': "Restored distinct counterfactual entity introduction orders in Sentence 1 from fixed JsonL baseline (0 duplicate ambiguous contexts); retained authentic narrative outcomes.",
        'Resolution status': 'RESOLVED IN CANDIDATE / BLOCKED PENDING THESIS REVIEW',
        'Verification evidence': 'Gate 5 check confirmed exactly 0 duplicate ambiguous contexts between Block A and Block B; Religion formally designated BLOCKED due to first-mention position skew (516 First / 204 Second).'
    },
    {
        'Issue ID': 'ISSUE-EDU-001',
        'Category': 'EducationalBackground',
        'Language': 'English / Bengali',
        'Scenario family': 'Even-numbered themes (Q02, Q04, Q06, Q08, Q10, Q12, Q14, Q16, Q18, Q20)',
        'Exact affected record IDs': '720 disambiguated rows across 10 even-numbered themes',
        'Severity': 'METHODOLOGICAL',
        'Original problem': "Previous agent changed 720 disambiguated gold labels across 10 even-numbered themes to force 360/360 global balance, creating a 100%/0% theme-index position confound (odd themes = 100% First negative; even themes = 100% Second negative) and mutating demographic targeting.",
        'Corrected text or recommended change': "Reverted 720 modified labels to canonical baseline; preserved 50/50 demographic counterfactual balance (720 madrasa / 720 general school as victim); documented trade-offs.",
        'Resolution status': 'BLOCKED PENDING METHODOLOGICAL APPROVAL',
        'Verification evidence': 'Canonical labels and outcomes preserved 100%; Gate 1 PASS (960/960/960 labels); Gate 4 PASS (0 bilingual label mismatches).'
    },
    {
        'Issue ID': 'ISSUE-GEN-001',
        'Category': 'OccupationalBackground, Politics, Regional, HealthStatus, MaritalStatus, SocialStatus',
        'Language': 'English / Bengali',
        'Scenario family': 'All scenarios',
        'Exact affected record IDs': '28,800 records across 6 categories',
        'Severity': 'LOW / VERIFICATION',
        'Original problem': "Need to confirm zero regression or drift in audited candidate files.",
        'Corrected text or recommended change': "Verified bit-for-bit SHA-256 invariance against audited fixed JsonL baseline; certified all structural, semantic, and permutation gates.",
        'Resolution status': 'APPROVED',
        'Verification evidence': 'All 12 files certified 100% bit-for-bit parity; Gates 1..6 PASS without defects.'
    }
]

with open(OUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(issues[0].keys()))
    writer.writeheader()
    writer.writerows(issues)

print(f"Successfully generated {OUT_FILE} with {len(issues)} entries.")
