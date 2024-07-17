from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command

import logging

from lexicon.lexicon_ru import LEXICON
from datebase.datebase import write_to_bd, UserBD
from keyboards.inline_kb import create_user_kb
from services.services import GamePole
from filters.filters import IsDigitCallbackData, IsBookmarksCallbackData, IsDelBookmarkCallbackData

user_router = Router()

logger = logging.getLogger(__name__)

@user_router.message(CommandStart())
async def get_start_command(message: Message):

    logger.debug('Начало хэндлера %s', __name__)
    await message.answer(text=LEXICON['/start'])


@user_router.message(Command(commands=['beginning']))
async def get_begin_command(message: Message, _user_bd: list[UserBD], user_id:int):

    logger.debug('Начало хэндлера %s', __name__)
    _user_bd[user_id].games += 1
    user_pole = GamePole()
    user_pole.init()
    _user_bd[user_id].comp_pole = user_pole
    await message.answer(text=f'{LEXICON["/beginning"]: ^40}',
                         reply_markup=create_user_kb(user_pole.get_pole()))
    logger.debug('Завершение хэндлера %s', __name__)


@user_router.callback_query(F.data == 'random')
async def get_callback_random(callback: CallbackQuery, _user_bd: list[UserBD], user_id:int):
    logger.debug('Начало хэндлера %s', __name__)

    user_pole = GamePole()
    user_pole.init()
    _user_bd[user_id].comp_pole = user_pole
    await callback.message.edit_text(
        text=LEXICON["inlain_random"].rjust(__width=40,),
        reply_markup=create_user_kb(user_pole.get_pole())
    )
