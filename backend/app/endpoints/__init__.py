from .users import router as users_router
from .customers import router as customers_router
from .invoices import router as invoices_router
from .auth import router as auth_router
from .analytics import router as analytics_router

__all__ = ["users_router", "customers_router", "invoices_router", "auth_router", "analytics_router"]
