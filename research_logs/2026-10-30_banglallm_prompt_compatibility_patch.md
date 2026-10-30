# BanglaLLM historical completion prompt compatibility patch (2026-10-30)

**Status: CODE UPDATED — GPU VALIDATION PENDING.**

Old (uncertified) report: 80.79% English / 59.15% Bengali with plain completion prompt (Answer: ( / উত্তর: () and 5-token budget. Legacy bias scores were defective.

Current canonical report: 48.04% English / 0.00% Bengali and all 30,656 Bengali responses unparseable with chat-template prompts and 16 output tokens.

Root cause remains unverified because original raw outputs have not been inspected here. To test this hypothesis, a standalone runner restores the exact historical completion prompt and 5 output tokens but retains the corrected BBQ scorer. It uses a different checkpoint namespace and `experimental_benchmark_report` prefix so prior reports and all existing prediction chunks are preserved.

Run tests locally first: `python -m unittest discover -s tests -p 'test_eval_pipeline_offline.py'`.

Optional user-initiated GPU run: `modal run scripts/modal_eval_banglallm_legacy_completion_l40s.py`.

Inspect the existing Bengali raw responses on Modal before drawing causal conclusions. Do not claim corrected accuracy or replace data in the publication table until the new protocol is validated.
