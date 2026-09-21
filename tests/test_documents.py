from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_and_get_document() -> None:
    """创建文档后，可以根据返回的 ID 查回同一篇文档。"""
    payload = {
        "title": "FastAPI 学习笔记",
        "content": "使用 Pydantic 校验输入。",
    }

    create_response = client.post("/documents", json=payload)
    assert create_response.status_code == 201

    created = create_response.json()
    assert created["title"] == payload["title"]
    assert created["content"] == payload["content"]
    assert isinstance(created["id"], str)
    assert created["id"]

    get_response = client.get(f"/documents/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_get_missing_document() -> None:
    """查询不存在的文档时，返回明确的 404。"""
    response = client.get("/documents/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Document not found",
    }