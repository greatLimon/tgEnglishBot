import os
import json
import asyncio
from aiogram import Bot, Dispatcher, exceptions
from aiogram.utils.token import TokenValidationError
from config import read_env, input_token

async def get_default_values()->dict:
    with open('db/default_values.json', 'r') as f:
        data = json.load(f)
    return data

async def start_db():
    from db.models import create_tables
    from db.requests import fill_default_values
    await create_tables()
    if os.path.exists('db/default_values.json'):
        await fill_default_values(await get_default_values())
        os.remove('db/default_values.json')

async def start_bot():
    from bot.messages import _upload_constants
    await _upload_constants()
    from bot.handlers import router
    try:
        bot = Bot(token=read_env('token'))
    except TokenValidationError:
        try: 
            bot = Bot(token = input_token())
        except TokenValidationError:
            print('This token is invalid!')
            return None
    try:
        await bot.delete_webhook(drop_pending_updates=True)#aiogram.exceptions.TelegramNetworkError
    except exceptions.TelegramNetworkError:
        print('Coonections error! Check Internet!')
        return None
    print('Bot is ready!')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

async def main():
    await start_db()
    await start_bot()


if __name__ == '__main__':
    asyncio.run(main())