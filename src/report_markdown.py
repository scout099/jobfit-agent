from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_REPORT_PATH = PROJECT_ROOT / "outputs" / "analysis_report.txt"
MARKDOWN_REPORT_PATH = PROJECT_ROOT / "outputs" / "career_analysis_report.md"


def main():
    if not ANALYSIS_REPORT_PATH.exists():
        raise FileNotFoundError(f"缺少分析报告: {ANALYSIS_REPORT_PATH}")

    report_text = ANALYSIS_REPORT_PATH.read_text(encoding="utf-8")

    markdown_text = (
        "# AI Career Intelligence Agent 分析报告\n\n"
        "## 报告摘要\n\n"
        "本报告基于当前项目中的 JD 样本，统计 AI Agent / 数据智能相关岗位的高频技能，"
        "并结合个人技能画像生成能力差距和学习路线建议。\n\n"
        "## 原始分析输出\n\n"
        "```text\n"
        f"{report_text}\n"
        "```\n"
    )

    MARKDOWN_REPORT_PATH.write_text(markdown_text, encoding="utf-8")

    print(f"Markdown 分析报告已保存到: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()