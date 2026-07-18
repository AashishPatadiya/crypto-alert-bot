"""
Message formatter for creating beautiful Telegram messages.
"""

from datetime import datetime, timezone
from typing import Any

from utils.helpers import format_currency, format_percentage


def format_price_update_message(currencies: dict[str, dict[str, Any]]) -> str:
    """Format price update message for BTC, ETH, SOL, XRP."""
    lines = ["💰 CRYPTO PRICE UPDATE\n"]

    for symbol, data in currencies.items():
        price = data.get("price", 0)
        change_24h = data.get("price_change_percent", 0)
        high_24h = data.get("high_price", 0)
        low_24h = data.get("low_price", 0)
        volume = data.get("volume", 0)

        change_emoji = "📈" if change_24h >= 0 else "📉"

        lines.append(f"\n🔹 {symbol} | {format_currency(price)}")
        lines.append(f"   {change_emoji} 24H: {format_percentage(change_24h)}")
        lines.append(f"   📊 Range: {format_currency(low_24h)} - {format_currency(high_24h)}")
        lines.append(f"   📦 Vol: {volume:,.0f}")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"\n🕒 Updated: {timestamp}")

    return "\n".join(lines)


def format_daily_summary_message(currencies: dict[str, dict[str, Any]]) -> str:
    """Format a comprehensive daily market summary."""
    lines = ["📊 DAILY MARKET SUMMARY\n"]

    for symbol, data in currencies.items():
        price = data.get("price", 0)
        change_24h = data.get("price_change_percent", 0)
        change_emoji = "📈" if change_24h >= 0 else "📉"

        lines.append(f"{symbol}: {format_currency(price)} {change_emoji} {format_percentage(change_24h)}")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"\n🕒 {timestamp}")

    return "\n".join(lines)


def build_footer() -> str:
    """Build message footer with channel mention."""
    return "\n" + "━" * 40 + f"\n📢 Join: @ULTIMATEFOREXFRONTIERS"


def wrap_in_code_block(text: str, language: str = "") -> str:
    """Wrap text in Telegram code block."""
    return f"```{language}\n{text}\n```"
