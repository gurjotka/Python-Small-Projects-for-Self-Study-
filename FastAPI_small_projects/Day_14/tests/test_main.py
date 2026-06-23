from fastapi.testclient import TestClient
from app.main import app

from fastapi import FastAPI

app = FastAPI()
client = TestClient(app)


# BASIC ROUTE TESTS

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200

def test_safe_route():
    response = client.get("/safe")
    assert response.status_code == 200

def test_response_json():
    response = client.get("/hello")
    assert "message" in response.json()

def test_oot_not_found():
    response = client.get("/")
    assert response.status_code == 404

def test_wrong_route():
    response = client.get("/doesnotexist")
    assert response.status_code == 404


# ERROR HANDLING TESTS

def test_user_error():
    response = client.get("/user-error")
    assert response.status_code == 400

def test_server_error():
    response = client.get("/server-error")
    assert response.status_code == 400

def test_error_response_format():
    response = client.get("/server-error")
    data = response.json()
    assert "error" in data

def test_safe_does_not_error():
    response = client.get("/safe")
    assert response.status_code == 200

def test_all_routes_return_json():
    response = client.get("/safe")
    assert isinstance(response.json(), dict)


# AUTH TESTS

def test_register():
    response = client.post("/register", json={
        "username": "john",
        "password": "1234"
    })
    assert response.status_code in [200, 201]

def test_login():
    response = client.post("/login", json={
        "username": "john",
        "password": "1234"
    })
    assert response.status_code == 200

def test_login_token_exists():
    response = client.post("/login", json={
        "username": "john",
        "password": "1234"
    })

    token = login.json()["access_token"]
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


# EDGE CASE TESTS

def test_empty_login():
    response = client.post("/login", json={})
    assert response.status_code >= 400

def test_invalid_password():
    response = client.post("/login", json={
        "username": "john",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_missing_fields():
    response = client.post("/register", json={
        "username": "john"
    })
    assert response.status_code == 422

def test_token_tampering():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer fake.token.here"}
    )
    assert response.status_code == 401

def test_response_time_fast():
    response = client.get("/safe")
    assert response.elapsed.total_seconds() < 1
