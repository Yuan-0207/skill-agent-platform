"""
获取点位信息（地图 POI、设备锚点等）。
"""
from __future__ import annotations


def get_points(args: dict) -> dict:
    message = (args.get("message") or "").strip()
    context = args.get("context") or {}

    # 演示数据：后续接真实地图/室内定位服务
    points = [
        {"id": "meeting_room_a", "name": "会议室 A", "floor": 3},
        {"id": "reception", "name": "前台", "floor": 1},
        {"id": "cafe", "name": "茶水间", "floor": 2},
    ]

    matched = points
    for p in points:
        if p["name"].lower() in message.lower() or p["id"] in message.lower():
            matched = [p]
            break

    return {
        "summary": f"找到 {len(matched)} 个相关点位",
        "points": matched,
        "from_context": context.get("location"),
    }
