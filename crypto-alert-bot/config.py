"""
Configuration loader for Crypto Alert Bot v2.

This module loads environment variables (with optional .env support),
validates required settings, and exposes a typed `Config` dataclass
and a `load_config()` factory to be used by the application.

Never hardcode secrets or environment-specific values in code.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    """Typed configuration for the bot.

    Attributes
    - bot_token: Telegram bot token (from BotFather).
    - channel_id: Telegram channel or chat id to post messages to.
    - cryptopanic_key: API key for CryptoPanic (optional but recommended).
    - price_interval_minutes: Interval in minutes for price updates.
    - news_interval_minutes: Interval in minutes for news updates.
    - summary_interval_hours: Interval in hours for daily summary posts.
    - feargreed_schedule: Daily schedule time (HH:MM, UTC) for Fear & Greed.
    - log_level: Logging level name (e.g. INFO, DEBUG).
    - coinmarketcap_url: External link for CoinMarketCap.
    - coingecko_url: External link for CoinGecko.
    - version: Application version string.
    """

    bot_token: str
    channel_id: int | str
    cryptopanic_key: Optional[str]
    price_interval_minutes: int
    news_interval_minutes: int
    summary_interval_hours: int
    feargreed_schedule: str
    log_level: str
    coinmarketcap_url: str
    coingecko_url: str
    version: str


def _get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return environment variable or default (None if not set).

    This thin wrapper centralizes future changes like trimming or
    decoding secrets.
    """

    val = os.getenv(name)
    if val is not None:
        return val.strip()
    return default


def _get_required(name: str) -> str:
    """Return required environment variable or raise ValueError."""

    val = _get_env(name)
    if not val:
        raise ValueError(f"Missing required environment variable: {name}")
    return val


def _to_int(value: Optional[str], default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def load_config() -> Config:
    """Load and validate configuration from environment and return `Config`.

    This function also supports a local `.env` file when present.
    """

    # Load .env if present (no harm if not found)
    load_dotenv()

    bot_token = _get_required("BOT_TOKEN")

    # CHANNEL_ID may be numeric (int) or a string like '@channelname'
    channel = _get_required("CHANNEL_ID")
    try:
        channel_id = int(channel)
    except ValueError:
        # keep non-numeric channel identifiers (e.g. @my_channel)
        # our callers support both int and str for Telegram channel ids
        channel_id = channel

    cryptopanic_key = _get_env("CRYPTOPANIC_KEY")

    price_interval_minutes = _to_int(_get_env("PRICE_INTERVAL_MINUTES"), 5)
    news_interval_minutes = _to_int(_get_env("NEWS_INTERVAL_MINUTES"), 10)
    summary_interval_hours = _to_int(_get_env("SUMMARY_INTERVAL_HOURS"), 6)

    feargreed_schedule = _get_env("FEARGREED_SCHEDULE", "08:00") or "08:00"

    log_level = _get_env("LOG_LEVEL", "INFO") or "INFO"

    coinmarketcap_url = _get_env(
        "COINMARKETCAP_URL", "https://coinmarketcap.com"
    ) or "https://coinmarketcap.com"
    coingecko_url = _get_env("COINGECKO_URL", "https://www.coingecko.com") or (
        "https://www.coingecko.com"
    )

    version = _get_env("APP_VERSION", "2.0.0") or "2.0.0"

    return Config(
        bot_token=bot_token,
        channel_id=channel_id,
        cryptopanic_key=cryptopanic_key,
        price_interval_minutes=price_interval_minutes,
        news_interval_minutes=news_interval_minutes,
        summary_interval_hours=summary_interval_hours,
        feargreed_schedule=feargreed_schedule,
        log_level=log_level,
        coinmarketcap_url=coinmarketcap_url,
        coingecko_url=coingecko_url,
        version=version,
    )


__all__ = ["Config", "load_config"]
