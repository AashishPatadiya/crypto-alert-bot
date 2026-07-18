"""
Ultimate Forex Frontiers Crypto Alert Bot
Entrypoint for starting the Telegram bot and scheduler.
"""

import asyncio

from bot import main


if __name__ == "__main__":
    asyncio.run(main())
