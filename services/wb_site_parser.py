# парсинг сайта WB
import aiohttp
import math
from typing import Dict, Any

from core.interfaces import IWBSiteParser


class WBSiteParser(IWBSiteParser):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def parse_card(self, nm_id: str) -> int | str:
        try:
            params = {
                "appType": "1",
                "curr": "rub",
                "dest": "-446115",
                "spp": "30",
                "hide_dtype": "14",
                "ab_testing": "false",
                "lang": "ru",
                "nm": nm_id,
            }
            async with self.session.get("https://card.wb.ru/cards/v4/detail", params=params) as resp:
                data = await resp.json()
                products = data["products"]
                for product in products:
                    if int(product["id"]) == int(nm_id):
                        sizes = product["sizes"]
                        for size in sizes:
                            if "price" in size:
                                return size["price"]["product"]
                return "Error in parse_card"
                # return "Нет в наличии"
        except Exception as e:
            # keep behavior similar to original
            return "Нет в наличии"

    async def parse_grade(self, nm_id: str) -> int | str:
        try:
            params = {"curr": "RUB"}
            headers = {
                "accept": "*/*",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTMyODA5NTAsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.j9wIg5qrJQ704rUBoGluS799qRoPMo5jAntv6oAnWeZG3ziD1dYR6Wusv-YE_InVoJP8IOpxdsODn5m2L7mrdCG-3YTl4wBz1MRRblvdxUpeBHiGZUHwE0t1bVDDpxv-NjcTVpjTnuAnvTXeMlciTJhnofkzO_Af6wHw-WpyKc-QMoiYb0qlY2qL1YKRMoQ4eTL6S4gvR5aBu-yL4i32tElhrCugn6sLKPjTpGuuzr6KLXflAolrLQ9nVNxX-R0CrMIm_PEiNo1sNFs19a2zTYg6cL9rDEK9L_JZbXcZQJTPkO7o4hTzb3bRp0zIoPnLGinZGmaHONeE2wNoZpxz8g",
                "origin": "https://www.wildberries.ru",
                "priority": "u=1, i",
                "referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=SP",
                "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
            }
            async with self.session.get("https://user-grade.wildberries.ru/api/v5/grade", params=params, headers=headers) as resp:
                data = await resp.json()
                return data["payload"]["payments"][0]["full_discount"]
        except Exception:
            return "Нет в наличии"

    async def fetch_price_data(self, nm_id: str) -> Dict[str, str]:
        full_discount = await self.parse_grade(nm_id)
        price_with_spp = await self.parse_card(nm_id)

        if isinstance(full_discount, int) and isinstance(price_with_spp, int):
            wallet_price = math.floor((price_with_spp / 100) * (1 - full_discount / 100))
            return {"price_with_spp_and_wb_wallet": str(wallet_price), "price_with_spp": str(price_with_spp // 100)}
        else:
            return {"price_with_spp_and_wb_wallet": "Нет в наличии", "price_with_spp": "Нет в наличии"}