import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.token import TokenValidationError
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.db.handlers import get_message, get_user_words, create_user, get_user_async
import app.bot.keyboards as kb
from app.config import read_env, input_token


dp = Dispatcher()


START_MESSAGE = get_message('start_message')
GAME_MESSAGE = get_message('game_message')
MENU_MESSAGE = get_message('menu_message')

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

class User():
    def __init__(self, user_id:int):
        self.user_id = user_id
        self.user_words = get_user_words(user_id)

class Game(StatesGroup):
    playing = State()
    check = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=await kb.register_keyboard())
    
async def generate_word(user:User):
    index_list = [n for n in range(len(user.user_words))]
    result_list = list()
    for _ in range(4):
        index = random.choice(index_list)
        result_list.append(index)
        index_list.remove(index)
    return result_list

@dp.message(F.text == kb.REGISTER_MESSAGE)
async def cmd_next(message: types.Message, state:FSMContext):
    if await get_user_async(message.chat.id) == None:
        await create_user(message.chat.id, message.chat.full_name)
    await state.set_state(Game.playing)
    user = User(message.chat.id)
    word_indexes = await generate_word(user)
    right_word_index = random.choice(word_indexes)
    await message.answer(MENU_MESSAGE, reply_markup=await kb.main_keyboard())
    await message.answer(GAME_MESSAGE + ' '+user.user_words[right_word_index][0], reply_markup=await kb.game_keyboard(user.user_words[word_indexes[0]][1],
                                                                                                                  user.user_words[word_indexes[1]][1],
                                                                                                                  user.user_words[word_indexes[2]][1],
                                                                                                                  user.user_words[word_indexes[3]][1]
                                                                                                                  ))