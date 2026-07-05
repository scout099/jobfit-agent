import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESUME_PROFILE_PATH = PROJECT_ROOT / "data" / "resume_profile.json"
PROCESSED_JD_INDEX_PATH = PROJECT_ROOT / "data" / "processed_jds" / "index.json"
ANALYSIS_REPORT_PATH = PROJECT_ROOT / "outputs" / "analysis_report.txt"
MATCH_REPORT_PATH = PROJECT_ROOT / "outputs" / "match_report.md"


TARGET_SKILLS = [
    "Python",
    "SQL",
    "数据分析",
    "LLM",
    "AI Agent",
    "Prompt设计",
    "RAG",
    "工作流自动化",
    "工具调用",
    "FastAPI",
    "Docker",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_processed_jds():
    if not PROCESSED_JD_INDEX_PATH.exists():
        raise FileNotFoundError(
            f"未找到标准化 JD 索引，请先运行: python3 src/process_jds.py\n{PROCESSED_JD_INDEX_PATH}"
        )

    return load_json(PROCESSED_JD_INDEX_PATH)

def collect_jd_skills(jds):
    skill_fields = [
        "technical_skills",
        "data_skills",
        "agent_llm_skills",
        "soft_skills",
        "required_skills",
    ]

    skills = []

    for jd in jds:
        for field in skill_fields:
            for skill in jd.get(field, []):
                if skill not in skills:
                    skills.append(skill)

    return skills

def get_score_confidence(target_skill_count):
    if target_skill_count < 5:
        return "低"

    if target_skill_count < 10:
        return "中"

    return "高"

def score_each_jd(profile, jds):
    resume_skills = collect_resume_skills(profile)
    scored_jobs = []

    for jd in jds:
        jd_skills = collect_jd_skills([jd])
        score = score_match(resume_skills, jd_skills)

        scored_jobs.append({
            "job_title": jd.get("job_title", "未知岗位"),
            "company": jd.get("company", "未知公司"),
            "data_source": jd.get("data_source", "unknown"),
            "total_score": score["total_score"],
            "target_skill_count": score["target_skill_count"],
            "confidence": get_score_confidence(score["target_skill_count"]),
            "matched_count": len(score["matched_skills"]),
            "missing_count": len(score["missing_skills"]),
            "matched_skills": score["matched_skills"],
            "missing_skills": score["missing_skills"],
        })

    return sorted(
        scored_jobs,
        key=lambda item: item["total_score"],
        reverse=True,
    )

def build_job_ranking_section(scored_jobs):
    lines = [
        "## 分岗位匹配排名",
        "",
        "| 排名 | 公司 | 岗位 | 来源 | 分数 | 可信度 | 目标技能 | 已匹配 | 缺口 |",
        "| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]

    for index, job in enumerate(scored_jobs, start=1):
        lines.append(
            f"| {index} | {job['company']} | {job['job_title']} | {job['data_source']} | {job['total_score']} | {job['confidence']} | {job['target_skill_count']} | {job['matched_count']} | {job['missing_count']} |"
        )

    return "\n".join(lines)

def print_job_ranking(scored_jobs):
    print("分岗位匹配排名")
    print("=" * 32)

    for index, job in enumerate(scored_jobs, start=1):
        title = f"{job['company']} - {job['job_title']}"
        print(
            f"{index}. {title} | "
            f"分数: {job['total_score']} | "
            f"可信度: {job['confidence']} | "
            f"目标技能: {job['target_skill_count']} | "
            f"已匹配: {job['matched_count']} | "
            f"缺口: {job['missing_count']} | "
            f"来源: {job['data_source']}"
        )

    print()

def collect_resume_skills(profile):
    skills = set(profile.get("skills", []))

    for project in profile.get("projects", []):
        for skill in project.get("skills", []):
            skills.add(skill)

    for tool in profile.get("tools", []):
        skills.add(tool)

    return skills


def score_match(resume_skills, target_skills):
    matched = [skill for skill in target_skills if skill in resume_skills]
    missing = [skill for skill in target_skills if skill not in resume_skills]

    skill_score = round(len(matched) / len(target_skills) * 40, 1)

    project_score = 25 if "AI Agent" in resume_skills else 15
    education_score = 12
    tool_score = 8 if "Git" in resume_skills else 5
    expression_score = 5

    total_score = round(
        skill_score + project_score + education_score + tool_score + expression_score,
        1,
    )

    return {
        "total_score": total_score,
        "skill_score": skill_score,
        "project_score": project_score,
        "education_score": education_score,
        "tool_score": tool_score,
        "expression_score": expression_score,
        "target_skill_count": len(target_skills),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def build_report(profile, score, scored_jobs):
    matched_text = "\n".join(f"- {skill}" for skill in score["matched_skills"]) or "- 暂无"
    missing_text = "\n".join(f"- {skill}" for skill in score["missing_skills"]) or "- 暂无"

    project_names = [
        project["name"]
        for project in profile.get("projects", [])
    ]
    project_text = "\n".join(f"- {name}" for name in project_names) or "- 暂无"

    return f"""# JD-Resume 匹配报告

## 总体匹配度

总分：{score["total_score"]} / 100

目标技能数：{score["target_skill_count"]}，已匹配：{len(score["matched_skills"])}，缺口：{len(score["missing_skills"])}

| 维度 | 分数 |
| --- | ---: |
| 技能匹配 | {score["skill_score"]} / 40 |
| 项目经历 | {score["project_score"]} / 30 |
| 专业/课程背景 | {score["education_score"]} / 15 |
| 工具栈 | {score["tool_score"]} / 10 |
| 表达质量 | {score["expression_score"]} / 5 |

## 已匹配能力

{matched_text}

{build_job_ranking_section(scored_jobs)}

## 当前缺口

{missing_text}

## 可重点展示的项目

{project_text}

## 简历优化建议

- 在项目经历中突出 AI Agent、Prompt 设计、数据分析和自动化 pipeline。
- 如果目标岗位强调 RAG 或工具调用，建议补充一个最小 RAG / Tool Calling demo。
- 简历 bullet 尽量写清楚输入、处理流程、输出结果和评测指标。
- 对 BOSS / 实习岗位，可以把项目描述压缩成“能解决什么问题 + 用了什么技术 + 产出什么结果”。

## 面试风险问题

- 你如何定义 AI Agent？它和普通 LLM 调用有什么区别？
- 你的 JD 抽取结果如何评测？
- 为什么要做技能标准化？
- 如果网页抓取失败，系统如何兜底？
- 规则抽取和 LLM 抽取分别适合什么场景？
"""


def main():
    profile = load_json(RESUME_PROFILE_PATH)
    jds = load_processed_jds()
    resume_skills = collect_resume_skills(profile)
    target_skills = collect_jd_skills(jds)
    print(f"已读取标准化 JD: {len(jds)} 条")
    score = score_match(resume_skills, target_skills)
    scored_jobs = score_each_jd(profile, jds)
    print_job_ranking(scored_jobs)

    report = build_report(profile, score, scored_jobs)
    MATCH_REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"匹配报告已保存到: {MATCH_REPORT_PATH}")


if __name__ == "__main__":
    main()
