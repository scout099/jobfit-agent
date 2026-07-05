# JobFit Agent

[![Python smoke test](https://github.com/scout099/jobfit-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/scout099/jobfit-agent/actions/workflows/ci.yml)

JobFit Agent is an AI-powered career analysis pipeline for JD extraction, resume matching, skill gap analysis, and job application material generation.

It starts from real job descriptions, converts unstructured JD text into structured data, standardizes skills across sources, evaluates JD-resume fit, and generates application-ready materials such as resume bullets, BOSS greeting messages, cover letters, and deliverable packages.

> This project evolved from an AI Career Intelligence Agent into a JobFit Agent MVP.

## What It Does

JobFit Agent helps answer a practical question:

> Given a set of target AI Agent / data intelligence jobs, what skills do they require, how well does my profile match them, and what materials should I prepare?

The current pipeline supports:

- Batch JD extraction from raw text files
- URL-based JD loading with manual paste fallback
- Structured JD schema validation with Pydantic
- Skill standardization and synonym normalization
- Rule-based and LLM-based JD extraction
- Mock, DeepSeek, and OpenAI LLM modes
- LLM JSON schema validation and failure-case testing
- JD-resume matching and explainable scoring
- Per-job match ranking with confidence labels
- Personal experience matching
- Resume bullet generation
- BOSS greeting message generation
- Cover letter generation
- One-command pipeline execution
- Streamlit MVP interface
- Deliverable package generation

## Why This Project

Many students and early-career candidates interested in AI Agent roles face three problems:

1. Job descriptions are noisy and hard to compare.
2. Skill requirements are written inconsistently across companies.
3. It is hard to translate personal projects into targeted application materials.

JobFit Agent turns this process into a reproducible pipeline:

```text
Raw JD
  -> JD extraction
  -> Skill normalization
  -> Structured JD index
  -> Job analysis
  -> Resume matching
  -> Experience matching
  -> Application material generation
  -> Deliverable package
```

## Quickstart

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full pipeline

By default, JobFit Agent uses mock LLM output, so no API key is required.

```bash
python3 run_all.py
```

### 4. Open the Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## LLM Modes

JobFit Agent supports three LLM modes.

### Mock Mode

Mock mode is the default. It requires no API key and is recommended for local development and stable testing.

```bash
python3 run_all.py
```

Equivalent to:

```bash
JOBFIT_LLM_MODE=mock python3 run_all.py
```

### DeepSeek API Mode

Set your DeepSeek API key first:

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```

Run the pipeline:

```bash
JOBFIT_LLM_MODE=deepseek python3 run_all.py
```

Default model:

```text
deepseek-v4-flash
```

To use another model:

```bash
DEEPSEEK_MODEL=deepseek-v4-pro JOBFIT_LLM_MODE=deepseek python3 run_all.py
```

### OpenAI API Mode

Set your OpenAI API key first:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

Run the pipeline:

```bash
JOBFIT_LLM_MODE=openai python3 run_all.py
```

Default model:

```text
gpt-4.1-mini
```

To use another model:

```bash
OPENAI_MODEL=gpt-4.1-mini JOBFIT_LLM_MODE=openai python3 run_all.py
```

## Important Security Note

Never commit real API keys.

This repository includes `.env.example` as a template only. If you create a local `.env` file, keep it private. The `.gitignore` file is configured to exclude `.env`.

## Project Structure

```text
jobfit-agent/
  app.py                         Streamlit MVP app
  run_all.py                     One-command pipeline runner
  check_outputs.py               Output completeness checker
  requirements.txt               Python dependencies
  .env.example                   Environment variable template

  data/
    raw_jds/                     Raw job description text files
    processed_jds/               Generated standardized JD files
    experience_library.json      Personal experience library
    resume_profile.json          Structured resume profile
    skill_config.json            Skill normalization config
    skill_weights.json           Skill scoring weights
    user_profile.json            User skill profile

  src/
    url_loader.py                JD URL loader
    manual_jd_input.py           Manual JD input helper
    extractor.py                 Rule-based JD extractor
    extractor_llm.py             LLM-based JD extractor
    jd_schema.py                 Pydantic JD schema
    process_jds.py               JD standardization pipeline
    analyzer.py                  JD analysis
    match_resume.py              JD-resume matching
    match_experiences.py         Experience matching
    generate_resume_bullets.py   Resume bullet generator
    generate_greeting.py         BOSS greeting generator
    generate_cover_letter.py     Cover letter generator
    package_deliverables.py      Deliverable packager
    report_markdown.py           Markdown report generator
    recommender.py               Learning recommendation logic

  evals/
    eval_extraction.py           Rule extraction evaluation
    eval_llm_extraction.py       LLM extraction evaluation
    compare_eval_reports.py      Rule vs LLM comparison
    test_llm_schema_validation.py
    gold_bytedance_agent_ops.json

  prompts/
    extract_jd.md
    extract_jd_llm.md

  outputs/
    llm_response_mock.json       Mock LLM success fixture
    llm_response_bad.json        Mock LLM failure fixture
```

Generated reports and deliverables are written to `outputs/`, but most generated files are ignored by Git.

## Common Commands

Run the full pipeline:

```bash
python3 run_all.py
```

Run rule-based extraction:

```bash
python3 src/extractor.py
```

Extract a specific JD file:

```bash
python3 src/extractor.py data/raw_jds/xiaohongshu_ai_product.txt data/extracted_xiaohongshu_ai_product.json
```

Run JD analysis:

```bash
python3 src/analyzer.py
```

Generate the JD-resume match report:

```bash
python3 src/match_resume.py
```

Generate the personal experience match report:

```bash
python3 src/match_experiences.py
```

Generate optimized resume bullets:

```bash
python3 src/generate_resume_bullets.py
```

Generate BOSS greeting text:

```bash
python3 src/generate_greeting.py
```

Generate cover letter:

```bash
python3 src/generate_cover_letter.py
```

Package deliverables:

```bash
python3 src/package_deliverables.py
```

Validate key outputs:

```bash
python3 check_outputs.py
```

Run tests:

```bash
pytest evals
```

## Output Examples

The pipeline can generate:

- `outputs/analysis_report.txt`
- `outputs/career_analysis_report.md`
- `outputs/match_report.md`
- `outputs/experience_match_report.md`
- `outputs/optimized_resume_bullets.md`
- `outputs/boss_greeting.txt`
- `outputs/cover_letter.md`
- `outputs/deliverables/jobfit_deliverable.md`
- `outputs/pipeline_run_report.txt`

## Engineering Highlights

This project is designed as a reproducible pipeline rather than a one-off script.

Key engineering choices include:

- Structured JD schema with Pydantic
- Config-driven skill normalization
- Rule extraction and LLM extraction paths
- Mock LLM mode for stable local testing
- Provider switch for DeepSeek and OpenAI
- Schema validation before downstream analysis
- Failure-case test for malformed LLM output
- Gold-file evaluation for extraction quality
- Unified processed JD index as the analysis entry point
- End-to-end pipeline runner and output checker
- Streamlit MVP for interactive usage

## Interview Explanation

I built JobFit Agent to analyze AI Agent and data intelligence job descriptions and turn them into actionable job-search insights.

The system reads raw JD text, extracts structured job information, normalizes skills across different expressions such as LLM, large language model, and Prompt Engineering, and then generates a standardized JD index. Based on that index, it computes skill frequency, resume match scores, per-job rankings, personal experience matches, and application materials.

From an engineering perspective, I did not directly trust LLM output. I added JSON parsing, Pydantic schema validation, mock response fixtures, and failure-case tests to prevent malformed data from entering downstream analysis. I also built a one-command pipeline with output checks, so the whole workflow from JD input to deliverable generation is reproducible.

## Roadmap

Planned improvements:

- Add more realistic sample JD datasets
- Improve Streamlit interaction and report navigation
- Add pytest-based automated test suite
- Add richer scoring explanations
- Add configurable resume profiles
- Add export options for PDF / DOCX application materials
- Add more LLM providers
- Add GitHub Actions CI
- Package the project as a reusable CLI tool

## License

MIT License