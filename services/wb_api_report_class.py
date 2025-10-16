import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import time 

class WBApiReportByPeriodClass():
    def __init__(
        self, 
        WB_TOKEN: str, 
        URL_REPORT_DETAIL_BY_PERIOD: str, 
        URL_GOODS_FILTER: str,
        MINUTES_STEP:int
    ):
        self.WB_TOKEN = WB_TOKEN
        self.URL_REPORT_DETAIL_BY_PERIOD = URL_REPORT_DETAIL_BY_PERIOD
        self.URL_GOODS_FILTER = URL_GOODS_FILTER
        self.HEADERS = {
            "Authorization": self.WB_TOKEN,
            "Content-Type": "application/json"
        }
        self.PARAMS = {
            "dateFrom": (datetime.now() - timedelta(minutes=MINUTES_STEP)).strftime("%Y-%m-%dT%H:%M:%S")
        }
    
    def parse_spp(self, list_all_nm_id: list):
        response = requests.get(self.URL_REPORT_DETAIL_BY_PERIOD, headers=self.HEADERS, params=self.PARAMS)
        main_dict = {"time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        dict_nm_id_spp = {}
        for nm_id in list_all_nm_id:
            dict_nm_id_spp[nm_id] = None

        if response.status_code == 200:
            data_json = response.json()
            for item in data_json:
                nm_id = item["nmId"]
                dict_nm_id_spp[nm_id] = item["spp"]
            main_dict["spp_per_nm_id"] = dict_nm_id_spp
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(main_dict, f, indent=4, ensure_ascii=False)
        else:
            print(response.json())

    # определяем все артикулы продавца    
    def get_all_nm_id(self):
        all_items = []
        limit = 1000
        offset = 0
        backoff = 1.0

        while True:
            try:
                resp = self.fetch_page(self.URL_GOODS_FILTER, self.HEADERS, limit=limit, offset=offset)
            except requests.RequestException as e:
                print("Network error:", e, "— повтор через", backoff, "c")
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
                continue

            if resp.status_code == 200:
                backoff = 1.0
                data = resp.json()
                # структура: data["data"]["listGoods"] (см. документацию)
                goods = data.get("data", {}).get("listGoods") or []
                if not goods:
                    break

                for g in goods:
                    nmID = g.get("nmID")
                    # vendorCode = g.get("vendorCode")  # это артикул продавца
                    all_items.append(nmID)
                offset += limit
                # небольшой sleep чтобы не попасть в лимит
                time.sleep(0.15)
            elif resp.status_code == 429:
                # слишком много запросов — exponential backoff
                print("429 Too Many Requests — делаем backoff", backoff, "c")
                time.sleep(backoff)
                backoff = min(backoff * 2, 30)
            elif resp.status_code in (401, 403):
                raise SystemExit(f"Ошибка авторизации (HTTP {resp.status_code}). Проверьте токен и права.")
            else:
                raise SystemExit(f"HTTP {resp.status_code}: {resp.text}")

        return all_items
    
    @staticmethod
    def fetch_page(BASE_URL: str, HEADERS: dict, limit=1000, offset=0):
        params = {"limit": limit, "offset": offset}
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
        return resp  
    