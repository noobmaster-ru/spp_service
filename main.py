from services.wb_api_report_class import WBApiReportByPeriodClass

from dotenv import load_dotenv
import os 

def main():
    parser = WBApiReportByPeriodClass(
        WB_TOKEN, 
        URL_REPORT_DETAIL_BY_PERIOD,
        URL_GOODS_FILTER, 
        MINUTES_STEP
    )
    all_nm_id = parser.get_all_nm_id()
    parser.parse_spp(all_nm_id)


if __name__ == "__main__":
    load_dotenv()
    WB_TOKEN = os.getenv("WB_TOKEN_STR")
    MINUTES_STEP = int(os.getenv("MINUTES_STEP_INT"))

    URL_GOODS_FILTER = os.getenv("URL_GOODS_FILTER_STR")
    URL_REPORT_DETAIL_BY_PERIOD = os.getenv("URL_REPORT_DETAIL_BY_PERIOD_STR")
    main()