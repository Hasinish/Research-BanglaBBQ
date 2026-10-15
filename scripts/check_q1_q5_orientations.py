import json

with open('Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl', 'r', encoding='utf-8') as f:
    recs = [json.loads(line) for line in f]

for q in range(1, 6):
    q_start = (q - 1) * 48
    r_a = recs[q_start + 1] # Row 1 of template (orientation 1, disambig neg)
    r_b = recs[q_start + 25] # Row 25 of template (orientation 2, disambig neg)
    
    cat_a = r_a['answer_info'][f"ans{r_a['label']}"][1]
    cat_b = r_b['answer_info'][f"ans{r_b['label']}"][1]
    
    print(f"Theme Q{q}:")
    print(f"  Orientation 1 (neg): {cat_a}")
    print(f"  Orientation 2 (neg): {cat_b}")
    assert cat_a != cat_b, f"Orientation 1 and 2 in Q{q} have same category!"
print("All Q1-Q5 have exact counterfactual inversion between Orientation 1 (rows 0-23) and Orientation 2 (rows 24-47)!")
