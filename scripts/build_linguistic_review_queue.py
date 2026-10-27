import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_FILE = ROOT / 'local_candidates/final_seven_category_qa/linguistic_review_queue.csv'

# We will collect high-priority examples from candidate and production files for human linguistic adjudication
review_rows = []
review_id_counter = 1

def add_queue_item(category, theme_id, variation, example_id, bn_ctx, bn_q, bn_ans, defect_type, issue_desc, check_prompt):
    global review_id_counter
    review_rows.append({
        'review_id': f"LRQ-{review_id_counter:04d}",
        'category': category,
        'theme_id': theme_id,
        'variation': variation,
        'example_id': example_id,
        'bengali_context': bn_ctx,
        'bengali_question': bn_q,
        'bengali_options_and_gold': bn_ans,
        'defect_type': defect_type,
        'flagged_issue_description': issue_desc,
        'recommended_human_eval_check': check_prompt,
        'status_label': 'NEEDS HUMAN REVIEW'
    })
    review_id_counter += 1

# 1. Ethnicity: Synthetic placeholders ('শিক্ষার্থী ক' / 'ব্যক্তি ক')
eth_bn = ROOT / 'local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl'
with open(eth_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        ctx = r['context']
        if 'শিক্ষার্থী ক' in ctx or 'ব্যক্তি ক' in ctx or 'প্রতিযোগী ক' in ctx or 'আবেদনকারী ক' in ctx:
            if r['example_id'] in [0, 48, 96, 144, 192, 240, 288, 336, 384, 432]: # 1 representative per theme
                add_queue_item(
                    category='Ethnicity',
                    theme_id=f"Q{int(r['question_index']):02d}",
                    variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                    example_id=r['example_id'],
                    bn_ctx=ctx,
                    bn_q=r['question'],
                    bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                    defect_type='SYNTHETIC_PLACEHOLDER_NAMES',
                    issue_desc="Uses artificial placeholders ('ক' and 'খ') instead of culturally authentic Bangladeshi indigenous and Bengali names.",
                    check_prompt="Judge whether synthetic letters ('ক'/'খ') diminish naturalness or introduce artificial reading comprehension cues."
                )

# 2. Regional Affiliation: Unnatural district phrasing ('জেলা থেকে আসা ব্যক্তি')
reg_bn = ROOT / 'local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Regional_FINAL_bengali.jsonl'
with open(reg_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        ctx = r['context']
        if 'থেকে আসা' in ctx and r['example_id'] in [0, 96, 192, 288, 384, 480, 576, 672, 768, 864]:
            add_queue_item(
                category='Regional Affiliation',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=ctx,
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='UNNATURAL_REGIONAL_DESCRIPTORS',
                issue_desc="Repetitive phrasing '[District] থেকে আসা ব্যক্তি' used in lieu of natural regional demonyms or authentic origin contexts.",
                check_prompt="Determine if natural dialect markers or authentic demonyms should be used without introducing unwanted linguistic complexity."
            )

# 3. Health Status: Confounder with legitimate infection control / medical precaution
hs_bn = ROOT / 'local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Health_Status_FINAL_bengali.jsonl'
with open(hs_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        if r['question_index'] in [1, 2, 4, 7] and r['example_id'] in [0, 48, 144, 288]:
            add_queue_item(
                category='Health Status',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=r['context'],
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='CONFOUNDED_MEDICAL_PRECAUTION',
                issue_desc="Potential confounder between irrational stigma vs legitimate infection prevention / occupational health protocols.",
                check_prompt="Adjudicate whether the adverse verdict is perceived as irrational social stigma or standard medical transmission safeguard."
            )

# 4. Occupational Background: Confounding tea garden workers with caste/ethnicity (Q07) & elevator access (Q03)
occ_bn = ROOT / 'Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_Occupational_Background_FINAL_bengali.jsonl'
with open(occ_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        if int(r['question_index']) in [3, 7, 8] and r['example_id'] in [96, 288, 336]:
            add_queue_item(
                category='Occupational Background',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=r['context'],
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='ETHNIC_CASTE_CONFOUNDING_AND_CLASS_HIERARCHY',
                issue_desc="Tea garden worker discrimination (Q07) is historically entwined with marginalized ethnic minority status, confounding occupational bias with ethnic bias.",
                check_prompt="Verify if tea worker bias in Bangladesh can be evaluated purely as occupational without triggering ethnic/caste stereotypes."
            )

# 5. Marital Status: Extreme concentration on 'বাঘ-বিধবা' (Tiger Widows) in Q04, Q07, Q10
mar_bn = ROOT / 'Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_MaritalStatus_FINAL_bengali.jsonl'
with open(mar_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        if int(r['question_index']) in [4, 7, 10] and r['example_id'] in [144, 288, 432]:
            add_queue_item(
                category='Marital Status',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=r['context'],
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='HIGH_FREQUENCY_GEOGRAPHIC_STEREOTYPE',
                issue_desc="3 out of 10 marital status themes focus exclusively on Sundarbans 'Tiger Widows' (বাঘ-বিধবা), which is a localized regional phenomena rather than a nationwide marital stereotype.",
                check_prompt="Assess whether 30% tiger widow representation distorts general Bangladeshi marital status evaluation and if urban divorcee/widow themes should replace some."
            )

# 6. Social Status: Generic English loan translation syntax
ss_bn = ROOT / 'Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_SocialStatus_FINAL_bengali.jsonl'
with open(ss_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        if int(r['question_index']) in [1, 5, 9] and r['example_id'] in [0, 192, 384]:
            add_queue_item(
                category='Social Status',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=r['context'],
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='CALQUE_TRANSLATION_REGISTER',
                issue_desc="Formalized bureaucratic phrasing like 'উচ্চ সামাজিক মর্যাদা সম্পন্ন ব্যক্তি' or 'নিম্ন আয়ের পারিবারিক প্রেক্ষাপট' sounds translated from English sociology papers rather than natural Bengali dialogue.",
                check_prompt="Rate Bengali phrasing naturalness on a 1-5 scale and suggest idiomatic conversational phrasing."
            )

# 7. Physical Appearance: Casting & profession confounding
pa_bn = ROOT / 'Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_Physical_Appearance_FINAL_bengali.jsonl'
with open(pa_bn, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        if int(r['question_index']) in [1, 3, 6] and r['example_id'] in [0, 96, 240]:
            add_queue_item(
                category='Physical Appearance',
                theme_id=f"Q{int(r['question_index']):02d}",
                variation=f"V{r.get('scenario_variation_id', r.get('scenario_variation', ''))}",
                example_id=r['example_id'],
                bn_ctx=r['context'],
                bn_q=r['question'],
                bn_ans=f"Gold: {r['label']} | Options: 0:{r['ans0']}, 1:{r['ans1']}, 2:{r['ans2']}",
                defect_type='ROLE_RELEVANT_APPEARANCE_CONFOUNDER',
                issue_desc="In acting, flight attendant, or modeling roles, appearance attributes may be interpreted as domain-specific occupational criteria rather than pure social bias.",
                check_prompt="Evaluate whether the benchmark scenario disentangles role requirements from irrational aesthetic discrimination."
            )

fieldnames = [
    'review_id', 'category', 'theme_id', 'variation', 'example_id',
    'bengali_context', 'bengali_question', 'bengali_options_and_gold',
    'defect_type', 'flagged_issue_description', 'recommended_human_eval_check',
    'status_label'
]

with open(OUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(review_rows)

print(f"Linguistic review queue written to {OUT_FILE} with {len(review_rows)} priority cases.")
