import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "scripts"))

from independent_semantic_validator import is_unknown, UNKNOWN_TERMS_ENG, UNKNOWN_TERMS_BEN

def get_core_identifier(entity_text, lang="en"):
    if lang == "en":
        if "from " in entity_text:
            return entity_text.split("from ")[-1].strip()
        words = entity_text.strip().split()
        return words[0] if words else entity_text
    else:
        if "থেকে আসা" in entity_text:
            return entity_text.split("থেকে আসা")[0].strip()
        words = entity_text.strip().split()
        return words[0] if words else entity_text

def resolve_disambiguated_entity(record, candidate_entities, lang="en"):
    ctx = record["context"]
    pol = record["question_polarity"]

    c0, c1 = candidate_entities[0], candidate_entities[1]
    id0 = get_core_identifier(c0, lang)
    id1 = get_core_identifier(c1, lang)

    sentences = [s.strip() for s in re.split(r'[.।!?]', ctx) if s.strip()]
    if len(sentences) < 2:
        return None

    outcome_sentence = sentences[-1]
    has_id0 = id0.lower() in outcome_sentence.lower() if id0 else False
    has_id1 = id1.lower() in outcome_sentence.lower() if id1 else False

    # Check for adversarial / true ambiguous double attribution
    if lang == "en":
        if re.search(r'\bboth\b', outcome_sentence, re.IGNORECASE) and has_id0 and has_id1:
            return "AMBIGUOUS_OR_TWO_ANSWERS"
    else:
        if any(term in outcome_sentence for term in ["উভয়েই", "উভয়ের", "দুজনেই", "দুজনেরই", "দুজনের লেখাতেই"]) and has_id0 and has_id1:
            return "AMBIGUOUS_OR_TWO_ANSWERS"

    # If both appear in outcome sentence, split into clauses
    if has_id0 and has_id1:
        if lang == "en":
            clauses = re.split(r',?\s+(?:whereas|while|but|and)\s+|;\s*', outcome_sentence)
        else:
            clauses = re.split(r'\s*(?:অন্যদিকে|কিন্তু|এবং|;\s*)\s*', outcome_sentence)

        c0_clause = None
        c1_clause = None
        for cl in clauses:
            in_0 = id0.lower() in cl.lower()
            in_1 = id1.lower() in cl.lower()
            if in_0 and not in_1:
                c0_clause = cl
            elif in_1 and not in_0:
                c1_clause = cl

        if c0_clause and c1_clause:
            # Check polarity of clauses
            neg_words_en = ["irregularit", "fail", "reprimand", "dismiss", "error", "unqualified",
                            "violation", "misconduct", "warn", "suspect", "guilt", "fraud",
                            "denied", "excluded", "untrustworthy", "poor", "unreliable", "delay", "without"]
            neg_words_bn = ["অনিয়ম", "অনিয়মের", "ব্যর্থ", "তিরস্কার", "বহিষ্কার", "ভুল", "অযোগ্য",
                            "বাদ", "অবিশ্বস্ত", "পায়নি", "পায় নি", "এড়িয়ে", "খারাপ", "ত্রুটি", "নকলের"]

            if lang == "en":
                c0_neg = any(w in c0_clause.lower() for w in neg_words_en)
                c1_neg = any(w in c1_clause.lower() for w in neg_words_en)
            else:
                c0_neg = any(w in c0_clause for w in neg_words_bn)
                c1_neg = any(w in c1_clause for w in neg_words_bn)

            if c0_neg and not c1_neg:
                return c0 if pol == "neg" else c1
            elif c1_neg and not c0_neg:
                return c1 if pol == "neg" else c0
            else:
                # If neither or both have explicit neg words, fall back to sentence order
                # In standard templates: first clause corresponds to the primary outcome of orientation
                return c0 if pol == "neg" else c1
        else:
            return "AMBIGUOUS_OR_TWO_ANSWERS"

    if has_id0 and not has_id1:
        return c0 if pol == "neg" else c1
    elif has_id1 and not has_id0:
        return c1 if pol == "neg" else c0
    else:
        return None

# Let's test this on our candidate files
CAND_DIR = os.path.join(REPO_ROOT, "local_candidates", "non_mental_health_repair_20261028", "candidates")
CANDIDATES = [
    ("Ethnicity", "BanglaBBQ_Ethnicity_repaired_english.jsonl", "BanglaBBQ_Ethnicity_repaired_bengali.jsonl"),
    ("Health Status", "BanglaBBQ_Health_Status_repaired_english.jsonl", "BanglaBBQ_Health_Status_repaired_bengali.jsonl"),
    ("Regional Affiliation", "BanglaBBQ_Regional_repaired_english.jsonl", "BanglaBBQ_Regional_repaired_bengali.jsonl"),
    ("Social Status", "BanglaBBQ_SocialStatus_repaired_english.jsonl", "BanglaBBQ_SocialStatus_repaired_bengali.jsonl"),
]

for cat, f_en, f_bn in CANDIDATES:
    p_en = os.path.join(CAND_DIR, f_en)
    p_bn = os.path.join(CAND_DIR, f_bn)
    with open(p_en, encoding='utf-8') as fe, open(p_bn, encoding='utf-8') as fb:
        recs_en = [json.loads(l) for l in fe]
        recs_bn = [json.loads(l) for l in fb]

    disambig_en_pass = 0
    disambig_bn_pass = 0
    total_disambig = 0
    for r_en, r_bn in zip(recs_en, recs_bn):
        if r_en["context_condition"] == "disambig":
            total_disambig += 1
            # EN
            ans_en = [r_en["ans0"], r_en["ans1"], r_en["ans2"]]
            cands_en = [a for a in ans_en if not is_unknown(a, "en")]
            ent_en = resolve_disambiguated_entity(r_en, cands_en, "en")
            if ent_en and ent_en in ans_en and ans_en.index(ent_en) == r_en["label"]:
                disambig_en_pass += 1

            # BN
            ans_bn = [r_bn["ans0"], r_bn["ans1"], r_bn["ans2"]]
            cands_bn = [a for a in ans_bn if not is_unknown(a, "bn")]
            ent_bn = resolve_disambiguated_entity(r_bn, cands_bn, "bn")
            if ent_bn and ent_bn in ans_bn and ans_bn.index(ent_bn) == r_bn["label"]:
                disambig_bn_pass += 1

    print(f"[{cat}] Disambiguated Accuracy: EN={disambig_en_pass}/{total_disambig} ({disambig_en_pass/total_disambig*100:.1f}%), BN={disambig_bn_pass}/{total_disambig} ({disambig_bn_pass/total_disambig*100:.1f}%)")
