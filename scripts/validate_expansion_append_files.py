#!/usr/bin/env python3
"""Independent, rigorous validator for the six BanglaBBQ Q11-Q20 expansion candidate files.

Validates Health Status, Marital Status, and Occupational Background candidate append files
against all benchmark structural, semantic, and bilingual parity invariants, plus deliberate
adversarial corruption tests.
"""
import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_FIELDS = (
    "example_id",
    "question_index",
    "question_polarity",
    "context_condition",
    "category",
    "answer_info",
    "additional_metadata",
    "context",
    "question",
    "ans0",
    "ans1",
    "ans2",
    "label",
    "type",
    "id",
)

CONDITIONS = (("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg"))

EXPANSION_CONFIGS = {
    "Health Status": {
        "category": "Health_status",
        "id_base": 8300000,
        "en_path": ROOT / "candidate_bundles/health_mental_q11_q20_review_20261028/BanglaBBQ_Health_Mental_Q11_Q20_english.jsonl",
        "bn_path": ROOT / "candidate_bundles/health_mental_q11_q20_review_20261028/BanglaBBQ_Health_Mental_Q11_Q20_bengali.jsonl",
    },
    "Marital Status": {
        "category": "Marital_status",
        "id_base": 8700000,
        "en_path": ROOT / "review_artifacts/marital_male_q11_q20/BanglaBBQ_Marital_Male_Q11_Q20_english.jsonl",
        "bn_path": ROOT / "review_artifacts/marital_male_q11_q20/BanglaBBQ_Marital_Male_Q11_Q20_bengali.jsonl",
    },
    "Occupational Background": {
        "category": "Occupational_background",
        "id_base": 8600000,
        "en_path": ROOT / "review_submissions/occupational_professional_q11_q20_2026-10-28/BanglaBBQ_Occupational_Professional_Q11_Q20_english.jsonl",
        "bn_path": ROOT / "review_submissions/occupational_professional_q11_q20_2026-10-28/BanglaBBQ_Occupational_Professional_Q11_Q20_bengali.jsonl",
    },
}


class ValidationError(Exception):
    pass


def demand(predicate: bool, msg: str):
    if not predicate:
        raise ValidationError(msg)


def load_jsonl(path: Path):
    demand(path.exists(), f"File does not exist: {path}")
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                raise ValidationError(f"{path.name}:{i} invalid JSON: {e}")
    return rows


def validate_file_structure(rows, category_name, lang, config):
    demand(len(rows) == 1440, f"{category_name} {lang}: expected exactly 1440 rows, got {len(rows)}")

    label_counts = Counter()
    condition_counts = Counter()
    theme_counts = Counter()
    seen_tuples = set()
    neg_intro_pos = Counter()
    nonneg_intro_pos = Counter()
    neg_target_comp = Counter()

    for idx, row in enumerate(rows):
        expected_eid = 1440 + idx
        expected_id = config["id_base"] + expected_eid

        # 1. Exact 15 fields and field order
        demand(tuple(row.keys()) == CANONICAL_FIELDS, f"{category_name} {lang} row {idx}: field keys/order mismatch")

        # 2. Field types and formulas
        demand(isinstance(row["example_id"], int) and row["example_id"] == expected_eid, f"Bad example_id {row.get('example_id')}")
        demand(isinstance(row["id"], int) and row["id"] == expected_id, f"Bad id {row.get('id')}")
        demand(row["category"] == config["category"], f"Bad category {row.get('category')}")
        demand(row["type"] == "NA", f"Bad type {row.get('type')}")
        if category_name == "Health Status":
            demand(isinstance(row["question_index"], int) and row["question_index"] in range(11, 21), f"Bad question_index {row.get('question_index')}")
        else:
            demand(isinstance(row["question_index"], str) and row["question_index"] in [str(q) for q in range(11, 21)], f"Bad question_index {row.get('question_index')}")
        demand(row["context_condition"] in ("ambig", "disambig"), f"Bad condition {row.get('context_condition')}")
        demand(row["question_polarity"] in ("neg", "nonneg"), f"Bad polarity {row.get('question_polarity')}")
        demand(row["label"] in (0, 1, 2), f"Bad label {row.get('label')}")

        # 3. Text fields
        demand(isinstance(row["context"], str) and len(row["context"]) > 20, "Malformed context")
        demand(isinstance(row["question"], str) and len(row["question"]) > 5, "Malformed question")

        # 4. Answer info & options
        ans_info = row["answer_info"]
        demand(isinstance(ans_info, dict) and set(ans_info.keys()) == {"ans0", "ans1", "ans2"}, "Malformed answer_info")
        unknown_count = 0
        for opt_key in ("ans0", "ans1", "ans2"):
            opt_text = row[opt_key]
            demand(isinstance(opt_text, str) and len(opt_text) > 0, f"Empty option {opt_key}")
            demand(isinstance(ans_info[opt_key], list) and len(ans_info[opt_key]) == 2, f"Malformed answer_info[{opt_key}]")
            demand(ans_info[opt_key][0] == opt_text, f"Text mismatch in answer_info[{opt_key}]: {ans_info[opt_key][0]} != {opt_text}")
            tag = ans_info[opt_key][1]
            demand(isinstance(tag, str) and len(tag) > 0, f"Empty or invalid semantic tag in {opt_key}")
            if tag == "unknown":
                unknown_count += 1
                if lang == "English":
                    demand("unknown" in opt_text.lower(), f"English unknown option text mismatch: {opt_text}")
                else:
                    demand("অজানা" in opt_text, f"Bengali unknown option text mismatch: {opt_text}")
        demand(unknown_count == 1, f"Expected exactly 1 unknown option, got {unknown_count}")

        # 5. Metadata
        meta = row["additional_metadata"]
        demand(isinstance(meta, dict) and "version" in meta and "source" in meta, "Malformed additional_metadata")
        demand(meta["version"] in ("a", "b"), f"Bad version {meta.get('version')}")

        # 6. Duplicate detection
        tup = (row["context"], row["question"], row["ans0"], row["ans1"], row["ans2"])
        demand(tup not in seen_tuples, f"{category_name} {lang}: duplicate tuple at eid {expected_eid}")
        seen_tuples.add(tup)

        # 7. Ambiguous Unknown label
        if row["context_condition"] == "ambig":
            gold_tag = ans_info[f"ans{row['label']}"][1]
            demand(gold_tag == "unknown", f"{category_name} {lang} eid {expected_eid}: ambig gold label must be unknown, got {gold_tag}")
        else:
            gold_tag = ans_info[f"ans{row['label']}"][1]
            demand(gold_tag != "unknown", f"{category_name} {lang} eid {expected_eid}: disambig gold label must NOT be unknown")

            # Extract first/second mentioned person from context to verify position
            # Get non-unknown options
            non_unk_names = [ans_info[f"ans{k}"][0].split(",")[0].strip() for k in (0, 1, 2) if ans_info[f"ans{k}"][1] != "unknown"]
            if len(non_unk_names) == 2:
                # Find which one appears first in context
                pos0 = row["context"].find(non_unk_names[0])
                pos1 = row["context"].find(non_unk_names[1])
                if pos0 != -1 and pos1 != -1:
                    first_person = non_unk_names[0] if pos0 < pos1 else non_unk_names[1]
                    gold_person = ans_info[f"ans{row['label']}"][0].split(",")[0].strip()
                    intro_order = "First" if gold_person == first_person else "Second"
                    if row["question_polarity"] == "neg":
                        neg_intro_pos[intro_order] += 1
                        role = "target" if gold_tag == "target" else "comparison"
                        neg_target_comp[role] += 1
                    else:
                        nonneg_intro_pos[intro_order] += 1

        label_counts[row["label"]] += 1
        condition_counts[(row["context_condition"], row["question_polarity"])] += 1
        theme_counts[int(row["question_index"])] += 1

    # Invariants
    demand(label_counts == Counter({0: 480, 1: 480, 2: 480}), f"{category_name} {lang}: label imbalance: {label_counts}")
    demand(condition_counts == Counter({c: 360 for c in CONDITIONS}), f"{category_name} {lang}: condition imbalance: {condition_counts}")
    demand(all(theme_counts[q] == 144 for q in range(11, 21)), f"{category_name} {lang}: theme imbalance: {theme_counts}")

    # Check 4-condition packet ordering
    for i in range(0, 1440, 4):
        packet_conds = [(r["context_condition"], r["question_polarity"]) for r in rows[i:i+4]]
        demand(packet_conds == list(CONDITIONS), f"{category_name} {lang}: packet {i//4} condition ordering broken: {packet_conds}")

    # Check 6-way permutation closure per 24-row orientation
    for block_idx in range(0, 1440, 24):
        perms = set()
        for p_idx in range(6):
            r = rows[block_idx + p_idx * 4]
            perm = tuple(r["answer_info"][f"ans{k}"][1] for k in (0, 1, 2))
            perms.add(perm)
        demand(len(perms) == 6, f"{category_name} {lang}: 24-row block {block_idx//24} has {len(perms)} permutations, expected 6")

    # Positional & demographic balance
    if neg_intro_pos:
        demand(neg_intro_pos == Counter({"First": 180, "Second": 180}), f"{category_name} {lang}: neg intro pos broken: {neg_intro_pos}")
    if nonneg_intro_pos:
        demand(nonneg_intro_pos == Counter({"First": 180, "Second": 180}), f"{category_name} {lang}: nonneg intro pos broken: {nonneg_intro_pos}")

    return {
        "rows": len(rows),
        "label_counts": dict(label_counts),
        "condition_counts": {f"{c[0]}_{c[1]}": v for c, v in condition_counts.items()},
        "theme_counts": len(theme_counts),
        "neg_intro_positions": dict(neg_intro_pos) if neg_intro_pos else "N/A",
        "nonneg_intro_positions": dict(nonneg_intro_pos) if nonneg_intro_pos else "N/A",
    }


def validate_bilingual_parity(en_rows, bn_rows, category_name):
    demand(len(en_rows) == len(bn_rows), f"{category_name}: row count mismatch: EN {len(en_rows)} != BN {len(bn_rows)}")
    for i, (e, b) in enumerate(zip(en_rows, bn_rows)):
        eid = e["example_id"]
        for field in ("example_id", "question_index", "question_polarity", "context_condition", "category", "label", "type", "id"):
            demand(e[field] == b[field], f"{category_name} bilingual mismatch at {eid} for field {field}: {e[field]} != {b[field]}")
        demand(e["additional_metadata"] == b["additional_metadata"], f"{category_name} metadata mismatch at {eid}")
        for k in ("ans0", "ans1", "ans2"):
            demand(e["answer_info"][k][1] == b["answer_info"][k][1], f"{category_name} option tag mismatch at {eid} for {k}")


def run_negative_fixture_tests(en_rows, bn_rows, category_name, config):
    """Run deliberate negative corrupted fixtures to verify the validator catches every defect."""
    fixtures = [
        ("wrong_example_id", lambda e, b: (e[0].__setitem__("example_id", 9999), b), "Bad example_id"),
        ("wrong_global_id", lambda e, b: (e[0].__setitem__("id", 1234567), b), "Bad id"),
        ("swapped_gold_label", lambda e, b: (e[1].__setitem__("label", (e[1]["label"] + 1) % 3), b), "label"),
        ("broken_condition_packet", lambda e, b: (e[0].__setitem__("context_condition", "disambig"), b), "packet"),
        ("ambig_label_not_unknown", lambda e, b: (e[0].__setitem__("label", 0), b), "ambig gold label must be unknown"),
        ("bilingual_label_mismatch", lambda e, b: (e, b[0].__setitem__("label", (b[0]["label"] + 1) % 3)), "bilingual mismatch"),
        ("missing_field", lambda e, b: (e[0].pop("context"), b), "field keys/order mismatch"),
        ("omitted_record", lambda e, b: (e.pop(), b.pop()), "expected exactly 1440 rows"),
        ("duplicate_scenario", lambda e, b: (e.__setitem__(1, copy.deepcopy(e[0])), b), "duplicate tuple"),
    ]

    caught = 0
    for name, mutator, needle in fixtures:
        e_copy = copy.deepcopy(en_rows)
        b_copy = copy.deepcopy(bn_rows)
        mutator(e_copy, b_copy)
        try:
            validate_file_structure(e_copy, category_name, "English", config)
            validate_file_structure(b_copy, category_name, "Bengali", config)
            validate_bilingual_parity(e_copy, b_copy, category_name)
            raise AssertionError(f"Negative fixture '{name}' was unexpectedly NOT caught!")
        except (ValidationError, AssertionError) as err:
            if "unexpectedly NOT caught" in str(err):
                raise
            caught += 1

    return {"fixtures_tested": len(fixtures), "fixtures_caught": caught}


def main():
    print("=" * 70)
    print("BanglaBBQ Final Three-Category Expansion Candidate Validation")
    print("=" * 70)

    summary = {}
    all_passed = True

    for cat_name, cfg in EXPANSION_CONFIGS.items():
        print(f"\n[+] Validating category: {cat_name}")
        en_rows = load_jsonl(cfg["en_path"])
        bn_rows = load_jsonl(cfg["bn_path"])

        en_res = validate_file_structure(en_rows, cat_name, "English", cfg)
        print(f"    - English 1,440 rows: PASS (labels: {en_res['label_counts']}, intro: {en_res['neg_intro_positions']})")

        bn_res = validate_file_structure(bn_rows, cat_name, "Bengali", cfg)
        print(f"    - Bengali 1,440 rows: PASS (labels: {bn_res['label_counts']}, intro: {bn_res['neg_intro_positions']})")

        validate_bilingual_parity(en_rows, bn_rows, cat_name)
        print("    - Bilingual parity: PASS (1,440 parallel pairs identical in schema, IDs, labels, metadata, tags)")

        neg_res = run_negative_fixture_tests(en_rows, bn_rows, cat_name, cfg)
        print(f"    - Adversarial corrupted fixtures: PASS ({neg_res['fixtures_caught']}/{neg_res['fixtures_tested']} caught)")

        summary[cat_name] = {
            "english": en_res,
            "bengali": bn_res,
            "adversarial_fixtures": neg_res,
            "status": "PASS",
        }

    print("\n" + "=" * 70)
    print("SUMMARY: ALL SIX EXPANSION CANDIDATE FILES PASSED 100% INVARIANTS")
    print("=" * 70)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
