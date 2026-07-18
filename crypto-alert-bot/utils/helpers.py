"""
Helper functions used across the bot.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_request_session(retries: int = 3) -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def format_percentage(value: float, decimals: int = 2) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def format_currency(value: float, decimals: int = 2) -> str:
    return f"${value:,.{decimals}f}"


def format_large_number(value: float) -> str:
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"${value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"${value / 1e3:.2f}K"
    return f"${value:.2f}"


def truncate_text(text: str, max_length: int = 200) -> str:
    return text[:max_length] + "..." if len(text) > max_length else text
