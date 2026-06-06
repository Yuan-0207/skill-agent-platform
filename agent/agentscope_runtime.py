import inspect
import json
import os
from dotenv import load_dotenv
from collections.abc import Awaitable, Callable
from importlib import import_module
from typing import Any
#agentscope 2.0
from agentscope.model import DashScopeChatModel
from agentscope.credential import DashScopeCredential
from agentscope.tool import Bash, Read, Write, Edit, FunctionTool
from agentscope.skill import LocalSkillLoader
from agentscope.permission import (
    PermissionContext, PermissionMode, PermissionRule, PermissionBehavior
)

# 加载 .env 文件中的环境变量
load_dotenv()

SYSTEM_PROMPT = """
你是专业的助手，会根据用户的不同需求来加载对应的技能解决问题
"""

class AgentScopeUnavailable(RuntimeError):
    pass


def _load_attr(candidates: list[tuple[str, str]]) -> Any:
    errors: list[str] = []
    for module_name, attr_name in candidates:
        try:
            module = import_module(module_name)
            return getattr(module, attr_name)
        except (ImportError, AttributeError) as exc:
            errors.append(f"{module_name}.{attr_name}: {exc}")
    raise AgentScopeUnavailable(
        "未找到兼容的 AgentScope API，请先安装或升级 agentscope。\n"
        + "\n".join(errors)
    )


def _call_with_supported_kwargs(factory: Callable[..., Any], **kwargs: Any) -> Any:
    """仅传入当前 AgentScope 版本构造函数支持的参数。"""
    signature = inspect.signature(factory)
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return factory(**kwargs)

    supported = {
        key: value
        for key, value in kwargs.items()
        if key in signature.parameters and value is not None
    }
    return factory(**supported)


def _build_openai_compatible_model() -> Any:
    """构建 model 模型客户端。"""
    return DashScopeChatModel(
        credential=DashScopeCredential(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        ),
        model="gpt-5.4",
    )


def _build_toolkit() -> Any:
    """注册业务工具函数。"""
    toolkit_cls = _load_attr(
        [
            ("agentscope.tool", "Toolkit"),
            ("agentscope.tools", "Toolkit"),
        ]
    )
    # 自定义工具
    # customer_tool = FunctionTool(getxxx)
    
    # 扫描SKILL目录
    loader = LocalSkillLoader(
        directory="../skills",
        scan_subdir=True,
    )
    
    toolList = [Bash()]
    toolkit = toolkit_cls(
        tools=toolList,
        skills_or_loaders=[loader]
    )

    return toolkit


def _build_agent() -> Any:
    """构建单个用户会话使用的地点识别 Agent。"""
    agent_cls = _load_attr(
        [
            ("agentscope.agent", "Agent"),
            ("agentscope.agents", "Agent"),
        ]
    )

    return _call_with_supported_kwargs(
        agent_cls,
        name="location_agent",
        sys_prompt=SYSTEM_PROMPT,
        system_prompt=SYSTEM_PROMPT,
        model=_build_openai_compatible_model(),
        toolkit=_build_toolkit(),
    )


_agents: dict[str, Any] = {}


def get_agent(user_id: str) -> Any:
    """按用户缓存 Agent，避免不同用户共享上下文。"""
    if user_id not in _agents:
        _agents[user_id] = _build_agent()
    return _agents[user_id]

# 暴露执行的接口
async def run_agent(user_id: str, user_input: str) -> str:
    """执行 Agent,并统一提取字符串结果。"""
    agent = get_agent(user_id)
    response = agent.reply(user_input)
    if isinstance(response, Awaitable):
        response = await response

    if hasattr(response, "content"):
        content = response.content
    elif isinstance(response, dict):
        content = response.get("content", response)
    else:
        content = response

    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False)

