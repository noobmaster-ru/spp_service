# клиент Wildberries API
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
import aiohttp

from core.constants import URL_POST_NM_REPORT, TIME_SLEEP
from core.interfaces import IWBApiClient


class WBApiClient(IWBApiClient):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_articles(self, token: str) -> Dict[str, Dict[str, Any]]:
        page = 1
        headers = {"Authorization": token, "Content-Type": "application/json"}
        parsed_data_api_articles: Dict[str, Dict[str, Any]] = {}

        while True:
            payload = {
                "period": {
                    "begin": str((datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)),
                    "end": str((datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)),
                },
                "page": page,
            }
            try:
                async with self.session.post(URL_POST_NM_REPORT, json=payload, headers=headers) as resp:
                    if resp.status != 200:
                        # stop paging if not OK
                        break

                    data_json = await resp.json()
                    if not isinstance(data_json, dict) or "data" not in data_json:
                        print("❌ Unexpected response format (no 'data'):", data_json)
                        break

                    data = data_json["data"]
                    cards = data.get("cards", [])
                    for card in cards:
                        parsed_data_api_articles[card["nmID"]] = {
                            "date": card["statistics"]["selectedPeriod"]["begin"][:10],
                            "nm_id": str(card["nmID"]),
                            "category": card["object"]["name"],
                            "avg_price_rub": str(card["statistics"]["selectedPeriod"]["avgPriceRub"]),
                            "remains": str(card["stocks"]["stocksMp"] + card["stocks"]["stocksWb"]),
                            "add_to_cart_percent": str(card["statistics"]["selectedPeriod"]["conversions"]["addToCartPercent"]),
                            "cart_to_order_percent": str(card["statistics"]["selectedPeriod"]["conversions"]["cartToOrderPercent"]),
                        }

                    if data.get("isNextPage"):
                        page += 1
                        await asyncio.sleep(TIME_SLEEP)
                    else:
                        break
            except Exception as e:
                print("❌ Exception in WBApiClient.fetch_articles:", repr(e))
                break
        return parsed_data_api_articles