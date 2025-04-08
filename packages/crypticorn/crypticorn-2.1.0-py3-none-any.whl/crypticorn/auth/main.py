from crypticorn.auth import (
    ApiClient,
    Configuration,
    AdminApi,
    ServiceApi,
    UserApi,
    WalletApi,
    AuthApi,
)
from crypticorn.common import BaseURL, ApiVersion, Service, apikey_header as aph


class AuthClient:
    """
    A client for interacting with the Crypticorn Auth API.
    """

    def __init__(
        self,
        base_url: BaseURL,
        api_version: ApiVersion,
        api_key: str = None,
        jwt: str = None,
    ):
        self.host = f"{base_url.value}/{api_version.value}/{Service.AUTH.value}"
        self.config = Configuration(
            host=self.host,
            access_token=jwt,
            api_key={aph.scheme_name: api_key} if api_key else None,
            api_key_prefix=({aph.scheme_name: aph.model.name} if api_key else None),
            debug=True,
        )
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.admin = AdminApi(self.base_client)
        self.service = ServiceApi(self.base_client)
        self.user = UserApi(self.base_client)
        self.wallet = WalletApi(self.base_client)
        self.login = AuthApi(self.base_client)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.base_client.close()
