"""
Agent 主入口：编排 技能路由 → 技能执行 → 返回结构化结果。
"""
from __future__ import annotations

from pathlib import Path

from agent.executor import SkillExecutor
from agent.router import SkillRouter

_SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"
_router = SkillRouter(_SKILLS_ROOT)
_executor = SkillExecutor()


def run_agent(
    message: str,
    session_id: str | None = None,
    context: dict | None = None,
) -> dict:
    ctx = context or {}
    route = _router.route(message)

    if route is None:
        return {
            "reply": "暂未识别你的意图，请换个说法试试。",
            "skill_id": None,
            "skill_name": None,
            "tool_calls": [],
            "data": {"session_id": session_id},
        }

    executed = _executor.execute(route, message, ctx)
    return {
        "reply": executed.reply,
        "skill_id": route.skill_id,
        "skill_name": route.skill_name,
        "tool_calls": executed.tool_calls,
        "data": {**executed.data, "session_id": session_id},
    }
