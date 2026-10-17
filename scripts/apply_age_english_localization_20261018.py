#!/usr/bin/env python3
"""Reproduce and validate the English Age working benchmark (2026-10-18).

The original PakBBQ Age file is immutable. Run with --write only to regenerate
BanglaBBQ_ENG_New/Age.jsonl, or with no arguments to validate the committed file.
Structural passing is NOT linguistic or source certification.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PakBBQ_Repo/PakBBQ/PakBBQ_ENG/Age.jsonl"
ENGLISH = ROOT / "BanglaBBQ_ENG_New/Age.jsonl"
BENGALI = ROOT / "BanglaBBQ_BEN_New/Age.jsonl"
FIELDS = (
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id",
)
META = (
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "answer_info", "additional_metadata", "category", "id", "label",
)
EXPECTED_CHANGES = {
    "9": 144, "10": 168, "13": 32, "14": 32, "15": 128,
    "16": 12, "18": 72, "20": 280,
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def corrected_context(row: dict) -> str:
    value = row["context"]
    question = row["question_index"]
    if question == "9":
        value = value.replace("whole processing", "whole process")
    elif question == "10":
        value = value.replace("They followed that was examples", "They followed that with examples")
    elif question == "13":
        value = value.replace("outside the Imtiaz", "outside a Shwapno supermarket")
        value = value.replace("on Indrive", "through Pathao")
        value = value.replace("listening the advice", "listening to the advice")
    elif question == "14":
        value = value.replace("near Jalal Sons", "near Tasty Treat")
    elif question == "15":
        value = value.replace("at a Chai Dhaba", "at a tea stall")
    elif question == "16":
        value = value.replace("a 18-year-old", "an 18-year-old")
    elif question == "18":
        for old in (
            "A family recently moved out of their long-time home in Lahore into a newly renovated apartment in Karachi.",
            "A family recently moved out of their long-time home in Lahore a newly renovated apartment in Karachi.",
        ):
            value = value.replace(
                old,
                "A family recently moved from their longtime home in Chattogram to a newly renovated apartment in Dhaka.",
            )
    elif question == "20":
        for old, new in (
            ("near the chowk", "at the crossroads"),
            ("going going", "going"),
            ("zone zone", "zone"),
            ("a 18 year old", "an 18-year-old"),
            ("when he came to a full stop", "when the younger driver came to a full stop"),
        ):
            value = value.replace(old, new)
    return value


def build(source: list[dict]) -> tuple[list[dict], Counter]:
    rows = []
    changes = Counter()
    for old in source:
        context = corrected_context(old)
        if context != old["context"]:
            changes[old["question_index"]] += 1
        rows.append({key: context if key == "context" else old[key] for key in FIELDS})
    assert dict(changes) == EXPECTED_CHANGES, f"Unexpected changes per theme: {dict(changes)}"
    return rows, changes


def validate(english: list[dict], bengali: list[dict]) -> None:
    assert len(english) == len(bengali) == 2920
    assert set(english[0]) == set(bengali[0]) == set(FIELDS)
    for i, (en, bn) in enumerate(zip(english, bengali)):
        assert en["example_id"] == bn["example_id"] == i
        assert set(en) == set(bn) == set(FIELDS)
        for key in META:
            assert en[key] == bn[key], (i, key)
        assert en["category"] == "Age"
        assert en["label"] in (0, 1, 2)
        assert len({en["ans0"], en["ans1"], en["ans2"]}) == 3
        if en["context_condition"] == "ambig":
            correct = en["answer_info"]["ans" + str(en["label"])][1]
            assert correct == "unknown", i
        else:
            assert en["context_condition"] == "disambig", i
    counts = Counter(row["context_condition"] for row in english)
    assert counts == {"ambig": 1460, "disambig": 1460}, counts
    polarities = Counter(row["question_polarity"] for row in english)
    assert polarities == {"neg": 1460, "nonneg": 1460}, polarities
    assert len({row["question_index"] for row in english}) == 20
    assert all(
        not any(token in row["context"] for token in (
            "Imtiaz", "Indrive", "Jalal Sons", "Chai Dhaba",
            "Lahore", "Karachi", "chowk", "going going", "zone zone",
        )) for row in english
    )
    underage = [
        row for row in english
        if row["question_index"] == "20"
        and (
            "15 year old" in row["context"]
            or "17-year-old" in row["context"]
        )
    ]
    assert len(underage) == 112, len(underage)
    print(
        "Age structural validation PASS: 2920 English + 2920 Bengali rows, "
        "868 approved English context repairs, bilingual metadata parity."
    )
    print(
        "RESEARCH BLOCKER: Q20 retains 112 rows with under-18 drivers. "
        "Neither native-language semantic QA nor scenario-source verification is certified."
    )


def main() -> None:
    original = read_jsonl(SOURCE)
    expected, changes = build(original)
    if "--write" in sys.argv:
        ENGLISH.parent.mkdir(parents=True, exist_ok=True)
        ENGLISH.write_text(
            "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                    for row in expected),
            encoding="utf-8",
        )
    actual = read_jsonl(ENGLISH)
    assert actual == expected, "GitHub English export differs from reproducible corrections"
    validate(actual, read_jsonl(BENGALI))
    print("English context modifications by theme:", dict(changes))


if __name__ == "__main__":
    main()
