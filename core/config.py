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
    allowed_users: list[int]


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    allowed_users = [int(uid) for uid in env.str("ALLOWED_USERS", "").split(",") if uid.strip()]

    mode = env.str("MODE", "prod").lower()
    if mode == "test":
        token = env("BOT_TOKEN_TEST")
    else:
        token = env("BOT_TOKEN_PROD")

    return Config(
        tg_bot=TgBot(
            token=token
        ),
        sheet_key=env("SHEET_KEY"),
        server_url=env("SERVER_URL"),
        allowed_users=allowed_users
    )


config: Config = load_config(".env")

default = DefaultBotProperties(parse_mode="HTML")
bot: Bot = Bot(token=config.tg_bot.token, default=default)
SHEET_KEY: str = config.sheet_key
SERVER_URL: str = config.server_url
allowed_users: list[int] = config.allowed_users

# redis = Redis(host="localhost")
# storage = RedisStorage(redis=redis)
dp: Dispatcher = Dispatcher(
    # storage=storage
    )
