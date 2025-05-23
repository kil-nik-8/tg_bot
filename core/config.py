from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from redis.asyncio import Redis

# === Конфигурации ===
@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    sheet_key: str
    server_url: str


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN")
        ),
        sheet_key=env("SHEET_KEY"),
        server_url=env("SERVER_URL"),
    )


config: Config = load_config(".env")

default = DefaultBotProperties(parse_mode="HTML")
bot: Bot = Bot(token=config.tg_bot.token, default=default)
SHEET_KEY: str = config.sheet_key
SERVER_URL: str = config.server_url

# redis = Redis(host="localhost")
# storage = RedisStorage(redis=redis)
dp: Dispatcher = Dispatcher(
    # storage=storage
    )
