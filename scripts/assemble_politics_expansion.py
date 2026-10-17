#!/usr/bin/env python3
"""Rebuild Politics v2/v3 canonical bilingual JSONL from immutable source plus shards.

This operation is append-only relative to the 960-record pre-expansion snapshot.
Running it again after a successful build is safe and leaves files unchanged.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "BanglaBBQ_Politics"
PARTS = BASE / "expansion_v2v3_20261017"
MANIFEST = json.loads((PARTS / "manifest.json").read_text(encoding="utf-8"))
HEADERS = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id",
]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def records(raw: bytes) -> list[dict]:
    return [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]


def assert_rows(rows: list[dict], label: str, start_id: int, n: int) -> None:
    assert len(rows) == n, f"{label}: expected {n} records, found {len(rows)}"
    for idx, row in enumerate(rows):
        assert list(row) == HEADERS, f"{label}: bad field schema at {idx}"
        assert row["id"] == row["example_id"] == start_id + idx, f"{label}: bad ID {idx}"
        assert 1 <= row["question_index"] <= 20, f"{label}: invalid theme {idx}"
        assert row["context_condition"] in {"ambig", "disambig"}
        assert row["question_polarity"] in {"neg", "nonneg"}
        assert row["label"] in {0, 1, 2}
        assert row["category"] == "Politics", f"{label}: wrong category {idx}"
        gold = row["answer_info"]["ans" + str(row["label"])][1]
        if row["context_condition"] == "ambig":
            assert gold == "unknown", f"{label}: ambiguous row has non-Unknown answer {idx}"
        else:
            assert gold != "unknown", f"{label}: disambiguated answer is Unknown {idx}"


def main() -> None:
    assembled: dict[str, bytes] = {}
    rows_by_language: dict[str, list[dict]] = {}
    pending: dict[str, Path] = {}

    for lang in ("english", "bengali"):
        spec = MANIFEST["languages"][lang]
        base_path = ROOT / spec["pre_expansion_backup"]
        source_bytes = base_path.read_bytes()
        assert git_blob_sha(source_bytes) == spec["pre_expansion_blob_sha"], f"{lang}: baseline blob mismatch"
        original = records(source_bytes)
        assert_rows(original, lang + "/original", 0, 960)

        extras: list[bytes] = []
        extras_records: list[dict] = []
        for part in spec["shards"]:
            path = ROOT / part["path"]
            fragment = path.read_bytes()
            assert git_blob_sha(fragment) == part["blob_sha"], f"{lang}: shard hash mismatch: {path}"
            block = records(fragment)
            assert_rows(block, lang + "/" + path.name, part["first_id"], 480)
            assert block[-1]["id"] == part["last_id"]
            extras_records.extend(block)
            extras.append(fragment)
        assert_rows(extras_records, lang + "/expansion", 960, 1920)

        combined = source_bytes + b"".join(extras)
        full_rows = records(combined)
        assert_rows(full_rows, lang + "/expanded", 0, 2880)
        assert full_rows[:960] == original, f"{lang}: legacy 960-row prefix changed"
        assert Counter(r["question_index"] for r in full_rows) == Counter({q: 144 for q in range(1, 21)})
        assert Counter(r["label"] for r in full_rows) == Counter({0: 960, 1: 960, 2: 960})
        if len(set((r["context"], r["question"], r["ans0"], r["ans1"], r["ans2"]) for r in full_rows)) != 2880:
            raise ValueError(f"{lang}: duplicate context/question/permutation row")

        canonical = BASE / ("banglabbq_politics_" + lang + ".jsonl")
        current = canonical.read_bytes()
        if current not in (source_bytes, combined):
            raise ValueError(f"{lang}: canonical snapshot differs from both pre-expansion baseline and derived 2,880-row expansion; refusing overwrite")
        pending[lang] = canonical
        assembled[lang] = combined
        rows_by_language[lang] = full_rows

    same_fields = ("example_id", "question_index", "context_condition", "question_polarity",
                   "type", "label", "answer_info", "additional_metadata", "category", "id")
    for idx, (en, bn) in enumerate(zip(rows_by_language["english"], rows_by_language["bengali"])):
        if any(en[key] != bn[key] for key in same_fields):
            raise ValueError(f"Bilingual structural or metadata mismatch at example ID {idx}")

    for lang, canonical in pending.items():
        output = assembled[lang]
        if canonical.read_bytes() == output:
            print(f"{lang}: 2,880-record canonical snapshot already up to date")
        else:
            canonical.write_bytes(output)
            print(f"{lang}: materialized 2,880 records (960 original + 1,920 v2/v3)")

    print("Politics expansion assembly verified in both languages.")


if __name__ == "__main__":
    main()
