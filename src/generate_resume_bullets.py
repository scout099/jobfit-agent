import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESUME_PROFILE_PATH = PROJECT_ROOT / "data" / "resume_profile.json"
EXPERIENCE_LIBRARY_PATH = PROJECT_ROOT / "data" / "experience_library.json"
MATCH_REPORT_PATH = PROJECT_ROOT / "outputs" / "match_report.md"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "optimized_resume_bullets.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_experience_library():
    if not EXPERIENCE_LIBRARY_PATH.exists():
        return []

    data = load_json(EXPERIENCE_LIBRARY_PATH)
    return data.get("experiences", [])

def build_project_bullets(project):
    name = project.get("name", "项目")
    skills = project.get("skills", [])
    skills_text = "、".join(skills[:6])

    return f"""## {name}

- 构建面向 AI Agent / 数据智能岗位的 JD 分析与简历匹配 pipeline，支持原始 JD 批量抽取、技能标准化、能力差距分析与 Markdown 报告生成。
- 设计技能词表与同义词标准化配置，将 LLM、大语言模型、Prompt Engineering 等表达统一归一，提升多来源 JD 统计的一致性。
- 实现 LLM 输出 JSON schema 校验与失败用例测试，避免字段缺失或类型错误的数据进入后续分析流程。
- 支持 URL 自动抓取与手动粘贴兜底机制，将岗位 JD 统一保存到 raw_jds 并接入批量抽取流程，提升系统对真实招聘页面的兼容性。
- 设计 JD-Resume 匹配评分逻辑，从技能、项目经历、课程背景、工具栈和表达质量等维度生成可解释匹配报告。
- 技术栈：{skills_text}
"""

def build_experience_bullets(experience):
    name = experience.get("name", "经历")
    role = experience.get("role", "")
    bullets = experience.get("resume_bullets", [])
    skills = experience.get("skills", [])

    bullet_text = "\n".join(f"- {bullet}" for bullet in bullets)
    skills_text = "、".join(skills[:8])

    return f"""## {name}

角色：{role}

{bullet_text}

- 相关技能：{skills_text}
"""

def build_resume_summary(profile):
    target_direction = profile.get("target_direction", "AI Agent / 数据智能实习")

    return f"""# 定制化简历项目描述

## 个人定位建议

面向 {target_direction}，建议突出以下关键词：

- AI Agent 应用开发
- JD 信息抽取
- 技能标准化
- JSON schema 校验
- 可复现 pipeline
- 匹配评分与报告生成

## 项目经历优化版

"""


def main():
    profile = load_json(RESUME_PROFILE_PATH)
    experiences = load_experience_library()

    markdown = build_resume_summary(profile)

    for project in profile.get("projects", []):
        markdown += build_project_bullets(project)
        markdown += "\n"

    if experiences:
        markdown += "## 个人经历库精选 Bullet\n\n"

        for experience in experiences:
            markdown += build_experience_bullets(experience)
            markdown += "\n"

    OUTPUT_PATH.write_text(markdown, encoding="utf-8")

    print(markdown)
    print(f"简历 bullet 建议已保存到: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()