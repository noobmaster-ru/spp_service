import requests
import json
from datetime import date

class WBApiReportByPeriodClass():
    def __init__(self, WB_TOKEN: str, URL_REPORT_DETAIL_BY_PERIOD: str):
        self.WB_TOKEN = WB_TOKEN
        self.URL_REPORT_DETAIL_BY_PERIOD = URL_REPORT_DETAIL_BY_PERIOD
        self.HEADERS = {
            "Authorization": self.WB_TOKEN
        }
        self.PARAMS = {
            "dateFrom": date.today()
        }
    def parse_spp(self):
        response = requests.get(self.URL_REPORT_DETAIL_BY_PERIOD, headers=self.HEADERS, params=self.PARAMS)
        if response.status_code == 200:
            dict_nm_id_spp = {}
            data_json = response.json()
            for item in data_json:
                nm_id = item["nmId"]
                dict_nm_id_spp[nm_id] = item["spp"]
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(dict_nm_id_spp, f, indent=4, ensure_ascii=False)
        else:
            print(response.json())
        