import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Welcome to Reddit API'


def test_create_user(client):
    res = client.post("/users/", json={"username":"Tejaswi", "password":"12345", "client_id": "hi", "client_secret": "dummy", "user_agent": "ddd"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.username == "Tejaswi"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['username'],"password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200