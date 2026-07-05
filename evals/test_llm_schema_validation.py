import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BAD_RESPONSE_PATH = PROJECT_ROOT / "outputs" / "llm_response_bad.json"


def main():
    result = subprocess.run(
        [
            sys.executable,
            "src/extractor_llm.py",
            str(BAD_RESPONSE_PATH),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    combined_output = result.stdout + result.stderr

    if result.returncode == 0:
        raise AssertionError("坏 LLM 输出不应该通过 schema 校验")

    expected_messages = [
        "字段类型错误: business_scenario 应该是 list",
        "缺少字段: project_ideas",
    ]

    for message in expected_messages:
        if message not in combined_output:
            raise AssertionError(f"没有找到预期错误信息: {message}")

    print("LLM schema 失败用例测试通过")


if __name__ == "__main__":
    main()