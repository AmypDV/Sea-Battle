from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_ru import LEXICON

_TEMP = dict(zip(range(1,11), 'АБВГДЕЖЗИК'))

class UsersCallbackFactory(CallbackData, prefix='user'):
    x: int
    y: int

class CompsCallbackFactory(CallbackData, prefix='comp'):
    x: int
    y: int

def create_user_kb(
        lst: list,
        *args: str
                   ) -> InlineKeyboardMarkup:
    '''
    :return: возвращает клавиатуру с флотом игрока
    '''
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Создаем кнопки
    buttons = []
    for y in range(len(lst)):
        for x in range(len(lst[0])):
            buttons.append(InlineKeyboardButton(
                text=_TEMP[y + 1] + str(x + 1) if lst[y][x] == 0 else '🟫' if lst[y][x] == 1 else '🟥',
                callback_data=UsersCallbackFactory(
                    x=x,
                    y=y,
                ).pack()
            ))
    width = len(lst)
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    if args:
        for button in args:
            kb_builder.row(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_comp_kb(
        lst: list,
        *args: str
                   ) -> InlineKeyboardMarkup:
    '''
    :return: возвращает клавиатуру с флотом компьютера
    '''
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Создаем кнопки
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=_TEMP[y + 1]+str(x + 1) if lst[y][x] in (0, 1) else '🌊' if lst[y][x] == 3 else '🟥',
            callback_data=CompsCallbackFactory(
                x=x,
                y=y,
            ).pack()
        )
        for y in range(len(lst))
        for x in range(len(lst[0]))
    ]
    width = len(lst)
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    if args:
        for button in args:
            kb_builder.row(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()