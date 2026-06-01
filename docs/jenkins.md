# Jenkins Pipeline 配置说明

仓库根目录已包含 `Jenkinsfile`，适用于 **Pipeline script from SCM**。

## 1. 创建 Jenkins 任务

1. 新建任务 → 名称：`skill-agent-platform` → 选 **Pipeline**
2. **Pipeline** → Definition：**Pipeline script from SCM**
3. SCM：**Git**
4. Repository URL：`git@github.com:Yuan-0207/skill-agent-platform.git`  
   （或 SSH 443：`ssh://git@ssh.github.com:443/Yuan-0207/skill-agent-platform.git`）
5. Branch：`*/main`
6. Script Path：`Jenkinsfile`

## 2. 构建机环境要求

| 组件 | 版本建议 |
|------|----------|
| Python | 3.10+ |
| Node.js | 18+（推荐 20 LTS） |
| npm | 随 Node 安装 |
| Git | 任意较新版本 |

Windows 节点：确保 `python`、`npm` 在 PATH 中。  
Linux 节点：同上。

## 3. Pipeline 阶段说明

| 阶段 | 动作 |
|------|------|
| Checkout | 拉取代码 |
| Backend | `pip install` + `pytest backend/tests` |
| Frontend | `npm install` + `npm run build` |
| Post | 归档 `frontend/dist/**`，发布 JUnit 报告 |

## 4. 可选：部署前端静态资源

构建成功后 `frontend/dist/` 即为可部署目录，可：

- 拷贝到 Nginx / IIS 静态目录
- 或上传到对象存储 + CDN

生产环境需在构建前设置：

```bash
# frontend/.env.production
VITE_API_BASE_URL=https://your-api-domain.com
```

## 5. 本地模拟 Jenkins 步骤

```powershell
cd d:\游戏\cc-skill-agent-platform
python -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
$env:PYTHONPATH = (Get-Location).Path
python -m pytest backend/tests -q

cd frontend
npm install
npm run build
```

## 6. 常见问题

- **pytest 找不到 agent 模块**：必须设置 `PYTHONPATH` 为仓库根目录（Pipeline 已处理）
- **npm 不在 PATH**：在 Jenkins 全局工具配置里安装 NodeJS 插件并绑定版本
- **前端请求 API 失败**：开发用 `npm run dev`（Vite 代理到 8000）；生产需配置 `VITE_API_BASE_URL`
