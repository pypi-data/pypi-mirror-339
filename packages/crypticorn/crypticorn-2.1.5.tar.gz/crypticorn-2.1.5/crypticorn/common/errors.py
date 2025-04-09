from enum import Enum


class ApiErrorType(str, Enum):
    """Type of API error"""

    USER_ERROR = "user error"
    """user error by people using our services"""
    EXCHANGE_ERROR = "exchange error"
    """re-tryable error by the exchange or network conditions"""
    SERVER_ERROR = "server error"
    """server error that needs a new version rollout for a fix"""
    NO_ERROR = "no error"
    """error that does not need to be handled or does not affect the program or is a placeholder."""


class ApiErrorIdentifier(str, Enum):
    """API error identifiers"""

    API_KEY_ALREADY_EXISTS = "api_key_already_exists"
    BLACK_SWAN = "black_swan"
    BOT_ALREADY_DELETED = "bot_already_deleted"
    BOT_DISABLED = "bot_disabled"
    BOT_STOPPING_COMPLETED = "bot_stopping_completed"
    CLIENT_ORDER_ID_REPEATED = "client_order_id_already_exists"
    CONTENT_TYPE_ERROR = "invalid_content_type"
    DELETE_BOT_ERROR = "delete_bot_error"
    EXCHANGE_API_KEY_IN_USE = "exchange_api_key_in_use"
    EXCHANGE_INVALID_SIGNATURE = "exchange_invalid_signature"
    EXCHANGE_INVALID_TIMESTAMP = "exchange_invalid_timestamp"
    EXCHANGE_IP_RESTRICTED = "exchange_ip_address_is_not_authorized"
    EXCHANGE_MAINTENANCE = "exchange_system_under_maintenance"
    EXCHANGE_RATE_LIMIT = "exchange_rate_limit_exceeded"
    EXCHANGE_SERVICE_UNAVAILABLE = "exchange_service_temporarily_unavailable"
    EXCHANGE_SYSTEM_BUSY = "exchange_system_is_busy"
    EXCHANGE_SYSTEM_CONFIG_ERROR = "exchange_system_configuration_error"
    EXCHANGE_SYSTEM_ERROR = "exchange_internal_system_error"
    EXCHANGE_USER_FROZEN = "exchange_user_account_is_frozen"
    EXCHANGE_PERMISSION_DENIED = "insufficient_permissions_spot_and_futures_required"
    HEDGE_MODE_NOT_ACTIVE = "hedge_mode_not_active"
    HTTP_ERROR = "http_request_error"
    INSUFFICIENT_BALANCE = "insufficient_balance"
    INSUFFICIENT_MARGIN = "insufficient_margin"
    INSUFFICIENT_SCOPES = "insufficient_scopes"
    INVALID_API_KEY = "invalid_api_key"
    INVALID_BEARER = "invalid_bearer"
    INVALID_EXCHANGE_API_KEY = "invalid_exchange_api_key"
    INVALID_MARGIN_MODE = "invalid_margin_mode"
    INVALID_PARAMETER = "invalid_parameter_provided"
    JWT_EXPIRED = "jwt_expired"
    LEVERAGE_EXCEEDED = "leverage_limit_exceeded"
    LIQUIDATION_PRICE_VIOLATION = "order_violates_liquidation_price_constraints"
    NO_CREDENTIALS = "no_credentials"
    OBJECT_NOT_FOUND = "object_not_found"
    ORDER_ALREADY_FILLED = "order_is_already_filled"
    ORDER_IN_PROCESS = "order_is_being_processed"
    ORDER_LIMIT_EXCEEDED = "order_quantity_limit_exceeded"
    ORDER_NOT_FOUND = "order_does_not_exist"
    ORDER_PRICE_INVALID = "order_price_is_invalid"
    ORDER_SIZE_TOO_LARGE = "order_size_too_large"
    ORDER_SIZE_TOO_SMALL = "order_size_too_small"
    POSITION_LIMIT_EXCEEDED = "position_limit_exceeded"
    POSITION_NOT_FOUND = "position_does_not_exist"
    POSITION_SUSPENDED = "position_opening_temporarily_suspended"
    POST_ONLY_REJECTED = "post_only_order_would_immediately_match"
    REQUEST_SCOPE_EXCEEDED = "request_scope_limit_exceeded"
    RISK_LIMIT_EXCEEDED = "risk_limit_exceeded"
    RPC_TIMEOUT = "rpc_timeout"
    SETTLEMENT_IN_PROGRESS = "system_settlement_in_process"
    STRATEGY_DISABLED = "strategy_disabled"
    SUCCESS = "success"
    SYMBOL_NOT_FOUND = "symbol_does_not_exist"
    TRADING_LOCKED = "trading_has_been_locked"
    TRADING_ACTION_EXPIRED = "trading_action_expired"
    TRADING_ACTION_SKIPPED = "trading_action_skipped"
    TRADING_SUSPENDED = "trading_is_suspended"
    UNKNOWN_ERROR = "unknown_error_occurred"
    URL_NOT_FOUND = "requested_resource_not_found"


class ApiErrorLevel(str, Enum):
    """API error levels"""

    ERROR = "error"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"


class ApiError(Enum):
    """API error codes"""

    API_KEY_ALREADY_EXISTS = (
        ApiErrorIdentifier.API_KEY_ALREADY_EXISTS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BLACK_SWAN = (
        ApiErrorIdentifier.BLACK_SWAN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.INFO,
    )
    BOT_ALREADY_DELETED = (
        ApiErrorIdentifier.BOT_ALREADY_DELETED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BOT_DISABLED = (
        ApiErrorIdentifier.BOT_DISABLED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    BOT_STOPPING_COMPLETED = (
        ApiErrorIdentifier.BOT_STOPPING_COMPLETED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    CLIENT_ORDER_ID_REPEATED = (
        ApiErrorIdentifier.CLIENT_ORDER_ID_REPEATED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    CONTENT_TYPE_ERROR = (
        ApiErrorIdentifier.CONTENT_TYPE_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    DELETE_BOT_ERROR = (
        ApiErrorIdentifier.DELETE_BOT_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_INVALID_SIGNATURE = (
        ApiErrorIdentifier.EXCHANGE_INVALID_SIGNATURE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_INVALID_TIMESTAMP = (
        ApiErrorIdentifier.EXCHANGE_INVALID_TIMESTAMP,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_IP_RESTRICTED = (
        ApiErrorIdentifier.EXCHANGE_IP_RESTRICTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_API_KEY_IN_USE = (
        ApiErrorIdentifier.EXCHANGE_API_KEY_IN_USE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_MAINTENANCE = (
        ApiErrorIdentifier.EXCHANGE_MAINTENANCE,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_PERMISSION_DENIED = (
        ApiErrorIdentifier.EXCHANGE_PERMISSION_DENIED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_RATE_LIMIT = (
        ApiErrorIdentifier.EXCHANGE_RATE_LIMIT,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SERVICE_UNAVAILABLE = (
        ApiErrorIdentifier.EXCHANGE_SERVICE_UNAVAILABLE,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_BUSY = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_BUSY,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_CONFIG_ERROR = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_CONFIG_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_ERROR = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_USER_FROZEN = (
        ApiErrorIdentifier.EXCHANGE_USER_FROZEN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    HEDGE_MODE_NOT_ACTIVE = (
        ApiErrorIdentifier.HEDGE_MODE_NOT_ACTIVE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    HTTP_ERROR = (
        ApiErrorIdentifier.HTTP_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_BALANCE = (
        ApiErrorIdentifier.INSUFFICIENT_BALANCE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_MARGIN = (
        ApiErrorIdentifier.INSUFFICIENT_MARGIN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_SCOPES = (
        ApiErrorIdentifier.INSUFFICIENT_SCOPES,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_API_KEY = (
        ApiErrorIdentifier.INVALID_API_KEY,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_BEARER = (
        ApiErrorIdentifier.INVALID_BEARER,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_EXCHANGE_API_KEY = (
        ApiErrorIdentifier.INVALID_EXCHANGE_API_KEY,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_MARGIN_MODE = (
        ApiErrorIdentifier.INVALID_MARGIN_MODE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_PARAMETER = (
        ApiErrorIdentifier.INVALID_PARAMETER,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    JWT_EXPIRED = (
        ApiErrorIdentifier.JWT_EXPIRED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    LEVERAGE_EXCEEDED = (
        ApiErrorIdentifier.LEVERAGE_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    LIQUIDATION_PRICE_VIOLATION = (
        ApiErrorIdentifier.LIQUIDATION_PRICE_VIOLATION,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    NO_CREDENTIALS = (
        ApiErrorIdentifier.NO_CREDENTIALS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    OBJECT_NOT_FOUND = (
        ApiErrorIdentifier.OBJECT_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_ALREADY_FILLED = (
        ApiErrorIdentifier.ORDER_ALREADY_FILLED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.INFO,
    )
    ORDER_IN_PROCESS = (
        ApiErrorIdentifier.ORDER_IN_PROCESS,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    ORDER_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.ORDER_LIMIT_EXCEEDED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_NOT_FOUND = (
        ApiErrorIdentifier.ORDER_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_PRICE_INVALID = (
        ApiErrorIdentifier.ORDER_PRICE_INVALID,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_SIZE_TOO_LARGE = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_LARGE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    ORDER_SIZE_TOO_SMALL = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_SMALL,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    POSITION_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.POSITION_LIMIT_EXCEEDED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    POSITION_NOT_FOUND = (
        ApiErrorIdentifier.POSITION_NOT_FOUND,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    POSITION_SUSPENDED = (
        ApiErrorIdentifier.POSITION_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    POST_ONLY_REJECTED = (
        ApiErrorIdentifier.POST_ONLY_REJECTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    REQUEST_SCOPE_EXCEEDED = (
        ApiErrorIdentifier.REQUEST_SCOPE_EXCEEDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    RISK_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.RISK_LIMIT_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    RPC_TIMEOUT = (
        ApiErrorIdentifier.RPC_TIMEOUT,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    SETTLEMENT_IN_PROGRESS = (
        ApiErrorIdentifier.SETTLEMENT_IN_PROGRESS,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    STRATEGY_DISABLED = (
        ApiErrorIdentifier.STRATEGY_DISABLED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    SUCCESS = (ApiErrorIdentifier.SUCCESS, ApiErrorType.NO_ERROR, ApiErrorLevel.SUCCESS)
    SYMBOL_NOT_FOUND = (
        ApiErrorIdentifier.SYMBOL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    TRADING_ACTION_EXPIRED = (
        ApiErrorIdentifier.TRADING_ACTION_EXPIRED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    TRADING_ACTION_SKIPPED = (
        ApiErrorIdentifier.TRADING_ACTION_SKIPPED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    TRADING_LOCKED = (
        ApiErrorIdentifier.TRADING_LOCKED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    TRADING_SUSPENDED = (
        ApiErrorIdentifier.TRADING_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    UNKNOWN_ERROR = (
        ApiErrorIdentifier.UNKNOWN_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    URL_NOT_FOUND = (
        ApiErrorIdentifier.URL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )

    @property
    def identifier(self) -> str:
        return self.value[0]

    @property
    def type(self) -> ApiErrorType:
        return self.value[1]

    @property
    def level(self) -> ApiErrorLevel:
        return self.value[2]
