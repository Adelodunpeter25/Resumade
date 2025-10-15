from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limit configurations
RATE_LIMITS = {
    "signup": "5/minute",
    "login": "10/minute",
    "forgot_password": "3/minute",
    "pdf_upload": "5/minute",
    "pdf_generate": "10/minute",
    "export": "20/minute",
    "ats_score": "30/minute",
    "create_resume": "20/minute",
    "default": "100/minute"
}

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RATE_LIMITS["default"]],
    storage_uri="memory://"
)
