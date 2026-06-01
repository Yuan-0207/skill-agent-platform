# Skill Agent 前端（Vite + React + TypeScript）

## 开发

```bash
# 终端 1：后端
cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 终端 2：前端
cd frontend
npm install
npm run dev
```

浏览器打开 http://127.0.0.1:5173  
开发模式下 `/api` 会通过 Vite 代理到 `http://127.0.0.1:8000`。

## 生产构建

```bash
npm run build
# 产物在 dist/
```

可选：复制 `.env.example` 为 `.env.production` 并设置 `VITE_API_BASE_URL`。
