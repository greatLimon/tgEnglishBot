from db.requests import get_message

START_MESSAGE = None
GAME_MESSAGE = None
CORRECT_ANSWER = None
INCORRECT_MESSAGE = None
ENTER_WORD_RU = None
ENTER_WORD_EN = None
ENTER_WORD_END = None
DELETE_WORD_RU = None
DELETE_WORD_EN = None
DELETE_WORD_END = None
DELETE_WORD_SURE = None
DELETE_WORD_CANCEL = None
NEXT_MESSAGE = None
ADD_WORD_MESSAGE = None
DELETE_WORD_MESSAGE = None
REGISTER_MESSAGE = None
YES_BUTTON = None
NO_BUTTON = None

async def _upload_constants():
    global START_MESSAGE 
    global GAME_MESSAGE 
    global CORRECT_ANSWER 
    global INCORRECT_MESSAGE 
    global ENTER_WORD_RU 
    global ENTER_WORD_EN 
    global ENTER_WORD_END 
    global DELETE_WORD_RU 
    global DELETE_WORD_EN 
    global DELETE_WORD_END 
    global DELETE_WORD_SURE 
    global DELETE_WORD_CANCEL 
    global NEXT_MESSAGE 
    global ADD_WORD_MESSAGE 
    global DELETE_WORD_MESSAGE
    global REGISTER_MESSAGE
    global YES_BUTTON
    global NO_BUTTON

    START_MESSAGE = await get_message('start_message')
    GAME_MESSAGE = await get_message('game_message')
    CORRECT_ANSWER = await get_message('correct_answer')
    INCORRECT_MESSAGE = await get_message('incorrect_message')
    ENTER_WORD_RU = await get_message('enter_word_ru')
    ENTER_WORD_EN = await get_message('enter_word_en')
    ENTER_WORD_END = await get_message('enter_word_end')
    DELETE_WORD_RU = await get_message('delete_word_ru')
    DELETE_WORD_EN = await get_message('delete_word_en')
    DELETE_WORD_END = await get_message('delete_word_end')
    DELETE_WORD_SURE = await get_message('delete_word_sure')
    DELETE_WORD_CANCEL = await get_message('delete_word_cancel')
    NEXT_MESSAGE = await get_message('next_message')
    ADD_WORD_MESSAGE = await get_message('add_word_message')
    DELETE_WORD_MESSAGE = await get_message('delete_word_message')
    REGISTER_MESSAGE = await get_message('register_message')
    YES_BUTTON = await get_message('yes_button')
    NO_BUTTON = await get_message('no_button')