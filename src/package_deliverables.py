from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DELIVERABLE_DIR = OUTPUTS_DIR / "deliverables"
DELIVERABLE_PATH = DELIVERABLE_DIR / "jobfit_deliverable.md"


SECTIONS = [
    ("岗位匹配报告", OUTPUTS_DIR / "match_report.md"),
    ("个人经历匹配报告", OUTPUTS_DIR / "experience_match_report.md"),
    ("定制简历项目 Bullet", OUTPUTS_DIR / "optimized_resume_bullets.md"),
    ("BOSS 招呼语", OUTPUTS_DIR / "boss_greeting.txt"),
    ("Cover Letter", OUTPUTS_DIR / "cover_letter.md"),
]


def read_section(path):
    if not path.exists():
        return "文件尚未生成。"

    return path.read_text(encoding="utf-8").strip()


def main():
    DELIVERABLE_DIR.mkdir(parents=True, exist_ok=True)

    parts = [
        "# JobFit Agent 求职材料交付包",
        "",
        "本文件汇总了当前 pipeline 生成的岗位匹配报告、简历优化建议、BOSS 招呼语和 Cover Letter。",
        "",
    ]

    for title, path in SECTIONS:
        parts.append(f"## {title}")
        parts.append("")
        parts.append(read_section(path))
        parts.append("")

    DELIVERABLE_PATH.write_text("\n".join(parts), encoding="utf-8")

    print(f"求职材料交付包已生成: {DELIVERABLE_PATH}")


if __name__ == "__main__":
    main()