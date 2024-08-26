from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import app.db.handlers as req

dp = Dispatcher()
db = None

async def start_pooling(bot, session)->None:
    global db
    db = session
    print('Bot is ready!')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def get_bot(token:str)->None:
    return Bot(token = token)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(await req.get_message('start_message', db))
    
@dp.message(Command('next'))
async def cmd_next(message: types.Message):
    await message.answer('next_text')