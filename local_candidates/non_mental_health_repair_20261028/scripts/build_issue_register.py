import os
import sys
import csv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "reports")
OUT_CSV = os.path.join(OUT_DIR, "issue_register.csv")

# Defect entries covering all prioritized issues across the seven categories
ISSUES = [
    {
        "issue_id": "ISSUE-001",
        "severity": "P0_CRITICAL",
        "category": "Health Status",
        "theme": "Q01-Q10",
        "variation": "V1-V3",
        "affected_ids": "0-1439 (360 negative disambiguated rows)",
        "language": "both",
        "defect_type": "POSITIONAL_SHORTCUT",
        "evidence": "100.0% of negative disambiguated gold answers were the first-mentioned entity (360/0). Models could achieve 100% accuracy without reading context.",
        "proposed_fix": "Introduced entity introduction order balancing across variations to achieve exactly 180 First / 180 Second (50.0% / 50.0%) while preserving 6-way permutations.",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Automated verification complete; human validation recommended."
    },
    {
        "issue_id": "ISSUE-002",
        "severity": "P0_CRITICAL",
        "category": "Regional Affiliation",
        "theme": "Q01-Q10",
        "variation": "V1-V3",
        "affected_ids": "0-1439 (360 negative disambiguated rows)",
        "language": "both",
        "defect_type": "POSITIONAL_SHORTCUT",
        "evidence": "100.0% of negative disambiguated gold answers were the first-mentioned entity (360/0).",
        "proposed_fix": "Balanced entity order to achieve 180 First / 180 Second (50.0% / 50.0%) across all variations.",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Automated verification complete; human validation recommended."
    },
    {
        "issue_id": "ISSUE-003",
        "severity": "P0_CRITICAL",
        "category": "Ethnicity",
        "theme": "Q01-Q10",
        "variation": "V1-V3",
        "affected_ids": "0-1439 (360 negative disambiguated rows)",
        "language": "both",
        "defect_type": "POSITIONAL_SHORTCUT",
        "evidence": "100.0% of negative disambiguated gold answers were the first-mentioned entity (360/0).",
        "proposed_fix": "Balanced entity order to achieve 180 First / 180 Second (50.0% / 50.0%) across all variations.",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Automated verification complete; human validation recommended."
    },
    {
        "issue_id": "ISSUE-004",
        "severity": "P0_CRITICAL",
        "category": "Ethnicity",
        "theme": "Q01-Q10",
        "variation": "V1-V3",
        "affected_ids": "0-1439 (all 1,440 rows in EN and BN)",
        "language": "both",
        "defect_type": "PLACEHOLDER_TOKEN_DEFECTION",
        "evidence": "Artificial participant tokens ('Munda student A', 'Chakma candidate A', 'ethnic Bengali student B', 'শিক্ষার্থী ক', 'শিক্ষার্থী খ') violated natural language realism.",
        "proposed_fix": "Replaced artificial placeholders across all 10 themes with authentic, culturally vetted Bangladeshi Indigenous and Bengali names (e.g., Bikash Munda, Tanvir Ahmed).",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Native community review recommended for indigenous naming nuance."
    },
    {
        "issue_id": "ISSUE-005",
        "severity": "P1_HIGH",
        "category": "Health Status",
        "theme": "Q02, Q04, Q05, Q07",
        "variation": "V1-V3",
        "affected_ids": "144-287, 432-575, 576-719, 864-1007 (576 rows)",
        "language": "both",
        "defect_type": "MEDICAL_CONTAGION_CONFOUND",
        "evidence": "Baseline contexts confounded demographic prejudice with legitimate medical infection control protocols (TB, COVID-19, Hepatitis B transmission risk).",
        "proposed_fix": "Replaced with audited non-confounded prototypes focusing on social stigma in non-transmissible desk/workplace settings (post-cure/asymptomatic/managed).",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Medical sociology expert confirmation."
    },
    {
        "issue_id": "ISSUE-006",
        "severity": "P1_HIGH",
        "category": "Social Status",
        "theme": "Q07",
        "variation": "V3",
        "affected_ids": "1008-1055 (48 rows)",
        "language": "both",
        "defect_type": "PROCEDURAL_COMPLIANCE_ASYMMETRY",
        "evidence": "Baseline context contained asymmetric documentation burdens that confounded class bias with administrative procedural non-compliance.",
        "proposed_fix": "Integrated audited V3 prototype establishing strictly matched procedural compliance before outcome.",
        "status": "REPAIRED_CANDIDATE_READY",
        "review_required": "Reviewed and verified."
    },
    {
        "issue_id": "ISSUE-007",
        "severity": "P1_HIGH",
        "category": "Regional Affiliation",
        "theme": "Q01",
        "variation": "V1-V3",
        "affected_ids": "0-143 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_HISTORICAL_MISATTRIBUTION",
        "evidence": "Schuman 1966 is a historical stereotype perception study from East Pakistan era, not empirical proof of contemporary market discrimination.",
        "proposed_fix": "Marked HISTORICAL_ONLY in source evidence matrix; documented residual construct limitation.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "Contemporary sociological citation required before production promotion."
    },
    {
        "issue_id": "ISSUE-008",
        "severity": "P1_HIGH",
        "category": "Regional Affiliation",
        "theme": "Q03",
        "variation": "V1-V3",
        "affected_ids": "288-431 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_EVIDENCE_INSUFFICIENT",
        "evidence": "Citation relies on a satirical column regarding Tangail stereotypes; satire does not establish institutional discrimination mechanisms.",
        "proposed_fix": "Marked UNSUPPORTED in source evidence matrix; blocked from unverified production deployment.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "Peer-reviewed sociological study required."
    },
    {
        "issue_id": "ISSUE-009",
        "severity": "P1_HIGH",
        "category": "Regional Affiliation",
        "theme": "Q05",
        "variation": "V1-V3",
        "affected_ids": "576-719 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_MISREPRESENTATION",
        "evidence": "Saad Quasem (June 14, 2025) discusses the linguistic evolution of 'Mofiz' as a regional slur, not controlled hiring exclusion rates.",
        "proposed_fix": "Classified as CONTEXTUALLY_SUPPORTED (slur existence established; scenario must be labeled illustrative).",
        "status": "SOURCE_AUDITED_FLAGGED",
        "review_required": "Linguistic review."
    },
    {
        "issue_id": "ISSUE-010",
        "severity": "P1_HIGH",
        "category": "Regional Affiliation",
        "theme": "Q10",
        "variation": "V1-V3",
        "affected_ids": "1296-1439 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_EVIDENCE_MISMATCH",
        "evidence": "Old Dhaka cultural pride and heritage feature article cited as proof of anti-Dhakaiya institutional discrimination.",
        "proposed_fix": "Marked UNSUPPORTED; blocked from production certification until relevant discrimination source is identified.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "New empirical source required."
    },
    {
        "issue_id": "ISSUE-011",
        "severity": "P1_HIGH",
        "category": "Physical Appearance",
        "theme": "Q05",
        "variation": "V1-V3",
        "affected_ids": "576-719 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_EVIDENCE_INSUFFICIENT",
        "evidence": "Humorous lifestyle column about height insecurity cited to substantiate institutional career exclusion.",
        "proposed_fix": "Marked UNSUPPORTED in source matrix; candidate held in review.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "Academic height-bias study required."
    },
    {
        "issue_id": "ISSUE-012",
        "severity": "P1_HIGH",
        "category": "Physical Appearance",
        "theme": "Q06",
        "variation": "V1-V3",
        "affected_ids": "720-863 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_EVIDENCE_INSUFFICIENT",
        "evidence": "Curly hair personal styling/care article cited to justify institutional hiring rejection.",
        "proposed_fix": "Marked UNSUPPORTED in source matrix; held in review.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "Grooming standard discrimination citation required."
    },
    {
        "issue_id": "ISSUE-013",
        "severity": "P1_HIGH",
        "category": "Occupational Background",
        "theme": "Q07",
        "variation": "V1-V3",
        "affected_ids": "864-1007 (144 rows)",
        "language": "both",
        "defect_type": "CONSTRUCT_CONFOUND_ETHNIC_CASTE",
        "evidence": "Tea-estate worker stigma is deeply intertwined with inherited ethnic/caste lineage and indentured labor history, confounding purely occupational bias.",
        "proposed_fix": "Documented residual confounder in audit; isolated occupational phrasing in candidate notes.",
        "status": "SOURCE_AUDITED_FLAGGED",
        "review_required": "Labor economist review."
    },
    {
        "issue_id": "ISSUE-014",
        "severity": "P1_HIGH",
        "category": "Occupational Background",
        "theme": "Q10",
        "variation": "V1-V3",
        "affected_ids": "1296-1439 (144 rows)",
        "language": "both",
        "defect_type": "SOURCE_MISATTRIBUTION",
        "evidence": "Paper on agricultural livelihood aspirations cited for assumed incompetence in corporate meeting facilitation.",
        "proposed_fix": "Marked UNSUPPORTED in source matrix; blocked from production promotion.",
        "status": "SOURCE_AUDITED_BLOCKED_FOR_PRODUCTION",
        "review_required": "Authentic meeting competency bias source required."
    },
    {
        "issue_id": "ISSUE-015",
        "severity": "P1_HIGH",
        "category": "Bilingual Alignment",
        "theme": "All Categories",
        "variation": "Various",
        "affected_ids": "53 identified candidate variations",
        "language": "both",
        "defect_type": "BILINGUAL_ASYMMETRY",
        "evidence": "Prior alignment queues contained placeholder English text ('See parallel candidate record') and truncated variation markers ('V').",
        "proposed_fix": "Reconstructed bilingual review queue with 100% full English contexts, Bengali contexts, and explicit variation IDs.",
        "status": "REPAIRED_QUEUE_GENERATED",
        "review_required": "Native Bengali speaker manual verification."
    }
]

FIELDS = [
    "issue_id", "severity", "category", "theme", "variation",
    "affected_ids", "language", "defect_type", "evidence",
    "proposed_fix", "status", "review_required"
]

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ISSUES)
    print(f"Generated issue_register.csv with {len(ISSUES)} prioritized issues at: {OUT_CSV}")

if __name__ == "__main__":
    main()
