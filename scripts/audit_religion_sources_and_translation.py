#!/usr/bin/env python3
"""Comprehensive audit of Religion benchmark sources, translations, and counterfactuals.

Audits all 20 Religion themes for:
1. Source relevance and grounding classification (incident-specific vs broad thematic).
2. Counterfactual symmetry across orientations A and B.
3. Structural checks of the disambiguated non-Unknown gold and ambiguous Unknown targets (not independent natural-language entailment certification).
4. Bilingual structural checks and reported translation-review limitations (not professional Bengali certification).
5. Answer permutation balance (3! = 6 per block).
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Dataset_BanglaBBQ_New/BanglaBBQ_Religion"
if not BASE.exists():
    BASE = ROOT / "BanglaBBQ_Religion"
ENG_PATH = BASE / "Religion_eng.jsonl"
BEN_PATH = BASE / "Religion_bng.jsonl"

SOURCE_EVALUATION = {
    1: {"type": "Incident Context", "notes": "Cites Daily Star reporting on widespread attacks on minority households/businesses following August 5, 2024 political transition."},
    2: {"type": "Thematic Background", "notes": "Cites Minority Rights Group (MRG) community profile on socio-economic vulnerabilities of Hindus in Bangladesh."},
    3: {"type": "IIDS Dalit Working Paper", "notes": "Reports Dalit water-access restrictions at privately controlled ponds; the exact Hindu-Dalit versus Muslim-Dalit contrast is a fictional intersectional counterfactual, not a measured religion-only effect."},
    4: {"type": "Human Rights Analysis", "notes": "Cites Daily Star human rights analysis regarding identity controversy and fear among minority children."},
    5: {"type": "Government Policy Note", "notes": "Cites UK Home Office CPIN (June 2025) on treatment of religious minorities and atheists in Bangladesh; grounds secular/nonreligious discrimination."},
    6: {"type": "Thematic Background", "notes": "Cites MRG report on educational barriers and cultural tensions experienced by Hindu students."},
    7: {"type": "Human Rights Report", "notes": "Cites Human Rights Watch report on systematic civic and religious persecution of the Ahmadiyya community in Bangladesh."},
    8: {"type": "High Court Reportage", "notes": "Daily Star (24 February 2026) reports High Court inquiry into an alleged legal-affairs job advertisement with Muslim-only eligibility. Revised scenario tests initial religion-based application screening, not a final hiring outcome or proven real incident."},
    9: {"type": "IIDS Dalit Working Paper", "notes": "IIDS working paper discusses school scholarship selection disadvantages among Dalit children; controlled Hindu-Dalit/Muslim-Dalit pairing is illustrative and does not establish religion-only causation."},
    10: {"type": "IIDS Dalit Working Paper", "notes": "IIDS reports Dalit children of both religions facing exclusion from school cultural activities, not the specific fictional equal-score performance audition."},
    11: {"type": "Thematic Report", "notes": "Cites MRG report documenting land disputes and institutional vulnerabilities of indigenous Buddhist communities in Bangladesh."},
    12: {"type": "Associated Press Reporting", "notes": "AP documents opposition to an Uttara Hindu festival venue in 2024 and organizers using a smaller location; equal-use Hindu/Muslim festival venue permits in the benchmark are fictional counterfactuals, with real-world venue-use confounds acknowledged."},
    13: {"type": "IIDS Dalit Working Paper", "notes": "IIDS documents non-Dalit wedding/feast exclusion of Dalits, including differential experiences by religion. Revised comparison matches Dalit status and relationships; no proof of a pure religion causal effect."},
    14: {"type": "Journalistic Investigation", "notes": "Cites Daily Star report on fear of discrimination among religious minorities in public and government service appointments."},
    15: {"type": "Journalistic Investigation", "notes": "Cites Daily Star spotlight on rental housing discrimination faced by minority tenants in Dhaka."},
    16: {"type": "Human Rights Report", "notes": "Cites Human Rights Watch report on social boycotts and exclusion of Ahmadiyya Muslim youth and students."},
    17: {"type": "Human Rights Report", "notes": "Cites MRG report on discrimination and healthcare access hurdles faced by religious minorities in rural districts."},
    18: {"type": "News Investigation", "notes": "Cites India Today report documenting discrimination in relief distribution during the catastrophic August 2024 floods in Feni/Noakhali."},
    19: {"type": "Thematic Background", "notes": "Cites MRG community profile on residential security and communal property pressures."},
    20: {"type": "Investigative Journalism", "notes": "Cites bdnews24 investigative report on historical admission restrictions excluding religious minority students from two premier Chittagong government high schools until 2006."}
}

def main():
    print("====================================================================")
    print("COMPREHENSIVE RELIGION AUDIT: SOURCES, TRANSLATION & COUNTERFACTUALS")
    print("====================================================================")

    eng_recs = [json.loads(line) for line in ENG_PATH.read_text(encoding='utf-8').splitlines() if line.strip()]
    ben_recs = [json.loads(line) for line in BEN_PATH.read_text(encoding='utf-8').splitlines() if line.strip()]

    assert len(eng_recs) == len(ben_recs) and len(eng_recs) in (960, 2880)
    count = len(eng_recs)
    wording_variants = ('v1',) if count == 960 else ('v1', 'v2', 'v3')

    print("\n--- 1. Theme-by-Theme Grounding & Source Classification ---")
    for q in range(1, 21):
        q_eng = [r for r in eng_recs if r['question_index'] == q]
        q_ben = [r for r in ben_recs if r['question_index'] == q]
        meta = q_eng[0]['additional_metadata']
        source = meta.get('source')
        groups = meta.get('stereotyped_groups')
        eval_info = SOURCE_EVALUATION.get(q, {"type": "General", "notes": "No notes"})

        print(f"\n[Q{q:02d}] Stereotyped Groups: {groups}")
        print(f"  Source URL:  {source}")
        print(f"  Classification: {eval_info['type']}")
        print(f"  Audit Note:  {eval_info['notes']}")
        print(f"  Sample Question (EN): {q_eng[0]['question']}")
        print(f"  Sample Question (BN): {q_ben[0]['question']}")

    print("\n--- 2. Counterfactual Balance & Reversibility Verification ---")
    cf_errors = 0
    for q in range(1, 21):
        q_eng = [r for r in eng_recs if r['question_index'] == q]
        for wording in wording_variants:
            ver_a = [r for r in q_eng if r['additional_metadata'].get('version') == 'a' and r['additional_metadata'].get('wording_variant', 'v1') == wording]
            ver_b = [r for r in q_eng if r['additional_metadata'].get('version') == 'b' and r['additional_metadata'].get('wording_variant', 'v1') == wording]
            if len(ver_a) != 24 or len(ver_b) != 24:
                cf_errors += 1
                print(f"  Q{q:02d}/{wording} wrong counterfactual counts: a={len(ver_a)}, b={len(ver_b)}")
                continue
            for cond in ('ambig', 'disambig'):
                for pol in ('neg', 'nonneg'):
                    sub_a = [r for r in ver_a if r['context_condition'] == cond and r['question_polarity'] == pol]
                    sub_b = [r for r in ver_b if r['context_condition'] == cond and r['question_polarity'] == pol]
                    if len(sub_a) != 6 or len(sub_b) != 6:
                        cf_errors += 1
                        continue
                    if cond == 'disambig':
                        target_a = sub_a[0]['answer_info']['ans' + str(sub_a[0]['label'])][1]
                        target_b = sub_b[0]['answer_info']['ans' + str(sub_b[0]['label'])][1]
                        if target_a == target_b:
                            cf_errors += 1
                            print(f"  Q{q:02d}/{wording}/{pol}: answer roles did not reverse: {target_a} / {target_b}")

    print(f"  Counterfactual Symmetry & Reversibility across all 20 themes: {'PASS' if cf_errors == 0 else f'FAIL ({cf_errors} errors)'}")

    print("\n--- 3. Ambiguous/Disambiguated Label-Role Checks (Not Entailment Proof) ---")
    ambig_err = 0
    disambig_err = 0
    for i, (e, b) in enumerate(zip(eng_recs, ben_recs)):
        if e['context_condition'] == 'ambig':
            if e['ans' + str(e['label'])] != 'Unknown' or b['ans' + str(b['label'])] != 'অজানা':
                ambig_err += 1
        else:
            if e['ans' + str(e['label'])] == 'Unknown' or b['ans' + str(b['label'])] == 'অজানা':
                disambig_err += 1
    print(f"  Ambiguous contexts target Unknown/অজানা ({count//2} rows): {'PASS' if ambig_err == 0 else f'FAIL ({ambig_err})'}")
    print(f"  Disambiguated gold answers are named entities ({count//2} rows): {'PASS' if disambig_err == 0 else f'FAIL ({disambig_err})'}")

    print("\n====================================================================")
    print("AUDIT RESULT: STRUCTURAL LABEL AND COUNTERFACTUAL CHECKS ONLY")
    print("LIMITATION: Independent native Bengali linguistic naturalness review")
    print("and independent source-to-scenario relevance checks remain required.")
    print("====================================================================")
    if cf_errors or ambig_err or disambig_err:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
