from fastapi.testclient import TestClient
# 利用已写好的app来测试
from app.main import app

# 为我的应用创建测试客户端
client = TestClient(app)


def test_user_without_nickname() -> None:
    """不提供昵称时，请求成功，响应中的昵称为空。"""
    response = client.post(
        "/users",
        json={
            "username": "Alice",
            "email": "alice@example.com",
            "age": 20,
            "password": "demo12345",
        },
    )

# assert 设置检查条件
    assert response.status_code == 200

    body = response.json()
    assert body["username"] == "Alice"
    assert body["nickname"] is None
    assert "password" not in body


def test_user_with_empty_nickname() -> None:
    """提供空字符串昵称时，请求因昵称校验失败而被拒绝。"""
    response = client.post(
        "/users",
        json={
            "username": "Alice",
            "email": "alice@example.com",
            "age": 20,
            "password": "demo12345",
            "nickname": "",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "nickname"]