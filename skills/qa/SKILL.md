---
id: qa
name: 问答
description: 通用知识问答与业务 FAQ
triggers:
  - 什么
  - 为什么
  - 怎么
  - 吗
  - ？ 
tools:
  - cloud_query
priority: 3
response_template: "{result}"
---

对接知识库 / RAG / 大模型 API 时，主要扩展 `cloud_query` 工具实现。
