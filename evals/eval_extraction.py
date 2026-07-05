import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_PATH = PROJECT_ROOT / "data" / "extracted_bytedance_agent_ops.json"
GOLD_PATH = PROJECT_ROOT / "evals" / "gold_bytedance_agent_ops.json"
REPORT_PATH = PROJECT_ROOT / "outputs" / "eval_report.txt"

EVAL_FIELDS = [
    "technical_skills",
    "data_skills",
    "agent_llm_skills",
    "soft_skills",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_list_field(predicted, gold):
    predicted_set = set(predicted)
    gold_set = set(gold)

    true_positive = predicted_set & gold_set
    false_positive = predicted_set - gold_set
    false_negative = gold_set - predicted_set

    precision = len(true_positive) / len(predicted_set) if predicted_set else 0
    recall = len(true_positive) / len(gold_set) if gold_set else 0

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": sorted(true_positive),
        "false_positive": sorted(false_positive),
        "false_negative": sorted(false_negative),
    }


def main():
    extracted = load_json(EXTRACTED_PATH)
    gold = load_json(GOLD_PATH)

    report_lines = []

    report_lines.append("JD 抽取评测报告")
    report_lines.append("=" * 32)

    for field in EVAL_FIELDS:
        result = evaluate_list_field(
            extracted.get(field, []),
            gold.get(field, []),
        )

        report_lines.append(field)
        report_lines.append("-" * 32)
        report_lines.append(f"Precision: {result['precision']:.0%}")
        report_lines.append(f"Recall: {result['recall']:.0%}")
        report_lines.append(f"F1: {result['f1']:.0%}")
        report_lines.append(f"命中: {result['true_positive']}")
        report_lines.append(f"误抽: {result['false_positive']}")
        report_lines.append(f"漏抽: {result['false_negative']}")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write(report_text)

    print(report_text)
    print(f"评测报告已保存到: {REPORT_PATH}")


if __name__ == "__main__":
    main()