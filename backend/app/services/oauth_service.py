"""OAuth authentication service"""
import httpx
from typing import Optional, Dict
from app.core.config import settings

class GoogleOAuthService:
    """Google OAuth 2.0 authentication"""
    
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    @staticmethod
    def get_authorization_url(state: str) -> str:
        """Generate Google OAuth authorization URL"""
        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{GoogleOAuthService.GOOGLE_AUTH_URL}?{query_string}"
    
    @staticmethod
    async def exchange_code_for_token(code: str) -> Optional[Dict]:
        """Exchange authorization code for access token"""
        data = {
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_redirect_uri,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(GoogleOAuthService.GOOGLE_TOKEN_URL, data=data)
            
            if response.status_code == 200:
                return response.json()
            return None
    
    @staticmethod
    async def get_user_info(access_token: str) -> Optional[Dict]:
        """Get user information from Google"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(GoogleOAuthService.GOOGLE_USERINFO_URL, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            return None
