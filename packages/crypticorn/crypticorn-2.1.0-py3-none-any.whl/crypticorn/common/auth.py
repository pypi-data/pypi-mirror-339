from typing import Optional, Callable, Any, Annotated
from typing_extensions import Doc
from enum import Enum

from fastapi import params
from fastapi.security import APIKeyHeader, HTTPBearer

from crypticorn.common import Scope


http_bearer = HTTPBearer(
    bearerFormat="JWT",
    auto_error=False,
    description="The JWT to use for authentication.",
)

apikey_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    description="The API key to use for authentication.",
)


def Security(  # noqa: N802
    dependency: Annotated[
        Optional[Callable[..., Any]], Doc("A dependable callable (like a function).")
    ] = None,
    scopes: Annotated[
        Optional[list[Scope]],
        Doc("API scopes required for the *path operation*."),
    ] = None,
    use_cache: Annotated[
        bool, Doc("Whether to cache the dependency during a single request.")
    ] = True,
) -> Any:
    """Security Dependency. Extends the fastapi.Security class to support enum scopes instead of strings."""

    # Convert Enum scopes to string
    scopes_str = [s.value for s in scopes] if scopes else None

    return params.Security(
        dependency=dependency, scopes=scopes_str, use_cache=use_cache
    )
