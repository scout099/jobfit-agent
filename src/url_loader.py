import argparse
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_JD_DIR = PROJECT_ROOT / "data" / "raw_jds"


def build_output_path(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_") or "unknown_site"
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    filename = f"url_{domain}_{url_hash}.txt"
    return RAW_JD_DIR / filename


def clean_text(text):
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def fetch_url_text(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    body_text = soup.get_text("\n", strip=True)

    combined_text = clean_text(f"{title}\n\n{body_text}")
    return combined_text


def save_raw_jd(text, output_path):
    RAW_JD_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="从公开 URL 抓取 JD 文本")
    parser.add_argument("url", help="岗位 JD 的公开网页链接")
    args = parser.parse_args()

    try:
        text = fetch_url_text(args.url)
    except Exception as error:
        raise SystemExit(
            "URL 抓取失败。可能原因：页面需要登录、动态渲染、反爬或网络异常。\n"
            f"错误信息: {error}\n"
            "兜底方案：手动复制 JD 到 data/raw_jds/xxx.txt，再运行 batch_extract.py。"
        )

    if len(text) < 100:
        raise SystemExit(
            "抓取到的正文太短，可能不是有效 JD 页面。\n"
            "建议手动复制 JD 到 data/raw_jds/xxx.txt。"
        )

    output_path = build_output_path(args.url)
    save_raw_jd(text, output_path)

    print(f"JD 网页文本已保存到: {output_path}")


if __name__ == "__main__":
    main()