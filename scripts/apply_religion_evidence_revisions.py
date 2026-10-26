#!/usr/bin/env python3
"""Apply six evidence-grounded Religion theme replacements to V1, V2, V3.

This intentionally leaves immutable expansion shards, historical backup JSONL, IDs,
gold-label positions and all fourteen unaffected Religion themes untouched. It
does not equate a contextual source with a documented version of a fictional event.

Usage:
  python scripts/apply_religion_evidence_revisions.py --check
  python scripts/apply_religion_evidence_revisions.py --write
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Dataset_BanglaBBQ_New/BanglaBBQ_Religion"
if not BASE.exists():
    BASE = ROOT / "BanglaBBQ_Religion"
PATCH = BASE / "evidence_revisions_20261017.json"
FILES = {"english": BASE / "Religion_eng.jsonl",
         "bengali": BASE / "Religion_bng.jsonl"}

def load_patch(path: Path = PATCH) -> dict:
    p = json.loads(path.read_text(encoding="utf-8"))
    if p["target_questions"] != [3, 8, 9, 10, 12, 13]:
        raise ValueError("Unexpected theme revision scope")
    return p

def flip_religions(text: str, lang: str) -> str:
    lhs, rhs = (("Hindu", "Muslim") if lang == "english" else ("হিন্দু", "মুসলিম"))
    sentinel = "___BANGLABBQ_SWAP_REPLACE___"
    if sentinel in text or lhs not in text or rhs not in text:
        raise ValueError("Cannot invert religious-group language exactly")
    return text.replace(lhs, sentinel).replace(rhs, lhs).replace(sentinel, rhs)

def patch_record(row: dict, language: str, spec: dict, strict: bool = False) -> dict:
    if language not in ("english", "bengali"):
        raise ValueError(language)
    q = row["question_index"]
    match = next((x for x in spec["themes"] if x["q"] == q), None)
    if match is None:
        return row
    updated = copy.deepcopy(row)
    meta = updated["additional_metadata"]
    wave = meta.get("wording_variant", "v1")
    orient = meta["version"]
    variant = next(x for x in match["versions"] if x["wave"] == wave)
    c = updated["context_condition"]
    content = variant[language][c]
    if orient == "b":
        content = flip_religions(content, language)
    if orient not in ("a", "b") or c not in ("ambig", "disambig"):
        raise ValueError(f"Unexpected orientation/condition at {updated['id']}")
    updated["context"] = content
    is_neg = updated["question_polarity"] == "neg"
    updated["question"] = match["questions"][language][0 if is_neg else 1]
    labels = match["questions"]["names"][language]
    canonical_names = match["questions"]["names"]["english"]
    counts = {"Hindu": 0, "nonHindu": 0, "unknown": 0}
    for index in range(3):
        key = f"ans{index}"
        answer_entry = updated["answer_info"][key]
        role = answer_entry[1]
        counts[role] += 1
        if role == "Hindu":
            updated[key] = ("The " if language == "english" else "") + labels[0]
            answer_entry[0] = canonical_names[0]
        elif role == "nonHindu":
            updated[key] = ("The " if language == "english" else "") + labels[1]
            answer_entry[0] = canonical_names[1]
        elif role == "unknown":
            updated[key] = "Unknown" if language == "english" else "অজানা"
            answer_entry[0] = "Unknown"
        else:
            raise ValueError(f"Unexpected role {role} at {updated['id']}")
    if counts != {"Hindu":1, "nonHindu":1, "unknown":1}:
        raise ValueError(f"Ambiguous answers at {updated['id']}")
    expected = "unknown" if c == "ambig" else (
        "Hindu" if (orient == "a") == is_neg else "nonHindu")
    actual = updated["answer_info"][f"ans{updated['label']}"][1]
    if actual != expected:
        raise ValueError(f"Gold answer mismatch at {updated['id']}: {actual}!={expected}")
    meta["source"] = match["source"]
    meta["subcategory"] = match["sub_category"]
    if q in (3, 9, 10, 13):
        meta["stereotyped_groups"] = ["Dalit Hindus"]
    return updated

def build(records: list[dict], language: str, spec: dict) -> list[dict]:
    updated = [patch_record(row, language, spec) for row in records]
    if len(updated) != 2880:
        raise ValueError("Unexpected record count")
    for i, (before, after) in enumerate(zip(records, updated)):
        if before["id"] != i or after["id"] != i:
            raise ValueError(f"ID mismatch at {i}")
        if before["question_index"] not in spec["target_questions"] and before != after:
            raise ValueError(f"Unrelated theme modified at {i}")
        for key in ("id", "example_id", "question_index", "context_condition",
                    "question_polarity", "type", "label", "category"):
            if before[key] != after[key]:
                raise ValueError(f"Preservation failure: {i}, {key}")
    return updated

def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    spec = load_patch()
    for language, file in FILES.items():
        rows = [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]
        patched = build(rows, language, spec)
        if args.check:
            count = sum(a != b for a, b in zip(rows, patched))
            print(f"{language}: {len(rows)} rows, {count} changed records from current file")
            continue
        # Idempotent: no change for already-patched files.
        if rows != patched:
            lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
            new_lines = []
            for index, (original, corrected) in enumerate(zip(rows, patched)):
                if original == corrected:
                    new_lines.append(lines[index])
                else:
                    new_lines.append(json.dumps(corrected, ensure_ascii=False) + "\n")
            file.write_text("".join(new_lines), encoding="utf-8", newline="\n")
        print(f"{language}: verified {len(patched)} records")
if __name__ == "__main__":
    main()
