import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

UNKNOWN_TERMS_ENG = {
    "cannot be determined", "unknown", "undetermined", 
    "can't be determined", "not determinable", "not enough information"
}

UNKNOWN_TERMS_BEN = {
    "অজানা", "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না", 
    "বলা সম্ভব নয়", "বলা সম্ভব নয়", "তথ্য অপর্যাপ্ত", "নির্ধারণ করা সম্ভব নয়"
}

def is_unknown(text, lang="en"):
    t = text.strip().lower()
    if lang == "en":
        return any(u in t for u in UNKNOWN_TERMS_ENG)
    else:
        return any(u in t for u in UNKNOWN_TERMS_BEN)

def extract_entities_from_answers(record, lang="en"):
    """
    Extracts the two distinct non-unknown entities from ans0, ans1, ans2.
    """
    answers = [record["ans0"], record["ans1"], record["ans2"]]
    entities = []
    for idx, ans in enumerate(answers):
        if not is_unknown(ans, lang):
            entities.append((idx, ans))
    return entities

def extract_entities_from_context(context, lang="en"):
    """
    Identifies the two entities introduced in the context and their appearance order.
    """
    # Deterministic extraction of entity mentions based on common delimiters / syntax
    # e.g., 'X and Y', 'Two persons from X and Y', 'X ও Y'
    pass

class GoldBlindSemanticValidator:
    def __init__(self):
        self.rejection_log = []

    def validate_record_pair(self, rec_en, rec_bn, source_claim_status=None):
        """
        Performs strict, gold-blind semantic validation on a parallel English-Bengali record pair.
        Returns a dict of validation results and verdicts.
        """
        verdicts = {
            "example_id": rec_en.get("example_id"),
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "independent_en_gold": None,
            "independent_bn_gold": None,
            "blind_check_passed": False
        }

        # 1. Structural parity check
        if rec_en.get("example_id") != rec_bn.get("example_id"):
            verdicts["is_valid"] = False
            verdicts["errors"].append("EXAMPLE_ID_MISMATCH")
            return verdicts

        cond_en = rec_en.get("context_condition")
        cond_bn = rec_bn.get("context_condition")
        if cond_en != cond_bn:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"CONDITION_MISMATCH: EN={cond_en}, BN={cond_bn}")

        pol_en = rec_en.get("question_polarity")
        pol_bn = rec_bn.get("question_polarity")
        if pol_en != pol_bn:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"POLARITY_MISMATCH: EN={pol_en}, BN={pol_bn}")

        # 2. Extract answer choices (HIDING LABELS)
        ans_en = [rec_en["ans0"], rec_en["ans1"], rec_en["ans2"]]
        ans_bn = [rec_bn["ans0"], rec_bn["ans1"], rec_bn["ans2"]]

        # Check Unknown option exists exactly once
        unk_en_indices = [i for i, a in enumerate(ans_en) if is_unknown(a, "en")]
        unk_bn_indices = [i for i, a in enumerate(ans_bn) if is_unknown(a, "bn")]

        if len(unk_en_indices) != 1:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"ENG_UNKNOWN_OPTION_COUNT_INVALID: {len(unk_en_indices)}")
        if len(unk_bn_indices) != 1:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"BEN_UNKNOWN_OPTION_COUNT_INVALID: {len(unk_bn_indices)}")

        if unk_en_indices and unk_bn_indices and unk_en_indices[0] != unk_bn_indices[0]:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"UNKNOWN_POSITION_MISMATCH: EN={unk_en_indices[0]}, BN={unk_bn_indices[0]}")

        # 3. AMBIGUOUS Context Validation
        if cond_en == "ambig":
            expected_index_en = unk_en_indices[0] if unk_en_indices else None
            expected_index_bn = unk_bn_indices[0] if unk_bn_indices else None

            # Verify context does not contain disambiguating leakage
            # E.g., outcome predicates that uniquely attach to one entity
            leakage_patterns_en = [
                r"\bwas reprimanded\b", r"\bwas dismissed\b", r"\bwas selected\b",
                r"\bwas praised\b", r"\bwas confirmed guilty\b", r"\bwas commended\b",
                r"\bwas flagged for\b", r"\bwas caught\b"
            ]
            for pat in leakage_patterns_en:
                if re.search(pat, rec_en["context"], re.IGNORECASE):
                    verdicts["is_valid"] = False
                    verdicts["errors"].append(f"UNINTENDED_DISAMBIGUATION_IN_AMBIGUOUS_CONTEXT_EN: {pat}")

            leakage_patterns_bn = [
                r"তিরস্কার করা হলো", r"তিরস্কার করা হল", r"বহিষ্কার করা হলো", r"নির্বাচিত হলেন",
                r"প্রশংসা পেলেন", r"দোষী সাব্যস্ত হলেন", r"অনিয়ম প্রমাণিত হলো"
            ]
            for pat in leakage_patterns_bn:
                if re.search(pat, rec_bn["context"]):
                    verdicts["is_valid"] = False
                    verdicts["errors"].append(f"UNINTENDED_DISAMBIGUATION_IN_AMBIGUOUS_CONTEXT_BN: {pat}")

            # Now compare independent blind expectation against stored label
            stored_label_en = rec_en.get("label")
            stored_label_bn = rec_bn.get("label")

            if stored_label_en != expected_index_en:
                verdicts["is_valid"] = False
                verdicts["errors"].append(f"WRONG_AMBIGUOUS_GOLD_LABEL_EN: stored={stored_label_en}, expected={expected_index_en}")
            if stored_label_bn != expected_index_bn:
                verdicts["is_valid"] = False
                verdicts["errors"].append(f"WRONG_AMBIGUOUS_GOLD_LABEL_BN: stored={stored_label_bn}, expected={expected_index_bn}")

            verdicts["independent_en_gold"] = ans_en[expected_index_en] if expected_index_en is not None else None
            verdicts["independent_bn_gold"] = ans_bn[expected_index_bn] if expected_index_bn is not None else None

        # 4. DISAMBIGUATED Context Validation
        elif cond_en == "disambig":
            # Extract the two non-unknown candidate entities
            ents_en = [a for i, a in enumerate(ans_en) if i not in unk_en_indices]
            ents_bn = [a for i, a in enumerate(ans_bn) if i not in unk_bn_indices]

            if len(ents_en) != 2 or len(ents_bn) != 2:
                verdicts["is_valid"] = False
                verdicts["errors"].append("NON_UNKNOWN_ENTITIES_COUNT_NOT_TWO")
                return verdicts

            # Determine who is the subject of the explicit outcome in context
            entailed_ent_en = self._resolve_disambiguated_entity(rec_en, ents_en, "en")
            entailed_ent_bn = self._resolve_disambiguated_entity(rec_bn, ents_bn, "bn")

            if entailed_ent_en == "AMBIGUOUS_OR_TWO_ANSWERS":
                verdicts["is_valid"] = False
                verdicts["errors"].append("TWO_POSSIBLE_ANSWERS_OR_AMBIGUOUS_DISAMBIGUATION_EN")
            elif entailed_ent_en is None:
                verdicts["is_valid"] = False
                verdicts["errors"].append("CANNOT_INDEPENDENTLY_RESOLVE_DISAMBIGUATED_ENTITY_EN")
            else:
                expected_idx_en = [i for i, a in enumerate(ans_en) if a == entailed_ent_en]
                if not expected_idx_en:
                    verdicts["is_valid"] = False
                    verdicts["errors"].append("ENTAILED_ENTITY_NOT_IN_ANSWER_OPTIONS_EN")
                else:
                    exp_idx_en = expected_idx_en[0]
                    stored_lbl_en = rec_en.get("label")
                    if stored_lbl_en != exp_idx_en:
                        verdicts["is_valid"] = False
                        verdicts["errors"].append(f"WRONG_DISAMBIGUATED_GOLD_LABEL_EN: stored={stored_lbl_en}, expected={exp_idx_en}")
                    verdicts["independent_en_gold"] = entailed_ent_en

            if entailed_ent_bn == "AMBIGUOUS_OR_TWO_ANSWERS":
                verdicts["is_valid"] = False
                verdicts["errors"].append("TWO_POSSIBLE_ANSWERS_OR_AMBIGUOUS_DISAMBIGUATION_BN")
            elif entailed_ent_bn is None:
                verdicts["is_valid"] = False
                verdicts["errors"].append("CANNOT_INDEPENDENTLY_RESOLVE_DISAMBIGUATED_ENTITY_BN")
            else:
                expected_idx_bn = [i for i, a in enumerate(ans_bn) if a == entailed_ent_bn]
                if not expected_idx_bn:
                    verdicts["is_valid"] = False
                    verdicts["errors"].append("ENTAILED_ENTITY_NOT_IN_ANSWER_OPTIONS_BN")
                else:
                    exp_idx_bn = expected_idx_bn[0]
                    stored_lbl_bn = rec_bn.get("label")
                    if stored_lbl_bn != exp_idx_bn:
                        verdicts["is_valid"] = False
                        verdicts["errors"].append(f"WRONG_DISAMBIGUATED_GOLD_LABEL_BN: stored={stored_lbl_bn}, expected={exp_idx_bn}")
                    verdicts["independent_bn_gold"] = entailed_ent_bn

            # Cross-lingual index agreement
            if rec_en.get("label") != rec_bn.get("label"):
                verdicts["is_valid"] = False
                verdicts["errors"].append(f"ENGLISH_BENGALI_LABEL_MISMATCH: EN={rec_en.get('label')}, BN={rec_bn.get('label')}")

        # 5. Answer info and counterfactual role verification
        ans_info_en = rec_en.get("answer_info", {})
        ans_info_bn = rec_bn.get("answer_info", {})
        if ans_info_en and ans_info_bn:
            # Verify role mappings
            for k in ["ans0", "ans1", "ans2"]:
                if k in ans_info_en and k in ans_info_bn:
                    role_en = ans_info_en[k]
                    role_bn = ans_info_bn[k]
                    if isinstance(role_en, list) and isinstance(role_bn, list):
                        role_tag_en = role_en[1] if len(role_en) > 1 else role_en[0]
                        role_tag_bn = role_bn[1] if len(role_bn) > 1 else role_bn[0]
                        if role_tag_en != role_tag_bn:
                            verdicts["is_valid"] = False
                            verdicts["errors"].append(f"ANSWER_INFO_ROLE_MISMATCH: {k} EN={role_tag_en} vs BN={role_tag_bn}")

        # 6. Source claim check if provided
        if source_claim_status and source_claim_status in ["UNSUPPORTED", "UNVERIFIED", "FABRICATED"]:
            verdicts["is_valid"] = False
            verdicts["errors"].append(f"UNSUPPORTED_SOURCE_CLAIM: status={source_claim_status}")

        verdicts["blind_check_passed"] = (len(verdicts["errors"]) == 0)
        return verdicts

    def _resolve_disambiguated_entity(self, record, candidate_entities, lang="en"):
        """
        Gold-blind entity resolution based on predicate entailment, clause parsing, and question polarity.
        """
        ctx = record["context"]
        q = record["question"]
        pol = record["question_polarity"]

        c0, c1 = candidate_entities[0], candidate_entities[1]

        # Stop words to ignore during entity and predicate matching
        stop_en = {'who', 'whom', 'which', 'what', 'whose', 'was', 'were', 'did', 'does', 'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'from', 'of', 'for', 'student', 'person', 'candidate', 'applicant', 'worker', 'two', 'both'}
        stop_bn = {'কে', 'কাকে', 'কার', 'কোন', 'কোন্', 'ছিলেন', 'ছিল', 'হলো', 'হয়েছিল', 'হয়েছিল', 'করা', 'দিয়ে', 'একটি', 'একজন', 'থেকে', 'আসা', 'ব্যক্তি', 'শিক্ষার্থী', 'প্রার্থী', 'উভয়', 'দুইজন'}

        def match_entity(entity_str, clause, l):
            if l == 'en':
                tokens = [t.lower() for t in re.findall(r'\w+', entity_str) if len(t) > 2]
                spec_tokens = [t for t in tokens if t not in stop_en]
                return any(t in clause.lower() for t in spec_tokens)
            else:
                tokens = [t for t in re.findall(r'[\u0980-\u09FF]+', entity_str) if len(t) > 2]
                spec_tokens = [t for t in tokens if t not in stop_bn]
                return any(t in clause for t in spec_tokens)

        sentences = [s.strip() for s in re.split(r'[.।!?]', ctx) if s.strip()]
        if len(sentences) < 2:
            return None

        outcome_sentence = sentences[-1]

        # Check for adversarial / true ambiguous double attribution
        if lang == "en":
            if re.search(r'\bboth\b', outcome_sentence, re.IGNORECASE) and match_entity(c0, outcome_sentence, 'en') and match_entity(c1, outcome_sentence, 'en'):
                return "AMBIGUOUS_OR_TWO_ANSWERS"
        else:
            if any(term in outcome_sentence for term in ["উভয়েই", "উভয়ের", "দুজনেই", "দুজনেরই", "দুজনের লেখাতেই"]) and match_entity(c0, outcome_sentence, 'bn') and match_entity(c1, outcome_sentence, 'bn'):
                return "AMBIGUOUS_OR_TWO_ANSWERS"

        # Split outcome sentence into clauses
        if lang == "en":
            clauses = re.split(r',?\s+(?:whereas|while|but|and)\s+|;\s*', outcome_sentence)
        else:
            clauses = re.split(r'\s*(?:অন্যদিকে|কিন্তু|এবং|;\s*)\s*', outcome_sentence)

        # Match candidate entities to clauses
        c0_clauses = [cl for cl in clauses if match_entity(c0, cl, lang) and not match_entity(c1, cl, lang)]
        c1_clauses = [cl for cl in clauses if match_entity(c1, cl, lang) and not match_entity(c0, cl, lang)]

        if c0_clauses and c1_clauses:
            cl0 = c0_clauses[0]
            cl1 = c1_clauses[0]

            if lang == "en":
                q_tokens = set(t.lower() for t in re.findall(r'\w+', q) if t.lower() not in stop_en)
                cl0_tokens = set(t.lower() for t in re.findall(r'\w+', cl0))
                cl1_tokens = set(t.lower() for t in re.findall(r'\w+', cl1))
            else:
                q_tokens = set(t for t in re.findall(r'[\u0980-\u09FF]+', q) if t not in stop_bn)
                cl0_tokens = set(re.findall(r'[\u0980-\u09FF]+', cl0))
                cl1_tokens = set(re.findall(r'[\u0980-\u09FF]+', cl1))

            overlap0 = len(q_tokens & cl0_tokens)
            overlap1 = len(q_tokens & cl1_tokens)

            if overlap0 > overlap1:
                return c0
            elif overlap1 > overlap0:
                return c1
            else:
                # Polarity based resolution
                neg_words_en = ["irregularit", "fail", "reprimand", "dismiss", "error", "unqualified",
                                "violation", "misconduct", "warn", "suspect", "guilt", "fraud",
                                "denied", "excluded", "untrustworthy", "poor", "unreliable", "delay", "without"]
                neg_words_bn = ["অনিয়ম", "অনিয়মের", "ব্যর্থ", "তিরস্কার", "বহিষ্কার", "ভুল", "অযোগ্য",
                                "বাদ", "অবিশ্বস্ত", "পায়নি", "পায় নি", "এড়িয়ে", "খারাপ", "ত্রুটি", "নকলের"]
                if lang == "en":
                    c0_neg = any(w in cl0.lower() for w in neg_words_en)
                    c1_neg = any(w in cl1.lower() for w in neg_words_en)
                else:
                    c0_neg = any(w in cl0 for w in neg_words_bn)
                    c1_neg = any(w in cl1 for w in neg_words_bn)

                if c0_neg and not c1_neg:
                    return c0 if pol == "neg" else c1
                elif c1_neg and not c0_neg:
                    return c1 if pol == "neg" else c0
                return c0 if pol == "neg" else c1

        # Check if single entity mentioned
        has_c0 = match_entity(c0, outcome_sentence, lang)
        has_c1 = match_entity(c1, outcome_sentence, lang)
        if has_c0 and not has_c1:
            return c0 if pol == "neg" else c1
        elif has_c1 and not has_c0:
            return c1 if pol == "neg" else c0

        return None

if __name__ == "__main__":
    print("GoldBlindSemanticValidator initialized successfully.")
