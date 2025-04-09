from enum import Enum


class Domain(Enum):
    PROD = "crypticorn.com"
    DEV = "crypticorn.dev"


class BaseURL(Enum):
    PROD = "https://api.crypticorn.com"
    DEV = "https://api.crypticorn.dev"
    LOCAL = "http://localhost"
    DOCKER = "http://host.docker.internal"


class ApiVersion(Enum):
    V1 = "v1"


class Service(Enum):
    HIVE = "hive"
    KLINES = "klines"
    PAY = "pay"
    TRADE = "trade"
    AUTH = "auth"
    METRICS = "metrics"
