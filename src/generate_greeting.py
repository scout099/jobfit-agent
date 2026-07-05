import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESUME_PROFILE_PATH = PROJECT_ROOT / "data" / "resume_profile.json"
EXPERIENCE_LIBRARY_PATH = PROJECT_ROOT / "data" / "experience_library.json"
MATCH_REPORT_PATH = PROJECT_ROOT / "outputs" / "match_report.md"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "boss_greeting.txt"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_experience_library():
    if not EXPERIENCE_LIBRARY_PATH.exists():
        return []

    data = load_json(EXPERIENCE_LIBRARY_PATH)
    return data.get("experiences", [])

def main():
    profile = load_json(RESUME_PROFILE_PATH)
    experiences = load_experience_library()
    target_direction = profile.get("target_direction", "AI Agent / 数据智能实习")
    skills = profile.get("skills", [])

    highlight_skills = [
        skill
        for skill in ["Python", "SQL", "数据分析", "AI Agent", "Prompt设计"]
        if skill in skills
    ]

    skills_text = "、".join(highlight_skills) or "Python、数据分析"

    experience_text = "之前做过 AI Career Intelligence Agent 项目，围绕 JD 信息抽取、技能标准化、匹配评分和报告生成搭建了完整 pipeline"

    if experiences:
        main_experience = experiences[0]
        experience_name = main_experience.get("name", "相关项目")
        evidence = main_experience.get("evidence", [])
        evidence_text = "、".join(evidence[:2])
        evidence_text = (
        evidence_text
        .replace("支持 raw_jds 目录批量抽取 JD", "支持批量解析岗位 JD")
        .replace("使用 skill_config.json 做技能标准化和同义词归一", "做技能标准化和同义词归一")
        .replace("生成 processed_jds/index.json 作为统一 JD 数据入口", "统一多来源 JD 数据")
        )

        if evidence_text:
            experience_text = f"之前做过 {experience_name}，主要包括{evidence_text}"
        else:
            experience_text = f"之前做过 {experience_name}"

    greeting = f"""您好，我正在寻找{target_direction}方向的实习机会。{experience_text}，也具备{skills_text}等基础能力。看到贵岗位和我的方向比较匹配，希望有机会进一步沟通，谢谢！"""

    OUTPUT_PATH.write_text(greeting, encoding="utf-8")

    print(greeting)
    print()
    print(f"BOSS 招呼语已保存到: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()