# парсинг сайта WB
import aiohttp
import math
from typing import Dict, Any

from core.interfaces import IWBSiteParser
import json 

# цена считается неправильно - неправильно парсится с сайта вб
def build_basket(short_nm_id: int) -> str:
    # Определяем basket (сокращённый вариант через switch не работает!)
    if 0 <= short_nm_id <= 143:
        basket = "01"
    elif 144 <= short_nm_id <= 287:
        basket = "02"
    elif 288 <= short_nm_id <= 431:
        basket = "03"
    elif 432 <= short_nm_id <= 719:
        basket = "04"
    elif 720 <= short_nm_id <= 1007:
        basket = "05"
    elif 1008 <= short_nm_id <= 1061:
        basket = "06"
    elif 1062 <= short_nm_id <= 1115:
        basket = "07"
    elif 1116 <= short_nm_id <= 1169:
        basket = "08"
    elif 1170 <= short_nm_id <= 1313:
        basket = "09"
    elif 1314 <= short_nm_id <= 1601:
        basket = "10"
    elif 1602 <= short_nm_id <= 1655:
        basket = "11"
    elif 1656 <= short_nm_id <= 1919:
        basket = "12"
    elif 1920 <= short_nm_id <= 2045:
        basket = "13"
    elif 2046 <= short_nm_id <= 2189:
        basket = "14"
    elif 2190 <= short_nm_id <= 2405:
        basket = "15"
    # здесь вб добавил новые basket - пришло добавить (см в network:  banners.js -> Response)
    elif 2406 <= short_nm_id <= 2621:
        basket = "16"
    elif 2622 <= short_nm_id <= 2837:
        basket = "17"
    elif 2838 <= short_nm_id <= 3053:
        basket = "18"
    elif 3054 <= short_nm_id <= 3269:
        basket = "19"
    elif 3270 <= short_nm_id <= 3485:
        basket = "20"
    elif 3486 <= short_nm_id <= 3701:
        basket = "21"
    elif 3702 <= short_nm_id <= 3917:
        basket = "22"
    elif 3918 <= short_nm_id <= 4133:
        basket = "23"
    elif 4134 <= short_nm_id <= 4349:
        basket = "24"
    elif 4350 <= short_nm_id <= 4565:
        basket = "25"
    elif 4566 <= short_nm_id <= 4877:
        basket = "26"
    elif 4878 <= short_nm_id <= 5189:
        basket = "27"
    elif 5190 <= short_nm_id <= 5501:
        basket = "28"
    elif 5502 <= short_nm_id <= 5813:
        basket = "29"
    elif 5814 <= short_nm_id <= 6125:
        basket = "30"
    elif 6126 <= short_nm_id <= 6437:
        basket = "31"
    else:
        basket = "32"
    # если ошибка будет, то возможно вб новые basket добавил
    return basket

class WBSiteParser(IWBSiteParser):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def parse_card(self, nm_id: str) -> int | str:
        try:
            int_nm_id = int(nm_id)
            short_nm_id = int_nm_id // 100000

            basket = build_basket(short_nm_id)

            headers_for_parse_description = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                'Referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx',

                # "sec-ch-ua-platform": '"Android"',
                # "Referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
                # "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
                # "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                # "sec-ch-ua-mobile": "?1",
            }
            url_for_parse_description = f"https://basket-{basket}.wbbasket.ru/vol{short_nm_id}/part{int_nm_id // 1000}/{nm_id}/info/ru/card.json"
            async with self.session.get(
                url_for_parse_description,
                headers=headers_for_parse_description,
            ) as response:
                data = await response.json()
                # data = json.loads(
                #     await response.text()
                # ) 
                list_nm_ids = data["colors"]
                nm = "".join([f"{item};" for item in list_nm_ids])
                params = {
                    "appType": "1",
                    "curr": "rub",
                    "dest": "-446115",
                    "spp": "40",
                    # "hide_dtype": "14",
                    "ab_testing": "false",
                    "lang": "ru",
                    "nm": nm[:-1],
                }
                headers = {
                    'accept': '*/*',
                    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTgxMjgxMzksInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.j6-YOl8ada1cNq4Qw9CR4Q7K7hhu3h5Ut1Iw7IpE9rwPiS8xVpbX50N2_l9IFZkHiArvAgwhqeIZLTvDVR93dBvuMeeUZWCAQRlZlqpdaRxjsiyT1sPup0l46MBGDkm9tpToYylD0qQbD-TboYsOkZTXLib-sNN2qe1qB1tg78ko0ZNzQ_bbWUfDfTHA1p1y7YVHU_PyK0YSA3z5BXA11x8Dr8v6qXbTEbi0PVn1FqYp6JWDKYPCk91v09MedMlXXdNW8K9sWSOS75Oklcf-yT8LHNv35C7HXFoomgQqXjlwTOf0OJJRDbgzl78gCZgsl4Xu7rK1fBSljGfLqEQ86g',
                    'origin': 'https://www.wildberries.ru',
                    'priority': 'u=1, i',
                    'referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
                    'x-pow': '2|site_4ece2ced581641d698ba9fe48af98991|1758184911|8,8,1,28f5c28f5c28f5c,9f1a690d-f890-488e-9e5d-848fc8d61d72,d6620ca4-6916-455c-ae1f-994644b941d6,1758185091,1,6eMQre2Zz4fRrxkIJezI3plDe0hsZv8SbcOdnrjLk3I=,7c99ada4bd882876acd9a427e27aae9015be2a8fb96428c81fddaa769fe7d4d79741a8ee0b9e919cba1626789a07a5107c0a56dc464cef7f652f7414a1db6bf5|46',
                }
                async with self.session.get("https://card.wb.ru/cards/v4/detail", params=params, headers=headers) as resp:
                    data = json.loads(
                        await resp.text()
                    ) 
                    # data = await resp.json()
                    products = data["products"]
                    for product in products:
                        if int(product["id"]) == int(nm_id):
                            sizes = product["sizes"]
                            return sizes[0]["price"]["product"]
                            # for size in sizes:
                                # if "price" in size:
                                # return size["price"]["product"]
                    print("dont find nm_id")
                    return "Error in parse_card"
        except Exception as e:
            # keep behavior similar to original
            print(f"aaaa error in parse_card, {str(e)}")
            return "Нет в наличии"

    async def parse_grade(self, nm_id: str) -> int | str:
        try:
            params = {"curr": "RUB"}
            headers = {
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTgxMjgxMzksInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.j6-YOl8ada1cNq4Qw9CR4Q7K7hhu3h5Ut1Iw7IpE9rwPiS8xVpbX50N2_l9IFZkHiArvAgwhqeIZLTvDVR93dBvuMeeUZWCAQRlZlqpdaRxjsiyT1sPup0l46MBGDkm9tpToYylD0qQbD-TboYsOkZTXLib-sNN2qe1qB1tg78ko0ZNzQ_bbWUfDfTHA1p1y7YVHU_PyK0YSA3z5BXA11x8Dr8v6qXbTEbi0PVn1FqYp6JWDKYPCk91v09MedMlXXdNW8K9sWSOS75Oklcf-yT8LHNv35C7HXFoomgQqXjlwTOf0OJJRDbgzl78gCZgsl4Xu7rK1fBSljGfLqEQ86g',
                'origin': 'https://www.wildberries.ru',
                'priority': 'u=1, i',
                'referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
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