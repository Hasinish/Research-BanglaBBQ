# QA handoff — 2026-10-28 — adversarial fixture integrity

## Fixed in this chat (REVIEW BRANCH ONLY)

Branch: `review/non-mental-health-repair-20261028`.

- Added `scripts/adversarial_integrity_gates.py` under this QA package: *actual* pair-level identity-swap validation, exact six-way permutation closure with correct label remapping, introduction-order shortcut check, and repeated-name/outcome correlation check.
- Replaced the four forced-success branches in `scripts/test_adversarial_validator.py` (F05, F09, F10, F11) with calls to the actual gate methods, in BOTH English and Bengali.
- The runner now rejects a fixture only if the validator actually rejects it **with the expected error code**.
- Added eight positive controls (valid EN/BN counterfactual pairs, six-way blocks, position-balanced examples, and name-balanced examples).
- Re-fetched both committed GitHub files and checked they contain no `is_rejected = True` forced-success instruction.
- A separately executed local reproduction of the fixture/gate checks passed 13/13 adversarial fixtures and 10 known-good controls. **This is not a remote execution of the updated exact GitHub runner**, and MUST NOT be presented as one.

Review commits: `5a1d0d783127e1fa9fa3adbcde079f9e749ceb62` (gate), `a575eac62bb56d1d58fd4936c289c0c43db3ae35` (runner).

## Verification needed before closing this issue

From the repo root on the latest review branch, run:

```bash
python local_candidates/non_mental_health_repair_20261028/scripts/test_adversarial_validator.py
```

Demand 13/13 real rejections, eight accepted positive controls, process exit 0. Treat failure as FAILED, and repair it **without adding simulated PASS**. Also run mutation tests where valid fixtures are deliberately altered; require the expected specific failure reason. Do NOT count an `UNRESOLVED_*` gate as proof of a defect. For name and positional audits, check the number and quality of independent contexts, not six answer permutations of one context. Do not assume the name-based heuristic detects all demographic shortcuts.

## Still open (not addressed in this chat)

1. The full semantic validator still guesses `c0` or `c1` on insufficient linguistic evidence. Replace with `UNRESOLVED` and adjudicate all 138 flags using independently checked bilingual meaning.
2. Independently verify all 70 source themes. Five unsupported and two historical-only in previous handoff; verify against source text and date.
3. Human Bengali QA and the 53-entry queue; cross-check with all 138 flagged cases and Ethnicity community naming review.
4. Compare all eight candidate JSONLs with current production for roles, labels, 15 fields, gold choices, six-way blocks, counterfactuals, full semantic equivalence, and residual shortcuts.
5. Reconcile and integrate only verified approved candidate changes, protecting all Q11–Q20 parallel expansions.
6. Production JSONLs and Google Sheets have NOT been edited here. Do not promote this review branch or claim publication readiness.

## Important limitations

The new checker enforces **literal identity-only swaps** for matched templates. Legitimate paraphrased counterfactuals require human adjudication: strict rejection is NOT a semantic error verdict. The shortcut checks recognize standalone participant names and require at least four distinct scenarios; they do not establish complete absence of bias. The original independent semantic validator remains imperfect; existing non-special F01–F04/F06–F08/F12–F13 tests require careful local execution.

Next action: execute the exact committed runner; only after its verified PASS, close the four fake-pass test issue. Then start semantic validator repair as a separately scoped task.
