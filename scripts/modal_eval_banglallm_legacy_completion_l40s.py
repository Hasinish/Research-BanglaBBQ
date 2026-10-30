"""EXPERIMENTAL BanglaLLM historical-completion prompt recovery, NOT certified.\nPreserves the existing canonical experiment and all original reports.\n"""

import os
import sys
import time
from pathlib import Path
import modal

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.modal_eval_core import (
    get_hf_token,
    run_full_benchmark_core,
    print_and_save_final_report,
)

MODEL_NAME = "BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct"
MODEL_SLUG = "banglallm_qwen_3b_legacy_completion_v2"
MODEL_VOLUME_NAME = "banglallm-qwen-3b-volume"
MODEL_DIR = "/models/banglallm-qwen-3b-it"

model_volume = modal.Volume.from_name(MODEL_VOLUME_NAME)
eval_volume = modal.Volume.from_name("banglabbq-eval-volume", create_if_missing=True)

full_eval_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.4.0",
        "vllm>=0.6.3",
        "transformers>=4.46.0",
        "accelerate>=0.33.0",
        "huggingface_hub",
    )
    .env({"HF_TOKEN": get_hf_token()})
    .add_local_dir("Dataset_BanglaBBQ_New", remote_path="/root/Dataset_BanglaBBQ_New", copy=True)
    .add_local_dir("metadata", remote_path="/root/metadata", copy=True)
    .add_local_dir("scripts", remote_path="/root/scripts", copy=True)
)

app = modal.App("banglabbq-banglallm-legacy-completion-evaluator")


@app.function(
    image=full_eval_image,
    gpu="L40S",
    volumes={"/models": model_volume, "/eval_data": eval_volume},
    timeout=3600,
)
def run_benchmark():
    import sys
    sys.path.insert(0, "/root")
    from scripts.modal_eval_core import run_full_benchmark_core

    return run_full_benchmark_core(
        model_name=MODEL_NAME,
        model_slug=MODEL_SLUG,
        model_dir=MODEL_DIR,
        eval_volume=eval_volume,
        data_dir_path="/root/Dataset_BanglaBBQ_New",
        metadata_dir_path="/root/metadata",
        durable_eval_dir="/eval_data",
        prompt_mode="legacy_completion",
        generation_max_tokens=5,
        report_prefix="experimental_benchmark_report",
    )


@app.local_entrypoint()
def main():
    print(f"[*] Launching EXPERIMENTAL 61,312-Query Benchmark for: {MODEL_NAME}")
    start = time.time()
    result = run_benchmark.remote()
    wall_time = time.time() - start
    print_and_save_final_report(result, wall_time)


if __name__ == "__main__":
    main()
