import json
from pathlib import Path
import sys


RAW_JD_PATH = Path(__file__).resolve().parents[1] / "data" / "raw_jds" / "bytedance_agent_ops.txt"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "extracted_jd.json"
def load_skill_config():
    with SKILL_CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config["skill_keywords"], config["skill_normalization"]
SKILL_CONFIG_PATH = Path(__file__).resolve().parents[1] / "data" / "skill_config.json"

def read_raw_jd():
    with RAW_JD_PATH.open("r", encoding="utf-8") as file:
        return file.read()


def extract_basic_fields(text):
    result = {
        "job_title": "未知",
        "company": "未知",
        "city": "未知",
        "source": "未知",
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("岗位名称："):
            result["job_title"] = line.replace("岗位名称：", "").strip()
        elif line.startswith("公司："):
            result["company"] = line.replace("公司：", "").strip()
        elif line.startswith("城市："):
            result["city"] = line.replace("城市：", "").strip()
        elif line.startswith("来源："):
            result["source"] = line.replace("来源：", "").strip()

    return result

def extract_skills(text):
    skill_keywords, skill_normalization = load_skill_config()
    extracted_skills = {}

    for field, keywords in skill_keywords.items():
        matched = []

        for keyword in keywords:
            if keyword in text:
                matched.append(keyword)

        extracted_skills[field] = normalize_skills(matched, skill_normalization)

    return extracted_skills

def save_extracted_jd(extracted, output_path=OUTPUT_PATH):
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(extracted, file, ensure_ascii=False, indent=2)

def normalize_skills(skills, skill_normalization):
    normalized = []

    for skill in skills:
        normalized_skill = skill_normalization.get(skill, skill)

        if normalized_skill not in normalized:
            normalized.append(normalized_skill)

    return normalized

    return normalized

def extract_section_items(text, section_title):
    lines = text.splitlines()
    items = []
    in_section = False

    for line in lines:
        line = line.strip()

        if line.startswith(section_title):
            in_section = True
            continue

        if in_section and line.endswith("："):
            break

        if in_section and line:
            cleaned_line = line.lstrip("0123456789.、 ").strip()
            items.append(cleaned_line)

    return items


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else RAW_JD_PATH
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT_PATH
    with input_path.open("r", encoding="utf-8") as file:
        raw_text = file.read()

    extracted = extract_basic_fields(raw_text)
    extracted["responsibilities"] = extract_section_items(raw_text, "岗位职责：")
    extracted["requirements"] = extract_section_items(raw_text, "任职要求：")
    extracted.update(extract_skills(raw_text))
    save_extracted_jd(extracted, output_path)
    print(json.dumps(extracted, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()