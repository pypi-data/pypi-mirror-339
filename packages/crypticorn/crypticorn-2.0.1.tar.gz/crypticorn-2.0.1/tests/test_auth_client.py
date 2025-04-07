from crypticorn.common import BaseURL, AuthHandler, Scope, http_bearer
import asyncio
from fastapi import HTTPException
import pytest_asyncio
import pytest
from fastapi.security import HTTPAuthorizationCredentials

VALID_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYlowNUVqS2ZqWGpXdDBTMDdvOSIsImF1ZCI6ImFwcC5jcnlwdGljb3JuLmNvbSIsImlzcyI6ImFjY291bnRzLmNyeXB0aWNvcm4uY29tIiwianRpIjoiTXY3ZTBpMkt0TlliYmN0TVp2aGYiLCJpYXQiOjE3NDM5NzI4NjgsImV4cCI6MTc0Mzk3NjQ2OCwic2NvcGVzIjpbInJlYWQ6cHJlZGljdGlvbnMiXX0.NkQ6FlmViPFZDqT9SLV0u8bnm2pegLQ0TknxYgutoGk"
EXPIRED_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYlowNUVqS2ZqWGpXdDBTMDdvOSIsImF1ZCI6ImFwcC5jcnlwdGljb3JuLmNvbSIsImlzcyI6ImFjY291bnRzLmNyeXB0aWNvcm4uY29tIiwianRpIjoiM3FlU0h5S082VVNvMkZBU1VxMmkiLCJpYXQiOjE3NDM5Njc2MzAsImV4cCI6MTc0Mzk3MTIzMCwic2NvcGVzIjpbInJlYWQ6cHJlZGljdGlvbnMiXX0.d3yfsTGIZaygORyrRQvPPZTZLK0oM2rYz4ijUtpl3xk"


@pytest_asyncio.fixture
async def auth_handler() -> AuthHandler:
    return AuthHandler(BaseURL.DEV)

@pytest.mark.asyncio
async def test_combined_auth_without_credentials(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == auth_handler.no_credentials_exception.detail

@pytest.mark.asyncio
async def test_combined_auth_with_invalid_bearer_token(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123"),
            api_key=None
        )
    assert e.value.status_code == 401

@pytest.mark.asyncio
async def test_combined_auth_with_expired_bearer_token(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=EXPIRED_JWT),
            api_key=None
        )
    assert e.value.status_code == 401
    assert e.value.detail == "jwt expired"

@pytest.mark.asyncio
async def test_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 500 # Not implemented

@pytest.mark.asyncio
async def test_combined_auth_with_valid_bearer_token(auth_handler: AuthHandler):
    res = await auth_handler.combined_auth(bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT), api_key=None)
    assert res.scopes == [Scope.READ_PREDICTIONS]

@pytest.mark.asyncio
async def test_combined_auth_with_valid_api_key(auth_handler: AuthHandler):
    # res = await auth_handler.combined_auth(bearer=None, api_key="123")
    # assert res.scopes == [Scope.READ_PREDICTIONS]
    assert True # not implemented

@pytest.mark.asyncio
async def test_api_key_auth_without_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key=None)
    assert e.value.status_code == 401

@pytest.mark.asyncio
async def test_api_key_auth_with_invalid_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key="123")
    assert e.value.status_code == 500 # Not implemented

@pytest.mark.asyncio
async def test_api_key_auth_with_valid_api_key(auth_handler: AuthHandler):  
    # res = await auth_handler.api_key_auth(api_key="123")
    # assert res.scopes == [Scope.READ_PREDICTIONS]
    assert True # not implemented

@pytest.mark.asyncio
async def test_bearer_auth_without_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(bearer=None)
    assert e.value.status_code == 401

@pytest.mark.asyncio
async def test_bearer_auth_with_invalid_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123"))
    assert e.value.status_code == 401

@pytest.mark.asyncio
async def test_bearer_auth_with_valid_bearer(auth_handler: AuthHandler):
    res = await auth_handler.bearer_auth(bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT))
    assert res.scopes == [Scope.READ_PREDICTIONS]

@pytest.mark.asyncio
async def test_bearer_auth_with_expired_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=EXPIRED_JWT))
    assert e.value.status_code == 401
    assert e.value.detail == "jwt expired"
    
    
    