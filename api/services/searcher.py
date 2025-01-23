from fastapi import HTTPException
from duckduckgo_search import DDGS 
import httpx
import random
from loguru import logger
import asyncio
from bs4 import BeautifulSoup as BS
from typing import Optional, List

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
]

class Searcher:
    async def get_page_text(self, url: str) -> str:
        """
        Получение контента страницы
        """
        # TODO: добавить обобщение или сокращение контента
        try:
            headers = {}
            headers['User-Agent'] = random.choice(user_agents)
            headers['Accept-Language'] = "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                if response.status_code != 200:
                    raise ValueError(f"HTTP: {response.status_code}")
                # Очистка текста от тегов
                soup = BS(response.text, 'html.parser')
                return soup.get_text()
        except Exception as e:
            logger.warning(f"Failed to get `{url}` content: {e}")
            return ""

    async def search(
        self,
        request: str,
        region: Optional[str] = "ru-ru",
        max_results: Optional[int] = 3
    ) -> Optional[List[str]]:
       
        try:
            sites = DDGS().text(request, region=region, max_results=max_results)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get search results: {e}"
            )

        if len(sites) == 0:
            return []
        
        # Создание задач
        tasks = []
        for site in sites:
            tasks.append(self.get_page_text(site['href']))
        # Получение страниц
        results = await asyncio.gather(*tasks)

        result = [result for result in results if result != ""]
        logger.debug(f"Got info from `{len(result)}` of `{len(sites)}` sites")

        return result
