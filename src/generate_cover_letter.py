import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESUME_PROFILE_PATH = PROJECT_ROOT / "data" / "resume_profile.json"
EXPERIENCE_LIBRARY_PATH = PROJECT_ROOT / "data" / "experience_library.json"
MATCH_REPORT_PATH = PROJECT_ROOT / "outputs" / "match_report.md"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "cover_letter.md"


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
    project_name = "AI Career Intelligence Agent"

    projects = profile.get("projects", [])
    if projects:
        project_name = projects[0].get("name", project_name)

    experience_summary = "这个项目从真实 JD 出发，构建了一个可复现的求职分析 pipeline。"
    experience_points = []

    if experiences:
        main_experience = experiences[0]
        project_name = main_experience.get("name", project_name)
        experience_summary = main_experience.get("summary", experience_summary)

        evidence = main_experience.get("evidence", [])
        story_points = main_experience.get("story_points", [])
        experience_points = evidence[:3] + story_points[:2]

        if experience_points:
            cleaned_points = []

        for point in experience_points:
            cleaned_point = (
                point
                .replace("支持 raw_jds 目录批量抽取 JD", "支持批量解析真实岗位 JD")
                .replace("使用 skill_config.json 做技能标准化和同义词归一", "设计技能词表，完成技能标准化和同义词归一")
                .replace("使用 Pydantic JDInfo schema 统一标准化 JD 结构", "使用 Pydantic schema 统一多来源 JD 数据结构")
                .replace("生成 processed_jds/index.json 作为统一 JD 数据入口", "建立统一的标准化 JD 数据入口")
            ).rstrip("。；;")

            cleaned_points.append(cleaned_point)

        experience_points_text = "\n".join(
            f"- {point}；"
            for point in cleaned_points
        )
    else:
        experience_points_text = """- 将非结构化岗位文本抽取成可分析的结构化数据；
- 设计可解释的匹配评分规则，而不是只依赖大模型主观判断；
- 用 schema 校验、失败用例测试和产物检查保证 pipeline 稳定性；
- 根据岗位要求生成简历优化建议、项目 bullet 和投递话术。"""

    cover_letter = f"""# Cover Letter

您好：

我正在申请 {target_direction} 相关岗位。我的专业背景与数据分析、算法思维和工程实现有一定关联，也在持续围绕 AI Agent 和大模型应用方向做项目实践。

近期我完成了 `{project_name}` 项目。{experience_summary}

通过这个项目，我重点训练了几类能力：

{experience_points_text}

我希望能在实习中继续参与 AI Agent、数据智能、RAG、工具调用或大模型应用落地方向的工作。如果有机会，我也很愿意进一步介绍项目实现细节和我对岗位的理解。

谢谢您的时间！

{profile.get("name", "你的名字")}
"""

    OUTPUT_PATH.write_text(cover_letter, encoding="utf-8")

    print(cover_letter)
    print(f"Cover Letter 已保存到: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()