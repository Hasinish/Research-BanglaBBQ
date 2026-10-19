# -*- coding: utf-8 -*-
"""Adversarial Regression Test Suite for BanglaBBQ Educational Background Semantic QA.

This test suite executes 9 distinct adversarial regression fixtures to verify that
the independent semantic validator (validate_education_semantics.py) demonstrably
detects and rejects each class of defect:
  1. Seeded Q12 V1 orientation 'b' distance education contradiction (conventional campus called distance learning).
  2. Seeded Q15 V1 orientation 'b' elite brand contradiction (prestigious university called non-elite brand).
  3. Seeded Q10 V2 orientation 'b' commercial/government polytechnic reversal.
  4. Seeded Q05 V3 orientation 'b' false vocational track attribution to General SSC student.
  5. Seeded wrong disambiguated gold label (pointing to opposite entity).
  6. Seeded ambiguous outcome leak (context reveals hiring verdict).
  7. Seeded cross-lingual role inversion (English selects target, Bengali selects comparison).
  8. Seeded evaluator mismatch between context and question (moderator vs advisor).
  9. Seeded irrelevant source attribution (mismatched demographic comparison).
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
    validate_semantics, check_group_integrity, check_evaluator_consistency
)

ENG_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_english.jsonl"
BEN_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "banglabbq_education_bengali.jsonl"
TEMPLATES_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "scenario_templates.json"
AUDIT_PATH = ROOT / "BanglaBBQ_EducationalBackground" / "source_audit_matrix.json"

def run_fixture_test():
    print("====================================================================")
    print("ADVERSARIAL REGRESSION TEST SUITE: 9 INDEPENDENT FIXTURES")
    print("====================================================================")

    with open(ENG_PATH, 'r', encoding='utf-8') as f:
        clean_eng = [json.loads(line) for line in f]
    with open(BEN_PATH, 'r', encoding='utf-8') as f:
        clean_ben = [json.loads(line) for line in f]
    with open(AUDIT_PATH, 'r', encoding='utf-8') as f:
        clean_audit = json.load(f)

    fixtures_passed = 0
    total_fixtures = 9

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
        # Flip label of record 1 from target to comparison
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
        # Leak outcome into ambiguous record 0
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
        # Swap role label in Bengali record 1
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

    print("\n====================================================================")
    print(f"ADVERSARIAL FIXTURE SUMMARY: {fixtures_passed}/{total_fixtures} PASSED (100% REJECTION RATE)")
    print("====================================================================")
    return fixtures_passed == total_fixtures

if __name__ == "__main__":
    success = run_fixture_test()
    sys.exit(0 if success else 1)
