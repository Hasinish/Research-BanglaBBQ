import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.bbq_scoring_engine import load_sidecar_map, classify_record_prediction

V21_DIR = ROOT / "fixed JsonL v2.1"
V2_DIR = ROOT / "fixed jsonL v2"
CANON_DIR = ROOT / "Dataset_BanglaBBQ_New"
BACKUP_LOCAL_DIR = ROOT / "backups" / "pre_v21_production_promotion_20261117" / "local_canonical"
AUDIT_V21_DIR = ROOT / "audits" / "fixed_jsonl_v21_repair_20261117"
PROMO_AUDIT_DIR = ROOT / "audits" / "v21_production_promotion_20261117"

MAPPING = [
    ("Education", "BanglaBBQ_ENG_Education_QA_fixed.jsonl", "BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl", 2880),
    ("Education", "BanglaBBQ_BEN_Education_QA_fixed.jsonl", "BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl", 2880),
    ("Ethnicity", "BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl", "BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl", 1440),
    ("Ethnicity", "BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl", "BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl", 1440),
    ("HealthStatus", "BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl", "BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl", 2880),
    ("HealthStatus", "BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl", "BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl", 2880),
    ("MaritalStatus", "BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl", "BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl", 2880),
    ("MaritalStatus", "BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl", "BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl", 2880),
    ("OccupationalBackground", "BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl", "BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl", 2880),
    ("OccupationalBackground", "BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl", "BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl", 2880),
    ("PhysicalAppearance", "BanglaBBQ_ENG_PhysicalAppearance_QA_fixed.jsonl", "BanglaBBQ_PhysicalAppearance/BanglaBBQ_ENG_PhysicalAppearance.jsonl", 1440),
    ("PhysicalAppearance", "BanglaBBQ_BEN_PhysicalAppearance_QA_fixed.jsonl", "BanglaBBQ_PhysicalAppearance/BanglaBBQ_BEN_PhysicalAppearance.jsonl", 1440),
    ("Politics", "BanglaBBQ_ENG_Politics_QA_fixed.jsonl", "BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl", 2880),
    ("Politics", "BanglaBBQ_BEN_Politics_QA_fixed.jsonl", "BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl", 2880),
    ("Regional", "BanglaBBQ_ENG_Regional_QA_fixed.jsonl", "BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl", 1440),
    ("Regional", "BanglaBBQ_BEN_Regional_QA_fixed.jsonl", "BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl", 1440),
    ("Religion", "BanglaBBQ_ENG_Religion_QA_fixed.jsonl", "BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl", 2880),
    ("Religion", "BanglaBBQ_BEN_Religion_QA_fixed.jsonl", "BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl", 2880),
    ("SocialStatus", "BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl", "BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl", 1440),
    ("SocialStatus", "BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl", "BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl", 1440),
]

UNTOUCHED_CANON = [
    "BanglaBBQ_Age/BanglaBBQ_ENG_Age.jsonl",
    "BanglaBBQ_Age/BanglaBBQ_BEN_Age.jsonl",
    "BanglaBBQ_Gender/BanglaBBQ_ENG_Gender.jsonl",
    "BanglaBBQ_Gender/BanglaBBQ_BEN_Gender.jsonl",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(p: Path) -> int:
    with open(p, "r", encoding="utf-8") as f:
        return sum(1 for l in f if l.strip())


def main():
    BACKUP_LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    PROMO_AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    # PHASE 1: Verify V2.1 candidates match audited SHA256_MANIFEST.json
    print("[*] Phase 1: Verifying V2.1 candidates against SHA256_MANIFEST.json...")
    manifest_v21 = json.loads((AUDIT_V21_DIR / "SHA256_MANIFEST.json").read_text(encoding="utf-8"))
    for cat, src_fn, dst_rel, exp_cnt in MAPPING:
        src_p = V21_DIR / src_fn
        assert src_p.exists(), f"Missing candidate: {src_p}"
        h_v21 = sha256_file(src_p)
        assert h_v21 == manifest_v21["files"][src_fn]["v21_sha256"], f"SHA mismatch on V2.1 candidate {src_fn}"
        assert count_lines(src_p) == exp_cnt, f"Line count mismatch on {src_fn}"
    print("    -> All 20 V2.1 source files match audited SHA-256 and expected counts [PASS]")

    # PHASE 3A: Backup existing local canonical datasets + record Age/Gender baseline hashes
    print("[*] Phase 3A: Backing up existing 20 local canonical JSONLs...")
    backup_manifest = {"promoted_targets": {}, "untouched_age_gender_before": {}}
    for cat, src_fn, dst_rel, exp_cnt in MAPPING:
        canon_p = CANON_DIR / dst_rel
        assert canon_p.exists(), f"Missing canonical file: {canon_p}"
        bak_p = BACKUP_LOCAL_DIR / dst_rel
        bak_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canon_p, bak_p)
        backup_manifest["promoted_targets"][dst_rel] = {
            "canonical_path": str(canon_p),
            "backup_path": str(bak_p),
            "sha256": sha256_file(bak_p),
            "bytes": bak_p.stat().st_size,
            "records": count_lines(bak_p),
        }

    for rel in UNTOUCHED_CANON:
        p = CANON_DIR / rel
        backup_manifest["untouched_age_gender_before"][rel] = {
            "sha256": sha256_file(p),
            "bytes": p.stat().st_size,
            "records": count_lines(p),
        }

    (BACKUP_LOCAL_DIR / "local_backup_manifest.json").write_text(json.dumps(backup_manifest, indent=2), encoding="utf-8")
    print("    -> Local canonical backup complete & hashed [PASS]")

    # PHASE 4: Exact byte copy promotion into Dataset_BanglaBBQ_New/
    print("[*] Phase 4: Promoting 20 V2.1 files into Dataset_BanglaBBQ_New/ (exact byte copy)...")
    promo_manifest = {"promoted_files": {}, "untouched_age_gender_after": {}, "scoring_engine_errors": 0}
    sidecar = load_sidecar_map(ROOT / "metadata" / "sidecar_stereotype_target_map.json")

    for cat, src_fn, dst_rel, exp_cnt in MAPPING:
        src_p = V21_DIR / src_fn
        dst_p = CANON_DIR / dst_rel
        shutil.copy2(src_p, dst_p)

        h_src = sha256_file(src_p)
        h_dst = sha256_file(dst_p)
        assert h_src == h_dst, f"Copy SHA mismatch: {src_p} -> {dst_p}"
        cnt_dst = count_lines(dst_p)
        assert cnt_dst == exp_cnt, f"Record count mismatch after copy: {dst_p}"

        # Validate scoring engine on promoted file
        with open(dst_p, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    try:
                        classify_record_prediction(r, r["label"], sidecar)
                    except Exception:
                        promo_manifest["scoring_engine_errors"] += 1

        promo_manifest["promoted_files"][dst_rel] = {
            "source_v21_file": src_fn,
            "v21_sha256": h_src,
            "canonical_sha256": h_dst,
            "bit_identical": True,
            "bytes": dst_p.stat().st_size,
            "records": cnt_dst,
        }

    # Verify Age & Gender untouched bit-for-bit
    for rel in UNTOUCHED_CANON:
        p = CANON_DIR / rel
        h_after = sha256_file(p)
        h_before = backup_manifest["untouched_age_gender_before"][rel]["sha256"]
        assert h_after == h_before, f"CRITICAL: Age/Gender file modified: {rel}"
        promo_manifest["untouched_age_gender_after"][rel] = {"sha256": h_after, "unchanged": True}

    assert promo_manifest["scoring_engine_errors"] == 0, "Scoring engine errors detected on promoted files!"
    (PROMO_AUDIT_DIR / "local_promotion_manifest.json").write_text(json.dumps(promo_manifest, indent=2), encoding="utf-8")
    print("    -> All 20 canonical JSONLs promoted with 100% SHA-256 parity, 0 scoring errors, Age/Gender unchanged [PASS]")


if __name__ == "__main__":
    main()
