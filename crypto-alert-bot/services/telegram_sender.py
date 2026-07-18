"""
Telegram Bot sender service.
Handles all Telegram message sending operations.
"""

import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from telegram import Bot, InlineKeyboardMarkup
from telegram.error import TelegramError

from utils.logger import setup_logger

logger = setup_logger(__name__)

# Telegram API message length limit
MAX_MESSAGE_LENGTH = 4096


class TelegramSender:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot: Bot | None = None

    async def initialize(self) -> None:
        """Initialize the bot asynchronously."""
        if self.bot is None:
            self.bot = Bot(self.bot_token)

    async def close(self) -> None:
        """Properly close the bot connection."""
        if self.bot:
            try:
                await self.bot.close() # type: ignore
            except TelegramError as e:
                logger.warning("Error closing Telegram bot: %s", e)
            finally:
                self.bot = None

    def _split_message(self, text: str) -> list[str]:
        """Split a long message into chunks that fit Telegram's 4096 limit."""
        if len(text) <= MAX_MESSAGE_LENGTH:
            return [text]

        lines = text.split("\n")
        chunks = []
        current_chunk = ""

        for line in lines:
            # If a single line is longer than limit, split the line itself
            if len(line) > MAX_MESSAGE_LENGTH:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                    current_chunk = ""

                # Split long line into smaller pieces
                for i in range(0, len(line), MAX_MESSAGE_LENGTH):
                    chunks.append(line[i : i + MAX_MESSAGE_LENGTH])
            elif len(current_chunk) + len(line) + 1 <= MAX_MESSAGE_LENGTH:
                current_chunk += line + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = line + "\n"

        if current_chunk:
            chunks.append(current_chunk.rstrip())

        return chunks if chunks else [text]

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> bool:
        """Send a message to a Telegram chat/channel."""
        try:
            if self.bot is None:
                await self.initialize()

            chunks = self._split_message(text)

            for i, chunk in enumerate(chunks, 1):
                if len(chunks) > 1:
                    chunk = f"{chunk}\n\n[Part {i}/{len(chunks)}]"

                # Ensure bot is initialized and not None
                if self.bot is None:
                    await self.initialize()
                if self.bot is None:
                    logger.error("Telegram bot is not initialized")
                    return False

                # Assert for the type checker that self.bot is not None
                assert self.bot is not None
                bot = self.bot
                await bot.send_message(
                    chat_id=chat_id,
                    text=chunk,
                    parse_mode="HTML",
                    reply_markup=reply_markup if i == 1 else None,
                ) # type: ignore
                logger.info(
                    "Message part %d/%d sent to channel %s",
                    i,
                    len(chunks),
                    chat_id,
                )

                # Small delay between parts to avoid rate limiting
                if i < len(chunks):
                    await asyncio.sleep(0.5)

            return True
        except TelegramError as error:
            logger.error("Failed to send message: %s", error)
            return False
        except Exception as error:
            logger.error("Unexpected error sending message: %s", error)
            return False

    async def send_message_with_retry(
        self,
        chat_id: str,
        text: str,
        reply_markup: InlineKeyboardMarkup | None = None,
        max_retries: int = 3,
    ) -> bool:
        """Send a message with automatic retry on failure."""
        for attempt in range(1, max_retries + 1):
            try:
                if await self.send_message(chat_id, text, reply_markup=reply_markup):
                    return True
            except Exception as error:
                logger.error("Attempt %d failed: %s", attempt, error)

            if attempt < max_retries:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        logger.error("Failed to send message after %d attempts", max_retries)
        return False
