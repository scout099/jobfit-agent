def recommend_learning_path(tiers, gap_report):
    matched_skills = gap_report["matched_skills"]
    missing_skills = gap_report["missing_skills"]

    print("学习路线建议")
    print("=" * 32)

    must_learn = tiers["第一梯队：必须优先学"]
    should_learn = tiers["第二梯队：建议重点补"]

    print("1. 第一阶段：打基础")
    focus_skills = set(gap_report["focus_skills"])

    priority_missing = [
        item
        for item in gap_report["missing_skill_items"]
        if item["skill"] in focus_skills
    ][:3]

    if priority_missing:
        print("优先补齐以下能力：")
        for item in priority_missing:
            print(f"- {item['skill']}（优先级分数：{item['score']:.1f}）")
    else:
        print("第一梯队能力已经基本具备，可以进入项目深化。")
    print("目标：能读懂 JD，能写简单脚本，能理解 Agent = 模型 + 工具 + 状态 + 反馈循环。")
    print()

    print("2. 第二阶段：做一个最小项目")
    print("项目：AI JD 分析 Agent")
    print("目标：输入岗位 JD，输出结构化 JSON、技能频率和学习建议。")
    print()

    print("3. 第三阶段：补强方向能力")
    if should_learn:
        print("根据当前 JD 样本，建议继续补：")
        for item in should_learn:
            skill = item.split(":")[0]
            print(f"- {skill}")
    else:
        print("当前样本没有明显的第二梯队能力。")
    print()

    print("4. 第四阶段：扩展到 RAG 和评测")
    print("目标：把更多 JD 放进知识库，让系统能回答“某类岗位最需要什么能力”，并评估抽取准确率。")