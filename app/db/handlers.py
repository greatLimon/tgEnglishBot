import sqlalchemy as sq
from app.db.models import recreate_tables, create_tables, Users, Words, Messages, UsersWords, Session
import psycopg2


def start_db():
    create_tables()

async def get_message(message:str) -> str:
    q = Session.query(Messages).filter(Messages.id == message).all()
    if len(q) > 0:
        return q[0].text
    else: return message

async def get_user(user_id:str)->bool:
    q = Session.query(Users).filter(Users.name == user_id).all()
    if len(q) == 0:
        return False
    else: return True

async def create_user(user_id:str)->bool:
    Session.add(Users(name = user_id))
    for n in range(4):
        Session.add(UsersWords(user_id = user_id, word_id = n+1))
    try:
        Session.commit()
        return True
    except:
        return False
