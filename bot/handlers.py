import os
from dotenv import load_dotenv

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.token import TokenValidationError

def _input_token()->str:
    token = input('Insert token from BotFather: ')
    with open('conf.env', 'w') as f:
        f.write(f"token = '{token}'")
    return token

def _load_token()->str:
    load_dotenv('conf.env')
    return os.getenv('token')

def _create_bot_class(token:str, error:bool = False)->Bot:
    try:
        bot = Bot(token=token)
        return bot
    except TokenValidationError:
        print('Token is incorrect!')
        if not error:
            tkn = _input_token()
            bot =  _create_bot_class(tkn, True)
            return bot
        return None

token = _load_token()
if token == '':
    token = _input_token()
# BOT
logging.basicConfig(level=logging.INFO)
bot = _create_bot_class(token)
if bot == None:
    exit()     
dp = Dispatcher()
    
async def _main_start_polling():
    await dp.start_polling(bot)

def start():
    asyncio.run(_main_start_polling())

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('start_text')
    
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    await message.answer('next_text')