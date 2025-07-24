import asyncio
import logging

from aiogram.types import BotCommand

from core import dp, bot
from handlers import handlers

import os
import json

# Получаем переменную среды с текстом JSON и создаём файл
if os.path.exists("credentials.json"):
    with open("credentials.json", "r") as f:
        creds = json.load(f)
else:
    creds_text = os.environ.get("GOOGLE_CREDENTIALS")
    if creds_text:
        creds = json.loads(creds_text)
        with open("credentials.json", "w") as f:
            json.dump(creds, f)
            
async def main() -> None:

    dp.include_router(handlers.router)
    logging.basicConfig(level=logging.INFO)
    
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=[
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        )
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
