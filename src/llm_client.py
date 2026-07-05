import os
from pathlib import Path


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def read_text(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return file.read()


def call_openai_llm(request_text):
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("未设置 OPENAI_API_KEY，无法使用 openai 模式")

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError("未安装 openai，请先运行: pip install openai") from error

    client = OpenAI()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=request_text,
    )

    return response.output_text, f"已使用 OpenAI API 模式，模型: {OPENAI_MODEL}"


def call_deepseek_llm(request_text):
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("未设置 DEEPSEEK_API_KEY，无法使用 deepseek 模式")

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError("未安装 openai，请先运行: pip install openai") from error

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=DEEPSEEK_BASE_URL,
    )

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": request_text,
                }
            ],
            response_format={
                "type": "json_object",
            },
            stream=False,
        )
    except Exception as error:
        raise RuntimeError(
            "DeepSeek API 调用失败。请检查 DEEPSEEK_API_KEY、余额/quota、模型名，"
            "或改用默认 mock 模式运行: python3 src/extractor_llm.py"
        ) from error

    return response.choices[0].message.content, f"已使用 DeepSeek API 模式，模型: {DEEPSEEK_MODEL}"


def call_llm_response(request_text, mock_response_path):
    llm_mode = os.getenv("JOBFIT_LLM_MODE", "mock")

    if llm_mode == "openai":
        return call_openai_llm(request_text)

    if llm_mode == "deepseek":
        return call_deepseek_llm(request_text)

    return read_text(mock_response_path), "已使用 mock LLM 模式"