from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, SecurityScopes
from typing_extensions import Annotated, Doc
import json

from crypticorn.auth import AuthClient, Verify200Response
from crypticorn.auth.client.exceptions import ApiException
from crypticorn.common import (
    ApiError,
    Scope,
    ApiVersion,
    BaseURL,
    Domain,
    apikey_header,
    http_bearer,
)


class AuthHandler:
    """
    Middleware for verifying API requests. Verifies the validity of the authentication token, allowed scopes, etc.
    """

    def __init__(
        self,
        base_url: Annotated[
            BaseURL, Doc("The base URL for the auth service.")
        ] = BaseURL.PROD,
        api_version: Annotated[
            ApiVersion, Doc("The API version of the auth service.")
        ] = ApiVersion.V1,
        whitelist: Annotated[
            list[Domain],
            Doc(
                "The domains of which requests are allowed full access to the service."
            ),
        ] = [
            Domain.PROD,
            Domain.DEV,
        ],  # TODO: decide whether this is needed, else omit
    ):
        self.whitelist = whitelist
        self.auth_client = AuthClient(base_url=base_url, api_version=api_version)

        self.no_credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError.NO_CREDENTIALS.identifier,
        )

    async def _verify_api_key(self, api_key: str) -> None:
        """
        Verifies the API key.
        """
        return await self.auth_client.login.verify_api_key(api_key)

    async def _verify_bearer(
        self, bearer: HTTPAuthorizationCredentials
    ) -> Verify200Response:
        """
        Verifies the bearer token.
        """
        self.auth_client.config.access_token = bearer.credentials
        return await self.auth_client.login.verify()

    async def _validate_scopes(
        self, api_scopes: list[Scope], user_scopes: list[Scope]
    ) -> bool:
        """
        Checks if the user scopes are a subset of the API scopes.
        """
        if not set(api_scopes).issubset(user_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ApiError.INSUFFICIENT_SCOPES.identifier,
            )

    async def _extract_message(self, e: ApiException) -> str:
        """
        Tries to extract the message from the body of the exception.
        """
        try:
            load = json.loads(e.body)
        except (json.JSONDecodeError, TypeError):
            return e.body
        else:
            common_keys = ["message"]
            for key in common_keys:
                if key in load:
                    return load[key]
            return load

    async def _handle_exception(self, e: Exception) -> HTTPException:
        """
        Handles exceptions and returns a HTTPException with the appropriate status code and detail.
        """
        if isinstance(e, ApiException):
            return HTTPException(
                status_code=e.status,
                detail=await self._extract_message(e),
            )
        elif isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def api_key_auth(
        self,
        api_key: Annotated[str | None, Depends(apikey_header)] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the API key.
        """
        return await self.combined_auth(bearer=None, api_key=api_key, sec=sec)

    async def bearer_auth(
        self,
        bearer: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(http_bearer),
        ] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the bearer token.
        """
        return await self.combined_auth(bearer=bearer, api_key=None, sec=sec)

    async def combined_auth(
        self,
        bearer: Annotated[
            HTTPAuthorizationCredentials | None, Depends(http_bearer)
        ] = None,
        api_key: Annotated[str | None, Depends(apikey_header)] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and/or API key and checks if the user scopes are a subset of the API scopes.
        Returns early on the first successful verification, otherwise tries all available tokens.
        Use this function if you want to allow access via either the bearer token or the API key.
        """
        tokens = [bearer, api_key]

        last_error = None
        for token in tokens:
            try:
                if token is None:
                    continue
                res = None
                if isinstance(token, str):
                    res = await self._verify_api_key(token)
                elif isinstance(token, HTTPAuthorizationCredentials):
                    res = await self._verify_bearer(token)
                if res is None:
                    continue
                if sec:
                    await self._validate_scopes(sec.scopes, res.scopes)
                return res

            except Exception as e:
                last_error = await self._handle_exception(e)
                continue

        raise last_error or self.no_credentials_exception

    async def ws_api_key_auth(
        self,
        api_key: Annotated[str | None, Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the API key.
        """
        return await self.api_key_auth(api_key=api_key, sec=sec)

    async def ws_bearer_auth(
        self,
        bearer: Annotated[str | None, Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the bearer token.
        """
        credentials = (
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=bearer)
            if bearer
            else None
        )
        return await self.bearer_auth(bearer=credentials, sec=sec)

    async def ws_combined_auth(
        self,
        bearer: Annotated[str | None, Query()] = None,
        api_key: Annotated[str | None, Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and/or API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you want to allow access via either the bearer token or the API key.
        """
        credentials = (
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=bearer)
            if bearer
            else None
        )
        return await self.combined_auth(bearer=credentials, api_key=api_key, sec=sec)
