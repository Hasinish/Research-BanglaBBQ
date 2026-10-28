"""Conservative, executable invariants for BanglaBBQ review candidates.

These audits do NOT prove natural-language entailment or cultural validity.
They return UNRESOLVED (not PASS) when supplied evidence is insufficient.
The unit of observation for shortcut audits is a distinct scenario, not a
six-way option permutation of the same scenario.
"""

from collections import Counter
from itertools import permutations
import re

UNKNOWN = {"cannot be determined", "unknown", "নির্ধারণ করা যায় না", "নির্ধারণ করা যায় না", "অজানা"}


def _result(errors, checked=0):
    return {"is_valid": not errors, "errors": errors, "checked": checked}


def _swap(text, left, right):
    if not isinstance(text, str) or not left or not right or left == right:
        raise ValueError("Two distinct non-empty identity strings are required")
    if left not in text or right not in text:
        raise ValueError("Both identity groups must occur in the source text")
    marker = "\u0000IDENTITY_SWAP\u0000"
    if marker in text:
        raise ValueError("Reserved token occurs in text")
    return text.replace(left, marker).replace(right, left).replace(marker, right)


class AdversarialIntegrityGates:
    """Independent, testable checks; no fixture names or gold overrides."""

    def validate_counterfactual_pair(self, original, swapped, group_a, group_b):
        """Counterfactual must differ *only* by the two stated identity strings.

        Strict template-level check. If genuine bilingual paraphrasing prevents
        literal comparison, route the pair to human review; never auto-pass.
        """
        errors = []
        for field in ("context", "question"):
            a, b = original.get(field), swapped.get(field)
            if field == "question" and a == b:
                continue
            try:
                expected = _swap(a, group_a, group_b)
            except (TypeError, ValueError):
                errors.append("UNRESOLVED_COUNTERFACTUAL_SWAP: " + field)
                continue
            if expected != b:
                errors.append("COUNTERFACTUAL_CONTEXT_MISMATCH: " + field)
        return _result(errors, 1)

    def validate_six_way_permutations(self, block):
        """Check exactly 3! permutations of identical scenario and gold text."""
        errors = []
        if len(block) != 6:
            errors.append(f"MISSING_PERMUTATION: expected=6 actual={len(block)}")
        if not block:
            return _result(errors, 0)
        seed = block[0]
        fields = ("context", "question", "context_condition", "question_polarity", "question_index")
        choices = tuple(seed.get(f"ans{i}") for i in range(3))
        if len(set(choices)) != 3:
            errors.append("PERMUTATION_OPTION_SET_INVALID")
            return _result(errors, 0)
        try:
            gold = choices[seed["label"]]
        except (IndexError, KeyError, TypeError):
            errors.append("PERMUTATION_GOLD_INVALID")
            return _result(errors, 0)
        observed = []
        for row in block:
            if any(row.get(f) != seed.get(f) for f in fields):
                errors.append("PERMUTATION_SCENARIO_MISMATCH")
            current = tuple(row.get(f"ans{i}") for i in range(3))
            if set(current) != set(choices) or len(set(current)) != 3:
                errors.append("PERMUTATION_OPTION_SET_INVALID")
            observed.append(current)
            label = row.get("label")
            if not isinstance(label, int) or label not in (0, 1, 2) or current[label] != gold:
                errors.append("PERMUTATION_LABEL_REMAP_INVALID")
        if set(observed) != set(permutations(choices)) or len(observed) != len(set(observed)):
            errors.append("MISSING_PERMUTATION: six distinct orders required")
        return _result(sorted(set(errors)), len(block))

    def _unique_negative_scenarios(self, records):
        seen = set()
        unique = []
        for row in records:
            if row.get("context_condition") != "disambig" or row.get("question_polarity") != "neg":
                continue
            key = (row.get("context"), row.get("question"))
            if key not in seen:
                unique.append(row)
                seen.add(key)
        return unique

    @staticmethod
    def _named_answers(record):
        """Conservative: accept standalone person names, not role descriptions."""
        answers = [record.get(f"ans{i}") for i in range(3)]
        people = []
        for i, ans in enumerate(answers):
            if not isinstance(ans, str) or ans.strip().lower() in UNKNOWN:
                continue
            clean = ans.strip()
            english_name = bool(re.fullmatch(r"[A-Z][a-z]+(?: [A-Z][a-z]+){0,2}", clean))
            bengali_name = bool(re.fullmatch(r"[\u0980-\u09ff]{2,}(?: [\u0980-\u09ff]{2,}){0,2}", clean))
            if english_name or bengali_name:
                people.append((i, clean))
        return people if len(people) == 2 else None

    def validate_position_shortcut(self, records, minimum_independent_scenarios=4):
        rows = self._unique_negative_scenarios(records)
        first_gold = []
        errors = []
        for row in rows:
            people = self._named_answers(row)
            if people is None:
                errors.append("UNRESOLVED_POSITIONAL_AUDIT: participant names unavailable")
                continue
            ctx = row.get("context", "")
            p0, p1 = people
            start0, start1 = ctx.find(p0[1]), ctx.find(p1[1])
            if start0 < 0 or start1 < 0 or start0 == start1:
                errors.append("UNRESOLVED_POSITIONAL_AUDIT: introduction order unavailable")
                continue
            first_idx = p0[0] if start0 < start1 else p1[0]
            if row.get("label") not in (p0[0], p1[0]):
                errors.append("UNRESOLVED_POSITIONAL_AUDIT: invalid gold answer")
                continue
            first_gold.append(row["label"] == first_idx)
        if len(first_gold) < minimum_independent_scenarios:
            errors.append("UNRESOLVED_POSITIONAL_AUDIT: too few independent scenarios")
        elif all(first_gold) or not any(first_gold):
            errors.append("POSITIONAL_SHORTCUT: all negative outcomes tied to one introduction position")
        return _result(sorted(set(errors)), len(first_gold))

    def validate_name_outcome_leakage(self, records, minimum_independent_scenarios=4):
        rows = self._unique_negative_scenarios(records)
        appearances = Counter()
        outcomes = Counter()
        errors = []
        for row in rows:
            people = self._named_answers(row)
            if people is None:
                errors.append("UNRESOLVED_NAME_LEAKAGE_AUDIT: participant names unavailable")
                continue
            for idx, name in people:
                appearances[name] += 1
                if row.get("label") == idx:
                    outcomes[name] += 1
            if row.get("label") not in [idx for idx, _ in people]:
                errors.append("UNRESOLVED_NAME_LEAKAGE_AUDIT: invalid gold answer")
        if len(rows) < minimum_independent_scenarios:
            errors.append("UNRESOLVED_NAME_LEAKAGE_AUDIT: too few independent scenarios")
        else:
            systematic = [name for name, n in appearances.items()
                          if n >= minimum_independent_scenarios and outcomes[name] in (0, n)]
            # In a valid matched contrast, at least one consistently selected or
            # never-selected repeated participant is an exploitable shortcut.
            if systematic:
                errors.append("NAME_OUTCOME_LEAKAGE: " + ", ".join(sorted(systematic)))
        return _result(sorted(set(errors)), len(rows))
