#!/usr/bin/env python3
"""Apply the approved Religion QA patch manifest to canonical JSONL, safely and idempotently.

Run from repository root on fix/religion-qa-repair-20261017:
    python scripts/apply_religion_qa_patch_manifest.py --dry-run
    python scripts/apply_religion_qa_patch_manifest.py
    python scripts/validate_religion_dataset.py

Authoritative working dataset is the live Google Sheet. This script materializes
the exact verified Sheets patch onto the pre-repair GitHub JSONL snapshots.
Never touches historical files or backups.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "research_logs/2026-10-17_religion_qa_patch_manifest.json"
FILES = {
    "en": ROOT / "BanglaBBQ_Religion/Religion_eng.jsonl",
    "bn": ROOT / "BanglaBBQ_Religion/Religion_bng.jsonl",
}
FIELDS = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id",
]
WRITABLE_COLS = {5, 6, 7, 8, 9, 11, 12}

def blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()

def prepare(path: Path, manifest: dict, lang: str) -> tuple[bytes, list[dict], int]:
    raw = path.read_bytes()
    spec = manifest["files"][lang]
    raw_sha = blob_sha(raw)
    lf_sha = blob_sha(raw.replace(b"\r\n", b"\n"))
    source_pristine = spec["preRepairBlobSha"] in {raw_sha, lf_sha}
    line_ending = "\r\n" if b"\r\n" in raw else "\n"
    lines = raw.decode("utf-8").splitlines()
    if len(lines) != 960:
        raise ValueError(f"{lang}: expected 960 records, found {len(lines)}")
    rows = [json.loads(x) for x in lines]
    if any(list(row) != FIELDS or row["example_id"] != i or row["id"] != i for i, row in enumerate(rows)):
        raise ValueError(f"{lang}: original schema/IDs differ from expected")
    patches = spec["changes"]
    if len(patches) != spec["changedRows"]:
        raise ValueError(f"{lang}: manifest changed row count mismatch")
    touched = set()
    fully_applied = True
    output_lines = list(lines)
    for change in patches:
        i = change["id"]
        if i in touched or not (0 <= i < 960):
            raise ValueError(f"{lang}: repeated or invalid ID {i}")
        touched.add(i)
        fields = {int(col): value for col, value in change["columns"].items()}
        if not fields or not set(fields) <= WRITABLE_COLS:
            raise ValueError(f"{lang}: invalid writable field selection at {i}")
        original = rows[i]
        target = json.loads(json.dumps(original, ensure_ascii=False))
        for col, value in fields.items():
            key = FIELDS[col]
            if original[key] != value:
                fully_applied = False
            target[key] = value
        output_lines[i] = json.dumps(target, ensure_ascii=False, separators=(",", ":"))
        rows[i] = target
    if not source_pristine and not fully_applied:
        raise ValueError(
            f"{lang}: current canonical file is neither the frozen pre-repair "
            "snapshot nor fully patched; refusing an uncertain merge"
        )
    counts = Counter(row["question_index"] for row in rows)
    if counts != Counter({q: 48 for q in range(1, 21)}):
        raise ValueError(f"{lang}: invalid theme counts")
    if Counter(row["label"] for row in rows) != Counter({0: 320, 1: 320, 2: 320}):
        raise ValueError(f"{lang}: changed label balance")
    if len(set((r["context"], r["question"], r["ans0"], r["ans1"], r["ans2"]) for r in rows)) != 960:
        raise ValueError(f"{lang}: duplicate QA tuple")
    for row in rows:
        gold = row["answer_info"]["ans" + str(row["label"])][1]
        if row["context_condition"] == "ambig" and gold != "unknown":
            raise ValueError(f"{lang}: ambiguous gold mismatch: {row['id']}")
        if row["context_condition"] == "disambig" and gold == "unknown":
            raise ValueError(f"{lang}: disambiguated gold mismatch: {row['id']}")
    content = (line_ending.join(output_lines) + line_ending).encode("utf-8")
    return content, rows, len(touched)

def main() -> None:
    argp = argparse.ArgumentParser()
    argp.add_argument("--dry-run", action="store_true")
    args = argp.parse_args()
    manifest = json.loads(PLAN.read_text(encoding="utf-8"))
    results = {lang: prepare(path, manifest, lang) for lang, path in FILES.items()}
    shared = [
        "example_id", "question_index", "context_condition", "question_polarity",
        "type", "label", "answer_info", "additional_metadata", "category", "id"
    ]
    for i, (en, bn) in enumerate(zip(results["en"][1], results["bn"][1])):
        if any(en[k] != bn[k] for k in shared):
            raise ValueError(f"Bilingual metadata mismatch at example ID {i}")
    for lang, path in FILES.items():
        content, _rows, changed = results[lang]
        if not args.dry_run:
            if path.read_bytes() != content:
                path.write_bytes(content)
        print(f"{lang}: {changed} rows in approved manifest; "
              f"{'dry-run verified' if args.dry_run else 'canonical JSONL materialized'}")
    print("QA patch safely applied in both languages; run full validator and Sheets parity audit.")

if __name__ == "__main__":
    main()
