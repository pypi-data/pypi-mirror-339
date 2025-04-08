from httpx._client import USER_AGENT

from ._base import httpx
from .async_client import AsyncClient
from .sync_client import SyncClient

__all__ = ["AsyncClient", "SyncClient", "httpx", "BASE_USER_AGENT"]

BASE_USER_AGENT = USER_AGENT
