import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE_LIBRARY_PATH = PROJECT_ROOT / "data" / "experience_library.json"
PROCESSED_JD_INDEX_PATH = PROJECT_ROOT / "data" / "processed_jds" / "index.json"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "experience_match_report.md"

SKILL_FIELDS = [
    "technical_skills",
    "data_skills",
    "agent_llm_skills",
    "soft_skills",
    "required_skills",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def collect_jd_skills(jd):
    skills = []

    for field in SKILL_FIELDS:
        for skill in jd.get(field, []):
            if skill not in skills:
                skills.append(skill)

    return skills


def score_experience_for_jd(experience, jd):
    jd_skills = collect_jd_skills(jd)
    experience_skills = experience.get("skills", [])

    matched_skills = [
        skill
        for skill in jd_skills
        if skill in experience_skills
    ]

    if not jd_skills:
        skill_score = 0
    else:
        skill_score = round(len(matched_skills) / len(jd_skills) * 100, 1)

    return {
        "experience_id": experience.get("id", ""),
        "experience_name": experience.get("name", "未知经历"),
        "job_title": jd.get("job_title", "未知岗位"),
        "company": jd.get("company", "未知公司"),
        "data_source": jd.get("data_source", "unknown"),
        "score": skill_score,
        "matched_skills": matched_skills,
        "missing_skills": [
            skill
            for skill in jd_skills
            if skill not in experience_skills
        ],
    }


def rank_experiences(experiences, jds):
    results = []

    for jd in jds:
        for experience in experiences:
            results.append(score_experience_for_jd(experience, jd))

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )


def render_report(results):
    lines = [
        "# 个人经历匹配报告",
        "",
        "## 经历-JD 匹配排名",
        "",
        "| 排名 | 公司 | 岗位 | 来源 | 经历 | 分数 | 命中技能 |",
        "| ---: | --- | --- | --- | --- | ---: | --- |",
    ]

    for index, result in enumerate(results, start=1):
        matched_text = "、".join(result["matched_skills"]) or "暂无"

        lines.append(
            f"| {index} | {result['company']} | {result['job_title']} | {result['data_source']} | {result['experience_name']} | {result['score']} | {matched_text} |"
        )

    return "\n".join(lines)


def print_top_results(results, limit=5):
    print("个人经历匹配 Top 结果")
    print("=" * 32)

    for index, result in enumerate(results[:limit], start=1):
        matched_text = "、".join(result["matched_skills"]) or "暂无"

        print(
            f"{index}. {result['company']} - {result['job_title']} | "
            f"经历: {result['experience_name']} | "
            f"分数: {result['score']} | "
            f"命中: {matched_text}"
        )

    print()


def main():
    experience_library = load_json(EXPERIENCE_LIBRARY_PATH)
    experiences = experience_library.get("experiences", [])
    jds = load_json(PROCESSED_JD_INDEX_PATH)

    results = rank_experiences(experiences, jds)
    report = render_report(results)

    OUTPUT_PATH.write_text(report, encoding="utf-8")

    print_top_results(results)
    print(f"个人经历匹配报告已保存到: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()