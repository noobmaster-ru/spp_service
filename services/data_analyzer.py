# анализ данных
import pandas as pd
from typing import Dict
from repositories.csv_repository import CSVRepository
from core.constants import WB_CATEGORY_CSV, DF_FILTERED_PATH
import os

class DataAnalyzerService:
    def __init__(self, csv_repo: CSVRepository):
        self.csv_repo = csv_repo

    def analyze_and_save(self, merged_data: Dict[str, Dict]):
        # build df
        columns_order = [
            "date",
            "nm_id",
            "category",
            "avg_price_rub",
            "remains",
            "add_to_cart_percent",
            "cart_to_order_percent",
            "price_with_spp_and_wb_wallet",
            "price_with_spp",
        ]

        if not merged_data:
            print("⚠️ Нет данных для анализа")
            return
        df_main = pd.DataFrame(columns=columns_order)
        df_new = pd.DataFrame.from_dict(merged_data, orient="index")
        # ensure columns exist
        df_new = df_new[columns_order]
        df_main = pd.concat([df_main, df_new])
        # filter remains
        df_with_remains = df_main[df_main["remains"] != "0"]

        # read categories from wb csv (semicolon separated)
        try:
            df_category_wb_csv = self.csv_repo.read(WB_CATEGORY_CSV, sep=";")
            df_category_wb = pd.DataFrame(df_category_wb_csv["Название ниши"].copy())
            df_category_wb = df_category_wb.rename(columns={"Название ниши": "category"})
        except Exception as e:
            print("⚠️ Ошибка чтения WB category csv:", e)
            df_category_wb = pd.DataFrame(columns=["category"])

        df_category_our = pd.DataFrame(df_with_remains[["nm_id", "category", "avg_price_rub", "price_with_spp"]].copy())
        df_category_our = df_category_our.reset_index(drop=True)

        df_filtred = df_category_our[
            (df_category_our["price_with_spp"] != "Нет в наличии") &
            (df_category_our["avg_price_rub"] != "0")
        ].copy()

        # convert to numeric
        df_filtred["avg_price_rub"] = df_filtred["avg_price_rub"].astype(int)
        df_filtred["price_with_spp"] = df_filtred["price_with_spp"].astype(int)
        df_filtred = df_filtred.reset_index(drop=True)
        df_filtred["spp"] = round(1 - df_filtred["price_with_spp"] / df_filtred["avg_price_rub"], 2)
        df_filtred = df_filtred.sort_values("category")

        # save
        os.makedirs("data", exist_ok=True)
        self.csv_repo.save(df_filtred, DF_FILTERED_PATH, index=False)
        df_filtred.to_csv('df_filtered.csv', index=False)
        print(f"✅ Анализ завершён, {len(df_filtred)} сохранено:", DF_FILTERED_PATH)
        # print(df_filtred.head(5))