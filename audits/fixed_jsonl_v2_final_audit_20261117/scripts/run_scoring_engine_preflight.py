import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.bbq_scoring_engine import load_sidecar_map, classify_record_prediction

V2_DIR = ROOT / "fixed jsonL v2"
sidecar_map = load_sidecar_map(ROOT / "metadata" / "sidecar_stereotype_target_map.json")

total = 0
errors = 0
for fn in sorted(V2_DIR.glob("*.jsonl")):
    rows = [json.loads(l) for l in fn.read_text(encoding="utf-8").splitlines() if l.strip()]
    for r in rows:
        total += 1
        try:
            classify_record_prediction(r, r["label"], sidecar_map)
        except Exception as e:
            errors += 1
            if errors <= 10:
                print(f"ERROR in {fn.name} EID {r.get('example_id')}: {e}")

print(f"Scoring Engine Preflight on V2: {total} records checked, {errors} errors.")
