import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.bbq_scoring_engine import load_sidecar_map, classify_record_prediction

V2_DIR = ROOT / "fixed jsonL v2"
V21_DIR = ROOT / "fixed JsonL v2.1"
V1_DIR = ROOT / "fixed JsonL"
PA_CANON_DIR = ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_PhysicalAppearance"
AUDIT_DIR = Path(__file__).resolve().parents[1]

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

CATEGORIES = [
    ("Education", "BanglaBBQ_ENG_Education_QA_fixed.jsonl", "BanglaBBQ_BEN_Education_QA_fixed.jsonl", 2880),
    ("Ethnicity", "BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl", "BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl", 1440),
    ("HealthStatus", "BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl", 2880),
    ("MaritalStatus", "BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl", 2880),
    ("OccupationalBackground", "BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl", "BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl", 2880),
    ("PhysicalAppearance", "BanglaBBQ_ENG_PhysicalAppearance_QA_fixed.jsonl", "BanglaBBQ_BEN_PhysicalAppearance_QA_fixed.jsonl", 1440),
    ("Politics", "BanglaBBQ_ENG_Politics_QA_fixed.jsonl", "BanglaBBQ_BEN_Politics_QA_fixed.jsonl", 2880),
    ("Regional", "BanglaBBQ_ENG_Regional_QA_fixed.jsonl", "BanglaBBQ_BEN_Regional_QA_fixed.jsonl", 1440),
    ("Religion", "BanglaBBQ_ENG_Religion_QA_fixed.jsonl", "BanglaBBQ_BEN_Religion_QA_fixed.jsonl", 2880),
    ("SocialStatus", "BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl", 1440),
]

SPOONFEED_ADMIN_PATTERNS = [
    r"\bcrossed out\b", r"\bstruck out\b", r"\bstruck through\b", r"\bcrossed off\b",
    r"\bremoved\b", r"\bdeleted\b", r"\berased\b", r"\brejected\b", r"\bpassed over\b"
]

STOP_TOKENS = {
    "the", "a", "an", "student", "candidate", "worker", "applicant", "person", "resident", "employee",
    "voter", "supporter", "activist", "demonstrators", "journalist", "outlet", "newspaper", "family", "from", "of",
    "প্রার্থী", "শিক্ষার্থী", "কর্মী", "ব্যক্তি", "বাসিন্দা", "ভোটার", "সমর্থক", "থেকে", "আসা", "একজন", "স্নাতক"
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def get_v1_path(cat: str, lang: str, fname: str) -> Path:
    if cat == "PhysicalAppearance":
        return PA_CANON_DIR / f"BanglaBBQ_{lang}_PhysicalAppearance.jsonl"
    return V1_DIR / fname


def tokenize_words(text: str):
    return re.findall(r"[a-zA-Z]+|[\u0980-\u09FF]+", text.lower())


def ngram_overlap(s1: str, s2: str, n: int = 3):
    w1 = tokenize_words(s1)
    w2 = tokenize_words(s2)
    if len(w1) < n or len(w2) < n:
        return []
    g1 = {tuple(w1[i:i+n]) for i in range(len(w1) - n + 1)}
    g2 = {tuple(w2[i:i+n]) for i in range(len(w2) - n + 1)}
    return [" ".join(g) for g in sorted(g1 & g2)]


def main():
    sidecar_map = load_sidecar_map(ROOT / "metadata" / "sidecar_stereotype_target_map.json")
    pre_hashes = json.loads((AUDIT_DIR / "v2_pre_hashes.json").read_text(encoding="utf-8"))

    sha_manifest = {"v2_untouched_all": True, "files": {}}
    structural_report = {"overall_status": "PASS", "scoring_engine_errors": 0, "files": {}}

    q_family_rows = []
    entailment_rows = []
    bilingual_rows = []

    expected_block = [("ambig", "neg"), ("disambig", "neg"), ("ambig", "nonneg"), ("disambig", "nonneg")]

    for cat, eng_fn, ben_fn, exp_count in CATEGORIES:
        for lang, fn in [("ENG", eng_fn), ("BEN", ben_fn)]:
            v2_path = V2_DIR / fn
            v21_path = V21_DIR / fn
            v1_path = get_v1_path(cat, lang, fn)

            # Check SHA-256 immutability of V2
            v2_now = sha256_file(v2_path)
            v2_before = pre_hashes[fn]["v2_sha256_before"]
            v2_untouched = (v2_now == v2_before)
            if not v2_untouched:
                sha_manifest["v2_untouched_all"] = False

            v21_now = sha256_file(v21_path)
            v1_now = sha256_file(v1_path)

            sha_manifest["files"][fn] = {
                "v1_sha256": v1_now,
                "v2_sha256_before": v2_before,
                "v2_sha256_after": v2_now,
                "v2_untouched": v2_untouched,
                "v21_sha256": v21_now,
                "changed_from_v2": (v21_now != v2_now)
            }

            # Structural validation
            rows = load_jsonl(v21_path)
            v2_rows = load_jsonl(v2_path)
            v1_rows = load_jsonl(v1_path)

            schema_err = 0
            seq_err = 0
            ambig_err = 0
            disambig_err = 0
            block_err = 0
            perm_err = 0
            cf_flip_err = 0
            prefix_err = 0
            scoring_err = 0
            protected_field_diff = 0
            label_counts = Counter()

            for idx, r in enumerate(rows):
                if set(r.keys()) != set(REQUIRED_FIELDS): schema_err += 1
                if r.get("example_id") != idx: seq_err += 1
                lbl = r.get("label")
                label_counts[lbl] += 1
                cond = r.get("context_condition")
                ai = r.get("answer_info", {})
                g_txt = r.get(f"ans{lbl}", "")
                g_role = ai.get(f"ans{lbl}", [None, None])[1]
                if cond == "ambig" and (g_txt.strip().lower() not in UNKNOWN_TERMS or g_role != "unknown"):
                    ambig_err += 1
                if cond == "disambig" and (g_txt.strip().lower() in UNKNOWN_TERMS or g_role == "unknown"):
                    disambig_err += 1

                # Check protected fields unchanged vs V2
                r_v2 = v2_rows[idx]
                for k in REQUIRED_FIELDS:
                    if k not in ("context", "question") and r.get(k) != r_v2.get(k):
                        protected_field_diff += 1

                # Scoring engine check
                try:
                    classify_record_prediction(r, lbl, sidecar_map)
                except Exception:
                    scoring_err += 1

            for i in range(0, len(rows), 4):
                blk = rows[i:i+4]
                if [(x["context_condition"], x["question_polarity"]) for x in blk] != expected_block:
                    block_err += 1

            for i in range(0, len(rows), 2):
                if not rows[i+1]["context"].startswith(rows[i]["context"]):
                    prefix_err += 1

            for i in range(0, len(rows), 24):
                ori = rows[i:i+24]
                for cp in expected_block:
                    sub = [x for x in ori if (x["context_condition"], x["question_polarity"]) == cp]
                    if len({(x["ans0"], x["ans1"], x["ans2"]) for x in sub}) != 6:
                        perm_err += 1

            for i in range(0, len(rows), 48):
                r1_neg = rows[i+1]["answer_info"][f"ans{rows[i+1]['label']}"][1]
                r2_neg = rows[i+25]["answer_info"][f"ans{rows[i+25]['label']}"][1]
                r1_pos = rows[i+3]["answer_info"][f"ans{rows[i+3]['label']}"][1]
                r2_pos = rows[i+27]["answer_info"][f"ans{rows[i+27]['label']}"][1]
                if r1_neg == r2_neg or r1_pos == r2_pos:
                    cf_flip_err += 1

            dups = sum(c - 1 for c in Counter((r["context_condition"], r["question_polarity"], r["context"], r["question"], r["ans0"], r["ans1"], r["ans2"]) for r in rows).values() if c > 1)

            f_status = "PASS" if (
                len(rows) == exp_count and schema_err == 0 and seq_err == 0 and
                ambig_err == 0 and disambig_err == 0 and block_err == 0 and
                perm_err == 0 and cf_flip_err == 0 and prefix_err == 0 and
                scoring_err == 0 and protected_field_diff == 0 and dups == 0 and
                set(label_counts.values()) == {exp_count // 3}
            ) else "FAIL"

            if f_status == "FAIL":
                structural_report["overall_status"] = "FAIL"
            structural_report["scoring_engine_errors"] += scoring_err
            structural_report["files"][fn] = {
                "status": f_status, "records": len(rows), "expected": exp_count,
                "schema_err": schema_err, "seq_err": seq_err, "ambig_err": ambig_err,
                "disambig_err": disambig_err, "block_err": block_err, "perm_err": perm_err,
                "cf_flip_err": cf_flip_err, "prefix_err": prefix_err, "scoring_err": scoring_err,
                "protected_field_diff": protected_field_diff, "duplicates": dups
            }

        # Bilingual & Question & S3 Audits per category
        eng_rows = load_jsonl(V21_DIR / eng_fn)
        ben_rows = load_jsonl(V21_DIR / ben_fn)
        v1_eng_rows = load_jsonl(get_v1_path(cat, "ENG", eng_fn))
        v1_ben_rows = load_jsonl(get_v1_path(cat, "BEN", ben_fn))

        # Check all 48-row families (and 24-row blocks)
        for i in range(0, len(eng_rows), 24):
            re_amb, re_dis = eng_rows[i], eng_rows[i+1]
            rb_amb, rb_dis = ben_rows[i], ben_rows[i+1]
            re_pos_a, re_pos_d = eng_rows[i+2], eng_rows[i+3]
            rb_pos_a, rb_pos_d = ben_rows[i+2], ben_rows[i+3]

            # Ambig/disambig question equality
            q_eq_e = (re_amb["question"] == re_dis["question"]) and (re_pos_a["question"] == re_pos_d["question"])
            q_eq_b = (rb_amb["question"] == rb_dis["question"]) and (rb_pos_a["question"] == rb_pos_d["question"])

            # Check rewritten vs V1
            rewritten_e = (v1_eng_rows[i+1]["question"] != re_dis["question"]) and (v1_eng_rows[i+3]["question"] != re_pos_d["question"])
            rewritten_b = (v1_ben_rows[i+1]["question"] != rb_dis["question"]) and (v1_ben_rows[i+3]["question"] != rb_pos_d["question"])

            # Check ambig entities present
            missing_ent = []
            for r, lng in [(re_amb, "ENG"), (rb_amb, "BEN")]:
                ctx_l = r["context"].lower()
                for k in range(3):
                    if r["answer_info"][f"ans{k}"][1] != "unknown":
                        words = [w.strip(",.") for w in r[f"ans{k}"].split() if len(w.strip(",.")) >= 3 and w.strip(",.").lower() not in STOP_TOKENS]
                        if words and not any(w[:4].lower() in ctx_l for w in words):
                            missing_ent.append(f"{lng}:{r[f'ans{k}']}")

            s3_e = re_dis["context"][len(re_amb["context"]):].strip()
            s3_b = rb_dis["context"][len(rb_amb["context"]):].strip()
            ov_e = ngram_overlap(s3_e, re_dis["question"], 3) + ngram_overlap(s3_e, re_pos_d["question"], 3)
            ov_b = ngram_overlap(s3_b, rb_dis["question"], 3) + ngram_overlap(s3_b, rb_pos_d["question"], 3)

            admin_hits = [p for p in SPOONFEED_ADMIN_PATTERNS if re.search(p, s3_e.lower())]
            lbl_parity = (re_dis["label"] == rb_dis["label"]) and (re_pos_d["label"] == rb_pos_d["label"])

            blk_num = (i // 24) + 1
            if i % 48 == 0:
                q_family_rows.append([
                    cat, re_dis["question_index"], (i // 48) % 3 + 1, re_dis["example_id"],
                    rewritten_e, rewritten_b, q_eq_e, q_eq_b,
                    re_dis["question"], re_pos_d["question"],
                    rb_dis["question"], rb_pos_d["question"],
                    "PASS" if (q_eq_e and q_eq_b and rewritten_e and rewritten_b) else "FAIL"
                ])

            entailment_rows.append([
                cat, re_dis["question_index"], blk_num, re_dis["example_id"],
                len(ov_e), len(ov_b), len(admin_hits), "; ".join(admin_hits),
                len(missing_ent), "; ".join(missing_ent),
                "PASS" if (len(ov_e) == 0 and len(ov_b) == 0 and len(admin_hits) == 0 and len(missing_ent) == 0) else "REVIEW",
                s3_e, s3_b
            ])

            bilingual_rows.append([
                cat, re_dis["question_index"], blk_num, re_dis["example_id"],
                lbl_parity, rewritten_e == rewritten_b, len(missing_ent) == 0,
                "PASS" if (lbl_parity and rewritten_e == rewritten_b and len(missing_ent) == 0) else "FAIL",
                re_dis["question"], rb_dis["question"]
            ])

    # Bengali leftover linguistic check across all 10 BEN files
    ben_scan = {}
    for cat, _, ben_fn, _ in CATEGORIES:
        b_rows = load_jsonl(V21_DIR / ben_fn)
        ben_scan[cat] = {
            "hyphen_nabil_r": sum(1 for r in b_rows if "নাবিল-র" in r["context"] or "নাবিল-র" in r["question"]),
            "hyphen_suffix_any": sum(1 for r in b_rows for tok in re.findall(r"\S+-\S+", r["context"] + " " + r["question"]) if re.search(r"-(?:র|কে|এর|তে|য়|য়ে|দের|গুলোর)$", tok) and tok != "৫-এর"),
            "sakhatkar_grahan": sum(1 for r in b_rows if "সাক্ষাৎকারগ্রহণকারী" in r["context"]),
            "sakhatkar_non_journalistic": sum(1 for r in b_rows if "সাক্ষাৎকার" in r["context"] and not ((cat == "HealthStatus" and int(r["question_index"]) == 16) or (cat == "Politics" and int(r["question_index"]) == 12))),
            "byabosthapok": sum(1 for r in b_rows if "ব্যবস্থাপক" in r["context"] or "ব্যবস্থাপক" in r["question"]),
            "bureaucratic_old": sum(1 for r in b_rows for w in ["উক্ত", "অবহিত", "দাখিল", "প্রদান করেন", "ব্যর্থ হন"] if w in r["context"] or w in r["question"]),
            "english_leaks": sum(1 for r in b_rows if re.search(r"[A-Za-z]{2,}", r["context"] + " " + r["question"]))
        }

    structural_report["bengali_post_repair_scan"] = ben_scan

    # Write all deliverables
    (AUDIT_DIR / "SHA256_MANIFEST.json").write_text(json.dumps(sha_manifest, indent=2), encoding="utf-8")
    (AUDIT_DIR / "final_structural_validation.json").write_text(json.dumps(structural_report, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(AUDIT_DIR / "question_family_validation.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "variation", "sample_eid", "rewritten_eng", "rewritten_ben", "ambig_eq_disambig_eng", "ambig_eq_disambig_ben", "q_neg_eng", "q_pos_eng", "q_neg_ben", "q_pos_ben", "status"])
        w.writerows(q_family_rows)

    with open(AUDIT_DIR / "semantic_entailment_audit.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "orientation_block", "sample_eid", "ngram3_eng", "ngram3_ben", "admin_marker_count", "admin_markers", "missing_ambig_entity_count", "missing_ambig_entities", "status", "s3_eng", "s3_ben"])
        w.writerows(entailment_rows)

    with open(AUDIT_DIR / "bilingual_alignment_report.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "orientation_block", "sample_eid", "label_parity", "rewrite_parity", "ambig_entity_parity", "status", "q_neg_eng", "q_neg_ben"])
        w.writerows(bilingual_rows)

    print(f"=== FINAL V2.1 REVALIDATION COMPLETE ===")
    print(f"V2 Untouched (SHA-256 bit-exact): {sha_manifest['v2_untouched_all']}")
    print(f"Overall Structural Status       : {structural_report['overall_status']} (Scoring errors: {structural_report['scoring_engine_errors']})")
    print(f"Question Families (480) PASS    : {sum(1 for r in q_family_rows if r[-1] == 'PASS')} / {len(q_family_rows)}")
    print(f"Semantic Blocks (960) PASS      : {sum(1 for r in entailment_rows if r[10] == 'PASS')} / {len(entailment_rows)}")
    print(f"Bilingual Blocks (960) PASS     : {sum(1 for r in bilingual_rows if r[7] == 'PASS')} / {len(bilingual_rows)}")
    print("\nBengali Post-Repair Residual Scan:")
    for cat, d in ben_scan.items():
        print(f"  {cat:<22}: {d}")


if __name__ == "__main__":
    main()
