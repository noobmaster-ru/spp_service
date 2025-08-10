# работа с JSON
import json
from typing import Any

class JsonRepository:
    def save(self, data: dict, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)