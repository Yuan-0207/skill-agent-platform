# CC Skill Agent Platform

面向「前端 App → 后端 API → Agent → 技能路由 → Function Calling」的分层 Agent 平台骨架。

## 架构总览

```
前端 App
   ↓
后端 API（/api/v1/chat）
   ↓
Agent 主入口（agent/main.py）
   ↓
【技能路由器】 ← 读取 skills/**/SKILL.md（地点、问答、导航、控制…）
   ↓
技能执行器（SkillExecutor）
   ↓
Function Calling（底层工具：获取点位、调用云接口）
   ↓
返回结果给前端
```

## 目录结构

| 目录 | 说明 |
|------|------|
| `frontend/` | 前端 App（占位，可接 Web / 移动端） |
| `backend/` | FastAPI 网关，对外暴露 HTTP API |
| `agent/` | Agent 主入口、技能路由、执行器 |
| `skills/` | 各能力 SKILL.md 配置（可热扩展） |
| `tools/` | Function Calling 工具注册与实现 |
| `docs/` | 架构与 SKILL 格式说明 |

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动后端（含 Agent）

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 调用示例

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"带我去会议室\", \"context\": {}}"
```

## 新增一个技能

1. 在 `skills/<技能名>/` 下新建 `SKILL.md`（参考 `skills/location/SKILL.md`）
2. 在 `tools/registry.py` 注册该技能需要的工具函数
3. 重启后端；路由器会自动扫描并加载

## 推送到 GitHub

1. 在 GitHub 新建空仓库（例如 `cc-skill-agent-platform`）
2. 本地执行：

```bash
git remote add origin git@github.com:<你的用户名>/cc-skill-agent-platform.git
git push -u origin main
```

若 HTTPS/22 端口不稳定，可使用 SSH over 443：

```bash
git remote set-url origin ssh://git@ssh.github.com:443/<你的用户名>/cc-skill-agent-platform.git
git push -u origin main
```

## 文档

- [架构说明](docs/architecture.md)
- [SKILL.md 格式](docs/skill-format.md)
