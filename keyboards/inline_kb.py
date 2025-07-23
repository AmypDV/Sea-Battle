from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon_ru import LEXICON

_TEMP = dict(zip(range(1,11), 'АБВГДЕЖZИК'))

class UsersCallbackFactory(CallbackData, prefix='user'):
    x: int
    y: int

class CompsCallbackFactory(CallbackData, prefix='comp'):
    x: int
    y: int

def _create_name_buttom(lst:list, x:int, y:int, users_kb=True)->str:
    res = None
    if lst[y][x] == 0:
        res = _TEMP[y + 1]+str(x + 1)
    elif lst[y][x] == 1:
        res = '🟫' if users_kb else _TEMP[y + 1]+str(x + 1)
    elif lst[y][x] == 3:
        res = '🌊'
    elif lst[y][x] == 2:
        res = '🟥'
    elif lst[y][x] == 4:
        res = '⬛'
    return  res


def create_user_kb(
        lst: list,
        *args: str
                   ) -> InlineKeyboardMarkup:
    '''
    :return: возвращает клавиатуру с флотом игрока
    '''
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()


    kb_builder.row(InlineKeyboardButton(
        text=LEXICON['this_pole_user'],
        callback_data='this_pole_user')
    )

    # Создаем кнопки
    buttons = []
    for y in range(len(lst)):
        for x in range(len(lst[0])):
            buttons.append(InlineKeyboardButton(
                text=_create_name_buttom(lst=lst, x=x, y=y, users_kb=True),
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

    kb_builder.row(InlineKeyboardButton(
        text=LEXICON['this_pole_comp'],
        callback_data='this_pole_comp')
    )
    # Создаем кнопки
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=_create_name_buttom(lst=lst, x=x, y=y, users_kb=False), #_TEMP[y + 1]+str(x + 1) if lst[y][x] in (0, 1) else '🌊' if lst[y][x] == 3 else '🟥',
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