from .users import router as users_router
from .resumes import router as resumes_router
from .auth import router as auth_router
from .admin import router as admin_router

__all__ = ["users_router", "resumes_router", "auth_router", "admin_router"]
