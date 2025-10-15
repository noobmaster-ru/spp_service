from services.wb_api_report_class import WBApiReportByPeriodClass
from dotenv import load_dotenv
import os 

def main():
    parser = WBApiReportByPeriodClass(NM_ID, LIMIT_NUMBER, WB_TOKEN, URL_REPORT_DETAIL_BY_PERIOD)
    parser.parse_spp()

if __name__ == "__main__":
    load_dotenv()
    NM_ID = int(os.getenv("NM_ID_INT"))
    LIMIT_NUMBER = int(os.getenv("LIMIT_NUMBER_INT"))
    WB_TOKEN = os.getenv("WB_TOKEN_STR")
    URL_REPORT_DETAIL_BY_PERIOD = os.getenv("URL_REPORT_DETAIL_BY_PERIOD_STR")
    main()