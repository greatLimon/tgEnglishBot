import asyncio
from aiogram import Dispatcher, types
from aiogram.filters.command import Command

from app.bot.Bot import Tg_bot

dp = Dispatcher()

async def _main_start_polling(bot)->None:
    await dp.start_polling(bot)


def start()->None:
    tg_bot = Tg_bot()
    asyncio.run(_main_start_polling(tg_bot.bot))

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('start_text')
    
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    await message.answer('next_text')