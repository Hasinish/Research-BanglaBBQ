# Physical Appearance — Post-local-fix QA statement

Audited upstream main: `e186b283fa5b184058e2cb395273e9968a893b20`. This is a **local candidate**, **not** a GitHub or Google Sheets update.

**Original JSONL:** 1,440 EN + 1,440 BN records. **Locally corrected:** 1,440 EN + 1,440 BN records. English byte-identical to source; Bengali changed in **720 unique records**, **1008 fields**, all of them contexts/questions and none of them source metadata/labels/IDs.

**Original independent diagnostic:** 288 P0 bilingual meaning findings, spread over Q06 and Q09. **Candidate independent diagnostic:** 0 implemented structural/semantic discrepancies across 2,880 per-row blind-gold checks and 240 bilingual anchor checks. Original generator validator returns 0 on candidate. **26/26 selected mutation types** still caught by independent adversarial suite on candidate.

**Remaining block:** source-premise mismatch and confounds (especially Q02/Q03/Q04/Q05/Q06/Q07/Q08/Q10), incomplete Q02 article full-text access, 10 correlated paraphrase families, Q03 V1 Bengali naturalness and no external human evaluation. **Not publication ready; SAFE_TO_IMPORT = false.**

**SHA-256 EN:** `851719a3d90c678f1cee6f61d3b23550c32d38bf202f8eeafcbc98e0d8e72e7c`  
**SHA-256 BN:** `f120b4149f877a27efd7d94b72e9de76a6c40496b81de61e1d7300f94523a8c9`

Always interpret full findings together with `physical_appearance_issue_ledger.csv`, `physical_appearance_source_evidence_matrix.csv`, the 240-anchor review and the unmodified committed snapshots.
