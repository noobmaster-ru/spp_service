import requests
from constants import WB_TOKENS_LIST, URL_REMAINS_CREATE_REPORT, URL_GET_LIST_SELLER_WAREHOUSES
import time
import json
from collections import defaultdict

def check_report_status(task_id: str, headers: dict):
    while True:
        time.sleep(5.5) # лимит: 5 секунд - 1 запрос (ночью ооочень долгое ожидание)
        url = f'https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/status'
        response_check_report_status = requests.get(url, headers=headers, params={'task_id': task_id})
        data_check_report_status = response_check_report_status.json()
        status = data_check_report_status.get("data")["status"]
        print(status, response_check_report_status.status_code)
        if status == "done":
            break

def get_list_of_seller_warehouses(headers: dict) -> list:
    response_list_seller_warehouses = requests.get(URL_GET_LIST_SELLER_WAREHOUSES, headers=headers)
    # print(response_list_seller_warehouses.status_code)
    list = []
    data_list_seller_warehoueses =  response_list_seller_warehouses.json()
    for warehouse in data_list_seller_warehoueses:
        name = warehouse["name"] # ID склада продавца
        office_id = warehouse["officeId"] # ID склада WB
        id = warehouse["id"]
        list.append({"seller_warehouse_name": name, "id_wb_warehouse": office_id, "id_seller_warehouse":id})
    return list


def get_remains_fbw(task_id: str, headers: dict) -> dict:
    url = f'https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/download'
    response_warehouse_remains = requests.get(url, headers=headers, params={'task_id': task_id})
    print(response_warehouse_remains.status_code)
    data_remains = response_warehouse_remains.json()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_remains, f, indent=4, ensure_ascii=False)  # indent=4 для читаемости
    dict = {}
    barcodes = []
    for article in data_remains:
        # если хотим ещё что-то распарсить, то нужно будет в params_create_report добавлять флаги
        # brand = article.get("brand", None) # у некоторых артикулов нет бренда
        # subject_name = article["subjectName"] 
        nm_id = article["nmId"]
        barcodes.append(article["barcode"])
        warehouses = article.get("warehouses", []) 
        for warehouse in warehouses:
            warehouse_name = warehouse["warehouseName"]
            quantity = warehouse["quantity"]
            if warehouse_name == "Всего находится на складах" and quantity > 0:
                dict[nm_id] = quantity
    return dict, barcodes

def get_remains_fbs(warehouse_id: int, barcodes: list, headers: dict):
    
    url = f'https://marketplace-api.wildberries.ru/api/v3/stocks/{warehouse_id}'
    # Тело запроса (JSON)
    payload = {
        "skus": barcodes  # barcodes должен быть списком строк, например: ["123456789", "987654321"]
    }
    headers["Content-Type"] = "application/json"
    print("begin get_remains_fbs request")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    data_remains = response.json()
    stocks = data_remains.get("stocks", [])
    dict = {}
    for product in stocks:
        sku = product["sku"]
        amount = product["amount"]
        dict[sku] = amount
    print("dict of remains in fbs", dict)
    return dict

def main(token: str):
    headers = {
        'Authorization': token
    }

    # тут включаем артикулы ВБ (nm_id), бренд (brand)
    params_create_report = {
        "groupByNm": True,
        "groupBySubject": True,
        "groupByBrand": True,
        "groupByBarcode": True,
        "locale": "ru"
    }
    response_create_report = requests.get(URL_REMAINS_CREATE_REPORT, headers=headers, params=params_create_report)
    data_create_report = response_create_report.json()
    task_id = data_create_report.get("data").get("taskId")
    print("task_id = ", task_id)

    check_report_status(task_id, headers)
    dict_of_remains_fbw, barcodes = get_remains_fbw(task_id, headers)
    # print(dict_of_remains_fbw)
    with open('articles_and_remains_fbo.json', 'w', encoding='utf-8') as f:
        json.dump(dict_of_remains_fbw, f, indent=4, ensure_ascii=False) 
    list_of_seller_warehouses = get_list_of_seller_warehouses(headers)
    
    print("len of barcodes", len(barcodes))
    dict_of_remains_fbs = {}
    for barcode in barcodes:
        dict_of_remains_fbs[barcode] = 0
    print(dict_of_remains_fbs)
    for seller_warehouse in list_of_seller_warehouses:
        id_seller_warehouse = seller_warehouse["id_seller_warehouse"]
        remains_fbs = get_remains_fbs(id_seller_warehouse, barcodes, headers)
        for sku, amount in remains_fbs.items():
            if sku in dict_of_remains_fbs:
                dict_of_remains_fbs[sku] += amount
            else:
                dict_of_remains_fbs[sku] = amount
        # for product in remains_fbs:
        #     sku = product["sku"]
        #     if sku in dict_of_remains_fbs:
        #         dict_of_remains_fbs[sku] += product["amount"]
        #     else:
        #         dict_of_remains_fbs[sku] = product["amount"]
    print(dict_of_remains_fbs)
    with open('barcodes_and_remains_fbs.json', 'w', encoding='utf-8') as f:
        json.dump(dict_of_remains_fbs, f, indent=4, ensure_ascii=False) 





if __name__ == "__main__":
    for token in WB_TOKENS_LIST:
        main(token)
        # time.sleep(60.5)
        print("\n")
    print("the end!")