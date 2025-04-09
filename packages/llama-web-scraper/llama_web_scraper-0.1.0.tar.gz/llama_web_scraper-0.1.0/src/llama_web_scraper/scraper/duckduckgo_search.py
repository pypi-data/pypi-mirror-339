from typing import List

from duckduckgo_search import ddg


def search_urls(query: str, max_results: int = 10) -> List[str]:
    results = ddg(query, max_results=max_results)
    urls = [result["href"] for result in results]
    return urls
