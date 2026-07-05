from pathlib import Path
import json
import sys

from llm_client import call_llm_response
from llm_schema import validate_llm_json_response

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROMPT_PATH = PROJECT_ROOT / "prompts" / "extract_jd_llm.md"
RAW_JD_PATH = PROJECT_ROOT / "data" / "raw_jds" / "bytedance_agent_ops.txt"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "llm_request_preview.txt"
MOCK_RESPONSE_PATH = PROJECT_ROOT / "outputs" / "llm_response_mock.json"
VALIDATED_OUTPUT_PATH = PROJECT_ROOT / "data" / "llm_extracted_jd.json"


def read_text(path):
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def build_llm_request(prompt, jd_text):
    return f"""{prompt}

---

以下是需要抽取的岗位 JD：

{jd_text}
"""


def save_preview(request_text):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        file.write(request_text)


def save_validated_output(extracted):
    with VALIDATED_OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(extracted, file, ensure_ascii=False, indent=2)


def main():
    prompt = read_text(PROMPT_PATH)
    jd_text = read_text(RAW_JD_PATH)

    request_text = build_llm_request(prompt, jd_text)
    save_preview(request_text)

    if len(sys.argv) > 1:
        mock_response_path = Path(sys.argv[1])
        response_text = read_text(mock_response_path)
        print(f"已使用指定 mock LLM 文件: {mock_response_path}")
    else:
        response_text, mode_message = call_llm_response(
            request_text,
            MOCK_RESPONSE_PATH,
        )
        print(mode_message)

    validated_output = validate_llm_json_response(response_text)
    save_validated_output(validated_output)

    print(request_text)
    print(f"LLM 请求预览已保存到: {OUTPUT_PATH}")
    print(f"LLM 校验后结果已保存到: {VALIDATED_OUTPUT_PATH}")


if __name__ == "__main__":
    main()