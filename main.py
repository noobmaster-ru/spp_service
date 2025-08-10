import asyncio
import pandas as pd
from use_cases.parse_and_save import ParseAndSaveUseCase
from use_cases.merge_data import MergeDataUseCase
from use_cases.analyze_data import AnalyzeDataUseCase
from use_cases.find_spp_by_nm_id import find_spp_by_nm_id
from core.constants import WB_TOKENS_CSV
import argparse


def load_tokens_from_csv(path: str):
    df = pd.read_csv(path)
    # берем все значения второго столбца
    return df.iloc[:, 1].tolist()


async def run_parse(tokens):
    usecase = ParseAndSaveUseCase(tokens)
    await usecase.execute()


def run_merge():
    MergeDataUseCase().execute()


def run_analyze():
    AnalyzeDataUseCase().execute()


def run_find_spp():
    try:
        nm_id = int(input("Введите nm_id: ").strip())
    except ValueError:
        print("Ошибка: nm_id должен быть числом.")
        return
    find_spp_by_nm_id(nm_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["parse", "merge", "analyze", "find-spp"])
    args = parser.parse_args()

    if args.command == "parse":
        tokens = load_tokens_from_csv(WB_TOKENS_CSV)
        asyncio.run(run_parse(tokens))
    elif args.command == "merge":
        run_merge()
    elif args.command == "analyze":
        run_analyze()
    elif args.command == "find-spp":
        run_find_spp()


if __name__ == "__main__":
    main()
