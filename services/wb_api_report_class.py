import requests
import json

class WBApiReportByPeriodClass():
    def __init__(self, NM_ID: int, LIMIT_NUMBER: int, WB_TOKEN: str, URL_REPORT_DETAIL_BY_PERIOD: str):
        self.WB_TOKEN = WB_TOKEN
        self.URL_REPORT_DETAIL_BY_PERIOD = URL_REPORT_DETAIL_BY_PERIOD
        self.HEADERS = {
            "Authorization": self.WB_TOKEN
        }
        self.PARAMS = {
            "limit": LIMIT_NUMBER,
            "filterNmID": NM_ID
        }
    def parse_spp(self):
        response = requests.get(self.URL_REPORT_DETAIL_BY_PERIOD, params=self.PARAMS, headers=self.HEADERS)
        if response.status_code == 200:
            data_json = response.json()
            print(data_json)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
        