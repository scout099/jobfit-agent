# AI Career Intelligence Agent 项目复盘

## 1. 我做了什么

这个项目从 AI Agent / 数据智能相关实习 JD 出发，构建了一条完整的信息抽取与分析 pipeline。

核心流程是：

原始 JD
-> 规则抽取
-> LLM 抽取模拟
-> JSON 校验
-> 多来源结构化数据合并
-> 来源标记
-> 可信来源去重
-> 技能频率分析
-> 个人能力差距分析
-> 学习路线推荐
-> 抽取质量评测
-> 规则 vs LLM 对比报告
-> pipeline 产物检查

最终项目可以通过一条命令运行：

python3 run_all.py

## 2. 这个项目解决什么问题

很多人在学习 AI Agent 时，容易只停留在概念层面：

- 不知道真实岗位到底要什么能力
- 不知道 Python、SQL、LLM、RAG、Agent 工具调用之间的关系
- 不知道应该做什么项目证明自己
- 不知道怎样判断一个抽取系统做得准不准

这个项目把真实 JD 转成可分析的数据，然后输出：

- 岗位高频技能
- 技能优先级
- 个人能力缺口
- 学习路线建议
- 项目方向建议
- 抽取评测结果

## 3. 为什么它像一个 AI Agent / 数据智能项目

它不是简单地调用一次 LLM，而是包含了工程化 AI 项目的多个关键环节：

1. 数据输入：原始 JD 文本和结构化 JD。
2. 信息抽取：规则抽取和 LLM 抽取。
3. 数据清洗：技能标准化、去重、来源标记。
4. 分析推理：技能频率、权重分数、分层优先级。
5. 个性化输出：根据个人能力生成学习路线。
6. 评测机制：用 gold 标准答案计算 Precision / Recall / F1。
7. 可复现 pipeline：用 run_all.py 一键运行完整流程。
8. 产物检查：用 check_outputs.py 验证关键输出文件。

## 4. 我学到的核心概念

### 4.1 结构化抽取

原始 JD 是非结构化文本，机器不方便直接分析。

所以第一步要把它变成 JSON，包含岗位名称、公司、技术技能、数据技能、Agent/LLM 技能、软技能等字段。

这一步让我理解：很多 AI 应用的本质，是把模糊文本变成稳定结构。

### 4.2 技能标准化

同一个能力可能有很多写法：

- 大语言模型 / LLM / 大模型
- AI智能体 / Agent / AI Agent
- 提示词 / Prompt / Prompt Engineering

如果不标准化，后面的统计会被稀释。

### 4.3 规则抽取和 LLM 抽取的区别

规则抽取：

- 优点：稳定、便宜、可控、容易 debug
- 缺点：不擅长处理隐含表达和复杂语言

LLM 抽取：

- 优点：灵活，适合复杂 JD
- 缺点：可能输出不合法 JSON，可能幻觉，需要校验和评测

所以更合理的系统不是只用 LLM，而是：

规则能解决的先用规则。
复杂表达交给 LLM。
LLM 输出必须校验。
所有抽取结果都要评测。

### 4.4 评测意识

项目里不只看“能不能抽出来”，还比较：

预测结果 vs gold 标准答案

并计算：

- Precision：抽出来的有多少是对的
- Recall：标准答案里有多少被抽到了
- F1：综合 Precision 和 Recall

这让我理解了 AI 项目里 eval 的重要性。

### 4.5 可复现 pipeline

一开始项目是多个脚本分散运行。

后来用 run_all.py 串起来，形成完整流程：

python3 run_all.py

这让项目从 demo 变成了可复现工程。

## 5. 当前项目亮点

- 有真实 JD 场景
- 有规则抽取
- 有 LLM 抽取模拟
- 有 JSON 校验
- 有多来源数据合并
- 有来源可信度去重
- 有个性化学习路线推荐
- 有 Precision / Recall / F1 评测
- 有规则 vs LLM 对比报告
- 有一键运行 pipeline
- 有关键产物检查

## 6. 当前局限

- 目前 JD 样本数量还少。
- LLM 部分还是 mock 输出，没有接真实 API。
- JSON 校验还只是 json.loads()，没有严格 schema 校验。
- 技能词表还需要继续扩充。
- 还没有 Web UI。
- 还没有支持上传任意 JD 文本。
- 推荐逻辑还比较简单。

## 7. 下一步可以怎么做

优先级从高到低：

1. 增加更多真实 JD 样本。
2. 把技能词表扩展成独立配置文件。
3. 增加 JSON schema 校验。
4. 接入真实 LLM API。
5. 支持输入任意 JD 文本。
6. 增加岗位相似度检索。
7. 做一个简单 Web UI。
8. 把项目整理成 GitHub repo。

## 8. 面试时可以怎么讲

可以这样介绍：

我做了一个 AI Career Intelligence Agent，用来分析 AI Agent 和数据智能相关实习岗位。它可以从 JD 中抽取技能要求，标准化技能名称，统计高频技能，并结合我的个人能力生成学习路线。项目里同时实现了规则抽取和 LLM 抽取模拟，并用 gold 标准答案计算 Precision、Recall 和 F1，比较两种抽取方式的效果。最后我用 run_all.py 把完整流程做成可复现 pipeline，并加入关键输出文件检查。

如果面试官问技术细节，可以展开：

- 为什么要做技能标准化
- 为什么不能只依赖 LLM
- 怎么做抽取评测
- 去重时为什么要考虑来源可信度
- 如何从 demo 变成 pipeline

## 9. 今天的收获

今天最重要的收获不是写了多少代码，而是理解了一个 AI 数据项目的基本骨架：

数据 -> 抽取 -> 清洗 -> 分析 -> 推荐 -> 评测 -> 复现

这条链路可以迁移到很多项目：

- 简历分析 Agent
- 招聘 JD 匹配 Agent
- 论文信息抽取 Agent
- 客服工单分析 Agent
- 企业知识库问答系统
- RAG 评测系统

## JobFit Agent MVP 阶段复盘

### 当前定位

项目已从最初的 AI Career Intelligence Agent / JD 分析 pipeline，升级为 JobFit Agent MVP。

当前系统目标是：JD 获取 -> JD 抽取 -> 技能标准化 -> 岗位分析 -> 简历匹配 -> 求职材料生成 -> 一键交付包。

### 已完成能力

- 支持 raw JD 文本输入。
- 支持 URL 自动抓取公开网页 JD。
- 针对 BOSS 等反爬或动态页面，提供手动粘贴兜底机制。
- 手动粘贴 JD 时自动补齐岗位名称、公司、城市和来源元信息。
- 支持批量抽取 data/raw_jds/*.txt。
- 支持技能词表配置化和同义词标准化。
- 支持多来源 JD 合并、去重和统一分析。
- 支持 LLM mock 抽取、JSON schema 校验和失败用例测试。
- 支持 Precision / Recall / F1 评测规则抽取和 LLM 抽取。
- 支持生成岗位技能分析报告和 Markdown 报告。
- 支持结构化简历画像。
- 支持 JD-Resume 匹配评分和可解释匹配报告。
- 支持生成简历 bullet、BOSS 招呼语、Cover Letter。
- 支持将求职材料打包成统一交付文件。
- 支持 run_all.py 一键运行完整 pipeline。
- 支持 check_outputs.py 检查关键产物是否生成。

### 当前项目阶段

当前属于 MVP 阶段，重点是跑通完整链路，而不是堆复杂技术栈。

已经跑通的核心链路是：岗位 JD / URL / 手动粘贴 -> raw_jds -> extracted JSON -> analysis report -> resume match report -> resume bullets / greeting / cover letter -> deliverable package。

### 当前局限

- URL 抓取只能处理公开静态网页，对 BOSS、LinkedIn、猎聘等动态或登录页面仍需手动粘贴兜底。
- JD 抽取主要依赖规则和 mock LLM，还没有接真实 LLM API。
- 简历匹配评分仍是规则版，还没有结合真实岗位权重动态计算。
- 简历生成目前是模板化输出，还没有基于不同 JD 自动改写每一段经历。
- 还没有 Web UI。
- 还没有 DOCX / PDF 导出。
- 还没有真实 RAG 经历库。

### 下一阶段方向

- 接入真实 LLM API，用于 JD 结构化抽取和材料生成。
- 增加 processed_jds/，用 Pydantic schema 保存标准化 JD。
- 改造匹配评分，让分数来自具体 JD，而不是固定技能列表。
- 增加个人经历库，用于生成更真实的简历 bullet。
- 增加 Streamlit UI，支持输入 URL、粘贴 JD、查看报告和下载材料。
- 支持导出 DOCX / PDF。
- 后续再考虑 LangGraph、RAG、向量库和多 Agent 工作流。