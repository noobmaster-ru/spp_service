from gspread import Client, service_account
from gspread_dataframe import set_with_dataframe
import pandas as pd

class GoogleSheetSaver:
    def __init__(self, service_account_json: str, table_url: str):
        self.client = service_account(filename=service_account_json)
        self.spreadsheet = self.client.open_by_url(table_url)


    def write_data_to_google_sheet(self, df: pd.DataFrame):
        spp_sheet = self.spreadsheet.worksheet("spp")
        
        # очищаем лист перед записью
        spp_sheet.clear()

        # пишем DataFrame в Google Sheets (с заголовками)
        set_with_dataframe(spp_sheet, df, include_index=False, include_column_header=True, resize=True)
        print("✅ Данные записаны в Google Sheets (вкладка 'spp')")
