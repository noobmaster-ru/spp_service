# абстракции (интерфейсы)
# core/interfaces.py
from typing import Protocol, Dict, Any


class IWBApiClient(Protocol):
    async def fetch_articles(self, token: str) -> Dict[str, Dict[str, Any]]:
        ...


class IWBSiteParser(Protocol):
    async def fetch_price_data(self, nm_id: str) -> Dict[str, str]:
        ...


class IJsonRepository(Protocol):
    def save(self, data: dict, path: str) -> None: ...
    def load(self, path: str) -> dict: ...