"""
Function Calling 注册表：技能执行器通过名称调用底层工具。
"""
from __future__ import annotations

from typing import Any, Callable

from tools.cloud_api import cloud_control, cloud_navigate, cloud_query
from tools.points import get_points

ToolFn = Callable[[dict], Any]

_REGISTRY: dict[str, ToolFn] = {
    "get_points": get_points,
    "cloud_query": cloud_query,
    "cloud_navigate": cloud_navigate,
    "cloud_control": cloud_control,
}


def register_tool(name: str, fn: ToolFn) -> None:
    _REGISTRY[name] = fn


def call_tool(name: str, args: dict) -> Any:
    fn = _REGISTRY.get(name)
    if fn is None:
        return {"error": f"unknown_tool:{name}"}
    return fn(args)


def list_tools() -> list[str]:
    return sorted(_REGISTRY.keys())
