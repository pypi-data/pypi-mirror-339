from typing import List

import openai
from config import settings
from models.data_models import PageAnalysis
from utils.nlp_utils import extract_keywords

openai.api_key = settings.openai_api_key


async def process_content_with_llm(url: str, content: str) -> PageAnalysis:
    summary = await summarize_content(content)
    sentiment = await analyze_sentiment(content)
    keywords = extract_keywords(content)
    topics = await topic_modeling(content)
    return PageAnalysis(
        url=url, summary=summary, sentiment=sentiment, keywords=keywords, topics=topics
    )


async def summarize_content(content: str, max_tokens: int = 150) -> str:
    response = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=f"Summarize the following content:\n\n{content}",
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


async def analyze_sentiment(content: str) -> str:
    response = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=f"Analyze the sentiment of the following content:\n\n{content}\n\nIs it Positive, Negative, or Neutral?",
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.0,
    )
    return response.choices[0].text.strip()


async def topic_modeling(content: str) -> List[str]:
    response = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=f"Extract the main topics from the following content:\n\n{content}\n\nProvide a comma-separated list of topics.",
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    topics = response.choices[0].text.strip()
    return [topic.strip() for topic in topics.split(",")]
