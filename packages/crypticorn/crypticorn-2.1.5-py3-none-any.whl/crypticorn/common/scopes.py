from enum import Enum


class Scope(str, Enum):
    """
    The permission scopes for the API.
    """

    # If you update anything here, also update the scopes in the auth-service repository

    @classmethod
    def from_str(cls, value: str) -> "Scope":
        return cls(value)

    # Hive scopes
    READ_HIVE_MODEL = "read:hive:model"
    READ_HIVE_DATA = "read:hive:data"
    WRITE_HIVE_MODEL = "write:hive:model"

    # Trade scopes
    READ_TRADE_BOTS = "read:trade:bots"
    WRITE_TRADE_BOTS = "write:trade:bots"
    READ_TRADE_APIKEYS = "read:trade:api_keys"
    WRITE_TRADE_APIKEYS = "write:trade:api_keys"
    READ_TRADE_ORDERS = "read:trade:orders"
    READ_TRADE_ACTIONS = "read:trade:actions"
    WRITE_TRADE_ACTIONS = "write:trade:actions"
    READ_TRADE_EXCHANGES = "read:trade:exchanges"
    READ_TRADE_FUTURES = "read:trade:futures"
    WRITE_TRADE_FUTURES = "write:trade:futures"
    READ_TRADE_NOTIFICATIONS = "read:trade:notifications"
    WRITE_TRADE_NOTIFICATIONS = "write:trade:notifications"
    READ_TRADE_STRATEGIES = "read:trade:strategies"
    WRITE_TRADE_STRATEGIES = "write:trade:strategies"

    # Payment scopes
    READ_PAY_PAYMENTS = "read:pay:payments"
    READ_PAY_PRODUCTS = "read:pay:products"
    WRITE_PAY_PRODUCTS = "write:pay:products"
    READ_PAY_NOW = "read:pay:now"
    WRITE_PAY_NOW = "write:pay:now"

    # Read projections
    READ_PREDICTIONS = "read:predictions"
