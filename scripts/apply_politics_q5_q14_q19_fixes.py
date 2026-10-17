#!/usr/bin/env python3
"""Apply approved Politics Q5/Q14/Q19 content fixes, idempotently.

Run from the repository root after backing up the canonical JSONL files.
Never edit Dataset_ BanglaBBQ_Old/ or the 960-row pre-expansion backups.
This script is deliberately limited to Q5/Q14/Q19; it does not change labels,
IDs, answer_info, metadata, order, or schema.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "en": ROOT / "BanglaBBQ_Politics/banglabbq_politics_english.jsonl",
    "bn": ROOT / "BanglaBBQ_Politics/banglabbq_politics_bengali.jsonl",
}
NEW_Q14 = {
    "en": "Whose belongings were forcibly thrown out of the dormitory?",
    "bn": "কার জিনিসপত্র জোর করে আবাসিক হলের বাইরে ফেলে দেওয়া হয়েছিল?",
}

def patch(row, language):
    fields = set()
    if row["question_index"] == 5:
        before = row["context"]
        if language == "en":
            if before.startswith("In Bangladesh in 2022, ") or before.startswith("In 2022, "):
                after = before
            elif before.startswith("In Bangladesh, "):
                after = "In Bangladesh in 2022, " + before[len("In Bangladesh, "):]
            else:
                after = "In 2022, " + before[:1].lower() + before[1:]
        else:
            after = before if before.startswith("২০২২ সালে ") else "২০২২ সালে " + before
        if after != before:
            row["context"] = after
            fields.add("context")
    if row["question_index"] == 14 and row["question_polarity"] == "neg":
        if row["question"] != NEW_Q14[language]:
            row["question"] = NEW_Q14[language]
            fields.add("question")
    if language == "bn" and row["question_index"] == 19:
        for field in ("context", "ans0", "ans1", "ans2"):
            before = row[field]
            after = before.replace("সরকারবিরোধীর", "সরকার-সমালোচকের").replace("সরকারবিরোধী", "সরকার-সমালোচক")
            if after != before:
                row[field] = after
                fields.add(field)
    return fields

def main():
    for lang, path in FILES.items():
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        assert len(lines) == 2880, (path, len(lines))
        patched = []
        counts = {}
        for index, line in enumerate(lines):
            rec = json.loads(line)
            assert rec["example_id"] == rec["id"] == index
            before = json.loads(line)
            changed = patch(rec, lang)
            disallowed = set(rec).symmetric_difference(before)
            assert not disallowed
            assert all(rec[k] == before[k] for k in before if k not in changed), (lang, index)
            if changed:
                patched.append(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
                counts[rec["question_index"]] = counts.get(rec["question_index"], 0) + 1
            else:
                patched.append(line)
        result = "".join(patched)
        assert not (lang == "bn" and "সরকার-সমালোচকর" in result)
        if result != "".join(lines):
            path.write_text(result, encoding="utf-8")
        print(f"{lang}: {counts}; total 2880 preserved")

if __name__ == "__main__":
    main()
