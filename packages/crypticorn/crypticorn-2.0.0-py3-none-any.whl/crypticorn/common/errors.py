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

    SUCCESS = "success"
    UNAUTHORIZED = "invalid_api_key"
    INVALID_SIGNATURE = "invalid_signature"
    INVALID_TIMESTAMP = "invalid_timestamp"
    IP_RESTRICTED = "ip_address_is_not_authorized"
    PERMISSION_DENIED = "insufficient_permissions_spot_and_futures_required"
    USER_FROZEN = "user_account_is_frozen"
    RATE_LIMIT = "rate_limit_exceeded"
    INVALID_PARAMETER = "invalid_parameter_provided"
    REQUEST_SCOPE_EXCEEDED = "request_scope_limit_exceeded"
    CONTENT_TYPE_ERROR = "invalid_content_type"
    URL_NOT_FOUND = "requested_resource_not_found"
    ORDER_NOT_FOUND = "order_does_not_exist"
    ORDER_ALREADY_FILLED = "order_is_already_filled"
    ORDER_IN_PROCESS = "order_is_being_processed"
    ORDER_LIMIT_EXCEEDED = "order_quantity_limit_exceeded"
    ORDER_PRICE_INVALID = "order_price_is_invalid"
    POST_ONLY_REJECTED = "post_only_order_would_immediately_match"
    SYMBOL_NOT_FOUND = "symbol_does_not_exist"
    CLIENT_ORDER_ID_REPEATED = "client_order_id_already_exists"

    POSITION_NOT_FOUND = "position_does_not_exist"
    POSITION_LIMIT_EXCEEDED = "position_limit_exceeded"
    POSITION_SUSPENDED = "position_opening_temporarily_suspended"
    INSUFFICIENT_BALANCE = "insufficient_balance"
    INSUFFICIENT_MARGIN = "insufficient_margin"

    LEVERAGE_EXCEEDED = "leverage_limit_exceeded"
    RISK_LIMIT_EXCEEDED = "risk_limit_exceeded"
    LIQUIDATION_PRICE_VIOLATION = "order_violates_liquidation_price_constraints"
    INVALID_MARGIN_MODE = "invalid_margin_mode"

    SYSTEM_ERROR = "internal_system_error"
    SYSTEM_CONFIG_ERROR = "system_configuration_error"
    SERVICE_UNAVAILABLE = "service_temporarily_unavailable"
    SYSTEM_BUSY = "system_is_busy_please_try_again_later"
    MAINTENANCE = "system_under_maintenance"
    RPC_TIMEOUT = "rpc_timeout"
    SETTLEMENT_IN_PROGRESS = "system_settlement_in_process"

    TRADING_SUSPENDED = "trading_is_suspended"
    TRADING_LOCKED = "trading_has_been_locked"

    UNKNOWN_ERROR = "unknown_error_occurred"
    HTTP_ERROR = "http_request_error"
    BLACK_SWAN = "black_swan"

    # our bot errors
    ACTION_EXPIRED = "trading_action_expired"
    ACTION_SKIPPED = "trading_action_skipped"
    BOT_DISABLED = "bot_disabled"
    ORDER_SIZE_TOO_SMALL = "order_size_too_small"
    ORDER_SIZE_TOO_LARGE = "order_size_too_large"
    HEDGE_MODE_NOT_ACTIVE = "hedge_mode_not_active"

    # our API errors
    API_KEY_ALREADY_EXISTS = "api_key_already_exists"
    DELETE_BOT_ERROR = "delete_bot_error"
    JWT_EXPIRED = "jwt_expired"
    BOT_STOPPING_COMPLETED = "bot_stopping_completed"
    OBJECT_NOT_FOUND = "object_not_found"
    STRATEGY_DISABLED = "strategy_disabled"
    API_KEY_IN_USE = "api_key_in_use_by_bots"
    BOT_ALREADY_DELETED = "bot_already_deleted"

    # our auth errors
    INVALID_API_KEY = "invalid_api_key"
    INVALID_BEARER = "invalid_bearer"
    NO_CREDENTIALS = "no_credentials"
    INSUFFICIENT_SCOPES = "insufficient_scopes"


class ApiErrorLevel(str, Enum):
    ERROR = "error"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"


class ApiError(Enum):
    """API error codes"""

    # Success
    SUCCESS = (ApiErrorIdentifier.SUCCESS, ApiErrorType.NO_ERROR, ApiErrorLevel.SUCCESS)
    # Authentication/Authorization
    UNAUTHORIZED = (
        ApiErrorIdentifier.UNAUTHORIZED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_SIGNATURE = (
        ApiErrorIdentifier.INVALID_SIGNATURE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_TIMESTAMP = (
        ApiErrorIdentifier.INVALID_TIMESTAMP,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    IP_RESTRICTED = (
        ApiErrorIdentifier.IP_RESTRICTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    PERMISSION_DENIED = (
        ApiErrorIdentifier.PERMISSION_DENIED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    USER_FROZEN = (
        ApiErrorIdentifier.USER_FROZEN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )

    # Rate Limiting
    RATE_LIMIT = (
        ApiErrorIdentifier.RATE_LIMIT,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )

    # Invalid Parameters
    INVALID_PARAMETER = (
        ApiErrorIdentifier.INVALID_PARAMETER,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    REQUEST_SCOPE_EXCEEDED = (
        ApiErrorIdentifier.REQUEST_SCOPE_EXCEEDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    CONTENT_TYPE_ERROR = (
        ApiErrorIdentifier.CONTENT_TYPE_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    URL_NOT_FOUND = (
        ApiErrorIdentifier.URL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    SYMBOL_NOT_FOUND = (
        ApiErrorIdentifier.SYMBOL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )

    # Order Related
    ORDER_NOT_FOUND = (
        ApiErrorIdentifier.ORDER_NOT_FOUND,
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
    ORDER_PRICE_INVALID = (
        ApiErrorIdentifier.ORDER_PRICE_INVALID,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    POST_ONLY_REJECTED = (
        ApiErrorIdentifier.POST_ONLY_REJECTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BLACK_SWAN = (
        ApiErrorIdentifier.BLACK_SWAN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.INFO,
    )
    CLIENT_ORDER_ID_REPEATED = (
        ApiErrorIdentifier.CLIENT_ORDER_ID_REPEATED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    # CONTRA_ORDER_MISSING = "No contra order available"

    # Position Related
    POSITION_NOT_FOUND = (
        ApiErrorIdentifier.POSITION_NOT_FOUND,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )  # not an error because user can close a position manually which we don't know about
    POSITION_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.POSITION_LIMIT_EXCEEDED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    POSITION_SUSPENDED = (
        ApiErrorIdentifier.POSITION_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    # FUTURES_BRAWL_RESTRICTED = "Operation restricted for Futures Brawl", ApiErrorType.USER_ERROR

    # Balance/Margin
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

    # Leverage/Risk
    LEVERAGE_EXCEEDED = (
        ApiErrorIdentifier.LEVERAGE_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    RISK_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.RISK_LIMIT_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    LIQUIDATION_PRICE_VIOLATION = (
        ApiErrorIdentifier.LIQUIDATION_PRICE_VIOLATION,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_MARGIN_MODE = (
        ApiErrorIdentifier.INVALID_MARGIN_MODE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )

    # System Status
    SYSTEM_ERROR = (
        ApiErrorIdentifier.SYSTEM_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    SYSTEM_CONFIG_ERROR = (
        ApiErrorIdentifier.SYSTEM_CONFIG_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    SERVICE_UNAVAILABLE = (
        ApiErrorIdentifier.SERVICE_UNAVAILABLE,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    SYSTEM_BUSY = (
        ApiErrorIdentifier.SYSTEM_BUSY,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    MAINTENANCE = (
        ApiErrorIdentifier.MAINTENANCE,
        ApiErrorType.EXCHANGE_ERROR,
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

    # Trading Status
    TRADING_SUSPENDED = (
        ApiErrorIdentifier.TRADING_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    TRADING_LOCKED = (
        ApiErrorIdentifier.TRADING_LOCKED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )

    # Generic
    UNKNOWN_ERROR = (
        ApiErrorIdentifier.UNKNOWN_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    HTTP_ERROR = (
        ApiErrorIdentifier.HTTP_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )

    # Our Bot Errors
    ACTION_EXPIRED = (
        ApiErrorIdentifier.ACTION_EXPIRED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    ACTION_SKIPPED = (
        ApiErrorIdentifier.ACTION_SKIPPED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    BOT_DISABLED = (
        ApiErrorIdentifier.BOT_DISABLED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    ORDER_SIZE_TOO_SMALL = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_SMALL,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    ORDER_SIZE_TOO_LARGE = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_LARGE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    HEDGE_MODE_NOT_ACTIVE = (
        ApiErrorIdentifier.HEDGE_MODE_NOT_ACTIVE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )

    # our API errors
    API_KEY_ALREADY_EXISTS = (
        ApiErrorIdentifier.API_KEY_ALREADY_EXISTS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    DELETE_BOT_ERROR = (
        ApiErrorIdentifier.DELETE_BOT_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    JWT_EXPIRED = (
        ApiErrorIdentifier.JWT_EXPIRED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BOT_STOPPING_COMPLETED = (
        ApiErrorIdentifier.BOT_STOPPING_COMPLETED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    OBJECT_NOT_FOUND = (
        ApiErrorIdentifier.OBJECT_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    STRATEGY_DISABLED = (
        ApiErrorIdentifier.STRATEGY_DISABLED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    API_KEY_IN_USE = (
        ApiErrorIdentifier.API_KEY_IN_USE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BOT_ALREADY_DELETED = (
        ApiErrorIdentifier.BOT_ALREADY_DELETED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )

    # our auth errors
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
    NO_CREDENTIALS = (
        ApiErrorIdentifier.NO_CREDENTIALS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_SCOPES = (
        ApiErrorIdentifier.INSUFFICIENT_SCOPES,
        ApiErrorType.USER_ERROR,
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
