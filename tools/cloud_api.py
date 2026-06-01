"""
调用云端业务接口（占位实现，后续替换为真实 HTTP/gRPC）。
"""
from __future__ import annotations


def cloud_query(args: dict) -> dict:
    message = args.get("message") or ""
    return {
        "answer": f"（演示）关于「{message}」的问答结果：当前为 Mock，请接入真实知识库。",
        "summary": "已返回问答结果",
    }


def cloud_navigate(args: dict) -> dict:
    message = args.get("message") or ""
    return {
        "route_id": "mock-route-001",
        "summary": f"（演示）导航指令已生成：{message}",
        "eta_minutes": 5,
    }


def cloud_control(args: dict) -> dict:
    message = args.get("message") or ""
    action = "turn_on" if any(k in message for k in ("开", "打开", "启动")) else "turn_off"
    return {
        "device_id": "mock-device-01",
        "action": action,
        "summary": f"（演示）已下发控制：{action}",
    }
