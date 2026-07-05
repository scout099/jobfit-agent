# JobFit Agent Handoff

项目路径：/Users/scout/Desktop/wo/ai-career-agent

## 当前状态

项目已从 AI Career Intelligence Agent / JD 分析 pipeline 升级为 JobFit Agent MVP。

当前完整链路：

JD URL / 手动粘贴 / raw_jds
-> 批量抽取
-> 技能标准化
-> 岗位分析
-> 简历匹配评分
-> 简历 bullet / BOSS 招呼语 / Cover Letter
-> 求职材料交付包
-> run_all.py 一键运行
-> check_outputs.py 产物检查

## 已完成模块

- src/url_loader.py
- src/manual_jd_input.py
- src/extractor.py
- src/batch_extract.py
- src/analyzer.py
- src/extractor_llm.py
- src/report_markdown.py
- src/match_resume.py
- src/generate_resume_bullets.py
- src/generate_greeting.py
- src/generate_cover_letter.py
- src/package_deliverables.py
- evals/test_llm_schema_validation.py
- src/process_jds.py
- src/match_experiences.py
- app.py
- data/experience_library.json

## 关键数据和输出

- data/raw_jds/
- data/skill_config.json
- data/resume_profile.json
- outputs/analysis_report.txt
- outputs/career_analysis_report.md
- outputs/match_report.md
- outputs/optimized_resume_bullets.md
- outputs/boss_greeting.txt
- outputs/cover_letter.md
- outputs/deliverables/jobfit_deliverable.md
- outputs/pipeline_run_report.txt
- data/processed_jds/
- data/processed_jds/index.json
- data/experience_library.json
- outputs/experience_match_report.md

## 当前验证

`python3 run_all.py` 已通过，所有 check_outputs 项均为 OK。
`python3 run_all.py` 已通过，所有 check_outputs 项均为 OK。
Streamlit UI 已可通过 `streamlit run app.py` 打开，并可在页面中运行完整 pipeline。

## 明天继续方向


1. 接入真实 LLM API。
2. 优化 Streamlit UI：结构化展示排名表，不只渲染 Markdown。
3. 增加更多个人经历样本。
4. 让简历 bullet / BOSS 招呼语 / Cover Letter 使用 experience_library。
5. 增加岗位筛选和目标岗位选择功能。

## 当前状态

项目已升级为 JobFit Agent MVP，并完成标准化 JD、具体 JD 匹配、个人经历库和 Streamlit UI MVP。

当前完整链路：

JD URL / 手动粘贴 / raw_jds
-> 批量抽取
-> LLM mock 抽取与 schema 校验
-> processed_jds 标准化 JD
-> 技能标准化
-> 岗位分析
-> 具体 JD-Resume 匹配评分
-> 分岗位匹配排名 / 可信度
-> 个人经历库匹配
-> 简历 bullet / BOSS 招呼语 / Cover Letter
-> 求职材料交付包
-> Streamlit UI 查看报告并一键运行 pipeline
-> run_all.py 一键运行
-> check_outputs.py 产物检查


## 当前新增进度

今天已完成以下升级：

- 新增 processed_jds 标准化 JD 数据层。
- 使用 Pydantic JDInfo schema 统一 JD 结构。
- analyzer.py 已优先读取 data/processed_jds/index.json。
- match_resume.py 已改为基于具体 JD 技能评分。
- 匹配报告已包含分岗位排名、目标技能数、已匹配数、缺口数和可信度。
- 新增 data/experience_library.json 个人经历库。
- 新增 src/match_experiences.py，生成个人经历匹配报告。
- 简历 bullet、BOSS 招呼语、Cover Letter 已接入 experience_library。
- package_deliverables.py 已把个人经历匹配报告打入最终交付包。
- 新增 app.py Streamlit UI，可查看报告并一键运行 pipeline。
- extractor_llm.py 已支持 mock / openai / deepseek 三种 LLM 模式。
- DeepSeek API 模式已跑通完整 pipeline。
- schema 失败用例已修复为强制读取指定 mock 文件，不受 JOBFIT_LLM_MODE 影响。

## 当前完整链路

JD URL / 手动粘贴 / raw_jds
-> 批量抽取
-> LLM mock / DeepSeek / OpenAI 抽取与 schema 校验
-> processed_jds 标准化 JD
-> 技能标准化
-> 岗位分析
-> 具体 JD-Resume 匹配评分
-> 分岗位匹配排名 / 可信度
-> 个人经历库匹配
-> 简历 bullet / BOSS 招呼语 / Cover Letter
-> 求职材料交付包
-> Streamlit UI 查看报告并一键运行 pipeline
-> run_all.py 一键运行
-> check_outputs.py 产物检查

## LLM 运行模式

默认 mock 模式：

`python3 run_all.py`

DeepSeek API 模式：

`export DEEPSEEK_API_KEY="你的 DeepSeek API key"`

`JOBFIT_LLM_MODE=deepseek python3 run_all.py`

OpenAI API 模式：

`export OPENAI_API_KEY="你的 OpenAI API key"`

`JOBFIT_LLM_MODE=openai python3 run_all.py`

当前 DeepSeek 默认模型：

`deepseek-v4-flash`

OpenAI 默认模型：

`gpt-4.1-mini`

注意：API key 不要写入代码或提交 Git。

## 当前验证

以下命令已通过：

`python3 run_all.py`

`JOBFIT_LLM_MODE=deepseek python3 run_all.py`

验证结果：

- 所有 check_outputs 项均为 OK。
- LLM schema 失败用例测试通过。
- DeepSeek API 模式完整 pipeline 已运行完成。
- 最终 deliverable 已包含个人经历匹配报告。
- Streamlit UI 可通过 `streamlit run app.py` 打开，并可在页面中运行完整 pipeline。

## 下一步方向

1. 优化 Streamlit UI：结构化展示排名表，不只渲染 Markdown。
2. 增加更多个人经历样本，让 experience_library 更像真实经历库。
3. 让用户在 UI 中选择目标岗位，再按目标岗位生成材料。
4. 增加真实 JD 粘贴 / URL 输入入口，并从 UI 触发抽取。
5. 增加 LLM provider 配置说明或 .env.example。