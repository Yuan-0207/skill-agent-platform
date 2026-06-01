# 启动后端 API（需在仓库根目录的 backend 下安装依赖）
$Root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $Root "backend")
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& .\.venv\Scripts\pip install -r requirements.txt -q
& .\.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
