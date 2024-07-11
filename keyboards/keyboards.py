from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON



# Функция для формирования инлайн-клавиатуры на лету
def create_bookmarks_kb(*args: int) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in sorted(args):
            buttons.append(
                InlineKeyboardButton(
                    text=f'{button}',
                    callback_data=str(button)
                )
            )

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)

    #Добавляем в клавиатуру 2 кнопки: редактировать и отменить
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel_bookmarks'
        )
    )

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()



