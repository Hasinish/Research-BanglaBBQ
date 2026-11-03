import json
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

categories = [
    ("EducationalBackground", "Education", 2880),
    ("Ethnicity", "Ethnicity", 1440),
    ("HealthStatus", "HealthStatus", 2880),
    ("MaritalStatus", "MaritalStatus", 2880),
    ("OccupationalBackground", "OccupationalBackground", 2880),
    ("Politics", "Politics", 2880),
    ("Regional", "Regional", 1440),
    ("Religion", "Religion", 2880),
    ("SocialStatus", "SocialStatus", 1440)
]

cand_dir = "qa_corrected_output/candidates"

def file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

audit_results = []

print("==========================================================================================================")
print("                                 EXHAUSTIVE 18-FILE CANDIDATE QA AUDIT")
print("==========================================================================================================")

for cat_dir, cat_name, expected_rows in categories:
    eng_file = os.path.join(cand_dir, f"BanglaBBQ_ENG_{cat_name}.jsonl")
    ben_file = os.path.join(cand_dir, f"BanglaBBQ_BEN_{cat_name}.jsonl")
    
    with open(eng_file, 'r', encoding='utf-8') as fe:
        erows = [json.loads(line) for line in fe]
    with open(ben_file, 'r', encoding='utf-8') as fb:
        brows = [json.loads(line) for line in fb]
        
    e_sha = file_sha256(eng_file)
    b_sha = file_sha256(ben_file)
    
    # 1. Row counts
    e_len = len(erows)
    b_len = len(brows)
    row_pass = (e_len == expected_rows and b_len == expected_rows)
    
    # 2. Sequential IDs
    seq_pass = all(erows[i]['example_id'] == i and brows[i]['example_id'] == i for i in range(expected_rows))
    
    # 3. Schema keys
    expected_keys = set(erows[0].keys())
    schema_pass = all(set(r.keys()) == expected_keys for r in erows + brows) and len(expected_keys) == 15
    
    # 4. Label counts and alignment
    e_labels = {0: 0, 1: 0, 2: 0}
    b_labels = {0: 0, 1: 0, 2: 0}
    label_mismatches = 0
    for i in range(expected_rows):
        el = erows[i]['label']
        bl = brows[i]['label']
        e_labels[el] = e_labels.get(el, 0) + 1
        b_labels[bl] = b_labels.get(bl, 0) + 1
        if el != bl:
            label_mismatches += 1
            
    expected_per_label = expected_rows // 3
    lbl_pass = (e_labels[0] == expected_per_label and e_labels[1] == expected_per_label and e_labels[2] == expected_per_label and label_mismatches == 0)
    
    # 5. Ambiguous Unknown
    amb_unk_pass = True
    for i in range(expected_rows):
        if erows[i]['context_condition'] == 'ambig':
            if erows[i]['answer_info'][f"ans{erows[i]['label']}"][1] != 'unknown':
                amb_unk_pass = False
            if brows[i]['answer_info'][f"ans{brows[i]['label']}"][1] != 'unknown':
                amb_unk_pass = False
                
    # 6. Position balance in ENG & BEN
    def calc_pos(rows, lang):
        neg_f, neg_s = 0, 0
        nonneg_f, nonneg_s = 0, 0
        for r in rows:
            if r['context_condition'] == 'disambig':
                ctx = r['context']
                ans_ents = [r[f'ans{i}'] for i in range(3) if r['answer_info'][f'ans{i}'][1] != 'unknown']
                e0, e1 = ans_ents[0], ans_ents[1]
                
                # Clean prefix for search
                e0_s = e0.replace('The ', '').replace('the ', '').split()[0]
                e1_s = e1.replace('The ', '').replace('the ', '').split()[0]
                p0 = ctx.find(e0_s)
                p1 = ctx.find(e1_s)
                first_ent = e0 if p0 < p1 else e1
                second_ent = e1 if p0 < p1 else e0
                gold = r[f"ans{r['label']}"]
                
                if r['question_polarity'] == 'neg':
                    if gold == first_ent: neg_f += 1
                    else: neg_s += 1
                else:
                    if gold == first_ent: nonneg_f += 1
                    else: nonneg_s += 1
        return neg_f, neg_s, nonneg_f, nonneg_s

    enf, ens, non_enf, non_ens = calc_pos(erows, "ENG")
    bnf, bns, non_bnf, non_bns = calc_pos(brows, "BEN")
    
    # Permutations check: 6 permutations per 24-row block
    num_blocks = expected_rows // 24
    perms_pass = True
    for b in range(num_blocks):
        block_rows = erows[b*24:(b+1)*24]
        seen_perms = set()
        for i in range(0, 24, 4):
            # ans0, ans1, ans2 arrangement
            r = block_rows[i]
            perm = (r['ans0'], r['ans1'], r['ans2'])
            seen_perms.add(perm)
        if len(seen_perms) != 6:
            perms_pass = False
            
    cat_summary = {
        "category": cat_dir,
        "expected_rows": expected_rows,
        "eng_rows": e_len,
        "ben_rows": b_len,
        "row_pass": row_pass,
        "schema_pass": schema_pass,
        "seq_pass": seq_pass,
        "lbl_pass": lbl_pass,
        "labels": e_labels,
        "label_mismatches": label_mismatches,
        "amb_unk_pass": amb_unk_pass,
        "perms_pass": perms_pass,
        "eng_pos_neg": f"{enf}/{ens}",
        "eng_pos_nonneg": f"{non_enf}/{non_ens}",
        "ben_pos_neg": f"{bnf}/{bns}",
        "ben_pos_nonneg": f"{non_bnf}/{non_bns}",
        "eng_sha256": e_sha,
        "ben_sha256": b_sha,
        "status": "PASS" if (row_pass and schema_pass and seq_pass and lbl_pass and amb_unk_pass and perms_pass) else "FAIL"
    }
    audit_results.append(cat_summary)
    
    print(f"[{cat_summary['status']}] {cat_dir:<25} | Rows: {e_len} | Labels: {e_labels[0]}/{e_labels[1]}/{e_labels[2]} | Mismatches: {label_mismatches} | Perms: {perms_pass}")
    print(f"       ENG Neg Pos: {enf}/{ens} ({enf/(enf+ens)*100:.1f}%) | BEN Neg Pos: {bnf}/{bns} ({bnf/(bnf+bns)*100:.1f}%)")

print("\nAll 9 categories audited.")

with open("qa_corrected_output/audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2, ensure_ascii=False)
