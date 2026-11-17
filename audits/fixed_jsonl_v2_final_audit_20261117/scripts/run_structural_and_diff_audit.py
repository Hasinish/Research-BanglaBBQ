import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V2_DIR = ROOT / "fixed jsonL v2"
V1_DIR = ROOT / "fixed JsonL"
PA_CANON_DIR = ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_PhysicalAppearance"
OUT_DIR = Path(__file__).resolve().parents[1]

REQUIRED_FIELDS = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2",
    "label", "answer_info", "additional_metadata", "category", "id"
]

UNKNOWN_TERMS = {
    "unknown", "cannot be determined", "can't be determined", "not enough info",
    "not enough information", "not known", "undetermined",
    "অজানা", "বলা সম্ভব নয়", "নির্ধারণ করা সম্ভব নয়", "নিশ্চিতভাবে বলা যায় না",
    "নিশ্চিতভাবে বলা যায় না", "পর্যাপ্ত তথ্য নেই", "জানা নেই", "অনির্ধারিত",
    "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না"
}

EXPECTED_FILES = [
    ("Education", "ENG", "BanglaBBQ_ENG_Education_QA_fixed.jsonl", 2880),
    ("Education", "BEN", "BanglaBBQ_BEN_Education_QA_fixed.jsonl", 2880),
    ("Ethnicity", "ENG", "BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl", 1440),
    ("Ethnicity", "BEN", "BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl", 1440),
    ("HealthStatus", "ENG", "BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl", 2880),
    ("HealthStatus", "BEN", "BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl", 2880),
    ("MaritalStatus", "ENG", "BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl", 2880),
    ("MaritalStatus", "BEN", "BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl", 2880),
    ("OccupationalBackground", "ENG", "BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl", 2880),
    ("OccupationalBackground", "BEN", "BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl", 2880),
    ("PhysicalAppearance", "ENG", "BanglaBBQ_ENG_PhysicalAppearance_QA_fixed.jsonl", 1440),
    ("PhysicalAppearance", "BEN", "BanglaBBQ_BEN_PhysicalAppearance_QA_fixed.jsonl", 1440),
    ("Politics", "ENG", "BanglaBBQ_ENG_Politics_QA_fixed.jsonl", 2880),
    ("Politics", "BEN", "BanglaBBQ_BEN_Politics_QA_fixed.jsonl", 2880),
    ("Regional", "ENG", "BanglaBBQ_ENG_Regional_QA_fixed.jsonl", 1440),
    ("Regional", "BEN", "BanglaBBQ_BEN_Regional_QA_fixed.jsonl", 1440),
    ("Religion", "ENG", "BanglaBBQ_ENG_Religion_QA_fixed.jsonl", 2880),
    ("Religion", "BEN", "BanglaBBQ_BEN_Religion_QA_fixed.jsonl", 2880),
    ("SocialStatus", "ENG", "BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl", 1440),
    ("SocialStatus", "BEN", "BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl", 1440),
]


def get_baseline_path(cat: str, lang: str, fname: str) -> Path:
    if cat == "PhysicalAppearance":
        return PA_CANON_DIR / f"BanglaBBQ_{lang}_PhysicalAppearance.jsonl"
    return V1_DIR / fname


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_unknown_text(txt: str) -> bool:
    return txt.strip().lower() in UNKNOWN_TERMS


def main():
    inventory_rows = []
    structural_report = {
        "v2_directory": str(V2_DIR),
        "total_expected_files": len(EXPECTED_FILES),
        "actual_files_found": len(list(V2_DIR.glob("*.jsonl"))),
        "overall_status": "PASS",
        "files": {}
    }
    diff_rows = []

    for cat, lang, fname, expected_count in EXPECTED_FILES:
        fpath = V2_DIR / fname
        if not fpath.exists():
            inventory_rows.append([cat, lang, fname, "MISSING", 0, "", 0, expected_count, "FAIL"])
            structural_report["overall_status"] = "FAIL"
            structural_report["files"][fname] = {"status": "FAIL", "error": "File missing"}
            continue

        raw_bytes = fpath.read_bytes()
        fhash = sha256_file(fpath)
        try:
            text = raw_bytes.decode("utf-8")
            utf8_ok = True
        except UnicodeDecodeError:
            text = ""
            utf8_ok = False

        lines = [l for l in text.splitlines() if l.strip()] if utf8_ok else []
        records = []
        json_errors = []
        for idx, line in enumerate(lines):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                json_errors.append({"line": idx + 1, "error": str(e)})

        # Structural checks
        schema_errors = 0
        seq_id_errors = 0
        ambig_label_errors = 0
        disambig_label_errors = 0
        answer_info_structure_errors = 0
        answer_info_text_mismatch = 0
        label_counts = Counter()
        cond_counts = Counter()
        pol_counts = Counter()
        block_order_errors = 0
        perm_errors = 0

        for idx, r in enumerate(records):
            if set(r.keys()) != set(REQUIRED_FIELDS):
                schema_errors += 1
            if r.get("example_id") != idx:
                seq_id_errors += 1

            lbl = r.get("label")
            label_counts[lbl] += 1
            cond = r.get("context_condition")
            pol = r.get("question_polarity")
            cond_counts[cond] += 1
            pol_counts[pol] += 1

            ai = r.get("answer_info", {})
            if lbl not in (0, 1, 2):
                ambig_label_errors += 1
            else:
                gold_text = r.get(f"ans{lbl}", "")
                gold_role = ai.get(f"ans{lbl}", [None, None])[1] if isinstance(ai, dict) and isinstance(ai.get(f"ans{lbl}"), list) and len(ai.get(f"ans{lbl}")) == 2 else None
                if cond == "ambig" and (not is_unknown_text(gold_text) or gold_role != "unknown"):
                    ambig_label_errors += 1
                if cond == "disambig" and (is_unknown_text(gold_text) or gold_role == "unknown"):
                    disambig_label_errors += 1

            if not isinstance(ai, dict) or set(ai.keys()) != {"ans0", "ans1", "ans2"}:
                answer_info_structure_errors += 1
            else:
                for k in ("ans0", "ans1", "ans2"):
                    v = ai[k]
                    if not isinstance(v, list) or len(v) != 2:
                        answer_info_structure_errors += 1
                        break
                    elif v[0] != r.get(k):
                        answer_info_text_mismatch += 1
                        break

        # Check 4-row block ordering & 6-way permutations per 24-row orientation block
        expected_block = [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]
        for i in range(0, len(records), 4):
            chunk = records[i:i+4]
            if len(chunk) == 4:
                actual_block = [(c.get("context_condition"), c.get("question_polarity")) for c in chunk]
                if actual_block != expected_block:
                    block_order_errors += 1

        # Group by (question_index, ambig_context_prefix_or_type) or 24-row blocks
        for i in range(0, len(records), 24):
            ori_block = records[i:i+24]
            if len(ori_block) == 24:
                for cond_pol in expected_block:
                    sub = [r for r in ori_block if (r.get("context_condition"), r.get("question_polarity")) == cond_pol]
                    perms = {tuple(sorted([r["ans0"], r["ans1"], r["ans2"]])) for r in sub}
                    exact_perms = {(r["ans0"], r["ans1"], r["ans2"]) for r in sub}
                    if len(sub) != 6 or len(exact_perms) != 6 or len(perms) != 1:
                        perm_errors += 1

        # Check duplicates within condition+polarity
        dup_counter = Counter((r.get("context_condition"), r.get("question_polarity"), r.get("context"), r.get("question"), r.get("ans0"), r.get("ans1"), r.get("ans2")) for r in records)
        unintended_dups = sum(cnt - 1 for cnt in dup_counter.values() if cnt > 1)

        file_status = "PASS"
        if (
            not utf8_ok or json_errors or len(records) != expected_count or
            schema_errors or seq_id_errors or ambig_label_errors or disambig_label_errors or
            answer_info_structure_errors or block_order_errors or perm_errors or unintended_dups or
            set(label_counts.values()) != {expected_count // 3}
        ):
            file_status = "FAIL"
            structural_report["overall_status"] = "FAIL"

        inventory_rows.append([
            cat, lang, fname, "PRESENT", len(raw_bytes), fhash,
            len(records), expected_count, file_status
        ])

        structural_report["files"][fname] = {
            "category": cat,
            "language": lang,
            "status": file_status,
            "record_count": len(records),
            "expected_count": expected_count,
            "utf8_ok": utf8_ok,
            "json_errors": len(json_errors),
            "schema_errors": schema_errors,
            "seq_id_errors": seq_id_errors,
            "ambig_label_errors": ambig_label_errors,
            "disambig_label_errors": disambig_label_errors,
            "answer_info_structure_errors": answer_info_structure_errors,
            "answer_info_text_mismatch_inherited": answer_info_text_mismatch,
            "block_order_errors": block_order_errors,
            "perm_errors": perm_errors,
            "unintended_duplicates": unintended_dups,
            "label_distribution": dict(label_counts),
            "condition_distribution": dict(cond_counts),
            "polarity_distribution": dict(pol_counts),
        }

        # Field-level diff against V1 / canonical baseline
        base_path = get_baseline_path(cat, lang, fname)
        if base_path.exists():
            base_records = [json.loads(l) for l in base_path.read_text(encoding="utf-8").splitlines() if l.strip()]
            changed_counts = Counter()
            unexpected_field_eids = defaultdict(list)
            total_changed_rows = 0
            for r_v1, r_v2 in zip(base_records, records):
                row_diff = False
                for k in REQUIRED_FIELDS:
                    if r_v1.get(k) != r_v2.get(k):
                        changed_counts[k] += 1
                        row_diff = True
                        if k not in ("context", "question"):
                            if len(unexpected_field_eids[k]) < 10:
                                unexpected_field_eids[k].append(r_v2.get("example_id"))
                if row_diff:
                    total_changed_rows += 1

            diff_rows.append([
                cat, lang, fname, str(base_path.relative_to(ROOT)),
                len(base_records), len(records), total_changed_rows,
                changed_counts["context"], changed_counts["question"],
                sum(v for k, v in changed_counts.items() if k not in ("context", "question")),
                json.dumps({k: v for k, v in changed_counts.items() if k not in ("context", "question")}),
                json.dumps(dict(unexpected_field_eids))
            ])
        else:
            diff_rows.append([cat, lang, fname, "MISSING_BASELINE", 0, len(records), 0, 0, 0, 0, "{}", "{}"])

    with open(OUT_DIR / "file_inventory.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "language", "filename", "presence", "bytes", "sha256", "actual_records", "expected_records", "structural_status"])
        w.writerows(inventory_rows)

    with open(OUT_DIR / "structural_validation_report.json", "w", encoding="utf-8") as f:
        json.dump(structural_report, f, indent=2, ensure_ascii=False)

    with open(OUT_DIR / "field_level_diff_manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "language", "v2_filename", "baseline_path", "v1_records", "v2_records", "total_modified_rows", "context_changes", "question_changes", "other_field_changes", "other_field_breakdown", "sample_other_field_eids"])
        w.writerows(diff_rows)

    print(f"[DONE] Overall structural status: {structural_report['overall_status']}")
    for row in diff_rows:
        print(f"  {row[0]:<22} {row[1]} | mod_rows={row[6]:<4} ctx={row[7]:<4} q={row[8]:<4} other={row[9]} {row[10]}")


if __name__ == "__main__":
    main()
