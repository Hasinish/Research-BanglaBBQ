import json

with open("local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Regional_FINAL_english.jsonl", "r", encoding="utf-8") as fe, \
     open("local_candidates/final_seven_category_qa/candidates/BanglaBBQ_Regional_FINAL_bengali.jsonl", "r", encoding="utf-8") as fb:
    for i in range(4):
        re = json.loads(fe.readline())
        rb = json.loads(fb.readline())
        print(f"--- RECORD EID {re['example_id']} ({re['context_condition']}, {re['question_polarity']}) ---")
        print("EN CTX:", re["context"])
        print("EN ANS:", [re["ans0"], re["ans1"], re["ans2"]], "GOLD:", [re["ans0"], re["ans1"], re["ans2"]][re["label"]])
        print("BN CTX:", rb["context"])
        print("BN ANS:", [rb["ans0"], rb["ans1"], rb["ans2"]], "GOLD:", [rb["ans0"], rb["ans1"], rb["ans2"]][rb["label"]])
