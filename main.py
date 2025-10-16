from services.wb_api_report_class import WBApiReportByPeriodClass
from dotenv import load_dotenv
import os 

def main():
    parser = WBApiReportByPeriodClass(WB_TOKEN, URL_REPORT_DETAIL_BY_PERIOD)
    parser.parse_spp()

if __name__ == "__main__":
    load_dotenv()
    WB_TOKEN = os.getenv("WB_TOKEN_STR")
    URL_REPORT_DETAIL_BY_PERIOD = os.getenv("URL_REPORT_DETAIL_BY_PERIOD_STR")
    main()