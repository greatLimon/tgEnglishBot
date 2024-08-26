from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.db.handlers import get_message

async def main_keyboard(user_id:str):

    main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = '1'), KeyboardButton(text = '2')],
        [KeyboardButton(text = '3'), KeyboardButton(text = '4')],
        [KeyboardButton(text = await get_message('next')), KeyboardButton(text = 'add_word')],
        [KeyboardButton(text = 'delete_word')]
        ])

register = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'register')]
])