from crypticorn.trade import (
    ApiClient,
    APIKeysApi,
    BotsApi,
    Configuration,
    ExchangesApi,
    FuturesTradingPanelApi,
    NotificationsApi,
    OrdersApi,
    StatusApi,
    StrategiesApi,
    TradingActionsApi,
)
from crypticorn.common import BaseURL, ApiVersion, Service, apikey_header as aph


class TradeClient:
    """
    A client for interacting with the Crypticorn Trade API.
    """

    def __init__(
        self,
        base_url: BaseURL,
        api_version: ApiVersion,
        api_key: str = None,
        jwt: str = None,
    ):
        self.host = f"{base_url.value}/{api_version.value}/{Service.TRADE.value}"
        self.config = Configuration(
            host=self.host,
            access_token=jwt,
            api_key={aph.scheme_name: api_key} if api_key else None,
            api_key_prefix=({aph.scheme_name: aph.model.name} if api_key else None),
        )
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.bots = BotsApi(self.base_client)
        self.exchanges = ExchangesApi(self.base_client)
        self.notifications = NotificationsApi(self.base_client)
        self.orders = OrdersApi(self.base_client)
        self.status = StatusApi(self.base_client)
        self.strategies = StrategiesApi(self.base_client)
        self.actions = TradingActionsApi(self.base_client)
        self.futures = FuturesTradingPanelApi(self.base_client)
        self.api_keys = APIKeysApi(self.base_client)
