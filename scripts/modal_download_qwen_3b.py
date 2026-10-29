"""
scripts/modal_download_qwen_3b.py
=================================
Dedicated, lightweight CPU-only downloader for Qwen/Qwen2.5-3B-Instruct.
Conforms strictly to Cloud & Modal Cost Optimization Rule:
- cpu=1.0, memory=2048, ZERO GPUs.
- Uses hf_transfer for ultra-fast multi-threaded download into persistent Modal Volume.
- Automatically commits volume upon completion.
"""

import os
import time
import modal

def get_hf_token() -> str:
    token = os.environ.get("HF_TOKEN", "").strip()
    if token:
        return token
    for p in [
        os.path.expanduser("~/.cache/huggingface/token"),
        r"D:\custom-antigravity\credentials\hf_token.txt",
    ]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    t = f.read().strip()
                    if t:
                        return t
            except Exception:
                pass
    return ""

VOLUME_NAME = "qwen-3b-volume"
qwen_volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
MODEL_DIR = "/models/qwen-3b-it"

download_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("huggingface_hub[hf_transfer]>=0.23.0")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

app = modal.App("qwen-3b-downloader")


@app.function(
    image=download_image,
    volumes={"/models": qwen_volume},
    cpu=1.0,
    memory=2048,
    timeout=1800,
)
def download_model(hf_token: str = ""):
    from huggingface_hub import snapshot_download

    token = hf_token.strip() or os.environ.get("HF_TOKEN", "").strip()
    if not token:
        token_file = os.path.expanduser("~/.cache/huggingface/token")
        if os.path.exists(token_file):
            with open(token_file, "r") as f:
                token = f.read().strip()

    print(f"[*] Starting download of Qwen/Qwen2.5-3B-Instruct into {MODEL_DIR}...")
    start_time = time.time()

    snapshot_download(
        repo_id="Qwen/Qwen2.5-3B-Instruct",
        local_dir=MODEL_DIR,
        token=token if token else None,
        max_workers=8,
    )

    elapsed = time.time() - start_time
    print(f"[+] Download completed in {elapsed:.2f} seconds.")

    print(f"[*] Committing persistent volume '{VOLUME_NAME}'...")
    qwen_volume.commit()
    print(f"[+] Volume '{VOLUME_NAME}' committed! Weights are permanently stored.")
    return f"Success: Qwen2.5-3B-Instruct downloaded in {elapsed:.2f}s"


@app.local_entrypoint()
def main(hf_token: str = ""):
    hf_token = hf_token or get_hf_token()
    res = download_model.remote(hf_token=hf_token)
    print(res)

