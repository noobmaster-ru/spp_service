# объединение JSON-файлов
import os
import json
from typing import Dict


class DataMergerService:
    def __init__(self, folder_path: str = "results"):
        self.folder_path = folder_path

    def merge(self) -> Dict:
        merged_data = {}
        if not os.path.exists(self.folder_path):
            print(f"⚠️ results folder {self.folder_path} not found")
            return merged_data

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if not content:
                            print(f"⚠️ Пустой файл пропущен: {filename}")
                            continue
                        data = json.loads(content)
                        if not isinstance(data, dict):
                            print(f"⚠️ Структура не словарь: {filename}")
                            continue
                        merged_data.update(data)
                except json.JSONDecodeError as e:
                    print(f"❌ Ошибка декодирования JSON в {filename}: {e}")
        return merged_data