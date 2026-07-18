"""
CoinGecko API service for fetching trending coins, gainers, and losers.
"""

from typing import Any

import requests

from utils.logger import setup_logger

logger = setup_logger(__name__)

COINGECKO_API = "https://api.coingecko.com/api/v3"


def fetch_trending_coins(session: requests.Session) -> list[dict[str, Any]]:
    """Fetch top 10 trending coins from CoinGecko."""
    try:
        url = f"{COINGECKO_API}/search/trending"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        trending = []
        for coin in data.get("coins", [])[:10]:
            coin_data = coin.get("item", {})
            trending.append(
                {
                    "name": coin_data.get("name", "Unknown"),
                    "symbol": coin_data.get("symbol", "").upper(),
                    "market_cap_rank": coin_data.get("market_cap_rank", "N/A"),
                }
            )
        logger.info("Fetched %d trending coins", len(trending))
        return trending
    except Exception as error:
        logger.error("Failed to fetch trending coins: %s", error)
        return []


def fetch_market_data(session: requests.Session) -> dict[str, Any]:
    """Fetch market data including top gainers and losers."""
    try:
        url = f"{COINGECKO_API}/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False,
        }
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        gainers = sorted(
            data,
            key=lambda x: x.get("price_change_percentage_24h", -999),
            reverse=True,
        )[:3]
        losers = sorted(
            data,
            key=lambda x: x.get("price_change_percentage_24h", 999),
        )[:3]

        return {
            "gainers": gainers,
            "losers": losers,
        }
    except Exception as error:
        logger.error("Failed to fetch market data: %s", error)
        return {"gainers": [], "losers": []}


def format_trending_message(coins: list[dict[str, Any]]) -> str:
    """Format trending coins into a message."""
    if not coins:
        return "❌ Could not fetch trending coins at this time."

    lines = ["🔥 TOP 10 TRENDING COINS\n"]
    for i, coin in enumerate(coins, 1):
        lines.append(
            f"{i}. {coin['name']} ({coin['symbol']}) "
            f"| Rank: #{coin['market_cap_rank']}"
        )

    return "\n".join(lines)


def format_gainers_losers_message(market_data: dict[str, Any]) -> str:
    """Format gainers and losers into a message."""
    gainers = market_data.get("gainers", [])
    losers = market_data.get("losers", [])

    lines = ["📈 TOP GAINERS & LOSERS\n"]
    lines.append("🟢 TOP GAINERS:\n")

    if gainers:
        for coin in gainers:
            change = coin.get("price_change_percentage_24h", 0)
            lines.append(f"• {coin['name']} (+{change:.2f}%)")
    else:
        lines.append("• No data available")

    lines.append("\n🔴 TOP LOSERS:\n")

    if losers:
        for coin in losers:
            change = coin.get("price_change_percentage_24h", 0)
            lines.append(f"• {coin['name']} ({change:.2f}%)")
    else:
        lines.append("• No data available")

    return "\n".join(lines)
