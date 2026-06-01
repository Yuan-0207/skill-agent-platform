# GitHub 仓库创建与推送

## 1. 在 GitHub 网页创建空仓库

1. 打开 https://github.com/new
2. Repository name：`cc-skill-agent-platform`（或你喜欢的名字）
3. **不要**勾选 README / .gitignore / license（保持空仓库）
4. 点击 Create repository

## 2. 本地推送（在本项目根目录执行）

```powershell
cd "d:\游戏\cc-skill-agent-platform"

git init -b main
git add -A
git commit -m "Initial commit: skill agent platform skeleton"

git remote add origin git@github.com:Yuan-0207/cc-skill-agent-platform.git

# 若 22 端口不通，用 SSH 443：
git remote set-url origin ssh://git@ssh.github.com:443/Yuan-0207/cc-skill-agent-platform.git

git push -u origin main
```

将 `Yuan-0207/cc-skill-agent-platform` 换成你的用户名与仓库名。

## 3. Jenkins / CI（可选）

构建步骤建议：

1. `pip install -r backend/requirements.txt`
2. `python -m pytest`（后续补测试）
3. 打包或部署 `uvicorn app.main:app`
