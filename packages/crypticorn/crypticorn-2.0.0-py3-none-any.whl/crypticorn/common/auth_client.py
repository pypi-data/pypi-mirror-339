from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing_extensions import Annotated, Doc

from crypticorn.auth import AuthClient, Verify200Response
from crypticorn.auth.client.exceptions import UnauthorizedException
from crypticorn.common import (
    ApiError,
    ApiScope,
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

        self.invalid_scopes_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ApiError.INSUFFICIENT_SCOPES.identifier,
        )
        self.no_credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError.NO_CREDENTIALS.identifier,
        )
        self.invalid_api_key_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError.INVALID_API_KEY.identifier,
        )
        self.invalid_bearer_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError.INVALID_BEARER.identifier,
        )

    async def _verify_api_key(self, api_key: str) -> None:
        """
        Verifies the API key.
        """
        # TODO: Implement in auth service
        return NotImplementedError()

    async def _verify_bearer(
        self, bearer: HTTPAuthorizationCredentials
    ) -> Verify200Response:
        """
        Verifies the bearer token.
        """
        self.auth_client.config.access_token = bearer.credentials
        return await self.auth_client.login.verify()

    async def _check_scopes(
        self, api_scopes: list[ApiScope], user_scopes: list[ApiScope]
    ) -> bool:
        """
        Checks if the user scopes are a subset of the API scopes.
        """
        return set(api_scopes).issubset(user_scopes)

    async def api_key_auth(
        self,
        api_key: Annotated[str | None, Depends(apikey_header)] = None,
        scopes: list[ApiScope] = [],
    ) -> Verify200Response:
        """
        Verifies the API key and checks if the user scopes are a subset of the API scopes.
        """
        if not api_key:
            raise self.no_credentials_exception
        try:
            res = await self._verify_api_key(api_key)
        except UnauthorizedException as e:
            raise self.invalid_api_key_exception
        valid_scopes = await self._check_scopes(scopes, res.scopes)
        if not valid_scopes:
            raise self.invalid_scopes_exception
        return res

    async def bearer_auth(
        self,
        bearer: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(http_bearer),
        ] = None,
        scopes: list[ApiScope] = [],
    ) -> Verify200Response:
        """
        Verifies the bearer token and checks if the user scopes are a subset of the API scopes.
        """
        if not bearer:
            raise self.no_credentials_exception

        try:
            res = await self._verify_bearer(bearer)
        except UnauthorizedException as e:
            raise self.invalid_bearer_exception
        valid_scopes = await self._check_scopes(scopes, res.scopes)
        if not valid_scopes:
            raise self.invalid_scopes_exception
        return res

    async def combined_auth(
        self,
        bearer: Annotated[
            HTTPAuthorizationCredentials | None, Depends(http_bearer)
        ] = None,
        api_key: Annotated[str | None, Depends(apikey_header)] = None,
        scopes: list[ApiScope] = [],
    ) -> Verify200Response:
        """
        Verifies the bearer token and API key and checks if the user scopes are a subset of the API scopes.
        Returns early on the first successful verification, otherwise tries all available tokens.
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
                if scopes:
                    valid_scopes = await self._check_scopes(scopes, res.scopes)
                    if not valid_scopes:
                        raise self.invalid_scopes_exception
                return res

            except UnauthorizedException as e:
                last_error = e
                continue

        raise last_error or self.no_credentials_exception
