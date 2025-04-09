"""Constants for the shardcast package."""

from typing import TYPE_CHECKING, Any, List
import os

if TYPE_CHECKING:
    SHARD_SIZE: int = 50_000_000
    MAX_DISTRIBUTION_FOLDERS: int = 15
    HTTP_PORT: int = 8000
    MAX_MIDDLE_NODE_LAYERS: int = 2
    RETRY_ATTEMPTS: int = 5
    FAST_RETRY_ATTEMPTS: int = 3
    FAST_RETRY_INTERVAL: int = 2
    SLOW_RETRY_INTERVAL: int = 15
    LOG_LEVEL: str = "INFO"
    DISTRIBUTION_FILE: str = "distribution.txt"
    HTTP_TIMEOUT: int = 30
    MAX_CONCURRENT_DOWNLOADS: int = 10
    VERSION_PREFIX: str = "v"

_env = {
    "SHARD_SIZE": lambda: int(os.getenv("SHARD_SIZE", "50000000")),
    "MAX_DISTRIBUTION_FOLDERS": lambda: int(os.getenv("MAX_DISTRIBUTION_FOLDERS", "15")),
    "HTTP_PORT": lambda: int(os.getenv("HTTP_PORT", "8000")),
    "MAX_MIDDLE_NODE_LAYERS": lambda: int(os.getenv("MAX_MIDDLE_NODE_LAYERS", "2")),
    "RETRY_ATTEMPTS": lambda: int(os.getenv("RETRY_ATTEMPTS", "5")),
    "FAST_RETRY_ATTEMPTS": lambda: int(os.getenv("FAST_RETRY_ATTEMPTS", "3")),
    "FAST_RETRY_INTERVAL": lambda: int(os.getenv("FAST_RETRY_INTERVAL", "2")),
    "SLOW_RETRY_INTERVAL": lambda: int(os.getenv("SLOW_RETRY_INTERVAL", "15")),
    "LOG_LEVEL": lambda: os.getenv("LOG_LEVEL", "INFO"),
    "DISTRIBUTION_FILE": lambda: os.getenv("DISTRIBUTION_FILE", "distribution.txt"),
    "HTTP_TIMEOUT": lambda: int(os.getenv("HTTP_TIMEOUT", "30")),
    "MAX_CONCURRENT_DOWNLOADS": lambda: int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "10")),
    "VERSION_PREFIX": lambda: os.getenv("VERSION_PREFIX", "v"),
}


def __getattr__(name: str) -> Any:
    if name not in _env:
        raise AttributeError(f"Invalid environment variable: {name}")
    return _env[name]()


def __dir__() -> List[str]:
    return list(_env.keys())
