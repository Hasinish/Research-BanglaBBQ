# BanglaBBQ Production Integration & Handoff Plan

## 1. Purpose & Authority
This integration plan outlines the exact, step-by-step procedure required to promote candidate repairs from review branch `review/non-mental-health-repair-20261028` into canonical production (`Dataset_BanglaBBQ_New/`) and the live master Google Spreadsheet.

> [!CAUTION]
> **No automatic or unauthorized deployment is permitted.**
> Promotion to production requires explicit written authorization from the lead researcher (Hasin Ishrak) and verification against human review queues.

---

## 2. Pre-Integration Prerequisites
Before any candidate file is integrated, the following verification gates must be satisfied:
1. **Human Linguistic Sign-Off**:
   - Verification of all 53 items in `local_candidates/non_mental_health_repair_20261028/reports/bilingual_review_queue.csv`.
2. **Community Verification of Ethnicity Names**:
   - Validation of indigenous participant names across Munda, Chakma, Marma, Garo, Santal, Tripuri, Rakhine, Tanchangya, Khasia, and Manipuri themes.
3. **Source Replacement for Blocked Themes**:
   - Provision of empirical, non-satirical citations for Regional Q01/Q03/Q10 and Physical Appearance Q05/Q06.
4. **Git Workspace Cleanliness**:
   - All tests passing with zero unstaged changes.

---

## 3. Step-by-Step Production Deployment Procedure

### Phase 1: Cryptographic Backup of Production Baselines
Before touching production directories, generate and verify cryptographic backups of all canonical files:
```powershell
# 1. Create a timestamped backup directory
$backupDir = "backups/pre_repair_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force

# 2. Copy current production JSONLs
Copy-Item -Path "Dataset_BanglaBBQ_New/*" -Destination $backupDir -Recurse

# 3. Export SHA-256 baseline manifest
Get-FileHash -Algorithm SHA256 (Get-ChildItem -Path "Dataset_BanglaBBQ_New" -Recurse -Filter *.jsonl) | 
    Export-Csv -Path "$backupDir/production_baseline_hashes.csv" -NoTypeInformation
```

### Phase 2: Staged Candidate Promotion
Promote only the candidate categories that have achieved `CANDIDATE_READY_FOR_HUMAN_REVIEW` status and received explicit sign-off:

1. **Ethnicity** (`BanglaBBQ_Ethnicity`):
   - English: `local_candidates/non_mental_health_repair_20261028/candidates/BanglaBBQ_Ethnicity_repaired_english.jsonl` -> `Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_english.jsonl`
   - Bengali: `local_candidates/non_mental_health_repair_20261028/candidates/BanglaBBQ_Ethnicity_repaired_bengali.jsonl` -> `Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_Ethnicity_FINAL_bengali.jsonl`

2. **Health Status (Q01–Q10)** (`BanglaBBQ_HealthStatus`):
   - Note: Strictly preserve lines 1441–2880 reserved for Mental Health expansion (Q11–Q20).
   - English: Replace lines 1–1440 with candidate lines 1–1440.
   - Bengali: Replace lines 1–1440 with candidate lines 1–1440.

3. **Social Status** (`BanglaBBQ_SocialStatus`):
   - English: `local_candidates/non_mental_health_repair_20261028/candidates/BanglaBBQ_SocialStatus_repaired_english.jsonl` -> `Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_SocialStatus_FINAL_english.jsonl`
   - Bengali: `local_candidates/non_mental_health_repair_20261028/candidates/BanglaBBQ_SocialStatus_repaired_bengali.jsonl` -> `Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_SocialStatus_FINAL_bengali.jsonl`

4. **Regional Affiliation** (`BanglaBBQ_Regional`):
   - **HOLD** until Q01, Q03, and Q10 citations are replaced. Once approved, deploy candidate files.

### Phase 3: Post-Integration Regression Testing
Immediately after copying candidate files to production, execute the automated invariant validator against `Dataset_BanglaBBQ_New/`:
```powershell
python local_candidates/non_mental_health_repair_20261028/scripts/validate_repaired_candidates.py
```
**Acceptance Criteria**:
- 1,440 rows per file (or 2,880 for expanded files).
- Exact 15-key schema.
- Label distribution: 480 `ans0`, 480 `ans1`, 480 `ans2` (1:1:1).
- 60 blocks of complete 6-way answer permutations.
- 180 First / 180 Second (50.0% / 50.0%) introduction order balance on negative disambiguated conditions.

### Phase 4: Master Google Spreadsheet Synchronization
1. **Export Live Spreadsheet Backup**:
   - Download current live tabs as CSVs before updating.
2. **Targeted Tab Update**:
   - Update tab `577820949` (Health Status English) rows 2–1441.
   - Update tab `1261981579` (Health Status Bengali) rows 2–1441.
   - Update Ethnicity tabs.
   - Update Social Status tabs.
3. **Integrity Re-Verification**:
   - Confirm row counts match committed JSONLs exactly.

---

## 4. Rollback Plan
If any discrepancy, unexpected model degradation, or formatting issue is detected:
1. Revert production JSONLs using the cryptographic backup:
   ```powershell
   Copy-Item -Path "$backupDir/*" -Destination "Dataset_BanglaBBQ_New" -Recurse -Force
   ```
2. Verify SHA-256 hashes against `production_baseline_hashes.csv`.
3. Revert Git staging with `git restore Dataset_BanglaBBQ_New/`.
