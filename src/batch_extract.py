from pathlib import Path
import subprocess
import sys
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_JD_DIR = PROJECT_ROOT / "data" / "raw_jds"
EXTRACTOR_PATH = PROJECT_ROOT / "src" / "extractor.py"


def build_output_path(raw_jd_path):
    return PROJECT_ROOT / "data" / f"extracted_{raw_jd_path.stem}.json"

def is_valid_extracted_jd(output_path):
    if not output_path.exists():
        return False

    with output_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    job_title = data.get("job_title", "未知")
    company = data.get("company", "未知")

    if job_title == "未知" and company == "未知":
        return False

    return True

def main():
    raw_jd_paths = sorted(RAW_JD_DIR.glob("*.txt"))

    if not raw_jd_paths:
        print("没有找到 raw JD 文件")
        return

    print(f"发现 {len(raw_jd_paths)} 个 JD 文件")
    print("=" * 32)

    for raw_jd_path in raw_jd_paths:
        output_path = build_output_path(raw_jd_path)

        print(f"抽取: {raw_jd_path.name} -> {output_path.name}")

        result = subprocess.run(
            [
                sys.executable,
                str(EXTRACTOR_PATH),
                str(raw_jd_path),
                str(output_path),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError(f"抽取失败: {raw_jd_path.name}")

        if not is_valid_extracted_jd(output_path):
            print(f"跳过无效 JD: {raw_jd_path.name}（岗位名称和公司均为未知）")
            output_path.unlink(missing_ok=True)
            continue

    print()
    print("批量抽取完成")


if __name__ == "__main__":
    main()