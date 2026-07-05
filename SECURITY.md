# Security Policy

## Supported Versions

This project is currently in MVP stage. Security fixes are applied to the main branch.

## Reporting a Security Issue

If you discover a security issue, please do not open a public issue with sensitive details.

Instead, contact the maintainer privately through GitHub profile contact information, or open a minimal issue that describes the category of the problem without exposing secrets, tokens, personal data, or exploit details.

## API Keys and Secrets

JobFit Agent supports mock, DeepSeek, and OpenAI LLM modes.

Never commit real API keys or credentials.

Do not commit:

- .env
- API keys
- access tokens
- private SSH keys
- personal credentials
- private resumes
- private job application records

Use .env.example as a template only. Local .env files should stay on your machine and are ignored by Git.

## Personal Data

This project may process resume-like profiles, job descriptions, and application materials.

Before publishing changes, review sample data carefully and remove anything that should not be public, including:

- real phone numbers
- real addresses
- private email addresses
- private application notes
- private company communications
- sensitive resume details

## Generated Outputs

Most generated files under outputs/ are ignored by Git.

Before committing, check the staged files:

    git status --short
    git diff --cached --name-only

Do not commit generated reports if they contain private information.

## Safe Local Development

For stable local development, use mock mode:

    JOBFIT_LLM_MODE=mock python3 run_all.py

Only use real LLM providers when needed. If using real providers, keep API keys in environment variables or a local .env file that is not committed.

## Dependency Security

Dependencies are listed in requirements.txt. Review dependency updates before merging them, especially packages related to LLM clients, web loading, parsing, and document generation.