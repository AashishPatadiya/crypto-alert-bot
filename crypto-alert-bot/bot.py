"""
Ultimate Forex Frontiers Crypto Alert Bot
Main entry point for the bot with scheduled tasks.
"""

import asyncio
import signal
import sys
from typing import Any

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import load_config
from scheduler import BotScheduler
from services.coingecko import (
    fetch_market_data,
    fetch_trending_coins,
    format_gainers_losers_message,
    format_trending_message,
)
from services.cryptopanic import fetch_crypto_news, format_news_message
from services.fear_greed import fetch_fear_greed_index, format_fear_greed_message
from services.formatter import (
    build_footer,
    format_daily_summary_message,
    format_price_update_message,
)
from services.telegram_sender import TelegramSender
from utils.helpers import create_request_session
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Global service instances
telegram_sender: TelegramSender | None = None
session: requests.Session | None = None
scheduler: BotScheduler | None = None
config: Any = None


async def fetch_crypto_prices() -> dict[str, dict[str, Any]]:
    """Fetch current prices for tracked cryptocurrencies."""
    if not session:
        return {}

    prices = {}
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]

    for symbol in symbols:
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr"
            response = session.get(url, params={"symbol": symbol}, timeout=10)
            response.raise_for_status()
            data = response.json()

            symbol_key = symbol.replace("USDT", "")
            prices[symbol_key] = {
                "price": float(data.get("lastPrice", 0)),
                "high_price": float(data.get("highPrice", 0)),
                "low_price": float(data.get("lowPrice", 0)),
                "price_change_percent": float(data.get("priceChangePercent", 0)),
                "volume": float(data.get("volume", 0)),
            }
        except Exception as error:
            logger.error("Failed to fetch price for %s: %s", symbol, error)

    return prices


async def post_price_update() -> None:
    """Job: Post price update every 5 minutes."""
    try:
        logger.info("Executing: price update")
        prices = await fetch_crypto_prices()

        if prices and telegram_sender:
            message = format_price_update_message(prices) + build_footer()
            await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in price update job: %s", error)


async def post_trending_coins() -> None:
    """Job: Post top 10 trending coins."""
    try:
        logger.info("Executing: trending coins")
        if not session or not telegram_sender:
            return

        trending = fetch_trending_coins(session)
        message = format_trending_message(trending) + build_footer()
        await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in trending coins job: %s", error)


async def post_gainers_losers() -> None:
    """Job: Post top gainers and losers."""
    try:
        logger.info("Executing: gainers and losers")
        if not session or not telegram_sender:
            return

        market_data = fetch_market_data(session)
        message = format_gainers_losers_message(market_data) + build_footer()
        await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in gainers/losers job: %s", error)


async def post_crypto_news() -> None:
    """Job: Post latest crypto news."""
    try:
        logger.info("Executing: crypto news")
        if not session or not telegram_sender:
            return

        news = fetch_crypto_news(session, config.cryptopanic_key)
        message = format_news_message(news) + build_footer()
        await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in news job: %s", error)


async def post_fear_greed() -> None:
    """Job: Post Fear & Greed Index."""
    try:
        logger.info("Executing: fear & greed index")
        if not session or not telegram_sender:
            return

        index = fetch_fear_greed_index(session)
        message = format_fear_greed_message(index) + build_footer()
        await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in fear & greed job: %s", error)


async def post_daily_summary() -> None:
    """Job: Post daily market summary."""
    try:
        logger.info("Executing: daily summary")
        prices = await fetch_crypto_prices()

        if prices and telegram_sender:
            message = format_daily_summary_message(prices) + build_footer()
            await telegram_sender.send_message(config.channel_id, message)
    except Exception as error:
        logger.error("Error in daily summary job: %s", error)


def wrap_async_job(coro_func):
    """Wrap async coroutine function for APScheduler."""
    def wrapper():
        try:
            asyncio.run(coro_func())
        except Exception as error:
            logger.error("Job execution error: %s", error)
    return wrapper


def setup_scheduler() -> None:
    """Configure all scheduled jobs."""
    global scheduler

    if not scheduler:
        logger.error("Scheduler not initialized")
        return

    # Price updates every 5 minutes
    scheduler.schedule_interval_job(
        wrap_async_job(post_price_update),
        minutes=config.price_interval_minutes,
        job_id="price_update",
    )

    # Trending coins every 10 minutes
    scheduler.schedule_interval_job(
        wrap_async_job(post_trending_coins),
        minutes=config.news_interval_minutes,
        job_id="trending_coins",
    )

    # Gainers/Losers every 15 minutes
    scheduler.schedule_interval_job(
        wrap_async_job(post_gainers_losers),
        minutes=15,
        job_id="gainers_losers",
    )

    # Crypto news every 20 minutes
    scheduler.schedule_interval_job(
        wrap_async_job(post_crypto_news),
        minutes=config.news_interval_minutes * 2,
        job_id="crypto_news",
    )

    # Daily summary every 6 hours
    scheduler.schedule_interval_job(
        wrap_async_job(post_daily_summary),
        minutes=config.summary_interval_hours * 60,
        job_id="daily_summary",
    )

    # Fear & Greed at scheduled time daily
    hour, minute = map(int, config.feargreed_schedule.split(":"))
    scheduler.schedule_cron_job(
        wrap_async_job(post_fear_greed),
        hour=hour,
        minute=minute,
        job_id="fear_greed",
    )

    scheduler.start()
    logger.info("All scheduled jobs configured and started")


def signal_handler(sig, frame) -> None:
    """Handle shutdown signal gracefully."""
    logger.info("Shutdown signal received")
    if scheduler:
        scheduler.stop()
    sys.exit(0)


async def main() -> None:
    """Initialize and start the bot."""
    global telegram_sender, session, scheduler, config

    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except ValueError as error:
        logger.error("Configuration error: %s", error)
        print(f"Configuration error: {error}")
        return

    # Initialize services
    session = create_request_session()
    telegram_sender = TelegramSender(config.bot_token)
    scheduler = BotScheduler()
    
    # Initialize telegram sender
    await telegram_sender.initialize()

    # Send startup message
    startup_message = (
        "🚀 Ultimate Forex Frontiers Crypto Alert Bot\n\n"
        "✅ Bot started successfully!\n\n"
        "📊 Scheduled tasks:\n"
        "• Price updates every 5 minutes\n"
        "• Trending coins every 10 minutes\n"
        "• Gainers/Losers every 15 minutes\n"
        "• Crypto news every 20 minutes\n"
        "• Daily summary every 6 hours\n"
        "• Fear & Greed Index at 08:00 UTC\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📢 Join: @ULTIMATEFOREXFRONTIERS"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url="https://t.me/ULTIMATEFOREXFRONTIERS",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await telegram_sender.send_message(
        config.channel_id,
        startup_message,
        reply_markup=reply_markup,
    )

    # Setup and start scheduler
    setup_scheduler()

    # Handle shutdown gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Bot running successfully")

    # Keep the bot running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        if scheduler:
            scheduler.stop()

    finally:
        # Cleanup
        if scheduler:
            scheduler.stop()
        if telegram_sender:
            await telegram_sender.close()
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())




