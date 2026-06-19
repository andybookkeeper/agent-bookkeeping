import os
from typing import Literal

from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader


Role = Literal["read", "write", "admin"]

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    scheme_name="ApiKeyAuth",
    description="API key required for all /api endpoints",
)


def _is_development() -> bool:
    env = os.getenv("ENV", "development").lower()
    return env in {"development", "dev", "local"}


def _required_key(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value

    if _is_development():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing API key configuration: {name}",
        )

    raise RuntimeError(f"Missing required API key environment variable: {name}")


def validate_auth_settings() -> None:
    if _is_development():
        return

    for key_name in ("API_KEY_READONLY", "API_KEY_READWRITE", "API_KEY_ADMIN"):
        if not os.getenv(key_name):
            raise RuntimeError(f"Missing required API key environment variable: {key_name}")


def _role_from_api_key(api_key: str | None) -> Role:
    read_key = _required_key("API_KEY_READONLY")
    write_key = _required_key("API_KEY_READWRITE")
    admin_key = _required_key("API_KEY_ADMIN")

    if api_key == admin_key:
        return "admin"
    if api_key == write_key:
        return "write"
    if api_key == read_key:
        return "read"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
    )


def get_current_role(api_key: str | None = Security(api_key_header)) -> Role:
    return _role_from_api_key(api_key)


def authorize_api_request(
    request: Request,
    role: Role = Security(get_current_role),
) -> None:
    method = request.method.upper()
    if method in {"GET", "HEAD", "OPTIONS"}:
        return

    if role in {"write", "admin"}:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Write permission required",
    )
