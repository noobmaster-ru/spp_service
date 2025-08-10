# работа с CSV
import pandas as pd
from typing import Any


class CSVRepository:
    def read(self, path: str, **kwargs) -> pd.DataFrame:
        return pd.read_csv(path, **kwargs)

    def save(self, df, path: str, **kwargs) -> None:
        df.to_csv(path, **kwargs)