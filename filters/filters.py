from aiogram.filters import BaseFilter
from core.config import config

class IsAllowedUser(BaseFilter):
    async def __call__(self, message) -> bool:
        return message.from_user.id in config.allowed_users

class IsNotAllowedUser(BaseFilter):
    async def __call__(self, message) -> bool:
        return not (message.from_user.id in config.allowed_users)