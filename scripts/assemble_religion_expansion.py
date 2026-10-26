#!/usr/bin/env python3
"""Safely assemble the 2,880-record BanglaBBQ Religion benchmark from immutable shards and an audited post-assembly patch.

The historical V1 source and 1,920 expansion rows remain frozen in SHA-pinned
snapshots and shards. For authorized Q3/Q8/Q9/Q10/Q12/Q13 repairs, this
assembler applies a separate versioned correction layer to the canonical
V1/V2/V3 records without rewriting historical inputs. Machine validation is
not independent native-speaker or causal source-verification certification.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from apply_religion_evidence_revisions import build as apply_evidence_revisions, load_patch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Dataset_BanglaBBQ_New/BanglaBBQ_Religion"
if not DATA.exists():
    DATA = ROOT / "BanglaBBQ_Religion"
EXP = DATA / "expansion_v2v3_20261017"
MANIFEST = json.loads((EXP / "manifest.json").read_text(encoding="utf-8"))
TEMPLATES = json.loads((EXP / "context_templates.json").read_text(encoding="utf-8"))
FIELDS = ["example_id", "question_index", "context_condition", "question_polarity",
          "type", "context", "question", "ans0", "ans1", "ans2", "label",
          "answer_info", "additional_metadata", "category", "id"]
LANG_NAMES = {"english": "Religion_eng.jsonl", "bengali": "Religion_bng.jsonl"}
SAME_FIELDS = ("question_index", "context_condition", "question_polarity", "type",
               "question", "ans0", "ans1", "ans2", "label", "answer_info", "category")
BILINGUAL_SHARED = ("example_id", "question_index", "context_condition",
                    "question_polarity", "type", "label", "answer_info",
                    "additional_metadata", "category", "id")


def git_blob_sha(content: bytes) -> str:
    prefix = b"blob " + str(len(content)).encode("ascii") + b"\0"
    return hashlib.sha1(prefix + content).hexdigest()


def load_jsonl(data: bytes) -> list[dict]:
    return [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_assembled(records: list[dict], language: str) -> None:
    require(len(records) == 2880, f"{language}: expected 2880, got {len(records)}")
    require(Counter(r["label"] for r in records) == Counter({0: 960, 1: 960, 2: 960}),
            f"{language}: gold-label imbalance")
    require(Counter(r["question_index"] for r in records) ==
            Counter({q: 144 for q in range(1, 21)}),
            f"{language}: theme counts unequal")
    seen = set()
    for i, row in enumerate(records):
        require(list(row) == FIELDS, f"{language}#{i}: 15-field schema/order changed")
        require(row["id"] == row["example_id"] == i, f"{language}#{i}: bad IDs")
        require(row["category"] == "Religion", f"{language}#{i}: bad category")
        require(row["context_condition"] in {"ambig", "disambig"}, f"{language}#{i}: condition")
        require(row["question_polarity"] in {"neg", "nonneg"}, f"{language}#{i}: polarity")
        gold_role = row["answer_info"][f"ans{row['label']}"][1]
        expected_unknown = row["context_condition"] == "ambig"
        require((gold_role == "unknown") == expected_unknown,
                f"{language}#{i}: answer role contradicts context condition")
        if expected_unknown:
            require(row[f"ans{row['label']}"] ==
                    ("Unknown" if language == "english" else "অজানা"),
                    f"{language}#{i}: ambiguous answer is not Unknown")
        else:
            require(row[f"ans{row['label']}"] not in {"Unknown", "অজানা"},
                    f"{language}#{i}: disambiguated gold answer Unknown")
        tup = (row["context"], row["question"], row["ans0"], row["ans1"], row["ans2"])
        require(tup not in seen, f"{language}#{i}: unintended duplicate QA tuple")
        seen.add(tup)
    for wave, variant in enumerate(("v1", "v2", "v3")):
        for q in range(1, 21):
            block = records[wave * 960 + (q - 1) * 48:
                            wave * 960 + q * 48]
            require(len(block) == 48 and all(r["question_index"] == q for r in block),
                    f"{language}: bad 48-row theme block {variant} Q{q}")
            for orientation in ("a", "b"):
                for cond in ("ambig", "disambig"):
                    for pol in ("neg", "nonneg"):
                        subset = [r for r in block if
                                  r["additional_metadata"]["version"] == orientation and
                                  r["context_condition"] == cond and
                                  r["question_polarity"] == pol]
                        require(len(subset) == 6, f"{language}: missing 6-way {variant} Q{q}")
                        require(len({(x["ans0"], x["ans1"], x["ans2"]) for x in subset}) == 6,
                                f"{language}: permutation failure {variant} Q{q}")


def main() -> None:
    ready = {}
    for lang in ("english", "bengali"):
        spec = MANIFEST["languages"][lang]
        base_path = ROOT / spec["pre_expansion_backup"]
        raw = base_path.read_bytes().replace(b"\r\n", b"\n")
        require(git_blob_sha(raw) == spec["pre_expansion_blob_sha"],
                f"{lang}: immutable V1 backup hash mismatch")
        require(raw.endswith(b"\n"), f"{lang}: missing terminating newline in V1 snapshot")
        baseline = load_jsonl(raw)
        require(len(baseline) == 960, f"{lang}: baseline count changed")
        require(len(spec["shards"]) == 8, f"{lang}: expected 8 shards")
        parts, appended = [], []
        for si, shard in enumerate(spec["shards"]):
            shard_path = ROOT / shard["path"]
            if not shard_path.exists():
                shard_path = DATA / "expansion_v2v3_20261017/shards" / Path(shard["path"]).name
            chunk = shard_path.read_bytes().replace(b"\r\n", b"\n")
            require(git_blob_sha(chunk) == shard["blob_sha"],
                    f"{lang}: shard hash mismatch {shard['path']}")
            require(chunk.endswith(b"\n"), f"{lang}: shard missing newline")
            rows = load_jsonl(chunk)
            require(len(rows) == 240, f"{lang}: unexpected shard row count")
            require(rows[0]["id"] == shard["first_id"] ==
                    960 + si * 240, f"{lang}: shard start mismatch")
            require(rows[-1]["id"] == shard["last_id"] ==
                    1199 + si * 240, f"{lang}: shard end mismatch")
            for row in rows:
                parent_id = (row["id"] - 960) % 960
                original = baseline[parent_id]
                variant = "v2" if row["id"] < 1920 else "v3"
                require(row["additional_metadata"]["wording_variant"] == variant,
                        f"{lang}#{row['id']}: variant mismatch")
                require(row["additional_metadata"]["parent_example_id"] == parent_id,
                        f"{lang}#{row['id']}: parent ID mismatch")
                for field in SAME_FIELDS:
                    require(row[field] == original[field],
                            f"{lang}#{row['id']}: changed original {field}")
                old_meta = dict(row["additional_metadata"])
                old_meta.pop("wording_variant", None)
                old_meta.pop("parent_example_id", None)
                require(old_meta == original["additional_metadata"],
                        f"{lang}#{row['id']}: citation/metadata mutation")
                key = f"{row['context_condition']}_{row['additional_metadata']['version']}"
                expected = TEMPLATES["themes"][str(row["question_index"])][variant][lang][key]
                require(row["context"] == expected,
                        f"{lang}#{row['id']}: changed approved wording template")
            parts.append(chunk)
            appended.extend(rows)
        combined = raw + b"".join(parts)
        original_rows = baseline + appended
        check_assembled(original_rows, lang)
        require(load_jsonl(combined) == original_rows, f"{lang}: byte assembly mismatch")

        # Apply the independently versioned six-theme correction layer; never
        # rewrite the pinned, uncorrected historical baseline or shards.
        revised_rows = apply_evidence_revisions(original_rows, lang, load_patch())
        check_assembled(revised_rows, lang)
        old_lines = combined.decode("utf-8").splitlines(keepends=True)
        corrected_lines = []
        for previous, fixed, raw_line in zip(original_rows, revised_rows, old_lines):
            corrected_lines.append(raw_line if previous == fixed else
                                   json.dumps(fixed, ensure_ascii=False) + "\n")
        corrected_bytes = "".join(corrected_lines).encode("utf-8")
        canonical = DATA / LANG_NAMES[lang]
        current = load_jsonl(canonical.read_bytes())
        require(current in (baseline, original_rows, revised_rows),
                f"{lang}: canonical differs from historical, pre-patch or approved corrected data")
        ready[lang] = (canonical, corrected_bytes, revised_rows)
        print(f"{lang}: 960+960+960 rows verified against shards and approved revisions")
    en = ready["english"][2]
    bn = ready["bengali"][2]
    for i, (a, b) in enumerate(zip(en, bn)):
        for field in BILINGUAL_SHARED:
            require(a[field] == b[field], f"bilingual mismatch at ID {i}, field {field}")
    for lang, (path, content, _) in ready.items():
        if path.read_bytes() == content:
            print(f"{lang}: canonical already synchronized")
        else:
            path.write_bytes(content)
            print(f"{lang}: materialized 2,880 rows")
    print("Religion expansion assembled with evidence-backed corrections; human linguistic/source caveats remain.")


if __name__ == "__main__":
    main()
