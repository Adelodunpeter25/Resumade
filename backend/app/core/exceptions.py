from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class ResumadeException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundError(ResumadeException):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404)


class ValidationError(ResumadeException):
    def __init__(self, message: str):
        super().__init__(message, 422)


class AuthenticationError(ResumadeException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


async def resumade_exception_handler(request: Request, exc: ResumadeException):
    logger.error(f"Resumade error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "status_code": exc.status_code},
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"Database integrity error: {str(exc)}")
    return JSONResponse(
        status_code=409,
        content={
            "error": "Data conflict - resource may already exist",
            "status_code": 409,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "status_code": 500}
    )
