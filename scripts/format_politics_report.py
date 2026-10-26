import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path

report_path = Path('docs/reports/politics_correction_report.json')
if not report_path.exists():
    report_path = Path('politics_correction_report.json')

with open(report_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== SUMMARY METRICS ===")
for k, v in d['summary'].items():
    print(f"  {k}: {v}")

print("\n=== LABEL FIXES ACROSS RAW 160 ROWS (40 records) ===")
by_q = {}
for l in d['label_fixes_all_raw']:
    by_q.setdefault(l['qi'], []).append(l)

for qi in sorted(by_q.keys()):
    print(f"\n--- Template Q{qi} ({len(by_q[qi])} label corrections) ---")
    for l in by_q[qi]:
        print(f"  Orig Sheet Row {l['orig_sheet_row']:3d} | Orig ID: {l['orig_id']:>3s} | {l['pol']:6s} | Old Label: {l['old_label']} -> New Label: {l['new_label']} | Target: {l['target_answer_eng']} / {l['target_answer_ben']}")

print("\n=== DUPLICATE RECORDS REMOVED (40 records) ===")
by_q_dup = {}
for dup in d['duplicates_removed']:
    by_q_dup.setdefault(dup['qi'], []).append(dup)

for qi in sorted(by_q_dup.keys()):
    print(f"\n--- Template Q{qi} ({len(by_q_dup[qi])} duplicates removed) ---")
    for dup in by_q_dup[qi]:
        print(f"  Orig Sheet Row {dup['orig_sheet_row']:3d} | Orig ID: {dup['orig_id']:>3s} | {dup['cond']:8s} | {dup['pol']:6s}")

print("\n=== PRESERVED 120 UNIQUE RECORDS MAPPING (first 10 and last 10) ===")
for m in d['id_mappings'][:5] + d['id_mappings'][-5:]:
    print(f"  Orig ID: {m['orig_id']:>3s} => New ID: {m['new_id']:>3s} (New Sheet Row: {m['new_sheet_row']:3d}) | Q{m['qi']} {m['cond']:8s} {m['pol']:6s} | Label: {m['label']}")
