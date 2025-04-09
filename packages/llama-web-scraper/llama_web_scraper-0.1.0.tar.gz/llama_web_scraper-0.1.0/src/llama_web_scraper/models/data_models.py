from typing import List

from pydantic import BaseModel


class PageContent(BaseModel):
    url: str
    content: str
    links: List[str]


class PageAnalysis(BaseModel):
    url: str
    summary: str
    sentiment: str
    keywords: List[str]
    topics: List[str]
