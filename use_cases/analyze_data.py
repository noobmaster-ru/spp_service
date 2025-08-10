# сценарий: анализ и выгрузка в CSV
from repositories.csv_repository import CSVRepository
from services.data_analyzer import DataAnalyzerService
from repositories.json_repository import JsonRepository
from core.constants import MERGED_RESULTS_PATH


class AnalyzeDataUseCase:
    def __init__(self):
        self.json_repo = JsonRepository()
        self.csv_repo = CSVRepository()
        self.analyzer = DataAnalyzerService(self.csv_repo)

    def execute(self):
        merged = self.json_repo.load(MERGED_RESULTS_PATH)
        self.analyzer.analyze_and_save(merged)