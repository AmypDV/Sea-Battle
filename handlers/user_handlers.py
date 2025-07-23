import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command

import logging

from pyexpat.errors import messages

from lexicon.lexicon_ru import LEXICON
from datebase.datebase import write_to_bd, UserBD
from keyboards.inline_kb import (create_user_kb, create_comp_kb,
                                 UsersCallbackFactory, CompsCallbackFactory, _TEMP)
from services.services import GamePole
from filters.filters import IsDigitCallbackData, IsBookmarksCallbackData, IsDelBookmarkCallbackData

user_router = Router()

logger = logging.getLogger(__name__)

@user_router.message(CommandStart())
async def get_start_command(message: Message, _user_bd):

    logger.debug('Начало хэндлера %s', __name__)

    user_id = message.from_user.id
    if user_id not in _user_bd:
        _user_bd[user_id] = UserBD()
        write_to_bd()
    await message.answer(text=LEXICON['/start'])


@user_router.message(Command(commands=['beginning']))
async def get_begin_command(message: Message, _user_bd: list[UserBD], user_id:int):

    logger.debug('Начало хэндлера %s', __name__)

    _user_bd[user_id].in_game = True
    _user_bd[user_id].games += 1
    user_pole = GamePole()
    user_pole.init()
    _user_bd[user_id].user_pole = user_pole
    _comp_pole = GamePole()
    _comp_pole.init()
    _comp_pole.show()
    _user_bd[user_id].chat = []

    _user_bd[user_id].comp_pole = _comp_pole
    await message.answer(text=f'{LEXICON["/beginning"]: ^40}',
                             reply_markup=create_user_kb(user_pole.get_pole(), 'random', 'start_game'))
    logger.debug('Завершение хэндлера %s', __name__)




@user_router.callback_query(F.data == 'random')
async def get_callback_random(callback: CallbackQuery, _user_bd: list[UserBD], user_id:int):
    logger.debug('Начало хэндлера %s', __name__)

    user_pole = GamePole()
    user_pole.init()
    _user_bd[user_id].comp_pole = user_pole
    await callback.message.edit_text(
        text=f"{LEXICON['inline_random']: ^40}",
        reply_markup=create_user_kb(user_pole.get_pole(), 'random', 'start_game')
    )

@user_router.callback_query(F.data.in_(['start_game', 'pole_comp']))
async def get_callback_random(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    pole = _user_bd[user_id].comp_pole
    await callback.message.edit_text(
        text=f"{LEXICON['your_step']: ^40}",
        reply_markup=create_comp_kb(pole.get_pole(), 'pole_user')
    )


@user_router.callback_query(F.data == 'pole_user')
async def get_callback_random(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    pole = _user_bd[user_id].user_pole
    await callback.message.edit_text(
        text=f"{LEXICON['your_flot']: ^40}",
        reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
    )

@user_router.callback_query(CompsCallbackFactory.filter())
async def get_callback_random(callback: CallbackQuery,
                              callback_data: CompsCallbackFactory,
                              _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    x = callback_data.x
    y = callback_data.y

    res = _user_bd[user_id].comp_pole.hit(y, x)
    pole = _user_bd[user_id].comp_pole
    if res == 'already_fight':
        try:
            await callback.message.edit_text(
                text=LEXICON['already_fight'],
                reply_markup=callback.message.reply_markup
            )
            await callback.answer(
                text=LEXICON['already_fight']
            )
        except Exception:
            await callback.answer()
    elif res == 'hit':
        await callback.message.edit_text(
            text=LEXICON['hit'].format(_TEMP[y + 1] + str(x + 1)),
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
        await callback.answer(
            text=LEXICON['hit'].format(_TEMP[y + 1] + str(x + 1))
        )
    elif res == 'sunk':
        await callback.message.edit_text(
            text=LEXICON['sunk'].format(_TEMP[y + 1] + str(x + 1)),
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
        await callback.answer(
            text=LEXICON['sunk'].format(_TEMP[y + 1] + str(x + 1)),
        )
    elif res == 'miss':
        await callback.message.edit_text(
            text=f"{LEXICON['miss']: ^40}",
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
        await asyncio.sleep(1)
        await comp_atack(callback=callback, _user_bd=_user_bd, user_id=user_id)

    elif res == 'victory':
        await callback.message.edit_text(
            text=f"{LEXICON['victory']: ^40}"
        )


@user_router.callback_query(UsersCallbackFactory.filter())
async def get_callback_random(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    try:
        await callback.message.edit_text(
            text=LEXICON['already_flot'],
            reply_markup=callback.message.reply_markup
        )
    except Exception:
        await callback.answer()

async def comp_atack(callback: CallbackQuery,
                     _user_bd: list[UserBD], user_id: int):
    messages= [callback.message.message_id]
    pole = _user_bd[user_id].user_pole
    await callback.message.edit_text(
        text=f"{LEXICON['miss']: ^40}",
        reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
    )
    await asyncio.sleep(1)
    pole = _user_bd[user_id].user_pole
    await callback.message.edit_text(
        text=f"{LEXICON['hit_comp']: ^40}",
        reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
    )
    await asyncio.sleep(1)
    y, x, res = _user_bd[user_id].user_pole.random_hit()

    while res in ('sunk', 'hit', 'already_fight'):
        while res == 'already_fight':
            y, x, res = _user_bd[user_id].user_pole.random_hit()
        await asyncio.sleep(1)
        pole = _user_bd[user_id].user_pole
        await callback.message.edit_text(
            text=LEXICON['luck_com_attak'].format(_TEMP[y + 1] + str(x + 1)),
            reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
        )
        await asyncio.sleep(1)
        res = _user_bd[user_id].user_pole.random_hit()
    if res == 'victory':
        await callback.message.edit_text(
            text=f"{LEXICON['lose']: ^40}"
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['miss_comp'].format(_TEMP[y + 1] + str(x + 1)),
            reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
        )
    callback.message.answer()