from pathlib import Path
import subprocess
import sys
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent

REPORT_FILES = {
    "JD-Resume 匹配报告": PROJECT_ROOT / "outputs" / "match_report.md",
    "个人经历匹配报告": PROJECT_ROOT / "outputs" / "experience_match_report.md",
    "岗位分析报告": PROJECT_ROOT / "outputs" / "career_analysis_report.md",
    "简历 Bullet 建议": PROJECT_ROOT / "outputs" / "optimized_resume_bullets.md",
    "Cover Letter": PROJECT_ROOT / "outputs" / "cover_letter.md",
}


def read_text(path):
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def render_report_selector():
    report_name = st.selectbox(
        "选择报告",
        list(REPORT_FILES.keys()),
    )

    report_path = REPORT_FILES[report_name]
    report_text = read_text(report_path)

    st.caption(str(report_path))

    if report_text:
        st.markdown(report_text)
    else:
        st.warning("报告还没有生成，请先运行 python3 run_all.py")


def render_output_status():
    st.subheader("关键产物状态")

    for name, path in REPORT_FILES.items():
        if path.exists():
            st.success(f"{name}: 已生成")
        else:
            st.error(f"{name}: 缺失")

def render_pipeline_runner():
    st.subheader("Pipeline")

    if st.button("运行完整 pipeline"):
        with st.spinner("正在运行 pipeline..."):
            result = subprocess.run(
                [sys.executable, "run_all.py"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        if result.returncode == 0:
            st.success("Pipeline 运行完成")
        else:
            st.error("Pipeline 运行失败")

        with st.expander("查看运行日志"):
            if result.stdout:
                st.text(result.stdout)

            if result.stderr:
                st.text(result.stderr)

def main():
    st.set_page_config(
        page_title="JobFit Agent",
        page_icon="",
        layout="wide",
    )

    st.title("JobFit Agent")
    st.caption("JD 分析、简历匹配、经历匹配与求职材料生成")
    st.info("当前页面读取 outputs 下的报告文件；点击右侧按钮可以重新运行完整 pipeline 并刷新产物。")

    left, right = st.columns([2, 1])

    with left:
        render_report_selector()

    with right:
        render_output_status()
        render_pipeline_runner()


if __name__ == "__main__":
    main()