# BanglaBBQ V2.1 Final Production Promotion Report

**Promotion Date**: 2026-11-17  
**Authorized Source**: `fixed JsonL v2.1/` (20 JSONLs, 46,080 records across 10 categories)  
**Audit Package**: `audits/v21_production_promotion_20261117/`  

---

## 1. Destination Readiness Matrix

| Destination | Required Verification | Outcome | Verified Evidence |
| :--- | :--- | :---: | :--- |
| **Local canonical datasets** (`Dataset_BanglaBBQ_New/`) | 20/20 SHA-256 matches | **PASS** | `local_promotion_manifest.json`: 20/20 files exact byte copy (`bit_identical: true`), 46,080 promoted records, 0 scoring errors, `test_all_61312_actual_records_mapping.py` 61,312/61,312 OK. |
| **Google Spreadsheet** (`1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`) | 20/20 worksheets, 691,200/691,200 data cells | **PASS** | `sheets_sync_verification_report.json`: **691,200 / 691,200** data cells read back & verified cell-for-cell (**0 mismatches**), headers & formatting & IDs preserved. |
| **Google Drive** (`1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe`) | 20/20 updated files, all 24 canonical verified | **PASS** | `scripts/sync_drive_dataset.py` + `--verify-only`: 20 files updated in-place preserving Drive IDs, **24 / 24** canonical files match MD5 & SHA-256 bit-for-bit. |
| **GitHub (`Hasinish/Research-BanglaBBQ` `main`)** | Successful main push and commit SHA | **PENDING PUSH** | To be finalized in Phase 7 commit `feat(dataset): promote BanglaBBQ V2.1 across 10 categories` and remote SHA-256 verification. |
| **Age and Gender Identity** | Zero unintended changes | **PASS** | Local SHA-256s unchanged (`true`), Sheets metadata unchanged (`true`), Drive MD5/SHA-256 untouched (`In-Sync 4/24` before upload). |
| **V2 and V2.1 Candidates (`fixed jsonL v2/`, `fixed JsonL v2.1/`, `fixed JsonL/`, `Dataset_ BanglaBBQ_Old/`)** | Original candidate files preserved | **PASS** | Untouched during promotion (`fixed JsonL v2.1/` SHA-256s match canonical byte-for-byte). |
| **Research Memory & Logs** | Updated and synchronized | **PASS** | Updated `memory/state.md`, `memory/history.md`, `research_logs/README.md`, `research_logs/2026-11-17_v21_production_promotion.md`. |
| **Human Native Bengali & Source Verification** | Independent human & external checks | **INCONCLUSIVE** | Benchmark is operationally synchronized but explicitly **NOT publication-ready** pending external native human review & live URL checks. |

---

## 2. Detailed Canonical File & Google Drive ID Parity Table

| Canonical Path | Records | Pre-Promo SHA-256 (prefix) | Promoted SHA-256 (prefix) | Local Parity | Google Drive ID |
| :--- | :---: | :--- | :--- | :---: | :--- |
| `Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl` | 2,880 | `2fdf05a428a04d6c...` | `36bf8425d61faf67...` | PASS (`== V2.1`) | `17ZAxExIseyuwBXOY6Okn_s4Tkg_JOvVb` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl` | 2,880 | `00d56efae76d45b9...` | `ac3693ef9bbf3454...` | PASS (`== V2.1`) | `1HG-QLziod0gcTozqpFl_IZsg8MrhDOlA` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl` | 1,440 | `536493d7f3b91b81...` | `555918dc09288aee...` | PASS (`== V2.1`) | `1HHbcrn7KmxJWyfORpMOwXxKljX8aedFF` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl` | 1,440 | `51d7bd89d3352096...` | `b97829e7bc97d838...` | PASS (`== V2.1`) | `1dnGc0DENVsutkDwFORkamO4vXuI6oX2t` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl` | 2,880 | `347f331af164d642...` | `294cfe6db06b425b...` | PASS (`== V2.1`) | `1oP6VhxdKbksw-zC8An6MmkY5yzQCqu27` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl` | 2,880 | `95df708344b573a6...` | `39d8aed9146b3e49...` | PASS (`== V2.1`) | `1u9t5HIuT5xuVPdHXSAKHOhR30MuCTqWx` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl` | 2,880 | `c32cb5e824cb2120...` | `02ac806d5035e52f...` | PASS (`== V2.1`) | `1667DyE5JOxs2zb2ZtSNZlz78boArTTRX` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl` | 2,880 | `5d7a61d125b6aae6...` | `1808a9137429db18...` | PASS (`== V2.1`) | `12B8wP9KfD_XB_6KhRh_zQcYqvUSR2pEx` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl` | 2,880 | `38b49bc0583aa29f...` | `4bddaa647c678086...` | PASS (`== V2.1`) | `105t8ER24toJBGRSglhX7TMQGCEyZpCEj` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl` | 2,880 | `fa83992ff05371fa...` | `b3f6caf6a939b1a7...` | PASS (`== V2.1`) | `1gm86AhrxpPyiIeGonOYgXfLrjdsGr9E_` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_ENG_PhysicalAppearance.jsonl` | 1,440 | `6ba7806435d0136f...` | `36c1b17e709cd3be...` | PASS (`== V2.1`) | `1Xq_gTTZPeLgkr8ulyRLWrs9s2uuQxyb9` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_PhysicalAppearance/BanglaBBQ_BEN_PhysicalAppearance.jsonl` | 1,440 | `23de8b2eafe5f092...` | `f3b4af8a0cdc1531...` | PASS (`== V2.1`) | `1wvMNoWSdr8-_0WrA8Gas-QXL7pgZVxMN` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl` | 2,880 | `b64bb72e4fb73226...` | `de73750686e86984...` | PASS (`== V2.1`) | `1db5ARGQZXwRcpA11jb_kKzn9i0x1sgkL` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl` | 2,880 | `126d967d2f9898ed...` | `ad2268e1700e6924...` | PASS (`== V2.1`) | `1A2mUqm-yR-qhXJPpi1tBNp63t5afJzzV` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl` | 1,440 | `aecb074e53ffc936...` | `25018689274fc9d6...` | PASS (`== V2.1`) | `1mOfulGqfzK5EObVqK7BuCabBbhTSF777` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl` | 1,440 | `c95be726598df84b...` | `55d0cf5c3f781448...` | PASS (`== V2.1`) | `1sghMSu6SW4NoWITxeGmRveJssvo19VhE` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl` | 2,880 | `53084712e3c0a2de...` | `be2f40099a9427f1...` | PASS (`== V2.1`) | `1FfMnILgPix7FSp_-S37MpfRdSTSWhp2u` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl` | 2,880 | `b814d7a586521403...` | `24851692c55f1d63...` | PASS (`== V2.1`) | `1bEYhKVM7p0ZcAyWOGxy7MsHW4UqhBW4M` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl` | 1,440 | `012c9543224d1d5a...` | `38e0289c8403e1d7...` | PASS (`== V2.1`) | `1GtgtO5cE5m90EM56qmRNxAfkWM1yQhNp` |
| `Dataset_BanglaBBQ_New/BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl` | 1,440 | `e56a2b674b7c7994...` | `a954331758d417d5...` | PASS (`== V2.1`) | `1DO07L4_Ck8ZM6316rFFuXVplkssBqfMl` |

---

## 3. Detailed Google Sheets Cell-Level Verification Table

| Worksheet | Sheet ID | Rows | Data Cells | Mismatches | Metadata Preserved | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `BanglaBBQ_ENG_Education` | `1544720708` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_Education` | `641606675` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_Ethnicity` | `210887456` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_Ethnicity` | `1845601757` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_HealthStatus` | `577820949` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_HealthStatus` | `1261981579` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_MaritalStatus` | `2049623557` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_MaritalStatus` | `1929463163` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_OccupationalBackground` | `1499154542` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_OccupationalBackground` | `934780717` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_PhysicalAppearance` | `984262367` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_PhysicalAppearance` | `934839633` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_Politics` | `1888499205` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_Politics` | `2128232344` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_Regional` | `1321419120` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_Regional` | `786932138` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_Religion` | `804112545` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_Religion` | `860941009` | 2,880 | 43,200 | 0 | True | **PASS** |
| `BanglaBBQ_ENG_SocialStatus` | `1061280109` | 1,440 | 21,600 | 0 | True | **PASS** |
| `BanglaBBQ_BEN_SocialStatus` | `1761692098` | 1,440 | 21,600 | 0 | True | **PASS** |

---

## 4. Rollback Evidence (`backups/pre_v21_production_promotion_20261117/`)

All pre-promotion snapshots (local canonical JSONLs, 20 exported Google Sheets JSONs + formatting metadata, and 20 downloaded Google Drive remote JSONLs) are archived with SHA-256 manifests under `backups/pre_v21_production_promotion_20261117/`.
