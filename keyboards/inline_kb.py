from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_ru import LEXICON

_TEMP = dict(zip(range(1,11), 'АБВГДЕЖЗИК'))

class UsersCallbackFactory(CallbackData, prefix='user'):
    x: str
    y: int

def create_user_kb(lst: list
                   ) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Создаем кнопки
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=_TEMP[x + 1]+str(y + 1) if lst[x][y] == 0 else '🟫',
            callback_data='user'+str(x)+str(y)
        )
        for y in range(len(lst))
        for x in range(len(lst[0]))
    ]
    width = len(lst)
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['random'],
            callback_data='random'
        ),
        InlineKeyboardButton(
            text=LEXICON['start_game'],
            callback_data='start_game'
        ),
        width=1
    )

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=lexicon_ru[button] if button in lexicon_ru else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()