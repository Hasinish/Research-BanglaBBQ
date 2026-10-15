import json
import re
import sys
from scan_family_terms_sheets import eng_data, ben_data

sys.stdout.reconfigure(encoding='utf-8')

# Check if there are any hyphenated forms or case variations
regex_broad = re.compile(r'\b(grand[\s-]?ma|grand[\s-]?mother|grand[\s-]?pa|grand[\s-]?father)s?\b', re.IGNORECASE)

broad_matches = []
for idx, (er, br) in enumerate(zip(eng_data, ben_data)):
    e_full = " ".join(er[5:10]) # context, question, ans0, ans1, ans2
    m = regex_broad.findall(e_full)
    if m:
        broad_matches.append((idx + 2, er[1], er[14], m))

print(f"Broad regex matches count: {len(broad_matches)}")
q_indices = set(b[1] for b in broad_matches)
print(f"Question indices matched: {sorted(list(q_indices), key=lambda x: int(x))}")

# Now let's inspect how Q2, Q13, Q14, Q16, Q18 are currently translated in Bengali!
print("\nInspecting current Bengali translations for each template:")
for qi in sorted(list(q_indices), key=lambda x: int(x)):
    sample_er = next(er for er in eng_data if er[1] == qi)
    sample_br = next(br for br in ben_data if br[1] == qi)
    print(f"\n=================== TEMPLATE Q{qi} ===================")
    print("ENG Context sample:", sample_er[5][:100])
    print("ENG Question sample:", sample_er[6])
    print("ENG Ans0:", sample_er[7], "| Ans1:", sample_er[8], "| Ans2:", sample_er[9])
    print("BEN Context sample:", sample_br[5][:100])
    print("BEN Question sample:", sample_br[6])
    print("BEN Ans0:", sample_br[7], "| Ans1:", sample_br[8], "| Ans2:", sample_br[9])
