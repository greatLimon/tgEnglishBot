import sqlalchemy as sq
from sqlalchemy.exc import ArgumentError
import psycopg2
from app.db.models import Users, Words, Messages, UsersWords, Session
from app.config import return_default_values

def start_db():
    answ = input('Fill DB default values?[y/n]: ')
    if answ.lower() == 'y':
        data = return_default_values()
        for words in data['Words']:
            create_words(words[1], words[0])
        for message_id, message in data['Messages'].items():
            create_messages(message_id, message)
        print('You need to restart program!')
    print('DB is active')

def get_message(message:str) -> str:
    try:
        q = Session.query(Messages).filter(Messages.id == message).all()
        if len(q) > 0:
            return q[0].text
        else: return message
    except:
        return message

async def get_user_async(user_id:int)->int|None:
    q = Session.query(Users).filter(Users.id == user_id).all()
    if len(q) == 0:
        return None
    else: return q[0].id

async def get_user_words_async(user_id:int)->list:
    q_user = await get_user(user_id)
    if not q_user == None: 
        q_users_words = Session.query(UsersWords).filter(UsersWords.user_id == q_user).all()
        words_list = list()
        for words in q_users_words:
            q_words = Session.query(Words).filter(Words.id == words.id).all()
            words_list.append((q_words[0].word_ru, q_words[0].word_en))
    return words_list

async def find_word(word_ru:str, word_en:str)->bool:
    q_exist = Session.query(Words).filter(Words.word_ru == word_ru, Words.word_en == word_en).all()
    if len(q_exist) == 0:
        return False
    else: return q_exist[0]

def get_user(user_id:int)->int|None:
    q = Session.query(Users).filter(Users.id == user_id).all()
    if len(q) == 0:
        return None
    else: return q[0].id

def get_user_words(user_id:int)->list:
    q_user = get_user(user_id)
    if not q_user == None: 
        q_users_words = Session.query(UsersWords).filter(UsersWords.user_id == q_user).all()
        words_list = list()
        for words in q_users_words:
            q_words = Session.query(Words).filter(Words.id == words.word_id).all()
            words_list.append((q_words[0].word_ru, q_words[0].word_en))
    return words_list

async def create_user(user_id:int, name:str)->bool:
    Session.add(Users(id = user_id, name = name))
    for n in range(4):
        Session.add(UsersWords(user_id = user_id, word_id = n+1))
    try:
        Session.commit()
        return True
    except:
        return False
    
def create_words(word_ru:str, word_en:str)->bool:
    Session.add(Words(word_ru = word_ru, word_en = word_en))
    Session.commit()

def create_messages(message_id:str, message:str)->bool:
    Session.add(Messages(id = message_id, text = message))
    Session.commit()

async def add_word_to_DB(word_ru:str, word_en:str, user_id:int)->bool:
    if await find_word(word_ru, word_en) == False:
        Session.add(Words(word_en = word_en, word_ru = word_ru))
    try:
        Session.commit()
    except:
        return False
    new_word = Session.query(Words).filter(Words.word_ru == word_ru, Words.word_en == word_en).all()
    Session.add(UsersWords(user_id = user_id, word_id = new_word[0].id))
    try:
        Session.commit()
        return True
    except:
        return False
    
async def delete_word_from_DB(word_ru:str, word_en:str, user_id:int)->bool:
    findest_word = find_word(word_en=word_en, word_ru=word_ru)
    check_user_words = Session.query(UsersWords).filter(UsersWords.word_id == findest_word.id)
    if len(check_user_words.all()) > 1:
        Session.query(UsersWords).filter(UsersWords.user_id == user_id, UsersWords.word_id == find_word.id).delete()
        Session.query(Words).filter(Words.id == findest_word.id)
    else:
        Session.query(UsersWords).filter(UsersWords.user_id == user_id, UsersWords.word_id == find_word.id).delete()
    try:
        Session.commit()
        return True
    except:
        return False
