import csv
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

QA_DIR = r"d:\Research-BanglaBBQ\local_candidates\final_seven_category_qa"
AUDIT_DIR = os.path.join(QA_DIR, "independent_source_semantic_audit")
REPORTS_DIR = os.path.join(AUDIT_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Read existing linguistic review queue if present
input_lrq = os.path.join(QA_DIR, "linguistic_review_queue.csv")

headers = [
    "review_id",
    "category",
    "theme_id",
    "variation",
    "example_id",
    "english_text",
    "bengali_text",
    "defect_type",
    "audit_evidence",
    "proposed_correction",
    "review_tier",
    "status_label"
]

def main():
    rows = []
    
    if os.path.exists(input_lrq):
        with open(input_lrq, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, r in enumerate(reader):
                rows.append({
                    "review_id": f"BAQ-{idx+1:04d}",
                    "category": r["category"],
                    "theme_id": r["theme_id"],
                    "variation": r["variation"],
                    "example_id": r["example_id"],
                    "english_text": r.get("english_context", "See parallel candidate record"),
                    "bengali_text": r["bengali_context"],
                    "defect_type": r["defect_type"],
                    "audit_evidence": r["flagged_issue_description"],
                    "proposed_correction": r["proposed_bilingual_repair"],
                    "review_tier": "AI_SEMANTIC_AUDIT",
                    "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
                })
                
    # Add prototype-specific alignment cases
    prototype_items = [
        {
            "category": "Health Status",
            "theme_id": "Q02",
            "variation": "V1",
            "example_id": "48",
            "english_text": "A university department committee was reviewing two candidates for a research fellowship award...",
            "bengali_text": "একটি বিশ্ববিদ্যালয়ের বিভাগীয় কমিটি গবেষণা ফেলোশিপের জন্য দুজন প্রার্থীর আবেদন পর্যালোচনা করছিল...",
            "defect_type": "CLINICAL_CONFOUNDER_ELIMINATION",
            "audit_evidence": "Replaced outpatient clinic consultation with academic fellowship evaluation to eliminate medical precaution confounder.",
            "proposed_correction": "Prototype implemented and structurally validated. Awaiting human clinical/linguistic panel sign-off.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        },
        {
            "category": "Health Status",
            "theme_id": "Q04",
            "variation": "V1",
            "example_id": "144",
            "english_text": "Two library volunteers were organizing rare regional manuscripts...",
            "bengali_text": "একটি পাঠাগারের দুজন স্বেচ্ছাসেবক দুর্লভ আঞ্চলিক পাণ্ডুলিপি তালিকাভুক্ত করছিলেন...",
            "defect_type": "SALIVA_CONTAGION_ELIMINATION",
            "audit_evidence": "Replaced shared afternoon tea table with archival manuscript cataloging to eliminate saliva transmission fear.",
            "proposed_correction": "Prototype implemented and structurally validated. Verify Bengali register reflects authentic archive terminology.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        },
        {
            "category": "Health Status",
            "theme_id": "Q05",
            "variation": "V1",
            "example_id": "192",
            "english_text": "Two remote project assistants were collating local health directories from home...",
            "bengali_text": "বাড়ি থেকে দূরবর্তী প্রকল্পে কর্মরত দুজন সহকারী স্থানীয় স্বাস্থ্য সহায়িকা সংকলন করছিলেন...",
            "defect_type": "AEROSOL_CONTAGION_ELIMINATION",
            "audit_evidence": "Replaced in-person clean-up with remote home directory collation, eliminating aerosol viral fear.",
            "proposed_correction": "Prototype implemented. Confirm remote working phrasing 'দূরবর্তী প্রকল্পে কর্মরত' is natural Bangladeshi Bengali.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        },
        {
            "category": "Health Status",
            "theme_id": "Q07",
            "variation": "V1",
            "example_id": "288",
            "english_text": "Two coordinators conducted phone verification for an agricultural information hotline...",
            "bengali_text": "একটি কৃষি তথ্য সেবার জন্য দুজন সমন্বয়কারী ফোনে তথ্য যাচাইয়ের কাজ করছিলেন...",
            "defect_type": "VISUAL_LESION_FEAR_ELIMINATION",
            "audit_evidence": "Replaced public event with phone-based verification, eliminating physical lesion revulsion / leprosy confusion.",
            "proposed_correction": "Prototype implemented. Check that phone-verification context preserves genuine arsenicosis stigma.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        },
        {
            "category": "Physical Appearance",
            "theme_id": "Q02",
            "variation": "V1",
            "example_id": "48",
            "english_text": "Two certified audit associates were verifying the annual financial ledger of a commercial bank...",
            "bengali_text": "একটি বাণিজ্যিক ব্যাংকের বার্ষিক হিসাব খাতা যাচাইয়ের দায়িত্বে ছিলেন সনদপ্রাপ্ত দুজন নিরীক্ষা সহযোগী...",
            "defect_type": "BONA_FIDE_JOB_REQUIREMENT_REMOVAL",
            "audit_evidence": "Replaced TV commercial acting audition with bank financial audit to remove visual appearance job criteria.",
            "proposed_correction": "Prototype implemented and structurally validated. Neutralizes casting confounder.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        },
        {
            "category": "Social Status",
            "theme_id": "Q07",
            "variation": "V3",
            "example_id": "1248",
            "english_text": "An independent audit team verified the distribution accounts of a flood relief initiative...",
            "bengali_text": "একটি বন্যা ত্রাণ উদ্যোগের বণ্টন হিসাব যাচাই করছিল একটি স্বাধীন নিরীক্ষা দল...",
            "defect_type": "QUESTION_PREDICATE_ASYMMETRY",
            "audit_evidence": "Symmetrized negative question (procedural misuse) and non-negative question (verified compliance) around official audit findings.",
            "proposed_correction": "Prototype implemented. Replaced certificate handover asymmetry with balanced audit verification.",
            "review_tier": "AI_SEMANTIC_AUDIT",
            "status_label": "NEEDS_NATIVE_HUMAN_REVIEW"
        }
    ]
    
    start_idx = len(rows) + 1
    for i, p in enumerate(prototype_items):
        p["review_id"] = f"BAQ-{start_idx + i:04d}"
        rows.append(p)
        
    out_csv = os.path.join(REPORTS_DIR, "bilingual_alignment_queue.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
            
    print(f"Generated {len(rows)} bilingual review queue items into: {out_csv}")

if __name__ == "__main__":
    main()
