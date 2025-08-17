# сценарий: поиск spp по nm_id
import requests
import pandas as pd
from repositories.csv_repository import CSVRepository
from repositories.json_repository import JsonRepository
from core.constants import DF_FILTERED_PATH, DF_ANSWER_PATH


def build_basket(nm_id: int) -> str:
    short_nm_id = nm_id // 100000
    if 0 <= short_nm_id <= 143:
        return "01"
    elif 144 <= short_nm_id <= 287:
        return "02"
    elif 288 <= short_nm_id <= 431:
        return "03"
    elif 432 <= short_nm_id <= 719:
        return "04"
    elif 720 <= short_nm_id <= 1007:
        return "05"
    elif 1008 <= short_nm_id <= 1061:
        return "06"
    elif 1062 <= short_nm_id <= 1115:
        return "07"
    elif 1116 <= short_nm_id <= 1169:
        return "08"
    elif 1170 <= short_nm_id <= 1313:
        return "09"
    elif 1314 <= short_nm_id <= 1601:
        return "10"
    elif 1602 <= short_nm_id <= 1655:
        return "11"
    elif 1656 <= short_nm_id <= 1919:
        return "12"
    elif 1920 <= short_nm_id <= 2045:
        return "13"
    elif 2046 <= short_nm_id <= 2189:
        return "14"
    elif 2190 <= short_nm_id <= 2405:
        return "15"
    elif 2406 <= short_nm_id <= 2621:
        return "16"
    elif 2622 <= short_nm_id <= 2837:
        return "17"
    elif 2838 <= short_nm_id <= 3053:
        return "18"
    elif 3054 <= short_nm_id <= 3269:
        return "19"
    elif 3270 <= short_nm_id <= 3485:
        return "20"
    elif 3486 <= short_nm_id <= 3701:
        return "21"
    elif 3702 <= short_nm_id <= 3917:
        return "22"
    elif 3918 <= short_nm_id <= 4133:
        return "23"
    elif 4134 <= short_nm_id <= 4349:
        return "24"
    elif 4350 <= short_nm_id <= 4565:
        return "25"
    else:
        return "26"


def parse_category(nm_id: int) -> str:
    headers = {
        "sec-ch-ua-platform": '"Android"',
        "Referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
        "User-Agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 CrKey/1.54.248666",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
    }
    basket = build_basket(nm_id)
    response = requests.get(f"https://basket-{basket}.wbbasket.ru/vol{nm_id // 100000}/part{nm_id // 1000}/{nm_id}/info/ru/card.json", headers=headers)
    data = response.json()
    return data.get("subj_name", "")


def find_spp_by_nm_id(nm_id: int):
    csv_repo = CSVRepository()
    json_repo = JsonRepository()
    try:
        df = csv_repo.read(DF_FILTERED_PATH)
    except Exception as e:
        print("⚠️ Не удалось прочитать df_filtered:", e)
        return

    category = parse_category(nm_id)
    print("\nCategory from WB:", category)
    filtered = df[df["category"] == category].copy()
    if filtered.empty:
        print("⚠️ Нет записей для категории:", category)
        return

    result = filtered.copy()
    # индексы приведём к нулю
    result = result.reset_index(drop=True)
    # print(result)

    dict_from_df = result.groupby('category').apply(lambda x: x.to_dict('index'),include_groups = False).to_dict()
    json_repo.save(dict_from_df, DF_ANSWER_PATH)
    print(f"✅ Saved to {DF_ANSWER_PATH}")
