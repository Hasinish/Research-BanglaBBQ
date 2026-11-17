# Research Log: V2.1 Official Production Promotion & Four-Way Synchronization

**Date**: 2026-11-17  
**Researcher / Agent**: Hasin Ishrak / Antigravity AI  
**Category**: Multi-Category V2.1 Production Promotion (10 Categories; Age & Gender Preserved Byte-for-Byte)  
**Milestone Scope**: Authorized four-way deployment of `fixed JsonL v2.1/` (46,080 records; 691,200 spreadsheet cells) across Local Canonical `Dataset_BanglaBBQ_New/`, Master Google Spreadsheet, Master Google Drive, and GitHub `Hasinish/Research-BanglaBBQ` `main`  
**Status**: OPERATIONAL FOUR-WAY PARITY PASS / NOT PUBLICATION-READY (HUMAN REVIEW PENDING)  

---

## 1. Research Objective & Governance Boundary

Following targeted repairs and 13-point revalidation of `fixed JsonL v2.1/` (`audits/fixed_jsonl_v21_repair_20261117/REPAIR_REPORT.md`), the explicitly authorized goal was to promote the 20 repaired JSONL files (10 categories × 2 languages = 23,040 ENG + 23,040 BEN = 46,080 records) bit-for-bit into production while preserving `BanglaBBQ_Age` (2,920/lang) and `BanglaBBQ_Gender` (4,696/lang) completely unchanged.

**Explicit Scientific Limitation**: Operational deployment and structural/programmatic parity do **NOT** constitute publication readiness. Independent native Bangladeshi Bengali human review across all 23,040 Bengali records, exhaustive manual entailment verification across all untouched Sentence 3 blocks, and live external URL verification of `additional_metadata` sources remain **INCONCLUSIVE / PENDING**.

---

## 2. Pre-Deployment Backups (`backups/pre_v21_production_promotion_20261117/`)

1. **Local Canonical Backup** (`backups/pre_v21_production_promotion_20261117/local_canonical/`): Archived all 20 prior canonical JSONLs + SHA-256 baseline manifest (`local_backup_manifest.json`), including untouched `Age` & `Gender` hashes.
2. **Google Sheets Backup** (`backups/pre_v21_production_promotion_20261117/google_sheets/`): Exported all 20 target worksheets (`A1:O{N+1}`) + full sheet properties, frozen rows, grid dimensions, conditional formatting, and column widths (`sheets_backup_manifest.json`).
3. **Google Drive Backup** (`backups/pre_v21_production_promotion_20261117/google_drive/`): Downloaded all 20 prior remote Drive files + recorded file IDs, MD5s, SHA-256 properties, and untouched `Age`/`Gender` metadata (`drive_backup_manifest.json`).

---

## 3. Canonical Files, SHA-256 Hashes & Google Drive IDs (20/20 Exact Parity)

| Canonical File (`Dataset_BanglaBBQ_New/`) | Pre-Promo SHA-256 | Post-Promo Canonical SHA-256 | Source V2.1 SHA-256 | Parity |
| :--- | :--- | :--- | :--- | :---: |
| `BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl` | `2fdf05a428a04d6c5df3c6bcda925ff1bd4d4ff13ea9217e70046c5bd3de73d5` | `36bf8425d61faf67b509355f9c048bebd89c8db1886d30dc2574128b70bb3c7a` | `36bf8425d61faf67b509355f9c048bebd89c8db1886d30dc2574128b70bb3c7a` | PASS |
| `BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl` | `00d56efae76d45b9722c383abf95bd8a0ce4f26be5b57cc6c448ce35eedcfd18` | `ac3693ef9bbf3454e8de84c40c633b660b25b42948e1544bf8a88146afd59fa6` | `ac3693ef9bbf3454e8de84c40c633b660b25b42948e1544bf8a88146afd59fa6` | PASS |
| `BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl` | `536493d7f3b91b816298e85abed87de489cbf11901e90170b7a2127d8bb729f9` | `555918dc09288aeea0e52be61f6e4c08e6cbe244bae01380f0dc03932e08ff8b` | `555918dc09288aeea0e52be61f6e4c08e6cbe244bae01380f0dc03932e08ff8b` | PASS |
| `BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl` | `51d7bd89d3352096cfd05fa4bfcacc6d084fe592bdfbae71050cbf69ec5dfb7d` | `b97829e7bc97d8383dcc418799f6caaee127cdf8e7b4f42239677627dd97b21b` | `b97829e7bc97d8383dcc418799f6caaee127cdf8e7b4f42239677627dd97b21b` | PASS |
| `BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl` | `347f331af164d642ad275a990dc0855610e6ccc1a805c95fb972008edd5f214a` | `294cfe6db06b425bab559a0c239cf957d41537a038aa0b4e4ce42f502f9c8760` | `294cfe6db06b425bab559a0c239cf957d41537a038aa0b4e4ce42f502f9c8760` | PASS |
| `BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl` | `95df708344b573a6d4c8f8c04079dbc0bf856e402cab81707022004874d5b74f` | `39d8aed9146b3e492a3ff8d375376927b3c7763a416cf387f12b84f09975c892` | `39d8aed9146b3e492a3ff8d375376927b3c7763a416cf387f12b84f09975c892` | PASS |
| `BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl` | `c32cb5e824cb2120e53b25fe6fe8345ef33b2461bb711b0e34dd98fdf98c951f` | `02ac806d5035e52fcac79ade0191ec507c3795dabc7a9a93e82d5b76da05c3b3` | `02ac806d5035e52fcac79ade0191ec507c3795dabc7a9a93e82d5b76da05c3b3` | PASS |
| `BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl` | `5d7a61d125b6aae623c5f198bbe7757a03167b7ab163689f2aba57ec1f974691` | `1808a9137429db1877ecde5411e7c6b9547b24fb39ecce351a67528fb5c004f8` | `1808a9137429db1877ecde5411e7c6b9547b24fb39ecce351a67528fb5c004f8` | PASS |
| `BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl` | `38b49bc0583aa29facd3c6c193793754aadae3849054b0d168ff331365edf073` | `4bddaa647c678086dced8d5251d5f56e6244019feb6a52e1aed18b8042e880f1` | `4bddaa647c678086dced8d5251d5f56e6244019feb6a52e1aed18b8042e880f1` | PASS |
| `BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl` | `fa83992ff05371fad776d6e4305988b641b75e582050b07283948ebaea562204` | `b3f6caf6a939b1a7bd8ecdf76674683c87d11e40ec800c78216dd2e8176fc474` | `b3f6caf6a939b1a7bd8ecdf76674683c87d11e40ec800c78216dd2e8176fc474` | PASS |
| `BanglaBBQ_PhysicalAppearance/BanglaBBQ_ENG_PhysicalAppearance.jsonl` | `6ba7806435d0136fb9d1918113c906841571f1d8b2df4bfc89fb667f481f946f` | `36c1b17e709cd3be9f80621a9091f2c497ecaff617d42592f96e9dd379e1ec92` | `36c1b17e709cd3be9f80621a9091f2c497ecaff617d42592f96e9dd379e1ec92` | PASS |
| `BanglaBBQ_PhysicalAppearance/BanglaBBQ_BEN_PhysicalAppearance.jsonl` | `23de8b2eafe5f092333948212868999eafafcdc2890cd275e33702530b2a04f2` | `f3b4af8a0cdc153134af24ecf6a45bac3437da936b142574163784b5eb12e0fa` | `f3b4af8a0cdc153134af24ecf6a45bac3437da936b142574163784b5eb12e0fa` | PASS |
| `BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl` | `b64bb72e4fb73226afe017970d3be4c2257cc9a2a19386a3a97eee1ff8e4b149` | `de73750686e86984439c1dc3ad064cb541ff3b018dd6d3e8b58de41bab71a0e4` | `de73750686e86984439c1dc3ad064cb541ff3b018dd6d3e8b58de41bab71a0e4` | PASS |
| `BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl` | `126d967d2f9898eddda482157e42490754db543ec35cb2d1eafceab4d49cc362` | `ad2268e1700e6924592ea5f7d4ca6b6189bebdfbd4d03be6c19c869156adb522` | `ad2268e1700e6924592ea5f7d4ca6b6189bebdfbd4d03be6c19c869156adb522` | PASS |
| `BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl` | `aecb074e53ffc93611ca144cb89b0151bb9909b19d8a3d75bdeeaa71549592d3` | `25018689274fc9d611a402e73244e86d528b4b3db54721980fb08fcc1bcba5f4` | `25018689274fc9d611a402e73244e86d528b4b3db54721980fb08fcc1bcba5f4` | PASS |
| `BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl` | `c95be726598df84b0d49ea52681ded4ea5bccb84e3c04a18ee01d5e93010e47f` | `55d0cf5c3f78144837611dd2912129a07558e654106a3f4988a62f1ba57c6e21` | `55d0cf5c3f78144837611dd2912129a07558e654106a3f4988a62f1ba57c6e21` | PASS |
| `BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl` | `53084712e3c0a2de510d5db5bf523e1ca1adeb3cf230a2aa03ff10df7a9868af` | `be2f40099a9427f120c7f65ba2666fde78292979426ebe5c0b8caaedd73ad8d1` | `be2f40099a9427f120c7f65ba2666fde78292979426ebe5c0b8caaedd73ad8d1` | PASS |
| `BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl` | `b814d7a586521403ed4258e379acf6e9692cc5dd5e2c6bacb60ab6ffd07c1476` | `24851692c55f1d63af6cffeab862f956d1e495bd3744cc4334b50274512a4d61` | `24851692c55f1d63af6cffeab862f956d1e495bd3744cc4334b50274512a4d61` | PASS |
| `BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl` | `012c9543224d1d5a781844f9a169f62bf665091fa6f30269c88f05b3c6586140` | `38e0289c8403e1d70618616ac37d1e3b52f55f043cdc258e130a997b1e13cbfe` | `38e0289c8403e1d70618616ac37d1e3b52f55f043cdc258e130a997b1e13cbfe` | PASS |
| `BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl` | `e56a2b674b7c7994468031916dfc1e881c180fa8742cab52d49164d2d2b59124` | `a954331758d417d5adbf74694816862ca2b0cc52acdf3da0d3f8a773261a07d5` | `a954331758d417d5adbf74694816862ca2b0cc52acdf3da0d3f8a773261a07d5` | PASS |

**Preserved Untouched Categories (Byte-for-Byte Identical)**:
- `BanglaBBQ_Age/BanglaBBQ_ENG_Age.jsonl`: `72e135ef87c8bf2b73002a9d81512e84bd707a5aa40cab22a9296aa8a173e39a` (unchanged: `True`)
- `BanglaBBQ_Age/BanglaBBQ_BEN_Age.jsonl`: `d844932f2fc64bf31bd51980016482c429f986fdb44e05ebdaf2ef1401b59b1d` (unchanged: `True`)
- `BanglaBBQ_Gender/BanglaBBQ_ENG_Gender.jsonl`: `b7ef4a13f4e1134c592e70349e01122ec62467717396ae6aaabcf6286db085dd` (unchanged: `True`)
- `BanglaBBQ_Gender/BanglaBBQ_BEN_Gender.jsonl`: `ae564aa6579a8444371cc298159b23ebf5f2cb0248ccbd0bc06542da619467c8` (unchanged: `True`)

---

## 4. Google Sheets Full Cell Readback (`scripts/sync_v21_all_20_sheets.py`)

**Spreadsheet ID**: `1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY`  
**Total Verified Data Cells**: **691,200 / 691,200** (**0 mismatches**)

| Worksheet | Sheet ID | Data Rows | Data Cells Verified | Cell Mismatches | Metadata & Formatting Preserved | Status |
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

## 5. Google Drive Dual-Hash Parity (`scripts/sync_drive_dataset.py --verify-only`)

- **Master Folder ID**: `1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe`
- **Result**: Updated all 20 outdated files **in-place** preserving original file IDs; all **24 / 24** canonical files (including 4 untouched Age/Gender files) verified **100% MD5 + SHA-256 bit-for-bit parity**.

---

## 6. Automated Validation & Remaining Limitations

- `scripts/sync_drive_dataset.py --validate-only`: 24/24 canonical JSONLs certified (61,312 records, 0 defects).
- `tests/test_all_61312_actual_records_mapping.py`: 61,312/61,312 records mapped (0 errors).
- `audits/v21_production_promotion_20261117/local_promotion_manifest.json`: 0 scoring engine errors across 46,080 promoted records.
- **Outstanding (`INCONCLUSIVE`)**: Human native Bangladeshi Bengali linguistic audit, exhaustive manual S3 entailment verification of untouched blocks, and live external URL verification remain incomplete; benchmark is **NOT publication-ready**.
