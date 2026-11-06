import os, shutil, hashlib, json

PROMOTION_MAP = [
    # 1. Education
    (
        "review_artifacts/education_linguistic_audit_20261106/BanglaBBQ_ENG_Education_QA_fixed.jsonl",
        "review_artifacts/education_linguistic_audit_20261106/BanglaBBQ_BEN_Education_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_Education_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_Education_QA_fixed.jsonl",
        2880
    ),
    # 2. Ethnicity
    (
        "review_artifacts/ethnicity_linguistic_audit_20261106/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl",
        "review_artifacts/ethnicity_linguistic_audit_20261106/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_Ethnicity_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_Ethnicity_QA_fixed.jsonl",
        1440
    ),
    # 3. Health Status
    (
        "review_artifacts/health_status_linguistic_audit_20261106/BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl",
        "review_artifacts/health_status_linguistic_audit_20261106/BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_HealthStatus_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_HealthStatus_QA_fixed.jsonl",
        2880
    ),
    # 4. Marital Status
    (
        "review_artifacts/marital_status_linguistic_audit_20261106/BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl",
        "review_artifacts/marital_status_linguistic_audit_20261106/BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_MaritalStatus_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_MaritalStatus_QA_fixed.jsonl",
        2880
    ),
    # 5. Occupational Background
    (
        "review_artifacts/occupational_background_linguistic_audit_20261106/BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl",
        "review_artifacts/occupational_background_linguistic_audit_20261106/BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_OccupationalBackground_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_OccupationalBackground_QA_fixed.jsonl",
        2880
    ),
    # 6. Politics
    (
        "review_artifacts/politics_linguistic_audit_20261106/BanglaBBQ_ENG_Politics_QA_fixed.jsonl",
        "review_artifacts/politics_linguistic_audit_20261106/BanglaBBQ_BEN_Politics_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_Politics_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_Politics_QA_fixed.jsonl",
        2880
    ),
    # 7. Regional Affiliation
    (
        "review_artifacts/regional_affiliation_linguistic_audit_20261106/BanglaBBQ_ENG_Regional_QA_fixed.jsonl",
        "review_artifacts/regional_affiliation_linguistic_audit_20261106/BanglaBBQ_BEN_Regional_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_Regional_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_Regional_QA_fixed.jsonl",
        1440
    ),
    # 8. Religion
    (
        "review_artifacts/religion_linguistic_audit_20261106/BanglaBBQ_ENG_Religion_QA_fixed.jsonl",
        "review_artifacts/religion_linguistic_audit_20261106/BanglaBBQ_BEN_Religion_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_Religion_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_Religion_QA_fixed.jsonl",
        2880
    ),
    # 9. Social Status
    (
        "review_artifacts/social_status_linguistic_audit_20261106/BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl",
        "review_artifacts/social_status_linguistic_audit_20261106/BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl",
        "Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl",
        "fixed JsonL/BanglaBBQ_ENG_SocialStatus_QA_fixed.jsonl",
        "fixed JsonL/BanglaBBQ_BEN_SocialStatus_QA_fixed.jsonl",
        1440
    )
]

BACKUP_DIR = "backups/pre_production_promotion_20261106"
os.makedirs(BACKUP_DIR, exist_ok=True)

print("Stage 1: Backing up current production files...")
for item in PROMOTION_MAP:
    prod_eng = item[2]
    prod_ben = item[3]
    for p in [prod_eng, prod_ben]:
        if os.path.exists(p):
            rel_dest = os.path.join(BACKUP_DIR, os.path.basename(p))
            shutil.copyfile(p, rel_dest)
            print(f"  Backed up {p} -> {rel_dest}")

print("\nStage 2: Promoting audited files to Dataset_BanglaBBQ_New/ and fixed JsonL/...")
for item in PROMOTION_MAP:
    src_eng, src_ben, dst_eng, dst_ben, fixed_eng, fixed_ben, exp_rows = item
    
    # Verify src row counts
    with open(src_eng, 'r', encoding='utf-8') as f:
        e_lines = [line for line in f if line.strip()]
    with open(src_ben, 'r', encoding='utf-8') as f:
        b_lines = [line for line in f if line.strip()]
    assert len(e_lines) == exp_rows, f"Row count mismatch in {src_eng}"
    assert len(b_lines) == exp_rows, f"Row count mismatch in {src_ben}"
    
    # Copy to Dataset_BanglaBBQ_New
    shutil.copyfile(src_eng, dst_eng)
    shutil.copyfile(src_ben, dst_ben)
    print(f"  Promoted to {dst_eng} ({len(e_lines)} rows)")
    print(f"  Promoted to {dst_ben} ({len(b_lines)} rows)")
    
    # Copy to fixed JsonL
    shutil.copyfile(src_eng, fixed_eng)
    shutil.copyfile(src_ben, fixed_ben)
    print(f"  Synchronized {fixed_eng}")
    print(f"  Synchronized {fixed_ben}")

print("\nStage 3: Verifying Dataset_BanglaBBQ_New files post-promotion...")
for item in PROMOTION_MAP:
    dst_eng = item[2]
    dst_ben = item[3]
    exp = item[6]
    with open(dst_eng, 'r', encoding='utf-8') as f:
        e_count = sum(1 for line in f if line.strip())
    with open(dst_ben, 'r', encoding='utf-8') as f:
        b_count = sum(1 for line in f if line.strip())
    assert e_count == exp, f"Failed verification on {dst_eng}"
    assert b_count == exp, f"Failed verification on {dst_ben}"
    print(f"  VERIFIED {dst_eng}: {e_count} rows [✓]")
    print(f"  VERIFIED {dst_ben}: {b_count} rows [✓]")

print("\nAll 18 production files successfully promoted and verified!")

