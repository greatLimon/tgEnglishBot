from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.handlers import get_message

NEXT_MESSAGE = get_message('next_message')
ADD_WORD_MESSAGE = get_message('add_word_message')
DELETE_WORD_MESSAGE = get_message('delete_word_message')
REGISTER_MESSAGE = get_message('register_message')

async def game_keyboard(word1:str, word2:str, word3:str, word4:str):
    game_board = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text= word1, callback_data= '1')],
        [InlineKeyboardButton(text= word2, callback_data= '2')],
        [InlineKeyboardButton(text= word3, callback_data= '3')],
        [InlineKeyboardButton(text= word4, callback_data= '4')]
    ])
    return game_board

async def main_keyboard()->ReplyKeyboardMarkup:

    main = ReplyKeyboardMarkup(keyboard=[
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