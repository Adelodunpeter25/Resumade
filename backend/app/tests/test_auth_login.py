"""Login endpoint tests"""
import pytest
from app.models import User

def test_login_success(client, valid_user):
    """Test successful login"""
    client.post("/api/auth/signup", json=valid_user)
    
    response = client.post("/api/auth/login", json={
        "email": valid_user["email"],
        "password": valid_user["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]

def test_login_wrong_password(client, valid_user):
    """Test login with wrong password"""
    client.post("/api/auth/signup", json=valid_user)
    
    response = client.post("/api/auth/login", json={
        "email": valid_user["email"],
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """Test login with non-existent email"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 401

def test_login_case_insensitive(client, valid_user):
    """Test email is case-insensitive"""
    client.post("/api/auth/signup", json=valid_user)
    
    response = client.post("/api/auth/login", json={
        "email": valid_user["email"].upper(),
        "password": valid_user["password"]
    })
    
    assert response.status_code == 200

def test_login_oauth_user_fails(client, db_session):
    """Test OAuth user cannot login with password"""
    oauth_user = User(
        email="oauth@example.com",
        full_name="OAuth User",
        oauth_provider="google",
        oauth_id="google123",
        hashed_password=None
    )
    db_session.add(oauth_user)
    db_session.commit()
    
    response = client.post("/api/auth/login", json={
        "email": "oauth@example.com",
        "password": "anypassword"
    })
    
    assert response.status_code == 401
