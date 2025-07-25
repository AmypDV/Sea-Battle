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

@user_router.callback_query(F.data =='start_game')
async def get_callback_start(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    pole = _user_bd[user_id].comp_pole
    await callback.message.edit_text(
        text=f"{LEXICON['your_step']: ^40}",
        reply_markup=create_comp_kb(pole.get_pole(), 'pole_user')
    )

@user_router.callback_query(F.data == 'pole_comp')
async def get_callback_polecomp(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    pole = _user_bd[user_id].comp_pole
    await callback.message.edit_text(
        text=await append_text(_user_bd, user_id, ''),
        reply_markup=create_comp_kb(pole.get_pole(), 'pole_user')
    )

@user_router.callback_query(F.data == 'pole_user')
async def get_callback_poleuser(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
    logger.debug('Начало хэндлера %s', __name__)

    pole = _user_bd[user_id].user_pole
    await callback.message.edit_text(
        text=await append_text(_user_bd, user_id, ''),
        reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
    )

@user_router.callback_query(CompsCallbackFactory.filter())
async def get_callback_compsbutton(callback: CallbackQuery,
                              callback_data: CompsCallbackFactory,
                              _user_bd: list[UserBD], user_id: int,
                              ):
    logger.debug('Начало хэндлера %s', __name__)

    x = callback_data.x
    y = callback_data.y

    res = _user_bd[user_id].comp_pole.hit(y, x)
    pole = _user_bd[user_id].comp_pole
    if res == 'already_fight':
        try:
            await callback.message.edit_text(
                text=await append_text(_user_bd, user_id, LEXICON['already_fight']),
                reply_markup=callback.message.reply_markup
            )
        except Exception:
            await callback.answer()
    elif res == 'hit':
        await callback.message.edit_text(
            text=await append_text(_user_bd, user_id, LEXICON['hit'].format(_TEMP[y + 1] + str(x + 1))),
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
    elif res == 'sunk':
        await callback.message.edit_text(
            text=await append_text(_user_bd, user_id, LEXICON['sunk'].format(_TEMP[y + 1] + str(x + 1))),
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
    elif res == 'miss':
        await callback.message.edit_text(
            text=await append_text(_user_bd, user_id, LEXICON['miss'].format(_TEMP[y + 1] + str(x + 1))),
            reply_markup=create_comp_kb(pole.get_pole(), 'pole_comp')
        )
        await asyncio.sleep(1)
        await comp_atack(callback=callback, _user_bd=_user_bd, user_id=user_id)

    elif res == 'victory':
        await callback.message.edit_text(
            text=f"{LEXICON['victory']: ^40}"
        )


@user_router.callback_query(UsersCallbackFactory.filter())
async def get_callback_userbutton(callback: CallbackQuery, _user_bd: list[UserBD], user_id: int):
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
    await asyncio.sleep(1)
    pole = _user_bd[user_id].user_pole
    await callback.message.edit_text(
        text=await append_text(_user_bd, user_id, LEXICON['hit_comp']),
        reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
    )

    y, x, res = _user_bd[user_id].user_pole.random_hit()

    while res in ('sunk', 'hit'):
        await asyncio.sleep(1)
        pole = _user_bd[user_id].user_pole
        if res == 'hit':
            await callback.message.edit_text(
                text=await append_text(_user_bd, user_id, LEXICON['luck_com_attak'].format(_TEMP[y + 1] + str(x + 1))),
                reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
            )
        else:
            await callback.message.edit_text(
                text=await append_text(_user_bd, user_id, LEXICON['sunk_com_attak'].format(_TEMP[y + 1] + str(x + 1))),
                reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
            )
        res = _user_bd[user_id].user_pole.random_hit()
    if res == 'victory':
        await asyncio.sleep(1)
        await callback.message.edit_text(
            text=await append_text(_user_bd, user_id,LEXICON['lose']),
        )
    else:
        await asyncio.sleep(1)
        await callback.message.edit_text(
            text=await append_text(_user_bd, user_id, LEXICON['miss_comp'].format(_TEMP[y + 1] + str(x + 1))),
            reply_markup=create_user_kb(pole.get_pole(), 'pole_comp')
        )


async def append_text(_user_bd: list[UserBD], user_id: int, text)-> str:
    if text:
        _user_bd[user_id].chat.append(text)
    return '\n\n'.join(_user_bd[user_id].chat)

