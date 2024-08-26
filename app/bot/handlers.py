from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.token import TokenValidationError

import app.db.handlers as req
import app.bot.keyboards as kb
from app.config import read_env, input_token


dp = Dispatcher()

async def start_bot()->None:
    try:
        bot = Bot(token=read_env('token'))
    except TokenValidationError:
        try: 
            bot = Bot(token = input_token())
        except TokenValidationError:
            print('This token is invalid!')
            return None
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot is ready!')
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(await req.get_message('start_message'), reply_markup=kb.register)
    
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    await message.answer('next_text')