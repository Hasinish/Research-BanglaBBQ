import json
import hashlib
import os
import subprocess
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\Research-BanglaBBQ"
QA_DIR = os.path.join(BASE_DIR, "local_candidates", "final_seven_category_qa")
AUDIT_DIR = os.path.join(QA_DIR, "independent_source_semantic_audit")
MANIFEST_PATH = os.path.join(AUDIT_DIR, "input_manifest.json")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    if not os.path.exists(MANIFEST_PATH):
        print(f"ERROR: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    all_match = True
    checked_count = 0
    
    print("=================================================================")
    print("       FINAL DATASET INPUT HASH INTEGRITY VERIFICATION           ")
    print("=================================================================")
    
    for cat_name, file_list in manifest["files"].items():
        print(f"\n--- Category: {cat_name} ---")
        for f_info in file_list:
            rel_path = f_info["path"]
            abs_path = os.path.join(BASE_DIR, rel_path.replace("/", "\\"))
            expected_hash = f_info["sha256"]
            expected_size = f_info["size_bytes"]
            
            if not os.path.exists(abs_path):
                print(f"  [MISSING] {rel_path}")
                all_match = False
                continue
                
            curr_size = os.path.getsize(abs_path)
            curr_hash = sha256_file(abs_path)
            checked_count += 1
            
            if curr_hash == expected_hash and curr_size == expected_size:
                print(f"  [PASS] {os.path.basename(rel_path)}: SHA256 unchanged ({curr_hash[:16]}...)")
            else:
                print(f"  [FAIL] {os.path.basename(rel_path)}: HASH MISMATCH!")
                print(f"         Expected: {expected_hash} ({expected_size} bytes)")
                print(f"         Actual  : {curr_hash} ({curr_size} bytes)")
                all_match = False
                
    # Git status check
    git_res = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True)
    tracked_mods = [line for line in git_res.stdout.splitlines() if not line.startswith("??")]
    
    print("\n--- GIT TRACKED PRODUCTION REPOSITORY STATUS ---")
    if not tracked_mods:
        print("  [PASS] Exactly 0 tracked files modified in repository.")
    else:
        print(f"  [FAIL] Tracked modifications detected ({len(tracked_mods)} files):")
        for line in tracked_mods:
            print(f"    {line}")
        all_match = False
        
    print("\n=================================================================")
    if all_match:
        print(f"VERDICT: 100% DATASET INTEGRITY PRESERVED ({checked_count}/{checked_count} files verified identical)")
        print("ZERO UNAPPROVED WRITES OR DATA MUTATIONS CONFIRMED.")
    else:
        print("VERDICT: INTEGRITY FAILURE DETECTED!")
        sys.exit(1)
    print("=================================================================")

if __name__ == "__main__":
    main()
