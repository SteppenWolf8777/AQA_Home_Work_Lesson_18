import requests

BASE_URL = "https://reqres.in/api"

# 1. Тесты на каждый из методов GET/POST/PUT/DELETE
def test_get_users_returns_list():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json().get("data"), list)

def test_post_create_user_returns_created_data():
    payload = {"name": "Test User", "job": "QA"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"

def test_put_update_user_returns_updated_data():
    payload = {"name": "Updated Name", "job": "Senior QA"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_user_returns_no_content():
    response = requests.delete(f"{BASE_URL}/users/2")
    assert response.status_code == 204
    assert response.text == ""

# 2. Позитивные и негативные тесты
def test_login_with_valid_credentials_returns_token():
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_with_missing_password_returns_bad_request():
    payload = {"email": "eve.holt@reqres.in"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()

# 3. Тесты на разные статус-коды 200/201/204/404/400
def test_status_200_get_single_user():
    resp = requests.get(f"{BASE_URL}/users/2")
    assert resp.status_code == 200

def test_status_201_create_user():
    payload = {"name": "New User", "job": "Tester"}
    resp = requests.post(f"{BASE_URL}/users", json=payload)
    assert resp.status_code == 201

def test_status_204_delete_user():
    resp = requests.delete(f"{BASE_URL}/users/2")
    assert resp.status_code == 204

def test_status_404_get_non_existing_user():
    resp = requests.get(f"{BASE_URL}/users/123")
    assert resp.status_code == 404

def test_status_400_login_without_password():
    payload = {"email": "eve.holt@reqres.in"}
    resp = requests.post(f"{BASE_URL}/login", json=payload)
    assert resp.status_code == 400

# 4. Тесты на разные схемы
def test_schema_users_list_contains_data_array_with_id_name_email():
    resp = requests.get(f"{BASE_URL}/users")
    data = resp.json().get("data", [])
    assert isinstance(data, list)
    if data:
        first = data
        assert "id" in first
        assert "name" in first
        assert "email" in first

def test_schema_single_user_contains_id_name_email():
    resp = requests.get(f"{BASE_URL}/users/2")
    data = resp.json().get("data", {})
    assert "id" in data
    assert "name" in data
    assert "email" in data

def test_schema_created_user_contains_name_job_and_created_at():
    payload = {"name": "Schema Test", "job": "Dev"}
    resp = requests.post(f"{BASE_URL}/users", json=payload)
    data = resp.json()
    assert "name" in data
    assert "job" in data
    assert "createdAt" in data

def test_schema_updated_user_contains_name_job_and_updated_at():
    payload = {"name": "Updated Schema", "job": "Lead"}
    resp = requests.put(f"{BASE_URL}/users/2", json=payload)
    data = resp.json()
    assert "name" in data
    assert "job" in data
    assert "updatedAt" in data

def test_schema_login_response_contains_token():
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    resp = requests.post(f"{BASE_URL}/login", json=payload)
    data = resp.json()
    assert "token" in data

# 5. Тесты с ответом и без ответа
def test_get_users_returns_non_empty_response_body():
    resp = requests.get(f"{BASE_URL}/users")
    assert resp.status_code == 200
    assert len(resp.content) > 0
    assert resp.text != ""

def test_delete_user_returns_empty_response_body():
    resp = requests.delete(f"{BASE_URL}/users/2")
    assert resp.status_code == 204
    assert resp.text == ""
    assert len(resp.content) == 0