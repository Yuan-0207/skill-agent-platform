# 前端 App（占位）

本目录预留给前端工程（Web / React Native / 原生 App 等）。

## 对接方式

调用后端统一接口：

```
POST /api/v1/chat
Content-Type: application/json

{
  "message": "带我去会议室",
  "session_id": "optional-uuid",
  "context": {
    "location": { "lat": 0, "lng": 0 }
  }
}
```

## 响应示例

```json
{
  "reply": "（演示）导航指令已生成：带我去会议室",
  "skill_id": "navigation",
  "skill_name": "导航",
  "tool_calls": [...],
  "data": { "route_id": "mock-route-001", "eta_minutes": 5 }
}
```

后续可在此目录初始化 Vite + React 或你的移动端工程。
