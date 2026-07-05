import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
PIPELINE_REPORT_PATH = PROJECT_ROOT / "outputs" / "pipeline_run_report.txt"

COMMANDS = [
    ("批量抽取 raw_jds 目录", ["src/batch_extract.py"]),
    ("模拟 LLM 抽取并校验 JSON", ["src/extractor_llm.py"]),
    ("标准化 JD schema 并生成 processed_jds", ["src/process_jds.py"]),
    ("分析岗位技能和个人差距", ["src/analyzer.py"]),
    ("生成 Markdown 分析报告", ["src/report_markdown.py"]),
    ("生成 JD-Resume 匹配报告", ["src/match_resume.py"]),
    ("生成个人经历匹配报告", ["src/match_experiences.py"]),
    ("生成定制简历 bullet", ["src/generate_resume_bullets.py"]),
    ("生成 BOSS 招呼语", ["src/generate_greeting.py"]),
    ("生成 Cover Letter", ["src/generate_cover_letter.py"]),
    ("打包求职材料交付包", ["src/package_deliverables.py"]),
    ("评测规则抽取", ["evals/eval_extraction.py"]),
    ("评测 LLM 抽取", ["evals/eval_llm_extraction.py"]),
    ("测试 LLM schema 失败用例", ["evals/test_llm_schema_validation.py"]),
    ("生成规则 vs LLM 对比报告", ["evals/compare_eval_reports.py"]),
    ("检查关键输出文件", ["check_outputs.py"]),
]


def run_step(title, script_path):
    section_header = f"""
============================================================
{title}
============================================================
"""

    print(section_header)

    result = subprocess.run(
        [sys.executable, *script_path],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    section_report = section_header

    if result.stdout:
        section_report += result.stdout

    if result.stderr:
        section_report += "\n[stderr]\n"
        section_report += result.stderr

    if result.returncode != 0:
        raise RuntimeError(f"步骤失败: {title}")

    return section_report


def main():
    report_parts = []

    for title, script_path in COMMANDS:
        section_report = run_step(title, script_path)
        report_parts.append(section_report)

    final_message = """
============================================================
完整 pipeline 已运行完成
============================================================
"""

    print(final_message)
    report_parts.append(final_message)

    PIPELINE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with PIPELINE_REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write("\n".join(report_parts))

    print(f"pipeline 总报告已保存到: {PIPELINE_REPORT_PATH}")

if __name__ == "__main__":
    main()
