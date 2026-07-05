# Contributing to JobFit Agent

Thanks for your interest in contributing to JobFit Agent.

This project is an AI-powered career analysis pipeline for JD extraction, resume matching, skill gap analysis, and job application material generation.

## Development Setup

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

## Run the Project Locally

Run the full mock pipeline:

    python3 run_all.py

Open the Streamlit app:

    streamlit run app.py

The default LLM mode is mock, so no API key is required for local development.

## Before Submitting Changes

Please run these checks before opening a pull request:

    python3 -m py_compile run_all.py check_outputs.py app.py
    python3 -m compileall src evals
    pytest evals
    JOBFIT_LLM_MODE=mock python3 run_all.py
    python3 check_outputs.py

## LLM Provider Notes

JobFit Agent supports mock, DeepSeek, and OpenAI modes.

Use mock mode for stable local development:

    JOBFIT_LLM_MODE=mock python3 run_all.py

Use real providers only when needed, and never commit API keys.

## Do Not Commit

Please do not commit:

- .env
- .venv/
- __pycache__/
- generated reports under outputs/
- generated standardized JD files under data/processed_jds/
- real API keys or private credentials
- personal data that should not be public

## Pull Request Guidelines

A good pull request should include:

- A clear description of what changed
- Why the change is useful
- How it was tested
- Any limitations or follow-up work

For larger changes, prefer small incremental pull requests over one large rewrite.

## Project Direction

Current priorities include:

- Better scoring explanations
- More robust test coverage
- Cleaner LLM provider abstraction
- Improved Streamlit user experience
- More reusable sample data and examples
- Export support for application materials