from typing import Any, Dict
from collections.abc import Callable, Awaitable
from pprint import pprint

import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from datebase.datebase import UserBD, write_to_bd


logger = logging.getLogger(__name__)

class MainMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        user_id = data.get('event_from_user').id
        user_bd = data.get('_user_bd')
        if user_id not in user_bd:
            user_bd[user_id] = UserBD
            write_to_bd()

        data['user_id'] = user_id
        result = await handler(event, data)


        return result