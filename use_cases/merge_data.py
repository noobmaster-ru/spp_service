# сценарий: объединение файлов
from services.data_merger import DataMergerService
from repositories.json_repository import JsonRepository
from core.constants import MERGED_RESULTS_PATH, RESULTS_DIR


class MergeDataUseCase:
    def __init__(self, folder: str = RESULTS_DIR, out_path: str = MERGED_RESULTS_PATH):
        self.merger = DataMergerService(folder)
        self.json_repo = JsonRepository()
        self.out_path = out_path

    def execute(self):
        merged = self.merger.merge()
        self.json_repo.save(merged, self.out_path)
        print(f"✅ Объединено {len(merged)} записей в {self.out_path}")