import json
from pathlib import Path

from jd_schema import JDInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_JD_DIR = DATA_DIR / "raw_jds"

STRUCTURED_JDS_PATH = DATA_DIR / "structured_jds.json"
LLM_EXTRACTED_JD_PATH = DATA_DIR / "llm_extracted_jd.json"

PROCESSED_JD_DIR = DATA_DIR / "processed_jds"
PROCESSED_INDEX_PATH = PROCESSED_JD_DIR / "index.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def read_raw_text(stem):
    raw_path = RAW_JD_DIR / f"{stem}.txt"

    if not raw_path.exists():
        return ""

    return raw_path.read_text(encoding="utf-8")


def normalize_to_jd_info(raw_job, data_source, fallback_id):
    job = dict(raw_job)

    job.setdefault("id", fallback_id)
    job.setdefault("data_source", data_source)

    if "location" not in job and "city" in job:
        job["location"] = job["city"]

    skill_fields = [
        "technical_skills",
        "data_skills",
        "agent_llm_skills",
        "soft_skills",
    ]

    required_skills = list(job.get("required_skills", []))

    for field in skill_fields:
        for skill in job.get(field, []):
            if skill not in required_skills:
                required_skills.append(skill)

    job["required_skills"] = required_skills

    return JDInfo(**job)


def collect_source_jobs():
    source_jobs = []

    if STRUCTURED_JDS_PATH.exists():
        structured_jobs = load_json(STRUCTURED_JDS_PATH)

        for index, job in enumerate(structured_jobs, start=1):
            fallback_id = job.get("id") or f"manual_{index:02d}"
            source_jobs.append((fallback_id, job, "manual"))

    for extracted_path in sorted(DATA_DIR.glob("extracted_*.json")):
        stem = extracted_path.stem.replace("extracted_", "", 1)
        job = load_json(extracted_path)
        job["raw_text"] = read_raw_text(stem)
        source_jobs.append((stem, job, "rule"))

    if LLM_EXTRACTED_JD_PATH.exists():
        job = load_json(LLM_EXTRACTED_JD_PATH)
        fallback_id = job.get("id") or "llm_default"
        source_jobs.append((fallback_id, job, "llm"))

    return source_jobs


def process_jds():
    processed_jobs = []

    for fallback_id, raw_job, data_source in collect_source_jobs():
        jd_info = normalize_to_jd_info(raw_job, data_source, fallback_id)
        processed_job = jd_info.model_dump()

        output_path = PROCESSED_JD_DIR / f"{fallback_id}.json"
        save_json(output_path, processed_job)

        processed_jobs.append(processed_job)

    save_json(PROCESSED_INDEX_PATH, processed_jobs)

    return processed_jobs


def main():
    processed_jobs = process_jds()

    print(f"标准化 JD 数量: {len(processed_jobs)}")
    print(f"标准化 JD 索引已保存到: {PROCESSED_INDEX_PATH}")


if __name__ == "__main__":
    main()