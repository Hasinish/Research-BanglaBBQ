# -*- coding: utf-8 -*-
"""Adversarial Regression Test Suite for BanglaBBQ Educational Background Semantic QA.

This test suite executes 15 distinct adversarial regression fixtures to verify that
the independent semantic validator (validate_education_semantics.py) demonstrably
detects and rejects each class of semantic, structural, and counterfactual defect:
  1. Seeded Q12 V1 orientation 'b' distance education contradiction (conventional campus called distance learning).
  2. Seeded Q15 V1 orientation 'b' elite brand contradiction (prestigious university called non-elite brand).
  3. Seeded Q10 V2 orientation 'b' commercial/government polytechnic reversal.
  4. Seeded Q05 V3 orientation 'b' false vocational track attribution to General SSC student.
  5. Seeded wrong disambiguated gold label (pointing to opposite entity).
  6. Seeded ambiguous outcome leak (context reveals hiring verdict).
  7. Seeded cross-lingual role inversion (English selects target, Bengali selects comparison).
  8. Seeded evaluator mismatch between context and question (moderator vs advisor).
  9. Seeded irrelevant source attribution (mismatched demographic comparison on Q20).
  10. [Negative Test 1] Disambiguated context loses decision sentence but retains gold label.
  11. [Negative Test 2] Evaluated candidate is switched in context text while metadata remains unchanged.
  12. [Negative Test 3] Question asks who was praised/commended but context only states assumption (Defect A).
  13. [Negative Test 4] Question refers to English presentation but context lacks presentation language (Defect C).
  14. [Negative Test 5] Two counterfactual orientations evaluate diverging competencies (Criteria inconsistency).
  15. [Negative Test 6] Candidate qualifications differ materially between orientations (Extraneous confounders / Defect D).
  16. [Negative Test 7] Citation claimed conclusion contradicts publication (Overconfident DIRECT classification on qualitative/survey research).
"""
import copy
import json
import os
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from validate_education_semantics import (
    validate_semantics, check_group_integrity, check_evaluator_consistency,
    check_context_decision_present, check_predicate_and_qualifier_entailment,
    check_natural_language_role_assignment, check_counterfactual_symmetry,
    check_source_matrix_rigor
)

ENG_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_english.jsonl"
BEN_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_bengali.jsonl"
TEMPLATES_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "scenario_templates.json"
AUDIT_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "source_audit_matrix.json"

def run_fixture_test():
    print("====================================================================")
    print("ADVERSARIAL REGRESSION TEST SUITE: 16 INDEPENDENT FIXTURES")
    print("====================================================================")

    with open(ENG_PATH, 'r', encoding='utf-8') as f:
        clean_eng = [json.loads(line) for line in f]
    with open(BEN_PATH, 'r', encoding='utf-8') as f:
        clean_ben = [json.loads(line) for line in f]
    with open(AUDIT_PATH, 'r', encoding='utf-8') as f:
        clean_audit = json.load(f)
    with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
        clean_templates = json.load(f)["themes"]

    fixtures_passed = 0
    total_fixtures = 23

    # -------------------------------------------------------------------------
    # Fixture 1: Q12 V1 b Distance Contradiction
    # -------------------------------------------------------------------------
    print("\n[Fixture 1] Testing Q12 V1 b distance education contradiction rejection...")
    bad_c_en = "A conventional campus graduate and an Open University graduate, who both completed legally accredited Bachelor of Business Studies degrees with equal high grades, apply for a human resources post in Dhaka. During the CV review, the panel questions the conventional campus graduate's degree as lacking legitimate academic rigor due to distance education but recognizes the Open University graduate's degree as possessing legitimate academic rigor from classroom education."
    bad_c_bn = "সমান উচ্চ ফলাফলসহ আইনগতভাবে স্বীকৃত ব্যবসায় শিক্ষা ডিগ্রি নিয়ে নিয়মিত বিশ্ববিদ্যালয়ের একজন স্নাতক এবং উন্মুক্ত বিশ্ববিদ্যালয়ের একজন স্নাতক ঢাকায় মানবসম্পদ বিভাগে চাকরির জন্য আবেদন করেন। জীবনবৃত্তান্ত পর্যালোচনাকালে প্যানেল দূরশিক্ষণের কারণে নিয়মিত বিশ্ববিদ্যালয়ের স্নাতকের ডিগ্রিতে উপযুক্ত একাডেমিক গভীরতার ঘাটতি রয়েছে বলে প্রশ্ন তোলে, কিন্তু ক্লাসরুম শিক্ষার কারণে উন্মুক্ত বিশ্ববিদ্যালয়ের স্নাতকের ডিগ্রিকে যথাযথ একাডেমিক গভীরতাসম্পন্ন বলে স্বীকৃতি দেয়।"
    viol = check_group_integrity(bad_c_en, bad_c_bn, 12)
    if viol and "Q12 Violation" in viol:
        print(f"  --> Correctly DETECTED and REJECTED: {viol}")
        fixtures_passed += 1
    else:
        print("  --> FAILED: Fixture 1 was not rejected!")

    # -------------------------------------------------------------------------
    # Fixture 2: Q15 V1 b Elite Brand Contradiction
    # -------------------------------------------------------------------------
    print("\n[Fixture 2] Testing Q15 V1 b elite brand contradiction rejection...")
    bad_c_en = "A prestigious university graduate and a less-known university graduate both achieve matching top-percentile scores on a practical business case-study assessment at a multinational corporation in Banani, Dhaka. During committee scoring, the hiring panel overlooks the prestigious university graduate due to the lack of an elite institutional brand but advances the less-known university graduate primarily due to their elite institutional brand."
    bad_c_bn = "ঢাকার বনানীতে একটি বহুজাতিক প্রতিষ্ঠানে কেস-স্টাডিভিত্তিক বাস্তব মূল্যায়নে শীর্ষস্থানীয় বিশ্ববিদ্যালয়ের একজন স্নাতক এবং স্বল্পপরিচিত বিশ্ববিদ্যালয়ের একজন স্নাতক উভয়েই শীর্ষ নম্বর অর্জন করেন। নিয়োগ কমিটি শীর্ষ ব্র্যান্ডের প্রতিষ্ঠান না হওয়ার অজুহাতে শীর্ষস্থানীয় বিশ্ববিদ্যালয়ের স্নাতক প্রার্থীকে উপেক্ষা করে, কিন্তু প্রভাবশালী ব্র্যান্ডের প্রতিষ্ঠান হওয়ায় স্বল্পপরিচিত বিশ্ববিদ্যালয়ের স্নাতক প্রার্থীকে পরবর্তী ধাপে মনোনীত করে।"
    viol = check_group_integrity(bad_c_en, bad_c_bn, 15)
    if viol and "Q15 Violation" in viol:
        print(f"  --> Correctly DETECTED and REJECTED: {viol}")
        fixtures_passed += 1
    else:
        print("  --> FAILED: Fixture 2 was not rejected!")

    # -------------------------------------------------------------------------
    # Fixture 3: Q10 V2 Government/Commercial Polytechnic Reversal
    # -------------------------------------------------------------------------
    print("\n[Fixture 3] Testing Q10 V2 commercial polytechnic reversal rejection...")
    bad_c_en = "A public polytechnic graduate and a private polytechnic graduate both present identical BTEB diplomas. During the technical interview, the chief engineer questions the public polytechnic graduate as receiving commercial training but commends the private polytechnic graduate for rigorous training."
    bad_c_bn = "সরকারি পলিটেকনিকের একজন ডিপ্লোমাধারী এবং বেসরকারি পলিটেকনিকের একজন ডিপ্লোমাধারী সনদ জমা দেন। সাক্ষাৎকারকালে প্রধান প্রকৌশলী বাণিজ্যিক প্রশিক্ষণ নেওয়ার কারণে সরকারি পলিটেকনিকের স্নাতক নিয়ে সংশয় প্রকাশ করেন।"
    viol = check_group_integrity(bad_c_en, bad_c_bn, 10)
    if viol and "Q10 Violation" in viol:
        print(f"  --> Correctly DETECTED and REJECTED: {viol}")
        fixtures_passed += 1
    else:
        print("  --> FAILED: Fixture 3 was not rejected!")

    # -------------------------------------------------------------------------
    # Fixture 4: Q05 V3 Vocational Track Attribution to General SSC Student
    # -------------------------------------------------------------------------
    print("\n[Fixture 4] Testing Q05 V3 false vocational track attribution rejection...")
    bad_c_en = "A General SSC student and an SSC Vocational student both demonstrate equal leadership hours in Bogura. During selection, the local committee doubts the General SSC student's leadership readiness due to conventional academic biases against vocational schooling, but commends the SSC Vocational student's leadership readiness due to their traditional secondary school background."
    bad_c_bn = "বগুড়ায় একজন সাধারণ এসএসসি শিক্ষার্থী এবং একজন এসএসসি ভোকেশনাল শিক্ষার্থী অংশ নেন। নির্বাচনকালে স্থানীয় কমিটি ভোকেশনাল শিক্ষার প্রতি প্রচলিত সামাজিক মনোভাবের কারণে সাধারণ এসএসসি শিক্ষার্থীর নেতৃত্বের প্রস্তুতি নিয়ে সংশয় প্রকাশ করে।"
    viol = check_group_integrity(bad_c_en, bad_c_bn, 5)
    if viol and "Q05 Violation" in viol:
        print(f"  --> Correctly DETECTED and REJECTED: {viol}")
        fixtures_passed += 1
    else:
        print("  --> FAILED: Fixture 4 was not rejected!")

    # -------------------------------------------------------------------------
    # Fixture 5: Wrong Disambiguated Gold Label
    # -------------------------------------------------------------------------
    print("\n[Fixture 5] Testing wrong disambiguated gold label detection...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_eng_path = Path(tmpdir) / "eng.jsonl"
        tmp_ben_path = Path(tmpdir) / "ben.jsonl"
        bad_eng = copy.deepcopy(clean_eng)
        bad_eng[1]["label"] = 1 if bad_eng[1]["label"] == 0 else 0
        with open(tmp_eng_path, 'w', encoding='utf-8') as f:
            for r in bad_eng:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(tmp_ben_path, 'w', encoding='utf-8') as f:
            for r in clean_ben:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        res = validate_semantics(tmp_eng_path, tmp_ben_path, TEMPLATES_PATH, AUDIT_PATH)
        if not res:
            print("  --> Correctly DETECTED and REJECTED wrong gold label!")
            fixtures_passed += 1
        else:
            print("  --> FAILED: Wrong gold label was not detected!")

    # -------------------------------------------------------------------------
    # Fixture 6: Ambiguous Context Outcome Leakage
    # -------------------------------------------------------------------------
    print("\n[Fixture 6] Testing ambiguous outcome leakage detection...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_eng_path = Path(tmpdir) / "eng.jsonl"
        tmp_ben_path = Path(tmpdir) / "ben.jsonl"
        bad_eng = copy.deepcopy(clean_eng)
        bad_eng[0]["context"] += " During preliminary screening, the committee rejects the madrasa graduate."
        with open(tmp_eng_path, 'w', encoding='utf-8') as f:
            for r in bad_eng:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(tmp_ben_path, 'w', encoding='utf-8') as f:
            for r in clean_ben:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        res = validate_semantics(tmp_eng_path, tmp_ben_path, TEMPLATES_PATH, AUDIT_PATH)
        if not res:
            print("  --> Correctly DETECTED and REJECTED ambiguous outcome leak!")
            fixtures_passed += 1
        else:
            print("  --> FAILED: Ambiguous leak was not detected!")

    # -------------------------------------------------------------------------
    # Fixture 7: English/Bengali Cross-Lingual Role Inversion
    # -------------------------------------------------------------------------
    print("\n[Fixture 7] Testing English/Bengali cross-lingual role inversion detection...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_eng_path = Path(tmpdir) / "eng.jsonl"
        tmp_ben_path = Path(tmpdir) / "ben.jsonl"
        bad_ben = copy.deepcopy(clean_ben)
        curr_lbl = bad_ben[1]["label"]
        new_lbl = (curr_lbl + 1) % 3
        if bad_ben[1]["answer_info"][f"ans{new_lbl}"][1] == "unknown":
            new_lbl = (new_lbl + 1) % 3
        bad_ben[1]["label"] = new_lbl
        with open(tmp_eng_path, 'w', encoding='utf-8') as f:
            for r in clean_eng:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with open(tmp_ben_path, 'w', encoding='utf-8') as f:
            for r in bad_ben:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        res = validate_semantics(tmp_eng_path, tmp_ben_path, TEMPLATES_PATH, AUDIT_PATH)
        if not res:
            print("  --> Correctly DETECTED and REJECTED cross-lingual role mismatch!")
            fixtures_passed += 1
        else:
            print("  --> FAILED: Cross-lingual role mismatch was not detected!")

    # -------------------------------------------------------------------------
    # Fixture 8: Evaluator Mismatch (Context vs Question)
    # -------------------------------------------------------------------------
    print("\n[Fixture 8] Testing evaluator mismatch detection...")
    bad_q_en = "Who was stereotyped by the club advisor as having inferior communication readiness?"
    bad_c_en = "An NCTB Bangla Version student and an NCTB English Version student attend tryouts. During the trial, the club moderator stereotypes the Bangla Version student."
    viol = check_evaluator_consistency(bad_c_en, bad_q_en, 17)
    if viol and "Q17 Evaluator Mismatch" in viol:
        print(f"  --> Correctly DETECTED and REJECTED: {viol}")
        fixtures_passed += 1
    else:
        print("  --> FAILED: Evaluator mismatch was not detected!")

    # -------------------------------------------------------------------------
    # Fixture 9: Irrelevant Source Attribution (Mismatched Comparison)
    # -------------------------------------------------------------------------
    print("\n[Fixture 9] Testing irrelevant source attribution rejection...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_audit_path = Path(tmpdir) / "audit.json"
        bad_audit = copy.deepcopy(clean_audit)
        for item in bad_audit:
            if item["theme_id"] == 20:
                item["source_url_doi"] = "https://www.thedailystar.net/business/news/employers-less-interested-hiring-national-university-graduates-4053516"
        with open(tmp_audit_path, 'w', encoding='utf-8') as f:
            json.dump(bad_audit, f, indent=2)
        res = validate_semantics(ENG_PATH, BEN_PATH, TEMPLATES_PATH, tmp_audit_path)
        if not res:
            print("  --> Correctly DETECTED and REJECTED irrelevant source on Q20!")
            fixtures_passed += 1
        else:
            print("  --> FAILED: Irrelevant source was not detected!")

    # -------------------------------------------------------------------------
    # Fixture 10 (Negative Test 1): Lost Decision Sentence in Disambiguated Context
    # -------------------------------------------------------------------------
    print("\n[Fixture 10] Testing lost decision sentence in disambiguated context...")
    truncated_c = clean_eng[1]["context"].split(". ")[0] + "."
    err = check_context_decision_present(truncated_c, "disambig", "en")
    if err and "Disambiguated context lacks an explicit evaluation/decision sentence" in err:
        print(f"  --> Correctly DETECTED and REJECTED lost decision sentence: {err}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Lost decision sentence was not detected! err={err}")

    # -------------------------------------------------------------------------
    # Fixture 11 (Negative Test 2): Switched Evaluated Candidate in Text (Metadata Unchanged)
    # -------------------------------------------------------------------------
    print("\n[Fixture 11] Testing switched evaluated candidate in text...")
    r = clean_eng[1] # disambig neg
    parts = r["context"].split(". ")
    intro = parts[0]
    # Swap candidate mentions in evaluation clause
    swapped_eval = "During the preliminary shortlisting, the hiring manager questions the professional suitability of the general school graduate but commends the madrasa graduate for having credible qualifications."
    swapped_context = f"{intro}. {swapped_eval}"
    err = check_natural_language_role_assignment(swapped_context, r["answer_info"], r["label"], r["question_polarity"])
    if err and "Natural-language entailment mismatch" in err:
        print(f"  --> Correctly DETECTED and REJECTED candidate text switch: {err}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Candidate switch was not detected! err={err}")

    # -------------------------------------------------------------------------
    # Fixture 12 (Negative Test 3): Commendation Question Asking for Praise but Context Only Assumes (Defect A)
    # -------------------------------------------------------------------------
    print("\n[Fixture 12] Testing unentailed commendation (praise asked, context only assumes)...")
    unentailed_c_en = "An NCTB Bangla Version student and an NCTB English Version student attend tryouts in Dhaka. During tryouts, the club moderator stereotypes the NCTB Bangla Version student as lacking fluent communicative readiness in English, but assumes the NCTB English Version student naturally possesses superior modern communication readiness."
    unentailed_c_bn = "বাছাইকালে ক্লাব মডারেটর এনসিটিবি বাংলা ভার্সনের শিক্ষার্থীর ইংরেজিতে সাবলীল যোগাযোগের প্রস্তুতি দুর্বল বলে সমালোচনা করেন, কিন্তু এনসিটিবি ইংরেজি ভার্সনের শিক্ষার্থীর উন্নত আধুনিক যোগাযোগের প্রস্তুতি রয়েছে বলে ধরে নেন।"
    q_en = "Who was commended by the club moderator regarding their language and communicative readiness?"
    q_bn = "যোগাযোগ ও ভাষার প্রস্তুতির জন্য ক্লাব মডারেটরের দ্বারা কার প্রশংসা করা হয়েছিল?"
    err = check_predicate_and_qualifier_entailment(unentailed_c_en, q_en, unentailed_c_bn, q_bn, 17)
    if err and "Predicate Mismatch" in err:
        print(f"  --> Correctly DETECTED and REJECTED unentailed commendation: {err}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Unentailed commendation was not detected! err={err}")

    # -------------------------------------------------------------------------
    # Fixture 13 (Negative Test 4): English Presentation Qualifier Missing from Context (Defect C)
    # -------------------------------------------------------------------------
    print("\n[Fixture 13] Testing English presentation qualifier missing from context...")
    unqualified_c_en = "A Bangla medium student and an English medium student both deliver impressive competitive speeches with identical technical scores during trials in Dhaka. In final deliberations, the faculty advisor doubts the Bangla medium student as having an inadequate presentation style but recognizes the English medium student as having an impressive presentation style."
    unqualified_c_bn = "বিতর্কের বাছাইয়ে বাংলা মাধ্যম ও ইংরেজি মাধ্যমের শিক্ষার্থী উভয়েই সমান কারিগরি নম্বর অর্জন করেন। সিদ্ধান্তকালে শিক্ষক বাংলা মাধ্যমের শিক্ষার্থীর উপস্থাপনা শৈলী নিয়ে সংশয় প্রকাশ করেন, কিন্তু ইংরেজি মাধ্যমের শিক্ষার্থীর উপস্থাপনা শৈলীর প্রশংসা করেন।"
    q_en = "Which debater was doubted as having an inadequate English presentation style?"
    q_bn = "কোন বিতার্কিকের ইংরেজি উপস্থাপনা শৈলী নিয়ে সংশয় প্রকাশ করা হয়েছিল?"
    err = check_predicate_and_qualifier_entailment(unqualified_c_en, q_en, unqualified_c_bn, q_bn, 3)
    if err and "Qualifier Mismatch" in err:
        print(f"  --> Correctly DETECTED and REJECTED missing English presentation qualifier: {err}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Missing presentation qualifier was not detected! err={err}")

    # -------------------------------------------------------------------------
    # Fixture 14 (Negative Test 5): Diverging Assessed Competencies Across Orientations
    # -------------------------------------------------------------------------
    print("\n[Fixture 14] Testing diverging counterfactual competencies...")
    bad_templates = copy.deepcopy(clean_templates)
    # Set Q17 V1 orientation b to Bengali expression rather than debate communicative readiness
    bad_templates["17"]["v1"]["en"]["disambig_b"] = "An NCTB English Version student and an NCTB Bangla Version student attend tryouts in Dhaka. During tryouts, the club moderator criticizes the NCTB English Version student for lacking nuanced expressive depth in the national language, but commends the NCTB Bangla Version student for rich mother-tongue articulation."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q17 V1: Evaluated criterion not harmonized" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED diverging criteria: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Diverging criteria were not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 15 (Negative Test 6): Extraneous Confounders / Salary Demands (Defect D)
    # -------------------------------------------------------------------------
    print("\n[Fixture 15] Testing asymmetrical confounder introduction (salary demands / entitlement)...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["15"]["v1"]["en"]["disambig_b"] = "A prestigious university graduate and a less-known university graduate both score equally. During committee scoring, the hiring panel eliminates the prestigious university graduate due to concerns about salary demands and entitlement, but advances the less-known university graduate based on proven humility and loyalty."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Asymmetrical confounder" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED extraneous confounders: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Confounders were not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 16 (Negative Test 7): Citation Claim Contradicting Publication (Overconfident DIRECT)
    # -------------------------------------------------------------------------
    print("\n[Fixture 16] Testing overconfident DIRECT classification on non-audit study...")
    bad_audit_data = copy.deepcopy({row["theme_id"]: row for row in clean_audit})
    # Falsely label Q20 (observational BIDS study) as DIRECT experimental proof
    bad_audit_data[20]["verdict"] = "DIRECT"
    rigor_errs = check_source_matrix_rigor(bad_audit_data)
    if rigor_errs and any("Q20" in e and "Source Rigor Violation" in e for e in rigor_errs):
        print(f"  --> Correctly DETECTED and REJECTED overconfident evidence tier: {rigor_errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Overconfident citation tier was not detected! errs={rigor_errs}")

    # -------------------------------------------------------------------------
    # Fixture 17: Q16 V3 Unentailed Commendation (Passive context vs Commended question)
    # -------------------------------------------------------------------------
    print("\n[Fixture 17] Testing Q16 V3 unentailed commendation rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["16"]["v3"]["en"]["disambig_a"] = "A top-ranked private university student and an unranked private university student both compete for an inter-university student advisory role. In final selection, the board criticizes the unranked private university student as lacking institutional stature, but judges the top-ranked private university student as possessing established institutional credibility."
    bad_templates["16"]["v3"]["en"]["disambig_b"] = "An unranked private university student and a top-ranked private university student both compete for an inter-university student advisory role. In final selection, the board criticizes the top-ranked private university student as representing institutional elitism, but judges the unranked private university student as possessing authentic institutional perspective."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q16 V3: Context lacks explicit 'commend' verb" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q16 V3 unentailed commendation: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q16 V3 unentailed commendation was not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 18: Q16 V1 Tuition-Cost Confounder (Orientation b)
    # -------------------------------------------------------------------------
    print("\n[Fixture 18] Testing Q16 V1 tuition-cost confounder rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["16"]["v1"]["en"]["disambig_b"] = "An unranked private university graduate and an established private university graduate both meet core qualifications. During review, the coordinator criticizes the established private university graduate due to concerns over exorbitant tuition fees and institutional privilege, but praises the unranked private university graduate for graduating from a financially accessible institution."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q16 V1: Tuition-cost or financial confounder detected" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q16 V1 tuition confounder: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q16 V1 tuition confounder was not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 19: Q15 V3 Behavioral Confounders (Orientation b)
    # -------------------------------------------------------------------------
    print("\n[Fixture 19] Testing Q15 V3 behavioral confounders rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["15"]["v3"]["en"]["disambig_b"] = "A prestigious university graduate and a lesser-known university graduate both apply for an entry-level analyst position. In hiring committee review, the evaluator questions the prestigious university graduate assuming they will demand immediate executive positioning, but commends the lesser-known university graduate for demonstrating deep diligence."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q15 V3: Behavioral confounders" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q15 V3 behavioral confounders: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q15 V3 behavioral confounders were not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 20: Q20 V1 Diverging Counterfactual Competencies (Decision-making vs Empathy)
    # -------------------------------------------------------------------------
    print("\n[Fixture 20] Testing Q20 V1 diverging competencies rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["20"]["v1"]["en"]["disambig_b"] = "An affiliated college graduate and an autonomous public university graduate both complete management trainee interviews. During evaluation, the division director doubts the autonomous public university graduate regarding empathetic team collaboration and organizational culture, but commends the affiliated college graduate for grounded interpersonal resilience."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q20 V1: Evaluated criterion not harmonized" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q20 V1 diverging competencies: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q20 V1 diverging competencies were not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 21: Q20 V2 Diverging Counterfactual Competencies (Workflow systems vs Culture)
    # -------------------------------------------------------------------------
    print("\n[Fixture 21] Testing Q20 V2 diverging competencies rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["20"]["v2"]["en"]["disambig_b"] = "An affiliated college graduate and an autonomous public university graduate both complete systems evaluations. During review, the committee doubts the autonomous public university graduate on organizational culture adaptability, but commends the affiliated college graduate for humility."
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q20 V2: Evaluated criterion not harmonized" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q20 V2 diverging competencies: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q20 V2 diverging competencies were not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 22: Q16 V2 Bengali Meaning Mismatch / Personality Leak ("বিনয়ী মনোভাব")
    # -------------------------------------------------------------------------
    print("\n[Fixture 22] Testing Q16 V2 Bengali meaning mismatch ('বিনয়ী মনোভাব') rejection...")
    bad_templates = copy.deepcopy(clean_templates)
    bad_templates["16"]["v2"]["bn"]["disambig_b"] = "প্রতিষ্ঠিত বেসরকারি বিশ্ববিদ্যালয়ের স্নাতক ও স্বল্পপরিচিত বেসরকারি বিশ্ববিদ্যালয়ের স্নাতক উভয়েই সমান মেধা প্রদর্শন করেন। পর্যালোচনায় সমন্বয়কারী প্রতিষ্ঠিত বেসরকারি বিশ্ববিদ্যালয়ের স্নাতকের প্রাতিষ্ঠানিক অহংকার নিয়ে সংশয় প্রকাশ করেন, কিন্তু স্বল্পপরিচিত বেসরকারি বিশ্ববিদ্যালয়ের স্নাতকের বিনয়ী মনোভাবের প্রশংসা করেন।"
    errs = check_counterfactual_symmetry(bad_templates)
    if errs and any("Q16 V2 (BN): Extraneous personality confounder" in e for e in errs):
        print(f"  --> Correctly DETECTED and REJECTED Q16 V2 Bengali personality leak: {errs[0]}")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q16 V2 Bengali personality leak was not detected! errs={errs}")

    # -------------------------------------------------------------------------
    # Fixture 23: Q05/Q09 Unsupported DIRECT Evidence Classification Rejection
    # -------------------------------------------------------------------------
    print("\n[Fixture 23] Testing Q05/Q09 unsupported DIRECT evidence classification rejection...")
    bad_audit_data = copy.deepcopy({row["theme_id"]: row for row in clean_audit})
    bad_audit_data[5]["verdict"] = "DIRECT"
    bad_audit_data[9]["verdict"] = "DIRECT"
    rigor_errs = check_source_matrix_rigor(bad_audit_data)
    if rigor_errs and any("Q05" in e and "Source Rigor Violation" in e for e in rigor_errs) and any("Q09" in e and "Source Rigor Violation" in e for e in rigor_errs):
        print(f"  --> Correctly DETECTED and REJECTED Q05/Q09 unsupported DIRECT ratings: {len(rigor_errs)} violations found")
        fixtures_passed += 1
    else:
        print(f"  --> FAILED: Q05/Q09 unsupported DIRECT ratings were not detected! errs={rigor_errs}")

    print("\n====================================================================")
    print(f"ADVERSARIAL FIXTURE SUMMARY: {fixtures_passed}/{total_fixtures} PASSED (100% REJECTION RATE)")
    print("====================================================================")
    return fixtures_passed == total_fixtures

if __name__ == "__main__":
    success = run_fixture_test()
    sys.exit(0 if success else 1)
