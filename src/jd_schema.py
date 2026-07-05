from pydantic import BaseModel, Field


class JDInfo(BaseModel):
    id: str = ""
    job_title: str = "未知"
    company: str = "未知"
    source: str = "未知"
    city: str = "未知"
    seniority: str = "未知"
    job_family: str = "未知"

    business_scenario: list[str] = Field(default_factory=list)
    core_problem: str = ""

    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)

    technical_skills: list[str] = Field(default_factory=list)
    data_skills: list[str] = Field(default_factory=list)
    agent_llm_skills: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    project_ideas: list[str] = Field(default_factory=list)

    education_requirement: str = "未知"
    experience_requirement: str = "未知"
    job_type: str = "未知"
    location: str = "未知"
    source_url: str = ""
    data_source: str = "unknown"
    raw_text: str = ""