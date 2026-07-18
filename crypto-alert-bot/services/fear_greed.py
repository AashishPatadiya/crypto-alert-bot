"""
Fear & Greed Index service.
Fetches the cryptocurrency fear and greed index.
"""

from typing import Any

import requests

from utils.logger import setup_logger

logger = setup_logger(__name__)

FEAR_GREED_API = "https://api.alternative.me/fng/"


def fetch_fear_greed_index(session: requests.Session) -> dict[str, Any] | None:
    """Fetch the current fear and greed index."""
    try:
        response = session.get(FEAR_GREED_API, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("data"):
            index_data = data["data"][0]
            return {
                "value": int(index_data.get("value", 0)),
                "classification": index_data.get("value_classification", "Unknown"),
                "timestamp": index_data.get("timestamp", ""),
            }
        return None
    except Exception as error:
        logger.error("Failed to fetch fear & greed index: %s", error)
        return None


def get_emotion_emoji(value: int) -> str:
    """Get emoji based on fear and greed index value."""
    if value <= 25:
        return "😱"
    elif value <= 50:
        return "😟"
    elif value <= 75:
        return "😐"
    else:
        return "🤑"


def format_fear_greed_message(index_data: dict[str, Any] | None) -> str:
    """Format fear and greed index into a message."""
    if not index_data:
        return "❌ Could not fetch Fear & Greed Index at this time."

    value = index_data.get("value", 0)
    classification = index_data.get("classification", "Unknown")
    emoji = get_emotion_emoji(value)

    return (
        f"{emoji} FEAR & GREED INDEX\n\n"
        f"📊 Value: {value}/100\n"
        f"📌 Classification: {classification}\n\n"
        f"0 = Extreme Fear | 50 = Neutral | 100 = Extreme Greed"
    )
