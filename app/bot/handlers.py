from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

dp = Dispatcher()

async def start_pooling(bot)->None:
    await dp.start_polling(bot)

def get_bot(token:str)->None:
    return Bot(token = token)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('start_text')
    
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    await message.answer('next_text')