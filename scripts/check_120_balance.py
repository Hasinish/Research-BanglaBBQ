import json
import sys
from analyze_politics_duplicates import eng_seen

sys.stdout.reconfigure(encoding='utf-8')

unique_records = [v['record'] for v in eng_seen.values()]

print(f"Total Unique Records: {len(unique_records)}")

# Breakdown by template
for qi in ['1', '2', '3', '4', '5']:
    q_recs = [r for r in unique_records if r[1] == qi]
    ambig_count = sum(1 for r in q_recs if r[2] == 'ambig')
    disambig_count = sum(1 for r in q_recs if r[2] == 'disambig')
    neg_count = sum(1 for r in q_recs if r[3] == 'neg')
    nonneg_count = sum(1 for r in q_recs if r[3] == 'nonneg')
    
    # Label counts
    labels = {}
    for r in q_recs:
        labels[r[10]] = labels.get(r[10], 0) + 1
        
    print(f"\nTemplate Q{qi} (Total: {len(q_recs)}):")
    print(f"  Condition: ambig={ambig_count}, disambig={disambig_count}")
    print(f"  Polarity:  neg={neg_count}, nonneg={nonneg_count}")
    print(f"  Labels:    {sorted(labels.items())}")

# Overall breakdown
total_ambig = sum(1 for r in unique_records if r[2] == 'ambig')
total_disambig = sum(1 for r in unique_records if r[2] == 'disambig')
total_neg = sum(1 for r in unique_records if r[3] == 'neg')
total_nonneg = sum(1 for r in unique_records if r[3] == 'nonneg')

print("\n" + "="*50)
print("OVERALL 120-RECORD BENCHMARK BALANCE:")
print(f"  Condition: ambig={total_ambig} (50%), disambig={total_disambig} (50%)")
print(f"  Polarity:  neg={total_neg} (50%), nonneg={total_nonneg} (50%)")
labels_all = {}
for r in unique_records:
    labels_all[r[10]] = labels_all.get(r[10], 0) + 1
print(f"  Labels:    {sorted(labels_all.items())}")
