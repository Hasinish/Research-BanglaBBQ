import os
import shutil
import json
from pathlib import Path

REPO_SRC = Path("d:/Research-BanglaBBQ")
BDBBQ_ROOT = Path("D:/BDBBQ")
ANALYSIS_DIR = BDBBQ_ROOT / "analysis"
SCRIPTS_DIR = ANALYSIS_DIR / "scripts"
RESULTS_DIR = ANALYSIS_DIR / "results"

def setup_directories():
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Directories ready under {ANALYSIS_DIR}")

def copy_target_map():
    src_map = REPO_SRC / "metadata" / "sidecar_stereotype_target_map.json"
    dst_map = ANALYSIS_DIR / "sidecar_stereotype_target_map.json"
    shutil.copy2(src_map, dst_map)
    print(f"[*] Copied target map to {dst_map}")

def copy_results():
    results_src = REPO_SRC / "metadata" / "eval_results"
    target_files = [
        "certified_benchmark_master_summary.csv",
        "certified_benchmark_master_summary.json",
        "certified_benchmark_report_gemma2_9b.csv",
        "certified_benchmark_report_gemma2_9b.json",
        "certified_benchmark_report_mistral_nemo_12b.csv",
        "certified_benchmark_report_mistral_nemo_12b.json",
        "certified_benchmark_report_qwen2_5_7b.csv",
        "certified_benchmark_report_qwen2_5_7b.json",
        "certified_benchmark_report_llama3_1_8b.csv",
        "certified_benchmark_report_llama3_1_8b.json",
        "certified_benchmark_report_ministral_8b.csv",
        "certified_benchmark_report_ministral_8b.json",
        "certified_benchmark_report_qwen2_5_3b.csv",
        "certified_benchmark_report_qwen2_5_3b.json",
        "certified_benchmark_report_banglallm_qwen_3b.csv",
        "certified_benchmark_report_banglallm_qwen_3b.json",
        "certified_benchmark_report_titulm_3b.csv",
        "certified_benchmark_report_titulm_3b.json",
        "experimental_benchmark_report_banglallm_qwen_3b_legacy_completion_v2.csv",
        "experimental_benchmark_report_banglallm_qwen_3b_legacy_completion_v2.json"
    ]
    for fname in target_files:
        src_file = results_src / fname
        dst_file = RESULTS_DIR / fname
        assert src_file.exists(), f"Missing result file {src_file}"
        shutil.copy2(src_file, dst_file)
        print(f"    -> Copied result: {fname}")
    print(f"[*] All {len(target_files)} certified result files staged.")

def copy_and_adapt_scripts():
    # 1. BBQ scoring engine
    src_engine = REPO_SRC / "scripts" / "bbq_scoring_engine.py"
    dst_engine = SCRIPTS_DIR / "bbq_scoring_engine.py"
    shutil.copy2(src_engine, dst_engine)
    print(f"[*] Staged bbq_scoring_engine.py")

    # 2. modal_eval_core.py with bilingual BDBBQ Data/ layout support
    core_text = (REPO_SRC / "scripts" / "modal_eval_core.py").read_text(encoding="utf-8")
    # Make imports agnostic
    import_fix = """try:
    from bbq_scoring_engine import (
        load_sidecar_map,
        parse_prediction,
        classify_record_prediction,
        compute_bbq_metrics,
    )
except ImportError:
    try:
        from analysis.scripts.bbq_scoring_engine import (
            load_sidecar_map,
            parse_prediction,
            classify_record_prediction,
            compute_bbq_metrics,
        )
    except ImportError:
        from scripts.bbq_scoring_engine import (
            load_sidecar_map,
            parse_prediction,
            classify_record_prediction,
            compute_bbq_metrics,
        )"""
    target_import = """from scripts.bbq_scoring_engine import (
    load_sidecar_map,
    parse_prediction,
    classify_record_prediction,
    compute_bbq_metrics,
)"""
    core_text = core_text.replace(target_import, import_fix)

    # Make default paths support BDBBQ root
    core_text = core_text.replace(
        'data_dir_path: str = "/root/Dataset_BanglaBBQ_New",\n    metadata_dir_path: str = "/root/metadata",',
        'data_dir_path: str = "/root/Data",\n    metadata_dir_path: str = "/root/analysis",',
    )
    core_text = core_text.replace(
        'sidecar_path = Path(metadata_dir_path) / "sidecar_stereotype_target_map.json"',
        'sidecar_path = Path(metadata_dir_path) / "sidecar_stereotype_target_map.json" if (Path(metadata_dir_path) / "sidecar_stereotype_target_map.json").exists() else Path(metadata_dir_path).parent / "sidecar_stereotype_target_map.json"'
    )

    # Support Data/BDBBQ_ENG and Data/BDBBQ_BN layout
    category_loading_old = """    for idx, cat_name in enumerate(categories, start=1):
        cat_dir = data_dir / cat_name
        eng_file = list(cat_dir.glob("*ENG*.jsonl"))[0]
        ben_file = list(cat_dir.glob("*BEN*.jsonl"))[0]

        with open(eng_file, "r", encoding="utf-8") as f:
            eng_rows = [json.loads(line) for line in f if line.strip()]

        with open(ben_file, "r", encoding="utf-8") as f:
            ben_rows = [json.loads(line) for line in f if line.strip()]"""

    category_loading_new = """    is_bdbbq_layout = (data_dir / "BDBBQ_ENG").exists() and (data_dir / "BDBBQ_BN").exists()
    if is_bdbbq_layout:
        eng_files = sorted(list((data_dir / "BDBBQ_ENG").glob("*.jsonl")))
        items = []
        for ef in eng_files:
            bf = (data_dir / "BDBBQ_BN") / ef.name
            cat_name = ef.stem
            items.append((cat_name, ef, bf))
    else:
        items = []
        for cat_name in categories:
            cat_dir = data_dir / cat_name
            ef = list(cat_dir.glob("*ENG*.jsonl"))[0]
            bf = list(cat_dir.glob("*BEN*.jsonl"))[0]
            items.append((cat_name, ef, bf))

    for idx, (cat_name, eng_file, ben_file) in enumerate(items, start=1):
        with open(eng_file, "r", encoding="utf-8") as f:
            eng_rows = [json.loads(line) for line in f if line.strip()]

        with open(ben_file, "r", encoding="utf-8") as f:
            ben_rows = [json.loads(line) for line in f if line.strip()]"""

    core_text = core_text.replace(category_loading_old, category_loading_new)

    (SCRIPTS_DIR / "modal_eval_core.py").write_text(core_text, encoding="utf-8")
    print(f"[*] Staged adapted modal_eval_core.py")

    # 3. Model evaluator scripts
    evaluators = [
        ("modal_eval_full_60k_l40s.py", "eval_gemma2_9b.py"),
        ("modal_eval_mistral_nemo_full_60k_l40s.py", "eval_mistral_nemo_12b.py"),
        ("modal_eval_qwen_7b_full_60k_l40s.py", "eval_qwen2_5_7b.py"),
        ("modal_eval_llama_full_60k_l40s.py", "eval_llama3_1_8b.py"),
        ("modal_eval_ministral_8b_full_60k_l40s.py", "eval_ministral_8b.py"),
        ("modal_eval_qwen_3b_full_60k_l40s.py", "eval_qwen2_5_3b.py"),
        ("modal_eval_banglallm_qwen_3b_full_60k_l40s.py", "eval_banglallm_3b_chatml.py"),
        ("modal_eval_titulm_3b_full_60k_l40s.py", "eval_titulm_3b.py"),
        ("modal_eval_banglallm_legacy_completion_l40s.py", "eval_banglallm_3b_completion.py")
    ]

    for src_name, dst_name in evaluators:
        code = (REPO_SRC / "scripts" / src_name).read_text(encoding="utf-8")
        # Adapt import of core
        code = code.replace(
            "from scripts.modal_eval_core import (",
            "try:\n    from modal_eval_core import (\nexcept ImportError:\n    from analysis.scripts.modal_eval_core import (\n"
        )
        # Adapt local dir mounting
        code = code.replace(
            '.add_local_dir("Dataset_BanglaBBQ_New", remote_path="/root/Dataset_BanglaBBQ_New", copy=True)\n    .add_local_dir("metadata", remote_path="/root/metadata", copy=True)\n    .add_local_dir("scripts", remote_path="/root/scripts", copy=True)',
            '.add_local_dir("Data", remote_path="/root/Data", copy=True)\n    .add_local_dir("analysis", remote_path="/root/analysis", copy=True)'
        )
        (SCRIPTS_DIR / dst_name).write_text(code, encoding="utf-8")
        print(f"    -> Staged evaluator script: {dst_name}")

if __name__ == "__main__":
    setup_directories()
    copy_target_map()
    copy_results()
    copy_and_adapt_scripts()
    print("\n[SUCCESS] All analysis assets successfully staged.")
