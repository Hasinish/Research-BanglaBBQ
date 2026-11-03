import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    erows = [json.loads(line) for line in f]
with open('fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl', 'r', encoding='utf-8') as f:
    brows = [json.loads(line) for line in f]

# Check demographic words
demographics_eng = ['Hindu', 'Muslim', 'Ahmadiyya', 'Sunni', 'Buddhist', 'Christian', 'Dalit Hindu', 'Dalit Muslim', 'nonreligious']
demographics_ben = ['হিন্দু', 'মুসলিম', 'আহমদিয়া', 'সুন্নি', 'বৌদ্ধ', 'খ্রিষ্টান', 'দলিত হিন্দু', 'দলিত মুসলিম', 'ধর্মবিশ্বাসহীন']

for lang, rows in [("ENG", erows), ("BEN", brows)]:
    neg_first, neg_second = 0, 0
    nonneg_first, nonneg_second = 0, 0
    
    for r in rows:
        if r['context_condition'] == 'disambig':
            ctx = r['context']
            ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
            e0, e1 = ans_ents[0], ans_ents[1]
            
            # Find which demographic term appears first in ctx
            # Extract demographic from e0 and e1
            def extract_demo(ent, lang):
                if lang == "ENG":
                    for d in ['Dalit Hindu', 'Dalit Muslim', 'Ahmadiyya Muslim', 'Sunni Muslim', 'Hindu', 'Muslim', 'Buddhist', 'Christian', 'nonreligious']:
                        if d in ent: return d
                else:
                    for d in ['দলিত হিন্দু', 'দলিত মুসলিম', 'আহমদিয়া মুসলিম', 'সুন্নি মুসলিম', 'হিন্দু', 'মুসলিম', 'বৌদ্ধ', 'খ্রিষ্টান', 'ধর্মবিশ্বাসহীন']:
                        if d in ent: return d
                return ent
                
            d0 = extract_demo(e0, lang)
            d1 = extract_demo(e1, lang)
            
            p0 = ctx.find(d0)
            p1 = ctx.find(d1)
            
            first_ent = e0 if p0 < p1 else e1
            second_ent = e1 if p0 < p1 else e0
            gold = r[f"ans{r['label']}"]
            
            if r['question_polarity'] == 'neg':
                if gold == first_ent: neg_first += 1
                else: neg_second += 1
            else:
                if gold == first_ent: nonneg_first += 1
                else: nonneg_second += 1
                
    print(f"Demographic-based {lang} Disambig Position Balance:")
    print(f"  Neg:    First={neg_first}, Second={neg_second}")
    print(f"  NonNeg: First={nonneg_first}, Second={nonneg_second}")
