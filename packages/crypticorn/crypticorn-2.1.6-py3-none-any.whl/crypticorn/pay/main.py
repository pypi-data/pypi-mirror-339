from crypticorn.pay import (
    ApiClient,
    Configuration,
    NOWPaymentsApi,
    StatusApi,
    PaymentsApi,
    ProductsApi,
)
from crypticorn.common import BaseURL, ApiVersion, Service, apikey_header as aph


class PayClient:
    """
    A client for interacting with the Crypticorn Pay API.
    """

    def __init__(
        self,
        base_url: BaseURL,
        api_version: ApiVersion,
        api_key: str = None,
        jwt: str = None,
    ):
        self.host = f"{base_url.value}/{api_version.value}/{Service.PAY.value}"
        self.config = Configuration(
            host=self.host,
            access_token=jwt,
            api_key={aph.scheme_name: api_key} if api_key else None,
            api_key_prefix=({aph.scheme_name: aph.model.name} if api_key else None),
        )
        self.base_client = ApiClient(configuration=self.config)
        self.now = NOWPaymentsApi(self.base_client)
        self.status = StatusApi(self.base_client)
        self.payments = PaymentsApi(self.base_client)
        self.products = ProductsApi(self.base_client)
