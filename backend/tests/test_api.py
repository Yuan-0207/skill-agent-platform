"""API 冒烟测试，供 Jenkins / 本地 CI 使用。"""
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat_navigation():
    r = client.post(
        "/api/v1/chat",
        json={"message": "带我去会议室", "context": {}},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["skill_id"] == "navigation"
    assert "reply" in body and body["reply"]
