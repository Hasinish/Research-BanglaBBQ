import json

with open("Dataset_ BanglaBBQ_Old/Politics/banglabbq_politics_english.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

for qi in ["1", "2", "3", "4", "5"]:
    qrows = [r for r in rows if r["question_index"] == qi]
    print(f"=== Question Index {qi} ({len(qrows)} rows) ===")
    r0 = qrows[0]
    print("Source:", r0["additional_metadata"].get("source"))
    print("Stereotyped:", r0["additional_metadata"].get("stereotyped_groups"))
    
    # Check contexts
    contexts = set(r["context"] for r in qrows)
    print(f"Unique contexts ({len(contexts)}):")
    for c in contexts:
        print("  -", c[:75], "..." if len(c)>75 else "")
        
    # Check questions
    questions = set((r["question_polarity"], r["question"]) for r in qrows)
    print("Questions:")
    for pol, q in questions:
        print(f"  [{pol}] {q}")
        
    # Check answer groups
    print("Answer info sample:", r0["answer_info"])
    print()
