import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

REPORT_FILES = {
    "match": OUTPUTS_DIR / "match_report.md",
    "experience": OUTPUTS_DIR / "experience_match_report.md",
    "career": OUTPUTS_DIR / "career_analysis_report.md",
    "resume_bullets": OUTPUTS_DIR / "optimized_resume_bullets.md",
    "greeting": OUTPUTS_DIR / "boss_greeting.txt",
    "cover_letter": OUTPUTS_DIR / "cover_letter.md",
    "deliverable": OUTPUTS_DIR / "deliverables" / "jobfit_deliverable.md",
}

app = FastAPI(
    title="JobFit Agent 求职分析 API",
    description="用于 JD 分析、简历匹配、经历匹配和求职材料生成的 API 服务。",
    version="0.1.0",
)


def read_text(path):
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Report not found: {path.name}")

    return path.read_text(encoding="utf-8")


@app.get("/health", summary="健康检查")
def health_check():
    return {
        "status": "ok",
        "service": "jobfit-agent-api",
    }


@app.get("/reports", summary="查看报告列表")
def list_reports():
    return {
        "reports": [
            {
                "name": name,
                "path": str(path.relative_to(PROJECT_ROOT)),
                "exists": path.exists(),
            }
            for name, path in REPORT_FILES.items()
        ]
    }


@app.get("/reports/{report_name}", summary="读取指定报告")
def get_report(report_name):
    if report_name not in REPORT_FILES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown report: {report_name}",
        )

    path = REPORT_FILES[report_name]

    return {
        "name": report_name,
        "path": str(path.relative_to(PROJECT_ROOT)),
        "content": read_text(path),
    }


@app.post("/pipeline/run", summary="运行完整 pipeline")
def run_pipeline():
    result = subprocess.run(
        [sys.executable, "run_all.py"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Pipeline failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )

    return {
        "status": "completed",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }