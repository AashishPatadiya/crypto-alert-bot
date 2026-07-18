"""
Constants used throughout the bot.
"""

# Cryptocurrencies to track
TRACKED_SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
}

# CoinGecko IDs for trending/gainers/losers
COINGECKO_IDS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "ripple": "XRP",
}

# API endpoints
BINANCE_24H_URL = "https://api.binance.com/api/v3/ticker/24hr"
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
CRYPTOPANIC_API_BASE = "https://cryptopanic.com/api/v1"
FEAR_GREED_API = "https://api.alternative.me/fng/"

# Message formatting
MESSAGE_DIVIDER = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
CHANNEL_MENTION = "@ULTIMATEFOREXFRONTIERS"

# Scheduler intervals (in minutes)
PRICE_UPDATE_INTERVAL = 5
NEWS_UPDATE_INTERVAL = 10
SUMMARY_UPDATE_INTERVAL = 360  # 6 hours

# Scheduler times (in HH:MM format)
FEARGREED_SCHEDULE_TIME = "08:00"

# Error messages
ERROR_CONFIG = "Configuration error: {}"
ERROR_API = "API error for {}: {}"
ERROR_TELEGRAM = "Telegram error: {}"
