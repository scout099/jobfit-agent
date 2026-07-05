from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


REQUIRED_OUTPUTS = [
    "data/extracted_bytedance_agent_ops.json",
    "data/llm_extracted_jd.json",
    "data/processed_jds/index.json",
    "data/experience_library.json",
    "outputs/llm_request_preview.txt",
    "outputs/eval_report.txt",
    "outputs/eval_llm_report.txt",
    "outputs/eval_comparison_report.txt",
    "outputs/pipeline_run_report.txt",
    "outputs/analysis_report.txt",
    "outputs/career_analysis_report.md",
    "outputs/match_report.md",
    "outputs/experience_match_report.md",
    "outputs/optimized_resume_bullets.md",
    "outputs/boss_greeting.txt",
    "outputs/cover_letter.md",
    "outputs/deliverables/jobfit_deliverable.md",
]


def main():
    print("关键输出文件检查")
    print("=" * 32)

    missing_files = []

    for relative_path in REQUIRED_OUTPUTS:
        path = PROJECT_ROOT / relative_path

        if path.exists():
            print(f"[OK] {relative_path}")
        else:
            print(f"[MISSING] {relative_path}")
            missing_files.append(relative_path)

    print()

    if missing_files:
        print("缺失文件：")
        for file in missing_files:
            print(f"- {file}")
        raise SystemExit(1)

    print("所有关键输出文件都已生成。")


if __name__ == "__main__":
    main()
