import random
import asyncio
from aiogram import types, F, Router
from aiogram.filters.command import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db.requests import get_user_by_id, add_user, add_users_word, get_userwords, delete_word_from_db
import bot.keyboards as kb
import bot.messages as msg

router = Router()

class User():
    def __init__(self, user_id:int):
        self.user_id = user_id
        
    async def play_next(self):
        self.word_indexes = await self.generate_word()
        self.right_word_index = random.choice(self.word_indexes)

    async def generate_word(self):
        index_list = [n for n in range(len(self.user_words))]
        result_list = list()
        for _ in range(4):
            index = random.choice(index_list)
            result_list.append(index)
            index_list.remove(index)
        return result_list
    
    async def update_words(self):
        self.user_words = await get_userwords(self.user_id)
        await self.play_next()

class UserStatus(StatesGroup):
    playing = State()
    add_ru = State()
    add_en = State()
    delete_sure = State()
    delete_ru = State()
    delete_en = State()
    register = State()
        
@router.message(Command('start'))
async def cmd_start(message: types.Message, state:FSMContext):
    if not await get_user_by_id(message.chat.id):
        await state.set_state(UserStatus.register)
        await message.answer(msg.START_MESSAGE, reply_markup=await kb.register_keyboard(REGISTER_MESSAGE = msg.REGISTER_MESSAGE))
    else:
        user = User(message.chat.id)
        await user.update_words()
        await state.set_state(UserStatus.playing)
        await state.update_data(user = user)
        await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                            reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                user.user_words[user.word_indexes[1]][1],
                                                                user.user_words[user.word_indexes[2]][1],
                                                                user.user_words[user.word_indexes[3]][1],
                                                                NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE
                                                                ))
    
@router.message(UserStatus.register, F.text == msg.REGISTER_MESSAGE)
async def cmd_next(message: types.Message, state:FSMContext):
    await add_user(message.chat.id, message.chat.full_name)
    await state.set_state(UserStatus.playing)
    user = User(message.chat.id)
    await user.update_words()
    await state.update_data(user = user)
    await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                         reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                             user.user_words[user.word_indexes[1]][1],
                                                             user.user_words[user.word_indexes[2]][1],
                                                             user.user_words[user.word_indexes[3]][1],
                                                                NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))
   
@router.message(UserStatus.playing, F.text != msg.NEXT_MESSAGE, F.text != msg.ADD_WORD_MESSAGE, F.text != msg.DELETE_WORD_MESSAGE)
async def check_word(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    if message.text == user.user_words[user.right_word_index][1]:
        await user.play_next()
        await state.set_state(UserStatus.playing)
        await state.update_data(user = user)
        await message.reply(msg.CORRECT_ANSWER)
        await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1],
                                                                 NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                 ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                 DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))
    else:
        await state.set_state(UserStatus.playing)
        await state.update_data(user = user)
        await message.reply(msg.INCORRECT_MESSAGE)
        await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1],
                                                                 NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                 ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                 DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))

@router.message(UserStatus.playing, F.text == msg.NEXT_MESSAGE)
async def check_word(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    await user.play_next()
    await state.set_state(UserStatus.playing)
    await state.update_data(user = user)
    await message.reply(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                    user.user_words[user.word_indexes[1]][1],
                                                                    user.user_words[user.word_indexes[2]][1],
                                                                    user.user_words[user.word_indexes[3]][1],
                                                                    NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                    ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                    DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))

@router.message(UserStatus.playing, F.text == msg.ADD_WORD_MESSAGE)
async def add_word(message:types.Message, state:FSMContext):
    await state.set_state(UserStatus.add_ru)
    await message.answer(msg.ENTER_WORD_RU, reply_markup=await kb.none_keyboard())

@router.message(UserStatus.add_ru)
async def add_word1(message:types.Message, state:FSMContext):
    await state.update_data(word_ru = message.text)
    await state.set_state(UserStatus.add_en)
    await message.answer(msg.ENTER_WORD_EN,reply_markup=await kb.none_keyboard())

@router.message(UserStatus.add_en)
async def add_word2(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    word_ru = data['word_ru']
    word_en = message.text
    await add_users_word(word_ru, word_en, user.user_id)
    await message.reply(msg.ENTER_WORD_END,reply_markup=await kb.none_keyboard())
    await user.update_words()
    await state.set_state(UserStatus.playing)
    await state.update_data(user = user)
    await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1],
                                                                NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))


@router.message(UserStatus.playing, F.text == msg.DELETE_WORD_MESSAGE)
async def delete_word(message:types.Message, state:FSMContext):
    await state.set_state(UserStatus.delete_ru)
    await message.answer(msg.DELETE_WORD_RU,reply_markup=await kb.none_keyboard())

@router.message(UserStatus.delete_ru)
async def delete_word1(message:types.Message, state:FSMContext):
    await state.update_data(word_ru = message.text)
    await state.set_state(UserStatus.delete_en)
    await message.answer(msg.DELETE_WORD_EN,reply_markup=await kb.none_keyboard())

@router.message(UserStatus.delete_en)
async def delete_word2(message:types.Message, state:FSMContext):
    # check does word exist
    data = await state.get_data()
    user = data['user']
    word_to_delete_ru = data['word_ru']
    word_to_delete_en = message.text
    if not (word_to_delete_ru, word_to_delete_en) in user.user_words:
        await state.set_state(UserStatus.playing)
        await message.answer(msg.DELETE_WORD_CANCEL)
    # if exist
    else:        
        await state.update_data(word_en = message.text)
        await state.set_state(UserStatus.delete_sure)
        await message.answer(msg.DELETE_WORD_SURE,reply_markup=await kb.yes_no_keyboard(YES_BUTTON=msg.YES_BUTTON, NO_BUTTON=msg.NO_BUTTON))

@router.message(UserStatus.delete_sure)
async def delete_word_sure(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user = data['user']
    word_to_delete_ru = data['word_ru']
    word_to_delete_en = data['word_en']
    await state.set_state(UserStatus.playing)
    if message.text == msg.YES_BUTTON:
        # update db
        if await delete_word_from_db(word_to_delete_ru, word_to_delete_en, user.user_id):
            await user.update_words()
            await state.update_data(user = user)
            await message.reply(msg.DELETE_WORD_END)
            await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                                 reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                     user.user_words[user.word_indexes[1]][1],
                                                                     user.user_words[user.word_indexes[2]][1],
                                                                     user.user_words[user.word_indexes[3]][1],
                                                                    NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                    ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                    DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))
        else:
            await message.reply(msg.DELETE_WORD_CANCEL)
            await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                                 reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                     user.user_words[user.word_indexes[1]][1],
                                                                     user.user_words[user.word_indexes[2]][1],
                                                                     user.user_words[user.word_indexes[3]][1],
                                                                    NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                    ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                    DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))
        
    else:
        await message.reply(msg.DELETE_WORD_CANCEL)
        await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                             reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                 user.user_words[user.word_indexes[1]][1],
                                                                 user.user_words[user.word_indexes[2]][1],
                                                                 user.user_words[user.word_indexes[3]][1],
                                                                    NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                    ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                    DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))
        
@router.message()
async def any_msg(message:types.Message, state:FSMContext):
    if not await get_user_by_id(message.chat.id):
        await message.answer('Use /start')
    else:
        user = User(message.chat.id)
        await user.update_words()
        await state.set_state(UserStatus.playing)
        await state.update_data(user = user)
        await message.answer(msg.GAME_MESSAGE + f' {user.user_words[user.right_word_index][0]}', 
                            reply_markup=await kb.main_keyboard(user.user_words[user.word_indexes[0]][1],
                                                                user.user_words[user.word_indexes[1]][1],
                                                                user.user_words[user.word_indexes[2]][1],
                                                                user.user_words[user.word_indexes[3]][1],
                                                                NEXT_MESSAGE=msg.NEXT_MESSAGE,
                                                                ADD_WORD_MESSAGE=msg.ADD_WORD_MESSAGE,
                                                                DELETE_WORD_MESSAGE=msg.DELETE_WORD_MESSAGE))