from crypticorn.metrics import (
    ApiClient,
    Configuration,
    ExchangesApi,
    HealthCheckApi,
    IndicatorsApi,
    LogsApi,
    MarketcapApi,
    MarketsApi,
    TokensApi,
    Market,
)
from crypticorn.common import BaseURL, ApiVersion, Service, apikey_header as aph
from typing import Optional, Dict, Any, Union, Tuple
from pydantic import StrictStr, StrictInt, StrictFloat, Field
from typing_extensions import Annotated

import pandas as pd


class MetricsClient:
    """
    A client for interacting with the Crypticorn Metrics API.
    """

    def __init__(
        self,
        base_url: BaseURL,
        api_version: ApiVersion,
        api_key: str = None,
        jwt: str = None,
    ):
        self.host = f"{base_url.value}/{api_version.value}/{Service.METRICS.value}"
        self.config = Configuration(
            host=self.host,
            access_token=jwt,
            api_key={aph.scheme_name: api_key} if api_key else None,
            api_key_prefix=({aph.scheme_name: aph.model.name} if api_key else None),
        )
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.status = HealthCheckApi(self.base_client)
        self.indicators = IndicatorsApi(self.base_client)
        self.logs = LogsApi(self.base_client)
        self.marketcap = MarketcapApiWrapper(self.base_client)
        self.markets = MarketsApi(self.base_client)
        self.tokens = TokensApiWrapper(self.base_client)
        self.exchanges = ExchangesApi(self.base_client)



class MarketcapApiWrapper(MarketcapApi):
    """
    A wrapper for the MarketcapApi class.
    """

    async def get_marketcap_symbols_fmt(
        self,
        start_timestamp: Annotated[
            Optional[StrictInt], Field(description="Start timestamp")
        ] = None,
        end_timestamp: Annotated[
            Optional[StrictInt], Field(description="End timestamp")
        ] = None,
        interval: Annotated[
            Optional[StrictStr],
            Field(description="Interval for which to fetch symbols and marketcap data"),
        ] = None,
        market: Annotated[
            Optional[Market],
            Field(description="Market for which to fetch symbols and marketcap data"),
        ] = None,
        exchange: Annotated[
            Optional[StrictStr],
            Field(description="Exchange for which to fetch symbols and marketcap data"),
        ] = None,
    ) -> pd.DataFrame:
        """
        Get the marketcap symbols in a pandas dataframe
        """
        response = await self.get_marketcap_symbols_without_preload_content(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            interval=interval,
            market=market,
            exchange=exchange,
        )
        json_response = await response.json()
        df = pd.DataFrame(json_response["data"])
        df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp']).astype("int64") // 10 ** 9
        return df


class TokensApiWrapper(TokensApi):
    """
    A wrapper for the TokensApi class.
    """

    async def get_tokens_fmt(
        self,
        token_type: Annotated[
            StrictStr,
            Field(description="Type of tokens to fetch"),
        ],
    ) -> pd.DataFrame:
        """
        Get the tokens in a pandas dataframe
        """
        response = await self.get_stable_and_wrapped_tokens_without_preload_content(token_type=token_type)
        json_data = await response.json()
        return pd.DataFrame(json_data['data'])
