from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def none_keyboard()->ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[])

async def yes_no_keyboard(YES_BUTTON:str, NO_BUTTON:str)->ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = YES_BUTTON), KeyboardButton(text= NO_BUTTON)]
    ], resize_keyboard= True)

async def main_keyboard(word1:str, word2:str, word3:str, word4:str, NEXT_MESSAGE:str, ADD_WORD_MESSAGE:str, DELETE_WORD_MESSAGE:str)->ReplyKeyboardMarkup:
    main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = word1), KeyboardButton(text = word2)],
        [KeyboardButton(text = word3), KeyboardButton(text = word4)],
        [KeyboardButton(text = NEXT_MESSAGE ), KeyboardButton(text = ADD_WORD_MESSAGE )],
        [KeyboardButton(text = DELETE_WORD_MESSAGE )]
        ], resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...')
    return main

async def register_keyboard(REGISTER_MESSAGE:str)->ReplyKeyboardMarkup:
    register = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = REGISTER_MESSAGE)]
        ],
        resize_keyboard=True, input_field_placeholder='Нажмите кнопку...')
    return register