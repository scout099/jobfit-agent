import json
from collections import Counter
from pathlib import Path
from recommender import recommend_learning_path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "structured_jds.json"
PROCESSED_JD_INDEX_PATH = Path(__file__).resolve().parents[1] / "data" / "processed_jds" / "index.json"
USER_PROFILE_PATH = Path(__file__).resolve().parents[1] / "data" / "user_profile.json"
SKILL_WEIGHTS_PATH = Path(__file__).resolve().parents[1] / "data" / "skill_weights.json"
SKILL_FIELDS = [
    "technical_skills",
    "data_skills",
    "agent_llm_skills",
    "soft_skills",
]
EXTRACTED_JD_PATH = Path(__file__).resolve().parents[1] / "data" / "extracted_jd.json"
LLM_EXTRACTED_JD_PATH = Path(__file__).resolve().parents[1] / "data" / "llm_extracted_jd.json"
DATA_SOURCE_PRIORITY = {
    "manual": 3,
    "llm": 2,
    "rule": 1,
}
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SKILL_CONFIG_PATH = Path(__file__).resolve().parents[1] / "data" / "skill_config.json"
ANALYSIS_REPORT_PATH = Path(__file__).resolve().parents[1] / "outputs" / "analysis_report.txt"

def load_jobs():
    if PROCESSED_JD_INDEX_PATH.exists():
        with PROCESSED_JD_INDEX_PATH.open("r", encoding="utf-8") as file:
            jobs = json.load(file)

        skill_normalization = load_skill_normalization()

        normalized_jobs = [
            normalize_job_skills(job, skill_normalization)
            for job in jobs
        ]

        deduplicated_jobs = deduplicate_jobs(normalized_jobs)
        print(f"已读取标准化 JD 索引: {len(jobs)} 条，去重后: {len(deduplicated_jobs)} 条")

        return deduplicate_jobs(normalized_jobs)

    with DATA_PATH.open("r", encoding="utf-8") as file:
        jobs = json.load(file)

    for job in jobs:
        attach_data_source(job, "manual")

    for extracted_path in sorted(DATA_DIR.glob("extracted_*.json")):
        with extracted_path.open("r", encoding="utf-8") as file:
            extracted_job = json.load(file)

        jobs.append(attach_data_source(extracted_job, "rule"))

    if LLM_EXTRACTED_JD_PATH.exists():
        with LLM_EXTRACTED_JD_PATH.open("r", encoding="utf-8") as file:
            llm_extracted_job = json.load(file)

        jobs.append(attach_data_source(llm_extracted_job, "llm"))

    skill_normalization = load_skill_normalization()

    normalized_jobs = [
        normalize_job_skills(job, skill_normalization)
        for job in jobs
    ]

    return deduplicate_jobs(normalized_jobs)

def attach_data_source(job, data_source):
    job["data_source"] = data_source
    return job

def get_source_priority(job):
    data_source = job.get("data_source", "unknown")
    return DATA_SOURCE_PRIORITY.get(data_source, 0)

def deduplicate_jobs(jobs):
    unique_by_key = {}

    for job in jobs:
        key = (
            job.get("company", "未知"),
            job.get("job_title", "未知"),
        )

        if key not in unique_by_key:
            unique_by_key[key] = job
            continue

        existing_job = unique_by_key[key]

        if get_source_priority(job) > get_source_priority(existing_job):
            unique_by_key[key] = job

    return list(unique_by_key.values())

def load_user_profile():
    with USER_PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_skill_weights():
    with SKILL_WEIGHTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_skill_normalization():
    with SKILL_CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config.get("skill_normalization", {})


def normalize_job_skills(job, skill_normalization):
    for field in SKILL_FIELDS:
        normalized_skills = []

        for skill in job.get(field, []):
            normalized_skill = skill_normalization.get(skill, skill)

            if normalized_skill not in normalized_skills:
                normalized_skills.append(normalized_skill)

        job[field] = normalized_skills

    return job

def count_skills(jobs):
    counter = Counter()
    skill_sources = {}

    for job in jobs:
        seen_in_job = set()
        for field in SKILL_FIELDS:
            for skill in job.get(field, []):
                seen_in_job.add(skill)

        for skill in seen_in_job:
            counter[skill] += 1
            skill_sources.setdefault(skill, []).append(job["job_title"])

    return counter, skill_sources

def score_skills(counter, skill_weights):
    scored_skills = []

    for skill, count in counter.items():
        weight = skill_weights.get(skill, 1.0)
        score = count * weight
        scored_skills.append({
            "skill": skill,
            "count": count,
            "weight": weight,
            "score": score,
        })

    return sorted(
        scored_skills,
        key=lambda item: item["score"],
        reverse=True
    )

def print_job_sources(jobs):
    print("参与分析的岗位样本")
    print("=" * 32)

    for index, job in enumerate(jobs, start=1):
        company = job.get("company", "未知公司")
        job_title = job.get("job_title", "未知岗位")
        data_source = job.get("data_source", "unknown")

        print(f"{index}. [{data_source}] {company} - {job_title}")

    print()

def print_skill_report(jobs, skill_weights):
    counter, skill_sources = count_skills(jobs)
    scored_skills = score_skills(counter, skill_weights)
    total = len(jobs)

    print("AI Career Intelligence Agent - 技能频率分析")
    print("=" * 32)
    print(f"样本数量: {total}")
    print()

    tiers = {
        "第一梯队：必须优先学": [],
        "第二梯队：建议重点补": [],
        "第三梯队：按目标岗位选择": [],
    }

    for item in scored_skills:
        skill = item["skill"]
        count = item["count"]
        weight = item["weight"]
        score = item["score"]

        jobs_text = "、".join(skill_sources[skill])
        frequency = count / total

        line = f"{skill}: {count}/{total} | 出现率: {frequency:.0%} | 权重: {weight} | 分数: {score:.1f} | 出现岗位: {jobs_text}"

        if frequency >= 0.7:
            tiers["第一梯队：必须优先学"].append(line)
        elif frequency >= 0.4:
            tiers["第二梯队：建议重点补"].append(line)
        else:
            tiers["第三梯队：按目标岗位选择"].append(line)

    for tier_name, lines in tiers.items():
        print(tier_name)
        print("-" * 32)

        if not lines:
            print("暂无")
        else:
            for line in lines:
                print(line)

        print()

    return tiers, scored_skills

def print_gap_report(tiers, user_profile, scored_skills):
    current_skills = set(user_profile["current_skills"])
    skill_score_map = {
    item["skill"]: item
    for item in scored_skills
    }

    required_skills = []
    for lines in tiers.values():
        for line in lines:
            skill = line.split(":")[0]
            required_skills.append(skill)

    missing_skills = [
        skill for skill in required_skills
        if skill not in current_skills
    ]

    matched_skills = [
        skill for skill in required_skills
        if skill in current_skills
    ]

    print("个人能力差距分析")
    print("=" * 32)
    print(f"目标方向: {user_profile['target_direction']}")
    print()

    print("你已经具备：")
    if matched_skills:
        for skill in matched_skills:
            print(f"- {skill}")
    else:
        print("- 暂无匹配技能")
    print()

    print("当前缺口：")
    for skill in missing_skills[:10]:
        print(f"- {skill}")
    print()

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "missing_skill_items": [
            skill_score_map[skill]
            for skill in missing_skills
            if skill in skill_score_map
        ],
        "focus_skills": user_profile["focus_skills"]
    }

def save_analysis_report(report_text):
    ANALYSIS_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with ANALYSIS_REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write(report_text)

    print()
    print(f"分析报告已保存到: {ANALYSIS_REPORT_PATH}")

if __name__ == "__main__":
    import io
    from contextlib import redirect_stdout

    jobs = load_jobs()
    user_profile = load_user_profile()
    skill_weights = load_skill_weights()

    buffer = io.StringIO()

    with redirect_stdout(buffer):
        print_job_sources(jobs)
        tiers, scored_skills = print_skill_report(jobs, skill_weights)
        gap_report = print_gap_report(tiers, user_profile, scored_skills)
        recommend_learning_path(tiers, gap_report)

    report_text = buffer.getvalue()
    print(report_text)
    save_analysis_report(report_text)
