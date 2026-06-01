"""
后端 API 网关：对外暴露 HTTP，内部调用 Agent 主入口。
"""
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 将仓库根目录加入 path，以便 import agent / tools
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.main import run_agent  # noqa: E402

app = FastAPI(
    title="CC Skill Agent API",
    version="0.1.0",
    description="前端 App → API → Agent → 技能路由 → Function Calling",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入")
    session_id: str | None = Field(None, description="会话 ID")
    context: dict = Field(default_factory=dict, description="设备/位置等上下文")


class ChatResponse(BaseModel):
    reply: str
    skill_id: str | None = None
    skill_name: str | None = None
    tool_calls: list[dict] = Field(default_factory=list)
    data: dict = Field(default_factory=dict)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = run_agent(
        message=req.message,
        session_id=req.session_id,
        context=req.context,
    )
    return ChatResponse(**result)

