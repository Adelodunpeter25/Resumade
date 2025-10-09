"""JWT token tests"""
import pytest
from jose import jwt
from app.core.config import settings

def test_get_current_user_success(client, valid_user):
    """Test getting user info with valid token"""
    signup_response = client.post("/api/auth/signup", json=valid_user)
    token = signup_response.json()["data"]["access_token"]
    
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == valid_user["email"].lower()

def test_get_current_user_no_token(client):
    """Test getting user without token fails"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 403

def test_get_current_user_invalid_token(client):
    """Test invalid token fails"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401

def test_token_contains_email(client, valid_user):
    """Test JWT contains user email"""
    response = client.post("/api/auth/signup", json=valid_user)
    token = response.json()["data"]["access_token"]
    
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    
    assert payload["sub"] == valid_user["email"].lower()
    assert "exp" in payload

def test_token_works_across_endpoints(client, valid_user):
    """Test token works on multiple endpoints"""
    signup_response = client.post("/api/auth/signup", json=valid_user)
    token = signup_response.json()["data"]["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    
    resumes_response = client.get("/api/resumes/", headers=headers)
    assert resumes_response.status_code == 200
