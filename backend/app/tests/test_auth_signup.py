"""Signup endpoint tests"""

from app.models import User


def test_signup_success(client, valid_user):
    """Test successful user signup"""
    response = client.post("/api/auth/signup", json=valid_user)

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


def test_signup_duplicate_email(client, valid_user):
    """Test signup with existing email"""
    client.post("/api/auth/signup", json=valid_user)
    response = client.post("/api/auth/signup", json=valid_user)

    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"]["message"].lower()


def test_signup_invalid_email(client):
    """Test signup with invalid email"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "password123",
        },
    )

    # Pydantic validation returns 422
    assert response.status_code == 422


def test_signup_short_password(client):
    """Test signup with short password"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "short",
        },
    )

    # Pydantic validation returns 422
    assert response.status_code == 422


def test_signup_xss_protection(client, db_session):
    """Test XSS protection in name field"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "xss@example.com",
            "full_name": "<script>alert('xss')</script>John",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    user = db_session.query(User).filter(User.email == "xss@example.com").first()
    assert "<script>" not in user.full_name
