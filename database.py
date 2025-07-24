from environs import Env
import asyncpg

env = Env()
env.read_env()

DB_CONFIG = {
    "host": env.str("DB_HOST"),
    "port": env.int("DB_PORT"),
    "database": env.str("DB_NAME"),
    "user": env.str("DB_USER"),
    "password": env.str("DB_PASSWORD")
}

_pool: asyncpg.Pool = None

async def get_pool():
    """
    Создаёт и возвращает пул соединений с базой данных.
    Если пул уже создан, возвращает его повторно.
    """
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(**DB_CONFIG)
    return _pool

async def fetch_one(query, *args):
    """
    Выполняет SQL-запрос и возвращает одну строку результата.
    :param query: SQL-запрос
    :param args: параметры запроса
    :return: asyncpg.Record или None
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)

async def fetch_all(query, *args):
    """
    Выполняет SQL-запрос и возвращает все строки результата.
    :param query: SQL-запрос
    :param args: параметры запроса
    :return: список asyncpg.Record
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def execute(query, *args):
    """
    Выполняет SQL-запрос без возврата результата (например, INSERT, UPDATE, DELETE).
    :param query: SQL-запрос
    :param args: параметры запроса
    :return: строка с результатом выполнения
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)