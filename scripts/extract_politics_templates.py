import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    eng_rows = [json.loads(line) for line in f if line.strip()]

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_bengali.jsonl", "r", encoding="utf-8") as f:
    ben_rows = [json.loads(line) for line in f if line.strip()]

for qi in ["1", "2", "3", "4", "5"]:
    e_q = [r for r in eng_rows if r["question_index"] == qi]
    b_q = [r for r in ben_rows if r["question_index"] == qi]
    
    # Ambig row and disambig row
    e_ambig = next(r for r in e_q if r["context_condition"] == "ambig")
    e_disambig = next(r for r in e_q if r["context_condition"] == "disambig")
    b_ambig = next(r for r in b_q if r["context_condition"] == "ambig")
    b_disambig = next(r for r in b_q if r["context_condition"] == "disambig")
    
    # Neg and nonneg questions
    e_neg = next(r for r in e_q if r["question_polarity"] == "neg")["question"]
    e_nonneg = next(r for r in e_q if r["question_polarity"] == "nonneg")["question"]
    b_neg = next(r for r in b_q if r["question_polarity"] == "neg")["question"]
    b_nonneg = next(r for r in b_q if r["question_polarity"] == "nonneg")["question"]
    
    print(f"=== TEMPLATE {qi} ({len(e_q)} rows) ===")
    print("Source:", e_ambig["additional_metadata"].get("source"))
    print("Stereotyped group:", e_ambig["additional_metadata"].get("stereotyped_groups"))
    print("\n[ENGLISH]")
    print("  Ambig Context:", e_ambig["context"])
    print("  Disambig Context:", e_disambig["context"])
    print("  Negative Q:", e_neg)
    print("  Non-negative Q:", e_nonneg)
    print("  Target vs Non-target:", e_ambig["ans0"], "vs", e_ambig["ans1"])
    print("\n[BENGALI]")
    print("  Ambig Context:", b_ambig["context"])
    print("  Disambig Context:", b_disambig["context"])
    print("  Negative Q:", b_neg)
    print("  Non-negative Q:", b_nonneg)
    print("  Target vs Non-target:", b_ambig["ans0"], "vs", b_ambig["ans1"])
    print("=" * 80)
