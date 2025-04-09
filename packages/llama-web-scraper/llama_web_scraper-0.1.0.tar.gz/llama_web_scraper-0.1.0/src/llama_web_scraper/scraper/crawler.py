import asyncio
from typing import Set

import aiohttp
from loguru import logger
from models.data_models import PageContent
from scraper.extractor import ScraperExtractor
from utils.db_utils import save_page_content


class Crawler:
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.visited: Set[str] = set()
        self.extractor = ScraperExtractor()

    async def crawl(self, start_url: str, max_depth: int = 2):
        await self.crawl_page(start_url, 0, max_depth)

    async def crawl_page(self, url: str, depth: int, max_depth: int):
        if depth > max_depth or url in self.visited:
            return
        self.visited.add(url)
        async with self.semaphore:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            page_content = self.extractor.extract_text_content(html)
                            links = self.extractor.extract_links(html, base_url=url)
                            save_page_content(
                                PageContent(url=url, content=page_content, links=links)
                            )
                            tasks = [self.crawl_page(link, depth + 1, max_depth) for link in links]
                            await asyncio.gather(*tasks)
                        else:
                            logger.warning(f"Failed to fetch {url} with status {response.status}")
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
