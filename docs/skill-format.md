# SKILL.md 格式说明

每个技能目录下放置一个 `SKILL.md`，供技能路由器读取。

## 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 技能唯一 ID，如 `location` |
| `name` | string | 中文显示名 |
| `description` | string | 能力描述 |
| `triggers` | string[] | 触发关键词/短语 |
| `tools` | string[] | 依赖的工具名（需在 `tools/registry.py` 注册） |

## 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `priority` | number | 路由优先级，越大越优先，默认 0 |
| `response_template` | string | 回复模板，支持 `{result}` 占位 |

## 示例

```yaml
---
id: navigation
name: 导航
description: 根据用户目标地点规划路径或下发导航指令
triggers:
  - 去
  - 导航
  - 带我去
  - 怎么走
tools:
  - get_points
  - cloud_navigate
priority: 10
response_template: "已为你规划：{result}"
---
```

正文（`---` 下方）可写更详细的提示词、边界条件，供后续接 LLM 时使用。
