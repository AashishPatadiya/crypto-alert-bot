"""
CryptoPanic API service for fetching crypto news.
"""

from typing import Any

import requests

from utils.logger import setup_logger

logger = setup_logger(__name__)

CRYPTOPANIC_API = "https://cryptopanic.com/api/v1"


def fetch_crypto_news(
    session: requests.Session, api_key: str | None = None
) -> list[dict[str, Any]]:
    """Fetch the latest crypto news from CryptoPanic."""
    try:
        url = f"{CRYPTOPANIC_API}/posts/"
        params = {
            "kind": "news",
            "limit": 5,
            "public": "true",
        }
        if api_key:
            params["auth_token"] = api_key

        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        news_articles = []
        for post in data.get("results", []):
            news_articles.append(
                {
                    "title": post.get("title", ""),
                    "url": post.get("url", ""),
                    "source": post.get("source", {}).get("title", "Unknown"),
                    "published_at": post.get("published_at", ""),
                }
            )
        logger.info("Fetched %d news articles", len(news_articles))
        return news_articles
    except Exception as error:
        logger.error("Failed to fetch crypto news: %s", error)
        return []


def format_news_message(articles: list[dict[str, Any]]) -> str:
    """Format crypto news into a message."""
    if not articles:
        return "❌ Could not fetch crypto news at this time."

    lines = ["📰 LATEST CRYPTO NEWS\n"]

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        source = article.get("source", "Unknown")
        lines.append(f"\n{i}. {title}")
        lines.append(f"   Source: {source}")

    lines.append("\n\n📎 Read more on CryptoPanic")
    return "\n".join(lines)
