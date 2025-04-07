from enum import Enum


class ApiScope(str, Enum):
    """
    The permission scopes for the API.
    """

    # Hive scopes
    HIVE_MODEL_READ = "hive:model:read"
    HIVE_DATA_READ = "hive:data:read"
    HIVE_MODEL_WRITE = "hive:model:write"
    HIVE_DATA_WRITE = "hive:data:write"

    # Trade scopes
    TRADE_BOTS_READ = "trade:bots:read"
    TRADE_BOTS_WRITE = "trade:bots:write"
    TRADE_API_KEYS_READ = "trade:api_keys:read"
    TRADE_API_KEYS_WRITE = "trade:api_keys:write"
    TRADE_ORDERS_READ = "trade:orders:read"
    TRADE_ACTIONS_READ = "trade:actions:read"
    TRADE_ACTIONS_WRITE = "trade:actions:write"
    TRADE_EXCHANGES_READ = "trade:exchanges:read"
    TRADE_FUTURES_READ = "trade:futures:read"
    TRADE_FUTURES_WRITE = "trade:futures:write"
    TRADE_NOTIFICATIONS_READ = "trade:notifications:read"
    TRADE_NOTIFICATIONS_WRITE = "trade:notifications:write"
    TRADE_STRATEGIES_READ = "trade:strategies:read"
    TRADE_STRATEGIES_WRITE = "trade:strategies:write"
