---
id: location
name: 地点查询
description: 查询附近点位、当前位置相关信息
triggers:
  - 在哪
  - 位置
  - 地点
  - 附近
  - 点位
tools:
  - get_points
priority: 5
response_template: "{result}"
---

用于回答「我在哪」「附近有什么」类问题。可结合 `context.location` 返回更精确结果。
