import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MEMORY_DIR = PROJECT_ROOT / "data" / "memory"
CONVERSATION_HISTORY_PATH = MEMORY_DIR / "conversation_history.json"

REPORT_FILES = {
    "match": OUTPUTS_DIR / "match_report.md",
    "experience": OUTPUTS_DIR / "experience_match_report.md",
    "career": OUTPUTS_DIR / "career_analysis_report.md",
    "resume_bullets": OUTPUTS_DIR / "optimized_resume_bullets.md",
    "greeting": OUTPUTS_DIR / "boss_greeting.txt",
    "cover_letter": OUTPUTS_DIR / "cover_letter.md",
    "deliverable": OUTPUTS_DIR / "deliverables" / "jobfit_deliverable.md",
}

REPORT_KEYWORDS = {
    "match": ["匹配", "分数", "岗位", "适合", "投哪个", "jd-resume", "resume match"],
    "experience": ["经历", "项目", "经验", "案例", "experience"],
    "career": ["分析", "方向", "能力差距", "学习路线", "career"],
    "resume_bullets": ["bullet", "简历优化", "项目描述", "简历"],
    "greeting": ["boss", "招呼", "打招呼", "开场白"],
    "cover_letter": ["cover", "求职信", "自荐信", "申请信"],
    "deliverable": ["交付包", "材料包", "deliverable"],
}

app = FastAPI(
    title="JobFit Agent 求职分析 API",
    description="用于 JD 分析、简历匹配、经历匹配和求职材料生成的 API 服务。",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str


def read_text(path):
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Report not found: {path.name}")

    return path.read_text(encoding="utf-8")


def load_conversation_history():
    if not CONVERSATION_HISTORY_PATH.exists():
        return []

    with CONVERSATION_HISTORY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_conversation_history(history):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    with CONVERSATION_HISTORY_PATH.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def append_conversation_turn(message, selected_report, reply):
    history = load_conversation_history()

    turn = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "selected_report": selected_report,
        "reply": reply,
    }

    history.append(turn)
    save_conversation_history(history)

    return turn


def select_report_name(message):
    normalized_message = message.lower()

    for report_name, keywords in REPORT_KEYWORDS.items():
        if any(keyword.lower() in normalized_message for keyword in keywords):
            return report_name

    return "match"


def build_chat_reply(message, report_name, report_content):
    preview = report_content.strip()

    if len(preview) > 1200:
        preview = preview[:1200] + "\n\n..."

    return (
        "我根据你的问题选择了相关报告进行回答。\n\n"
        f"你的问题：{message}\n\n"
        f"参考报告：{report_name}\n\n"
        "当前结论可以先看这部分内容：\n\n"
        f"{preview}\n\n"
        "如果你想继续，我可以基于这份报告进一步帮你总结投递策略、优化简历表达，"
        "或者生成更具体的求职材料。"
    )


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


@app.post("/chat", summary="对话式求职分析")
def chat(request: ChatRequest):
    report_name = select_report_name(request.message)
    report_path = REPORT_FILES[report_name]
    report_content = read_text(report_path)
    reply = build_chat_reply(
        request.message,
        report_name,
        report_content,
    )
    memory_turn = append_conversation_turn(
        request.message,
        report_name,
        reply,
    )

    return {
        "message": request.message,
        "selected_report": report_name,
        "reply": reply,
        "memory_saved": True,
        "memory_turn": memory_turn,
    }


@app.get("/memory/conversations", summary="查看对话记忆")
def get_conversation_history():
    return {
        "count": len(load_conversation_history()),
        "conversations": load_conversation_history(),
    }


@app.delete("/memory/conversations", summary="清空对话记忆")
def clear_conversation_history():
    save_conversation_history([])

    return {
        "status": "cleared",
        "count": 0,
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