import json


REQUIRED_FIELDS = {
    "job_title": str,
    "company": str,
    "source": str,
    "city": str,
    "seniority": str,
    "job_family": str,
    "business_scenario": list,
    "core_problem": str,
    "responsibilities": list,
    "requirements": list,
    "technical_skills": list,
    "data_skills": list,
    "agent_llm_skills": list,
    "soft_skills": list,
    "project_ideas": list,
}


def validate_llm_json_response(response_text):
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError(f"LLM 输出不是合法 JSON: {error}") from error

    errors = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append(f"缺少字段: {field}")
            continue

        if not isinstance(data[field], expected_type):
            errors.append(
                f"字段类型错误: {field} 应该是 {expected_type.__name__}"
            )

    if errors:
        raise ValueError("LLM JSON schema 校验失败:\n" + "\n".join(errors))

    return data