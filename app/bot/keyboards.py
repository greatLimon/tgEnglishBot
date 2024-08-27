from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.db.handlers import get_message

NEXT_MESSAGE = get_message('next_message')
ADD_WORD_MESSAGE = get_message('add_word_message')
DELETE_WORD_MESSAGE = get_message('delete_word_message')
REGISTER_MESSAGE = get_message('register_message')
YES_BUTTON = get_message('yes_button')
NO_BUTTON = get_message('no_button')

yes_no_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = YES_BUTTON), KeyboardButton(text= NO_BUTTON)]
], resize_keyboard= True)

async def main_keyboard(word1:str, word2:str, word3:str, word4:str)->ReplyKeyboardMarkup:
    main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = word1), KeyboardButton(text = word2)],
        [KeyboardButton(text = word3), KeyboardButton(text = word4)],
        [KeyboardButton(text = NEXT_MESSAGE ), KeyboardButton(text = ADD_WORD_MESSAGE )],
        [KeyboardButton(text = DELETE_WORD_MESSAGE )]
        ], resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...')
    return main

async def register_keyboard()->ReplyKeyboardMarkup:
    register = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = REGISTER_MESSAGE)]
        ],
        resize_keyboard=True, input_field_placeholder='Нажмите кнопку...')
    return register