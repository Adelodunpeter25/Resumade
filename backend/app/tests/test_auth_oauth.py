"""Google OAuth tests"""

from unittest.mock import patch
from app.models import User


def test_google_auth_initiation(client):
    """Test initiating Google OAuth"""
    response = client.get("/api/auth/google")

    assert response.status_code == 200
    data = response.json()
    assert "auth_url" in data
    assert "accounts.google.com" in data["auth_url"]


@patch("app.services.oauth_service.GoogleOAuthService.exchange_code_for_token")
@patch("app.services.oauth_service.GoogleOAuthService.get_user_info")
def test_google_callback_new_user(
    mock_get_user_info, mock_exchange_token, client, db_session
):
    """Test OAuth callback creates new user"""
    mock_exchange_token.return_value = {"access_token": "mock_token"}
    mock_get_user_info.return_value = {
        "id": "google123",
        "email": "newuser@gmail.com",
        "name": "New User",
    }

    init_response = client.get("/api/auth/google")
    auth_url = init_response.json()["auth_url"]
    state = auth_url.split("state=")[1].split("&")[0]

    response = client.get(
        f"/api/auth/google/callback?code=mock_code&state={state}",
        follow_redirects=False,
    )

    # Should redirect with token
    assert response.status_code == 307  # Redirect
    assert "token=" in response.headers.get("location", "")

    # Verify user was created
    user = db_session.query(User).filter(User.email == "newuser@gmail.com").first()
    assert user is not None
    assert user.oauth_provider == "google"


@patch("app.services.oauth_service.GoogleOAuthService.exchange_code_for_token")
@patch("app.services.oauth_service.GoogleOAuthService.get_user_info")
def test_google_callback_existing_user(
    mock_get_user_info, mock_exchange_token, client, db_session, valid_user
):
    """Test OAuth links to existing user"""
    client.post("/api/auth/signup", json=valid_user)

    mock_exchange_token.return_value = {"access_token": "mock_token"}
    mock_get_user_info.return_value = {
        "id": "google456",
        "email": valid_user["email"],
        "name": valid_user["full_name"],
    }

    init_response = client.get("/api/auth/google")
    auth_url = init_response.json()["auth_url"]
    state = auth_url.split("state=")[1].split("&")[0]

    response = client.get(
        f"/api/auth/google/callback?code=mock_code&state={state}",
        follow_redirects=False,
    )

    # Should redirect
    assert response.status_code == 307

    # Verify OAuth was linked
    user = (
        db_session.query(User).filter(User.email == valid_user["email"].lower()).first()
    )
    assert user.oauth_provider == "google"


def test_google_callback_invalid_state(client):
    """Test OAuth with invalid state fails"""
    response = client.get("/api/auth/google/callback?code=mock&state=invalid")

    assert response.status_code == 400
