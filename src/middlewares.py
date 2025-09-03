from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ClientMiddleware(BaseMiddleware):
    def __init__(self, **clients):
        self.clients = clients

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        for key, client in self.clients.items():
            data[key] = client
        return await handler(event, data)
