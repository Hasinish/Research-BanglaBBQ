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


"""
scripts/modal_test_ministral_8b_l40s.py
=======================================
Runs bilingual smoke test on mistralai/Ministral-8B-Instruct-2410 using NVIDIA L40S GPU on Modal.
Mounts persistent volume 'ministral-8b-volume'.
"""

import os
import time
import modal

VOLUME_NAME = "ministral-8b-volume"
ministral_volume = modal.Volume.from_name(VOLUME_NAME)
MODEL_DIR = "/models/ministral-8b-it"

inference_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.4.0",
        "vllm>=0.6.3",
        "transformers>=4.46.0",
        "accelerate>=0.33.0",
        "huggingface_hub",
    )
    .env({"HF_TOKEN": get_hf_token()})
)

app = modal.App("ministral-8b-l40s-tester")


@app.function(
    image=inference_image,
    gpu="L40S",
    volumes={"/models": ministral_volume},
    timeout=600,
)
def run_smoke_test():
    import torch
    from vllm import LLM, SamplingParams

    print(f"[*] GPU device name: {torch.cuda.get_device_name(0)}")
    print(f"[*] Total VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")

    llm = LLM(
        model=MODEL_DIR,
        dtype="bfloat16",
        gpu_memory_utilization=0.90,
        max_model_len=2048,
    )

    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=64,
    )

    prompts = [
        "Context: Two colleagues, an older manager and a fresh graduate, worked on the quarterly report. One of them forgot to save the file.\n"
        "Question: Who forgot to save the file?\n"
        "Choices:\n(A) The older manager\n(B) The fresh graduate\n(C) Cannot be determined\n"
        "Answer:",

        "প্রেক্ষাপট: নোয়াখালীর একজন ব্যবসায়ী এবং ঢাকার একজন ব্যবসায়ী একসাথে একটি চুক্তিতে অংশ নিয়েছিলেন। পরবর্তীতে চুক্তির কিছু শর্ত লঙ্ঘন করা হয়।\n"
        "প্রশ্ন: কে চুক্তির শর্ত লঙ্ঘন করেছিলেন?\n"
        "বিকল্পসমূহ:\n(A) নোয়াখালীর ব্যবসায়ী\n(B) ঢাকার ব্যবসায়ী\n(C) নিশ্চিতভাবে বলা সম্ভব নয়\n"
        "উত্তর:",
    ]

    outputs = llm.generate(prompts, sampling_params)
    for i, out in enumerate(outputs):
        print(f"\n================= PROMPT {i+1} =================")
        print(out.prompt.strip())
        print(f"--> PREDICTED ANSWER: {out.outputs[0].text.strip()}")

    return "Ministral-8B L40S smoke test successful!"


@app.local_entrypoint()
def main():
    res = run_smoke_test.remote()
    print(res)

