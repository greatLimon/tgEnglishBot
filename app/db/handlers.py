import sqlalchemy as sq
from app.db.models import recreate_tables, create_tables, Users, Words, Messages, UsersWords, Session
import psycopg2


def start_db():
    create_tables()

def get_message(message:str) -> str:
    q = Session.query(Messages).filter(Messages.id == message).all()
    if len(q) > 0:
        return q[0].text
    else: return message

async def get_user_async(user_id:int)->int:
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

def get_user(user_id:int)->int:
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