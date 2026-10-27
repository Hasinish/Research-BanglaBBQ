import os
import sys
import json
from collections import Counter, defaultdict
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = Path(__file__).resolve().parents[3]
CAND_DIR = REPO_ROOT / "local_candidates" / "non_mental_health_repair_20261028" / "candidates"

CANDIDATE_CATEGORIES = [
    {
        "name": "Ethnicity",
        "eng_file": CAND_DIR / "BanglaBBQ_Ethnicity_repaired_english.jsonl",
        "ben_file": CAND_DIR / "BanglaBBQ_Ethnicity_repaired_bengali.jsonl",
    },
    {
        "name": "Health Status",
        "eng_file": CAND_DIR / "BanglaBBQ_Health_Status_repaired_english.jsonl",
        "ben_file": CAND_DIR / "BanglaBBQ_Health_Status_repaired_bengali.jsonl",
    },
    {
        "name": "Regional Affiliation",
        "eng_file": CAND_DIR / "BanglaBBQ_Regional_repaired_english.jsonl",
        "ben_file": CAND_DIR / "BanglaBBQ_Regional_repaired_bengali.jsonl",
    },
    {
        "name": "Social Status",
        "eng_file": CAND_DIR / "BanglaBBQ_SocialStatus_repaired_english.jsonl",
        "ben_file": CAND_DIR / "BanglaBBQ_SocialStatus_repaired_bengali.jsonl",
    }
]

EXPECTED_SCHEMA_KEYS = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id"
]

UNKNOWN_TERMS_ENG = {"cannot be determined", "unknown", "undetermined"}
UNKNOWN_TERMS_BEN = {"অজানা", "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না"}

def validate_candidate_category(cat):
    name = cat["name"]
    eng_p = cat["eng_file"]
    ben_p = cat["ben_file"]

    assert eng_p.exists(), f"Missing English candidate: {eng_p}"
    assert ben_p.exists(), f"Missing Bengali candidate: {ben_p}"

    with open(eng_p, "r", encoding="utf-8") as fe, open(ben_p, "r", encoding="utf-8") as fb:
        recs_en = [json.loads(l) for l in fe]
        recs_bn = [json.loads(l) for l in fb]

    # Gate 1: Row count
    assert len(recs_en) == 1440, f"[{name}] English row count {len(recs_en)} != 1440"
    assert len(recs_bn) == 1440, f"[{name}] Bengali row count {len(recs_bn)} != 1440"

    # Gate 2: Schema integrity
    for i, (r_en, r_bn) in enumerate(zip(recs_en, recs_bn)):
        assert set(r_en.keys()) == set(EXPECTED_SCHEMA_KEYS) and len(r_en.keys()) == 15, f"[{name}] EN schema invalid at row {i}"
        assert set(r_bn.keys()) == set(EXPECTED_SCHEMA_KEYS) and len(r_bn.keys()) == 15, f"[{name}] BN schema invalid at row {i}"

        # Gate 3: Example IDs sequential
        assert r_en["example_id"] == i, f"[{name}] EN example_id {r_en['example_id']} != {i}"
        assert r_bn["example_id"] == i, f"[{name}] BN example_id {r_bn['example_id']} != {i}"

        # Gate 4: Label valid 0, 1, 2
        assert r_en["label"] in [0, 1, 2], f"[{name}] EN label {r_en['label']} not in [0, 1, 2]"
        assert r_bn["label"] in [0, 1, 2], f"[{name}] BN label {r_bn['label']} not in [0, 1, 2]"

        # Gate 5: Cross-lingual parity
        assert r_en["context_condition"] == r_bn["context_condition"], f"[{name}] Condition mismatch at row {i}"
        assert r_en["question_polarity"] == r_bn["question_polarity"], f"[{name}] Polarity mismatch at row {i}"
        assert r_en["label"] == r_bn["label"], f"[{name}] Label mismatch at row {i}"

        # Gate 6: Ambiguous unknown resolution
        if r_en["context_condition"] == "ambig":
            gold_en = [r_en["ans0"], r_en["ans1"], r_en["ans2"]][r_en["label"]].lower().strip()
            gold_bn = [r_bn["ans0"], r_bn["ans1"], r_bn["ans2"]][r_bn["label"]].strip()
            assert any(u in gold_en for u in UNKNOWN_TERMS_ENG), f"[{name}] EN ambig gold not unknown at row {i}: {gold_en}"
            assert any(u in gold_bn for u in UNKNOWN_TERMS_BEN), f"[{name}] BN ambig gold not unknown at row {i}: {gold_bn}"

    # Gate 7: Label distribution (exactly 480 each of 0, 1, 2 across 1,440 rows)
    counts_en = Counter(r["label"] for r in recs_en)
    counts_bn = Counter(r["label"] for r in recs_bn)
    assert counts_en[0] == 480 and counts_en[1] == 480 and counts_en[2] == 480, f"[{name}] EN label distribution not 480/480/480: {counts_en}"
    assert counts_bn[0] == 480 and counts_bn[1] == 480 and counts_bn[2] == 480, f"[{name}] BN label distribution not 480/480/480: {counts_bn}"

    # Gate 8: Condition distribution (360 each of ambig-neg, disambig-neg, ambig-nonneg, disambig-nonneg)
    cond_counts_en = Counter((r["context_condition"], r["question_polarity"]) for r in recs_en)
    for c_tuple in [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]:
        assert cond_counts_en[c_tuple] == 360, f"[{name}] Condition count for {c_tuple} != 360 ({cond_counts_en[c_tuple]})"

    # Gate 9: 6-way answer permutations across all 60 blocks of 24 rows
    for block_idx in range(60):
        block_recs = recs_en[block_idx * 24 : (block_idx + 1) * 24]
        # Group by (condition, polarity)
        for cond, pol in [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]:
            sub = [r for r in block_recs if r["context_condition"] == cond and r["question_polarity"] == pol]
            assert len(sub) == 6, f"[{name}] Block {block_idx} ({cond}, {pol}) has {len(sub)} rows != 6"
            # Verify 6 distinct answer tuples
            ans_tuples = set((r["ans0"], r["ans1"], r["ans2"]) for r in sub)
            assert len(ans_tuples) == 6, f"[{name}] Block {block_idx} ({cond}, {pol}) missing permutations: {len(ans_tuples)} unique != 6"

    print(f"[{name}] ALL 9 INVARIANT GATES PASSED (100% COMPLIANT).")

def main():
    print("=== VALIDATING REPAIRED CANDIDATES INVARIANT SUITE ===")
    for cat in CANDIDATE_CATEGORIES:
        validate_candidate_category(cat)
    print("\nALL 4 CANDIDATE CATEGORIES FULLY CERTIFIED AGAINST INVARIANT GATES!")

if __name__ == "__main__":
    main()
