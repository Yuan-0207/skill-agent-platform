"""
技能执行器：按 SKILL 声明调用 tools 注册表中的 Function。
"""
from __future__ import annotations

from dataclasses import dataclass, field

from agent.router import SkillRoute
from tools.registry import call_tool


@dataclass
class ExecuteResult:
    reply: str
    tool_calls: list[dict] = field(default_factory=list)
    data: dict = field(default_factory=dict)


class SkillExecutor:
    def execute(self, route: SkillRoute, message: str, context: dict) -> ExecuteResult:
        tool_calls: list[dict] = []
        merged_data: dict = {"skill_id": route.skill_id}

        for tool_name in route.tools:
            args = {"message": message, "context": context, "skill_id": route.skill_id}
            result = call_tool(tool_name, args)
            tool_calls.append({"name": tool_name, "args": args, "result": result})
            if isinstance(result, dict):
                merged_data.update(result)

        summary = merged_data.get("summary") or merged_data.get("answer") or str(merged_data)
        reply = route.response_template.format(result=summary)

        return ExecuteResult(reply=reply, tool_calls=tool_calls, data=merged_data)
