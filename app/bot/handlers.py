import random
from aiogram import Bot, Dispatcher, types, F, exceptions
from aiogram.filters.command import Command
from aiogram.utils.token import TokenValidationError
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.db.handlers import get_message, get_user_words, create_user, get_user_async, add_word_to_DB, delete_word_from_DB
import app.bot.keyboards as kb
from app.config import read_env, input_token


dp = Dispatcher()


START_MESSAGE = get_message('start_message')
GAME_MESSAGE = get_message('game_message')
MENU_MESSAGE = get_message('menu_message')
CORRECT_ANSWER = get_message('correct_answer')
INCORRECT_MESSAGE = get_message('incorrect_message')
ENTER_WORD_RU = get_message('enter_word_ru')
ENTER_WORD_EN = get_message('enter_word_en')
ENTER_WORD_END = get_message('enter_word_end')
DELETE_WORD_RU = get_message('delete_word_ru')
DELETE_WORD_EN = get_message('delete_word_en')
DELETE_WORD_END = get_message('delete_word_end')
DELETE_WORD_SURE = get_message('delete_word_sure')
DELETE_WORD_END = get_message('delete_word_end')
DELETE_WORD_CANCEL = get_message('delete_word_cancel')

async def start_bot()->None:
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
    await dp.start_polling(bot)

class User():
    def __init__(self, user_id:int):
        self.user_id = user_id
        self.user_words = get_user_words(user_id)
        self.word_indexes = self.generate_word()
        self.right_word_index = random.choice(self.word_indexes)
    
    def play_next(self):
        self.word_indexes = self.generate_word()
        self.right_word_index = random.choice(self.word_indexes)

    def generate_word(self):
        index_list = [n for n in range(len(self.user_words))]
        result_list = list()
        for _ in range(4):
            index = random.choice(index_list)
            result_list.append(index)
            index_list.remove(index)
        return result_list
    
    def update_words(self):
        self.user_words = get_user_words(self.user_id)

class Game(StatesGroup):
    playing = State()
    add_ru = State()
    add_en = State()
    delete_sure = State()
    delete_ru = State()
    delete_en = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=await kb.register_keyboard())
    
@dp.message(F.text == kb.REGISTER_MESSAGE)
async def cmd_next(message: types.Message, state:FSMContext):
    if await get_user_async(message.chat.id) == None:
        await create_user(message.chat.id, message.chat.full_name)
    await state.set_state(Game.playing)
    user = User(message.chat.id)
    await state.update_data(user = user)
    await message.answer(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                         reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                             user.user_words[user.word_indexes[1]][1],
                                                             user.user_words[user.word_indexes[2]][1],
                                                             user.user_words[user.word_indexes[3]][1])
                                                             )
   
@dp.message(Game.playing, F.text != kb.NEXT_MESSAGE, F.text != kb.ADD_WORD_MESSAGE, F.text != kb.DELETE_WORD_MESSAGE)
async def check_word(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    if message.text == user.user_words[user.right_word_index][1]:
        user.play_next()
        await state.set_state(Game.playing)
        await state.update_data(user = user)
        await message.reply(CORRECT_ANSWER + f' {user.user_words[user.right_word_index][0]}', reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                           user.user_words[user.word_indexes[1]][1],
                                                                           user.user_words[user.word_indexes[2]][1],
                                                                           user.user_words[user.word_indexes[3]][1]))
    else:
        await state.set_state(Game.playing)
        await state.update_data(user = user)
        await message.reply(INCORRECT_MESSAGE)
        await message.answer(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1])
                                                                 )

@dp.message(Game.playing, F.text == kb.NEXT_MESSAGE)
async def check_word(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    user.play_next()
    await state.set_state(Game.playing)
    await state.update_data(user = user)
    await message.reply(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                       user.user_words[user.word_indexes[1]][1],
                                                                       user.user_words[user.word_indexes[2]][1],
                                                                       user.user_words[user.word_indexes[3]][1]))

@dp.message(Game.playing, F.text == kb.ADD_WORD_MESSAGE)
async def add_word(message:types.Message, state:FSMContext):
    await state.set_state(Game.add_ru)
    await message.answer(ENTER_WORD_RU, reply_markup=None)

@dp.message(Game.add_ru)
async def add_word1(message:types.Message, state:FSMContext):
    await state.update_data(word_ru = message.text)
    await state.set_state(Game.add_en)
    await message.answer(ENTER_WORD_EN,reply_markup=None)

@dp.message(Game.add_en)
async def add_word2(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    word_ru = data['word_ru']
    word_en = message.text
    await add_word_to_DB(word_ru, word_en, user.user_id)
    await message.reply(ENTER_WORD_END,reply_markup=None)
    user.update_words()
    user.play_next()
    await state.set_state(Game.playing)
    await state.update_data(user = user)
    await message.answer(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1])
                                                                 )


@dp.message(Game.playing, F.text == kb.DELETE_WORD_MESSAGE)
async def delete_word(message:types.Message, state:FSMContext):
    await state.set_state(Game.delete_ru)
    await message.answer(DELETE_WORD_RU,reply_markup=None)

@dp.message(Game.delete_ru)
async def delete_word1(message:types.Message, state:FSMContext):
    await state.update_data(word_ru = message.text)
    await state.set_state(Game.delete_en)
    await message.answer(DELETE_WORD_EN,reply_markup=None)

@dp.message(Game.delete_en)
async def delete_word2(message:types.Message, state:FSMContext):
    # check does word exist
    data = await state.get_data()
    user = data['user']
    word_to_delete_ru = data['word_ru']
    word_to_delete_en = message.text
    if not (word_to_delete_ru, word_to_delete_en) in user.user_words:
        await state.set_state(Game.playing)
        await message.answer(DELETE_WORD_CANCEL)
    # if exist
    else:
        # delete from DB
        await delete_word_from_DB(word_to_delete_ru, word_to_delete_en, user.user_id)
        await state.set_state(Game.delete_sure)
        await message.answer(DELETE_WORD_SURE,reply_markup=kb.yes_no_keyboard)

@dp.message(Game.delete_sure)
async def delete_word_sure(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data[user]
    await state.set_state(Game.playing)
    await state.update_data(user)
    if message.text == kb.YES_BUTTON:
        # update db
        
        await message.reply(DELETE_WORD_END)
        await message.reply(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                       user.user_words[user.word_indexes[1]][1],
                                                                       user.user_words[user.word_indexes[2]][1],
                                                                       user.user_words[user.word_indexes[3]][1]))
    else:
        await message.reply(DELETE_WORD_END)
        await message.reply(GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                       user.user_words[user.word_indexes[1]][1],
                                                                       user.user_words[user.word_indexes[2]][1],
                                                                       user.user_words[user.word_indexes[3]][1]))