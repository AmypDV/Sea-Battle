from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command

from lexicon.lexicon_ru import LEXICON
from datebase.datebase import users_bd, write_to_bd, UserBD
from services.services import BOOK
from keyboards.pagination_kb import create_pagination_kb
from keyboards.keyboards import create_bookmarks_kb, change_bookmarks_kb
from filters.filters import IsDigitCallbackData, IsBookmarksCallbackData, IsDelBookmarkCallbackData

user_router = Router()

@user_router.message(CommandStart())
async def get_start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users_bd:
        users_bd[user_id] = UserBD()
        write_to_bd()
    await message.answer(text=LEXICON['/start'])

@user_router.message(Command(commands='help'))
async def get_command_help(message: Message):
    await message.answer(text=LEXICON['/help'])

@user_router.message(Command(commands='beginning'))
async def get_command_help(message: Message):
    user_id = message.from_user.id
    users_bd[user_id].page = 1
    page = users_bd[user_id].page
    text = BOOK[page]
    write_to_bd()
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'forward',
            f'{page}/{len(BOOK)}',
            'backward',
        )
    )

@user_router.message(Command(commands='continue'))
async def get_command_help(message: Message):
    user_id = message.from_user.id
    page = users_bd[user_id].page
    text = BOOK[page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'forward',
            f'{page}/{len(BOOK)}',
            'backward',
        )
    )

@user_router.message(Command(commands='bookmarks'))
async def get_command_help(message: Message):
    user_id = message.from_user.id
    bookmarks = users_bd[user_id].bookmarks
    if bookmarks:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_kb(*bookmarks)
        )
    else:
        await message.answer(
            text=LEXICON['no_bookmarks']
        )

@user_router.callback_query(F.data == 'edit_bookmarks')
async def change_bookmarks(callback:CallbackQuery):
    user_id = callback.from_user.id
    bookmarks = users_bd[user_id].bookmarks
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=change_bookmarks_kb(*bookmarks)
    )

@user_router.callback_query(F.data == 'forward')
async def get_callback_forward(callback: CallbackQuery):
    user_id = callback.from_user.id
    len_book = len(BOOK)
    if users_bd[user_id].page < len_book:
        users_bd[user_id].page += 1
        page = users_bd[user_id].page
        text = BOOK[page]
        write_to_bd()
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'forward',
                f'{page}/{len(BOOK)}',
                'backward',
            )
        )
    else:
        await callback.answer()


@user_router.callback_query(F.data == 'backward')
async def get_callback_backward(callback: CallbackQuery):
    user_id = callback.from_user.id
    if users_bd[user_id].page > 1:
        users_bd[user_id].page -= 1
        page = users_bd[user_id].page
        text = BOOK[page]
        write_to_bd()
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'forward',
                f'{page}/{len(BOOK)}',
                'backward',
            )
        )
    else:
        await callback.answer()

@user_router.callback_query(IsBookmarksCallbackData())
async def get_callback_backward(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = users_bd[user_id].page
    users_bd[user_id].bookmarks.add(page)
    write_to_bd()
    await callback.answer(
        text=LEXICON['add_bookmarks']
    )

@user_router.callback_query(IsDigitCallbackData())
async def open_bookmarks(callback: CallbackQuery):
    page = callback.data
    user_id = callback.from_user.id
    users_bd[user_id].page = int(page)
    write_to_bd()
    await callback.message.edit_text(
        text=BOOK[int(page)],
        reply_markup=create_pagination_kb(
                'forward',
                f'{page}/{len(BOOK)}',
                'backward',
        )
    )


@user_router.callback_query(IsDelBookmarkCallbackData())
async def open_bookmarks(callback: CallbackQuery):
    page = int(callback.data[:-3])
    user_id = callback.from_user.id
    users_bd[user_id].bookmarks.remove(page)
    write_to_bd()
    if users_bd[user_id].bookmarks:
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=change_bookmarks_kb(*users_bd[user_id].bookmarks)
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['no_bookmarks']
        )

@user_router.callback_query(F.data == 'cancel_bookmarks')
async def get_cansel_bookmarks_command(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = users_bd[user_id].page
    text = BOOK[page]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            'forward',
            f'{page}/{len(BOOK)}',
            'backward',
        )
    )

@user_router.callback_query(F.data == 'cancel_edit_bookmarks')
async def get_cansel_edit_bookmarks(callback: CallbackQuery):
    user_id = callback.from_user.id
    bookmarks = users_bd[user_id].bookmarks
    await callback.message.edit_text(
        text=LEXICON['/bookmarks'],
        reply_markup=create_bookmarks_kb(*bookmarks)
    )