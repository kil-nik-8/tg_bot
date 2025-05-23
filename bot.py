import asyncio
import logging

from aiogram.types import BotCommand

from core import dp, bot
from handlers import handlers

async def main() -> None:

    dp.include_router(handlers.router)
    logging.basicConfig(level=logging.INFO)
    
    await bot.delete_webhook(drop_pending_updates=False)

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
