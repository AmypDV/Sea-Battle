from aiogram.handlers import message
from aiogram import Router
from aiogram.types import Message

other_router = Router()

@other_router.message()
async def other_handler(message: Message):
    await message.answer(f'Это эхо! {message.text}')

