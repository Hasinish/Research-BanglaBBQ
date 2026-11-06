import os
import shutil
import subprocess
from pathlib import Path

SOURCE_ROOT = Path("Dataset_BanglaBBQ_New")
DEST_ROOT = Path("D:/BDBBQ")

COMMITS = [
    # 1 & 2: Educational Background
    {
        "src": "BanglaBBQ_EducationalBackground/BanglaBBQ_ENG_Education.jsonl",
        "dst": "Data/BDBBQ_ENG/Educational Background.jsonl",
        "msg": "fix(data): update Educational Background English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_EducationalBackground/BanglaBBQ_BEN_Education.jsonl",
        "dst": "Data/BDBBQ_BN/Educational Background.jsonl",
        "msg": "fix(data): update Educational Background Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 3 & 4: Ethnicity
    {
        "src": "BanglaBBQ_Ethnicity/BanglaBBQ_ENG_Ethnicity.jsonl",
        "dst": "Data/BDBBQ_ENG/Ethnicity.jsonl",
        "msg": "fix(data): update Ethnicity English benchmark with audited dataset (1,440 records)",
        "expected_lines": 1440
    },
    {
        "src": "BanglaBBQ_Ethnicity/BanglaBBQ_BEN_Ethnicity.jsonl",
        "dst": "Data/BDBBQ_BN/Ethnicity.jsonl",
        "msg": "fix(data): update Ethnicity Bengali benchmark with native linguistic refinements (1,440 records)",
        "expected_lines": 1440
    },

    # 5 & 6: Health Status
    {
        "src": "BanglaBBQ_HealthStatus/BanglaBBQ_ENG_HealthStatus.jsonl",
        "dst": "Data/BDBBQ_ENG/HealthStatus.jsonl",
        "msg": "fix(data): restore and update Health Status English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_HealthStatus/BanglaBBQ_BEN_HealthStatus.jsonl",
        "dst": "Data/BDBBQ_BN/HealthStatus.jsonl",
        "msg": "fix(data): restore and update Health Status Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 7 & 8: Marital Status
    {
        "src": "BanglaBBQ_MaritalStatus/BanglaBBQ_ENG_MaritalStatus.jsonl",
        "dst": "Data/BDBBQ_ENG/MaritalStatus.jsonl",
        "msg": "fix(data): restore and update Marital Status English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_MaritalStatus/BanglaBBQ_BEN_MaritalStatus.jsonl",
        "dst": "Data/BDBBQ_BN/MaritalStatus.jsonl",
        "msg": "fix(data): restore and update Marital Status Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 9 & 10: Occupational Background
    {
        "src": "BanglaBBQ_OccupationalBackground/BanglaBBQ_ENG_OccupationalBackground.jsonl",
        "dst": "Data/BDBBQ_ENG/OccupationalBackground.jsonl",
        "msg": "fix(data): update Occupational Background English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_OccupationalBackground/BanglaBBQ_BEN_OccupationalBackground.jsonl",
        "dst": "Data/BDBBQ_BN/OccupationalBackground.jsonl",
        "msg": "fix(data): update Occupational Background Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 11 & 12: Politics
    {
        "src": "BanglaBBQ_Politics/BanglaBBQ_ENG_Politics.jsonl",
        "dst": "Data/BDBBQ_ENG/Politics.jsonl",
        "msg": "fix(data): restore and update Politics English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_Politics/BanglaBBQ_BEN_Politics.jsonl",
        "dst": "Data/BDBBQ_BN/Politics.jsonl",
        "msg": "fix(data): restore and update Politics Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 13 & 14: Regional Affiliation
    {
        "src": "BanglaBBQ_Regional/BanglaBBQ_ENG_Regional.jsonl",
        "dst": "Data/BDBBQ_ENG/Regional Affiliation.jsonl",
        "msg": "fix(data): update Regional Affiliation English benchmark with audited dataset (1,440 records)",
        "expected_lines": 1440
    },
    {
        "src": "BanglaBBQ_Regional/BanglaBBQ_BEN_Regional.jsonl",
        "dst": "Data/BDBBQ_BN/Regional Affiliation.jsonl",
        "msg": "fix(data): update Regional Affiliation Bengali benchmark with native linguistic refinements (1,440 records)",
        "expected_lines": 1440
    },

    # 15 & 16: Religion
    {
        "src": "BanglaBBQ_Religion/BanglaBBQ_ENG_Religion.jsonl",
        "dst": "Data/BDBBQ_ENG/Religion.jsonl",
        "msg": "fix(data): update Religion English benchmark with audited dataset (2,880 records)",
        "expected_lines": 2880
    },
    {
        "src": "BanglaBBQ_Religion/BanglaBBQ_BEN_Religion.jsonl",
        "dst": "Data/BDBBQ_BN/Religion.jsonl",
        "msg": "fix(data): update Religion Bengali benchmark with native linguistic refinements (2,880 records)",
        "expected_lines": 2880
    },

    # 17 & 18: Social Status
    {
        "src": "BanglaBBQ_SocialStatus/BanglaBBQ_ENG_SocialStatus.jsonl",
        "dst": "Data/BDBBQ_ENG/SocialStatus.jsonl",
        "msg": "fix(data): update Social Status English benchmark with audited dataset (1,440 records)",
        "expected_lines": 1440
    },
    {
        "src": "BanglaBBQ_SocialStatus/BanglaBBQ_BEN_SocialStatus.jsonl",
        "dst": "Data/BDBBQ_BN/SocialStatus.jsonl",
        "msg": "fix(data): update Social Status Bengali benchmark with native linguistic refinements (1,440 records)",
        "expected_lines": 1440
    }
]

def run_git(args, cwd):
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def main():
    print(f"[*] Starting 18-Commit Deployment to {DEST_ROOT}...")
    assert len(COMMITS) == 18, f"Expected 18 commits, got {len(COMMITS)}"

    for i, c in enumerate(COMMITS, 1):
        src_path = SOURCE_ROOT / c["src"]
        dst_path = DEST_ROOT / c["dst"]

        assert src_path.exists(), f"Source file does not exist: {src_path}"
        assert dst_path.parent.exists(), f"Destination directory does not exist: {dst_path.parent}"

        # Copy file
        shutil.copy2(src_path, dst_path)

        # Verify line count
        with open(dst_path, "r", encoding="utf-8") as f:
            lines = [l for l in f if l.strip()]
        assert len(lines) == c["expected_lines"], f"Line count mismatch for {dst_path}: {len(lines)} vs {c['expected_lines']}"

        # Git add & commit
        run_git(["add", str(c["dst"])], cwd=DEST_ROOT)
        commit_out = run_git(["commit", "-m", c["msg"]], cwd=DEST_ROOT)
        commit_hash = run_git(["rev-parse", "--short", "HEAD"], cwd=DEST_ROOT)

        print(f"[{i:02d}/18] [{commit_hash}] {c['msg']}")

    print("\n[*] All 18 commits successfully created locally in D:/BDBBQ!")
    print("[*] Pushing all 18 commits to BDBBQ-Research/BDBBQ (origin/main)...")
    push_out = run_git(["push", "origin", "main"], cwd=DEST_ROOT)
    print(push_out)
    print("\n[SUCCESS] All 18 separate commits pushed to https://github.com/BDBBQ-Research/BDBBQ!")

if __name__ == "__main__":
    main()
