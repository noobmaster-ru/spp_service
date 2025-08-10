# сценарий: получить данные, рассчитать цены, сохранить
import asyncio
from typing import List
import aiohttp
import os
from repositories.json_repository import JsonRepository
from services.wb_api_client import WBApiClient
from services.wb_site_parser import WBSiteParser
from core.constants import RESULTS_DIR


class ParseAndSaveUseCase:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.json_repo = JsonRepository()
        os.makedirs(RESULTS_DIR, exist_ok=True)

    async def _process_token(self, session: aiohttp.ClientSession, token: str, index: int):
        api_client = WBApiClient(session)
        site_parser = WBSiteParser(session)
        start = asyncio.get_event_loop().time()
        try:
            parsed_data_api_articles = await api_client.fetch_articles(token)
            # create tasks to fetch prices concurrently (limit concurrency if needed)
            tasks = []
            for nm in parsed_data_api_articles.keys():
                tasks.append(site_parser.fetch_price_data(nm))

            # gather prices in batches to avoid heavy memory
            prices_results = await asyncio.gather(*tasks)

            # merge data
            for nm, price_data in zip(parsed_data_api_articles.keys(), prices_results):
                parsed_data_api_articles[nm].update(price_data)

            # save to file per cabinet
            out_path = f"{RESULTS_DIR}/cabinet_data_{index}.json"
            self.json_repo.save(parsed_data_api_articles, out_path)
            duration = asyncio.get_event_loop().time() - start
            print(f"✅ cabinet_{index}: {duration:.2f}s , saved {len(parsed_data_api_articles)} items to {out_path}")
        except Exception as e:
            print("❌ Exception in _process_token:", e)

    async def execute(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self._process_token(session, token, i) for i, token in enumerate(self.tokens)]
            await asyncio.gather(*tasks)