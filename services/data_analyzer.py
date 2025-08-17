# анализ данных
import pandas as pd
import numpy as np
from typing import Dict
from repositories.csv_repository import CSVRepository
from core.constants import WB_CATEGORY_CSV, DF_FILTERED_PATH, SERVICE_ACCOUNT_JSON, GOOGLE_SHEETS_URL
import os
from datetime import datetime

from services.google_sheets_saver import GoogleSheetSaver

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
        df_filtred["nm_id"] = df_filtred["nm_id"].astype(int)
        df_filtred = df_filtred.reset_index(drop=True)
        
        
        # считаем спп по часу и записываем в новый столбец
        hour = datetime.now().strftime("%H")
        new_col = f"spp{hour}"
        # считаем новый столбец спп
        df_filtred[new_col] = round(
            1 - df_filtred["price_with_spp"] / df_filtred["avg_price_rub"], 2
        )


        # save dataframe with f"spp{hour}""
        if os.path.exists(DF_FILTERED_PATH):
            df_old = pd.read_csv(DF_FILTERED_PATH)

            # если столбец с таким именем уже есть → убираем его (будет перезаписан)
            if new_col in df_old.columns:
                df_old.drop(columns=[new_col], inplace=True)

            df_old['nm_id'] = df_old['nm_id'].astype(int)
            spp_cols = sorted([c for c in df_old.columns if c.startswith("spp")])
            df_old[spp_cols] = df_old[spp_cols].astype(float)

            # делаем outer merge только с нужными колонками
            df_merged = df_old.merge(
                df_filtred[["nm_id", "category", new_col]],
                on="nm_id",
                how="outer"
            )

            # если в merge появились дубликаты category → оставляем старое или новое
            if "category_x" in df_merged.columns and "category_y" in df_merged.columns:
                df_merged["category"] = df_merged["category_x"].combine_first(df_merged["category_y"])
                df_merged.drop(["category_x", "category_y"], axis=1, inplace=True)

            # сортируем по category
            df_merged = df_merged.sort_values("category").reset_index(drop=True)


            # порядок колонок: nm_id, category, потом все spp*
            spp_cols = sorted([c for c in df_merged.columns if c.startswith("spp")])
            df_merged = df_merged[["nm_id", "category"] + spp_cols]
            
            # сохраняем в csv и google sheets
            self.csv_repo.save(df_merged, DF_FILTERED_PATH, index=False)
            GoogleSheetSaver(SERVICE_ACCOUNT_JSON, GOOGLE_SHEETS_URL).write_data_to_google_sheet(df_merged)
            
            print(f"✅ Анализ завершён, час: {hour}, {len(df_merged)} строк добавлено в", DF_FILTERED_PATH)
        else:
            # сортируем по категории
            df_filtred = df_filtred.sort_values("category").reset_index(drop=True)

            # файла нет → создаём с нужными колонками 
            df_save = df_filtred[["nm_id", "category", new_col]]


            # сохраняем в csv и google sheets
            self.csv_repo.save(df_save, DF_FILTERED_PATH, index=False)
            GoogleSheetSaver(SERVICE_ACCOUNT_JSON, GOOGLE_SHEETS_URL).write_data_to_google_sheet(df_save)

            print(f"✅ Анализ завершён, час {hour}, {len(df_save)} строк сохранено в", DF_FILTERED_PATH)
        