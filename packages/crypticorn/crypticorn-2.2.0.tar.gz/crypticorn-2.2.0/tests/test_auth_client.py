import asyncio
import os

import dotenv
import pytest
import pytest_asyncio
from crypticorn.common import AuthHandler, BaseUrl, Scope
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

dotenv.load_dotenv()
print(dotenv.dotenv_values())

# JWT
EXPIRED_JWT = os.getenv("EXPIRED_JWT")
VALID_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYlowNUVqS2ZqWGpXdDBTMDdvOSIsImF1ZCI6ImFwcC5jcnlwdGljb3JuLmNvbSIsImlzcyI6ImFjY291bnRzLmNyeXB0aWNvcm4uY29tIiwianRpIjoibHlmQktacTM1OXBWYlZldkQ1MWgiLCJpYXQiOjE3NDQyMjc2NDMsImV4cCI6MTc0NDIzMTI0Mywic2NvcGVzIjpbInJlYWQ6aGl2ZTptb2RlbCIsInJlYWQ6aGl2ZTpkYXRhIiwicmVhZDp0cmFkZTpib3RzIiwicmVhZDp0cmFkZTpvcmRlcnMiLCJyZWFkOnRyYWRlOmFjdGlvbnMiLCJyZWFkOnRyYWRlOnN0cmF0ZWdpZXMiLCJyZWFkOnRyYWRlOmV4Y2hhbmdlcyIsInJlYWQ6dHJhZGU6ZnV0dXJlcyIsInJlYWQ6dHJhZGU6bm90aWZpY2F0aW9ucyIsInJlYWQ6dHJhZGU6YXBpX2tleXMiLCJyZWFkOnBheTpub3ciLCJyZWFkOnBheTpwcm9kdWN0cyIsInJlYWQ6cGF5OnBheW1lbnRzIiwid3JpdGU6aGl2ZTptb2RlbCIsIndyaXRlOnRyYWRlOmJvdHMiLCJ3cml0ZTp0cmFkZTpmdXR1cmVzIiwid3JpdGU6dHJhZGU6bm90aWZpY2F0aW9ucyIsIndyaXRlOnRyYWRlOmFwaV9rZXlzIiwid3JpdGU6dHJhZGU6c3RyYXRlZ2llcyIsInJlYWQ6cHJlZGljdGlvbnMiLCJ3cml0ZTpwYXk6cHJvZHVjdHMiLCJ3cml0ZTpwYXk6bm93IiwicmVhZDpwcmVkaWN0aW9ucyJdfQ.q_zjXytY7lDmwIDB0B7LIpQ-b83JOEboECLTTBAnT9M"
# API KEY
FULL_SCOPE_API_KEY = os.getenv("FULL_SCOPE_API_KEY")
ONE_SCOPE_API_KEY = os.getenv("ONE_SCOPE_API_KEY")
EXPIRED_API_KEY = os.getenv("EXPIRED_API_KEY")

# ASSERT SCOPE
ALL_SCOPES = list(Scope)
JWT_SCOPE = Scope.READ_PREDICTIONS
API_KEY_SCOPE = Scope.READ_TRADE_BOTS

# ERROR MESSAGES
API_KEY_EXPIRED = "API key expired"
API_KEY_INVALID = "Invalid API key"
BEARER_EXPIRED = "jwt expired"

# Debug
UPDATE_SCOPES = "you probably need to bring the scopes in both the api client and the auth service in sync"

# Each function is tested without credentials, with invalid credentials, and with valid credentials.
# The test is successful if the correct HTTPException is raised.


@pytest_asyncio.fixture
async def auth_handler() -> AuthHandler:
    return AuthHandler(BaseUrl.LOCAL)


# COMBINED AUTH


@pytest.mark.asyncio
async def test_combined_auth_without_credentials(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == auth_handler.no_credentials_exception.detail


# BEARER
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_bearer_token(auth_handler: AuthHandler):
    """With invalid bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123"),
            api_key=None,
        )
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_combined_auth_with_expired_bearer_token(auth_handler: AuthHandler):
    """With expired bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=EXPIRED_JWT
            ),
            api_key=None,
        )
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


@pytest.mark.asyncio
async def test_combined_auth_with_valid_bearer_token(auth_handler: AuthHandler):
    """With valid bearer token"""
    res = await auth_handler.combined_auth(
        bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT),
        api_key=None,
    )
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


# API KEY
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_combined_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    """With full scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_combined_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_combined_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.combined_auth(bearer=None, api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# API KEY AUTH
@pytest.mark.asyncio
async def test_api_key_auth_without_api_key(auth_handler: AuthHandler):
    """Without api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_api_key_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_api_key_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    """With full scope valid api key"""
    res = await auth_handler.api_key_auth(api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_api_key_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.api_key_auth(api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_api_key_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.api_key_auth(api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# BEARER AUTH
@pytest.mark.asyncio
async def test_bearer_auth_without_bearer(auth_handler: AuthHandler):
    """Without bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(bearer=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_bearer_auth_with_invalid_bearer(auth_handler: AuthHandler):
    """With invalid bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123")
        )
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_bearer_auth_with_valid_bearer(auth_handler: AuthHandler):
    """With valid bearer"""
    res = await auth_handler.bearer_auth(
        bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT)
    )
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_bearer_auth_with_expired_bearer(auth_handler: AuthHandler):
    """With expired bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(
            bearer=HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=EXPIRED_JWT
            )
        )
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


# WS COMBINED AUTH
@pytest.mark.asyncio
async def test_ws_combined_auth_without_credentials(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == auth_handler.no_credentials_exception.detail


# BEARER
@pytest.mark.asyncio
async def test_ws_combined_auth_with_invalid_bearer(auth_handler: AuthHandler):
    """With invalid bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_combined_auth(bearer="123", api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_combined_auth_with_valid_bearer(auth_handler: AuthHandler):
    res = await auth_handler.ws_combined_auth(bearer=VALID_JWT, api_key=None)
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_expired_bearer(auth_handler: AuthHandler):
    """With expired bearer"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=EXPIRED_JWT, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


# API KEY
@pytest.mark.asyncio
async def test_ws_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_combined_auth_with_full_scope_valid_api_key(
    auth_handler: AuthHandler,
):
    """With full scope valid api key"""
    res = await auth_handler.ws_combined_auth(bearer=None, api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.ws_combined_auth(bearer=None, api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=None, api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# WS BEARER AUTH
@pytest.mark.asyncio
async def test_ws_bearer_auth_without_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_bearer_auth(bearer=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_bearer_auth_with_invalid_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_bearer_auth(bearer="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_bearer_auth_with_valid_bearer(auth_handler: AuthHandler):
    res = await auth_handler.ws_bearer_auth(bearer=VALID_JWT)
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


# WS API KEY AUTH
@pytest.mark.asyncio
async def test_ws_api_key_auth_without_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_invalid_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_expired_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    res = await auth_handler.ws_api_key_auth(api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    res = await auth_handler.ws_api_key_auth(api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


# print(asyncio.run(test_ws_api_key_auth_with_one_scope_valid_api_key(AuthHandler(BaseUrl.LOCAL))))
