from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RULE_REPORT_PATH = PROJECT_ROOT / "outputs" / "eval_report.txt"
LLM_REPORT_PATH = PROJECT_ROOT / "outputs" / "eval_llm_report.txt"
COMPARISON_REPORT_PATH = PROJECT_ROOT / "outputs" / "eval_comparison_report.txt"


def read_text(path):
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def main():
    rule_report = read_text(RULE_REPORT_PATH)
    llm_report = read_text(LLM_REPORT_PATH)

    comparison_report = f"""规则抽取 vs LLM 抽取评测对比
================================

一、规则抽取评测
--------------------------------
{rule_report}

二、LLM 抽取评测
--------------------------------
{llm_report}

三、初步结论
--------------------------------
当前 mock LLM 输出与 gold 标准答案高度一致，因此 LLM 抽取评测结果表现很好。

但在真实系统里，不能只看一次结果。后续需要重点比较：

1. 规则抽取是否漏掉隐含表达。
2. LLM 抽取是否产生不存在的技能。
3. LLM 输出是否始终符合 JSON schema。
4. 两种方法在更多 JD 样本上的稳定性。
"""

    COMPARISON_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with COMPARISON_REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write(comparison_report)

    print(comparison_report)
    print(f"对比报告已保存到: {COMPARISON_REPORT_PATH}")


if __name__ == "__main__":
    main()