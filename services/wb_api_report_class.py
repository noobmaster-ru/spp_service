import requests

class WBApiReportByPeriodClass():
    def __init__(self, WB_TOKEN: str, URL_REPORT_DETAIL_BY_PERIOD: str):
        self.WB_TOKEN = WB_TOKEN
        self.URL_REPORT_DETAIL_BY_PERIOD = URL_REPORT_DETAIL_BY_PERIOD
        self.HEADERS = {
            "Authorization": self.WB_TOKEN
        }
        self.PARAMS = {
            "dateFrom": "2025-10-14",
            "dateTo": "2025-10-15",
            "period": "daily"
        }
    def parse_spp(self):
        response = requests.get(self.URL_REPORT_DETAIL_BY_PERIOD, params=self.PARAMS, headers=self.HEADERS)
        print(response.status_code)