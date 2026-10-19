# -*- coding: utf-8 -*-
"""Assemble canonical 2,880-record English and Bengali Educational Background datasets.
Generates:
  - BanglaBBQ_EducationalBackground/banglabbq_education_english.jsonl
  - BanglaBBQ_EducationalBackground/banglabbq_education_bengali.jsonl
  - BanglaBBQ_EducationalBackground/expansion_manifest.json
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "BanglaBBQ_EducationalBackground"
TEMPLATES_FILE = OUT_DIR / "scenario_templates.json"

with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
    tpl_data = json.load(f)

themes = tpl_data["themes"]

FIELDS = [
    "example_id", "question_index", "context_condition", "question_polarity",
    "type", "context", "question", "ans0", "ans1", "ans2", "label",
    "answer_info", "additional_metadata", "category", "id"
]

def make_records_for_theme_variant(qid, theme, variant, wave_idx, lang):
    vdata = theme[variant][lang]
    target_role = theme["target_role"]
    comp_role = theme["comp_role"]
    source = theme["source"]
    stereotyped_groups = theme["stereotyped_groups"]
    
    if lang == "en":
        target_name = theme["target_ans_en"]
        comp_name = theme["comp_ans_en"]
        unknown_name = "Unknown"
    else:
        target_name = theme["target_ans_bn"]
        comp_name = theme["comp_ans_bn"]
        unknown_name = "অজানা"
        
    records = []
    
    # Orientation 'a': entity1 = target, entity2 = comparison
    # 6 complete permutations (3!)
    perms_a = [
        [(target_name, target_role), (comp_name, comp_role), (unknown_name, "unknown")],
        [(target_name, target_role), (unknown_name, "unknown"), (comp_name, comp_role)],
        [(comp_name, comp_role), (target_name, target_role), (unknown_name, "unknown")],
        [(comp_name, comp_role), (unknown_name, "unknown"), (target_name, target_role)],
        [(unknown_name, "unknown"), (target_name, target_role), (comp_name, comp_role)],
        [(unknown_name, "unknown"), (comp_name, comp_role), (target_name, target_role)]
    ]
    
    for perm in perms_a:
        roles = [p[1] for p in perm]
        names = [p[0] for p in perm]
        
        # Row 0: ambig, neg
        meta0 = {
            "subcategory": "None",
            "stereotyped_groups": stereotyped_groups,
            "version": "a",
            "source": source
        }
        if variant != "v1":
            meta0["wording_variant"] = variant
            meta0["parent_example_id"] = None # set in assembler
            
        r0 = {
            "question_index": qid,
            "context_condition": "ambig",
            "question_polarity": "neg",
            "type": "NA",
            "context": vdata["ambig_a"],
            "question": vdata["neg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index("unknown"),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta0,
            "category": "EducationalBackground"
        }
        
        # Row 1: disambig, neg -> target is disadvantaged
        meta1 = dict(meta0)
        r1 = {
            "question_index": qid,
            "context_condition": "disambig",
            "question_polarity": "neg",
            "type": "NA",
            "context": vdata["disambig_a"],
            "question": vdata["neg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index(target_role),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta1,
            "category": "EducationalBackground"
        }
        
        # Row 2: ambig, nonneg
        meta2 = dict(meta0)
        r2 = {
            "question_index": qid,
            "context_condition": "ambig",
            "question_polarity": "nonneg",
            "type": "NA",
            "context": vdata["ambig_a"],
            "question": vdata["nonneg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index("unknown"),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta2,
            "category": "EducationalBackground"
        }
        
        # Row 3: disambig, nonneg -> comparison is advantaged
        meta3 = dict(meta0)
        r3 = {
            "question_index": qid,
            "context_condition": "disambig",
            "question_polarity": "nonneg",
            "type": "NA",
            "context": vdata["disambig_a"],
            "question": vdata["nonneg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index(comp_role),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta3,
            "category": "EducationalBackground"
        }
        records.extend([r0, r1, r2, r3])
        
    # Orientation 'b': entity1 = comparison, entity2 = target
    perms_b = [
        [(comp_name, comp_role), (target_name, target_role), (unknown_name, "unknown")],
        [(comp_name, comp_role), (unknown_name, "unknown"), (target_name, target_role)],
        [(target_name, target_role), (comp_name, comp_role), (unknown_name, "unknown")],
        [(target_name, target_role), (unknown_name, "unknown"), (comp_name, comp_role)],
        [(unknown_name, "unknown"), (comp_name, comp_role), (target_name, target_role)],
        [(unknown_name, "unknown"), (target_name, target_role), (comp_name, comp_role)]
    ]
    
    for perm in perms_b:
        roles = [p[1] for p in perm]
        names = [p[0] for p in perm]
        
        # Row 0: ambig, neg
        meta0 = {
            "subcategory": "None",
            "stereotyped_groups": stereotyped_groups,
            "version": "b",
            "source": source
        }
        if variant != "v1":
            meta0["wording_variant"] = variant
            meta0["parent_example_id"] = None
            
        r0 = {
            "question_index": qid,
            "context_condition": "ambig",
            "question_polarity": "neg",
            "type": "NA",
            "context": vdata["ambig_b"],
            "question": vdata["neg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index("unknown"),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta0,
            "category": "EducationalBackground"
        }
        
        # Row 1: disambig, neg -> comparison is disadvantaged
        meta1 = dict(meta0)
        r1 = {
            "question_index": qid,
            "context_condition": "disambig",
            "question_polarity": "neg",
            "type": "NA",
            "context": vdata["disambig_b"],
            "question": vdata["neg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index(comp_role),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta1,
            "category": "EducationalBackground"
        }
        
        # Row 2: ambig, nonneg
        meta2 = dict(meta0)
        r2 = {
            "question_index": qid,
            "context_condition": "ambig",
            "question_polarity": "nonneg",
            "type": "NA",
            "context": vdata["ambig_b"],
            "question": vdata["nonneg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index("unknown"),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta2,
            "category": "EducationalBackground"
        }
        
        # Row 3: disambig, nonneg -> target is advantaged
        meta3 = dict(meta0)
        r3 = {
            "question_index": qid,
            "context_condition": "disambig",
            "question_polarity": "nonneg",
            "type": "NA",
            "context": vdata["disambig_b"],
            "question": vdata["nonneg_q"],
            "ans0": names[0],
            "ans1": names[1],
            "ans2": names[2],
            "label": roles.index(target_role),
            "answer_info": {
                "ans0": [names[0], roles[0]],
                "ans1": [names[1], roles[1]],
                "ans2": [names[2], roles[2]]
            },
            "additional_metadata": meta3,
            "category": "EducationalBackground"
        }
        records.extend([r0, r1, r2, r3])
        
    return records


def assemble_language(lang):
    assembled = []
    current_eid = 0
    
    for wave_idx, variant in enumerate(["v1", "v2", "v3"]):
        for qid in range(1, 21):
            t = themes[str(qid)]
            batch = make_records_for_theme_variant(qid, t, variant, wave_idx, lang)
            for r in batch:
                r_full = {
                    "example_id": current_eid,
                    "question_index": r["question_index"],
                    "context_condition": r["context_condition"],
                    "question_polarity": r["question_polarity"],
                    "type": r["type"],
                    "context": r["context"],
                    "question": r["question"],
                    "ans0": r["ans0"],
                    "ans1": r["ans1"],
                    "ans2": r["ans2"],
                    "label": r["label"],
                    "answer_info": r["answer_info"],
                    "additional_metadata": r["additional_metadata"],
                    "category": r["category"],
                    "id": current_eid
                }
                if variant != "v1":
                    r_full["additional_metadata"]["parent_example_id"] = current_eid % 960
                assembled.append(r_full)
                current_eid += 1
                
    return assembled

print("Assembling English and Bengali datasets...")
eng_records = assemble_language("en")
ben_records = assemble_language("bn")

assert len(eng_records) == 2880, f"ENG count {len(eng_records)} != 2880"
assert len(ben_records) == 2880, f"BEN count {len(ben_records)} != 2880"

eng_path = OUT_DIR / "banglabbq_education_english.jsonl"
with open(eng_path, 'w', encoding='utf-8') as f:
    for r in eng_records:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f"Wrote 2,880 records to {eng_path}")

ben_path = OUT_DIR / "banglabbq_education_bengali.jsonl"
with open(ben_path, 'w', encoding='utf-8') as f:
    for r in ben_records:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f"Wrote 2,880 records to {ben_path}")

# Checksums
with open(eng_path, 'rb') as f:
    eng_sha = hashlib.sha256(f.read()).hexdigest()
with open(ben_path, 'rb') as f:
    ben_sha = hashlib.sha256(f.read()).hexdigest()

manifest = {
    "category": "EducationalBackground",
    "status": "VALIDATED_CANONICAL_WORKING_BENCHMARK",
    "generation_date": "2026-10-19",
    "schema_columns": FIELDS,
    "english_records": 2880,
    "bengali_records": 2880,
    "combined_records": 5760,
    "themes_count": 20,
    "records_per_theme_per_lang": 144,
    "variants_per_theme": 3,
    "records_per_variant_per_theme": 48,
    "label_distribution": {
        "0": 960,
        "1": 960,
        "2": 960
    },
    "condition_distribution": {
        "ambig": 1440,
        "disambig": 1440
    },
    "polarity_distribution": {
        "neg": 1440,
        "nonneg": 1440
    },
    "sha256_checksums": {
        "banglabbq_education_english.jsonl": eng_sha,
        "banglabbq_education_bengali.jsonl": ben_sha
    },
    "legacy_baselines_preserved": {
        "legacy_english_sha256": "d66b34ee1ef147ceec25a51f9e5cedd8569fd0eac6bfa48a4095125a4bc49ebd",
        "legacy_bengali_sha256": "ba308416a74e0dc070fb58f98d495fac7f4ef34a137680ec6a590eea94e319ee"
    }
}

manifest_path = OUT_DIR / "expansion_manifest.json"
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Wrote expansion manifest to: {manifest_path}")
print(f"ENG SHA256: {eng_sha}")
print(f"BEN SHA256: {ben_sha}")
