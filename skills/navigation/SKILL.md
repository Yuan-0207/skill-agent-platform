---
id: navigation
name: 导航
description: 根据目标地点生成导航路径或下发导航指令
triggers:
  - 去
  - 导航
  - 带我去
  - 怎么走
  - 路线
tools:
  - get_points
  - cloud_navigate
priority: 10
response_template: "{result}"
---

先 `get_points` 解析目标，再 `cloud_navigate` 生成路线。
