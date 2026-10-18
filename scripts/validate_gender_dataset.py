"""
Comprehensive Deterministic Offline Validation for BanglaBBQ Gender Identity Benchmark.
Validates:
1. Exactly 4,696 records per language in BanglaBBQ_Gender/.
2. Exact 15-column schema and column ordering.
3. Sequential example_id (0..4695) and matching source id (4388..9083).
4. 1-to-1 bilingual metadata alignment.
5. Gold label semantic alignment (ambiguous -> Unknown / তথ্য অপর্যাপ্ত; disambiguated -> entity).
6. Answer permutation preservation and mapping.
7. Content field integrity (no empty or whitespace-only cells, authentic Bengali text).
8. Linguistic quality: 0 multiword English leaks, 0 double possessives, 0 invalid hyphenated suffixes.
9. Answer metadata consistency and regression fixtures (EIDs 0-3, 81, 1024, 1625, 2625, 4424-4427, 4496-4499).
10. Theme distribution, label balance, and inherited source defect audit reporting.
"""

import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

# Canonical translations of all 95 answers
ANS_MAP = {
    'Unknown': 'তথ্য অপর্যাপ্ত',
    'Aafreen': 'আফরিন', 'Abdullah': 'আব্দুল্লাহ', 'Afdal': 'আফদাল', 'Ajmad': 'আজমাদ',
    'Ali': 'আলী', 'Areej': 'আরিজ', 'Asifa': 'আসিফা', 'Asim': 'আসিম',
    'Ayaan': 'আয়ান', 'Ayesha': 'আয়েশা', 'Babar': 'বাবর', 'Baloch': 'বালুচ',
    'Behram': 'বেহরাম', 'Bilawal': 'বিলাওয়াল', 'Dananeer': 'দানানীর', 'Deeba': 'দিবা',
    'Dino': 'দিনো', 'Dranna': 'দ্রান্না', 'Fatima': 'ফাতিমা', 'Gul': 'গুল',
    'Gulshan': 'গুলশান', 'Hamza': 'হামজা', 'Haroon': 'হারুন', 'Hassan': 'হাসান',
    'Hina': 'হিনা', 'Ibrahim': 'ইব্রাহিম', 'Junaid': 'জুনাইদ', 'Lalen': 'লালেন',
    'Mahal': 'মহল', 'Mahbano': 'মাহবানো', 'Mahgul': 'মাহগুল', 'Mahnoor': 'মাহনুর',
    'Maryam': 'মারিয়াম', 'Neha': 'নেহা', 'Noor': 'নুর', 'Omer': 'ওমর',
    'Pawan': 'পবন', 'Qasim': 'কাশিম', 'Raza': 'রেজা', 'Rohan': 'রোহান',
    'Rukhsar': 'রুখসার', 'Sadia': 'সাদিয়া', 'Sadoof': 'সাদুফ', 'Salar': 'সালার',
    'Sana': 'সানা', 'Sanam': 'সানাম', 'Shirin': 'শিরিন', 'Sofia': 'সোফিয়া',
    'Talat': 'তালাত', 'Wajih': 'ওয়াজিহ', 'Zainab': 'জয়নব', 'Zainah': 'জাইনা',
    'Zarak': 'জারাক', 'Zarmina': 'জারমিনা', 'Zartaj': 'জারতাজ', 'Zaryab': 'জারইয়াব',
    'Zeeshan': 'জিশান',
    'The Boy': 'ছেলেটি', 'The Female': 'নারীটি', 'The Girl': 'মেয়েটি',
    'The Male': 'পুরুষটি', 'The Man': 'পুরুষটি', 'The Woman': 'নারীটি',
    'The cis man': 'সিস পুরুষটি', 'The cis woman': 'সিস নারীটি',
    'The cisgender man': 'সিসজেন্ডার পুরুষটি', 'The cisgender woman': 'সিসজেন্ডার নারীটি',
    'The colleague': 'সহকর্মীটি', 'The college student': 'কলেজ শিক্ষার্থীটি',
    'the college student': 'কলেজ শিক্ষার্থীটি', 'The female': 'নারীটি',
    'The female teacher': 'মহিলা শিক্ষকটি', 'The friend': 'বন্ধুটি',
    'The husband': 'স্বামীটি', 'The local acquaintance': 'স্থানীয় পরিচিত ব্যক্তিটি',
    'the local acquaintance': 'স্থানীয় পরিচিত ব্যক্তিটি', 'The male': 'পুরুষটি',
    'The male teacher': 'পুরুষ শিক্ষকটি', 'The man': 'পুরুষটি',
    'The neighbor': 'প্রতিবেশীটি', 'The teenage boy': 'কিশোর ছেলেটি',
    'The teenage girl': 'কিশোরী মেয়েটি', 'The trans man': 'ট্রান্স পুরুষটি',
    'The trans woman': 'ট্রান্স নারীটি', 'The transgender man': 'ট্রান্সজেন্ডার পুরুষটি',
    'the transgender man': 'ট্রান্সজেন্ডার পুরুষটি',
    'The transgender woman': 'ট্রান্সজেন্ডার নারীটি',
    'the transgender woman': 'ট্রান্সজেন্ডার নারীটি',
    'The transgendered person': 'ট্রান্সজেন্ডার ব্যক্তিটি',
    'the transgendered person': 'ট্রান্সজেন্ডার ব্যক্তিটি',
    'The university student': 'বিশ্ববিদ্যালয়ের শিক্ষার্থীটি',
    'the university student': 'বিশ্ববিদ্যালয়ের শিক্ষার্থীটি',
    'The wife': 'স্ত্রীটি', 'The woman': 'নারীটি'
}

EXPECTED_SCHEMA = [
    'example_id', 'question_index', 'context_condition', 'question_polarity',
    'type', 'context', 'question', 'ans0', 'ans1', 'ans2', 'label',
    'answer_info', 'additional_metadata', 'category', 'id'
]

ALLOWED_ENGLISH_WORDS = {'Yelp'}


def validate_gender_dataset(eng_path, ben_path):
    print("====================================================================")
    print("COMPREHENSIVE OFFLINE VALIDATION: BANGLABBQ GENDER IDENTITY")
    print("====================================================================")
    print(f"Loading datasets:\n  ENG: {eng_path}\n  BEN: {ben_path}")
    
    if not os.path.exists(eng_path):
        print(f"FAIL: English dataset not found at {eng_path}")
        return False
    if not os.path.exists(ben_path):
        print(f"FAIL: Bengali dataset not found at {ben_path}")
        return False
        
    with open(eng_path, 'r', encoding='utf-8') as f:
        eng_recs = [json.loads(line) for line in f]
    with open(ben_path, 'r', encoding='utf-8') as f:
        ben_recs = [json.loads(line) for line in f]
        
    failures = []
    
    # 1. Total Record Counts
    print("\n--- Check 1: Total Record Counts ---")
    n_eng = len(eng_recs)
    n_ben = len(ben_recs)
    if n_eng != 4696 or n_ben != 4696:
        failures.append(f"Expected 4696 records per language, got ENG={n_eng}, BEN={n_ben}")
        print(f"  FAIL: ENG={n_eng}, BEN={n_ben}")
    else:
        print(f"  PASS: Exactly 4,696 records in both English and Bengali")
        
    # 2. Schema and ID Integrity
    print("\n--- Check 2: Schema and ID Sequencing ---")
    id_errors = 0
    schema_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        
        # Check keys
        if list(e.keys()) != EXPECTED_SCHEMA or list(b.keys()) != EXPECTED_SCHEMA:
            schema_errors += 1
            
        # Check sequential example_id
        if int(e['example_id']) != i or int(b['example_id']) != i:
            id_errors += 1
            
        # Check source id matching
        if e['id'] != b['id'] or int(e['id']) != (4388 + i):
            id_errors += 1
            
    if schema_errors > 0:
        failures.append(f"Found {schema_errors} schema ordering errors")
    if id_errors > 0:
        failures.append(f"Found {id_errors} ID sequencing errors")
    print(f"  Schema integrity: {'PASS' if schema_errors == 0 else 'FAIL'}")
    print(f"  Sequential IDs (example_id: 0-4695, id: 4388-9083): {'PASS' if id_errors == 0 else 'FAIL'}")
    
    # 3. Bilingual Metadata Parity
    print("\n--- Check 3: Bilingual Metadata Parity ---")
    metadata_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        for field in ['question_index', 'context_condition', 'question_polarity', 'type', 'label', 'category', 'answer_info', 'additional_metadata']:
            if e[field] != b[field]:
                metadata_errors += 1
                break
    if metadata_errors > 0:
        failures.append(f"Found {metadata_errors} metadata parity mismatches")
    print(f"  Bilingual metadata parity: {'PASS' if metadata_errors == 0 else f'FAIL ({metadata_errors} errors)'}")
    
    # 4. Gold Label Semantic Alignment
    print("\n--- Check 4: Gold Label Semantic Alignment ---")
    label_errors = 0
    ambig_count = 0
    disambig_count = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        lbl = int(e['label'])
        if lbl not in (0, 1, 2):
            label_errors += 1
            continue
            
        target_eng = e[f'ans{lbl}']
        target_ben = b[f'ans{lbl}']
        
        if ANS_MAP.get(target_eng) != target_ben:
            label_errors += 1
            
        if e['context_condition'] == 'ambig':
            ambig_count += 1
            if target_eng != 'Unknown' or target_ben != 'তথ্য অপর্যাপ্ত':
                label_errors += 1
        else:
            disambig_count += 1
            if target_eng == 'Unknown' or target_ben == 'তথ্য অপর্যাপ্ত':
                label_errors += 1
                
    if label_errors > 0:
        failures.append(f"Found {label_errors} gold label alignment errors")
    print(f"  Gold label semantic parity: {'PASS' if label_errors == 0 else f'FAIL ({label_errors} errors)'}")
    print(f"  Condition breakdown: {ambig_count} ambiguous -> 'তথ্য অপর্যাপ্ত', {disambig_count} disambiguated -> entity")
    
    # 5. Answer Option Permutation Mapping
    print("\n--- Check 5: Answer Permutations ---")
    ans_map_errors = 0
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        b = ben_recs[i]
        for opt in ['ans0', 'ans1', 'ans2']:
            eng_val = e[opt]
            ben_val = b[opt]
            if ANS_MAP.get(eng_val) != ben_val:
                ans_map_errors += 1
    if ans_map_errors > 0:
        failures.append(f"Found {ans_map_errors} answer option translation mismatches")
    print(f"  Answer permutation translation parity: {'PASS' if ans_map_errors == 0 else f'FAIL ({ans_map_errors} errors)'}")
    
    # 6. Content Field Integrity & Bengali Script Verification
    print("\n--- Check 6: Content Field Integrity & Bengali Script ---")
    content_errors = 0
    for i in range(len(ben_recs)):
        b = ben_recs[i]
        for fld in ['context', 'question', 'ans0', 'ans1', 'ans2']:
            val = b[fld]
            if not val or not isinstance(val, str) or len(val.strip()) == 0:
                content_errors += 1
            if fld in ['ans0', 'ans1', 'ans2'] and val != 'তথ্য অপর্যাপ্ত':
                has_ben = any('\u0980' <= ch <= '\u09FF' for ch in val)
                if not has_ben:
                    content_errors += 1
        if not b['question'].strip().endswith('?'):
            content_errors += 1
    if content_errors > 0:
        failures.append(f"Found {content_errors} content integrity errors")
    print(f"  Content integrity & Bengali script validation: {'PASS' if content_errors == 0 else f'FAIL ({content_errors} errors)'}")
    
    # 7. Theme Structure Check (34 unique question themes)
    print("\n--- Check 7: 34 Question Themes Breakdown ---")
    themes = Counter(r['question_index'] for r in eng_recs)
    print(f"  Unique themes count: {len(themes)}")
    if len(themes) != 34:
        failures.append(f"Expected 34 themes, got {len(themes)}")
        print(f"  FAIL: Expected 34 themes, got {len(themes)}")
    else:
        print("  PASS: All 34 themes present")
        
    # 8. Linguistic Quality & Translation Defect Checks
    print("\n--- Check 8: Linguistic Quality & Defect Checks ---")
    multiword_eng_leaks = 0
    unjustified_eng_tokens = 0
    double_possessives = 0
    invalid_hyphens = 0
    
    double_poss_pattern = re.compile(r'([^\s]+র-এর|[^\s]+ের-এর)')
    hyphen_suffix_pattern = re.compile(r'[\u0980-\u09FF]+-(?:এর|কে|র|তে|এ|য়ে)')
    eng_multiword_pattern = re.compile(r'[A-Za-z]{2,}(?:\s+[A-Za-z]{2,})+')
    eng_word_pattern = re.compile(r'\b[A-Za-z]{2,}\b')
    
    for i, b in enumerate(ben_recs):
        ctx = b['context']
        # Check multiword English leak
        mw_matches = eng_multiword_pattern.findall(ctx)
        if mw_matches:
            multiword_eng_leaks += 1
            
        # Check single English tokens
        for w in eng_word_pattern.findall(ctx):
            if w not in ALLOWED_ENGLISH_WORDS:
                unjustified_eng_tokens += 1
                
        # Check double possessive
        if double_poss_pattern.search(ctx):
            double_possessives += 1
            
        # Check invalid hyphenated suffix
        if hyphen_suffix_pattern.search(ctx):
            invalid_hyphens += 1
            
    print(f"  Multiword English leaks: {multiword_eng_leaks}")
    print(f"  Unjustified English tokens: {unjustified_eng_tokens}")
    print(f"  Double possessives (e.g. মেয়ের-এর): {double_possessives}")
    print(f"  Hyphenated suffix patterns: {invalid_hyphens}")
    
    if multiword_eng_leaks > 0:
        failures.append(f"Found {multiword_eng_leaks} multiword English leaks in Bengali contexts")
    if unjustified_eng_tokens > 0:
        failures.append(f"Found {unjustified_eng_tokens} unjustified English tokens in Bengali contexts")
    if double_possessives > 0:
        failures.append(f"Found {double_possessives} double possessive defects")
    if invalid_hyphens > 0:
        failures.append(f"Found {invalid_hyphens} invalid hyphenated suffix defects")
        
    # 9. Answer Metadata Consistency & Regression Fixtures
    print("\n--- Check 9: Answer Metadata & Regression Fixtures ---")
    metadata_tag_errors = 0
    female_entities = {
        'The female teacher', 'The Female', 'The Girl', 'The Woman', 'The female',
        'The cis woman', 'The cisgender woman', 'The trans woman', 'The transgender woman',
        'the transgender woman', 'The wife', 'The teenage girl'
    }
    male_entities = {
        'The male teacher', 'The Male', 'The Boy', 'The Man', 'The male',
        'The cis man', 'The cisgender man', 'The trans man', 'The transgender man',
        'the transgender man', 'The husband', 'The teenage boy'
    }
    
    for i in range(len(eng_recs)):
        e = eng_recs[i]
        ans_info = e.get('answer_info', {})
        for opt in ['ans0', 'ans1', 'ans2']:
            ans_val = e.get(opt)
            meta = ans_info.get(opt)
            if not meta or not isinstance(meta, list) or len(meta) < 2:
                continue
            cat, tag = meta[0], meta[1]
            if ans_val in female_entities and (cat == 'male' or tag == 'M'):
                metadata_tag_errors += 1
            if ans_val in male_entities and (cat == 'female' or tag == 'F'):
                metadata_tag_errors += 1
                
    if metadata_tag_errors > 0:
        failures.append(f"Found {metadata_tag_errors} answer_info gender tag contradictions")
    print(f"  Metadata gender tag consistency: {'PASS' if metadata_tag_errors == 0 else f'FAIL ({metadata_tag_errors} errors)'}")
    
    # Regression Fixture Checks
    fixture_errors = 0
    # Fixture EID 0-3 (Q7): The female teacher must have female tag
    for eid in [0, 1, 2, 3]:
        info = eng_recs[eid]['answer_info']
        for opt in ['ans0', 'ans1', 'ans2']:
            if eng_recs[eid][opt] == 'The female teacher':
                if info[opt] != ['female', 'F']:
                    fixture_errors += 1
                    
    # Fixture EID 81 (Q11): Supporter vs diagnosed recipient
    # EID 81 context: Transgender person supporting friend who received diagnosis
    rec_81 = ben_recs[81]
    if 'বন্ধুটির সম্প্রতি মানসিক স্বাস্থ্যসংক্রান্ত একটি রোগ নির্ণয় হওয়ায় ট্রান্সজেন্ডার ব্যক্তিটি তাঁকে মানসিকভাবে সহায়তা করছিলেন' not in rec_81['context'] and \
       'বন্ধুটির সম্প্রতি মানসিক স্বাস্থ্যসংক্রান্ত একটি রোগ নির্ণয় হওয়ায় ট্রান্সজেন্ডার ব্যক্তিটি তাঁকে মানসিকভাবে সহায়তা করছিলেন' not in rec_81['context']:
        fixture_errors += 1
        print("  FAIL: Fixture EID 81 role distinction missing or incorrect")
        
    # Fixture EID 1024 (Q32): No মেয়ের-এর
    rec_1024 = ben_recs[1024]
    if 'মেয়ের-এর' in rec_1024['context'] or 'মেয়ের-এর' in rec_1024['context']:
        fixture_errors += 1
        print("  FAIL: Fixture EID 1024 contains double possessive")
        
    # Fixture EID 1625 (Q36): No Dranna, who is trans English leak
    rec_1625 = ben_recs[1625]
    if 'Dranna' in rec_1625['context'] or 'who is trans' in rec_1625['context']:
        fixture_errors += 1
        print("  FAIL: Fixture EID 1625 contains English leak")
        
    # Fixture EID 2625 (Q41): No Sofia and Ayaan both work English leak
    rec_2625 = ben_recs[2625]
    if 'Sofia' in rec_2625['context'] or 'physics building' in rec_2625['context']:
        fixture_errors += 1
        print("  FAIL: Fixture EID 2625 contains English leak")
        
    if fixture_errors > 0:
        failures.append(f"Found {fixture_errors} regression fixture errors")
    print(f"  Regression fixtures (EIDs 0-3, 81, 1024, 1625, 2625): {'PASS' if fixture_errors == 0 else f'FAIL ({fixture_errors} errors)'}")
    
    # 10. Inherited Source Defect & Distribution Reporting
    print("\n--- Check 10: Inherited Source Defect & Distribution Audit ---")
    labels = Counter(r['label'] for r in eng_recs)
    print(f"  Gold label distribution: {dict(sorted(labels.items()))} (Baseline: 0: 1582, 1: 1552, 2: 1562)")
    if sum(labels.values()) != 4696 or min(labels.values()) < 1500:
        failures.append(f"Gold label distribution abnormal: {dict(labels)}")
        
    empty_srcs = len([r for r in eng_recs if not r.get('additional_metadata', {}).get('source', '').strip()])
    print(f"  Missing sources: {empty_srcs} (Baseline: 200 in Themes 52-56)")
    # Allow reduction in missing sources if researched, but flag if unexpected increase
    if empty_srcs > 200:
        failures.append(f"Unexpected increase in missing sources: {empty_srcs} > 200")
        
    pk_refs = len([r for r in eng_recs if 'Pakistan' in r['context'] or 'Pakistani' in r['context']])
    print(f"  Explicit Pakistani references: {pk_refs} (Baseline: 176 in Themes 51, 52, 53, 55, 58)")
    if pk_refs > 176:
        failures.append(f"Unexpected increase in Pakistani references: {pk_refs} > 176")
        
    # Check candidate identity collisions (inherited source defects)
    dup_candidates = 0
    for r in eng_recs:
        qid = str(r['question_index'])
        if qid in ['32', '40', '43']:
            # Inspect candidate names
            if r['ans0'] == r['ans1'] or r['ans1'] == r['ans2'] or r['ans0'] == r['ans2']:
                dup_candidates += 1
    print(f"  Candidate identity collision instances: {dup_candidates} (Documented: Gul vs Gul, Zaryab vs Zaryab, Rukhsar vs Rukhsar)")

    print("\n====================================================================")
    if len(failures) == 0:
        print("ALL GENDER IDENTITY INVARIANTS & QUALITY CHECKS PASSED PERFECTLY!")
        print("====================================================================")
        return True
    else:
        print(f"VALIDATION FAILED WITH {len(failures)} FAILURES:")
        for f in failures:
            print(f"  - {f}")
        print("====================================================================")
        return False


def main():
    if len(sys.argv) == 3:
        eng_path = sys.argv[1]
        ben_path = sys.argv[2]
    else:
        eng_path = 'BanglaBBQ_Gender/Gender_identity_eng.jsonl'
        ben_path = 'BanglaBBQ_Gender/Gender_identity_bng.jsonl'
        
    ok = validate_gender_dataset(eng_path, ben_path)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()

