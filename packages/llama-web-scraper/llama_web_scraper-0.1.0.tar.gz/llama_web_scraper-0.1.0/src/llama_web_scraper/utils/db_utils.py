import json

import sqlite_utils
from config import settings
from loguru import logger
from models.data_models import PageAnalysis, PageContent
from utils.schema_validator import validate_json

db = sqlite_utils.Database(settings.database_url.replace("sqlite:///", ""))


def init_db():
    if "pages" not in db.table_names():
        db["pages"].create(
            {
                "url": str,
                "content": str,
                "links": str,
            },
            pk="url",
        )
    if "analysis" not in db.table_names():
        db["analysis"].create(
            {
                "url": str,
                "summary": str,
                "sentiment": str,
                "keywords": str,
                "topics": str,
            },
            pk="url",
        )


def save_page_content(page: PageContent):
    schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "format": "uri"},
            "content": {"type": "string"},
            "links": {"type": "array", "items": {"type": "string", "format": "uri"}},
        },
        "required": ["url", "content"],
    }
    data = page.dict()
    if validate_json(data, schema):
        db["pages"].upsert(
            {"url": page.url, "content": page.content, "links": json.dumps(page.links)},
            pk="url",
        )
    else:
        logger.error(f"Validation failed for page: {page.url}")


def update_page_analysis(analysis: PageAnalysis):
    db["analysis"].upsert(
        {
            "url": analysis.url,
            "summary": analysis.summary,
            "sentiment": analysis.sentiment,
            "keywords": json.dumps(analysis.keywords),
            "topics": json.dumps(analysis.topics),
        },
        pk="url",
    )


def get_all_pages():
    return list(db["pages"].rows)
