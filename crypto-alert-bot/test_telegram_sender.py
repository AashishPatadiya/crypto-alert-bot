import asyncio
from services.telegram_sender import TelegramSender

async def t():
    ts = TelegramSender('TEST_TOKEN')
    await ts.initialize()
    print('initialized:', ts.bot is not None)
    chunks = ts._split_message('x'*5000)
    print('chunks:', len(chunks), 'len0:', len(chunks[0]))
    await ts.close()
    print('closed:', ts.bot is None)

asyncio.run(t())
