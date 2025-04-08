import pandas as pd
from crypticorn.klines import (
    ApiClient,
    Configuration,
    FundingRatesApi,
    HealthCheckApi,
    OHLCVDataApi,
    SymbolsApi,
    UDFApi,
)
from crypticorn.common import BaseURL, ApiVersion, Service, apikey_header as aph


class FundingRatesApiWrapper(FundingRatesApi):
    """
    A wrapper for the FundingRatesApi class.
    """

    def get_funding_rates_fmt(self):
        response = self.funding_rate_funding_rates_symbol_get()
        return pd.DataFrame(response.json())


class OHLCVDataApiWrapper(OHLCVDataApi):
    """
    A wrapper for the OHLCVDataApi class.
    """

    def get_ohlcv_data_fmt(self):
        response = self.get_ohlcv_market_timeframe_symbol_get()
        return pd.DataFrame(response.json())


class SymbolsApiWrapper(SymbolsApi):
    """
    A wrapper for the SymbolsApi class.
    """

    def get_symbols_fmt(self):
        response = self.symbols_symbols_market_get()
        return pd.DataFrame(response.json())


class UDFApiWrapper(UDFApi):
    """
    A wrapper for the UDFApi class.
    """

    def get_udf_fmt(self):
        response = self.get_history_udf_history_get()
        return pd.DataFrame(response.json())


class KlinesClient:
    """
    A client for interacting with the Crypticorn Klines API.
    """

    def __init__(
        self,
        base_url: BaseURL,
        api_version: ApiVersion,
        api_key: str = None,
        jwt: str = None,
    ):
        self.host = f"{base_url.value}/{api_version.value}/{Service.KLINES.value}"
        self.config = Configuration(
            host=self.host,
            access_token=jwt,
            api_key={aph.scheme_name: api_key} if api_key else None,
            api_key_prefix=({aph.scheme_name: aph.model.name} if api_key else None),
        )
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.funding = FundingRatesApiWrapper(self.base_client)
        self.ohlcv = OHLCVDataApiWrapper(self.base_client)
        self.symbols = SymbolsApiWrapper(self.base_client)
        self.udf = UDFApiWrapper(self.base_client)
        self.health = HealthCheckApi(self.base_client)
