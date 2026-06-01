---
id: control
name: 设备控制
description: 控制灯光、空调、开关等设备
triggers:
  - 开
  - 关
  - 打开
  - 关闭
  - 控制
  - 空调
  - 灯
tools:
  - cloud_control
priority: 8
response_template: "{result}"
---

通过 `cloud_control` 调用 IoT / 智能家居云端接口。
