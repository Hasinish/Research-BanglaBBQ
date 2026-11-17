import csv
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V2_DIR = ROOT / "fixed jsonL v2"
V1_DIR = ROOT / "fixed JsonL"
PA_CANON_DIR = ROOT / "Dataset_BanglaBBQ_New" / "BanglaBBQ_PhysicalAppearance"
OUT_DIR = Path(__file__).resolve().parents[1]

CATEGORIES = [
    ("Education", "BanglaBBQ_ENG_Education_QA_fixed.jsonl", "BanglaBBQ_BEN_Education_QA_fixed.jsonl"),
    ("Ethnicity", "BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl", "BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl"),
    ("HealthStatus", "BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl"),
    ("MaritalStatus", "BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl"),
    ("OccupationalBackground", "BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl", "BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl"),
    ("PhysicalAppearance", "BanglaBBQ_ENG_PhysicalAppearance_QA_fixed.jsonl", "BanglaBBQ_BEN_PhysicalAppearance_QA_fixed.jsonl"),
    ("Politics", "BanglaBBQ_ENG_Politics_QA_fixed.jsonl", "BanglaBBQ_BEN_Politics_QA_fixed.jsonl"),
    ("Regional", "BanglaBBQ_ENG_Regional_QA_fixed.jsonl", "BanglaBBQ_BEN_Regional_QA_fixed.jsonl"),
    ("Religion", "BanglaBBQ_ENG_Religion_QA_fixed.jsonl", "BanglaBBQ_BEN_Religion_QA_fixed.jsonl"),
    ("SocialStatus", "BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl", "BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl"),
]

SOCIAL_BIAS_PATTERNS_EN = [
    r"\bmore likely to\b", r"\bconsidered less\b", r"\bconsidered more\b",
    r"\bviewed as\b", r"\bseen as\b", r"\btreated with\b", r"\btreated as\b",
    r"\bconsidered untrustworthy\b", r"\bconsidered incompetent\b", r"\bconsidered irresponsible\b",
    r"\bconsidered incapable\b", r"\bless capable\b", r"\bmore capable\b",
    r"\bless trustworthy\b", r"\bmore trustworthy\b", r"\bsocially excluded\b",
    r"\bperceived as\b", r"\bjudged as\b", r"\bfaced prejudice\b", r"\bassumed to be\b",
    r"\btoo lazy\b", r"\bincompetent\b", r"\bcompetent\b", r"\buntrustworthy\b",
    r"\bexcluded from\b", r"\bdenied service\b", r"\btrouble remembering\b",
]

INCIDENT_LOOKUP_PATTERNS_EN = [
    r"\bpassed over\b", r"\bskipped over\b", r"\bleft out\b", r"\bcrossed out\b",
    r"\bremoved from\b", r"\bwent home\b", r"\bgot to ride\b", r"\bsent home\b",
    r"\bhad to take another route\b", r"\bcould not get into\b", r"\bwas denied\b",
    r"\bdid not get the\b", r"\breceived no formal\b", r"\bwere not invited\b",
    r"\bwas not invited\b", r"\bwas turned away\b", r"\bwas closed\b",
    r"\bwas set aside\b", r"\bwas held back\b", r"\bwas detained\b",
]

SPOONFEED_MARKERS_EN = [
    r"\brefused to\b", r"\brejected\b", r"\bdenied\b", r"\bexcluded\b",
    r"\bcrossed out\b", r"\bremoved\b", r"\bturned away\b", r"\bpassed over\b",
    r"\bskipped\b", r"\bclosed .* application\b", r"\bexplicitly invited\b",
    r"\bwithout checking\b", r"\bwithout answering\b"
]

STIFF_BEN_WORDS = [
    "উক্ত", "অবহিত", "দাখিল", "প্রদান করেন", "ব্যর্থ হন", "সংশ্লিষ্ট", "পরিলক্ষিত",
    "বিবেচনাধীন", "অনুধাবন", "সম্পাদন করেন", "মূল্যায়ন", "সাক্ষাৎকার", "ব্যবস্থাপক",
    "সনদ", "বিজ্ঞপ্তি", "কর্মশালা", "প্রথমজন", "দ্বিতীয়জন", "মাঠপর্যায়ের"
]


def load_jsonl(path: Path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def get_v1_path(cat: str, lang: str, fname: str) -> Path:
    if cat == "PhysicalAppearance":
        return PA_CANON_DIR / f"BanglaBBQ_{lang}_PhysicalAppearance.jsonl"
    return V1_DIR / fname


def extract_s3(ambig_ctx: str, disambig_ctx: str) -> str:
    if disambig_ctx.startswith(ambig_ctx):
        return disambig_ctx[len(ambig_ctx):].strip()
    # fallback: common prefix
    i = 0
    limit = min(len(ambig_ctx), len(disambig_ctx))
    while i < limit and ambig_ctx[i] == disambig_ctx[i]:
        i += 1
    return disambig_ctx[i:].strip()


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


def classify_en_question(q: str) -> str:
    ql = q.lower()
    has_social = any(re.search(p, ql) for p in SOCIAL_BIAS_PATTERNS_EN)
    has_incident = any(re.search(p, ql) for p in INCIDENT_LOOKUP_PATTERNS_EN)
    if has_social and not has_incident:
        return "SOCIAL_BIAS_FOCUSED"
    if has_incident and not has_social:
        return "INCIDENT_LOOKUP"
    if has_social and has_incident:
        return "MIXED_BORDERLINE"
    return "OTHER_REVIEW"


def main():
    q_audit_rows = []
    q_consistency_rows = []
    s3_audit_rows = []
    bilingual_rows = []

    summary_stats = defaultdict(lambda: Counter())

    for cat, eng_fn, ben_fn in CATEGORIES:
        v2_eng = load_jsonl(V2_DIR / eng_fn)
        v2_ben = load_jsonl(V2_DIR / ben_fn)
        v1_eng = load_jsonl(get_v1_path(cat, "ENG", eng_fn))
        v1_ben = load_jsonl(get_v1_path(cat, "BEN", ben_fn))

        # Group by question_index
        by_qi_v2_eng = defaultdict(list)
        by_qi_v2_ben = defaultdict(list)
        by_qi_v1_eng = defaultdict(list)
        by_qi_v1_ben = defaultdict(list)

        for r in v2_eng: by_qi_v2_eng[str(r["question_index"])].append(r)
        for r in v2_ben: by_qi_v2_ben[str(r["question_index"])].append(r)
        for r in v1_eng: by_qi_v1_eng[str(r["question_index"])].append(r)
        for r in v1_ben: by_qi_v1_ben[str(r["question_index"])].append(r)

        qis = sorted(by_qi_v2_eng.keys(), key=lambda x: int(x) if x.isdigit() else 9999)

        for qi in qis:
            summary_stats[cat]["total_q_families"] += 1
            recs_e = by_qi_v2_eng[qi]
            recs_b = by_qi_v2_ben[qi]
            v1_e = by_qi_v1_eng[qi]
            v1_b = by_qi_v1_ben[qi]

            # Check question consistency between ambig & disambig for neg and nonneg
            # Both at 48-row scenario-family level (exact pairwise ambig==disambig) and 144-row question_index level
            for pol in ("neg", "nonneg"):
                amb_list_e = [r["question"] for r in recs_e if r["context_condition"] == "ambig" and r["question_polarity"] == pol]
                dis_list_e = [r["question"] for r in recs_e if r["context_condition"] == "disambig" and r["question_polarity"] == pol]
                amb_list_b = [r["question"] for r in recs_b if r["context_condition"] == "ambig" and r["question_polarity"] == pol]
                dis_list_b = [r["question"] for r in recs_b if r["context_condition"] == "disambig" and r["question_polarity"] == pol]

                pairwise_same_e = (amb_list_e == dis_list_e and len(amb_list_e) > 0)
                pairwise_same_b = (amb_list_b == dis_list_b and len(amb_list_b) > 0)
                amb_q_e = set(amb_list_e)
                dis_q_e = set(dis_list_e)
                amb_q_b = set(amb_list_b)
                dis_q_b = set(dis_list_b)

                v1_q_e = next(iter({r["question"] for r in v1_e if r["question_polarity"] == pol}), "")
                v1_q_b = next(iter({r["question"] for r in v1_b if r["question_polarity"] == pol}), "")
                v2_q_e = next(iter(dis_q_e), "")
                v2_q_b = next(iter(dis_q_b), "")

                rewritten_e = (set(r["question"] for r in v1_e if r["question_polarity"] == pol) != dis_q_e)
                rewritten_b = (set(r["question"] for r in v1_b if r["question_polarity"] == pol) != dis_q_b)
                q_style = classify_en_question(v2_q_e)

                q_consistency_rows.append([
                    cat, qi, pol, pairwise_same_e, pairwise_same_b, len(amb_q_e), len(dis_q_e), len(amb_q_b), len(dis_q_b),
                    "PASS" if (pairwise_same_e and pairwise_same_b) else "FAIL"
                ])

                q_audit_rows.append([
                    cat, qi, pol, rewritten_e, rewritten_b, q_style,
                    v1_q_e, v2_q_e, v1_q_b, v2_q_b
                ])

                if pol == "neg":
                    if rewritten_e:
                        summary_stats[cat]["rewritten_families"] += 1
                    else:
                        summary_stats[cat]["unchanged_families"] += 1
                    summary_stats[cat][f"style_{q_style}"] += 1

            # Inspect distinct scenario variations inside this question_index (by 24-row orientation blocks, or 48-row families)
            # Group by ambig context in ENG (each unique ambig context = 1 orientation of a variation)
            for idx_start in range(0, len(recs_e), 24):
                blk_e = recs_e[idx_start:idx_start+24]
                blk_b = recs_b[idx_start:idx_start+24]
                v1_blk_e = v1_e[idx_start:idx_start+24]
                v1_blk_b = v1_b[idx_start:idx_start+24]

                amb_e = next(r for r in blk_e if r["context_condition"] == "ambig")
                dis_e = next(r for r in blk_e if r["context_condition"] == "disambig")
                amb_b = next(r for r in blk_b if r["context_condition"] == "ambig")
                dis_b = next(r for r in blk_b if r["context_condition"] == "disambig")
                v1_dis_e = next(r for r in v1_blk_e if r["context_condition"] == "disambig")
                v1_dis_b = next(r for r in v1_blk_b if r["context_condition"] == "disambig")

                s3_e = extract_s3(amb_e["context"], dis_e["context"])
                s3_b = extract_s3(amb_b["context"], dis_b["context"])
                s3_changed_e = (v1_dis_e["context"] != dis_e["context"])
                s3_changed_b = (v1_dis_b["context"] != dis_b["context"])

                neg_q_e = next(r["question"] for r in blk_e if r["context_condition"] == "disambig" and r["question_polarity"] == "neg")
                nonneg_q_e = next(r["question"] for r in blk_e if r["context_condition"] == "disambig" and r["question_polarity"] == "nonneg")
                neg_q_b = next(r["question"] for r in blk_b if r["context_condition"] == "disambig" and r["question_polarity"] == "neg")
                nonneg_q_b = next(r["question"] for r in blk_b if r["context_condition"] == "disambig" and r["question_polarity"] == "nonneg")

                ov_neg_e = ngram_overlap(s3_e, neg_q_e, 3)
                ov_nonneg_e = ngram_overlap(s3_e, nonneg_q_e, 3)
                ov_neg_b = ngram_overlap(s3_b, neg_q_b, 3)
                ov_nonneg_b = ngram_overlap(s3_b, nonneg_q_b, 3)

                spoonfeed_hits = [p for p in SPOONFEED_MARKERS_EN if re.search(p, s3_e.lower())]
                stiff_hits = [w for w in STIFF_BEN_WORDS if w in dis_b["context"] or w in neg_q_b or w in nonneg_q_b]

                gold_neg_e = dis_e[f"ans{dis_e['label']}"]
                gold_neg_b = dis_b[f"ans{dis_b['label']}"]

                # Also grab nonneg disambig gold
                dis_nonneg_e = next(r for r in blk_e if r["context_condition"] == "disambig" and r["question_polarity"] == "nonneg")
                dis_nonneg_b = next(r for r in blk_b if r["context_condition"] == "disambig" and r["question_polarity"] == "nonneg")
                gold_nonneg_e = dis_nonneg_e[f"ans{dis_nonneg_e['label']}"]
                gold_nonneg_b = dis_nonneg_b[f"ans{dis_nonneg_b['label']}"]

                block_num = idx_start // 24 + 1
                s3_audit_rows.append([
                    cat, qi, block_num, dis_e["example_id"],
                    s3_changed_e, s3_changed_b,
                    len(ov_neg_e) + len(ov_nonneg_e), len(ov_neg_b) + len(ov_nonneg_b),
                    "; ".join(ov_neg_e + ov_nonneg_e), "; ".join(ov_neg_b + ov_nonneg_b),
                    "; ".join(spoonfeed_hits),
                    gold_neg_e, gold_nonneg_e,
                    s3_e, s3_b
                ])

                bilingual_rows.append([
                    cat, qi, block_num, dis_e["example_id"],
                    dis_e["label"] == dis_b["label"],
                    len(stiff_hits), "; ".join(stiff_hits),
                    neg_q_e, neg_q_b, s3_e, s3_b
                ])

    with open(OUT_DIR / "question_rewrite_audit.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "polarity", "rewritten_eng", "rewritten_ben", "eng_style_class", "v1_eng_question", "v2_eng_question", "v1_ben_question", "v2_ben_question"])
        w.writerows(q_audit_rows)

    with open(OUT_DIR / "question_family_consistency.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "polarity", "same_amb_dis_eng", "same_amb_dis_ben", "n_amb_eng", "n_dis_eng", "n_amb_ben", "n_dis_ben", "status"])
        w.writerows(q_consistency_rows)

    with open(OUT_DIR / "sentence3_entailment_audit.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "orientation_block", "sample_eid", "s3_changed_eng", "s3_changed_ben", "ngram3_overlap_eng_count", "ngram3_overlap_ben_count", "ngram3_overlap_eng", "ngram3_overlap_ben", "spoonfeed_markers_eng", "gold_neg_eng", "gold_nonneg_eng", "s3_eng", "s3_ben"])
        w.writerows(s3_audit_rows)

    with open(OUT_DIR / "bilingual_alignment_audit.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "question_index", "orientation_block", "sample_eid", "label_parity", "stiff_ben_word_count", "stiff_ben_words", "neg_q_eng", "neg_q_ben", "s3_eng", "s3_ben"])
        w.writerows(bilingual_rows)

    print("=== QUESTION REWRITE SUMMARY BY CATEGORY ===")
    for cat, _, _ in CATEGORIES:
        st = summary_stats[cat]
        print(f"{cat:<22} | families={st['total_q_families']:<2} | rewritten={st['rewritten_families']:<2} | unchanged={st['unchanged_families']:<2} | social_bias={st['style_SOCIAL_BIAS_FOCUSED']:<2} | incident={st['style_INCIDENT_LOOKUP']:<2} | mixed={st['style_MIXED_BORDERLINE']:<2} | other={st['style_OTHER_REVIEW']:<2}")

    # Check consistency failures
    cons_fails = [r for r in q_consistency_rows if r[-1] != "PASS"]
    print(f"\nQuestion ambig/disambig consistency failures: {len(cons_fails)}")
    # Check label parity failures
    lbl_fails = [r for r in bilingual_rows if not r[4]]
    print(f"Bilingual label parity mismatches: {len(lbl_fails)}")
    # Check spoonfeed hits
    sp_hits = [r for r in s3_audit_rows if r[10]]
    print(f"Orientation blocks with explicit spoonfeed markers in S3: {len(sp_hits)} / {len(s3_audit_rows)}")
    # Check 3-gram overlap
    ov_e = [r for r in s3_audit_rows if r[6] > 0]
    ov_b = [r for r in s3_audit_rows if r[7] > 0]
    print(f"Orientation blocks with 3-gram overlap (ENG / BEN): {len(ov_e)} / {len(ov_b)}")
    # Check stiff ben words
    stiff_blocks = [r for r in bilingual_rows if r[5] > 0]
    print(f"Orientation blocks with stiff Bengali markers: {len(stiff_blocks)} / {len(bilingual_rows)}")


if __name__ == "__main__":
    main()
