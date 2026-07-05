import argparse
import re
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_JD_DIR = PROJECT_ROOT / "data" / "raw_jds"


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "_", value)
    value = value.strip("_")
    return value or "manual_jd"


def build_output_path(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"manual_{slugify(name)}_{timestamp}.txt"
    return RAW_JD_DIR / filename


def read_multiline_input():
    print("请粘贴 JD 文本。")
    print("粘贴完成后，单独输入一行 END 并回车保存。")
    print("=" * 32)

    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(description="手动粘贴 JD 并保存到 raw_jds")
    parser.add_argument("--name", default="manual_jd", help="用于生成文件名的岗位或公司名称")
    parser.add_argument("--company", default="未知", help="公司名称")
    parser.add_argument("--city", default="未知", help="城市")
    parser.add_argument("--source", default="手动粘贴", help="JD 来源")
    args = parser.parse_args()

    text = read_multiline_input()

    if len(text) < 50:
        raise SystemExit("JD 文本太短，未保存。")

    RAW_JD_DIR.mkdir(parents=True, exist_ok=True)
    output_path = build_output_path(args.name)
    formatted_text = (
    f"岗位名称：{args.name}\n"
    f"公司：{args.company}\n"
    f"城市：{args.city}\n"
    f"来源：{args.source}\n\n"
    f"{text}\n"
)

    output_path.write_text(formatted_text, encoding="utf-8")

    print()
    print(f"手动 JD 已保存到: {output_path}")


if __name__ == "__main__":
    main()